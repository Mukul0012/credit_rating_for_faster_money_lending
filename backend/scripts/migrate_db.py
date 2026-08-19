#!/usr/bin/env python3
"""
==============================================================================
Database Migration & Schema Sync Script
==============================================================================
Provides automated schema synchronization and database migration capabilities:
  - Verifies database connectivity and credentials.
  - Automatically creates missing tables from SQLAlchemy models.
  - Detects and applies missing column migrations (ALTER TABLE ADD COLUMN).
  - Detects and creates missing indexes.
  - Provides detailed schema inspection and status reports.
  - Supports database reset and optional seed population.

Usage:
  python scripts/migrate_db.py                  # Apply pending migrations & create missing tables
  python scripts/migrate_db.py --status         # Check database status and pending changes
  python scripts/migrate_db.py --seed           # Migrate schema and seed default/test data
  python scripts/migrate_db.py --reset          # Drop and recreate all tables
  python scripts/migrate_db.py --reset --force  # Force drop and recreate without prompt
==============================================================================
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Any

# Ensure backend root is on sys.path
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from sqlalchemy import inspect, text, Table, Column, Index
from app.core.database import engine, Base, SessionLocal
from app.core.config import settings
import app.models  # Ensure all models are registered with Base.metadata


# Terminal Color Helpers
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


def format_db_url(url: str) -> str:
    """Mask sensitive password in database URL for safe terminal display."""
    try:
        from urllib.parse import urlsplit, urlunsplit
        parsed = urlsplit(url)
        if parsed.password:
            netloc = f"{parsed.username}:****@{parsed.hostname}"
            if parsed.port:
                netloc += f":{parsed.port}"
            return urlunsplit((parsed.scheme, netloc, parsed.path, parsed.query, parsed.fragment))
    except Exception:
        pass
    return "Configured Database"


def check_db_connection() -> bool:
    """Check if the database is reachable."""
    print(f"{Colors.BLUE}[+] Checking database connection...{Colors.RESET}")
    print(f"    Target: {Colors.CYAN}{format_db_url(str(settings.DATABASE_URL))}{Colors.RESET}")
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(f"{Colors.GREEN}✓ Database connection successful.{Colors.RESET}\n")
        return True
    except Exception as e:
        print(f"{Colors.RED}✗ Failed to connect to database: {e}{Colors.RESET}")
        return False


def get_column_sql_type(column: Column, dialect) -> str:
    """Compile column SQL type definition for the active database dialect."""
    col_type = column.type.compile(dialect)
    return col_type


def inspect_schema_status() -> Dict[str, Any]:
    """
    Compare SQLAlchemy models with the live database.
    Returns details on existing tables, missing tables, missing columns, and missing indexes.
    """
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())
    model_tables = Base.metadata.tables

    missing_tables: List[str] = []
    missing_columns: Dict[str, List[Tuple[str, str]]] = {}
    synced_tables: Dict[str, Dict[str, Any]] = {}

    for table_name, table in model_tables.items():
        if table_name not in existing_tables:
            missing_tables.append(table_name)
        else:
            live_columns = {c["name"]: c for c in inspector.get_columns(table_name)}
            missing_cols = []
            for col in table.columns:
                if col.name not in live_columns:
                    col_type = get_column_sql_type(col, engine.dialect)
                    missing_cols.append((col.name, col_type))

            # Fetch row count
            try:
                with engine.connect() as conn:
                    result = conn.execute(text(f'SELECT COUNT(*) FROM "{table_name}"'))
                    row_count = result.scalar() or 0
            except Exception:
                row_count = 0

            synced_tables[table_name] = {
                "live_column_count": len(live_columns),
                "model_column_count": len(table.columns),
                "row_count": row_count,
                "missing_columns": missing_cols,
            }
            if missing_cols:
                missing_columns[table_name] = missing_cols

    return {
        "existing_tables": existing_tables,
        "model_tables": model_tables,
        "missing_tables": missing_tables,
        "missing_columns": missing_columns,
        "synced_tables": synced_tables,
    }


def show_status():
    """Print a clean status table of the current database state."""
    if not check_db_connection():
        return

    status = inspect_schema_status()
    print(f"{Colors.BOLD}{'=' * 75}{Colors.RESET}")
    print(f"{Colors.BOLD} DATABASE SCHEMA STATUS REPORT{Colors.RESET}")
    print(f"{Colors.BOLD}{'=' * 75}{Colors.RESET}")
    print(f"{'Table Name':<28} | {'Rows':<8} | {'Columns (Live/Model)':<22} | {'Status':<12}")
    print(f"{'-' * 28}-+-{'-' * 8}-+-{'-' * 22}-+-{'-' * 12}")

    for table_name, table in status["model_tables"].items():
        if table_name in status["missing_tables"]:
            status_text = f"{Colors.RED}MISSING{Colors.RESET}"
            print(f"{table_name:<28} | {'-':<8} | {f'0 / {len(table.columns)}':<22} | {status_text}")
        else:
            table_info = status["synced_tables"][table_name]
            live_cols = table_info["live_column_count"]
            model_cols = table_info["model_column_count"]
            missing_cols = table_info["missing_columns"]
            row_count = table_info["row_count"]

            if missing_cols:
                status_text = f"{Colors.YELLOW}OUT OF SYNC ({len(missing_cols)} col missing){Colors.RESET}"
            else:
                status_text = f"{Colors.GREEN}SYNCED{Colors.RESET}"

            print(f"{table_name:<28} | {row_count:<8} | {f'{live_cols} / {model_cols}':<22} | {status_text}")

            if missing_cols:
                for col_name, col_type in missing_cols:
                    print(f"  └─ Missing column: {Colors.YELLOW}+{col_name} ({col_type}){Colors.RESET}")

    print(f"{Colors.BOLD}{'=' * 75}{Colors.RESET}\n")

    if not status["missing_tables"] and not status["missing_columns"]:
        print(f"{Colors.GREEN}✓ All tables and columns are completely in sync with models!{Colors.RESET}")
    else:
        pending_count = len(status["missing_tables"]) + sum(len(cols) for cols in status["missing_columns"].values())
        print(f"{Colors.YELLOW}⚠ {pending_count} schema change(s) pending. Run `python scripts/migrate_db.py` to apply.{Colors.RESET}")


def apply_migrations() -> bool:
    """Apply schema migrations: creates missing tables and adds missing columns."""
    if not check_db_connection():
        return False

    print(f"{Colors.BOLD}{Colors.BLUE}[1/3] Detecting schema diffs...{Colors.RESET}")
    status = inspect_schema_status()

    # Step 1: Create missing tables
    if status["missing_tables"]:
        print(f"{Colors.YELLOW}-> Found {len(status['missing_tables'])} missing table(s): {', '.join(status['missing_tables'])}{Colors.RESET}")
        print(f"   Creating missing tables via SQLAlchemy metadata...")
        Base.metadata.create_all(bind=engine)
        print(f"{Colors.GREEN}✓ Created missing tables successfully.{Colors.RESET}")
    else:
        print(f"{Colors.GREEN}✓ All tables exist.{Colors.RESET}")

    # Re-inspect to check for missing columns in existing tables
    status = inspect_schema_status()
    missing_columns = status["missing_columns"]

    # Step 2: Add missing columns
    print(f"\n{Colors.BOLD}{Colors.BLUE}[2/3] Checking column consistency...{Colors.RESET}")
    if missing_columns:
        total_cols = sum(len(cols) for cols in missing_columns.values())
        print(f"{Colors.YELLOW}-> Applying {total_cols} missing column migration(s)...{Colors.RESET}")
        
        with engine.begin() as conn:
            for table_name, cols in missing_columns.items():
                for col_name, col_type in cols:
                    alter_sql = f'ALTER TABLE "{table_name}" ADD COLUMN "{col_name}" {col_type};'
                    print(f"   Executing: {Colors.CYAN}{alter_sql}{Colors.RESET}")
                    conn.execute(text(alter_sql))
                    print(f"   {Colors.GREEN}✓ Added column `{col_name}` to `{table_name}`{Colors.RESET}")
        print(f"{Colors.GREEN}✓ Column migrations applied successfully.{Colors.RESET}")
    else:
        print(f"{Colors.GREEN}✓ All columns are up-to-date.{Colors.RESET}")

    # Step 3: Check and create indexes
    print(f"\n{Colors.BOLD}{Colors.BLUE}[3/3] Checking table indexes...{Colors.RESET}")
    try:
        Base.metadata.create_all(bind=engine)
        print(f"{Colors.GREEN}✓ Indexes verified and up-to-date.{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.YELLOW}Note on index creation: {e}{Colors.RESET}")

    print(f"\n{Colors.BOLD}{Colors.GREEN}{'=' * 50}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}✓ Database migration completed successfully!{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'=' * 50}{Colors.RESET}\n")
    return True


def reset_database(force: bool = False):
    """Drop and recreate all database tables."""
    if not check_db_connection():
        return

    if not force:
        print(f"{Colors.RED}{Colors.BOLD}WARNING: This will DROP ALL TABLES and ERASE ALL DATA in the database!{Colors.RESET}")
        confirm = input(f"Are you sure you want to continue? (type 'yes' to confirm): ").strip().lower()
        if confirm != "yes":
            print(f"{Colors.YELLOW}Operation cancelled.{Colors.RESET}")
            return

    print(f"\n{Colors.RED}-> Dropping all database tables...{Colors.RESET}")
    Base.metadata.drop_all(bind=engine)
    print(f"{Colors.GREEN}✓ Dropped all tables.{Colors.RESET}")

    print(f"\n{Colors.BLUE}-> Re-creating all tables from metadata...{Colors.RESET}")
    Base.metadata.create_all(bind=engine)
    print(f"{Colors.GREEN}✓ Re-created all database tables.{Colors.RESET}\n")


def seed_data():
    """Trigger the train and seed data script."""
    print(f"\n{Colors.BLUE}[+] Running initial data seeding...{Colors.RESET}")
    try:
        from scripts.train_and_seed import seed_database
        seed_database()
        print(f"{Colors.GREEN}✓ Seeding completed successfully.{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}✗ Seeding encountered an error: {e}{Colors.RESET}")


def main():
    parser = argparse.ArgumentParser(
        description="Database Migration and Schema Management CLI for Credit Rating Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/migrate_db.py                  # Migrate schema (create missing tables & columns)
  python scripts/migrate_db.py --status         # View live schema status
  python scripts/migrate_db.py --seed           # Migrate schema and seed initial test accounts
  python scripts/migrate_db.py --reset --force  # Recreate database tables from scratch
        """
    )
    parser.add_argument(
        "--status", "--check",
        dest="status",
        action="store_true",
        help="Check and display current database schema status without applying changes"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop and recreate all tables in the database"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force dangerous operations (e.g., --reset) without interactive confirmation prompt"
    )
    parser.add_argument(
        "--seed",
        action="store_true",
        help="Run database seeding after migration"
    )

    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.reset:
        reset_database(force=args.force)
        if args.seed:
            seed_data()
    else:
        success = apply_migrations()
        if success and args.seed:
            seed_data()


if __name__ == "__main__":
    main()
