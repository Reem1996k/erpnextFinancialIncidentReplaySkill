@echo off
REM Financial Incident Replay System - Quick Start for Windows

color 0A
title Financial Incident Replay System - Quick Start

echo.
echo ========================================
echo   Financial Incident Replay System
echo   Quick Start Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.11+ and try again
    exit /b 1
)

REM Check if Node/npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js/npm is not installed or not in PATH
    echo Please install Node.js LTS and try again
    exit /b 1
)

echo [OK] Python found: 
python --version

echo [OK] Node.js found: 
npm --version

echo.
echo Step 1: Installing frontend dependencies...
cd ui
if not exist node_modules (
    call npm install
    if errorlevel 1 (
        echo [ERROR] npm install failed
        exit /b 1
    )
) else (
    echo [OK] node_modules already exists, skipping npm install
)

echo.
echo [SUCCESS] Setup complete!
echo.
echo Next: Start the system with start_system.bat
echo.
pause
