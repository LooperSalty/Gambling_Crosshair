import tkinter as tk
import random
import time
import threading
import json
import os
from datetime import datetime
from tkinter import ttk, colorchooser, filedialog, messagebox
from PIL import Image, ImageTk
from pynput import keyboard
import pygame
from import_dialog import ImportCrosshairDialog

class CrosshairOverlay:
    """Transparent overlay window to display crosshair at screen center"""
    def __init__(self, crosshair_props):
        self.overlay = tk.Toplevel()
        self.overlay.title("Crosshair Overlay")
        
        # Drawing lock to prevent concurrent updates
        self.is_drawing = False
        
        # Make window transparent and always on top
        self.overlay.attributes('-alpha', 1.0)
        self.overlay.attributes('-topmost', True)
        self.overlay.overrideredirect(True)  # Remove window decorations
        
        # Get screen dimensions
        screen_width = self.overlay.winfo_screenwidth()
        screen_height = self.overlay.winfo_screenheight()
        
        # Check if this is a full-screen crosshair
        is_fullscreen = (
            crosshair_props.get("Longueur", 0) >= 9999 or 
            crosshair_props.get("Épaisseur", 0) >= 9999
        )
        
        # Set window size based on crosshair type
        if is_fullscreen:
            # Full screen overlay for full-screen crosshairs
            window_width = screen_width
            window_height = screen_height
            x = 0
            y = 0
        else:
            # Small centered overlay for normal crosshairs
            window_width = 200
            window_height = 200
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
        
        self.overlay.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.current_position = (x, y)
        self.window_size = (window_width, window_height)
        
        # Create transparent canvas
        self.canvas = tk.Canvas(
            self.overlay,
            width=window_width,
            height=window_height,
            bg='black',
            highlightthickness=0,
            cursor="arrow"  # Normal cursor (no drag)
        )
        self.canvas.pack()
        
        # Make background transparent (works on Windows)
        self.overlay.wm_attributes('-transparentcolor', 'black')
        
        # CRITICAL: Make window click-through so mouse clicks pass to game underneath
        # This prevents the overlay from blocking mouse clicks during gameplay
        self.overlay.update_idletasks()  # Ensure window is created
        try:
            import ctypes
            import ctypes.wintypes
            
            # Get window handle
            hwnd = ctypes.windll.user32.GetParent(self.overlay.winfo_id())
            
            # Get current window style
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x00080000
            WS_EX_TRANSPARENT = 0x00000020
            
            # Get current extended style
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            
            # Add click-through flag (WS_EX_TRANSPARENT)
            style = style | WS_EX_LAYERED | WS_EX_TRANSPARENT
            
            # Set new extended style
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
            
            print("Overlay is now click-through! Mouse clicks will pass to the game.")
        except Exception as e:
            print(f"Warning: Could not make overlay click-through: {e}")
        
        # No drag functionality - crosshair stays centered
        self.drag_data = None
        
        # Draw crosshair at center
        self.crosshair_props = crosshair_props
        center_x = window_width // 2
        center_y = window_height // 2
        self.draw_crosshair(center_x, center_y, crosshair_props)
        
        # ESC binding removed - window is click-through so can't be closed by clicking
        # User must use the "Afficher/Masquer Overlay" button to close
    
    def start_drag(self, event):
        """Start dragging the overlay"""
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
    
    def on_drag(self, event):
        """Drag the overlay"""
        deltax = event.x - self.drag_data["x"]
        deltay = event.y - self.drag_data["y"]
        x = self.overlay.winfo_x() + deltax
        y = self.overlay.winfo_y() + deltay
        self.overlay.geometry(f"+{x}+{y}")
        self.current_position = (x, y)
    
    def stop_drag(self, event):
        """Stop dragging"""
        pass
        
    def update_crosshair(self, props):
        """Update the overlay with new crosshair"""
        # Prevent concurrent updates
        if self.is_drawing:
            return
        
        self.is_drawing = True
        try:
            self.crosshair_props = props
            
            # Clear canvas completely - multiple passes to ensure clean slate
            self.canvas.delete("all")
            if hasattr(self.canvas, 'image'):
                self.canvas.image = None
            
            # Force immediate update
            self.canvas.update()
            
            # Small delay to ensure canvas is cleared
            time.sleep(0.001)
            
            # Redraw at center
            center_x = self.window_size[0] // 2
            center_y = self.window_size[1] // 2
            self.draw_crosshair(center_x, center_y, props)
            
            # Force display update
            self.canvas.update_idletasks()
        finally:
            self.is_drawing = False
        
    def draw_crosshair(self, cx, cy, props):
        """Draw crosshair based on properties"""
        # Check if it's an image (PNG or GIF)
        if props.get("Type") == "image":
            image_path = props.get("ImagePath")
            if image_path:
                try:
                    img = Image.open(image_path)
                    
                    # Check if it's an animated GIF
                    if hasattr(img, 'is_animated') and img.is_animated:
                        # Extract all frames
                        self._animate_gif(cx, cy, image_path)
                        return
                    else:
                        # Static image (PNG or single-frame GIF)
                        # Resize to fit in overlay
                        img.thumbnail((150, 150), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img)
                        self.canvas.create_image(cx, cy, image=photo)
                        # Keep reference to prevent garbage collection
                        self.canvas.image = photo
                        return
                except Exception as e:
                    print(f"Error loading image: {e}")
                    pass
        
        style = props.get("Style", "cross")
        color = props.get("Couleur", "#00ff00")
        thickness = props.get("Épaisseur", 2)
        length = props.get("Longueur", 20) 
        gap = props.get("Gap", 5)
        outline = props.get("Contour", 1)
        dot_size = props.get("Taille point", 2)
        
        # Draw outline if needed
        if outline > 0:
            self._draw_crosshair_shape(cx, cy, style, "#000000", 
                                      thickness + outline * 2, length, gap, dot_size + outline * 2)
        
        # Draw main crosshair
        self._draw_crosshair_shape(cx, cy, style, color, thickness, length, gap, dot_size)
    
    def _animate_gif(self, cx, cy, gif_path):
        """Animate a GIF crosshair"""
        try:
            img = Image.open(gif_path)
            
            # Extract frames
            frames = []
            durations = []
            
            for frame_num in range(img.n_frames):
                img.seek(frame_num)
                # Copy frame and resize
                frame = img.copy()
                frame.thumbnail((150, 150), Image.Resampling.LANCZOS)
                frames.append(frame)
                # Get frame duration (in milliseconds)
                durations.append(img.info.get('duration', 100))
            
            # Store frames for animation
            self.gif_frames = frames
            self.gif_durations = durations
            self.gif_center = (cx, cy)
            self.gif_current_frame = 0
            
            # Start animation
            self._update_gif_frame()
            
        except Exception as e:
            print(f"Error animating GIF: {e}")
    
    def _update_gif_frame(self):
        """Update to next GIF frame"""
        if not hasattr(self, 'gif_frames') or not self.gif_frames:
            return
        
        try:
            # Clear canvas
            self.canvas.delete("all")
            
            # Get current frame
            frame = self.gif_frames[self.gif_current_frame]
            duration = self.gif_durations[self.gif_current_frame]
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(frame)
            
            # Draw frame
            cx, cy = self.gif_center
            self.canvas.create_image(cx, cy, image=photo)
            
            # Keep reference
            self.canvas.image = photo
            
            # Move to next frame
            self.gif_current_frame = (self.gif_current_frame + 1) % len(self.gif_frames)
            
            # Schedule next frame update
            self.overlay.after(duration, self._update_gif_frame)
            
        except Exception as e:
            print(f"Error updating GIF frame: {e}")
        
    def _draw_crosshair_shape(self, cx, cy, style, color, thickness, length, gap, dot_size):
        """Draw crosshair shape"""
        # Check if full-screen dimensions
        is_fullscreen_length = (length >= 9999)
        is_fullscreen_thickness = (thickness >= 9999)
        
        # Get screen dimensions for full-screen crosshairs
        screen_width = self.overlay.winfo_screenwidth()
        screen_height = self.overlay.winfo_screenheight()
        
        # For full-screen, draw from edge to edge
        if is_fullscreen_thickness:
            # Use a very large thickness that spans the screen
            thickness = max(screen_width, screen_height)
        
        if style == "classic" or style == "cross":
            # Draw vertical and horizontal lines
            if is_fullscreen_length:
                # Vertical line - full screen
                self.canvas.create_line(cx, 0, cx, screen_height,
                                      fill=color, width=thickness, capstyle=tk.BUTT)
                # Horizontal line - full screen
                self.canvas.create_line(0, cy, screen_width, cy,
                                      fill=color, width=thickness, capstyle=tk.BUTT)
            else:
                # Normal crosshair with gap
                # Vertical lines
                self.canvas.create_line(cx, cy - gap - length, cx, cy - gap,
                                      fill=color, width=thickness, capstyle=tk.BUTT)
                self.canvas.create_line(cx, cy + gap, cx, cy + gap + length,
                                      fill=color, width=thickness, capstyle=tk.BUTT)
                # Horizontal lines
                self.canvas.create_line(cx - gap - length, cy, cx - gap, cy,
                                      fill=color, width=thickness, capstyle=tk.BUTT)
                self.canvas.create_line(cx + gap, cy, cx + gap + length, cy,
                                      fill=color, width=thickness, capstyle=tk.BUTT)
                              
        elif style == "dot":
            self.canvas.create_oval(cx - dot_size, cy - dot_size, 
                                  cx + dot_size, cy + dot_size, 
                                  fill=color, outline=color)
        elif style == "circle":
            radius = length if not is_fullscreen_length else min(screen_width, screen_height) // 4
            self.canvas.create_oval(cx - radius, cy - radius, 
                                  cx + radius, cy + radius, 
                                  outline=color, width=thickness)
            self.canvas.create_oval(cx - 2, cy - 2, cx + 2, cy + 2, 
                                  fill=color, outline=color)
        elif style == "square":
            size = length if not is_fullscreen_length else min(screen_width, screen_height) // 4
            self.canvas.create_rectangle(cx - size, cy - size, 
                                        cx + size, cy + size, 
                                        outline=color, width=thickness)
            self.canvas.create_oval(cx - 2, cy - 2, cx + 2, cy + 2, 
                                  fill=color, outline=color)
        elif style == "T-shape":
            # Vertical line
            if is_fullscreen_length:
                self.canvas.create_line(cx, 0, cx, screen_height,
                                      fill=color, width=thickness, capstyle=tk.BUTT)
            else:
                self.canvas.create_line(cx, cy - gap, cx, cy - gap - length, 
                                      fill=color, width=thickness, capstyle=tk.BUTT)
            
            # Horizontal line (full width for T-shape)
            if is_fullscreen_length:
                self.canvas.create_line(0, cy, screen_width, cy,
                                      fill=color, width=thickness, capstyle=tk.BUTT)
            else:
                self.canvas.create_line(cx - gap, cy, cx - gap - length, cy, 
                                      fill=color, width=thickness, capstyle=tk.BUTT)
                self.canvas.create_line(cx + gap, cy, cx + gap + length, cy, 
                                      fill=color, width=thickness, capstyle=tk.BUTT)
        elif style == "plus":
            # Vertical line from top to bottom
            if is_fullscreen_length:
                self.canvas.create_line(cx, 0, cx, screen_height, 
                                      fill=color, width=thickness, capstyle=tk.BUTT)
            else:
                self.canvas.create_line(cx, cy - length, cx, cy + length, 
                                      fill=color, width=thickness, capstyle=tk.BUTT)
            
            # Horizontal line from left to right
            if is_fullscreen_length:
                self.canvas.create_line(0, cy, screen_width, cy, 
                                      fill=color, width=thickness, capstyle=tk.BUTT)
            else:
                self.canvas.create_line(cx - length, cy, cx + length, cy, 
                                      fill=color, width=thickness, capstyle=tk.BUTT)
    
    def close(self):
        """Close the overlay window"""
        self.overlay.destroy()


class SavedCrosshairsDialog:
    """Dialog to view and load saved crosshairs"""
    def __init__(self, parent, callback):
        self.callback = callback
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("📁 Crosshairs Sauvegardés")
        self.dialog.geometry("600x500")
        self.dialog.configure(bg="#1a1a1a")
        
        self.saved_dir = "saved_crosshairs"
        
        # Title
        title = tk.Label(
            self.dialog,
            text="📁 Mes Crosshairs Sauvegardés",
            font=("Arial", 16, "bold"),
            fg="#00ff00",
            bg="#1a1a1a"
        )
        title.pack(pady=20)
        
        # Listbox frame
        list_frame = tk.Frame(self.dialog, bg="#1a1a1a")
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Listbox
        self.listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            bg="#2a2a2a",
            fg="#ffffff",
            font=("Arial", 11),
            selectbackground="#0066ff",
            height=15
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Load saved crosshairs
        self.load_crosshairs_list()
        
        # Buttons
        btn_frame = tk.Frame(self.dialog, bg="#1a1a1a")
        btn_frame.pack(pady=20)
        
        load_btn = tk.Button(btn_frame, text="✅ Charger", command=self.load_selected,
                            bg="#00ff00", fg="#000000", font=("Arial", 11, "bold"),
                            width=12, relief="flat", cursor="hand2")
        load_btn.pack(side="left", padx=10)
        
        delete_btn = tk.Button(btn_frame, text="🗑️ Supprimer", command=self.delete_selected,
                              bg="#ff6600", fg="#ffffff", font=("Arial", 11, "bold"),
                              width=12, relief="flat", cursor="hand2")
        delete_btn.pack(side="left", padx=10)
        
        close_btn = tk.Button(btn_frame, text="❌ Fermer", command=self.dialog.destroy,
                             bg="#ff0000", fg="#ffffff", font=("Arial", 11, "bold"),
                             width=12, relief="flat", cursor="hand2")
        close_btn.pack(side="left", padx=10)
    
    def load_crosshairs_list(self):
        """Load list of saved crosshairs"""
        self.listbox.delete(0, tk.END)
        
        if not os.path.exists(self.saved_dir):
            self.listbox.insert(tk.END, "Aucun crosshair sauvegardé")
            return
        
        files = [f for f in os.listdir(self.saved_dir) if f.endswith('.json')]
        if not files:
            self.listbox.insert(tk.END, "Aucun crosshair sauvegardé")
            return
        
        for file in sorted(files, reverse=True):
            self.listbox.insert(tk.END, file.replace('.json', ''))
    
    def load_selected(self):
        """Load the selected crosshair"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un crosshair")
            return
        
        filename = self.listbox.get(selection[0])
        if filename == "Aucun crosshair sauvegardé":
            return
        
        filepath = os.path.join(self.saved_dir, f"{filename}.json")
        try:
            with open(filepath, 'r') as f:
                props = json.load(f)
            self.callback(props)
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le crosshair: {e}")
    
    def delete_selected(self):
        """Delete the selected crosshair"""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un crosshair")
            return
        
        filename = self.listbox.get(selection[0])
        if filename == "Aucun crosshair sauvegardé":
            return
        
        if messagebox.askyesno("Confirmation", f"Supprimer '{filename}' ?"):
            filepath = os.path.join(self.saved_dir, f"{filename}.json")
            try:
                os.remove(filepath)
                self.load_crosshairs_list()
                messagebox.showinfo("Succès", "Crosshair supprimé")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de supprimer: {e}")


class ManualCrosshairDialog:
    """Dialog to create a crosshair manually"""
    def __init__(self, parent, callback):
        self.callback = callback
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("✏️ Créer un Crosshair Manuel")
        self.dialog.geometry("400x600")
        self.dialog.configure(bg="#1a1a1a")
        self.dialog.resizable(False, False)
        self.dialog.attributes('-topmost', True)  # Keep dialog on top
        
        # Selected color and image
        self.selected_color = "#00ff00"
        self.image_path = None
        self.crosshair_type = "generated"  # or "image"
        
        # Create form
        self.create_form()
        
    def create_form(self):
        """Create the manual input form"""
        # Title
        title = tk.Label(
            self.dialog,
            text="✏️ Créer un Crosshair",
            font=("Arial", 16, "bold"),
            fg="#00ff00",
            bg="#1a1a1a"
        )
        title.pack(pady=20)
        
        # Type selection
        type_frame = tk.Frame(self.dialog, bg="#1a1a1a")
        type_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(type_frame, text="Type:", fg="#ffffff", bg="#1a1a1a",
                font=("Arial", 10, "bold")).pack(anchor="w")
        
        self.type_var = tk.StringVar(value="generated")
        
        type_btn_frame = tk.Frame(type_frame, bg="#1a1a1a")
        type_btn_frame.pack(pady=5)
        
        tk.Radiobutton(type_btn_frame, text="Généré", variable=self.type_var, 
                      value="generated", bg="#1a1a1a", fg="#ffffff", 
                      selectcolor="#2a2a2a", command=self.on_type_change,
                      font=("Arial", 10)).pack(side="left", padx=10)
        
        tk.Radiobutton(type_btn_frame, text="Image PNG", variable=self.type_var, 
                      value="image", bg="#1a1a1a", fg="#ffffff", 
                      selectcolor="#2a2a2a", command=self.on_type_change,
                      font=("Arial", 10)).pack(side="left", padx=10)
        
        # Image selection (initially hidden)
        self.image_frame = tk.Frame(self.dialog, bg="#1a1a1a")
        self.image_frame.pack(pady=10, padx=20, fill="x")
        
        self.image_label = tk.Label(self.image_frame, text="Aucune image sélectionnée",
                                    fg="#888888", bg="#1a1a1a", font=("Arial", 9))
        self.image_label.pack()
        
        image_btn = tk.Button(self.image_frame, text="📁 Choisir une Image PNG",
                             command=self.choose_image, bg="#2a2a2a", fg="#ffffff",
                             relief="flat", cursor="hand2", font=("Arial", 10))
        image_btn.pack(pady=5)
        
        # Form frame for generated crosshair
        self.form_frame = tk.Frame(self.dialog, bg="#1a1a1a")
        self.form_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Style
        tk.Label(self.form_frame, text="Style:", fg="#ffffff", bg="#1a1a1a", 
                font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=10)
        self.style_var = tk.StringVar(value="cross")
        style_combo = ttk.Combobox(self.form_frame, textvariable=self.style_var, 
                                   values=["classic", "cross", "dot", "circle", "square", "T-shape", "plus"],
                                   state="readonly", width=25)
        style_combo.grid(row=0, column=1, pady=10, padx=10)
        
        # Color
        tk.Label(self.form_frame, text="Couleur:", fg="#ffffff", bg="#1a1a1a",
                font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=10)
        color_frame = tk.Frame(self.form_frame, bg="#1a1a1a")
        color_frame.grid(row=1, column=1, pady=10, padx=10, sticky="w")
        
        self.color_preview = tk.Label(color_frame, text="  ████  ", fg=self.selected_color, 
                                      bg="#1a1a1a", font=("Arial", 12))
        self.color_preview.pack(side="left")
        
        color_btn = tk.Button(color_frame, text="Choisir", command=self.choose_color,
                             bg="#2a2a2a", fg="#ffffff", relief="flat")
        color_btn.pack(side="left", padx=10)
        
        # Thickness
        tk.Label(self.form_frame, text="Épaisseur (1-1000 ou 9999):", fg="#ffffff", bg="#1a1a1a",
                font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=10)
        self.thickness_var = tk.IntVar(value=2)
        self.thickness_spin = tk.Spinbox(self.form_frame, from_=1, to=9999, textvariable=self.thickness_var,
                                   width=24, increment=1)
        self.thickness_spin.grid(row=2, column=1, pady=10, padx=10)
        
        # Length
        tk.Label(self.form_frame, text="Longueur (5-1000 ou 9999):", fg="#ffffff", bg="#1a1a1a",
                font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", pady=10)
        self.length_var = tk.IntVar(value=20)
        length_spin = tk.Spinbox(self.form_frame, from_=5, to=9999, textvariable=self.length_var,
                                width=24, increment=1)
        length_spin.grid(row=3, column=1, pady=10, padx=10)
        
        # Gap
        tk.Label(self.form_frame, text="Gap (0-30):", fg="#ffffff", bg="#1a1a1a",
                font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="w", pady=10)
        self.gap_var = tk.IntVar(value=5)
        gap_spin = tk.Spinbox(self.form_frame, from_=0, to=30, textvariable=self.gap_var,
                             width=24)
        gap_spin.grid(row=4, column=1, pady=10, padx=10)
        
        # Outline
        tk.Label(self.form_frame, text="Contour (0-5):", fg="#ffffff", bg="#1a1a1a",
                font=("Arial", 10, "bold")).grid(row=5, column=0, sticky="w", pady=10)
        self.outline_var = tk.IntVar(value=1)
        outline_spin = tk.Spinbox(self.form_frame, from_=0, to=5, textvariable=self.outline_var,
                                 width=24)
        outline_spin.grid(row=5, column=1, pady=10, padx=10)
        
        # Dot size
        tk.Label(self.form_frame, text="Taille point (1-10):", fg="#ffffff", bg="#1a1a1a",
                font=("Arial", 10, "bold")).grid(row=6, column=0, sticky="w", pady=10)
        self.dot_size_var = tk.IntVar(value=2)
        dot_size_spin = tk.Spinbox(self.form_frame, from_=1, to=10, textvariable=self.dot_size_var,
                                   width=24)
        dot_size_spin.grid(row=6, column=1, pady=10, padx=10)
        
        # Buttons
        btn_frame = tk.Frame(self.dialog, bg="#1a1a1a")
        btn_frame.pack(pady=20)
        
        create_btn = tk.Button(btn_frame, text="✅ Créer", command=self.create_crosshair,
                              bg="#00ff00", fg="#000000", font=("Arial", 12, "bold"),
                              width=12, relief="flat", cursor="hand2")
        create_btn.pack(side="left", padx=10)
        
        cancel_btn = tk.Button(btn_frame, text="❌ Annuler", command=self.dialog.destroy,
                              bg="#ff0000", fg="#ffffff", font=("Arial", 12, "bold"),
                              width=12, relief="flat", cursor="hand2")
        cancel_btn.pack(side="left", padx=10)
        
        # Initial state
        self.on_type_change()
        
    def on_type_change(self):
        """Handle type radio button change"""
        if self.type_var.get() == "image":
            self.form_frame.pack_forget()
            self.image_frame.pack(pady=10, padx=20, fill="x")
        else:
            self.image_frame.pack_forget()
            self.form_frame.pack(pady=10, padx=20, fill="both", expand=True)
    
    def choose_image(self):
        """Open file dialog to choose PNG or GIF image"""
        # Ensure dialog stays on top
        self.dialog.lift()
        self.dialog.focus_force()
        
        filename = filedialog.askopenfilename(
            title="Sélectionner une image PNG ou GIF",
            filetypes=[("Images", "*.png *.gif"), ("PNG files", "*.png"), ("GIF files", "*.gif"), ("All files", "*.*")],
            parent=self.dialog
        )
        
        # Bring dialog back to front
        self.dialog.lift()
        self.dialog.focus_force()
        
        if filename:
            import os
            import shutil
            
            # Create crosshair_images directory if it doesn't exist
            images_dir = "crosshair_images"
            if not os.path.exists(images_dir):
                os.makedirs(images_dir)
            
            # Get filename and copy to crosshair_images folder
            basename = os.path.basename(filename)
            
            # If file has same name, add timestamp to avoid overwrite
            dest_path = os.path.join(images_dir, basename)
            if os.path.exists(dest_path) and os.path.abspath(filename) != os.path.abspath(dest_path):
                # Add timestamp to make unique
                name, ext = os.path.splitext(basename)
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                basename = f"{name}_{timestamp}{ext}"
                dest_path = os.path.join(images_dir, basename)
            
            # Copy file to crosshair_images folder (only if not already there)
            if os.path.abspath(filename) != os.path.abspath(dest_path):
                try:
                    shutil.copy2(filename, dest_path)
                    print(f"Image copied to: {dest_path}")
                except Exception as e:
                    print(f"Error copying image: {e}")
                    # Use original path if copy fails
                    dest_path = filename
            
            # Use the path in crosshair_images folder
            self.image_path = dest_path
            self.image_label.config(text=f"✓ {basename}", fg="#00ff00")
        
    def choose_color(self):
        """Open color chooser dialog"""
        # Keep parent dialog on top temporarily
        self.dialog.attributes('-topmost', False)
        
        color = colorchooser.askcolor(initialcolor=self.selected_color, title="Choisir une couleur")
        
        # Restore parent dialog to top
        self.dialog.attributes('-topmost', True)
        self.dialog.lift()
        self.dialog.focus_force()
        
        if color[1]:
            self.selected_color = color[1]
            self.color_preview.config(fg=self.selected_color)
    
    def create_crosshair(self):
        """Create crosshair with manual properties"""
        if self.type_var.get() == "image":
            if not self.image_path:
                messagebox.showerror("Erreur", "Veuillez sélectionner une image PNG")
                return
            props = {
                "Type": "image",
                "ImagePath": self.image_path
            }
        else:
            props = {
                "Type": "generated",
                "Style": self.style_var.get(),
                "Couleur": self.selected_color,
                "Épaisseur": self.thickness_var.get(),
                "Longueur": self.length_var.get(),
                "Gap": self.gap_var.get(),
                "Contour": self.outline_var.get(),
                "Taille point": self.dot_size_var.get()
            }
        self.callback(props)
        self.dialog.destroy()


class HotkeyConfigDialog:
    """Dialog to configure global hotkey"""
    def __init__(self, parent, current_key, callback):
        self.callback = callback
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("⌨️ Configuration Touche")
        self.dialog.geometry("400x250")
        self.dialog.configure(bg="#1a1a1a")
        self.dialog.resizable(False, False)
        
        self.selected_key = current_key
        self.waiting_for_key = False
        
        # Title
        title = tk.Label(
            self.dialog,
            text="⌨️ Choisir la Touche",
            font=("Arial", 16, "bold"),
            fg="#00ff00",
            bg="#1a1a1a"
        )
        title.pack(pady=20)
        
        # Instructions
        info = tk.Label(
            self.dialog,
            text="Cliquez sur 'Capturer' puis appuyez sur n'importe quelle touche\npour définir le raccourci global",
            font=("Arial", 9),
            fg="#ffffff",
            bg="#1a1a1a",
            justify="center"
        )
        info.pack(pady=10)
        
        # Current key display
        self.key_label = tk.Label(
            self.dialog,
            text=f"Touche actuelle: {current_key}",
            font=("Arial", 12, "bold"),
            fg="#ffff00",
            bg="#1a1a1a"
        )
        self.key_label.pack(pady=10)
        
        # Capture button
        self.capture_btn = tk.Button(
            self.dialog,
            text="🎯 Capturer une touche",
            command=self.start_capture,
            bg="#0066ff",
            fg="#ffffff",
            font=("Arial", 11, "bold"),
            width=20,
            relief="flat",
            cursor="hand2"
        )
        self.capture_btn.pack(pady=10)
        
        # Buttons
        btn_frame = tk.Frame(self.dialog, bg="#1a1a1a")
        btn_frame.pack(pady=20)
        
        self.save_btn = tk.Button(btn_frame, text="✅ Sauvegarder", command=self.save_key,
                            bg="#00ff00", fg="#000000", font=("Arial", 11, "bold"),
                            width=12, relief="flat", cursor="hand2")
        self.save_btn.pack(side="left", padx=10)
        
        cancel_btn = tk.Button(btn_frame, text="❌ Annuler", command=self.dialog.destroy,
                              bg="#ff0000", fg="#ffffff", font=("Arial", 11, "bold"),
                              width=12, relief="flat", cursor="hand2")
        cancel_btn.pack(side="left", padx=10)
    
    def start_capture(self):
        """Start capturing key press with pynput"""
        self.waiting_for_key = True
        self.capture_btn.config(text="⏳ Appuyez sur une touche ou un bouton de souris...", bg="#ff6600")
        self.key_label.config(text="En attente...", fg="#ff6600")
        
        # Use pynput to capture ANY key or mouse button
        from pynput import keyboard as kb, mouse
        
        def on_key_press(key):
            try:
                # Get key name
                if hasattr(key, 'char') and key.char:
                    key_name = key.char
                elif hasattr(key, 'name'):
                    key_name = key.name
                else:
                    key_name = str(key)
                
                self.captured_key = key_name
                self.dialog.after(0, self.finish_capture)
                return False  # Stop listener
            except:
                return True
        
        def on_mouse_click(x, y, button, pressed):
            if pressed:
                button_name = f"mouse_{button.name}"
                self.captured_key = button_name
                self.dialog.after(0, self.finish_capture)
                return False  # Stop listener
        
        # Start listeners
        self.key_listener = kb.Listener(on_press=on_key_press)
        self.mouse_listener = mouse.Listener(on_click=on_mouse_click)
        self.key_listener.start()
        self.mouse_listener.start()
    
    def finish_capture(self):
        """Finish the capture process"""
        self.waiting_for_key = False
        self.selected_key = self.captured_key
        self.capture_btn.config(text="🎯 Capturer une touche", bg="#0066ff")
        self.key_label.config(text=f"Touche capturée: {self.selected_key}", fg="#00ff00")
        
        # Stop listeners if they exist
        if hasattr(self, 'key_listener'):
            try:
                self.key_listener.stop()
            except:
                pass
        if hasattr(self, 'mouse_listener'):
            try:
                self.mouse_listener.stop()
            except:
                pass
        
        # Auto-save the captured key immediately
        self.callback(self.selected_key)
        
        # Highlight the save button and update text to indicate saved
        if hasattr(self, 'save_btn'):
            self.save_btn.config(text="✅ Sauvegardé ! Fermer", bg="#00aa00")
        
        # Show confirmation message
        messagebox.showinfo("Touche Sauvegardée", f"La touche '{self.selected_key}' a été sauvegardée automatiquement !\n\nVous pouvez fermer cette fenêtre ou capturer une autre touche.")
    
    def save_key(self):
        """Save the selected key"""
        self.callback(self.selected_key)
        self.dialog.destroy()


class CrosshairGambler:
    def __init__(self, root):
        self.root = root
        self.root.title("🎰 Crosshair Gambler Pro")
        self.root.geometry("850x800")
        self.root.configure(bg="#0a0a0a")
        
        self.overlay_window = None
        # NO global overlay_position - each crosshair has its own!
        
        # Initialize pygame mixer for MP3 playback
        pygame.mixer.init()
        self.sound_file = "gambling.MP3"
        
        # Load configuration (including hotkey)
        self.config_file = "config.json"
        self.load_config()
        
        self.hotkey_listener = None
        self.is_roulette_running = False
        self.saved_dir = "saved_crosshairs"
        
        # Create saved directory if it doesn't exist
        if not os.path.exists(self.saved_dir):
            os.makedirs(self.saved_dir)
        
        # NO key bindings for space/enter - only global hotkey
        
        # Start global hotkey listener
        self.start_hotkey_listener()
        
        # Title with gradient effect
        title_frame = tk.Frame(root, bg="#0a0a0a")
        title_frame.pack(pady=25)
        
        title_label = tk.Label(
            title_frame, 
            text="🎰 CROSSHAIR GAMBLER PRO 🎰",
            font=("Arial", 26, "bold"),
            fg="#00ff88",
            bg="#0a0a0a"
        )
        title_label.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="Générateur de Crosshairs Ultime avec Roulette Casino",
            font=("Arial", 10, "italic"),
            fg="#888888",
            bg="#0a0a0a"
        )
        subtitle.pack()
        
        # Instructions with modern style
        instruction_label = tk.Label(
            root,
            text="Utilisez le hotkey global (configurez-le ci-dessous) pour lancer la roulette !",
            font=("Arial", 11),
            fg="#cccccc",
            bg="#0a0a0a"
        )
        instruction_label.pack(pady=8)
        
        # Hotkey info with modern badge style
        hotkey_frame = tk.Frame(root, bg="#1a1a2a", relief="ridge", bd=2)
        hotkey_frame.pack(pady=10, padx=20, fill="x")
        
        self.hotkey_label = tk.Label(
            hotkey_frame,
            text=f"🎹 Touche globale: {self.hotkey} (cliquez pour changer)",
            font=("Arial", 11, "bold"),
            fg="#ffdd00",
            bg="#1a1a2a",
            cursor="hand2",
            pady=10
        )
        self.hotkey_label.pack()
        self.hotkey_label.bind('<Button-1>', lambda e: self.open_hotkey_config())
        
        # Buttons frame 1 - Main actions with gradient backgrounds
        btn_frame1 = tk.Frame(root, bg="#0a0a0a")
        btn_frame1.pack(pady=12)
        
        manual_btn = tk.Button(
            btn_frame1,
            text="✏️ Créer Manuellement",
            command=self.open_manual_dialog,
            bg="#2563eb",
            fg="#ffffff",
            font=("Arial", 11, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            activebackground="#1d4ed8"
        )
        manual_btn.pack(side="left", padx=8)
        
        import_btn = tk.Button(
            btn_frame1,
            text="📋 Importer Code",
            command=self.open_import_dialog,
            bg="#f59e0b",
            fg="#ffffff",
            font=("Arial", 11, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            activebackground="#d97706"
        )
        import_btn.pack(side="left", padx=8)
        
        save_btn = tk.Button(
            btn_frame1,
            text="💾 Sauvegarder",
            command=self.save_current_crosshair,
            bg="#7c3aed",
            fg="#ffffff",
            font=("Arial", 11, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            activebackground="#6d28d9"
        )
        save_btn.pack(side="left", padx=8)
        
        load_btn = tk.Button(
            btn_frame1,
            text="📁 Charger",
            command=self.open_saved_crosshairs,
            bg="#059669",
            fg="#ffffff",
            font=("Arial", 11, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            activebackground="#047857"
        )
        load_btn.pack(side="left", padx=8)
        
        # Buttons frame 2 - Overlay controls
        btn_frame2 = tk.Frame(root, bg="#0a0a0a")
        btn_frame2.pack(pady=8)
        
        overlay_btn = tk.Button(
            btn_frame2,
            text="🎯 Afficher/Masquer Overlay",
            command=self.toggle_overlay,
            bg="#ea580c",
            fg="#ffffff",
            font=("Arial", 11, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            activebackground="#c2410c"
        )
        overlay_btn.pack(side="left", padx=8)
        
        center_btn = tk.Button(
            btn_frame2,
            text="📍 Centrer Overlay",
            command=self.center_overlay,
            bg="#0891b2",
            fg="#ffffff",
            font=("Arial", 11, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            activebackground="#0e7490"
        )
        center_btn.pack(side="left", padx=8)
        
        # Canvas for crosshair with modern border
        canvas_frame = tk.Frame(root, bg="#1a1a2a", relief="solid", bd=3)
        canvas_frame.pack(pady=20)
        
        self.canvas = tk.Canvas(
            canvas_frame,
            width=450,
            height=450,
            bg="#15151f",
            highlightthickness=0
        )
        self.canvas.pack(padx=3, pady=3)
        
        # Info frame with modern design
        self.info_frame = tk.Frame(root, bg="#0a0a0a")
        self.info_frame.pack(pady=15)
        
        # Crosshair properties
        self.crosshair_props = {}
        
        # Generate first crosshair
        self.generate_random_crosshair()
        
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.hotkey = config.get("hotkey", "F1")
            else:
                self.hotkey = "F1"
        except:
            self.hotkey = "F1"
    
    def save_config(self):
        """Save configuration to file"""
        try:
            config = {"hotkey": self.hotkey}
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def save_current_crosshair(self):
        """Save current crosshair to file"""
        if not self.crosshair_props:
            messagebox.showwarning("Attention", "Aucun crosshair à sauvegarder")
            return
        
        # Save crosshair properties (no position - always centered)
        save_data = self.crosshair_props.copy()
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"crosshair_{timestamp}.json"
        filepath = os.path.join(self.saved_dir, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(save_data, f, indent=2)
            messagebox.showinfo("Succès", f"Crosshair sauvegardé :\n{filename}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder : {e}")
    
    def open_saved_crosshairs(self):
        """Open dialog to view and load saved crosshairs"""
        SavedCrosshairsDialog(self.root, self.load_crosshair)
    
    def load_crosshair(self, props):
        """Load a crosshair from saved data"""
        self.crosshair_props = props
        self.redraw_crosshair()
        
        # Always recreate overlay with proper size for this crosshair
        if self.overlay_window and self.overlay_window.overlay.winfo_exists():
            self.overlay_window.close()
        
        # Create overlay with correct size (will auto-detect full-screen)
        self.overlay_window = CrosshairOverlay(self.crosshair_props)
    
    def start_hotkey_listener(self):
        """Start listening for global hotkey - supports keyboard and mouse"""
        from pynput import keyboard as kb, mouse
        
        def on_key_press(key):
            try:
                # Get key name
                if hasattr(key, 'char') and key.char:
                    key_name = key.char
                elif hasattr(key, 'name'):
                    key_name = key.name
                else:
                    key_name = str(key).replace("Key.", "")
                
                if key_name.lower() == self.hotkey.lower():
                    self.root.after(0, self.hotkey_triggered)
            except:
                pass
            return True
        
        def on_mouse_click(x, y, button, pressed):
            if pressed:
                button_name = f"mouse_{button.name}"
                if button_name == self.hotkey:
                    self.root.after(0, self.hotkey_triggered)
            return True
        
        # Stop existing listeners
        if self.hotkey_listener:
            try:
                self.hotkey_listener.stop()
            except:
                pass
        
        # Start new listeners
        if self.hotkey.startswith("mouse_"):
            # Mouse button hotkey
            self.hotkey_listener = mouse.Listener(on_click=on_mouse_click)
        else:
            # Keyboard hotkey
            self.hotkey_listener = kb.Listener(on_press=on_key_press)
        
        self.hotkey_listener.start()
    
    def hotkey_triggered(self):
        """Called when global hotkey is pressed"""
        # Generate random crosshair with animation on screen
        self.start_roulette_animation()
    
    def open_hotkey_config(self):
        """Open hotkey configuration dialog"""
        HotkeyConfigDialog(self.root, self.hotkey, self.set_hotkey)
    
    def set_hotkey(self, key):
        """Set new hotkey and save to config"""
        self.hotkey = key
        self.hotkey_label.config(text=f"🎹 Touche globale: {self.hotkey} (cliquez pour changer)")
        self.save_config()  # Save to file
        self.start_hotkey_listener()
        messagebox.showinfo("Succès", f"Touche globale changée et sauvegardée: {key}")
    
    def open_manual_dialog(self):
        """Open dialog to create crosshair manually"""
        ManualCrosshairDialog(self.root, self.set_manual_crosshair)
    
    def set_manual_crosshair(self, props):
        """Set crosshair with manual properties"""
        self.crosshair_props = props
        self.redraw_crosshair()
        
        # Check if we need to recreate overlay (size type changed)
        if self.overlay_window and self.overlay_window.overlay.winfo_exists():
            # Check if this is a full-screen crosshair
            is_fullscreen = (
                props.get("Longueur", 0) >= 9999 or 
                props.get("Épaisseur", 0) >= 9999
            )
            
            # Recreate overlay if size type changed
            # (simple way: always recreate if overlay exists)
            self.overlay_window.close()
            self.overlay_window = CrosshairOverlay(self.crosshair_props)
        elif self.overlay_window:
            # Overlay exists but window was destroyed, recreate
            self.overlay_window = CrosshairOverlay(self.crosshair_props)
    
    def open_import_dialog(self):
        """Open dialog to import crosshair code"""
        ImportCrosshairDialog(self.root, self.set_manual_crosshair)
        
    def toggle_overlay(self):
        """Toggle overlay window"""
        if self.overlay_window and self.overlay_window.overlay.winfo_exists():
            self.overlay_window.close()
            self.overlay_window = None
        else:
            # Always create centered overlay
            self.overlay_window = CrosshairOverlay(self.crosshair_props)
    
    def center_overlay(self):
        """Center the overlay on screen"""
        if self.overlay_window and self.overlay_window.overlay.winfo_exists():
            # Get screen center
            screen_width = self.overlay_window.overlay.winfo_screenwidth()
            screen_height = self.overlay_window.overlay.winfo_screenheight()
            x = (screen_width - 200) // 2
            y = (screen_height - 200) // 2
            
            # Move overlay to center
            self.overlay_window.overlay.geometry(f"+{x}+{y}")
            self.overlay_window.current_position = (x, y)
        else:
            messagebox.showinfo("Info", "Ouvrez d'abord l'overlay avec le bouton 'Afficher/Masquer Overlay'")
    
    def start_roulette_animation(self):
        """Start the roulette animation with sound ON SCREEN"""
        if self.is_roulette_running:
            return
        
        # Make sure overlay is open (always centered)
        if not self.overlay_window or not self.overlay_window.overlay.winfo_exists():
            self.overlay_window = CrosshairOverlay(self.crosshair_props)
        
        self.is_roulette_running = True
        
        # Play MP3 sound
        try:
            if os.path.exists(self.sound_file):
                pygame.mixer.music.load(self.sound_file)
                pygame.mixer.music.play()
        except Exception as e:
            print(f"Sound error: {e}")
        
        # Start animation in thread
        thread = threading.Thread(target=self._roulette_animation)
        thread.start()
    
    def _roulette_animation(self):
        """Animate the roulette spinning ON SCREEN"""
        duration = 6.0  # seconds (match MP3 duration)
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # Generate random crosshair
            temp_props = self._generate_temp_crosshair_props()
            
            # Update overlay on screen (stays centered)
            if self.overlay_window and self.overlay_window.overlay.winfo_exists():
                try:
                    # Direct synchronous update
                    self.overlay_window.update_crosshair(temp_props)
                except Exception as e:
                    print(f"Overlay update error: {e}")
                    pass
            
            # Also update main window
            try:
                self.root.after(0, lambda p=temp_props: self._update_display(p))
            except:
                pass
            
            # Calculate delay based on progress (slow down over time)
            elapsed = time.time() - start_time
            progress = elapsed / duration
            delay = 0.05 + (progress * 0.3)  # Slow from 50ms to 350ms
            
            time.sleep(delay)
            
            # Add small extra delay to ensure previous draw is complete
            time.sleep(0.01)
        
        # Final crosshair
        time.sleep(0.1)  # Pause before final
        self.root.after(0, self.generate_random_crosshair)
        self.is_roulette_running = False
    
    def _load_saved_crosshairs(self):
        """Load all saved crosshairs from the saved directory"""
        saved_crosshairs = []
        
        if not os.path.exists(self.saved_dir):
            return saved_crosshairs
        
        try:
            files = [f for f in os.listdir(self.saved_dir) if f.endswith('.json')]
            for file in files:
                filepath = os.path.join(self.saved_dir, file)
                try:
                    with open(filepath, 'r') as f:
                        props = json.load(f)
                        saved_crosshairs.append(props)
                except:
                    pass  # Skip corrupted files
        except:
            pass
        
        return saved_crosshairs
    
    def _generate_temp_crosshair_props(self):
        """Generate temporary crosshair properties for animation - includes saved crosshairs"""
        # Load saved crosshairs
        saved_crosshairs = self._load_saved_crosshairs()
        
        # 60% chance to use saved crosshair if any exist, 40% generate new
        if saved_crosshairs and random.random() < 0.6:
            return random.choice(saved_crosshairs)
        
        # Generate random crosshair
        styles = ["classic", "cross", "dot", "circle", "square", "T-shape", "plus"]
        colors = ["#00ff00", "#ff0000", "#00ffff", "#ffff00", "#ff00ff", "#ffffff", "#ff6600"]
        
        return {
            "Type": "generated",
            "Style": random.choice(styles),
            "Couleur": random.choice(colors),
            "Épaisseur": random.randint(1, 8),
            "Longueur": random.randint(5, 40),
            "Gap": random.randint(0, 20),
            "Contour": random.randint(0, 3),
            "Taille point": random.randint(1, 8)
        }
    
    def _update_display(self, props):
        """Update the main display with temporary crosshair"""
        self.canvas.delete("all")
        center_x, center_y = 200, 200
        self.canvas.create_line(center_x, 0, center_x, 400, fill="#444444", dash=(2, 2))
        self.canvas.create_line(0, center_y, 400, center_y, fill="#444444", dash=(2, 2))
        
        outline = props.get("Contour", 0)
        if outline > 0:
            self.draw_crosshair(center_x, center_y, "#000000",
                              props.get("Épaisseur", 2) + outline * 2,
                              props.get("Taille point", 2) + outline * 2,
                              props)
        
        self.draw_crosshair(center_x, center_y,
                          props.get("Couleur", "#00ff00"),
                          props.get("Épaisseur", 2),
                          props.get("Taille point", 2),
                          props)
        
    def generate_random_crosshair(self):
        """Generate a random crosshair - includes saved crosshairs"""
        # Load saved crosshairs
        saved_crosshairs = self._load_saved_crosshairs()
        
        # 60% chance to use saved crosshair if any exist, 40% generate new
        if saved_crosshairs and random.random() < 0.6:
            self.crosshair_props = random.choice(saved_crosshairs)
        else:
            # Generate random crosshair
            styles = ["classic", "cross", "dot", "circle", "square", "T-shape", "plus"]
            colors = ["#00ff00", "#ff0000", "#00ffff", "#ffff00", "#ff00ff", "#ffffff", "#ff6600"]
            
            style = random.choice(styles)
            color = random.choice(colors)
            thickness = random.randint(1, 8)
            length = random.randint(5, 40)
            gap = random.randint(0, 20)
            outline = random.randint(0, 3)
            dot_size = random.randint(1, 8)
            
            self.crosshair_props = {
                "Type": "generated",
                "Style": style,
                "Couleur": color,
                "Épaisseur": thickness,
                "Longueur": length,
                "Gap": gap,
                "Contour": outline,
                "Taille point": dot_size
            }
        
        self.redraw_crosshair()
        
        # Recreate overlay if it exists (to handle size changes)
        if self.overlay_window and self.overlay_window.overlay.winfo_exists():
            self.overlay_window.close()
            self.overlay_window = CrosshairOverlay(self.crosshair_props)
        
    def redraw_crosshair(self):
        """Redraw crosshair on canvas"""
        # Clear canvas
        self.canvas.delete("all")
        
        # Check if it's an image
        if self.crosshair_props.get("Type") == "image":
            image_path = self.crosshair_props.get("ImagePath")
            if image_path:
                try:
                    img = Image.open(image_path)
                    img.thumbnail((300, 300), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.canvas.create_image(200, 200, image=photo)
                    self.canvas.image = photo  # Keep reference
                    self.update_info()
                    return
                except Exception as e:
                    print(f"Error loading image: {e}")
        
        # Draw background crosshair reference
        center_x, center_y = 200, 200
        self.canvas.create_line(center_x, 0, center_x, 400, fill="#444444", dash=(2, 2))
        self.canvas.create_line(0, center_y, 400, center_y, fill="#444444", dash=(2, 2))
        
        # Draw outline if needed
        outline = self.crosshair_props.get("Contour", 0)
        if outline > 0:
            self.draw_crosshair(center_x, center_y, "#000000", 
                              self.crosshair_props.get("Épaisseur", 2) + outline * 2,
                              self.crosshair_props.get("Taille point", 2) + outline * 2,
                              self.crosshair_props)
        
        # Draw main crosshair
        self.draw_crosshair(center_x, center_y, 
                          self.crosshair_props.get("Couleur", "#00ff00"),
                          self.crosshair_props.get("Épaisseur", 2),
                          self.crosshair_props.get("Taille point", 2),
                          self.crosshair_props)
        
        # Update info
        self.update_info()
        
    def draw_crosshair(self, cx, cy, color, thickness, dot_size, props=None):
        """Draw crosshair based on style"""
        if props is None:
            props = self.crosshair_props
            
        style = props.get("Style", "cross")
        length = props.get("Longueur", 20)
        gap = props.get("Gap", 5)
        
        if style == "classic" or style == "cross":
            self.canvas.create_line(cx, cy - gap, cx, cy - gap - length, 
                                  fill=color, width=thickness, capstyle=tk.BUTT)
            self.canvas.create_line(cx, cy + gap, cx, cy + gap + length, 
                                  fill=color, width=thickness, capstyle=tk.BUTT)
            self.canvas.create_line(cx - gap, cy, cx - gap - length, cy, 
                                  fill=color, width=thickness, capstyle=tk.BUTT)
            self.canvas.create_line(cx + gap, cy, cx + gap + length, cy, 
                                  fill=color, width=thickness, capstyle=tk.BUTT)
        elif style == "dot":
            self.canvas.create_oval(cx - dot_size, cy - dot_size, 
                                  cx + dot_size, cy + dot_size, 
                                  fill=color, outline=color)
        elif style == "circle":
            radius = length
            self.canvas.create_oval(cx - radius, cy - radius, 
                                  cx + radius, cy + radius, 
                                  outline=color, width=thickness)
            self.canvas.create_oval(cx - 2, cy - 2, cx + 2, cy + 2, 
                                  fill=color, outline=color)
        elif style == "square":
            size = length
            self.canvas.create_rectangle(cx - size, cy - size, 
                                        cx + size, cy + size, 
                                        outline=color, width=thickness)
            self.canvas.create_oval(cx - 2, cy - 2, cx + 2, cy + 2, 
                                  fill=color, outline=color)
        elif style == "T-shape":
            self.canvas.create_line(cx, cy - gap, cx, cy - gap - length, 
                                  fill=color, width=thickness, capstyle=tk.BUTT)
            self.canvas.create_line(cx - gap, cy, cx - gap - length, cy, 
                                  fill=color, width=thickness, capstyle=tk.BUTT)
            self.canvas.create_line(cx + gap, cy, cx + gap + length, cy, 
                                  fill=color, width=thickness, capstyle=tk.BUTT)
        elif style == "plus":
            self.canvas.create_line(cx, cy - length, cx, cy + length, 
                                  fill=color, width=thickness, capstyle=tk.BUTT)
            self.canvas.create_line(cx - length, cy, cx + length, cy, 
                                  fill=color, width=thickness, capstyle=tk.BUTT)
    
    def update_info(self):
        """Update the info display with current crosshair properties"""
        # Clear previous info
        for widget in self.info_frame.winfo_children():
            widget.destroy()
        
        # Check if image type
        if self.crosshair_props.get("Type") == "image":
            import os
            image_path = self.crosshair_props.get("ImagePath", "")
            label = tk.Label(
                self.info_frame,
                text=f"Type: Image PNG - {os.path.basename(image_path)}",
                font=("Arial", 11, "bold"),
                fg="#00ff00",
                bg="#1a1a1a"
            )
            label.pack(pady=5)
            return
        
        # Create info labels for generated crosshair
        row = 0
        col = 0
        for prop, value in self.crosshair_props.items():
            if prop == "Type":
                continue
            if prop == "Couleur":
                label = tk.Label(
                    self.info_frame,
                    text=f"{prop}: ",
                    font=("Arial", 10, "bold"),
                    fg="#00ff00",
                    bg="#1a1a1a"
                )
                label.grid(row=row, column=col, sticky="w", padx=5)
                
                color_box = tk.Label(
                    self.info_frame,
                    text="  ██  ",
                    font=("Arial", 10),
                    fg=value,
                    bg="#1a1a1a"
                )
                color_box.grid(row=row, column=col+1, sticky="w")
                
                value_label = tk.Label(
                    self.info_frame,
                    text=value,
                    font=("Arial", 10),
                    fg="#ffffff",
                    bg="#1a1a1a"
                )
                value_label.grid(row=row, column=col+2, sticky="w", padx=5)
            else:
                # Check if value is full-screen
                display_value = value
                if prop in ["Épaisseur", "Longueur"] and value >= 9999:
                    display_value = f"{value} 🖥️ PLEIN ÉCRAN"
                
                label = tk.Label(
                    self.info_frame,
                    text=f"{prop}: {display_value}",
                    font=("Arial", 10),
                    fg="#ffffff",
                    bg="#1a1a1a"
                )
                label.grid(row=row, column=col, columnspan=3, sticky="w", padx=5)
            
            row += 1
            if row > 3:
                row = 0
                col += 3
    
    def on_closing(self):
        """Clean up when closing the application"""
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        if self.overlay_window:
            self.overlay_window.close()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = CrosshairGambler(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
