@echo off
REM ==============================================================================
REM Credit Risk Assessment & Lending Platform Windows Startup Script
REM ==============================================================================

echo ====================================================
echo    Starting Credit Rating ^& Lending Platform
echo ====================================================

set PROJECT_ROOT=%~dp0
set BACKEND_DIR=%PROJECT_ROOT%backend
set FRONTEND_DIR=%PROJECT_ROOT%frontend

REM 1. Start Backend in a new window
echo [1/2] Starting FastAPI Backend...
start "Backend Server - FastAPI" cmd /k "cd /d %BACKEND_DIR% && if exist .venv\Scripts\activate.bat (call .venv\Scripts\activate.bat) && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

REM 2. Start Frontend in a new window
echo [2/2] Starting Vite Frontend...
start "Frontend Server - Vite" cmd /k "cd /d %FRONTEND_DIR% && npm run dev -- --host 0.0.0.0 --port 5173"

echo ====================================================
echo All services launched in separate windows!
echo Frontend: http://localhost:5173
echo Backend API Docs: http://localhost:8000/docs
echo ====================================================
