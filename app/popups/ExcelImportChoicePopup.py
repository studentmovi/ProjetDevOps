import tkinter as tk
from tkinter import ttk

class ExcelImportChoicePopup:
    def __init__(self, parent, on_students, on_events):
        self.popup = tk.Toplevel(parent)
        self.popup.title("Choix de l'import Excel")
        self.popup.geometry("360x200")
        self.popup.transient(parent)
        self.popup.grab_set()

        frame = ttk.Frame(self.popup, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Que souhaitez-vous importer ?",
            font=("Arial", 12, "bold")
        ).pack(pady=(0, 20))

        ttk.Button(
            frame,
            text="👥 Élèves",
            command=lambda: self._select(on_students)
        ).pack(fill="x", pady=5)

        ttk.Button(
            frame,
            text="📅 Participants d’événement",
            command=lambda: self._select(on_events)
        ).pack(fill="x", pady=5)

    def _select(self, callback):
        self.popup.destroy()
        callback()
