import tkinter as tk
from tkinter import ttk, messagebox
import uuid
from datetime import datetime

from tkcalendar import DateEntry

from data.event_data_manager import event_manager
from data.sample_data import get_all_students, get_available_years, get_available_classes


class EventFormPopup:
    def __init__(self, parent, on_save_callback, event=None):
        """
        Popup de création / modification d'événement
        Toute la persistance passe par EventDataManager (JSON)
        """
        self.parent = parent
        self.event = event
        self.on_save_callback = on_save_callback

        self.popup = tk.Toplevel(parent)
        self.popup.title("✏️ Modifier l'événement" if event else "➕ Nouvel événement")
        self.popup.geometry("560x650")
        self.popup.transient(parent)
        self.popup.grab_set()

        self._create_widgets()

    # ====================================================
    #  UI
    # ====================================================
    def _create_widgets(self):
        frame = ttk.Frame(self.popup, padding=20)
        frame.pack(fill="both", expand=True)

        # ---------- NOM ----------
        ttk.Label(frame, text="Nom de l'événement").pack(anchor="w")
        self.name_var = tk.StringVar(value=self.event["nom"] if self.event else "")
        ttk.Entry(frame, textvariable=self.name_var).pack(fill="x", pady=5)

        # ---------- DATE (CALENDRIER) ----------
        ttk.Label(frame, text="Date").pack(anchor="w")
        self.date_var = tk.StringVar(value=self.event["date"] if self.event else "")

        DateEntry(
            frame,
            textvariable=self.date_var,
            date_pattern="yyyy-mm-dd",
            firstweekday="monday"
        ).pack(fill="x", pady=5)

        # ---------- CATÉGORIE ----------
        ttk.Label(frame, text="Catégorie").pack(anchor="w")
        self.category_var = tk.StringVar(
            value=self.event.get("categorie", "") if self.event else ""
        )
        ttk.Combobox(
            frame,
            textvariable=self.category_var,
            values=["musée", "théâtre", "concert", "voyage", "autre"],
            state="readonly"
        ).pack(fill="x", pady=5)

        # ---------- COÛT ----------
        ttk.Label(frame, text="Coût total (€)").pack(anchor="w")
        self.cost_var = tk.DoubleVar(value=self.event["cout_total"] if self.event else 0.0)
        ttk.Entry(frame, textvariable=self.cost_var).pack(fill="x", pady=5)

        # ---------- DESCRIPTION ----------
        ttk.Label(frame, text="Description").pack(anchor="w")
        self.desc_text = tk.Text(frame, height=4)
        self.desc_text.pack(fill="x", pady=5)
        if self.event:
            self.desc_text.insert("1.0", self.event.get("description", ""))

        # ---------- VENTES ----------
        self.sales_var = tk.BooleanVar(
            value=self.event.get("ventes_activees", False) if self.event else False
        )
        ttk.Checkbutton(
            frame,
            text="Ventes activées",
            variable=self.sales_var
        ).pack(anchor="w", pady=10)

        # ---------- INSCRIPTION PAR GROUPE ----------
        ttk.Separator(frame).pack(fill="x", pady=10)

        ttk.Label(frame, text="Ajouter des élèves par groupe").pack(anchor="w")

        group_frame = ttk.Frame(frame)
        group_frame.pack(fill="x", pady=5)

        self.year_var = tk.StringVar()
        self.class_var = tk.StringVar()

        ttk.Combobox(
            group_frame,
            textvariable=self.year_var,
            values=get_available_years(),
            width=10,
            state="readonly"
        ).pack(side="left", padx=5)

        ttk.Combobox(
            group_frame,
            textvariable=self.class_var,
            values=get_available_classes(),
            width=10,
            state="readonly"
        ).pack(side="left", padx=5)

        ttk.Button(
            group_frame,
            text="➕ Ajouter les élèves",
            command=self._add_students_by_group
        ).pack(side="left", padx=5)

        # ---------- BOUTONS ----------
        btns = ttk.Frame(frame)
        btns.pack(fill="x", pady=20)

        ttk.Button(btns, text="Annuler", command=self.popup.destroy).pack(side="right")
        ttk.Button(btns, text="Enregistrer", command=self._save).pack(side="right", padx=5)

    # ====================================================
    #  LOGIQUE
    # ====================================================
    def _save(self):
        try:
            name = self.name_var.get().strip()
            date = self.date_var.get().strip()

            if not name:
                raise ValueError("Le nom est obligatoire")

            # Validation date ISO
            datetime.fromisoformat(date)

            data = {
                "nom": name,
                "date": date,
                "categorie": self.category_var.get(),
                "cout_total": float(self.cost_var.get()),
                "description": self.desc_text.get("1.0", "end").strip(),
                "ventes_activees": self.sales_var.get()
            }

            if self.event:
                # ✏️ MODIFICATION
                event_manager.update_event(self.event["id"], data)
            else:
                # ➕ CRÉATION
                event_id = f"{name.lower().replace(' ', '_')}_{uuid.uuid4().hex[:6]}"
                data.update({
                    "id": event_id,
                    "participants": {},
                    "total_ventes": 0.0
                })
                event_manager.create_event(data)
                self.event = event_manager.get_event(event_id)

            self.on_save_callback()
            messagebox.showinfo("Succès", "Événement enregistré avec succès")

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def _add_students_by_group(self):
        if not self.event:
            messagebox.showwarning(
                "Information",
                "Enregistre d'abord l'événement avant d'ajouter des élèves"
            )
            return

        year = self.year_var.get()
        classe = self.class_var.get()

        if not year and not classe:
            messagebox.showwarning("Erreur", "Sélectionne une année ou une classe")
            return

        students = get_all_students()
        added = 0

        for student in students:
            if (year and student.get("annee") == year) or \
               (classe and student.get("classe") == classe):
                event_manager.assign_student_to_event(student["id"], self.event["id"])
                added += 1

        self.on_save_callback()

        messagebox.showinfo(
            "Succès",
            f"{added} élèves ajoutés à l'événement"
        )
