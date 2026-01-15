@echo off
REM Check Python version and start server
echo.
echo ======================================================================
echo  VOC DASHBOARD - SETUP & RUN
echo ======================================================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please ensure Python 3.x is installed from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python found!
echo.

REM Check if required files exist
if not exist "Original Code.html" (
    echo ERROR: Original Code.html not found!
    pause
    exit /b 1
)

if not exist "latest_t_mapped.csv" (
    echo WARNING: latest_t_mapped.csv not found!
    echo The dashboard may not load data properly.
    echo.
)

echo.
echo ======================================================================
echo  STARTING SERVER...
echo ======================================================================
echo.
echo Your dashboard will be available at:
echo   http://localhost:8000
echo.
echo If port 8000 is busy, try:
echo   http://localhost:8001
echo   http://localhost:8002
echo.
echo To STOP the server: Press Ctrl+C
echo.

REM Start Python server
cd /d "%~dp0"
python run_server.py

if errorlevel 1 (
    echo.
    echo Server failed to start. Press Enter to see error details.
    pause
)
