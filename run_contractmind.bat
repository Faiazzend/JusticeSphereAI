@echo off
title ContractMind v1.5 Studio - Autonomous Legal AI
color 0B

cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python was not found in your PATH!
    echo Please install Python 3.10+ from https://www.python.org and ensure "Add Python to PATH" is checked.
    pause
    exit /b 1
)

python -c "import fastapi" >nul 2>nul
if %errorlevel% neq 0 (
    echo [*] Installing required Python dependencies...
    pip install -r backend\requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b 1
    )
)

python launch.py

pause
