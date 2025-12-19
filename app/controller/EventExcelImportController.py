import pandas as pd
from tkinter import filedialog, messagebox

from data.event_data_manager import event_manager
from data.sample_data import get_students_data_source
from popups.ExcelEventStructureInfoPopup import ExcelEventStructureInfoPopup
from utils.logger import log_error, log_info


class EventExcelImportController:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.on_import_success_callback = None

        self.required_columns = [
            "id",
            "nom",
            "date",
            "categorie",
            "cout_total"
        ]

    # ====================================================
    #  POINT D’ENTRÉE
    # ====================================================
    def start_import_process(self):
        """
        Affiche le popup d'information avant l'import
        """
        try:
            popup = ExcelEventStructureInfoPopup(
                self.parent_window,
                callback=self._open_file_dialog
            )
            popup.show()

        except Exception as e:
            log_error(str(e))
            messagebox.showerror(
                "Erreur",
                "Impossible d'afficher les informations d'import Excel"
            )

    # ====================================================
    #  SÉLECTION DU FICHIER
    # ====================================================
    def _open_file_dialog(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Importer des événements (Excel)",
                filetypes=[("Excel", "*.xlsx")]
            )

            if file_path:
                self._process_excel(file_path)

        except Exception as e:
            log_error(str(e))
            messagebox.showerror(
                "Erreur",
                "Erreur lors de la sélection du fichier Excel"
            )

    # ====================================================
    #  TRAITEMENT EXCEL
    # ====================================================
    def _process_excel(self, file_path):
        try:
            df = pd.read_excel(file_path, engine="openpyxl")
            df.columns = [c.strip() for c in df.columns]

            # Vérification colonnes obligatoires
            for col in self.required_columns:
                if col not in df.columns:
                    raise ValueError(f"Colonne obligatoire manquante : {col}")

            students = get_students_data_source()

            imported = 0
            ignored = 0

            for index, row in df.iterrows():
                try:
                    event_id = str(row["id"]).strip()

                    # 🔁 Ignorer si l'événement existe déjà
                    if event_manager.get_event(event_id):
                        log_info(f"Événement déjà existant ignoré : {event_id}")
                        ignored += 1
                        continue

                    ventes_raw = str(row.get("ventes_activees", "")).lower()
                    ventes_activees = ventes_raw in ("true", "1", "yes", "oui")

                    event_data = {
                        "id": event_id,
                        "nom": str(row["nom"]).strip(),
                        "date": str(row["date"]).strip(),
                        "categorie": str(row["categorie"]).strip(),
                        "cout_total": float(row["cout_total"]),
                        "ventes_activees": ventes_activees,
                        "participants": {},
                        "total_ventes": 0.0,
                        "description": str(row.get("description", "")).strip()
                    }

                    # Création de l'événement
                    event_manager.create_event(event_data)

                    # Assignation optionnelle des participants
                    self._assign_participants(row, event_id, students)

                    imported += 1

                except Exception as e:
                    log_error(f"Ligne {index + 2} ignorée : {e}")
                    ignored += 1

            messagebox.showinfo(
                "Import terminé",
                f"✅ Événements importés : {imported}\n"
                f"⚠️ Lignes ignorées : {ignored}"
            )

            if self.on_import_success_callback:
                self.on_import_success_callback()

        except Exception as e:
            log_error(str(e))
            messagebox.showerror("Erreur", str(e))

    # ====================================================
    #  PARTICIPANTS OPTIONNELS
    # ====================================================
    def _assign_participants(self, row, event_id, students):
        """
        Ajoute les participants selon la priorité :
        1. student_id
        2. classe
        3. annee
        """

        # 1️⃣ student_id
        if "student_id" in row and not pd.isna(row["student_id"]):
            event_manager.assign_student_to_event(
                int(row["student_id"]), event_id
            )
            return

        # 2️⃣ classe
        if "classe" in row and not pd.isna(row["classe"]):
            classe = str(row["classe"]).strip()
            for s in students:
                if s.get("classe") == classe:
                    event_manager.assign_student_to_event(s["id"], event_id)
            return

        # 3️⃣ année
        if "annee" in row and not pd.isna(row["annee"]):
            annee = str(row["annee"]).strip()
            for s in students:
                if s.get("annee") == annee:
                    event_manager.assign_student_to_event(s["id"], event_id)

        # Sinon : aucun participant
        return
