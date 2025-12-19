import tkinter as tk
from tkinter import ttk


class ExcelEventStructureInfoPopup:
    def __init__(self, parent, callback=None):
        self.parent = parent
        self.callback = callback
        self.popup = None

    def show(self):
        self.popup = tk.Toplevel(self.parent)
        self.popup.title("Structure du fichier Excel (Événements)")
        self.popup.geometry("720x560")
        self.popup.resizable(False, False)
        self.popup.transient(self.parent)
        self.popup.grab_set()

        # Fermer avec Échap
        self.popup.bind("<Escape>", lambda e: self.popup.destroy())

        self._create_widgets()

    def _create_widgets(self):
        # ===== CONTENEUR PRINCIPAL =====
        container = ttk.Frame(self.popup)
        container.pack(fill="both", expand=True)

        # ===== ZONE SCROLLABLE =====
        canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)

        scroll_frame = ttk.Frame(canvas, padding=20)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ===== CONTENU =====
        ttk.Label(
            scroll_frame,
            text="📋 Import Excel — Événements",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(0, 10))

        ttk.Label(
            scroll_frame,
            text="Le fichier Excel doit respecter la structure suivante :",
            font=("Arial", 10)
        ).pack(anchor="w")

        # Colonnes
        cols_required = [
            "id (unique, sans espaces)",
            "nom",
            "date (YYYY-MM-DD)",
            "categorie",
            "cout_total (nombre)"
        ]

        cols_optional = [
            "ventes_activees (TRUE / FALSE)",
            "description",
            "student_id (1 élève précis)",
            "classe (ex : 3A)",
            "annee (ex : 3)"
        ]

        box_req = ttk.LabelFrame(scroll_frame, text="Colonnes obligatoires", padding=10)
        box_req.pack(fill="x", pady=(10, 5))
        for c in cols_required:
            ttk.Label(box_req, text=f"• {c}").pack(anchor="w")

        box_opt = ttk.LabelFrame(scroll_frame, text="Colonnes optionnelles", padding=10)
        box_opt.pack(fill="x", pady=(5, 10))
        for c in cols_optional:
            ttk.Label(box_opt, text=f"• {c}").pack(anchor="w")

        # Exemple
        example_frame = ttk.LabelFrame(scroll_frame, text="Exemple de fichier Excel", padding=10)
        example_frame.pack(fill="x", pady=(10, 10))

        example_text = (
            "id              | nom             | date       | categorie | cout_total | classe\n"
            "sortie_theatre  | Sortie Théâtre  | 2025-11-15 | théâtre   | 450        | 3A\n"
            "voyage_paris    | Voyage Paris    | 2025-12-10 | voyage    | 1200       | 5\n"
            "concert_noel    | Concert Noël    | 2025-12-20 | concert   | 600        |"
        )

        ttk.Label(
            example_frame,
            text=example_text,
            font=("Courier New", 9),
            justify="left"
        ).pack(anchor="w")

        ttk.Label(
            scroll_frame,
            text=(
                "ℹ️ Une ligne = un événement\n"
                "ℹ️ Les participants sont ajoutés automatiquement si student_id, classe ou annee est présent\n"
                "⚠️ Si l'ID existe déjà, l'événement sera ignoré"
            ),
            font=("Arial", 9)
        ).pack(anchor="w", pady=(10, 20))

        # ===== BOUTONS FIXÉS EN BAS =====
        btns = ttk.Frame(self.popup, padding=10)
        btns.pack(fill="x")

        ttk.Button(
            btns,
            text="Annuler",
            command=self.popup.destroy
        ).pack(side="right", padx=5)

        ttk.Button(
            btns,
            text="Importer",
            command=self._import
        ).pack(side="right")

    def _import(self):
        self.popup.destroy()
        if self.callback:
            self.callback()
