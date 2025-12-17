import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from component.Button import StyledButton as Button


class ExcelEventStructureInfoPopup:
    def __init__(self, parent, callback=None):
        self.parent = parent
        self.callback = callback
        self.popup = None

    def show(self):
        self.popup = tk.Toplevel(self.parent)
        self.popup.title("Structure du fichier Excel (Événements)")
        self.popup.geometry("560x420")
        self.popup.resizable(False, False)
        self.popup.transient(self.parent)
        self.popup.grab_set()

        # Centrer
        self.popup.update_idletasks()
        x = (self.popup.winfo_screenwidth() // 2) - (560 // 2)
        y = (self.popup.winfo_screenheight() // 2) - (420 // 2)
        self.popup.geometry(f"560x420+{x}+{y}")

        self._create_widgets()

    def _create_widgets(self):
        main_frame = ttk.Frame(self.popup, padding="20")
        main_frame.pack(fill="both", expand=True)

        title_label = ttk.Label(
            main_frame,
            text="📋 Structure du fichier Excel pour l'import des participants (événements)",
            font=("Arial", 13, "bold")
        )
        title_label.pack(pady=(0, 15))

        info_frame = ttk.LabelFrame(main_frame, text="Instructions", padding="15")
        info_frame.pack(fill="x", pady=(0, 15))

        instructions = [
            "📄 Le fichier doit être au format .xlsx",
            "📌 Le fichier doit contenir une feuille nommée : participants",
            "📊 Colonnes obligatoires : student_id",
            "✅ Colonnes optionnelles : classe, annee (au moins une des deux conseillée)",
            "⚠️ Les IDs inconnus seront ignorés automatiquement"
        ]
        for it in instructions:
            ttk.Label(info_frame, text=it, font=("Arial", 10)).pack(anchor="w", pady=2)

        example_frame = ttk.LabelFrame(main_frame, text="Exemple", padding="15")
        example_frame.pack(fill="x", pady=(0, 15))

        example_text = (
            "student_id | annee | classe\n"
            "17         | 3     | 3A\n"
            "18         | 3     | 3A\n"
            "25         | 4     | 4A"
        )

        ttk.Label(
            example_frame,
            text=example_text,
            font=("Courier", 10),
            justify="left"
        ).pack(anchor="w")

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side="bottom", fill="x")

        cancel_btn = Button(
            button_frame,
            text="Annuler",
            command=self._on_cancel,
            style="secondary"
        )
        cancel_btn.pack(side="right", padx=(10, 0))

        continue_btn = Button(
            button_frame,
            text="Continuer l'import",
            command=self._on_continue,
            style="primary"
        )
        continue_btn.pack(side="right")

    def _on_cancel(self):
        self.popup.destroy()

    def _on_continue(self):
        self.popup.destroy()
        if self.callback:
            self.callback()
