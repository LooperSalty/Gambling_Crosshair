"""
Setup Script for Image Crosshairs
Copies generated images to crosshair_images folder and creates JSON files
"""

import os
import shutil
import json
from datetime import datetime

# Create directories
crosshair_images_dir = "crosshair_images"
saved_crosshairs_dir = "saved_crosshairs"

for directory in [crosshair_images_dir, saved_crosshairs_dir]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# List of generated crosshair images
crosshair_images = [
    # Static images
    ("crosshair_sniper_scope_1766347905200.png", "Sniper Scope", "Realistic sniper scope reticle"),
    ("crosshair_neon_grid_1766347918270.png", "Neon Grid", "Cyberpunk neon grid crosshair"),
    ("crosshair_target_lock_1766347936894.png", "Target Lock", "Sci-fi target lock system"),
    ("crosshair_laser_dot_1766347955163.png", "Laser Dot", "Precise red laser dot"),
    ("crosshair_tactical_1766347984363.png", "Tactical Reticle", "Military tactical reticle"),
    ("crosshair_pixel_retro_1766348004658.png", "Pixel Retro", "8-bit pixel art crosshair"),
    ("crosshair_scifi_hud_1766348019334.png", "Sci-Fi HUD", "Futuristic HUD interface"),
    ("crosshair_minimalist_dot_1766348033837.png", "Minimalist Dot", "Elegant minimalist dot"),
    ("crosshair_rainbow_1766348047847.png", "Rainbow", "Vibrant rainbow crosshair"),
    ("crosshair_diamond_reticle_1766348061708.png", "Diamond Reticle", "Diamond-shaped reticle"),
    # Animated GIFs (PNG for now, but will work with GIFs too)
    ("crosshair_pulsing_circle_1766348086504.png", "Pulsing Circle", "Animated pulsing circle"),
    ("crosshair_rotating_star_1766348100647.png", "Rotating Star", "Spinning 5-point star"),
    ("crosshair_glowing_pulse_1766348116885.png", "Glowing Pulse", "Glowing pulse animation"),
    ("crosshair_blinking_dot_1766348139545.png", "Blinking Dot", "Flashing tactical dot"),
    ("crosshair_expanding_circles_1766348154639.png", "Expanding Circles", "Sonar ping effect"),
    ("crosshair_rainbow_wave_1766348167579.png", "Rainbow Wave", "Rainbow wave animation"),
    ("crosshair_matrix_rain_1766348180297.png", "Matrix Rain", "Matrix-style digital rain"),
    ("crosshair_heartbeat_1766348196843.png", "Heartbeat", "ECG heartbeat monitor"),
]

# Source directory where images are generated
source_dir = r"C:\Users\ANAKIN\.gemini\antigravity\brain\ec8233a0-48d5-46ab-92d4-e9ad6151c127"

print("🖼️  Setting up image crosshairs...")
print("=" * 70)

copied_count = 0
skipped_count = 0

for filename, name, description in crosshair_images:
    source_path = os.path.join(source_dir, filename)
    
    # Check if source file exists
    if not os.path.exists(source_path):
        print(f"⚠️  Skipped: {filename} (not found)")
        skipped_count += 1
        continue
    
    # Determine file extension
    ext = os.path.splitext(filename)[1]
    is_gif = ext.lower() == '.gif'
    
    # Copy to crosshair_images folder
    dest_filename = filename
    dest_path = os.path.join(crosshair_images_dir, dest_filename)
    shutil.copy2(source_path, dest_path)
    
    # Create JSON file in saved_crosshairs
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = f"image_{os.path.splitext(dest_filename)[0]}.json"
    json_path = os.path.join(saved_crosshairs_dir, json_filename)
    
    crosshair_data = {
        "Type": "image",
        "Nom": name,
        "Description": description,
        "Fichier_Image": dest_filename,
        "Est_GIF": is_gif
    }
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(crosshair_data, f, indent=2, ensure_ascii=False)
    
    gif_indicator = "🎞️ GIF" if is_gif else "🖼️ PNG"
    print(f"✅ {copied_count+1:2d}. {name:20s} {gif_indicator}")
    print(f"    Image: {dest_filename}")
    print(f"    JSON:  {json_filename}")
    
    copied_count += 1

print("=" * 70)
print(f"🎉 Successfully set up {copied_count} image crosshairs!")
if skipped_count > 0:
    print(f"⚠️  Skipped {skipped_count} images (not found)")
print(f"\n📁 Images saved to: {crosshair_images_dir}/")
print(f"📄 JSON files saved to: {saved_crosshairs_dir}/")
print(f"\n🎮 Load them in Gambling Crosshair and enjoy!")
