import json
import os
import shutil
import sys
import subprocess
import threading
import time

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


def resource_path(*parts):
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, *parts)


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

        self.VERSION_FILE = resource_path("version.txt")
        self.LOCAL_EXE_PATH = resource_path("main.exe")
        self.MAIN_PY_PATH = resource_path("main.py")

        self.GITHUB_RAW = f"https://raw.githubusercontent.com/{self.USER}/{self.REPO}/main/app"
        self.EXE_URL = f"https://github.com/{self.USER}/{self.REPO}/releases/latest/download/main.exe"

    # --------------------------------------------------
    # VERSION
    # --------------------------------------------------
    def get_local_version(self):
        if not os.path.exists(self.VERSION_FILE):
            return "0.0.0"
        with open(self.VERSION_FILE, "r") as f:
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
            self.safe_update_exe()

            with open(self.VERSION_FILE, "w") as f:
                f.write(remote)

            self.view.animate_progress(80, 100, 0.4, "Finalisation...")

        except Exception as e:
            log_error(e, "Erreur MAJ")
            self.view.show_error("Mise à jour échouée")

        self.start_app_once()

    # --------------------------------------------------
    # 🔐 UPDATE SAFE
    # --------------------------------------------------
    def safe_update_exe(self):
        tmp = self.LOCAL_EXE_PATH + ".tmp"
        bak = self.LOCAL_EXE_PATH + ".bak"

        r = requests.get(self.EXE_URL, stream=True)
        if r.status_code != 200:
            raise Exception("Téléchargement échoué")

        with open(tmp, "wb") as f:
            shutil.copyfileobj(r.raw, f)

        if os.path.exists(self.LOCAL_EXE_PATH):
            shutil.move(self.LOCAL_EXE_PATH, bak)

        shutil.move(tmp, self.LOCAL_EXE_PATH)

        if os.path.exists(bak):
            os.remove(bak)

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
    # 🚀 LANCEMENT UNIQUE (clé du fix)
    # --------------------------------------------------
    def start_app_once(self):
        if self.app_started:
            return  # 🔒 empêche double lancement

        self.app_started = True
        self.view.update_status("🚀 Lancement de l'application...")

        try:
            if self.DEV_MODE:
                subprocess.Popen(
                    [sys.executable, self.MAIN_PY_PATH],
                    close_fds=True
                )
            else:
                subprocess.Popen(
                    [self.LOCAL_EXE_PATH],
                    close_fds=True
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
