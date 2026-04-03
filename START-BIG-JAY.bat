@echo off
title Big-Jay AI-OS Launcher
echo ========================================
echo      Initializing Big-Jay AI-OS
echo ========================================
echo.

:: Ensure the script is running in its own folder
cd /d "%~dp0"

echo [1/2] Waking up the background engines...
docker compose up -d

echo.
echo [2/2] Launching Command Center GUI...
:: Check if the UI library is installed, if not, install it silently
python -c "import customtkinter" 2>nul || pip install customtkinter -q

:: Run the GUI without leaving a black terminal window open
start pythonw big_jay_gui.py

:: Close this launcher window automatically
exit