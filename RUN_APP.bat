@echo off
REM Crosshair Gambler Pro - Run Application Script
REM Double-click this file to launch the application

echo ========================================
echo  Crosshair Gambler Pro
echo ========================================
echo.
echo Starting application...
echo.

REM Check if Python is installed in PATH
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto :run_app
)

REM Check for py launcher
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto :run_app
)

REM Check common installation paths
if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    set PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    goto :run_app
)
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    goto :run_app
)
if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    set PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    goto :run_app
)
if exist "%LOCALAPPDATA%\Programs\Python\Python39\python.exe" (
    set PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python39\python.exe"
    goto :run_app
)

echo [ERROR] Python is not installed or not found!
echo.
echo Please run "INSTALL.bat" first to set up the application.
echo.
pause
exit /b 1

:run_app

REM Run the application
%PYTHON_CMD% crosshair_gambler.py

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
