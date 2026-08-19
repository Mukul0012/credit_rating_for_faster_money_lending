import os
import sys
from datetime import date
from pathlib import Path
from decimal import Decimal

# Add backend root to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder

from app.core.database import engine, Base, SessionLocal
from app.core.security import hash_password
from app.models.applicant import Applicant
from app.models.employment import Employment
from app.models.application import Application
from app.models.credit_profile import CreditProfile
from app.models.credit_rating import CreditRating
from app.models.loan_request import LoanRequest
from app.models.debt_payment_metrics import DebtPaymentMetrics
from app.models.existing_loan import ExistingLoan
from app.models.loan_assessment import LoanAssessment
from app.models.user_account import UserAccount
from app.models.lender_account import LenderAccount


def train_model():
    print("-> Training Random Forest Model & Encoder...")
    raw_data_path = backend_dir / "Random-Forest-Classifier" / "data" / "raw" / "ml_training_dataset.csv"
    if not raw_data_path.exists():
        print(f"Error: Dataset not found at {raw_data_path}")
        return

    df = pd.read_csv(raw_data_path)

    categorical_cols = ["Employment_Type", "Loan_Purpose"]
    numerical_cols = [
        "Age",
        "Annual_Income",
        "Employment_Duration_Years",
        "Number_of_Dependents",
        "Loan_Amount",
        "Loan_Tenure_Months",
        "Existing_Loans_Count",
        "Total_Outstanding_Debt",
        "Existing_Monthly_EMI",
        "Debt_to_Income_Ratio",
        "Loan_to_Income_Ratio",
        "Credit_Utilization",
        "Previous_Defaults",
        "Missed_Payments",
        "Maximum_Days_Past_Due",
        "Recent_Credit_Enquiries",
        "Credit_History_Length",
        "Number_of_Credit_Accounts",
        "Payment_History",
        "Credit_Score"
    ]

    X = df[numerical_cols + categorical_cols]
    y = df["Decision"].map({"Reject": 0, "Approve": 1})

    # Fit encoder
    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    X_cat = encoder.fit_transform(X[categorical_cols])
    encoded_cols = encoder.get_feature_names_out(categorical_cols)
    X_cat_df = pd.DataFrame(X_cat, columns=encoded_cols, index=X.index)

    X_final = pd.concat([X[numerical_cols], X_cat_df], axis=1)

    # Train model
    model = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
    model.fit(X_final, y)

    # Ensure model directories exist
    app_models_dir = backend_dir / "app" / "ml" / "models"
    rf_models_dir = backend_dir / "Random-Forest-Classifier" / "models"
    app_models_dir.mkdir(parents=True, exist_ok=True)
    rf_models_dir.mkdir(parents=True, exist_ok=True)

    # Save to both destinations
    joblib.dump(encoder, app_models_dir / "encoder.pkl")
    joblib.dump(model, app_models_dir / "random_forest_tuned.pkl")

    joblib.dump(encoder, rf_models_dir / "encoder.pkl")
    joblib.dump(model, rf_models_dir / "random_forest_tuned.pkl")
    joblib.dump(model, rf_models_dir / "random_forest_baseline.pkl")

    print(f"✓ Model and Encoder successfully saved to {app_models_dir}")


def seed_database():
    print("-> Creating tables and seeding initial database...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # 1. Seed Lender Account
        existing_lender = db.query(LenderAccount).filter(LenderAccount.email == "underwriter@bank.com").first()
        if not existing_lender:
            lender = LenderAccount(
                email="underwriter@bank.com",
                password_hash=hash_password("password123"),
                full_name="Sarah Jenkins (Senior Underwriter)",
                is_active=True
            )
            db.add(lender)
            db.commit()
            print("✓ Seeded Lender Account: underwriter@bank.com / password123")
        else:
            print("✓ Lender Account already exists.")

        # 2. Seed Applicant Aarav Sharma
        existing_applicant = db.query(Applicant).filter(Applicant.email == "applicant@example.com").first()
        if not existing_applicant:
            applicant1 = Applicant(
                full_name="Aarav Sharma",
                date_of_birth=date(1995, 6, 15),
                age=31,
                gender="Male",
                pan="ABCDE1234F",
                aadhaar_number="123456789012",
                address="402, Skyline Residency, Bandra West, Mumbai",
                phone_number="+91 98765 43210",
                email="applicant@example.com"
            )
            db.add(applicant1)
            db.commit()
            db.refresh(applicant1)

            # User account
            user_acc1 = UserAccount(
                applicant_id=applicant1.applicant_id,
                password_hash=hash_password("password123"),
                is_active=True
            )
            db.add(user_acc1)

            # Employment
            emp1 = Employment(
                applicant_id=applicant1.applicant_id,
                employment_type="Salaried",
                employer_name="Tata Consultancy Services",
                annual_income=Decimal("1200000.00"),
                employment_duration=5
            )
            db.add(emp1)

            # Application 1 (Historical - Approved)
            app1 = Application(
                applicant_id=applicant1.applicant_id,
                application_date=date(2025, 4, 10),
                loan_purpose="Personal",
                loan_amount=Decimal("300000.00"),
                loan_tenure=36,
                status="Approved"
            )
            db.add(app1)
            db.commit()
            db.refresh(app1)

            # Credit Profile
            cp1 = CreditProfile(
                application_id=app1.application_id,
                annual_income=Decimal("1200000.00"),
                employment_type="Salaried",
                employment_duration=5,
                number_of_dependents=1,
                debt_to_income_ratio=Decimal("0.24"),
                credit_utilization=Decimal("0.20"),
                previous_defaults=0,
                missed_payments=0,
                maximum_days_past_due=0,
                recent_credit_enquiries=1,
                number_of_credit_accounts=4,
                credit_history_length=6,
                payment_history=Decimal("0.98"),
                loan_to_income_ratio=Decimal("0.25")
            )
            db.add(cp1)

            # Credit Rating
            cr1 = CreditRating(
                application_id=app1.application_id,
                credit_score=755,
                risk_grade="A",
                rating_date=date(2025, 4, 10)
            )
            db.add(cr1)

            # Loan Request
            lr1 = LoanRequest(
                application_id=app1.application_id,
                loan_amount=Decimal("300000.00"),
                loan_tenure=36
            )
            db.add(lr1)
            db.commit()
            db.refresh(lr1)

            # Debt Metrics
            dm1 = DebtPaymentMetrics(
                loan_request_id=lr1.loan_request_id,
                existing_loans_count=1,
                total_outstanding_debt=Decimal("140000.00"),
                monthly_emi=Decimal("8500.00")
            )
            db.add(dm1)

            # Existing Loan
            ex1 = ExistingLoan(
                applicant_id=applicant1.applicant_id,
                loan_request_id=lr1.loan_request_id,
                loan_type="Personal Loan",
                loan_amount=Decimal("300000.00"),
                outstanding_amount=Decimal("140000.00"),
                monthly_emi=Decimal("8500.00")
            )
            db.add(ex1)

            # Loan Assessment
            la1 = LoanAssessment(
                application_id=app1.application_id,
                prediction=1,
                approval_probability=0.885,
                risk_score=11.5,
                risk_level="LOW",
                decision="APPROVE",
                risk_factors=[],
                assessment_date=date(2025, 4, 10)
            )
            db.add(la1)
            db.commit()
            print("✓ Seeded Customer Aarav Sharma: applicant@example.com / password123")

        # 3. Seed Sample Pending Loan Applications for Underwriter Queue
        existing_priya = db.query(Applicant).filter(Applicant.email == "priya.patel@example.com").first()
        if not existing_priya:
            priya = Applicant(
                full_name="Priya Patel",
                date_of_birth=date(1993, 11, 22),
                age=33,
                gender="Female",
                pan="PQRSP5678K",
                aadhaar_number="987654321098",
                address="701, Green Heights, Viman Nagar, Pune",
                phone_number="+91 91234 56789",
                email="priya.patel@example.com"
            )
            db.add(priya)
            db.commit()
            db.refresh(priya)

            emp2 = Employment(
                applicant_id=priya.applicant_id,
                employment_type="Self-Employed",
                employer_name="Patel Creative Studio",
                annual_income=Decimal("850000.00"),
                employment_duration=4
            )
            db.add(emp2)

            app2 = Application(
                applicant_id=priya.applicant_id,
                application_date=date.today(),
                loan_purpose="Business",
                loan_amount=Decimal("500000.00"),
                loan_tenure=36,
                status="Pending"
            )
            db.add(app2)
            db.commit()
            db.refresh(app2)

            cp2 = CreditProfile(
                application_id=app2.application_id,
                annual_income=Decimal("850000.00"),
                employment_type="Self-Employed",
                employment_duration=4,
                number_of_dependents=2,
                debt_to_income_ratio=Decimal("0.38"),
                credit_utilization=Decimal("0.45"),
                previous_defaults=0,
                missed_payments=1,
                maximum_days_past_due=15,
                recent_credit_enquiries=2,
                number_of_credit_accounts=3,
                credit_history_length=4,
                payment_history=Decimal("0.91"),
                loan_to_income_ratio=Decimal("0.58")
            )
            db.add(cp2)

            cr2 = CreditRating(
                application_id=app2.application_id,
                credit_score=660,
                risk_grade="C",
                rating_date=date.today()
            )
            db.add(cr2)

            lr2 = LoanRequest(
                application_id=app2.application_id,
                loan_amount=Decimal("500000.00"),
                loan_tenure=36
            )
            db.add(lr2)
            db.commit()
            db.refresh(lr2)

            dm2 = DebtPaymentMetrics(
                loan_request_id=lr2.loan_request_id,
                existing_loans_count=1,
                total_outstanding_debt=Decimal("120000.00"),
                monthly_emi=Decimal("6500.00")
            )
            db.add(dm2)

            la2 = LoanAssessment(
                application_id=app2.application_id,
                prediction=1,
                approval_probability=0.582,
                risk_score=41.8,
                risk_level="MEDIUM",
                decision="REVIEW",
                risk_factors=["Moderate Debt-to-Income ratio (38%)", "1 missed payment in past records"],
                assessment_date=date.today()
            )
            db.add(la2)
            db.commit()
            print("✓ Seeded Pending Application for Priya Patel (#" + str(app2.application_id) + ")")

        # 4. Seed Rahul Verma
        existing_rahul = db.query(Applicant).filter(Applicant.email == "rahul.verma@example.com").first()
        if not existing_rahul:
            rahul = Applicant(
                full_name="Rahul Verma",
                date_of_birth=date(1990, 3, 5),
                age=36,
                gender="Male",
                pan="MNOPR9012L",
                aadhaar_number="567890123456",
                address="12B, Palm Grove, Indiranagar, Bengaluru",
                phone_number="+91 99887 76655",
                email="rahul.verma@example.com"
            )
            db.add(rahul)
            db.commit()
            db.refresh(rahul)

            emp3 = Employment(
                applicant_id=rahul.applicant_id,
                employment_type="Salaried",
                employer_name="Infosys Ltd",
                annual_income=Decimal("1600000.00"),
                employment_duration=7
            )
            db.add(emp3)

            app3 = Application(
                applicant_id=rahul.applicant_id,
                application_date=date.today(),
                loan_purpose="Home Loan",
                loan_amount=Decimal("800000.00"),
                loan_tenure=48,
                status="Pending"
            )
            db.add(app3)
            db.commit()
            db.refresh(app3)

            cp3 = CreditProfile(
                application_id=app3.application_id,
                annual_income=Decimal("1600000.00"),
                employment_type="Salaried",
                employment_duration=7,
                number_of_dependents=2,
                debt_to_income_ratio=Decimal("0.22"),
                credit_utilization=Decimal("0.18"),
                previous_defaults=0,
                missed_payments=0,
                maximum_days_past_due=0,
                recent_credit_enquiries=1,
                number_of_credit_accounts=5,
                credit_history_length=8,
                payment_history=Decimal("0.99"),
                loan_to_income_ratio=Decimal("0.50")
            )
            db.add(cp3)

            cr3 = CreditRating(
                application_id=app3.application_id,
                credit_score=780,
                risk_grade="A",
                rating_date=date.today()
            )
            db.add(cr3)

            lr3 = LoanRequest(
                application_id=app3.application_id,
                loan_amount=Decimal("800000.00"),
                loan_tenure=48
            )
            db.add(lr3)
            db.commit()
            db.refresh(lr3)

            dm3 = DebtPaymentMetrics(
                loan_request_id=lr3.loan_request_id,
                existing_loans_count=0,
                total_outstanding_debt=Decimal("0.00"),
                monthly_emi=Decimal("0.00")
            )
            db.add(dm3)

            la3 = LoanAssessment(
                application_id=app3.application_id,
                prediction=1,
                approval_probability=0.895,
                risk_score=10.5,
                risk_level="LOW",
                decision="APPROVE",
                risk_factors=[],
                assessment_date=date.today()
            )
            db.add(la3)
            db.commit()
            print("✓ Seeded Pending Application for Rahul Verma (#" + str(app3.application_id) + ")")

        print("✓ All initial seeds completed successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    train_model()
    seed_database()
