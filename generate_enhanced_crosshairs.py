"""
Enhanced Crosshair Generator - 50 Crosshairs with Advanced Shapes
Generates diverse crosshairs with 17+ different shapes and varied styles
"""

import json
import random
import os
from datetime import datetime

# Create output directory
output_dir = "saved_crosshairs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Extended crosshair styles - 17 different shapes!
styles = [
    # Original styles
    "classic", "cross", "dot", "circle", "square", "T-shape", "plus",
    # NEW geometric shapes
    "triangle", "diamond", "star", "pentagon", "hexagon",
    # NEW tactical shapes
    "arrow", "X-shape", "V-shape", "bracket", "ring"
]

# Extended rich color palette with neon and vibrant colors
colors = [
    # Original colors
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
    "#ff1493",  # Deep pink
    "#7fff00",  # Chartreuse
    "#ffd700",  # Gold
    "#ff69b4",  # Hot pink
    # NEW neon colors
    "#00ff9f",  # Spring green
    "#ff007f",  # Rose
    "#0080ff",  # Azure
    "#ff4500",  # Orange red
    "#adff2f",  # Green yellow
    "#ff1493",  # Deep pink
    "#00ced1",  # Dark turquoise
    "#ff6347",  # Tomato
    "#40e0d0",  # Turquoise
    "#da70d6",  # Orchid
    "#00fa9a",  # Medium spring green
]

def generate_crosshair(index):
    """Generate a single crosshair with varied properties"""
    
    # Determine size profile
    size_roll = random.random()
    
    if size_roll < 0.05:  # 5% tiny
        length_range = (2, 15)
        thickness_range = (1, 3)
    elif size_roll < 0.25:  # 20% small
        length_range = (10, 50)
        thickness_range = (1, 5)
    elif size_roll < 0.60:  # 35% medium (most common)
        length_range = (30, 150)
        thickness_range = (2, 10)
    elif size_roll < 0.85:  # 25% large
        length_range = (100, 500)
        thickness_range = (5, 25)
    elif size_roll < 0.95:  # 10% xlarge
        length_range = (300, 1000)
        thickness_range = (10, 50)
    else:  # 5% fullscreen
        length_range = (9999, 9999)
        thickness_range = (9999, 9999)
    
    # Generate properties with weighted randomization
    length = random.randint(*length_range)
    thickness = random.randint(*thickness_range)
    
    # Random style and color
    style = random.choice(styles)
    color = random.choice(colors)
    
    # Other properties with more variety
    gap = random.randint(0, 40)  # Increased max gap
    outline = random.randint(0, 6)  # Thicker outlines possible
    dot_size = random.randint(1, 20)  # Larger dots possible
    
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
print("🎰 Generating 50 ENHANCED crosshairs with advanced shapes...")
print("=" * 70)

generated_crosshairs = []

for i in range(50):
    crosshair = generate_crosshair(i)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"enhanced_{timestamp}_{i+1:03d}.json"
    filepath = os.path.join(output_dir, filename)
    
    # Save to file
    with open(filepath, 'w') as f:
        json.dump(crosshair, f, indent=2)
    
    generated_crosshairs.append(crosshair)
    
    # Print info with size category
    size_category = ""
    if crosshair["Longueur"] == 9999 or crosshair["Épaisseur"] == 9999:
        size_category = "🔥 FULLSCREEN"
    elif crosshair["Longueur"] > 300:
        size_category = "⭐ X-LARGE"
    elif crosshair["Longueur"] > 100:
        size_category = "📏 LARGE"
    elif crosshair["Longueur"] > 30:
        size_category = "📐 MEDIUM"
    elif crosshair["Longueur"] > 10:
        size_category = "🔸 SMALL"
    else:
        size_category = "🔹 TINY"
    
    print(f"✅ {i+1:3d}. {filename}")
    print(f"     {size_category:15s} | Style: {crosshair['Style']:10s} | "
          f"Color: {crosshair['Couleur']} | T:{crosshair['Épaisseur']:4d} | L:{crosshair['Longueur']:4d}")

print("=" * 70)

# Statistics
styles_used = {}
for ch in generated_crosshairs:
    style = ch['Style']
    styles_used[style] = styles_used.get(style, 0) + 1

print(f"🎉 Successfully generated 50 ENHANCED crosshairs!")
print(f"\n📊 Shape Distribution:")
for style, count in sorted(styles_used.items(), key=lambda x: x[1], reverse=True):
    bar = "█" * count
    print(f"   {style:12s}: {bar} ({count})")

print(f"\n💡 Features:")
print(f"   ✨ {len(styles)} different shapes (classic, triangle, star, diamond, etc.)")
print(f"   🎨 {len(colors)} vibrant colors")
print(f"   📏 6 size profiles (tiny → fullscreen)")
print(f"   🎯 Enhanced randomization for maximum variety")
print(f"\n🎮 Load them in Gambling Crosshair and enjoy!")
