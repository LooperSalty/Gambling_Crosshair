@echo off
REM Crosshair Gambler Pro - Installation automatique
REM Ce script installe Python automatiquement si nécessaire

echo ========================================
echo  Crosshair Gambler Pro - Installation
echo ========================================
echo.

REM Vérifier si Python est installé
echo [1/4] Verification de Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python est deja installe
    python --version
    echo.
    goto :install_libs
)

REM Python n'est pas installé, on va l'installer automatiquement
echo [!] Python n'est pas installe sur votre ordinateur
echo.
echo Installation automatique de Python en cours...
echo Cela peut prendre quelques minutes, veuillez patienter...
echo.

REM Créer un dossier temporaire
set TEMP_DIR=%TEMP%\python_installer
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

REM Télécharger l'installateur Python (version 3.11.9 - stable et compatible)
echo [2/4] Telechargement de Python 3.11.9...
set PYTHON_URL=https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
set INSTALLER=%TEMP_DIR%\python-installer.exe

REM Utiliser PowerShell pour télécharger (disponible sur tous les Windows modernes)
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%INSTALLER%'}" 2>nul

if not exist "%INSTALLER%" (
    echo.
    echo [ERREUR] Le telechargement a echoue.
    echo.
    echo Veuillez verifier votre connexion Internet et reessayer.
    echo Ou installez Python manuellement depuis: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Telechargement termine
echo.

REM Installer Python silencieusement avec toutes les options nécessaires
echo [3/4] Installation de Python en cours...
echo Cela peut prendre 2-3 minutes...
echo.

REM Options d'installation :
REM /quiet = installation silencieuse sans interface graphique
REM InstallAllUsers=0 = installation pour l'utilisateur actuel seulement (pas besoin d'admin)
REM PrependPath=1 = ajoute Python au PATH automatiquement
REM Include_pip=1 = installe pip
REM Include_tcltk=1 = installe tkinter (nécessaire pour l'interface graphique)
"%INSTALLER%" /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1 Include_tcltk=1

REM Attendre que l'installation se termine
timeout /t 10 /nobreak >nul

REM Nettoyer
del "%INSTALLER%" 2>nul
rmdir "%TEMP_DIR%" 2>nul

REM Rafraîchir les variables d'environnement
echo Rafraichissement des variables d'environnement...
call refreshenv >nul 2>&1

REM Vérifier que Python est bien installé
echo.
echo Verification de l'installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ATTENTION] Python a ete installe mais n'est pas encore accessible.
    echo Veuillez FERMER cette fenetre et relancer INSTALL.bat
    echo.
    pause
    exit /b 0
)

echo [OK] Python a ete installe avec succes !
python --version
echo.

:install_libs
REM Mise à jour de pip
echo [3/4] Mise a jour de pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip mis a jour
echo.

REM Installation des bibliothèques requises
echo [4/4] Installation des bibliotheques requises...
echo.
echo Installation de Pillow (traitement d'images)...
python -m pip install pillow --quiet
if %errorlevel% neq 0 (
    echo [ERREUR] Echec de l'installation de Pillow
    pause
    exit /b 1
)
echo [OK] Pillow installe
echo.

echo Installation de pynput (controle clavier/souris)...
python -m pip install pynput --quiet
if %errorlevel% neq 0 (
    echo [ERREUR] Echec de l'installation de pynput
    pause
    exit /b 1
)
echo [OK] pynput installe
echo.

echo Installation de pygame (son)...
python -m pip install pygame --quiet
if %errorlevel% neq 0 (
    echo [ERREUR] Echec de l'installation de pygame
    pause
    exit /b 1
)
echo [OK] pygame installe
echo.

echo ========================================
echo  Installation terminee avec succes !
echo ========================================
echo.
echo Toutes les bibliotheques ont ete installees.
echo.
echo Vous pouvez maintenant lancer l'application avec "RUN_APP.bat"
echo.
echo Appuyez sur une touche pour terminer...
pause >nul
