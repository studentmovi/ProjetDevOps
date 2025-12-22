# utils/font_manager.py
import tkinter.font as tkfont
from tkinter import ttk
import json
import os


class FontManager:
    DEFAULT_FONT = {
        "family": "Segoe UI",
        "size": 10
    }

    SETTINGS_FILE = "font_settings.json"

    def __init__(self, root):
        self.root = root
        self.font_config = self.DEFAULT_FONT.copy()
        self._load()
        self._apply()

    # =====================================================
    # LOAD / SAVE
    # =====================================================

    def _load(self):
        if os.path.exists(self.SETTINGS_FILE):
            try:
                with open(self.SETTINGS_FILE, "r", encoding="utf-8") as f:
                    self.font_config.update(json.load(f))
            except Exception:
                pass

    def save(self):
        with open(self.SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.font_config, f, indent=2)

    # =====================================================
    # APPLY
    # =====================================================

    def _apply(self):
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(
            family=self.font_config["family"],
            size=self.font_config["size"]
        )

        text_font = tkfont.nametofont("TkTextFont")
        text_font.configure(
            family=self.font_config["family"],
            size=self.font_config["size"]
        )

        fixed_font = tkfont.nametofont("TkFixedFont")
        fixed_font.configure(
            family=self.font_config["family"],
            size=self.font_config["size"]
        )

        # ttk widgets
        style = ttk.Style()
        style.configure(".", font=(self.font_config["family"], self.font_config["size"]))

    # =====================================================
    # API PUBLIQUE
    # =====================================================

    def set_font(self, family, size):
        self.font_config["family"] = family
        self.font_config["size"] = size
        self._apply()
        self.save()

    def get_font(self):
        return self.font_config.copy()
