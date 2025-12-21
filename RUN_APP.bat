@echo off
REM Crosshair Gambler Pro - Run Application Script
REM Double-click this file to launch the application

echo ========================================
echo  Crosshair Gambler Pro
echo ========================================
echo.
echo Starting application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please run "INSTALL.bat" first to set up the application.
    echo.
    pause
    exit /b 1
)

REM Run the application
python crosshair_gambler.py

REM If the application exits with an error
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] The application encountered an error.
    echo.
    echo If you see "ModuleNotFoundError", please run "INSTALL.bat"
    echo to install the required libraries.
    echo.
    pause
)
