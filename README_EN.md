# 🎰 Crosshair Gambler Pro

![Application Interface](appli.png)

![Demo Animation](gif_demo.gif)

Ultimate Python application for generating random crosshairs with casino effects and transparent overlay!

## 🎮 Features

- **7+ crosshair styles** : Classic, Cross, Dot, Circle, Square, T-shape, Plus, and more!
- **PNG & GIF support** : Use your own images or animated GIFs as crosshairs
- **Full-screen crosshairs** : Lines that span your entire screen (length/thickness 9999)
- **Code import** : Import crosshair codes directly from CS2 and Valorant
- **Casino roulette animation** : 6-second animation with MP3 sound
- **Customizable global hotkey** : Trigger random crosshair anywhere
- **Save/Load library** : Complete library of your favorite crosshairs
- **Fixed transparent overlay** : Always centered, click-through for gaming

## 🚀 Installation

### Requirements

- Python 3.6+
- Pygame, Pillow, pynput

### Install dependencies

```bash
pip install pillow pynput pygame
```

## 💻 Usage

```bash
python crosshair_gambler.py
```

### ⌨️ Global Hotkey

1. Click the yellow **"Global Key"** text to change the key
2. Click **"Capture"** and press any key (keyboard or mouse)
3. The key is **automatically saved** in `config.json`
4. Press your key anywhere to trigger the roulette!

### 📋 Import Crosshair Codes

Click **"📋 Import Code"** to import codes from games:

#### Counter-Strike 2 (CS2)

Format: Console commands

```
cl_crosshairsize "5"; cl_crosshairthickness "1"; cl_crosshairgap "0"; cl_crosshaircolor "1"
```

#### Valorant

Format: Profile code

```
0;P;c;5;h;0;f;0;0l;4;0o;2;0a;1;0f;0;1b;0
```

### ✏️ Manual Creation

**Available options**:

- **Type** : Generated, PNG Image, or GIF Animation
- **Style** : 7+ different styles
- **Color** : Custom color picker
- **Thickness** : 1-1000 or 9999 (full-screen)
- **Length** : 5-1000 or 9999 (full-screen)
- **Gap, Outline, Dot size** : Customizable

**Tip** : Check **"📏 Full screen"** for crosshairs that span the entire screen!

### 🎯 Transparent Overlay

- **Click-through enabled** : Mouse clicks pass through to your game
- Always **centered** (cannot be moved)
- Auto-sizing:
  - 200x200 for normal crosshairs
  - Full screen for 9999 crosshairs
- Close with **"🎯 Show/Hide Overlay"** button

## 🎮 Hiding Game Crosshair

### Counter-Strike 2 (CS2)

**Console (temporary)**:

```
cl_crosshairalpha 0
```

**Permanent (autoexec.cfg)**:

```
cl_crosshairalpha 0
cl_crosshair_drawoutline 0
```

**Quick toggle**:

```
bind "p" "toggle cl_crosshairalpha 0 255"
```

File location: `C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg\autoexec.cfg`

### Valorant

**Settings → Crosshair**:

1. Open settings (ESC)
2. Go to **Crosshair**
3. Set **Opacity** to **0**
4. Or disable **Show Inner Lines** and **Show Outer Lines**

**Alternative**: Create a Valorant profile with invisible crosshair and toggle between profiles.

### Call of Duty (Modern Warfare / Warzone)

**In-game**:

1. **Options** → **General**
2. Go to **Crosshair**
3. Select **Crosshair Type** : **Disabled**

**Or**:

1. **Options** → **Graphics**
2. Find **Crosshair Opacity**
3. Set to **0%**

**Note**: Varies by Call of Duty version. Look for "Crosshair", "Reticle" or "Sight Opacity".

### Fortnite

**Disable native crosshair**:

1. Launch **Fortnite**
2. Open **Settings** (ESC)
3. Go to **HUD and User Interface**
4. Disable **"Custom Crosshair"** or **"Show Crosshair"**

**Alternative with opacity**:

1. In **HUD** settings
2. Look for **"Crosshair Opacity"**
3. Set to **0%**

#### 🎯 Complete Fortnite Guide

##### Initial Setup

1. **Launch the app**: `RUN_APP.bat`
2. **Load a crosshair**: Click "📂 Load Crosshair"
3. **Disable Fortnite crosshair**: Follow steps above
4. **Launch Fortnite**: Overlay stays visible on top of the game

##### 🎲 In-Game Roulette

The signature feature: **change crosshair during your matches**!

**Configure your key**:

1. Click "🎹 Global Key: F1"
2. Click "🎯 Capture a key"
3. Press **F2**, **F3**, **F4** or a **mouse side button**
4. **Avoid F1** (Fortnite menu) and **Tab/Esc**

**During match**:

- Press your key → 6-second animation → Random new crosshair! 🎰

##### 🏆 Recommended Crosshairs

**For competitive gameplay**:

- **Minimalist Dot**: Ultra-precise point
- **Laser Dot**: Classic red dot
- **Classic (small)**: Length 15-30px, Thickness 2-4px
- **Colors**: Green/Cyan (good visibility)

**For fun**:

- **Rainbow**: Multicolor rainbow 🌈
- **Pulsing Circle**: Pulsing animation
- **Star (fullscreen)**: Giant star ⭐

**"Roulette Challenge" Mode**:

- Change crosshair **after each elimination**!
- Test your adaptability with random crosshairs

##### ⚡ Tips

- ✅ **Click-through**: Your clicks pass through the overlay
- ✅ **FPS impact**: Nearly none (very light overlay)
- ✅ **Compatible**: Full screen and windowed mode
- 🎨 **Colors by map**: Red/Magenta on green environments, Green/Cyan elsewhere
- 📐 **Centering**: Drag-and-drop overlay to adjust position

## 🎨 Crosshair Styles

- **Classic/Cross** : Cross with gap
- **Dot** : Central dot
- **Circle** : Circle + dot
- **Square** : Square + dot
- **T-shape** : T shape
- **Plus** : Cross without gap
- **PNG Image** : Your image
- **GIF Animation** : Animated GIF

## 🎲 Full-Screen Crosshairs

**Length 9999** : Vertical/horizontal lines edge-to-edge
**Thickness 9999** : Ultra-wide bars covering screen

Perfect for:

- Maximum visibility
- Dramatic visual effects
- Complete screen markers

## 💾 Saving

- Click **"💾 Save"**
- JSON file in `saved_crosshairs/`
- Format: `crosshair_YYYYMMDD_HHMMSS.json`
- All parameters preserved

## 📁 Library

- Click **"📁 Load"**
- Complete list of your crosshairs
- Delete unwanted crosshairs
- Sorted by date

## ⚙️ Configuration

- **Hotkey** : Saved in `config.json`
- **Animation** : 6 seconds
- **Sound** : `gambling.MP3` (customizable)
- **Overlay** : Always on top, transparent, centered, **click-through**

## 📝 Technical Notes

- **OS** : Windows only
- **Permissions** : Global keyboard listener (pynput)
- **Image formats** : PNG with transparency, Animated GIFs
- **Thread-safe** : Async animation and sound
- **Click-through** : Uses Windows WS_EX_TRANSPARENT flag

## 🎯 Use Cases

✅ Test different crosshairs for FPS games
✅ Custom crosshairs overlay
✅ Import pro player codes
✅ Create extreme crosshairs (full-screen)
✅ Have fun with casino effect

## 🔧 Crosshair Generator

Included script: `generate_crosshairs.py`

```bash
python generate_crosshairs.py
```

Generates 20 varied random crosshairs in `saved_crosshairs/`.

---

**Developed with ❤️ for the FPS community** 🎮🎰✨

Have fun and find your perfect crosshair!
