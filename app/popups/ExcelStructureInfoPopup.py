import tkinter as tk
from tkinter import ttk
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from component.Button import StyledButton as Button


class ExcelStructureInfoPopup:
    def __init__(self, parent, callback=None):
        self.parent = parent
        self.callback = callback
        self.popup = None

    # ====================================================
    #  AFFICHAGE
    # ====================================================
    def show(self):
        self.popup = tk.Toplevel(self.parent)
        self.popup.title("Structure du fichier Excel")
        self.popup.geometry("720x560")
        self.popup.resizable(False, False)
        self.popup.transient(self.parent)
        self.popup.grab_set()

        # Centrage écran
        self.popup.update_idletasks()
        w, h = 720, 560
        x = (self.popup.winfo_screenwidth() // 2) - (w // 2)
        y = (self.popup.winfo_screenheight() // 2) - (h // 2)
        self.popup.geometry(f"{w}x{h}+{x}+{y}")

        self._create_widgets()

    # ====================================================
    #  UI
    # ====================================================
    def _create_widgets(self):
        # Canvas + Scrollbar (future-proof)
        canvas = tk.Canvas(self.popup, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.popup, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        content = ttk.Frame(canvas, padding=25)
        canvas.create_window((0, 0), window=content, anchor="nw")

        content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # ================= TITRE =================
        ttk.Label(
            content,
            text="📋 Structure du fichier Excel pour l'import des élèves",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", pady=(0, 25))

        # ================= INSTRUCTIONS =================
        info_frame = ttk.LabelFrame(content, text="Instructions", padding=20)
        info_frame.pack(fill="x", pady=(0, 25))

        instructions = [
            "📁 Nom du fichier : eleves.xlsx",
            "📄 Le fichier doit contenir une seule feuille Excel",
            "📊 Colonnes obligatoires (dans cet ordre) :"
        ]

        for txt in instructions:
            ttk.Label(
                info_frame,
                text=txt,
                font=("Segoe UI", 11)
            ).pack(anchor="w", pady=4)

        ttk.Label(info_frame, text="").pack()

        columns = ["1. Nom", "2. Prénom", "3. Classe", "4. Email"]
        for col in columns:
            ttk.Label(
                info_frame,
                text=f"• {col}",
                font=("Segoe UI", 11)
            ).pack(anchor="w", padx=20, pady=2)

        # ================= EXEMPLE =================
        example_frame = ttk.LabelFrame(content, text="Exemple", padding=20)
        example_frame.pack(fill="x", pady=(0, 25))

        example_text = (
            "Nom      | Prénom  | Classe | Email\n"
            "---------+---------+--------+---------------------------\n"
            "Dupont   | Pierre  | 3A     | pierre.dupont@email.com\n"
            "Martin   | Sophie  | 2B     | sophie.martin@email.com"
        )

        ttk.Label(
            example_frame,
            text=example_text,
            font=("Consolas", 10),
            justify="left"
        ).pack(anchor="w")

        # ================= BOUTONS =================
        btn_frame = ttk.Frame(content)
        btn_frame.pack(fill="x", pady=(10, 0))

        Button(
            btn_frame,
            text="Annuler",
            command=self._on_cancel,
            style="light"
        ).pack(side="right", padx=(10, 0))

        Button(
            btn_frame,
            text="Continuer l'import",
            command=self._on_continue,
            style="primary"
        ).pack(side="right")

    # ====================================================
    #  ACTIONS
    # ====================================================
    def _on_cancel(self):
        self.popup.destroy()

    def _on_continue(self):
        self.popup.destroy()
        if self.callback:
            self.callback()
