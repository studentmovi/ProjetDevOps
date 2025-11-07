import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from utils.logger import log_info, log_warning, log_error
from views.home_view import HomeView
from views.student_view import StudentsView

class CulturalEventManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion Sorties Culturelles - Collège Notre-Dame")
        self.root.geometry("900x700")
        self.root.configure(bg="#f5f6fa")

        # Style général pour un look moderne et épuré
        self.setup_styles()
        
        # Navigation
        self.create_navigation()
        
        # Container principal pour les vues
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill="both", expand=True)
        
        # Initialisation des vues
        self.views = {}
        self.current_view = None
        
        # Créer les vues
        self.views['home'] = HomeView(self.main_container)
        self.views['home'].create_widgets()
        
        self.views['students'] = StudentsView(self.main_container)
        self.views['students'].create_widgets()
        
        # Afficher la page d'accueil par défaut
        self.show_view('home')
        
        log_info("Application Cultural Event Manager initialisée")

    def setup_styles(self):
        """Configure les styles pour une interface épurée avec couleurs"""
        style = ttk.Style()
        
        # Thème de base
        style.theme_use('clam')
        
        # Couleurs principales
        colors = {
            'primary': '#3742fa',      # Bleu vif
            'success': '#2ed573',      # Vert
            'info': '#1e90ff',         # Bleu clair
            'warning': '#ffa502',      # Orange
            'danger': '#ff4757',       # Rouge
            'light': '#f1f2f6',        # Gris clair
            'dark': '#2f3542'          # Gris foncé
        }
        
        # Style pour les boutons de navigation avec couleurs
        style.configure("Nav.Home.TButton", 
                       padding=(12, 8), 
                       font=("Helvetica", 9, "bold"),
                       foreground='white',
                       background=colors['success'])
        
        style.configure("Nav.Students.TButton", 
                       padding=(12, 8), 
                       font=("Helvetica", 9, "bold"),
                       foreground='white',
                       background=colors['primary'])
        
        style.configure("Nav.Events.TButton", 
                       padding=(12, 8), 
                       font=("Helvetica", 9, "bold"),
                       foreground='white',
                       background=colors['info'])
        
        style.configure("Nav.Import.TButton", 
                       padding=(12, 8), 
                       font=("Helvetica", 9, "bold"),
                       foreground='white',
                       background=colors['warning'])
        
        # Effets hover (survolé)
        style.map("Nav.Home.TButton",
                 background=[('active', '#27ae60')])
        
        style.map("Nav.Students.TButton",
                 background=[('active', '#2c3e50')])
        
        style.map("Nav.Events.TButton",
                 background=[('active', '#3498db')])
        
        style.map("Nav.Import.TButton",
                 background=[('active', '#e67e22')])
        
        # Style pour les LabelFrame avec couleurs
        style.configure("Success.TLabelframe", 
                       background="#d5f4e6", 
                       borderwidth=2, 
                       relief="solid",
                       bordercolor=colors['success'])
        
        style.configure("Success.TLabelframe.Label", 
                       font=("Helvetica", 10, "bold"), 
                       background="#d5f4e6",
                       foreground=colors['success'])
        
        style.configure("Info.TLabelframe", 
                       background="#e3f2fd", 
                       borderwidth=2, 
                       relief="solid",
                       bordercolor=colors['info'])
        
        style.configure("Info.TLabelframe.Label", 
                       font=("Helvetica", 10, "bold"), 
                       background="#e3f2fd",
                       foreground=colors['info'])
        
        style.configure("Warning.TLabelframe", 
                       background="#fff3cd", 
                       borderwidth=2, 
                       relief="solid",
                       bordercolor=colors['warning'])
        
        style.configure("Warning.TLabelframe.Label", 
                       font=("Helvetica", 10, "bold"), 
                       background="#fff3cd",
                       foreground=colors['warning'])

    def create_navigation(self):
        """Crée la barre de navigation avec couleurs"""
        # Barre de navigation avec fond coloré
        nav_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        nav_frame.pack(fill="x", padx=0, pady=0)
        nav_frame.pack_propagate(False)
        
        # Container interne avec padding
        nav_container = tk.Frame(nav_frame, bg="#2c3e50")
        nav_container.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Logo/Titre à gauche avec couleur
        title_label = tk.Label(nav_container, 
                              text="🎭 Cultural Manager", 
                              font=("Helvetica", 14, "bold"),
                              fg="#ecf0f1",
                              bg="#2c3e50")
        title_label.pack(side="left")
        
        # Sous-titre
        subtitle_label = tk.Label(nav_container, 
                                 text="Collège Notre-Dame", 
                                 font=("Helvetica", 8),
                                 fg="#bdc3c7",
                                 bg="#2c3e50")
        subtitle_label.pack(side="left", padx=(10, 0))
        
        # Boutons de navigation à droite avec styles colorés
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
        # Cacher la vue actuelle
        if self.current_view and self.current_view in self.views:
            self.views[self.current_view].hide()
        
        # Afficher la nouvelle vue
        if view_name in self.views:
            self.views[view_name].show()
            self.current_view = view_name
            log_info(f"Vue '{view_name}' affichée")

    def show_events_view(self):
        """Affiche la vue des événements (placeholder)"""
        messagebox.showinfo("Info", "Vue des événements en cours de développement")
        log_info("Tentative d'accès à la vue événements")

    def load_excel(self):
        """Charge un fichier Excel (conservé de votre version originale)"""
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