import tkinter as tk
from tkinter import ttk
import time

class LauncherView:
    """Vue moderne et stylée pour le launcher de l'application"""
    
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        
        # Variables d'interface
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Initialisation...")
        
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        
    def setup_window(self):
        """Configure la fenêtre du loader"""
        self.root.title("ProjetDevOps - Launcher")
        
        # Dimensions et centrage
        width, height = 450, 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(False, False)
        
        # Style moderne
        self.root.configure(bg="#1e1e1e")
        self.root.overrideredirect(True)  # Enlève la barre de titre
        
        # Rendre la fenêtre toujours au premier plan
        self.root.attributes("-topmost", True)
        
    def setup_styles(self):
        """Configure les styles modernes"""
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Style pour la barre de progression moderne
        self.style.configure("Modern.Horizontal.TProgressbar",
                           background="#4CAF50",
                           troughcolor="#333333",
                           borderwidth=0,
                           lightcolor="#4CAF50",
                           darkcolor="#4CAF50")
    
    def create_widgets(self):
        """Crée l'interface du loader"""
        # Container principal avec coins arrondis simulés
        main_frame = tk.Frame(self.root, bg="#1e1e1e", padx=40, pady=30)
        main_frame.pack(fill="both", expand=True)
        
        # Logo/Titre de l'application
        title_frame = tk.Frame(main_frame, bg="#1e1e1e")
        title_frame.pack(pady=(0, 30))
        
        # Icône principale (emoji ou caractère stylé)
        icon_label = tk.Label(title_frame, 
                            text="🎓",  # Icône éducation
                            font=("Segoe UI", 32),
                            bg="#1e1e1e",
                            fg="#4CAF50")
        icon_label.pack()
        
        # Nom de l'application
        app_name = tk.Label(title_frame,
                          text="ProjetDevOps",
                          font=("Segoe UI", 18, "bold"),
                          bg="#1e1e1e",
                          fg="#ffffff")
        app_name.pack()
        
        # Sous-titre
        subtitle = tk.Label(title_frame,
                          text="Gestion Élèves & Événements",
                          font=("Segoe UI", 10),
                          bg="#1e1e1e",
                          fg="#cccccc")
        subtitle.pack()
        
        # Container pour la progression
        progress_frame = tk.Frame(main_frame, bg="#1e1e1e")
        progress_frame.pack(fill="x", pady=20)
        
        # Barre de progression moderne
        self.progress_bar = ttk.Progressbar(progress_frame,
                                          style="Modern.Horizontal.TProgressbar",
                                          mode="determinate",
                                          variable=self.progress_var)
        self.progress_bar.pack(fill="x", pady=(0, 10))
        
        # Texte de statut
        self.status_label = tk.Label(progress_frame,
                                   textvariable=self.status_var,
                                   font=("Segoe UI", 9),
                                   bg="#1e1e1e",
                                   fg="#cccccc")
        self.status_label.pack()
        
        # Pourcentage
        self.percent_label = tk.Label(progress_frame,
                                    text="0%",
                                    font=("Segoe UI", 9, "bold"),
                                    bg="#1e1e1e",
                                    fg="#4CAF50")
        self.percent_label.pack()
        
        # Version info en bas
        version_frame = tk.Frame(main_frame, bg="#1e1e1e")
        version_frame.pack(side="bottom", fill="x")
        
        local_version = self.controller.get_local_version()
        version_label = tk.Label(version_frame,
                               text=f"Version {local_version}",
                               font=("Segoe UI", 8),
                               bg="#1e1e1e",
                               fg="#666666")
        version_label.pack(side="left")
        
        # Mode affiché
        mode_text = "Mode Développement" if self.controller.DEV_MODE else "Mode Production"
        mode_label = tk.Label(version_frame,
                            text=mode_text,
                            font=("Segoe UI", 8),
                            bg="#1e1e1e",
                            fg="#FFA726" if self.controller.DEV_MODE else "#4CAF50")
        mode_label.pack(side="right")
        
    def update_progress(self, value, status):
        """Met à jour la progression et le statut"""
        self.progress_var.set(value)
        self.status_var.set(status)
        self.percent_label.config(text=f"{int(value)}%")
        self.root.update()
        
    def animate_progress(self, start, end, duration, status):
        """Animation fluide de la barre de progression"""
        steps = 50
        step_value = (end - start) / steps
        step_duration = duration / steps
        
        for i in range(steps + 1):
            current_value = start + (step_value * i)
            self.update_progress(current_value, status)
            time.sleep(step_duration)
    
    def update_status(self, status):
        """Met à jour seulement le statut"""
        self.root.after(0, lambda: self.status_var.set(status))
    
    def show_error(self, error_msg):
        """Affiche une erreur dans le loader"""
        def show_error_ui():
            self.status_var.set(f"❌ Erreur: {error_msg}")
            self.progress_var.set(0)
            self.percent_label.config(text="Erreur", fg="#F44336")
            
            # Bouton pour fermer en cas d'erreur
            error_button = tk.Button(self.root,
                                   text="Fermer",
                                   command=self.root.quit,
                                   bg="#F44336",
                                   fg="white",
                                   font=("Segoe UI", 9),
                                   relief="flat",
                                   padx=20)
            error_button.pack(pady=10)
        
        self.root.after(0, show_error_ui)
    
    def close_loader(self):
        """Ferme le loader seulement si l'app est lancée"""
        def close_ui():
            if self.controller.is_app_launched():
                self.root.quit()
                self.root.destroy()
            else:
                # Si l'app n'a pas pu se lancer, garder le loader ouvert avec l'erreur
                self.show_error("L'application n'a pas pu se lancer correctement")
        
        self.root.after(0, close_ui)
    
    def run(self):
        """Lance le loader"""
        # Démarrer la séquence de chargement après un court délai
        self.root.after(500, self.controller.start_loading_sequence)
        self.root.mainloop()