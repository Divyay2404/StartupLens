@echo off
echo ========================================================
echo   Starting StartupLens (SerpApi Hackathon Track 5)
echo ========================================================
start "StartupLens Backend" cmd /c "%~dp0start_backend.bat"
start "StartupLens Frontend" cmd /c "%~dp0start_frontend.bat"
echo Services launched!
echo Access the web interface at: http://localhost:5173
echo Backend API documentation at: http://localhost:8000/docs
