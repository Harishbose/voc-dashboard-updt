@echo off
REM Automated Git Setup Launcher for VOC Dashboard

echo.
echo ======================================================================
echo  VOC DASHBOARD - GIT SETUP LAUNCHER
echo ======================================================================
echo.

REM Get the directory where this batch file is located
cd /d "%~dp0"

REM Run the PowerShell script with proper execution policy
powershell -NoProfile -ExecutionPolicy Bypass -File "SETUP_GIT_AUTO.ps1"

pause
