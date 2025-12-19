import tkinter as tk
from tkinter import ttk, messagebox


class StudentDetailPopup:
    """
    Popup de détail d'un élève
    - affiche les infos
    - permet de modifier classe / année
    - renvoie l'élève modifié via callback
    """

    def __init__(self, parent, student, on_save_callback=None, styles=None):
        self.parent = parent
        self.student = student.copy()
        self.on_save_callback = on_save_callback
        self.styles = styles

        self.popup = None
        self.class_var = tk.StringVar()
        self.year_var = tk.StringVar()

        self._create_popup()

    # =========================================================
    # SETUP
    # =========================================================

    def _create_popup(self):
        self.popup = tk.Toplevel(self.parent)
        self.popup.title(
            f"Détails - {self.student.get('prenom', '')} {self.student.get('nom', '')}"
        )
        self.popup.geometry("420x320")
        self.popup.resizable(False, False)
        self.popup.transient(self.parent)
        self.popup.grab_set()

        bg = self.styles.colors['off_white'] if self.styles else "#f0f0f0"
        self.popup.configure(bg=bg)

        self._center_window()
        self._create_content()

    def _center_window(self):
        self.popup.update_idletasks()
        x = (self.popup.winfo_screenwidth() // 2) - 210
        y = (self.popup.winfo_screenheight() // 2) - 160
        self.popup.geometry(f"+{x}+{y}")

    # =========================================================
    # CONTENT
    # =========================================================

    def _create_content(self):
        frame = tk.Frame(self.popup, bg=self.popup.cget("bg"))
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Infos fixes
        self._info_row(frame, "Nom", self.student.get("nom", ""))
        self._info_row(frame, "Prénom", self.student.get("prenom", ""))

        # Classe (modifiable)
        self.class_var.set(self.student.get("classe", ""))
        self._combo_row(
            frame,
            "Classe",
            self.class_var,
            values=[]
        )

        # Année (modifiable)
        self.year_var.set(str(self.student.get("annee", "")))
        self._combo_row(
            frame,
            "Année",
            self.year_var,
            values=["1", "2", "3", "4", "5", "6"]
        )

        # Boutons
        btn_frame = tk.Frame(frame, bg=frame.cget("bg"))
        btn_frame.pack(fill="x", pady=(20, 0))

        tk.Button(
            btn_frame,
            text="Annuler",
            command=self.close,
            width=10
        ).pack(side="right", padx=(5, 0))

        tk.Button(
            btn_frame,
            text="Enregistrer",
            command=self._save,
            width=12
        ).pack(side="right")

    # =========================================================
    # UI HELPERS
    # =========================================================

    def _info_row(self, parent, label, value):
        row = tk.Frame(parent, bg=parent.cget("bg"))
        row.pack(fill="x", pady=5)

        tk.Label(
            row,
            text=f"{label} :",
            width=12,
            anchor="w",
            bg=row.cget("bg")
        ).pack(side="left")

        tk.Label(
            row,
            text=value,
            anchor="w",
            bg=row.cget("bg"),
            fg="#555"
        ).pack(side="left")

    def _combo_row(self, parent, label, var, values):
        row = tk.Frame(parent, bg=parent.cget("bg"))
        row.pack(fill="x", pady=5)

        tk.Label(
            row,
            text=f"{label} :",
            width=12,
            anchor="w",
            bg=row.cget("bg")
        ).pack(side="left")

        combo = ttk.Combobox(
            row,
            textvariable=var,
            values=values,
            state="readonly",
            width=10
        )
        combo.pack(side="left")

    # =========================================================
    # ACTIONS
    # =========================================================

    def _save(self):
        if not self.class_var.get() or not self.year_var.get():
            messagebox.showerror(
                "Erreur",
                "La classe et l'année sont obligatoires."
            )
            return

        updated_student = self.student.copy()
        updated_student["classe"] = self.class_var.get()
        updated_student["annee"] = int(self.year_var.get())

        if self.on_save_callback:
            self.on_save_callback(updated_student)

        self.close()

    def close(self):
        self.popup.destroy()
# ====================================================