@echo off
chcp 65001 >nul
title Préparation de l'Installateur - Crosshair Gambler Pro
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║   🎰 Crosshair Gambler Pro - Préparation Installer       ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Vérifier si Python est installé
echo [1/4] 🔍 Vérification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERREUR: Python n'est pas installé ou n'est pas dans le PATH
    echo.
    echo 📥 Veuillez installer Python 3.10 ou 3.11 depuis:
    echo    https://www.python.org/downloads/
    echo.
    echo ⚠️  N'oubliez pas de cocher "Add Python to PATH" lors de l'installation!
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% détecté
echo.

REM Mettre à jour pip
echo [2/4] 📦 Mise à jour de pip...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo ⚠️  Avertissement: Impossible de mettre à jour pip
) else (
    echo ✅ pip mis à jour
)
echo.

REM Installer les dépendances requises pour l'installateur
echo [3/4] 📥 Installation des dépendances de l'installateur...
echo    - pywin32 (pour les raccourcis Windows)
echo    - winshell (pour l'intégration système)
echo.

python -m pip install pywin32 winshell --quiet
if errorlevel 1 (
    echo ❌ ERREUR: Impossible d'installer les dépendances
    echo.
    echo 💡 Essayez manuellement:
    echo    pip install pywin32 winshell
    echo.
    pause
    exit /b 1
)

echo ✅ Dépendances installées avec succès
echo.

REM Lancer l'installateur en tant qu'administrateur
echo [4/4] 🚀 Lancement de l'installateur...
echo.
echo ⚠️  Une fenêtre UAC va s'ouvrir pour demander les droits administrateur
echo    Cliquez sur "Oui" pour continuer l'installation
echo.
timeout /t 2 /nobreak >nul

REM Lancer installer.py avec les droits admin
powershell -Command "Start-Process python -ArgumentList '%~dp0installer.py' -Verb RunAs"

if errorlevel 1 (
    echo.
    echo ❌ ERREUR: Impossible de lancer l'installateur en mode administrateur
    echo.
    echo 💡 Solution alternative:
    echo    1. Faites clic-droit sur installer.py
    echo    2. Sélectionnez "Exécuter en tant qu'administrateur"
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Installateur lancé!
echo.
echo Vous pouvez fermer cette fenêtre.
timeout /t 3 /nobreak >nul
exit /b 0
