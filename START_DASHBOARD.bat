@echo off
echo.
echo ======================================================================
echo  VOC DASHBOARD SERVER
echo ======================================================================
echo.
echo Starting server...
echo.
echo Open your browser and go to:
echo   http://localhost:8000/Original%20Code.html
echo.
echo Press Ctrl+C to stop the server when done.
echo.
echo ======================================================================
echo.

cd /d "%~dp0"
python server.py

pause
