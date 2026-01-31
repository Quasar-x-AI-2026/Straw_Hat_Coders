import webview
import json
import os
import time
import subprocess
import tkinter as tk
from PIL import Image, ImageTk # pip install pillow

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UTILS_FOLDER = os.path.join(BASE_DIR, 'startup_utils')
CONFIG_PATH = os.path.join(UTILS_FOLDER, 'config.json')
LOGO_PATH = os.path.join(UTILS_FOLDER, 'logo.png')

class Api:
    def grant(self, is_forever):
        config_data = {"ask_every_time": not is_forever, "permission_granted_forever": is_forever}
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config_data, f, indent=4)
        window.destroy()

    def decline(self):
        window.destroy()
        os._exit(0)

def show_professional_splash():
    """Creates a high-end, frameless logo reveal window."""
    splash = tk.Tk()
    splash.overrideredirect(True) # Removes window borders/buttons
    
    # Window Dimensions
    width, height = 600, 400
    s_width = splash.winfo_screenwidth()
    s_height = splash.winfo_screenheight()
    splash.geometry(f'{width}x{height}+{int(s_width/2 - width/2)}+{int(s_height/2 - height/2)}')
    
    # Load Logo Image
    try:
        img = Image.open(LOGO_PATH)
        img = img.resize((600,600), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(splash, image=photo, bg='white')
        label.image = photo
        label.pack(expand=True)
    except:
        tk.Label(splash, text="AI HEALTH INTELLIGENCE", font=("Arial", 20, "bold"), bg='white').pack(expand=True)

    
    # Show for 7 seconds then destroy
    splash.after(7000, splash.destroy)
    splash.mainloop()

def launch_streamlit():
    print("\n[SYSTEM] Launching Streamlit Server...")
    subprocess.run(["streamlit", "run", "app.py"])

if __name__ == '__main__':
    # 1. Check Config
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
    else:
        config = {"permission_granted_forever": False}

    # 2. Show Consent UI if not already granted
    if not config.get("permission_granted_forever"):
        api = Api()
        html_path = os.path.join(UTILS_FOLDER, 'index.html')
        window = webview.create_window('Permission', html_path, js_api=api, width=500, height=600, resizable=False)
        webview.start()

    # 3. The Professional Logo Reveal (7 Seconds)
    show_professional_splash()

    # 4. Launch the App
    launch_streamlit()