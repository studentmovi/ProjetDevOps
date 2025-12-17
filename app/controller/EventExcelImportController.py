import pandas as pd
from tkinter import filedialog, messagebox
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from popups.ExcelEventStructureInfoPopup import ExcelEventStructureInfoPopup
from data.event_data_manager import event_manager
from utils.logger import log_error, log_info


class EventExcelImportController:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.on_import_success_callback = None

        # Nom de feuille attendu
        self.required_sheet = "participants"

        # Colonnes attendues
        self.required_columns = ["student_id"]

    def start_import_process(self, event_id):
        """Démarre le processus d'import Excel pour un événement précis"""
        self.event_id = event_id

        try:
            info_popup = ExcelEventStructureInfoPopup(
                self.parent_window,
                callback=self._show_file_dialog
            )
            info_popup.show()

        except Exception as e:
            log_error(f"Erreur démarrage import event: {str(e)}")
            messagebox.showerror("Erreur", "Impossible de démarrer l'import Excel (événement).")

    def _show_file_dialog(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Sélectionner le fichier Excel (participants)",
                filetypes=[("Fichiers Excel", "*.xlsx"), ("Tous les fichiers", "*.*")],
                initialdir=os.path.expanduser("~")
            )

            if file_path:
                self._process_excel_file(file_path)

        except Exception as e:
            log_error(f"Erreur file dialog event: {str(e)}")
            messagebox.showerror("Erreur", "Erreur lors de la sélection du fichier.")

    def _process_excel_file(self, file_path):
        try:
            if not file_path.lower().endswith(".xlsx"):
                messagebox.showerror("Format invalide", "Le fichier doit être au format .xlsx")
                return

            log_info(f"Lecture Excel participants: {file_path}")

            # Lire la feuille "participants"
            df = pd.read_excel(file_path, sheet_name=self.required_sheet, engine="openpyxl")

            # Nettoyage colonnes
            df.columns = [str(c).strip() for c in df.columns]

            # Vérif colonnes
            for col in self.required_columns:
                if col not in df.columns:
                    messagebox.showerror(
                        "Structure invalide",
                        f"Colonne obligatoire manquante: {col}\n\nColonnes trouvées: {', '.join(df.columns)}"
                    )
                    return

            imported = 0
            ignored = 0

            for _, row in df.iterrows():
                student_id = row.get("student_id")

                if pd.isna(student_id):
                    ignored += 1
                    continue

                try:
                    student_id = int(student_id)
                    # ✅ Réutilise ta logique JSON existante
                    event_manager.assign_student_to_event(student_id, self.event_id)
                    imported += 1
                except Exception:
                    ignored += 1

            messagebox.showinfo(
                "Import terminé",
                f"✅ Participants importés: {imported}\n"
                f"⚠️ Lignes ignorées: {ignored}"
            )

            if self.on_import_success_callback:
                self.on_import_success_callback()

        except ValueError as e:
            log_error(f"Excel mal formé: {str(e)}")
            messagebox.showerror("Erreur", "Le fichier Excel n'a pas la bonne structure.")
        except Exception as e:
            log_error(f"Erreur import event excel: {str(e)}")
            messagebox.showerror("Erreur", f"Impossible d'importer.\n\n{str(e)}")
