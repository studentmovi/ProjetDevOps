import os
import shutil
import sys
import subprocess
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
    if DEV_MODE:
        if os.path.exists(MAIN_PY_PATH):
            log_info("Lancement de main.py en mode dev...")
            try:
                subprocess.run([sys.executable, MAIN_PY_PATH], check=True)
            except subprocess.CalledProcessError as e:
                log_error(e, "Erreur lors du lancement de main.py")
                print("❌ Erreur lors du lancement de main.py :", e)
        else:
            log_warning("main.py introuvable !")
            print("⚠️ main.py introuvable !")
    else:
        if os.path.exists(LOCAL_EXE_PATH):
            os.startfile(LOCAL_EXE_PATH)
        else:
            log_warning("main.exe introuvable ! Compilez d'abord main.py en exe.")
            print("⚠️ main.exe introuvable ! Compilez d'abord main.py en exe.")


if __name__ == "__main__":
    check_update()
    run_app()

