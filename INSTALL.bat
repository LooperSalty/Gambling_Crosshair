@echo off
REM Crosshair Gambler Pro - Installation Script
REM This script checks for Python and installs required libraries

echo ========================================
echo  Crosshair Gambler Pro - Installation
echo ========================================
echo.

REM Check if Python is installed
echo [1/3] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Python is not installed!
    echo.
    echo Please download and install Python from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version
echo.

REM Upgrade pip
echo [2/3] Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install required libraries
echo [3/3] Installing required libraries...
echo.
echo Installing Pillow (image processing)...
python -m pip install pillow
echo.

echo Installing pynput (keyboard/mouse control)...
python -m pip install pynput
echo.

echo Installing pygame (sound)...
python -m pip install pygame
echo.

echo ========================================
echo  Installation Complete!
echo ========================================
echo.
echo All libraries have been installed successfully.
echo You can now run the application with "RUN_APP.bat"
echo.
pause
