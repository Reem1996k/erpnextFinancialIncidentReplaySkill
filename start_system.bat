@echo off
REM Financial Incident Replay System - Start Both Backend and Frontend

color 0A
title Financial Incident Replay System - Running

echo.
echo ============================================================
echo   Financial Incident Replay System
echo   Starting Backend and Frontend...
echo ============================================================
echo.

echo [1/2] Starting Backend (FastAPI on port 8000)...
echo.
echo Backend will run in a new window...
echo.
start "Financial Incident Replay - Backend" cmd /k cd /d "%CD%\backend" && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

timeout /t 3 /nobreak

echo [2/2] Starting Frontend (Next.js on port 3000)...
echo.
echo Frontend will run in a new window...
echo.
start "Financial Incident Replay - Frontend" cmd /k cd /d "%CD%\ui" && npm run dev

echo.
echo ============================================================
echo   ✓ Both services starting...
echo.
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:3000
echo   API Docs: http://localhost:8000/docs
echo.
echo   Press Ctrl+C in the windows to stop services
echo ============================================================
echo.

echo Opening browser in 5 seconds...
timeout /t 5 /nobreak

start http://localhost:3000

echo.
echo [OK] System started!
echo.
pause
