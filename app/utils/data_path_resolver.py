import os
from utils.settings_manager import SettingsManager


class DataPathResolver:
    def __init__(self):
        self.settings = SettingsManager()

    def get_data_root(self):
        path = self.settings.get_data_path()

        # Sécurité : fallback si pas encore configuré
        if not path:
            path = os.path.join(os.getcwd(), "data")

        os.makedirs(path, exist_ok=True)
        return path

    def get_file(self, filename):
        return os.path.join(self.get_data_root(), filename)
