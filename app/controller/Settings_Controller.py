from tkinter import messagebox
from utils.settings_manager import SettingsManager


class SettingsController:
    def __init__(self):
        self.settings = SettingsManager()

    def get_settings(self):
        return {
            "data_path": self.settings.get_data_path(),
            "font": self.settings.get_font(),
            "auto_update": self.settings.is_auto_update_enabled()
        }

    def save_settings(self, data_path, font, auto_update):
        if not data_path:
            messagebox.showerror(
                "Erreur",
                "Le dossier de données est obligatoire."
            )
            return False

        self.settings.set_data_path(data_path)
        self.settings.set_font(font)
        self.settings.set_auto_update(auto_update)
        return True
