"""
Script to generate 20 random crosshairs for Gambling Crosshair

This script creates a variety of crosshairs including:
- Generated crosshairs with random properties
- Some with full-screen dimensions
"""

import json
import random
import os
from datetime import datetime

# Create output directory if it doesn't exist
output_dir = "saved_crosshairs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Crosshair styles
styles = ["classic", "cross", "dot", "circle", "square", "T-shape", "plus"]

# Color palette
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
]

def generate_random_crosshair(index):
    """Generate a random crosshair with varied properties"""
    
    # 20% chance of full-screen dimensions
    use_fullscreen_length = random.random() < 0.2
    use_fullscreen_thickness = random.random() < 0.15
    
    # Generate properties
    style = random.choice(styles)
    color = random.choice(colors)
    
    # Thickness: either normal (1-1000) or full-screen (9999)
    if use_fullscreen_thickness:
        thickness = 9999
    else:
        thickness = random.randint(1, min(100, random.randint(1, 1000)))  # Weighted toward smaller values
    
    # Length: either normal (5-1000) or full-screen (9999)
    if use_fullscreen_length:
        length = 9999
    else:
        length = random.randint(5, min(200, random.randint(5, 1000)))  # Weighted toward smaller values
    
    gap = random.randint(0, 20)
    outline = random.randint(0, 3)
    dot_size = random.randint(1, 8)
    
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

# Generate 20 crosshairs
print("🎰 Generating 20 random crosshairs...")
print("=" * 50)

for i in range(20):
    crosshair = generate_random_crosshair(i)
    
    # Generate unique filename with timestamp and index
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"crosshair_{timestamp}_{i+1:02d}.json"
    filepath = os.path.join(output_dir, filename)
    
    # Save to file
    with open(filepath, 'w') as f:
        json.dump(crosshair, f, indent=2)
    
    # Print info
    fullscreen_info = []
    if crosshair["Épaisseur"] == 9999:
        fullscreen_info.append("FULL THICKNESS")
    if crosshair["Longueur"] == 9999:
        fullscreen_info.append("FULL LENGTH")
    
    fullscreen_str = f" [{', '.join(fullscreen_info)}]" if fullscreen_info else ""
    
    print(f"✅ {i+1:2d}. {filename}")
    print(f"    Style: {crosshair['Style']:10s} | Color: {crosshair['Couleur']} | "
          f"Thickness: {crosshair['Épaisseur']:4d} | Length: {crosshair['Longueur']:4d}{fullscreen_str}")

print("=" * 50)
print(f"🎉 Successfully generated 20 crosshairs in '{output_dir}' directory!")
print(f"\n💡 Tip: 3 crosshairs have full-screen dimensions for variety!")
