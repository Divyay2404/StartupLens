@echo off
echo Starting StartupLens Frontend...
cd /d "%~dp0frontend"
npm.cmd run dev
pause
