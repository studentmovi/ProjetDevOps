# ====================================================
#  IMPORTS
# ====================================================
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import json
import datetime
import threading
import subprocess

# Ajout du chemin pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ===== Utils =====
from utils.appStyles import AppStyles
from utils.font_manager import FontManager   # 🔤 FONT MANAGER

# ===== Views =====
from views.home_view import HomeView
from views.student_view import StudentView
from views.events_view import EventsView
from views.settings_view import SettingsView

# ===== Controllers / Popups =====
from controller.ExcelImportController import ExcelImportController
from popups.EventFormPopup import EventFormPopup


# ====================================================
#  MODE
# ====================================================
DEV_MODE = not getattr(sys, "frozen", False)

# ====================================================
#  CONFIG MAJ
# ====================================================
UPDATE_DELAY_DAYS = 7


# ====================================================
#  GESTION ÉTAT MAJ
# ====================================================
def get_update_state():
    path = os.path.join(os.path.dirname(__file__), "update_state.json")
    if not os.path.exists(path):
        return {"ignored_since": None}
    with open(path, "r") as f:
        return json.load(f)


def save_update_state(state):
    path = os.path.join(os.path.dirname(__file__), "update_state.json")
    with open(path, "w") as f:
        json.dump(state, f)


def should_force_update(state):
    if not state["ignored_since"]:
        return False
    ignored = datetime.datetime.fromisoformat(state["ignored_since"])
    return (datetime.datetime.now() - ignored).days >= UPDATE_DELAY_DAYS


# ====================================================
#  SPLASH SCREEN
# ====================================================
def show_splash(root):
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    splash.configure(bg="#1e1e1e")

    w, h = 420, 220
    x = (splash.winfo_screenwidth() - w) // 2
    y = (splash.winfo_screenheight() - h) // 2
    splash.geometry(f"{w}x{h}+{x}+{y}")

    tk.Label(
        splash,
        text="🎓 TripSchool",
        font=("Segoe UI", 22, "bold"),
        fg="white",
        bg="#1e1e1e"
    ).pack(pady=(45, 10))

    tk.Label(
        splash,
        text="Chargement de l'application…",
        font=("Segoe UI", 11),
        fg="#cccccc",
        bg="#1e1e1e"
    ).pack()

    splash.update()
    return splash


# ====================================================
#  APPLICATION PRINCIPALE
# ====================================================
class MainApplication:
    def __init__(self):
        # ====================================================
        #  ROOT
        # ====================================================
        self.root = tk.Tk()

        # 🔤 POLICE GLOBALE (ICI ET NULLE PART AILLEURS)
        self.font_manager = FontManager(self.root)

        # Splash
        self.splash = show_splash(self.root)

        # Icône
        icon = os.path.join(os.path.dirname(__file__), "assets", "logo.ico")
        try:
            self.root.iconbitmap(icon)
        except Exception:
            pass

        # ====================================================
        #  STYLES (COULEURS / LAYOUT)
        # ====================================================
        self.styles = AppStyles()
        self.styles.configure_ttk_style(self.root)
        self.styles.configure_window(self.root, "🎓 TripSchool - Gestion Événements")

        # Fenêtre
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        self.root.state("zoomed")

        # ====================================================
        #  NAVIGATION
        # ====================================================
        self.current_view = None
        self.views = {}

        # Controller Excel global (home)
        self.excel_import_controller = ExcelImportController(self.root)

        # UI
        self.setup_ui()
        self.show_home()

        # Fin splash
        self.root.after(100, self.splash.destroy)

        # Update
        self.check_update_background()

    # ====================================================
    #  UI
    # ====================================================
    def setup_ui(self):
        nav = self.styles.create_header_frame(self.root, padding="10")
        nav.pack(fill="x", side="top")

        ttk.Label(nav, text="🎓 Gestion Scolaire", style="Header.TLabel").pack(side="left")

        btns = ttk.Frame(nav, style="Header.TFrame")
        btns.pack(side="right")

        ttk.Button(btns, text="🏠 Accueil", command=self.show_home, style="Secondary.TButton").pack(side="left", padx=5)
        ttk.Button(btns, text="👥 Élèves", command=self.show_students, style="Secondary.TButton").pack(side="left", padx=5)
        ttk.Button(btns, text="📅 Événements", command=self.show_events, style="Secondary.TButton").pack(side="left", padx=5)
        ttk.Button(btns, text="⚙️ Paramètres", command=self.show_settings, style="Light.TButton").pack(side="left")

        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(fill="both", expand=True)

    # ====================================================
    #  VUES
    # ====================================================
    def switch_view(self, name):
        if self.current_view:
            self.current_view.hide()

        if name not in self.views:
            if name == "home":
                self.views[name] = HomeView(self.content_frame, self.styles, self)
            elif name == "students":
                self.views[name] = StudentView(self.content_frame, self.styles)
            elif name == "events":
                self.views[name] = EventsView(self.content_frame, self.styles)
            elif name == "settings":
                from views.settings_view import SettingsView
                self.views[name] = SettingsView(self.content_frame, self.styles, self)

            if hasattr(self.views[name], "create_widgets"):
                self.views[name].create_widgets()

        self.current_view = self.views[name]
        self.current_view.show()

    def show_home(self): self.switch_view("home")
    def show_students(self): self.switch_view("students")
    def show_events(self): self.switch_view("events")
    def show_settings(self): self.switch_view("settings")

    # ====================================================
    #  HOME CALLBACKS
    # ====================================================
    def open_students_from_home(self):
        self.show_students()

    def import_students_excel(self):
        self.excel_import_controller.start_import_process()

    def create_event_from_home(self):
        EventFormPopup(
            self.root,
            on_save_callback=self.refresh_home_after_event
        )

    def refresh_home_after_event(self):
        if "home" in self.views:
            self.views["home"].create_widgets()

    # ====================================================
    #  VERSION
    # ====================================================
    def get_local_version(self):
        path = os.path.join(os.path.dirname(__file__), "version.txt")
        return open(path).read().strip() if os.path.exists(path) else "0.0.0"

    def get_remote_version(self):
        try:
            if DEV_MODE:
                path = os.path.join(os.path.dirname(__file__), "version_remote.txt")
                return open(path).read().strip() if os.path.exists(path) else None

            import requests
            url = "https://raw.githubusercontent.com/studentmovi/ProjetDevOps/main/app/version.txt"
            r = requests.get(url, timeout=5)
            return r.text.strip() if r.status_code == 200 else None
        except Exception:
            return None

    # ====================================================
    #  UPDATE
    # ====================================================
    def check_update_background(self):
        threading.Thread(target=self.check_update, daemon=True).start()

    def check_update(self):
        local = self.get_local_version()
        remote = self.get_remote_version()
        if not remote or remote == local:
            return

        state = get_update_state()
        force = should_force_update(state)
        self.root.after(0, lambda: self.show_update_popup(local, remote, force))

    def show_update_popup(self, local, remote, force):
        from popups.update_popup import update_popup_custom
        state = get_update_state()
        action = update_popup_custom(self.root, local, remote, force)

        if action == "update":
            self.start_update()
        else:
            if not state["ignored_since"]:
                state["ignored_since"] = datetime.datetime.now().isoformat()
                save_update_state(state)

    def start_update(self):
        launcher = os.path.join(os.path.dirname(__file__), "launcher.py")
        subprocess.Popen([sys.executable, launcher, "--update"])
        self.root.destroy()

    # ====================================================
    #  RUN
    # ====================================================
    def run(self):
        self.root.mainloop()


# ====================================================
#  LANCEMENT
# ====================================================
if __name__ == "__main__":
    MainApplication().run()
