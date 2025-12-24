"""
Crosshair Gambler Pro - Installateur Professionnel
Gère l'installation, la réparation et la désinstallation
"""

import tkinter as tk
from tkinter import messagebox, ttk
import os
import sys
import subprocess
import json
import shutil
from pathlib import Path
import urllib.request
import tempfile
import threading
import winshell
from win32com.client import Dispatch
import ctypes

def is_admin():
    """Vérifier si le script s'exécute avec les droits admin"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Relancer le script en tant qu'administrateur"""
    try:
        if sys.argv[0].endswith('.py'):
            # Script Python
            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                sys.executable, 
                f'"{os.path.abspath(sys.argv[0])}"',
                None, 
                1
            )
        else:
            # Exe compilé
            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                sys.executable,
                " ".join(sys.argv),
                None, 
                1
            )
        # Fermer cette instance immédiatement
        sys.exit(0)
    except Exception as e:
        # Afficher l'erreur dans la console si possible
        print(f"Erreur: Impossible de demander les droits administrateur: {e}")
        print("Veuillez faire clic-droit > Exécuter en tant qu'administrateur")
        input("Appuyez sur Entrée pour quitter...")
        sys.exit(1)

class InstallerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Crosshair Gambler Pro - Installateur")
        self.root.geometry("600x550")
        self.root.configure(bg="#1a1a1a")
        self.root.resizable(False, False)
        
        # Paths
        self.source_dir = os.path.dirname(os.path.abspath(__file__))
        self.install_dir = r"C:\Program Files\Crosshair Gambler Pro"
        self.config_file = os.path.join(self.install_dir, ".install_info.json")
        self.desktop_shortcut = os.path.join(winshell.desktop(), "Crosshair Gambler Pro.lnk")
        self.start_menu_folder = os.path.join(
            os.environ['APPDATA'], 
            r"Microsoft\Windows\Start Menu\Programs\Crosshair Gambler Pro"
        )
        
        # Variables
        self.is_installed = self.check_installation()
        self.python_version = self.get_python_version()
        self.create_desktop_shortcut_var = tk.BooleanVar(value=True)
        
        self.create_ui()
    
    def refresh_ui(self):
        """Rafraîchir l'interface sans recréer la fenêtre"""
        # Destroy all existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Update variables
        self.is_installed = self.check_installation()
        self.python_version = self.get_python_version()
        
        # Recreate UI
        self.create_ui()
        
    def create_ui(self):
        """Créer l'interface utilisateur"""
        # Header
        header = tk.Frame(self.root, bg="#2a2a2a", height=80)
        header.pack(fill="x")
        
        title = tk.Label(
            header,
            text="🎰 Crosshair Gambler Pro",
            font=("Arial", 20, "bold"),
            fg="#00ff00",
            bg="#2a2a2a"
        )
        title.pack(pady=25)
        
        # Main content
        content = tk.Frame(self.root, bg="#1a1a1a")
        content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Status section
        status_frame = tk.LabelFrame(
            content,
            text="📊 État du Système",
            font=("Arial", 12, "bold"),
            fg="#ffffff",
            bg="#1a1a1a",
            bd=2,
            relief="groove"
        )
        status_frame.pack(fill="x", pady=10)
        
        # Python status
        python_frame = tk.Frame(status_frame, bg="#1a1a1a")
        python_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(
            python_frame,
            text="🐍 Python:",
            font=("Arial", 10, "bold"),
            fg="#ffffff",
            bg="#1a1a1a"
        ).pack(side="left")
        
        python_status = self.get_python_status()
        self.python_label = tk.Label(
            python_frame,
            text=python_status["text"],
            font=("Arial", 10),
            fg=python_status["color"],
            bg="#1a1a1a"
        )
        self.python_label.pack(side="left", padx=10)
        
        # Installation status
        install_frame = tk.Frame(status_frame, bg="#1a1a1a")
        install_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(
            install_frame,
            text="📦 Application:",
            font=("Arial", 10, "bold"),
            fg="#ffffff",
            bg="#1a1a1a"
        ).pack(side="left")
        
        if self.is_installed:
            install_info = self.load_install_info()
            install_text = f"✅ Installée dans {self.install_dir}"
            install_color = "#00ff00"
        else:
            install_text = "❌ Non installée"
            install_color = "#ff6600"
        
        self.install_label = tk.Label(
            install_frame,
            text=install_text,
            font=("Arial", 10),
            fg=install_color,
            bg="#1a1a1a"
        )
        self.install_label.pack(side="left", padx=10)
        
        # Desktop shortcut option (only for new install)
        if not self.is_installed:
            shortcut_frame = tk.Frame(content, bg="#1a1a1a")
            shortcut_frame.pack(fill="x", pady=10)
            
            self.desktop_check = tk.Checkbutton(
                shortcut_frame,
                text="🖥️ Créer un raccourci sur le Bureau",
                variable=self.create_desktop_shortcut_var,
                bg="#1a1a1a",
                fg="#ffffff",
                selectcolor="#2a2a2a",
                font=("Arial", 10),
                activebackground="#1a1a1a",
                activeforeground="#ffffff"
            )
            self.desktop_check.pack(anchor="w")
        
        # Progress bar (hidden initially)
        self.progress_frame = tk.Frame(content, bg="#1a1a1a")
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="Installation en cours...",
            font=("Arial", 10),
            fg="#ffffff",
            bg="#1a1a1a"
        )
        self.progress_label.pack(pady=5)
        
        self.progress = ttk.Progressbar(
            self.progress_frame,
            mode='indeterminate',
            length=400
        )
        self.progress.pack(pady=10)
        
        self.status_text = tk.Text(
            self.progress_frame,
            height=6,
            width=60,
            bg="#2a2a2a",
            fg="#00ff00",
            font=("Consolas", 9),
            state="disabled"
        )
        self.status_text.pack(pady=10)
        
        # Buttons
        btn_frame = tk.Frame(content, bg="#1a1a1a")
        btn_frame.pack(pady=20)
        
        if not self.is_installed:
            # Install button
            self.install_btn = tk.Button(
                btn_frame,
                text="📥 INSTALLER",
                command=self.start_installation,
                bg="#00ff00",
                fg="#000000",
                font=("Arial", 14, "bold"),
                width=20,
                height=2,
                relief="flat",
                cursor="hand2"
            )
            self.install_btn.pack(pady=5)
        else:
            # Repair button
            self.repair_btn = tk.Button(
                btn_frame,
                text="🔧 RÉPARER",
                command=self.repair_installation,
                bg="#0066ff",
                fg="#ffffff",
                font=("Arial", 12, "bold"),
                width=20,
                height=1,
                relief="flat",
                cursor="hand2"
            )
            self.repair_btn.pack(pady=5)
            
            # Uninstall button
            self.uninstall_btn = tk.Button(
                btn_frame,
                text="🗑️ DÉSINSTALLER",
                command=self.uninstall,
                bg="#ff0000",
                fg="#ffffff",
                font=("Arial", 12, "bold"),
                width=20,
                height=1,
                relief="flat",
                cursor="hand2"
            )
            self.uninstall_btn.pack(pady=5)
            
            # Launch button
            self.launch_btn = tk.Button(
                btn_frame,
                text="🚀 LANCER L'APPLICATION",
                command=self.launch_app,
                bg="#00ff00",
                fg="#000000",
                font=("Arial", 12, "bold"),
                width=20,
                height=1,
                relief="flat",
                cursor="hand2"
            )
            self.launch_btn.pack(pady=5)
        
        # Exit button
        exit_btn = tk.Button(
            btn_frame,
            text="❌ Quitter",
            command=self.root.quit,
            bg="#666666",
            fg="#ffffff",
            font=("Arial", 10),
            width=20,
            relief="flat",
            cursor="hand2"
        )
        exit_btn.pack(pady=10)
        
    def check_installation(self):
        """Vérifier si l'application est déjà installée"""
        return os.path.exists(self.config_file)
    
    def load_install_info(self):
        """Charger les informations d'installation"""
        if not os.path.exists(self.config_file):
            return {}
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_install_info(self, info):
        """Sauvegarder les informations d'installation"""
        with open(self.config_file, 'w') as f:
            json.dump(info, f, indent=2)
    
    def get_python_version(self):
        """Obtenir la version de Python"""
        try:
            result = subprocess.run(
                ["python", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                version_str = result.stdout.strip().split()[1]
                return version_str
            return None
        except:
            return None
    
    def get_python_status(self):
        """Obtenir le statut de Python"""
        if not self.python_version:
            return {
                "text": "❌ Non installé",
                "color": "#ff0000",
                "valid": False
            }
        
        # Parse version
        major, minor, patch = map(int, self.python_version.split('.')[:3])
        
        # Check if version is compatible (3.10 or 3.11)
        if (major == 3 and minor == 10) or (major == 3 and minor == 11):
            return {
                "text": f"✅ {self.python_version} (Compatible)",
                "color": "#00ff00",
                "valid": True
            }
        elif major == 3 and minor < 10:
            return {
                "text": f"⚠️ {self.python_version} (Trop ancien, 3.10-3.11 requis)",
                "color": "#ff6600",
                "valid": False
            }
        else:
            return {
                "text": f"⚠️ {self.python_version} (Trop récent, 3.10-3.11 requis)",
                "color": "#ff6600",
                "valid": False
            }
    
    def log(self, message):
        """Ajouter un message au log"""
        self.status_text.config(state="normal")
        self.status_text.insert("end", f"{message}\n")
        self.status_text.see("end")
        self.status_text.config(state="disabled")
        self.root.update()
    
    def start_installation(self):
        """Démarrer l'installation"""
        python_status = self.get_python_status()
        
        if not python_status["valid"]:
            # Need to install Python
            response = messagebox.askyesno(
                "Python Incompatible",
                "Python 3.10 ou 3.11 est requis.\n\n"
                "Voulez-vous télécharger et installer Python 3.11.9 automatiquement ?\n\n"
                "Cela prendra environ 3-5 minutes."
            )
            if response:
                self.install_python()
            else:
                messagebox.showinfo(
                    "Installation annulée",
                    "Installez Python 3.10 ou 3.11 manuellement depuis:\n"
                    "https://www.python.org/downloads/"
                )
            return
        
        # Python OK, proceed with installation
        self.progress_frame.pack(fill="x", pady=10)
        self.install_btn.config(state="disabled")
        if hasattr(self, 'desktop_check'):
            self.desktop_check.config(state="disabled")
        self.progress.start()
        
        # Run installation in background thread to avoid freezing UI
        thread = threading.Thread(target=self.perform_installation, daemon=True)
        thread.start()

    
    def install_python(self):
        """Installer Python 3.11.9"""
        self.progress_frame.pack(fill="x", pady=10)
        self.install_btn.config(state="disabled")
        self.progress.start()
        
        self.log("📥 Téléchargement de Python 3.11.9...")
        
        # Download Python installer
        python_url = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
        temp_dir = tempfile.gettempdir()
        installer_path = os.path.join(temp_dir, "python-3.11.9-installer.exe")
        
        try:
            urllib.request.urlretrieve(python_url, installer_path)
            self.log("✅ Téléchargement terminé")
            
            self.log("📦 Installation de Python en cours...")
            self.log("⏳ Veuillez patienter 2-3 minutes...")
            
            # Install Python silently
            result = subprocess.run(
                [
                    installer_path,
                    "/quiet",
                    "InstallAllUsers=0",
                    "PrependPath=1",
                    "Include_pip=1",
                    "Include_tcltk=1"
                ],
                capture_output=True
            )
            
            if result.returncode == 0:
                self.log("✅ Python installé avec succès")
                self.log("")
                self.log("⚠️ IMPORTANT: Veuillez REDÉMARRER cet installateur")
                self.log("pour que Python soit reconnu.")
                
                messagebox.showinfo(
                    "Redémarrage requis",
                    "Python a été installé avec succès!\n\n"
                    "Veuillez FERMER et RELANCER cet installateur."
                )
                
                # Clean up
                try:
                    os.remove(installer_path)
                except:
                    pass
                
                self.root.quit()
            else:
                self.log("❌ Erreur lors de l'installation de Python")
                messagebox.showerror(
                    "Erreur",
                    "L'installation de Python a échoué.\n"
                    "Installez-le manuellement depuis python.org"
                )
        except Exception as e:
            self.log(f"❌ Erreur: {e}")
            messagebox.showerror("Erreur", f"Erreur lors du téléchargement: {e}")
        
        self.progress.stop()
        self.install_btn.config(state="normal")
    
    def perform_installation(self):
        """Effectuer l'installation complète"""
        try:
            # Step 1: Copy files
            self.log("📁 Copie des fichiers vers Program Files...")
            self.copy_files()
            
            # Step 2: Install dependencies
            self.log("📦 Installation des bibliothèques...")
            self.install_dependencies()
            
            # Step 3: Create shortcuts
            self.log("🔗 Création des raccourcis...")
            self.create_shortcuts()
            
            # Step 4: Save installation info
            self.log("💾 Sauvegarde des informations d'installation...")
            install_info = {
                "version": "1.0",
                "install_date": Path(self.install_dir).stat().st_mtime if os.path.exists(self.install_dir) else 0,
                "python_version": self.python_version,
                "install_dir": self.install_dir,
                "dependencies": ["pillow", "pynput", "pygame", "pywin32", "winshell"]
            }
            self.save_install_info(install_info)
            
            self.log("")
            self.log("✅ Installation terminée avec succès!")
            
            self.root.after(0, self.progress.stop)
            
            self.root.after(0, lambda: messagebox.showinfo(
                "Installation réussie",
                f"Crosshair Gambler Pro a été installé avec succès!\n\n"
                f"Emplacement: {self.install_dir}\n\n"
                f"Vous pouvez lancer l'application depuis:\n"
                f"- Le Menu Démarrer (recherche Windows)\n"
                f"- Le raccourci sur le Bureau (si créé)"
            ))
            
            # Refresh UI
            self.root.after(0, self.refresh_ui)
            
        except Exception as e:
            self.log(f"❌ Erreur: {e}")
            self.root.after(0, lambda: messagebox.showerror("Erreur", f"Erreur d'installation: {e}"))
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self.install_btn.config(state="normal"))
    
    def copy_files(self):
        """Copier les fichiers vers le dossier d'installation"""
        # Create install directory
        os.makedirs(self.install_dir, exist_ok=True)
        
        # Files to copy
        files_to_copy = [
            "crosshair_gambler.py",
            "import_dialog.py",
            "config.json",
            "icone.png",
            "gambling.MP3"
        ]
        
        # Folders to copy
        folders_to_copy = [
            "saved_crosshairs",
            "crosshair_images"
        ]
        
        # Copy files
        for file in files_to_copy:
            src = os.path.join(self.source_dir, file)
            dst = os.path.join(self.install_dir, file)
            if os.path.exists(src):
                shutil.copy2(src, dst)
                self.log(f"  ✅ Copié: {file}")
        
        # Copy folders
        for folder in folders_to_copy:
            src = os.path.join(self.source_dir, folder)
            dst = os.path.join(self.install_dir, folder)
            if os.path.exists(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
                self.log(f"  ✅ Copié: {folder}/")
    
    def install_dependencies(self):
        """Installer les dépendances Python"""
        dependencies = ["pillow", "pynput", "pygame", "pywin32", "winshell"]
        
        for dep in dependencies:
            self.log(f"  Installation de {dep}...")
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", dep, "--quiet"],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    self.log(f"  ✅ {dep} installé")
                else:
                    self.log(f"  ❌ Erreur avec {dep}")
                    raise Exception(f"Impossible d'installer {dep}")
            except Exception as e:
                raise Exception(f"Erreur d'installation de {dep}: {e}")
    
    def create_shortcuts(self):
        """Créer les raccourcis"""
        try:
            # Create start menu folder
            os.makedirs(self.start_menu_folder, exist_ok=True)
            
            # Start menu shortcut
            start_menu_shortcut = os.path.join(self.start_menu_folder, "Crosshair Gambler Pro.lnk")
            self.create_shortcut(
                start_menu_shortcut,
                os.path.join(self.install_dir, "crosshair_gambler.py"),
                "Crosshair Gambler Pro - Application de viseurs personnalisés"
            )
            self.log(f"  ✅ Raccourci Menu Démarrer créé")
            
            # Desktop shortcut (optional)
            if self.create_desktop_shortcut_var.get():
                self.create_shortcut(
                    self.desktop_shortcut,
                    os.path.join(self.install_dir, "crosshair_gambler.py"),
                    "Crosshair Gambler Pro - Application de viseurs personnalisés"
                )
                self.log(f"  ✅ Raccourci Bureau créé")
                
        except Exception as e:
            self.log(f"  ⚠️ Erreur création raccourcis: {e}")
    
    def create_shortcut(self, shortcut_path, target_path, description):
        """Créer un raccourci Windows"""
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = sys.executable  # Python executable
        shortcut.Arguments = f'"{target_path}"'
        shortcut.WorkingDirectory = self.install_dir
        shortcut.Description = description
        
        # Set icon
        icon_path = os.path.join(self.install_dir, "icone.png")
        if os.path.exists(icon_path):
            # Convert PNG to ICO
            ico_path = os.path.join(self.install_dir, "icone.ico")
            self.convert_png_to_ico(icon_path, ico_path)
            if os.path.exists(ico_path):
                shortcut.IconLocation = ico_path
        
        shortcut.save()
    
    def convert_png_to_ico(self, png_path, ico_path):
        """Convertir PNG en ICO pour l'icône"""
        try:
            from PIL import Image
            img = Image.open(png_path)
            img.save(ico_path, format='ICO', sizes=[(256, 256)])
        except Exception as e:
            self.log(f"  ⚠️ Impossible de convertir l'icône: {e}")
    
    def repair_installation(self):
        """Réparer l'installation"""
        response = messagebox.askyesno(
            "Réparer l'installation",
            "Cela va réinstaller toutes les dépendances.\n\nContinuer ?"
        )
        if not response:
            return
        
        self.progress_frame.pack(fill="x", pady=10)
        self.repair_btn.config(state="disabled")
        self.uninstall_btn.config(state="disabled")
        self.launch_btn.config(state="disabled")
        self.progress.start()
        
        # Run repair in background thread
        thread = threading.Thread(target=self.perform_repair, daemon=True)
        thread.start()

    def perform_repair(self):
        """Effectuer la réparation"""
        try:
            self.log("🔧 Réparation en cours...")
            self.install_dependencies()
            self.log("✅ Réparation terminée!")
            
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: messagebox.showinfo("Réparation réussie", "L'application a été réparée avec succès!"))
            self.root.after(0, self.refresh_ui)
        except Exception as e:
            self.log(f"❌ Erreur: {e}")
            self.root.after(0, lambda: messagebox.showerror("Erreur", f"Erreur de réparation: {e}"))
            self.root.after(0, self.progress.stop)
    
    def uninstall(self):
        """Désinstaller l'application"""
        response = messagebox.askyesno(
            "Désinstallation",
            "Êtes-vous sûr de vouloir désinstaller Crosshair Gambler Pro?\n\n"
            "Les crosshairs sauvegardés seront conservés dans:\n"
            f"{os.path.join(self.install_dir, 'saved_crosshairs')}"
        )
        if not response:
            return
        
        self.progress_frame.pack(fill="x", pady=10)
        self.repair_btn.config(state="disabled")
        self.uninstall_btn.config(state="disabled")
        self.launch_btn.config(state="disabled")
        self.progress.start()
        
        thread = threading.Thread(target=self.perform_uninstall, daemon=True)
        thread.start()
    
    def perform_uninstall(self):
        """Effectuer la désinstallation"""
        try:
            self.log("🗑️ Désinstallation en cours...")
            
            # Remove shortcuts
            if os.path.exists(self.desktop_shortcut):
                os.remove(self.desktop_shortcut)
                self.log("  ✅ Raccourci Bureau supprimé")
            
            if os.path.exists(self.start_menu_folder):
                shutil.rmtree(self.start_menu_folder)
                self.log("  ✅ Raccourci Menu Démarrer supprimé")
            
            # Backup saved crosshairs
            saved_crosshairs_src = os.path.join(self.install_dir, "saved_crosshairs")
            saved_crosshairs_backup = os.path.join(os.path.expanduser("~"), "Desktop", "Crosshair_Gambler_Backup")
            
            if os.path.exists(saved_crosshairs_src):
                shutil.copytree(saved_crosshairs_src, saved_crosshairs_backup, dirs_exist_ok=True)
                self.log(f"  ✅ Crosshairs sauvegardés sur le Bureau")
            
            # Remove installation directory
            if os.path.exists(self.install_dir):
                shutil.rmtree(self.install_dir)
                self.log("  ✅ Fichiers supprimés")
            
            self.log("")
            self.log("✅ Désinstallation terminée!")
            
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: messagebox.showinfo(
                "Désinstallation réussie",
                f"Crosshair Gambler Pro a été désinstallé.\n\n"
                f"Vos crosshairs ont été sauvegardés sur le Bureau:\n"
                f"{saved_crosshairs_backup}"
            ))
            
            self.root.after(0, self.refresh_ui)
            
        except Exception as e:
            self.log(f"❌ Erreur: {e}")
            self.root.after(0, lambda: messagebox.showerror("Erreur", f"Erreur de désinstallation: {e}"))
            self.root.after(0, self.progress.stop)
    
    def launch_app(self):
        """Lancer l'application"""
        app_path = os.path.join(self.install_dir, "crosshair_gambler.py")
        if not os.path.exists(app_path):
            messagebox.showerror(
                "Erreur",
                "Le fichier crosshair_gambler.py est introuvable!"
            )
            return
        
        try:
            subprocess.Popen([sys.executable, app_path], cwd=self.install_dir)
            self.root.quit()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer l'application: {e}")
    
    def run(self):
        """Lancer l'installateur"""
        self.root.mainloop()


if __name__ == "__main__":
    # Vérifier les droits admin AVANT de créer l'interface
    if not is_admin():
        print("Demande des droits administrateur...")
        # Relancer en tant qu'admin sans créer de fenêtre
        run_as_admin()
        # La fonction run_as_admin() fait sys.exit(0) si succès
        # Si on arrive ici, c'est qu'il y a eu une erreur
    else:
        # On a les droits admin, lancer l'installateur
        app = InstallerApp()
        app.run()
