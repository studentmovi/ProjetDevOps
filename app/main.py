import tkinter as tk
from tkinter import ttk, filedialog, messagebox
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
        
        # Bouton Accueil
        home_btn = tk.Button(nav_buttons, 
                            text="🏠 Accueil",
                            command=lambda: self.show_view('home'),
                            bg=self.styles.colors['primary'],
                            fg='white',
                            font=("Helvetica", 9, "bold"),
                            relief='flat',
                            padx=12,
                            pady=6,
                            cursor='hand2')
        home_btn.pack(side="left", padx=(0, 5))
        
        # Bouton Élèves
        students_btn = tk.Button(nav_buttons, 
                                text="👥 Élèves",
                                command=lambda: self.show_view('students'),
                                bg=self.styles.colors['primary'],
                                fg='white',
                                font=("Helvetica", 9, "bold"),
                                relief='flat',
                                padx=12,
                                pady=6,
                                cursor='hand2')
        students_btn.pack(side="left", padx=(0, 5))
        
        # Bouton Événements
        events_btn = tk.Button(nav_buttons, 
                              text="📅 Événements",
                              command=self.show_events_view,
                              bg=self.styles.colors['primary'],
                              fg='white',
                              font=("Helvetica", 9, "bold"),
                              relief='flat',
                              padx=12,
                              pady=6,
                              cursor='hand2')
        events_btn.pack(side="left", padx=(0, 5))
        
        # Bouton Excel
        excel_btn = tk.Button(nav_buttons, 
                             text="📊 Excel",
                             command=self.load_excel,
                             bg=self.styles.colors['success'],
                             fg='white',
                             font=("Helvetica", 9, "bold"),
                             relief='flat',
                             padx=12,
                             pady=6,
                             cursor='hand2')
        excel_btn.pack(side="left")

    def show_view(self, view_name):
        """Affiche une vue spécifique et cache les autres"""
        # Cacher la vue actuelle
        if self.current_view and self.current_view in self.views:
            self.views[self.current_view].hide()
        
        # Afficher la nouvelle vue
        if view_name in self.views:
            self.views[view_name].show()
            self.current_view = view_name
            log_info(f"Vue '{view_name}' affichée")
        else:
            log_warning(f"Vue '{view_name}' non trouvée")

    def show_events_view(self):
        """Affiche la vue des événements (à développer)"""
        messagebox.showinfo("Info", "Vue des événements à développer")

    def load_excel(self):
        """Lance l'import Excel depuis la navigation"""
        if 'students' in self.views:
            # Basculer vers la vue élèves et lancer l'import
            self.show_view('students')
            # Délai pour s'assurer que la vue est affichée
            self.root.after(100, lambda: self.views['students']._on_import_excel())
        else:
            messagebox.showwarning("Attention", "Vue des élèves non disponible")


if __name__ == "__main__":
    root = tk.Tk()
    app = CulturalEventManager(root)
    root.mainloop()