import os
import shutil
import sys
import subprocess
import threading
import time
from utils.logger import log_info, log_warning, log_error
from views.launcher_view import LauncherView

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

class LauncherController:
    """Contrôleur pour la gestion du launcher de l'application"""
    
    def __init__(self):
        # Configuration
        self.DEV_MODE = True
        self.setup_config()
        
        # État du launcher
        self.app_launched = False
        self.app_process = None  # ✅ NOUVEAU: Garder référence du processus
        
        # Créer la vue
        self.view = LauncherView(self)
        
    def setup_config(self):
        """Configure les chemins et URLs"""
        # Config GitHub
        self.USER = "studentmovi"
        self.REPO = "ProjetDevOps"
        self.VERSION_FILE = os.path.join("version.txt")
        self.CHANGELOG_FILE = os.path.join("changelog.txt")
        self.LOCAL_EXE_PATH = os.path.join("main.exe")
        self.MAIN_PY_PATH = os.path.join(os.path.dirname(__file__), "main.py")
        
        self.GITHUB_RAW = f"https://raw.githubusercontent.com/{self.USER}/{self.REPO}/main/appdevops"
        
        self.LOCAL_VERSION_FILE = os.path.join("appdevops", self.VERSION_FILE)
        self.LOCAL_EXE_PATH_FULL = os.path.join("appdevops", self.LOCAL_EXE_PATH)
    
    # ...existing code... (get_local_version, get_remote_version, show_changelog, update_main_exe, check_update restent identiques)
    
    def get_local_version(self):
        """Récupère la version locale"""
        if not os.path.exists(self.LOCAL_VERSION_FILE):
            return "0.0.0"
        with open(self.LOCAL_VERSION_FILE, "r") as f:
            return f.read().strip()
    
    def get_remote_version(self):
        """Récupère la version distante"""
        try:
            r = requests.get(f"{self.GITHUB_RAW}/{self.VERSION_FILE}", timeout=5)
            if r.status_code == 200:
                return r.text.strip()
        except Exception as e:
            log_error(e, "Erreur en récupérant la version distante")
            print("Erreur en récupérant la version distante:", e)
        return None
    
    def show_changelog(self):
        """Affiche le changelog"""
        try:
            r = requests.get(f"{self.GITHUB_RAW}/{self.CHANGELOG_FILE}", timeout=5)
            if r.status_code == 200:
                log_info("Changelog récupéré avec succès.")
                print("\n📝 Nouveautés :\n" + r.text)
        except Exception as e:
            log_error(e, "Impossible de charger le changelog.")
            print("Impossible de charger le changelog.")
    
    def update_main_exe(self):
        """Met à jour le fichier exe"""
        try:
            r = requests.get(f"{self.GITHUB_RAW}/{self.LOCAL_EXE_PATH_FULL}", timeout=10, stream=True)
            if r.status_code == 200:
                tmp_path = self.LOCAL_EXE_PATH_FULL + ".tmp"
                with open(tmp_path, "wb") as f:
                    shutil.copyfileobj(r.raw, f)
                shutil.move(tmp_path, self.LOCAL_EXE_PATH_FULL)
                print("✅ main.exe mis à jour !")
        except Exception as e:
            log_error(e, "Erreur lors de la mise à jour de main.exe")
            print("Erreur lors de la mise à jour de main.exe :", e)
    
    def check_update(self):
        """Vérifie et applique les mises à jour"""
        local = self.get_local_version()
        remote = self.get_remote_version()
        if remote and remote != local:
            print(f"⚠️ Nouvelle version disponible : {remote} (vous avez {local})")
            self.show_changelog()
            self.update_main_exe()
            # On met à jour la version locale
            with open(self.LOCAL_VERSION_FILE, "w") as f:
                f.write(remote)
        else:
            print("✅ Application à jour.")
    
    def start_loading_sequence(self):
        """Lance la séquence de chargement complète"""
        def loading_thread():
            try:
                # Étape 1: Initialisation
                self.view.animate_progress(0, 15, 0.5, "🔧 Initialisation du système...")
                
                # Étape 2: Vérification des mises à jour
                self.view.animate_progress(15, 35, 0.8, "🔄 Vérification des mises à jour...")
                self.check_update()
                
                # Étape 3: Chargement des composants
                self.view.animate_progress(35, 55, 0.6, "📦 Chargement des composants...")
                time.sleep(0.3)  # Simulation du chargement
                
                # Étape 4: Préparation de l'interface
                self.view.animate_progress(55, 75, 0.5, "🎨 Préparation de l'interface...")
                time.sleep(0.3)  # Simulation de la préparation
                
                # Étape 5: Préparation du lancement
                self.view.animate_progress(75, 90, 0.4, "🚀 Préparation du lancement...")
                time.sleep(0.2)
                
                # Étape 6: Finalisation
                self.view.animate_progress(90, 100, 0.3, "✅ Finalisation...")
                time.sleep(0.3)
                
                # 🎯 LANCEMENT DE L'APP MAINTENANT (à 100%)
                self.view.update_status("🚀 Lancement de l'application...")
                
                # ✅ MODIFICATION CLÉE: Lancer l'app ET attendre confirmation
                success = self.launch_app_and_wait()
                
                if success:
                    # Message final
                    self.view.update_status("✅ Application lancée avec succès !")
                    time.sleep(0.5)  # Court délai pour voir le message
                    
                    # Fermer le loader immédiatement après le lancement réussi
                    self.view.close_loader()
                else:
                    raise Exception("Échec du lancement de l'application")
                
            except Exception as e:
                log_error(e, "Erreur pendant le chargement")
                self.view.show_error(str(e))
        
        # Lancer le thread de chargement
        thread = threading.Thread(target=loading_thread, daemon=True)
        thread.start()
    
    def launch_app_and_wait(self):
        """Lance l'application et attend la confirmation qu'elle démarre"""
        try:
            if self.DEV_MODE:
                return self.launch_dev_mode()
            else:
                return self.launch_prod_mode()
        except Exception as e:
            log_error(e, "Erreur au lancement de l'application")
            return False
    
    def launch_dev_mode(self):
        """Lance l'application en mode développement"""
        if not os.path.exists(self.MAIN_PY_PATH):
            raise FileNotFoundError("main.py introuvable !")
        
        log_info("Lancement de main.py en mode dev...")
        
        # ✅ Lancer le processus
        self.app_process = subprocess.Popen([sys.executable, self.MAIN_PY_PATH])
        
        # ✅ Attendre un peu et vérifier que le processus tourne
        max_attempts = 10
        for attempt in range(max_attempts):
            time.sleep(0.2)  # Attendre 200ms
            
            if self.app_process.poll() is None:  # None = le processus tourne toujours
                self.app_launched = True
                log_info(f"Application lancée avec succès ! (tentative {attempt + 1})")
                return True
            
            if attempt < max_attempts - 1:  # Pas la dernière tentative
                log_info(f"Vérification du processus... (tentative {attempt + 1})")
        
        # Si on arrive ici, le processus s'est fermé
        raise Exception("L'application s'est fermée immédiatement")
    
    def launch_prod_mode(self):
        """Lance l'application en mode production"""
        if not os.path.exists(self.LOCAL_EXE_PATH_FULL):
            raise FileNotFoundError("main.exe introuvable ! Compilez d'abord main.py en exe.")
        
        log_info("Lancement de main.exe en mode production...")
        
        # ✅ Lancer l'exe
        os.startfile(self.LOCAL_EXE_PATH_FULL)
        
        # ✅ En mode production, on assume que ça marche après un délai
        time.sleep(1.5)  # Laisser le temps à l'exe de se lancer
        self.app_launched = True
        log_info("Application lancée en mode production !")
        return True
    
    def is_app_launched(self):
        """Retourne si l'application a été lancée avec succès"""
        return self.app_launched
    
    def run(self):
        """Lance le launcher"""
        self.view.run()

if __name__ == "__main__":
    # Lancer le contrôleur du launcher
    launcher = LauncherController()
    launcher.run()