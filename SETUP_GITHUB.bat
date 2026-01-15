@echo off
REM Quick Setup for GitHub + Render Deployment

echo.
echo ======================================================================
echo  VOC DASHBOARD - GITHUB SETUP
echo ======================================================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo Download from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo Git found!
echo.

REM Initialize git repo
echo Initializing Git repository...
git init
git add .
git commit -m "Initial commit: VOC Dashboard"

echo.
echo ======================================================================
echo  NEXT STEPS:
echo ======================================================================
echo.
echo 1. Create GitHub Repository:
echo    - Go to https://github.com/new
echo    - Create repo named: voc-dashboard
echo    - Copy the HTTPS URL from GitHub
echo.
echo 2. Connect to GitHub:
echo    Open VS Code terminal and run:
echo    git remote add origin https://github.com/YOUR_USERNAME/voc-dashboard.git
echo    git push -u origin main
echo.
echo 3. Deploy to Render:
echo    - Go to https://render.com
echo    - Sign up (free)
echo    - Select "New Web Service"
echo    - Connect your GitHub repository
echo    - Render will deploy automatically!
echo.
echo 4. Your dashboard will be live at:
echo    https://voc-dashboard.onrender.com
echo.
echo ======================================================================
echo.
pause
