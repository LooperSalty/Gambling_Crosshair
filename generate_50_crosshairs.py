"""
Advanced Crosshair Generator - 50 Crosshairs with Troll/Funny Shapes
Generates diverse crosshairs including normal, extreme, and troll styles
"""

import json
import random
import os
from datetime import datetime

# Create output directory
output_dir = "saved_crosshairs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# All crosshair styles (including some funny repeated names for variation)
styles = [
    "classic", "cross", "dot", "circle", "square", "T-shape", "plus",
    "classic", "cross", "circle",  # Repeat popular ones
]

# Rich color palette
colors = [
    "#00ff00",  # Green
    "#ff0000",  # Red
    "#00ffff",  # Cyan
    "#ffff00",  # Yellow
    "#ff00ff",  # Magenta
    "#ffffff",  # White
    "#ff6600",  # Orange
    "#00ff88",  # Mint
    "#8800ff",  # Purple
    "#ff0088",  # Hot pink
    "#00ffff",  # Aqua
    "#ff1493",  # Deep pink
    "#7fff00",  # Chartreuse
    "#ffd700",  # Gold
    "#ff69b4",  # Hot pink
]

def generate_crosshair(index):
    """Generate a single crosshair with varied properties"""
    
    # Determine crosshair type
    rand_type = random.random()
    
    if rand_type < 0.1:  # 10% full-screen length
        length = 9999
    elif rand_type < 0.2:  # 10% large
        length = random.randint(200, 1000)
    else:  # 80% normal
        length = random.randint(5, min(100, random.randint(5, 200)))
    
    rand_thick = random.random()
    if rand_thick < 0.05:  # 5% full-screen thickness
        thickness = 9999
    elif rand_thick < 0.15:  # 10% very thick
        thickness = random.randint(20, 100)
    else:  # 85% normal
        thickness = random.randint(1, random.randint(2, 15))
    
    # Random style and color
    style = random.choice(styles)
    color = random.choice(colors)
    
    # Other properties
    gap = random.randint(0, 30)
    outline = random.randint(0, 4)
    dot_size = random.randint(1, 12)
    
    crosshair = {
        "Type": "generated",
        "Style": style,
        "Couleur": color,
        "Épaisseur": thickness,
        "Longueur": length,
        "Gap": gap,
        "Contour": outline,
        "Taille point": dot_size
    }
    
    return crosshair

# Generate 50 crosshairs
print("🎰 Generating 50 diverse crosshairs...")
print("=" * 60)

for i in range(50):
    crosshair = generate_crosshair(i)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"crosshair_{timestamp}_{i+1:03d}.json"
    filepath = os.path.join(output_dir, filename)
    
    # Save to file
    with open(filepath, 'w') as f:
        json.dump(crosshair, f, indent=2)
    
    # Print info
    fullscreen_info = []
    if crosshair["Épaisseur"] == 9999:
        fullscreen_info.append("FULL THICKNESS")
    elif crosshair["Épaisseur"] > 50:
        fullscreen_info.append("VERY THICK")
        
    if crosshair["Longueur"] == 9999:
        fullscreen_info.append("FULL LENGTH")
    elif crosshair["Longueur"] > 500:
        fullscreen_info.append("VERY LONG")
    
    fullscreen_str = f" [{', '.join(fullscreen_info)}]" if fullscreen_info else ""
    
    print(f"✅ {i+1:3d}. {filename}")
    print(f"     Style: {crosshair['Style']:10s} | Color: {crosshair['Couleur']} | "
          f"T:{crosshair['Épaisseur']:4d} | L:{crosshair['Longueur']:4d}{fullscreen_str}")

print("=" * 60)
print(f"🎉 Successfully generated 50 crosshairs in '{output_dir}' directory!")
print(f"\n💡 Variety included:")
print(f"   - Normal crosshairs (small/medium)")
print(f"   - Large crosshairs (200-1000 length)")
print(f"   - Full-screen crosshairs (9999)")
print(f"   - Thick crosshairs (20-100)")
print(f"   - Rainbow colors ({len(colors)} colors)")
print(f"\n🎮 Load them in the app and enjoy!")
