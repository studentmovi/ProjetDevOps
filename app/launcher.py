import os
import shutil
import sys
import subprocess
import threading
import time
from utils.logger import log_info, log_warning, log_error
from views.launcher_view import LauncherView

try:
    import requests
except Exception:
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
                    self.text = content.decode("utf-8")
                except Exception:
                    self.text = content.decode("latin-1", errors="ignore")
                self.raw = io.BytesIO(content)
            else:
                self.text = str(content)
                self.raw = io.BytesIO(self.text.encode("utf-8"))

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
    """Contrôleur principal du launcher TripSchool"""

    def __init__(self):
        self.DEV_MODE = True
        self.setup_config()

        self.app_launched = False
        self.app_process = None

        self.view = LauncherView(self)

    # -----------------------------------------------------
    # CONFIG
    # -----------------------------------------------------
    def setup_config(self):
        self.USER = "studentmovi"
        self.REPO = "ProjetDevOps"

        self.VERSION_FILE = "version.txt"
        self.CHANGELOG_FILE = "changelog.txt"
        self.LOCAL_EXE_PATH = "main.exe"

        self.MAIN_PY_PATH = os.path.join(os.path.dirname(__file__), "main.py")

        self.GITHUB_RAW = (
            f"https://raw.githubusercontent.com/{self.USER}/{self.REPO}/main/app"
        )

        self.LOCAL_VERSION_FILE = os.path.join(os.path.dirname(__file__), self.VERSION_FILE)
        self.LOCAL_EXE_PATH_FULL = os.path.join(os.path.dirname(__file__), self.LOCAL_EXE_PATH)

    # -----------------------------------------------------
    # VERSION
    # -----------------------------------------------------
    def get_local_version(self):
        if not os.path.exists(self.LOCAL_VERSION_FILE):
            return "0.0.0"
        with open(self.LOCAL_VERSION_FILE, "r") as f:
            return f.read().strip()

    def get_remote_version(self):
        try:
            r = requests.get(f"{self.GITHUB_RAW}/{self.VERSION_FILE}", timeout=5)
            if r.status_code == 200:
                return r.text.strip()
        except Exception as e:
            log_error(e, "Erreur en récupérant la version distante")
        return None

    # -----------------------------------------------------
    # CHANGELOG + MAJ
    # -----------------------------------------------------
    def show_changelog(self):
        try:
            r = requests.get(f"{self.GITHUB_RAW}/{self.CHANGELOG_FILE}", timeout=5)
            if r.status_code == 200:
                print("\n📝 Nouveautés :\n" + r.text)
        except:
            print("Impossible de charger le changelog.")

    def update_main_exe(self):
        try:
            r = requests.get(
                f"{self.GITHUB_RAW}/{self.LOCAL_EXE_PATH_FULL}",
                timeout=10,
                stream=True,
            )
            if r.status_code == 200:
                tmp = self.LOCAL_EXE_PATH_FULL + ".tmp"
                with open(tmp, "wb") as f:
                    shutil.copyfileobj(r.raw, f)
                shutil.move(tmp, self.LOCAL_EXE_PATH_FULL)
                print("✅ main.exe mis à jour")
        except Exception as e:
            log_error(e, "Erreur lors de la mise à jour")

    def check_update(self):
        local = self.get_local_version()
        remote = self.get_remote_version()

        if remote and remote != local:
            print(f"⚠️ Mise à jour disponible : {remote}")
            self.show_changelog()
            self.update_main_exe()
            with open(self.LOCAL_VERSION_FILE, "w") as f:
                f.write(remote)
        else:
            print("✅ Application à jour.")

    # -----------------------------------------------------
    # SÉQUENCE DE CHARGEMENT
    # -----------------------------------------------------
    def start_loading_sequence(self):
        def run_loading():
            try:
                self.view.animate_progress(0, 20, 0.5, "Initialisation...")
                self.view.animate_progress(
                    20, 40, 0.7, "Vérification des mises à jour..."
                )
                self.check_update()

                self.view.animate_progress(
                    40, 65, 0.6, "Chargement des modules..."
                )
                time.sleep(0.3)

                self.view.animate_progress(
                    65, 85, 0.5, "Préparation de l'interface..."
                )
                time.sleep(0.2)

                self.view.animate_progress(85, 100, 0.4, "Finalisation...")

                self.view.update_status("🚀 Lancement de l'application...")
                success = self.launch_app_and_wait()

                if success:
                    self.view.update_status("✅ Application lancée !")
                    time.sleep(0.5)
                    self.view.close_loader()
                else:
                    raise Exception("L'application n'a pas pu démarrer.")

            except Exception as e:
                log_error(e, "Erreur pendant le chargement")
                self.view.show_error(str(e))

        threading.Thread(target=run_loading, daemon=True).start()

    # -----------------------------------------------------
    # LANCEMENT APPLICATION
    # -----------------------------------------------------
    def launch_app_and_wait(self):
        try:
            if self.DEV_MODE:
                return self.launch_dev_mode()
            else:
                return self.launch_prod_mode()
        except:
            return False

    def launch_dev_mode(self):
        if not os.path.exists(self.MAIN_PY_PATH):
            raise FileNotFoundError("main.py introuvable")

        self.app_process = subprocess.Popen([sys.executable, self.MAIN_PY_PATH])

        for _ in range(10):
            time.sleep(0.2)
            if self.app_process.poll() is None:
                self.app_launched = True
                return True

        raise Exception("Le processus s'est fermé directement.")

    def launch_prod_mode(self):
        if not os.path.exists(self.LOCAL_EXE_PATH_FULL):
            raise FileNotFoundError("main.exe introuvable")

        os.startfile(self.LOCAL_EXE_PATH_FULL)
        time.sleep(1.5)
        self.app_launched = True
        return True

    def is_app_launched(self):
        return self.app_launched

    # -----------------------------------------------------
    def run(self):
        self.view.run()


if __name__ == "__main__":
    launcher = LauncherController()
    launcher.run()
