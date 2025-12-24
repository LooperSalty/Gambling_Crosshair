# 📦 Guide de l'Installateur Professionnel

## 🎯 Pour les Développeurs

### Créer l'installateur .exe

1. **Ouvrez une invite de commande** dans le dossier du projet
2. **Exécutez** : `build_installer.bat`
3. **Attendez** 1-2 minutes
4. **L'installateur sera créé** : `Crosshair_Gambler_Installer.exe`

```bash
# Commande directe
build_installer.bat
```

### Distribuer l'installateur

Une fois `Crosshair_Gambler_Installer.exe` créé, vous pouvez le distribuer à vos utilisateurs.

**Fichiers à distribuer** :

- ✅ `Crosshair_Gambler_Installer.exe` (l'installateur)
- ✅ Tout le dossier du projet (pour que l'installateur trouve les fichiers)

**Alternative simple** :
Distribuez uniquement le fichier `installer.py` et demandez aux utilisateurs de lancer :

```bash
python installer.py
```

---

## 🎮 Pour les Utilisateurs

### Installation Simple

1. **Double-cliquez** sur `Crosshair_Gambler_Installer.exe`
2. **L'installateur vérifie** :
   - ✅ Si Python est installé
   - ✅ Si la version est compatible (3.10 ou 3.11)
   - ✅ Si l'application est déjà installée
3. **Cliquez sur "INSTALLER"**
4. **Attendez** que l'installation se termine
5. **Lancez l'application** avec le bouton "LANCER"

### Fonctionnalités de l'Installateur

#### 🔍 Vérification Automatique de Python

L'installateur détecte :

- ❌ **Python non installé** → Propose de l'installer automatiquement
- ⚠️ **Version trop ancienne** (< 3.10) → Propose d'installer 3.11.9
- ⚠️ **Version trop récente** (> 3.11) → Propose d'installer 3.11.9
- ✅ **Version compatible** (3.10-3.11) → Continue l'installation

#### 📥 Installation de Python Automatique

Si votre version Python n'est pas compatible :

1. **L'installateur propose** de télécharger Python 3.11.9
2. **Cliquez "Oui"** pour accepter
3. **Attendez 3-5 minutes** (téléchargement + installation)
4. **Relancez l'installateur** après l'installation de Python

#### 🔧 Réparation

Si votre installation est corrompue :

1. **Lancez l'installateur**
2. **Cliquez "RÉPARER"**
3. **Les dépendances seront réinstallées**

#### 🗑️ Désinstallation

Pour désinstaller proprement :

1. **Lancez l'installateur**
2. **Cliquez "DÉSINSTALLER"**
3. **Confirmez**
4. ✅ **Vos crosshairs sauvegardés sont conservés**

---

## 🛠️ Détails Techniques

### Versions Python Supportées

- ✅ **Python 3.10.x** (Recommandé)
- ✅ **Python 3.11.x** (Recommandé)
- ❌ **Python 3.9 et antérieur** (Trop ancien)
- ❌ **Python 3.12+** (Incompatibilités avec pygame/pynput)

### Dépendances Installées

L'installateur installe automatiquement :

- `pillow` - Traitement d'images
- `pynput` - Contrôle clavier/souris
- `pygame` - Sons et musique

### Fichiers de Configuration

L'installateur crée `.install_info.json` qui contient :

```json
{
  "version": "1.0",
  "install_date": "...",
  "python_version": "3.11.9",
  "dependencies": ["pillow", "pynput", "pygame"]
}
```

Ce fichier permet de :

- ✅ Détecter si l'application est installée
- ✅ Afficher la version installée
- ✅ Proposer la réparation si nécessaire

---

## 🚀 Cas d'Usage

### Scénario 1 : Première Installation (Python OK)

1. Double-clic sur l'installateur
2. Python 3.11 détecté ✅
3. Clic sur "INSTALLER"
4. Installation des dépendances (1 minute)
5. ✅ Terminé !

### Scénario 2 : Première Installation (Python manquant)

1. Double-clic sur l'installateur
2. Python non détecté ❌
3. Clic sur "Oui" pour installer Python
4. Téléchargement Python 3.11.9 (3 minutes)
5. **Relancer l'installateur**
6. Clic sur "INSTALLER"
7. ✅ Terminé !

### Scénario 3 : Réparation

1. Double-clic sur l'installateur
2. Application déjà installée détectée
3. Clic sur "RÉPARER"
4. Réinstallation des dépendances
5. ✅ Réparé !

### Scénario 4 : Désinstallation

1. Double-clic sur l'installateur
2. Clic sur "DÉSINSTALLER"
3. Confirmation
4. ✅ Désinstallé (crosshairs conservés)

---

## 💡 Avantages

### Pour les Utilisateurs

- ✅ **Aucune connaissance technique requise**
- ✅ **Installation de Python automatique**
- ✅ **Vérification de compatibilité**
- ✅ **Interface graphique claire**
- ✅ **Réparation facile**
- ✅ **Désinstallation propre**

### Pour les Développeurs

- ✅ **Un seul fichier .exe à distribuer**
- ✅ **Gestion automatique des dépendances**
- ✅ **Détection d'installation existante**
- ✅ **Moins de support utilisateur nécessaire**

---

## 🐛 Dépannage

### L'installateur ne démarre pas

- Vérifiez que vous utilisez **Windows**
- Essayez de lancer `installer.py` directement avec Python

### "Python n'est pas reconnu"

- L'installateur peut installer Python automatiquement
- Ou installez manuellement depuis [python.org](https://www.python.org/downloads/)
- **Cochez "Add Python to PATH"** lors de l'installation manuelle

### Erreur lors de l'installation des dépendances

- Vérifiez votre **connexion Internet**
- Lancez l'installateur en **administrateur**
- Utilisez la fonction "RÉPARER"

### L'application ne se lance pas après installation

- Utilisez la fonction "RÉPARER"
- Vérifiez que `crosshair_gambler.py` existe
- Vérifiez que Python 3.10 ou 3.11 est installé

---

## 📞 Support

En cas de problème :

1. Utilisez d'abord la fonction **"RÉPARER"**
2. Consultez ce fichier README
3. Vérifiez que Python 3.10 ou 3.11 est installé

---

**Développé avec ❤️ pour une installation sans prise de tête** 🎮✨
