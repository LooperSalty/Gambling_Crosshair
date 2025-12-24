@echo off
REM Script pour créer l'installateur .exe

echo ========================================
echo  Crosshair Gambler Pro - Build Installer
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe!
    pause
    exit /b 1
)

echo [1/4] Installation des dependances requises...
python -m pip install pyinstaller pywin32 winshell pillow --quiet
if %errorlevel% neq 0 (
    echo [ERREUR] Impossible d'installer les dependances
    pause
    exit /b 1
)
echo [OK] Dependances installees
echo.

echo [2/4] Creation de l'executable...
echo Cela peut prendre 1-2 minutes...
echo.

REM Créer l'exe avec PyInstaller en incluant tous les fichiers nécessaires
REM --manifest inclut le fichier qui force l'exécution en mode admin
pyinstaller --onefile --windowed --name="Crosshair_Gambler_Installer" --icon=icone.png --manifest=installer.manifest --add-data="icone.png;." installer.py

if %errorlevel% neq 0 (
    echo [ERREUR] Echec de la creation de l'exe
    pause
    exit /b 1
)

echo [OK] Executable cree
echo.

echo [3/4] Nettoyage...
REM Déplacer l'exe vers le dossier principal
if exist "dist\Crosshair_Gambler_Installer.exe" (
    move /Y "dist\Crosshair_Gambler_Installer.exe" "Crosshair_Gambler_Installer.exe" >nul
    echo [OK] Fichier deplace vers le dossier principal
)

REM Nettoyer les fichiers temporaires
if exist "build" rmdir /S /Q "build"
if exist "dist" rmdir /S /Q "dist"
if exist "Crosshair_Gambler_Installer.spec" del "Crosshair_Gambler_Installer.spec"

echo.
echo [4/4] Creation du script de lancement administrateur...
echo @echo off > Run_Installer_As_Admin.bat
echo echo Lancement de l'installateur en mode administrateur... >> Run_Installer_As_Admin.bat
echo powershell -Command "Start-Process '%~dp0Crosshair_Gambler_Installer.exe' -Verb RunAs" >> Run_Installer_As_Admin.bat
echo [OK] Script administrateur cree

echo.
echo ========================================
echo  Build termine!
echo ========================================
echo.
echo L'installateur a ete cree: Crosshair_Gambler_Installer.exe
echo.
echo IMPORTANT: Pour installer dans Program Files, lancez:
echo   - Run_Installer_As_Admin.bat (recommande)
echo   - OU faites clic-droit sur l'exe ^> Executer en tant qu'administrateur
echo.
pause
