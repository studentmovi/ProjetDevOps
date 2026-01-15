import json
import os
import shutil
import sys
import subprocess
import threading
import time
import zipfile

try:
    import requests
except Exception:
    import urllib.request
    import io

    class SimpleResponse:
        def __init__(self, status_code, content):
            self.status_code = status_code
            self.raw = io.BytesIO(content)
            self.text = content.decode("utf-8", errors="ignore")

    class SimpleRequests:
        @staticmethod
        def get(url, timeout=10, stream=False):
            req = urllib.request.Request(url, headers={"User-Agent": "python"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return SimpleResponse(resp.status, resp.read())

    requests = SimpleRequests()

from utils.logger import log_error
from views.launcher_view import LauncherView


def app_dir() -> str:
    """
    Dossier réel d'exécution.
    - En prod (exe PyInstaller): dossier contenant launcher.exe (ex: .../launcher/)
    - En dev (python launcher.py): dossier contenant launcher.py (ex: .../app/)
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def root_dir() -> str:
    """
    Racine du "pack" distribué.
    Structure attendue en prod (zip onedir):
      PyTrip/
        version.txt
        changelog.json
        launcher/launcher.exe
        main/main.exe
    Donc root = parent de .../launcher/
    """
    base = app_dir()
    # Si on est dans un dossier "launcher" en prod, le root est le parent
    parent = os.path.abspath(os.path.join(base, ".."))
    # Heuristique: si parent contient "main" ou "version.txt", c'est bien le root
    if os.path.exists(os.path.join(parent, "main")) or os.path.exists(os.path.join(parent, "version.txt")):
        return parent
    # En dev, app_dir() est déjà app/ donc root == app/
    return base


class LauncherController:

    def __init__(self):
        self.DEV_MODE = not getattr(sys, "frozen", False)
        self.setup_config()

        self.app_started = False  # 🔒 anti double lancement
        self.view = LauncherView(self)

    # --------------------------------------------------
    # CONFIG
    # --------------------------------------------------
    def setup_config(self):
        self.USER = "studentmovi"
        self.REPO = "ProjetDevOps"

        # Root local (prod: dossier du zip, dev: app/)
        self.ROOT = root_dir()

        # Fichiers communs à la racine du package (prod)
        # En dev, tu peux laisser version.txt dans app/ (comme maintenant)
        self.VERSION_FILE = os.path.join(self.ROOT, "version.txt")

        # ✅ ONEDIR : main.exe est dans /main/main.exe
        self.LOCAL_EXE_PATH = os.path.join(self.ROOT, "main", "main.exe")

        # Dev only : main.py est dans le même dossier que launcher.py (app/)
        self.MAIN_PY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")

        # Remote
        self.GITHUB_RAW = f"https://raw.githubusercontent.com/{self.USER}/{self.REPO}/main/app"

        # ⚠️ En onedir, on ne met plus à jour via main.exe seul.
        # On télécharge un ZIP (le zip release complet ou un zip "main-only").
        # Ici on suppose que tu publies un zip "main-windows.zip" (recommandé).
        # Si tu n'as que le zip global, mets plutôt l'URL du zip global.
        self.MAIN_ZIP_URL = f"https://github.com/{self.USER}/{self.REPO}/releases/latest/download/main-windows.zip"

    # --------------------------------------------------
    # VERSION
    # --------------------------------------------------
    def get_local_version(self):
        if not os.path.exists(self.VERSION_FILE):
            return "0.0.0"
        with open(self.VERSION_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()

    def get_remote_version(self):
        r = requests.get(f"{self.GITHUB_RAW}/version.txt")
        return r.text.strip() if r.status_code == 200 else None

    # --------------------------------------------------
    # 🔁 UPDATE FLOW (UNIQUEMENT avec --update)
    # --------------------------------------------------
    def perform_update_flow(self):
        local = self.get_local_version()
        remote = self.get_remote_version()

        if not remote or remote == local:
            self.start_app_once()
            return

        accepted = self.view.show_update_popup(local, remote)
        if not accepted:
            self.start_app_once()
            return

        try:
            self.view.animate_progress(20, 80, 1.2, "Téléchargement de la mise à jour...")
            self.safe_update_main_dir()

            with open(self.VERSION_FILE, "w", encoding="utf-8") as f:
                f.write(remote)

            self.view.animate_progress(80, 100, 0.4, "Finalisation...")

        except Exception as e:
            log_error(e, "Erreur MAJ")
            self.view.show_error("Mise à jour échouée")

        self.start_app_once()

    # --------------------------------------------------
    # 🔐 UPDATE SAFE (ONEDIR)
    # --------------------------------------------------
    def safe_update_main_dir(self):
        """
        En mode --onedir, on met à jour le dossier /main (pas seulement main.exe).
        On télécharge un zip qui contient un dossier "main/" (ou directement le contenu du dossier main).
        """
        # Dossiers
        main_dir = os.path.join(self.ROOT, "main")
        tmp_dir = os.path.join(self.ROOT, "_update_tmp_main")
        tmp_zip = os.path.join(self.ROOT, "main_update.tmp.zip")

        # Téléchargement ZIP
        r = requests.get(self.MAIN_ZIP_URL, stream=True)
        if r.status_code != 200:
            raise Exception("Téléchargement échoué (zip)")

        with open(tmp_zip, "wb") as f:
            shutil.copyfileobj(r.raw, f)

        # Nettoyer temp
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)
        os.makedirs(tmp_dir, exist_ok=True)

        # Extraire
        with zipfile.ZipFile(tmp_zip, "r") as z:
            z.extractall(tmp_dir)

        # Trouver le contenu "main"
        # Cas 1: zip contient "main/..."
        extracted_main = os.path.join(tmp_dir, "main")
        # Cas 2: zip contient directement les fichiers du main (main.exe, *.dll, ...)
        if not os.path.isdir(extracted_main):
            extracted_main = tmp_dir

        # Vérifs minimales
        candidate_exe = os.path.join(extracted_main, "main.exe")
        if not os.path.exists(candidate_exe):
            raise Exception("Zip invalide: main.exe introuvable dans la mise à jour")

        # Remplacement atomique (best effort sous Windows)
        bak_dir = main_dir + ".bak"

        # Supprimer ancien backup
        if os.path.exists(bak_dir):
            shutil.rmtree(bak_dir, ignore_errors=True)

        # Renommer main -> main.bak (si existe)
        if os.path.exists(main_dir):
            shutil.move(main_dir, bak_dir)

        # Déployer nouveau main
        os.makedirs(main_dir, exist_ok=True)
        for item in os.listdir(extracted_main):
            src = os.path.join(extracted_main, item)
            dst = os.path.join(main_dir, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)

        # Cleanup
        try:
            os.remove(tmp_zip)
        except Exception:
            pass
        shutil.rmtree(tmp_dir, ignore_errors=True)

        # Supprimer backup si tout est ok
        shutil.rmtree(bak_dir, ignore_errors=True)

    # --------------------------------------------------
    # 🚌 SÉQUENCE DE CHARGEMENT (UI SEULEMENT)
    # --------------------------------------------------
    def start_loading_sequence(self):
        def run_loading():
            try:
                self.view.animate_progress(0, 20, 0.4, "Initialisation...")
                self.view.animate_progress(20, 45, 0.6, "Chargement des ressources...")
                self.view.animate_progress(45, 70, 0.6, "Préparation de l'application...")
                self.view.animate_progress(70, 90, 0.4, "Finalisation...")
                self.view.animate_progress(90, 100, 0.3, "Lancement...")

                self.start_app_once()

            except Exception as e:
                self.view.show_error(str(e))

        threading.Thread(target=run_loading, daemon=True).start()

    # --------------------------------------------------
    # 🚀 LANCEMENT UNIQUE
    # --------------------------------------------------
    def start_app_once(self):
        if self.app_started:
            return  # 🔒 empêche double lancement

        self.app_started = True
        self.view.update_status("🚀 Lancement de l'application...")

        try:
            if self.DEV_MODE:
                # Dev : lancer main.py
                subprocess.Popen(
                    [sys.executable, self.MAIN_PY_PATH],
                    close_fds=True
                )
            else:
                # Prod : lancer main/main.exe
                if not os.path.exists(self.LOCAL_EXE_PATH):
                    raise FileNotFoundError(f"main.exe introuvable: {self.LOCAL_EXE_PATH}")
                subprocess.Popen(
                    [self.LOCAL_EXE_PATH],
                    close_fds=True,
                    cwd=os.path.dirname(self.LOCAL_EXE_PATH)  # important pour onedir (DLL à côté)
                )
        except Exception as e:
            self.view.show_error(str(e))
            return

        # fermer le launcher APRÈS avoir lancé le main
        self.view.root.after(120, self.view.close_loader)

    # --------------------------------------------------
    # RUN
    # --------------------------------------------------
    def run(self):
        if "--update" in sys.argv:
            self.view.root.after(300, self.perform_update_flow)
        else:
            self.view.root.after(300, self.start_loading_sequence)

        self.view.run()


if __name__ == "__main__":
    LauncherController().run()
