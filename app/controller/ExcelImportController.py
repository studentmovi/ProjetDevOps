import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from popups.ExcelStructureInfoPopup import ExcelStructureInfoPopup
from utils.logger import log_error, log_info, log_warning


def extract_year_from_class(classe: str):
    """
    Extrait l'année depuis une classe.
    Exemples:
    - 1A -> 1
    - 4D -> 4
    - 6INFO -> 6
    """
    if not classe:
        return None

    match = re.match(r"(\d+)", classe.strip())
    if match:
        return match.group(1)

    return None


class ExcelImportController:
    def __init__(self, parent_window):
        """
        Contrôleur pour l'import Excel des élèves
        """
        self.parent_window = parent_window
        self.imported_students = []
        self.excel_data_loaded = False

        # Callback optionnel
        self.on_import_success_callback = None

        # Colonnes attendues
        self.required_columns = ['Nom', 'Prénom', 'Classe', 'Email']

    # ====================================================
    #  Lancement import
    # ====================================================
    def start_import_process(self):
        try:
            print("START IMPORT EXCEL")
            print("Parent window =", self.parent_window)

            info_popup = ExcelStructureInfoPopup(
                self.parent_window,
                callback=self._show_file_dialog
            )
            info_popup.show()

        except Exception as e:
            import traceback
            traceback.print_exc()   # 🔥 LA LIGNE QUI MANQUAIT
            messagebox.showerror(
                "Erreur",
                f"Impossible de démarrer l'import Excel.\n\n{e}"
            )

            try:
                info_popup = ExcelStructureInfoPopup(
                    self.parent_window,
                    callback=self._show_file_dialog
                )
                info_popup.show()

            except Exception as e:
                log_error(f"Erreur lors du démarrage de l'import: {e}")
                messagebox.showerror("Erreur", "Impossible de démarrer l'import Excel.")

    # ====================================================
    #  Sélection fichier
    # ====================================================
    def _show_file_dialog(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Sélectionner le fichier Excel des élèves",
                filetypes=[("Fichiers Excel", "*.xlsx")],
                initialdir=os.path.expanduser("~")
            )

            if file_path:
                self._process_excel_file(file_path)

        except Exception as e:
            log_error(f"Erreur sélection fichier: {e}")
            messagebox.showerror("Erreur", "Erreur lors de la sélection du fichier.")

    # ====================================================
    #  Traitement Excel
    # ====================================================
    def _process_excel_file(self, file_path):
        try:
            if not file_path.lower().endswith(".xlsx"):
                messagebox.showerror("Erreur", "Le fichier doit être au format .xlsx")
                return

            log_info(f"Lecture Excel: {file_path}")
            df = pd.read_excel(file_path, engine="openpyxl")

            if not self._validate_columns(df):
                return

            students = self._process_student_data(df)

            if not students:
                return

            self.imported_students = students
            self.excel_data_loaded = True

            messagebox.showinfo(
                "Import réussi",
                f"Import terminé avec succès.\n\n"
                f"• {len(students)} élèves importés\n"
                f"• Fichier : {os.path.basename(file_path)}"
            )

            log_info(f"Import Excel réussi ({len(students)} élèves)")

            if self.on_import_success_callback:
                self.on_import_success_callback()

        except Exception as e:
            log_error(f"Erreur traitement Excel: {e}")
            messagebox.showerror(
                "Erreur",
                f"Impossible de lire le fichier Excel.\n\n{e}"
            )

    # ====================================================
    #  Validation structure
    # ====================================================
    def _validate_columns(self, df):
        df_columns = [col.strip() for col in df.columns]
        missing = [c for c in self.required_columns if c not in df_columns]

        if missing:
            messagebox.showerror(
                "Erreur de structure",
                f"Colonnes manquantes : {', '.join(missing)}\n\n"
                f"Colonnes attendues : {', '.join(self.required_columns)}"
            )
            return False

        return True

    # ====================================================
    #  Traitement élèves
    # ====================================================
    def _process_student_data(self, df):
        students = []
        errors = []

        for index, row in df.iterrows():
            try:
                nom = str(row['Nom']).strip() if pd.notna(row['Nom']) else ""
                prenom = str(row['Prénom']).strip() if pd.notna(row['Prénom']) else ""
                classe = str(row['Classe']).strip() if pd.notna(row['Classe']) else ""
                email = str(row['Email']).strip() if pd.notna(row['Email']) else ""

                if not nom or not prenom:
                    errors.append(f"Ligne {index + 2} : nom/prénom manquant")
                    continue

                if not classe:
                    errors.append(f"Ligne {index + 2} : classe manquante")
                    continue

                annee = extract_year_from_class(classe)
                if not annee:
                    errors.append(
                        f"Ligne {index + 2} : impossible de déduire l'année depuis '{classe}'"
                    )
                    continue

                if email and '@' not in email:
                    errors.append(f"Ligne {index + 2} : email invalide ({email})")
                    continue

                student = {
                    "id": len(students) + 1,
                    "nom": nom,
                    "prenom": prenom,
                    "classe": classe,
                    "annee": annee,
                    "email": email,
                    "source": "excel"
                }

                students.append(student)

            except Exception as e:
                errors.append(f"Ligne {index + 2} : erreur ({e})")

        if errors:
            messagebox.showwarning(
                "Avertissements",
                "Erreurs détectées :\n\n" + "\n".join(errors[:10]) +
                (f"\n… et {len(errors) - 10} autres" if len(errors) > 10 else "")
            )

        if not students:
            messagebox.showerror("Erreur", "Aucune donnée valide trouvée.")
            return []

        return students

    # ====================================================
    #  Accès aux données
    # ====================================================
    def get_students_data(self):
        if self.excel_data_loaded and self.imported_students:
            return self.imported_students, True
        return None, False

    def reset_to_json_data(self):
        self.imported_students = []
        self.excel_data_loaded = False
        log_info("Retour aux données JSON")
