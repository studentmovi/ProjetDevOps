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
        
        # ========== INITIALISATION DES STYLES ==========
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
    
    def setup_ui(self):
        """Configure l'interface utilisateur avec le nouveau design"""
        # ========== BARRE DE NAVIGATION SUPÉRIEURE ==========
        nav_frame = self.styles.create_header_frame(self.root, padding="10")
        nav_frame.pack(fill="x", side="top")
        
        # Logo/Titre
        title_label = ttk.Label(
            nav_frame,
            text="🎓 Gestion Scolaire",
            style="Header.TLabel"
        )
        title_label.pack(side="left")
        
        # Menu de navigation
        nav_buttons_frame = ttk.Frame(nav_frame, style="Header.TFrame")
        nav_buttons_frame.pack(side="right")
        
        # Boutons de navigation avec nouveau style
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
        
        # ========== ZONE DE CONTENU PRINCIPAL ==========
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(fill="both", expand=True, padx=5, pady=(5, 0))
        
        # ========== BARRE DE STATUT INFÉRIEURE ==========
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
                # Ajouter d'autres vues ici
                
                # Créer les widgets de la vue
                if hasattr(self.views[new_view_name], 'create_widgets'):
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
    
    def show_home(self):
        """Affiche la vue d'accueil"""
        self.switch_view("home")
    
    def show_students(self):
        """Affiche la vue des élèves"""
        self.switch_view("students")
    
    def show_events(self):
        """Affiche la vue des événements"""
        messagebox.showinfo("📅 Événements", "Vue des événements\n(À développer)")
    
    def show_settings(self):
        """Affiche la vue des paramètres"""
        messagebox.showinfo("⚙️ Paramètres", "Vue des paramètres\n(À développer)")
    
    def run(self):
        """Lance l'application"""
        try:
            # Message de démarrage stylé
            print("🚀 Démarrage de l'application avec le nouveau design bleu...")
            
            # Centrer la fenêtre
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            self.root.geometry(f'{width}x{height}+{x}+{y}')
            
            # Démarrer la boucle principale
            self.root.mainloop()
            
        except Exception as e:
            print(f"❌ Erreur critique: {e}")
            messagebox.showerror("Erreur critique", f"Erreur lors du démarrage:\n{e}")

if __name__ == "__main__":
    app = MainApplication()
    app.run()