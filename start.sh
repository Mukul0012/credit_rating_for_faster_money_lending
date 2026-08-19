#!/usr/bin/env bash

# ==============================================================================
# Credit Risk Assessment & Lending Platform Startup Script
# ==============================================================================

set -e

# Set working directory to the project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="${PROJECT_ROOT}/backend"
FRONTEND_DIR="${PROJECT_ROOT}/frontend"

# Colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}====================================================${NC}"
echo -e "${CYAN}   Starting Credit Rating & Lending Platform        ${NC}"
echo -e "${CYAN}====================================================${NC}"

# 1. Check & Setup Backend
echo -e "\n${BLUE}[1/3] Checking Backend Environment...${NC}"
PYTHON_EXEC=""
if [ -f "${BACKEND_DIR}/.venv/bin/python" ]; then
    PYTHON_EXEC="${BACKEND_DIR}/.venv/bin/python"
elif command -v python3 &>/dev/null; then
    PYTHON_EXEC="$(command -v python3)"
else
    echo -e "${RED}Error: Python 3 was not found. Please install Python 3.${NC}"
    exit 1
fi

echo -e "Using Python: ${GREEN}${PYTHON_EXEC}${NC}"

# Check if model exists or seed is required
if [ ! -f "${BACKEND_DIR}/app/ml/models/random_forest_tuned.pkl" ]; then
    echo -e "${YELLOW}ML model not found. Training model and seeding database...${NC}"
    (cd "${BACKEND_DIR}" && "${PYTHON_EXEC}" scripts/train_and_seed.py)
fi

# 2. Check & Setup Frontend
echo -e "\n${BLUE}[2/3] Checking Frontend Environment...${NC}"
if [ ! -d "${FRONTEND_DIR}/node_modules" ]; then
    echo -e "${YELLOW}Node modules not found. Running npm install...${NC}"
    (cd "${FRONTEND_DIR}" && npm install)
fi

# 3. Process Management & Cleanup
BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
    echo -e "\n\n${YELLOW}Shutting down services...${NC}"
    if [ -n "$BACKEND_PID" ] && kill -0 "$BACKEND_PID" 2>/dev/null; then
        kill "$BACKEND_PID" 2>/dev/null || true
    fi
    if [ -n "$FRONTEND_PID" ] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
        kill "$FRONTEND_PID" 2>/dev/null || true
    fi
    wait 2>/dev/null || true
    echo -e "${GREEN}All services stopped cleanly.${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

# Start Backend
echo -e "\n${BLUE}[3/3] Starting Services...${NC}"
echo -e "${GREEN}-> Launching FastAPI backend on http://127.0.0.1:8000 ...${NC}"
(cd "${BACKEND_DIR}" && exec "${PYTHON_EXEC}" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload) &
BACKEND_PID=$!

# Start Frontend
echo -e "${GREEN}-> Launching Vite frontend on http://localhost:5173 ...${NC}"
(cd "${FRONTEND_DIR}" && exec npm run dev -- --host 0.0.0.0 --port 5173) &
FRONTEND_PID=$!

sleep 2

echo -e "\n${CYAN}====================================================${NC}"
echo -e "${GREEN}✓ All services are up and running!${NC}"
echo -e "${CYAN}====================================================${NC}"
echo -e "  ${BLUE}Frontend Application:${NC} http://localhost:5173"
echo -e "  ${BLUE}Backend API Docs:${NC}     http://localhost:8000/docs"
echo -e "  ${BLUE}Backend API Root:${NC}     http://localhost:8000/"
echo -e "${CYAN}----------------------------------------------------${NC}"
echo -e "  ${YELLOW}Lender Credentials:${NC}    underwriter@bank.com / password123"
echo -e "  ${YELLOW}Customer Credentials:${NC}  applicant@example.com / password123"
echo -e "${CYAN}====================================================${NC}"
echo -e "${YELLOW}Press [Ctrl+C] at any time to stop all services.${NC}\n"

# Wait for background processes
wait "$BACKEND_PID" "$FRONTEND_PID"
