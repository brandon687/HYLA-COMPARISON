@echo off
REM Hyla Stock Comparison Dashboard Startup Script for Windows

echo ========================================
echo Hyla Stock Comparison Dashboard
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed.
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo Dependencies installed.
echo.

REM Start the Flask application
echo ========================================
echo Starting dashboard...
echo ========================================
echo.
echo The dashboard will open at:
echo     http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python web_app.py

pause
