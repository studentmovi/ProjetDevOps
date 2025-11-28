import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Ajout du chemin pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.appStyles import AppStyles
from views.home_view import HomeView
from views.student_view import StudentView


class MainApplication:
    def __init__(self):
        self.root = tk.Tk()

        # ====================================================
        #  ICON PERSONNALISÉ (fenêtre + barre des tâches)
        # ====================================================
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "logo.ico")
        try:
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"[WARN] Impossible de charger l'icône : {e}")

        # ====================================================
        #  INITIALISATION DES STYLES
        # ====================================================
        self.styles = AppStyles()
        self.ttk_style = self.styles.configure_ttk_style(self.root)
        self.styles.configure_window(self.root, "🎓 CND - Gestion Événements")

        # Configuration de la fenêtre
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        self.root.state('zoomed')  # Maximisé par défaut sur Windows

        # Variables
        self.current_view = None
        self.views = {}

        self.setup_ui()
        self.show_home()

    # ====================================================
    #  UI PRINCIPALE
    # ====================================================
    def setup_ui(self):
        """Configure l'interface utilisateur avec le nouveau design"""

        # ---------- BARRE DE NAVIGATION SUPÉRIEURE ----------
        nav_frame = self.styles.create_header_frame(self.root, padding="10")
        nav_frame.pack(fill="x", side="top")

        # Logo / Titre
        title_label = ttk.Label(
            nav_frame,
            text="🎓 Gestion Scolaire",
            style="Header.TLabel"
        )
        title_label.pack(side="left")

        # Boutons de navigation
        nav_buttons_frame = ttk.Frame(nav_frame, style="Header.TFrame")
        nav_buttons_frame.pack(side="right")

        home_btn = ttk.Button(
            nav_buttons_frame,
            text="🏠 Accueil",
            command=self.show_home,
            style="Secondary.TButton"
        )
        home_btn.pack(side="left", padx=(0, 8))

        students_btn = ttk.Button(
            nav_buttons_frame,
            text="👥 Élèves",
            command=self.show_students,
            style="Secondary.TButton"
        )
        students_btn.pack(side="left", padx=(0, 8))

        events_btn = ttk.Button(
            nav_buttons_frame,
            text="📅 Événements",
            command=self.show_events,
            style="Secondary.TButton"
        )
        events_btn.pack(side="left", padx=(0, 8))

        settings_btn = ttk.Button(
            nav_buttons_frame,
            text="⚙️ Paramètres",
            command=self.show_settings,
            style="Light.TButton"
        )
        settings_btn.pack(side="left")

        # ---------- CONTENU PRINCIPAL ----------
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(fill="both", expand=True, padx=5, pady=(5, 0))

        # ---------- BARRE DE STATUT ----------
        status_frame = self.styles.create_card_frame(self.root, padding="8")
        status_frame.pack(fill="x", side="bottom")

        self.status_label = ttk.Label(
            status_frame,
            text="🚀 Application démarrée - Prêt à utiliser",
            style="Small.TLabel"
        )
        self.status_label.pack(side="left")

        version_label = ttk.Label(
            status_frame,
            text="v0.3.0",
            style="Small.TLabel"
        )
        version_label.pack(side="right")

    # ====================================================
    #  GESTION DES VUES
    # ====================================================
    def switch_view(self, new_view_name):
        """Bascule entre les vues avec animation"""
        try:
            # Masquer la vue actuelle
            if self.current_view:
                self.current_view.hide()

            # Créer la nouvelle vue si nécessaire
            if new_view_name not in self.views:
                if new_view_name == "home":
                    self.views[new_view_name] = HomeView(self.content_frame, self.styles)
                elif new_view_name == "students":
                    self.views[new_view_name] = StudentView(self.content_frame, self.styles)
                # Ajout futur : events, settings, etc.

                # Créer les widgets de la vue
                if hasattr(self.views[new_view_name], "create_widgets"):
                    self.views[new_view_name].create_widgets()

            # Afficher la nouvelle vue
            self.current_view = self.views[new_view_name]
            self.current_view.show()

            # Mettre à jour le statut
            view_names = {
                "home": "🏠 Accueil",
                "students": "👥 Gestion des Élèves",
                "events": "📅 Gestion des Événements"
            }
            self.status_label.config(text=f"📍 Page Active: {view_names.get(new_view_name, new_view_name)}")

        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur lors du changement de vue: {e}")
            print(f"Erreur switch_view: {e}")

    # ====================================================
    #  MÉTHODES POUR CHAQUE PAGE
    # ====================================================
    def show_home(self):
        self.switch_view("home")

    def show_students(self):
        self.switch_view("students")

    def show_events(self):
        messagebox.showinfo("📅 Événements", "Vue des événements\n(À développer)")

    def show_settings(self):
        messagebox.showinfo("⚙️ Paramètres", "Vue des paramètres\n(À développer)")

    # ====================================================
    #  DÉMARRAGE DE L’APPLICATION
    # ====================================================
    def run(self):
        try:
            print("🚀 Démarrage de l'application...")

            # Centrer la fenêtre
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            self.root.geometry(f"{width}x{height}+{x}+{y}")

            self.root.mainloop()

        except Exception as e:
            print(f"❌ Erreur critique: {e}")
            messagebox.showerror("Erreur critique", f"Erreur lors du démarrage:\n{e}")


# ====================================================
#  LANCEMENT
# ====================================================
if __name__ == "__main__":
    app = MainApplication()
    app.run()
