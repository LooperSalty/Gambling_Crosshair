"""
Crosshair Code Import Dialog
Supports CS2 and Valorant crosshair codes
"""

import tkinter as tk
from tkinter import messagebox
import re
import base64


class ImportCrosshairDialog:
    """Dialog to import crosshair codes from CS2 or Valorant"""
    
    # Color mappings
    CS2_COLORS = {
        "0": "#ff0000",  # Red
        "1": "#00ff00",  # Green  
        "2": "#ffff00",  # Yellow
        "3": "#0000ff",  # Blue
        "4": "#00ffff",  # Cyan
        "5": "#ffffff",  # White (custom)
    }
    
    VALORANT_COLORS = {
        "0": "#ffffff",  # White
        "1": "#00ff00",  # Green
        "2": "#ffff00",  # Yellow Chartreuse
        "3": "#00ffff",  # Cyan
        "4": "#ff00ff",  # Magenta
        "5": "#ff0000",  # Red
        "6": "#ffa500",  # Orange
        "7": "#ff1493",  # Pink
    }
    
    def __init__(self, parent, callback):
        self.callback = callback
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("📋 Importer Code Crosshair")
        self.dialog.geometry("550x500")
        self.dialog.configure(bg="#1a1a1a")
        self.dialog.resizable(False, False)
        self.dialog.attributes('-topmost', True)
        
        # Title
        title = tk.Label(
            self.dialog,
            text="📋 Importer Code Crosshair",
            font=("Arial", 16, "bold"),
            fg="#00ff00",
            bg="#1a1a1a"
        )
        title.pack(pady=20)
        
        # Instructions
        info = tk.Label(
            self.dialog,
            text="Collez votre code CS2 ou Valorant ci-dessous",
            font=("Arial", 10),
            fg="#ffffff",
            bg="#1a1a1a"
        )
        info.pack(pady=5)
        
        # Code input frame
        input_frame = tk.Frame(self.dialog, bg="#1a1a1a")
        input_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        tk.Label(input_frame, text="Code:", fg="#ffffff", bg="#1a1a1a",
                font=("Arial", 10, "bold")).pack(anchor="w")
        
        # Text area for code
        self.code_text = tk.Text(
            input_frame,
            height=6,
            width=60,
            font=("Consolas", 10),
            bg="#2a2a2a",
            fg="#ffffff",
            insertbackground="#ffffff"
        )
        self.code_text.pack(pady=5)
        
        # Parse button
        parse_btn = tk.Button(
            self.dialog,
            text="🔍 Analyser le Code",
            command=self.parse_code,
            bg="#0066ff",
            fg="#ffffff",
            font=("Arial", 11, "bold"),
            width=20,
            relief="flat",
            cursor="hand2"
        )
        parse_btn.pack(pady=10)
        
        # Result preview
        self.result_frame = tk.Frame(self.dialog, bg="#1a1a1a")
        self.result_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.result_label = tk.Label(
            self.result_frame,
            text="",
            font=("Arial", 9),
            fg="#888888",
            bg="#1a1a1a",
            justify="left"
        )
        self.result_label.pack()
        
        # Buttons
        btn_frame = tk.Frame(self.dialog, bg="#1a1a1a")
        btn_frame.pack(pady=20)
        
        self.import_btn = tk.Button(
            btn_frame,
            text="✅ Importer",
            command=self.import_crosshair,
            bg="#00ff00",
            fg="#000000",
            font=("Arial", 11, "bold"),
            width=12,
            relief="flat",
            cursor="hand2",
            state="disabled"
        )
        self.import_btn.pack(side="left", padx=10)
        
        cancel_btn = tk.Button(
            btn_frame,
            text="❌ Annuler",
            command=self.dialog.destroy,
            bg="#ff0000",
            fg="#ffffff",
            font=("Arial", 11, "bold"),
            width=12,
            relief="flat",
            cursor="hand2"
        )
        cancel_btn.pack(side="left", padx=10)
        
        self.parsed_props = None
    
    def parse_code(self):
        """Parse the entered code"""
        code = self.code_text.get("1.0", "end-1c").strip()
        
        if not code:
            messagebox.showerror("Erreur", "Veuillez entrer un code")
            return
        
        # Try to detect format
        if code.startswith("CSGO-") or "cl_crosshair" in code:
            self.parsed_props = self.parse_cs2_code(code)
            format_name = "CS2"
        elif ";" in code and ("P;" in code or "p;" in code):
            self.parsed_props = self.parse_valorant_code(code)
            format_name = "Valorant"
        else:
            messagebox.showerror("Erreur", "Format de code non reconnu.\\n\\nFormats supportés:\\n- CS2: CSGO-xxxxx ou commandes cl_crosshair...\\n- Valorant: 0;P;c;5;...")
            return
        
        if self.parsed_props:
            # Show preview
            preview_text = f"✅ Code {format_name} détecté !\\n\\n"
            preview_text += f"Style: {self.parsed_props.get('Style', 'N/A')}\\n"
            preview_text += f"Couleur: {self.parsed_props.get('Couleur', 'N/A')}\\n"
            preview_text += f"Épaisseur: {self.parsed_props.get('Épaisseur', 'N/A')}\\n"
            preview_text += f"Longueur: {self.parsed_props.get('Longueur', 'N/A')}\\n"
            preview_text += f"Gap: {self.parsed_props.get('Gap', 'N/A')}"
            
            self.result_label.config(text=preview_text, fg="#00ff00")
            self.import_btn.config(state="normal")
        else:
            messagebox.showerror("Erreur", "Impossible de parser le code")
    
    def parse_cs2_code(self, code):
        """Parse CS2 crosshair code"""
        props = {
            "Type": "generated",
            "Style": "cross",
            "Couleur": "#00ff00",
            "Épaisseur": 2,
            "Longueur": 20,
            "Gap": 5,
            "Contour": 1,
            "Taille point": 2
        }
        
        # Extract parameters from console commands
        # Example: cl_crosshairsize "5"; cl_crosshairthickness "1"
        
        # Size -> Length
        size_match = re.search(r'cl_crosshairsize["\s]+([0-9.]+)', code, re.IGNORECASE)
        if size_match:
            props["Longueur"] = int(float(size_match.group(1)) * 4)  # Scale up
        
        # Thickness
        thick_match = re.search(r'cl_crosshairthickness["\s]+([0-9.]+)', code, re.IGNORECASE)
        if thick_match:
            props["Épaisseur"] = max(1, int(float(thick_match.group(1))))
        
        # Gap
        gap_match = re.search(r'cl_crosshairgap["\s]+([0-9.-]+)', code, re.IGNORECASE)
        if gap_match:
            props["Gap"] = max(0, int(float(gap_match.group(1))))
        
        # Color
        color_match = re.search(r'cl_crosshaircolor["\s]+([0-9]+)', code, re.IGNORECASE)
        if color_match:
            color_code = color_match.group(1)
            props["Couleur"] = self.CS2_COLORS.get(color_code, "#00ff00")
        
        # Dot
        dot_match = re.search(r'cl_crosshairdot["\s]+([01])', code, re.IGNORECASE)
        if dot_match and dot_match.group(1) == "1":
            props["Style"] = "dot"
        
        # Outline
        outline_match = re.search(r'cl_crosshair_outlinethickness["\s]+([0-9.]+)', code, re.IGNORECASE)
        if outline_match:
            props["Contour"] = int(float(outline_match.group(1)))
        
        return props
    
    def parse_valorant_code(self, code):
        """Parse Valorant crosshair code"""
        props = {
            "Type": "generated",
            "Style": "cross",
            "Couleur": "#ffffff",
            "Épaisseur": 2,
            "Longueur": 20,
            "Gap": 5,
            "Contour": 1,
            "Taille point": 2
        }
        
        # Split by semicolon
        parts = code.split(";")
        
        # Parse key-value pairs
        for i in range(0, len(parts) - 1, 2):
            try:
                key = parts[i].strip()
                value = parts[i + 1].strip() if i + 1 < len(parts) else "0"
                
                # Color
                if key == "c":
                    props["Couleur"] = self.VALORANT_COLORS.get(value, "#ffffff")
                
                # Thickness (inner lines)
                elif key == "t" or key == "h":
                    props["Épaisseur"] = max(1, min(10, int(value)))
                
                # Length (inner lines)
                elif key == "0l":
                    props["Longueur"] = int(value) * 5  # Scale up
                
                # Offset (gap)
                elif key == "0o":
                    props["Gap"] = int(value)
                
                # Outline
                elif key == "1b":
                    props["Contour"] = 1 if int(value) == 1 else 0
                    
            except:
                continue
        
        return props
    
    def import_crosshair(self):
        """Import the parsed crosshair"""
        if self.parsed_props:
            self.callback(self.parsed_props)
            self.dialog.destroy()
        else:
            messagebox.showerror("Erreur", "Veuillez d'abord analyser un code")
