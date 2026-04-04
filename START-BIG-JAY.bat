@echo off
title Big-Jay OS Launcher
color 0B

echo Verifying system dependencies...
python -c "import customtkinter" 2>nul || pip install customtkinter -q
python -c "import gradio" 2>nul || pip install gradio -q

cls
echo ===================================================
echo             ROCKET BIG-JAY AI-OS
echo ===================================================
echo.
echo Select your Command Center interface:
echo.
echo   [1] Desktop App (Native Windows GUI)
echo   [2] Web App (Remote Access via Phone/Tablet)
echo   [3] Launch BOTH (Desktop GUI + Background Web Server)
echo.
set /p choice="Enter your choice (1, 2, or 3): "

if "%choice%"=="1" goto desktop
if "%choice%"=="2" goto web
if "%choice%"=="3" goto both

:desktop
start pythonw big_jay_gui.py
exit

:web
start python big_jay_web.py
exit

:both
echo Starting Web Server in the background...
start /B pythonw big_jay_web.py
timeout /t 2 /nobreak >nul
start pythonw big_jay_gui.py
exit