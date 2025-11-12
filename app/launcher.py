import os
import shutil
import sys
import subprocess
import tkinter as tk
from tkinter import ttk
import threading
import time
from utils.logger import log_info, log_warning, log_error

try:
    import requests  # type: ignore
except Exception:
    # Minimal fallback using urllib if 'requests' is not available.
    import urllib.request
    import urllib.error
    import io

    class SimpleResponse:
        def __init__(self, status_code, content, url=None):
            self.status_code = status_code
            self._content = content
            self.url = url
            if isinstance(content, bytes):
                try:
                    self.text = content.decode('utf-8')
                except Exception:
                    self.text = content.decode('latin-1', errors='ignore')
                self.raw = io.BytesIO(content)
            else:
                self.text = str(content)
                self.raw = io.BytesIO(self.text.encode('utf-8'))

    class SimpleRequests:
        @staticmethod
        def get(url, timeout=5, stream=False):
            req = urllib.request.Request(url, headers={"User-Agent": "python"})
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    data = resp.read()
                    status = getattr(resp, "status", getattr(resp, "getcode", 200))
                    return SimpleResponse(status, data, url=url)
            except urllib.error.HTTPError as e:
                try:
                    data = e.read()
                except Exception:
                    data = b""
                return SimpleResponse(getattr(e, "code", 500), data, url=url)
            except Exception as e:
                return SimpleResponse(0, str(e).encode("utf-8"), url=url)

    requests = SimpleRequests()

DEV_MODE = True

# Config GitHub
USER = "studentmovi"
REPO = "ProjetDevOps"
VERSION_FILE = os.path.join("version.txt")
CHANGELOG_FILE = os.path.join("changelog.txt")
LOCAL_EXE_PATH = os.path.join("main.exe")
MAIN_PY_PATH = os.path.join(os.path.dirname(__file__), "main.py")

GITHUB_RAW = f"https://raw.githubusercontent.com/{USER}/{REPO}/main/appdevops"

LOCAL_VERSION_FILE = os.path.join("appdevops", VERSION_FILE)
LOCAL_EXE_PATH = os.path.join("appdevops", LOCAL_EXE_PATH)

class ModernLoader:
    """Loader moderne et stylé pour le lancement de l'application"""
    
    def __init__(self):
        self.root = tk.Tk()
        
        # Variables définies AVANT create_widgets()
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Initialisation...")
        self.app_launched = False
        
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
        
        local_version = get_local_version()
        version_label = tk.Label(version_frame,
                               text=f"Version {local_version}",
                               font=("Segoe UI", 8),
                               bg="#1e1e1e",
                               fg="#666666")
        version_label.pack(side="left")
        
        # Mode affiché
        mode_text = "Mode Développement" if DEV_MODE else "Mode Production"
        mode_label = tk.Label(version_frame,
                            text=mode_text,
                            font=("Segoe UI", 8),
                            bg="#1e1e1e",
                            fg="#FFA726" if DEV_MODE else "#4CAF50")
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
    
    def start_loading_sequence(self):
        """Lance la séquence de chargement complète"""
        def loading_thread():
            try:
                # Étape 1: Initialisation
                self.animate_progress(0, 15, 0.5, "🔧 Initialisation du système...")
                
                # Étape 2: Vérification des mises à jour
                self.animate_progress(15, 35, 0.8, "🔄 Vérification des mises à jour...")
                check_update()
                
                # Étape 3: Chargement des composants
                self.animate_progress(35, 55, 0.6, "📦 Chargement des composants...")
                time.sleep(0.3)  # Simulation du chargement
                
                # Étape 4: Préparation de l'interface
                self.animate_progress(55, 75, 0.5, "🎨 Préparation de l'interface...")
                time.sleep(0.3)  # Simulation de la préparation
                
                # Étape 5: Préparation du lancement
                self.animate_progress(75, 90, 0.4, "🚀 Préparation du lancement...")
                time.sleep(0.2)
                
                # Étape 6: Finalisation
                self.animate_progress(90, 100, 0.3, "✅ Finalisation...")
                time.sleep(0.5)
                
                # 🎯 LANCEMENT DE L'APP MAINTENANT (à 100%)
                self.root.after(0, lambda: self.status_var.set("🚀 Lancement de l'application..."))
                self.launch_app()
                
                # Attendre que l'app se lance vraiment
                time.sleep(1.0)
                
                # Message final
                self.root.after(0, lambda: self.status_var.set("✅ Application lancée avec succès !"))
                time.sleep(0.8)
                
                # Fermer le loader APRÈS le lancement
                self.root.after(0, self.close_loader)
                
            except Exception as e:
                log_error(e, "Erreur pendant le chargement")
                self.root.after(0, lambda: self.show_error(str(e)))
        
        # Lancer le thread de chargement
        thread = threading.Thread(target=loading_thread, daemon=True)
        thread.start()
    
    def launch_app(self):
        """Lance l'application principale"""
        try:
            if DEV_MODE:
                if os.path.exists(MAIN_PY_PATH):
                    log_info("Lancement de main.py en mode dev...")
                    # 🎯 MODIFICATION: Lancer et attendre que le processus démarre
                    process = subprocess.Popen([sys.executable, MAIN_PY_PATH])
                    
                    # Vérifier que le processus a bien démarré
                    time.sleep(0.5)  # Laisser le temps au processus de démarrer
                    if process.poll() is None:  # None = le processus tourne
                        self.app_launched = True
                        log_info("Application lancée avec succès !")
                    else:
                        raise Exception("L'application s'est fermée immédiatement")
                        
                else:
                    raise FileNotFoundError("main.py introuvable !")
            else:
                if os.path.exists(LOCAL_EXE_PATH):
                    log_info("Lancement de main.exe en mode production...")
                    os.startfile(LOCAL_EXE_PATH)
                    time.sleep(1.0)  # Laisser le temps à l'exe de se lancer
                    self.app_launched = True
                else:
                    raise FileNotFoundError("main.exe introuvable ! Compilez d'abord main.py en exe.")
                    
        except Exception as e:
            log_error(e, "Erreur au lancement de l'application")
            raise e
    
    def show_error(self, error_msg):
        """Affiche une erreur dans le loader"""
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
    
    def close_loader(self):
        """Ferme le loader seulement si l'app est lancée"""
        if self.app_launched:
            log_info("Fermeture du loader - Application lancée avec succès")
            self.root.quit()
            self.root.destroy()
        else:
            # Si l'app n'a pas pu se lancer, garder le loader ouvert avec l'erreur
            self.show_error("L'application n'a pas pu se lancer correctement")
    
    def run(self):
        """Lance le loader"""
        # Démarrer la séquence de chargement après un court délai
        self.root.after(500, self.start_loading_sequence)
        self.root.mainloop()

def get_local_version():
    if not os.path.exists(LOCAL_VERSION_FILE):
        return "0.0.0"
    with open(LOCAL_VERSION_FILE, "r") as f:
        return f.read().strip()

def get_remote_version():
    try:
        r = requests.get(f"{GITHUB_RAW}/{VERSION_FILE}", timeout=5)
        if r.status_code == 200:
            return r.text.strip()
    except Exception as e:
        log_error(e, "Erreur en récupérant la version distante")
        print("Erreur en récupérant la version distante:", e)
    return None

def show_changelog():
    try:
        r = requests.get(f"{GITHUB_RAW}/{CHANGELOG_FILE}", timeout=5)
        if r.status_code == 200:
            log_info("Changelog récupéré avec succès.")
            print("\n📝 Nouveautés :\n" + r.text)
    except Exception as e:
        log_error(e, "Impossible de charger le changelog.")
        print("Impossible de charger le changelog.")

def update_main_exe():
    try:
        r = requests.get(f"{GITHUB_RAW}/{LOCAL_EXE_PATH}", timeout=10, stream=True)
        if r.status_code == 200:
            tmp_path = LOCAL_EXE_PATH + ".tmp"
            with open(tmp_path, "wb") as f:
                shutil.copyfileobj(r.raw, f)
            shutil.move(tmp_path, LOCAL_EXE_PATH)
            print("✅ main.exe mis à jour !")
    except Exception as e:
        log_error(e, "Erreur lors de la mise à jour de main.exe")
        print("Erreur lors de la mise à jour de main.exe :", e)

def check_update():
    local = get_local_version()
    remote = get_remote_version()
    if remote and remote != local:
        print(f"⚠️ Nouvelle version disponible : {remote} (vous avez {local})")
        show_changelog()
        update_main_exe()
        # On met à jour la version locale
        with open(LOCAL_VERSION_FILE, "w") as f:
            f.write(remote)
    else:
        print("✅ Application à jour.")

def run_app():
    """Fonction simplifiée, maintenant gérée par le loader"""
    pass

if __name__ == "__main__":
    # Lancer le loader moderne au lieu de l'ancien système
    loader = ModernLoader()
    loader.run()