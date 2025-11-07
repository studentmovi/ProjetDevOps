import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from utils.logger import log_info, log_warning, log_error
from utils.appStyles import AppStyles
from views.home_view import HomeView
from views.student_view import StudentsView

class CulturalEventManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion Sorties Culturelles - Collège Notre-Dame")
        self.root.geometry("900x700")
        
        # Initialiser les styles
        self.styles = AppStyles()
        self.root.configure(bg=self.styles.colors['background'])
        
        # Configurer les styles TTK
        self.styles.setup_ttk_styles()
        
        # Navigation
        self.create_navigation()
        
        # Container principal pour les vues
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill="both", expand=True)
        
        # Initialisation des vues
        self.views = {}
        self.current_view = None
        
        # Créer les vues en passant les styles
        self.views['home'] = HomeView(self.main_container, self.styles)
        self.views['home'].create_widgets()
        
        self.views['students'] = StudentsView(self.main_container, self.styles)
        self.views['students'].create_widgets()
        
        # Afficher la page d'accueil par défaut
        self.show_view('home')
        
        log_info("Application Cultural Event Manager initialisée")

    def create_navigation(self):
        """Crée la barre de navigation avec styles"""
        # Configuration de la navbar
        navbar_config = self.styles.get_navbar_config()
        
        nav_frame = tk.Frame(self.root, **navbar_config)
        nav_frame.pack(fill="x", padx=0, pady=0)
        nav_frame.pack_propagate(False)
        
        # Container interne avec padding
        nav_container = tk.Frame(nav_frame, bg=navbar_config['bg'])
        nav_container.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Logo/Titre à gauche
        title_label = tk.Label(nav_container, 
                              text="🎭 Cultural Manager", 
                              font=("Helvetica", 14, "bold"),
                              fg=self.styles.colors['white'],
                              bg=navbar_config['bg'])
        title_label.pack(side="left")
        
        # Sous-titre
        subtitle_label = tk.Label(nav_container, 
                                 text="Collège Notre-Dame", 
                                 font=("Helvetica", 8),
                                 fg=self.styles.colors['text_light'],
                                 bg=navbar_config['bg'])
        subtitle_label.pack(side="left", padx=(10, 0))
        
        # Boutons de navigation à droite
        nav_buttons = ttk.Frame(nav_container)
        nav_buttons.pack(side="right")
        
        ttk.Button(nav_buttons, 
                  text="🏠 Accueil", 
                  style="Nav.Home.TButton",
                  command=lambda: self.show_view('home')).pack(side="left", padx=3)
        
        ttk.Button(nav_buttons, 
                  text="👥 Élèves", 
                  style="Nav.Students.TButton",
                  command=lambda: self.show_view('students')).pack(side="left", padx=3)
        
        ttk.Button(nav_buttons, 
                  text="📊 Événements", 
                  style="Nav.Events.TButton",
                  command=self.show_events_view).pack(side="left", padx=3)
        
        ttk.Button(nav_buttons, 
                  text="📁 Import Excel", 
                  style="Nav.Import.TButton",
                  command=self.load_excel).pack(side="left", padx=3)

    def show_view(self, view_name):
        """Affiche une vue et cache les autres"""
        if self.current_view and self.current_view in self.views:
            self.views[self.current_view].hide()
        
        if view_name in self.views:
            self.views[view_name].show()
            self.current_view = view_name
            log_info(f"Vue '{view_name}' affichée")

    def show_events_view(self):
        """Affiche la vue des événements (placeholder)"""
        messagebox.showinfo("Info", "Vue des événements en cours de développement")
        log_info("Tentative d'accès à la vue événements")

    def load_excel(self):
        """Charge un fichier Excel"""
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if not file_path:
            return

        try:
            df = pd.read_excel(file_path)
            messagebox.showinfo("Succès", f"Fichier Excel chargé: {len(df)} lignes")
            log_info(f"Fichier Excel chargé avec succès: {len(df)} lignes")
        except Exception as e:
            log_error(e, "Erreur lors du chargement du fichier Excel")
            messagebox.showerror("Erreur", f"Impossible de charger le fichier:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CulturalEventManager(root)
    root.mainloop()