import json
import os
from pathlib import Path


class SettingsManager:
    DEFAULT_SETTINGS = {
        "data_path": "",
        "font": "Arial",
        "auto_update": True
    }

    def __init__(self):
        self.settings_file = os.path.join(
            Path.home(),
            ".pytrip_settings.json"
        )
        self.settings = self._load_settings()

    def _load_settings(self):
        if not os.path.exists(self.settings_file):
            return self.DEFAULT_SETTINGS.copy()

        try:
            with open(self.settings_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {**self.DEFAULT_SETTINGS, **data}
        except Exception:
            return self.DEFAULT_SETTINGS.copy()

    def save(self):
        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)

    # ===== Getters =====
    def get_data_path(self):
        return self.settings["data_path"]

    def get_font(self):
        return self.settings["font"]

    def is_auto_update_enabled(self):
        return self.settings["auto_update"]

    # ===== Setters =====
    def set_data_path(self, path):
        self.settings["data_path"] = path
        self.save()

    def set_font(self, font):
        self.settings["font"] = font
        self.save()

    def set_auto_update(self, value: bool):
        self.settings["auto_update"] = value
        self.save()
