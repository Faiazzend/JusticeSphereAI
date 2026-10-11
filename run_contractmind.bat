@echo off
setlocal enabledelayedexpansion

echo ======================================================================
echo  🏛️ ContractMind v1.5 — 1-Click Launch Launcher
echo  Autonomous Multi-Agent Legal AI Studio (JusticeSphere_AI)
echo ======================================================================

REM Check for Python
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python was not found in PATH!
    echo Please install Python 3.10+ and add it to your system PATH.
    pause
    exit /b 1
)

echo [1/3] Python detected.
python --version

echo [2/3] Verifying and installing backend dependencies...
python -m pip install -r backend\requirements.txt --quiet --disable-pip-version-check
if %ERRORLEVEL% neq 0 (
    echo [WARNING] Pip encountered warnings or errors, proceeding to launch...
)

echo [3/3] Launching ContractMind v1.5 Studio...
python launch.py

pause
