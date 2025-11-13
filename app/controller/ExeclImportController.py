import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from popups.ExcelStructureInfoPopup import ExcelStructureInfoPopup
from utils.logger import log_error, log_info, log_warning

class ExcelImportController:
    def __init__(self, parent_window):
        """
        Contrôleur pour l'import Excel des élèves
        
        Args:
            parent_window: Fenêtre parent pour les popups
        """
        self.parent_window = parent_window
        self.imported_students = []
        self.excel_data_loaded = False
        
        # Callback pour notifier le succès de l'import
        self.on_import_success_callback = None
        
        # Colonnes attendues dans le fichier Excel
        self.required_columns = ['Nom', 'Prénom', 'Classe', 'Email']
        
    def start_import_process(self):
        """Démarre le processus d'import Excel"""
        try:
            # Afficher d'abord la popup d'information
            info_popup = ExcelStructureInfoPopup(
                self.parent_window, 
                callback=self._show_file_dialog
            )
            info_popup.show()
            
        except Exception as e:
            log_error(f"Erreur lors du démarrage de l'import: {str(e)}")
            messagebox.showerror("Erreur", "Une erreur est survenue lors du démarrage de l'import.")
            
    def _show_file_dialog(self):
        """Affiche la boîte de dialogue de sélection de fichier"""
        try:
            file_path = filedialog.askopenfilename(
                title="Sélectionner le fichier Excel des élèves",
                filetypes=[
                    ("Fichiers Excel", "*.xlsx"),
                    ("Tous les fichiers", "*.*")
                ],
                initialdir=os.path.expanduser("~")
            )
            
            if file_path:
                self._process_excel_file(file_path)
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la sélection de fichier: {str(e)}")
            messagebox.showerror("Erreur", "Erreur lors de la sélection du fichier.")
            
    def _process_excel_file(self, file_path):
        """
        Traite le fichier Excel sélectionné
        
        Args:
            file_path: Chemin vers le fichier Excel
        """
        try:
            # Vérifier l'extension
            if not file_path.lower().endswith('.xlsx'):
                messagebox.showerror(
                    "Erreur de format", 
                    "Le fichier doit être au format .xlsx"
                )
                return
                
            # Lire le fichier Excel
            log_info(f"Lecture du fichier Excel: {file_path}")
            df = pd.read_excel(file_path, engine='openpyxl')
            
            # Vérifier les colonnes
            if not self._validate_columns(df):
                return
                
            # Valider et traiter les données
            students = self._process_student_data(df)
            
            if students:
                self.imported_students = students
                self.excel_data_loaded = True
                
                # Popup de succès
                messagebox.showinfo(
                    "Import réussi !", 
                    f"Import réussi !\n\n"
                    f"• {len(students)} élèves importés\n"
                    f"• Fichier: {os.path.basename(file_path)}\n\n"
                    f"Les données Excel sont maintenant utilisées."
                )
                
                log_info(f"Import Excel réussi: {len(students)} élèves")
                
                # Appeler le callback de succès si défini
                if self.on_import_success_callback:
                    self.on_import_success_callback()
                
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Le fichier sélectionné n'existe pas.")
        except pd.errors.EmptyDataError:
            messagebox.showerror("Erreur", "Le fichier Excel est vide.")
        except Exception as e:
            log_error(f"Erreur lors du traitement du fichier Excel: {str(e)}")
            messagebox.showerror(
                "Erreur de lecture", 
                f"Impossible de lire le fichier Excel.\n\nErreur: {str(e)}"
            )
            
    def _validate_columns(self, df):
        """
        Valide que toutes les colonnes requises sont présentes
        
        Args:
            df: DataFrame pandas
            
        Returns:
            bool: True si les colonnes sont valides
        """
        missing_columns = []
        df_columns = [col.strip() for col in df.columns]
        
        for required_col in self.required_columns:
            if required_col not in df_columns:
                missing_columns.append(required_col)
                
        if missing_columns:
            error_msg = (
                f"Colonnes manquantes dans le fichier Excel:\n\n"
                f"• {', '.join(missing_columns)}\n\n"
                f"Colonnes attendues: {', '.join(self.required_columns)}\n"
                f"Colonnes trouvées: {', '.join(df_columns)}"
            )
            messagebox.showerror("Erreur de structure", error_msg)
            return False
            
        return True
        
    def _process_student_data(self, df):
        """
        Traite et valide les données des élèves
        
        Args:
            df: DataFrame pandas
            
        Returns:
            list: Liste des élèves valides
        """
        students = []
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Nettoyer et valider les données
                nom = str(row['Nom']).strip() if pd.notna(row['Nom']) else ""
                prenom = str(row['Prénom']).strip() if pd.notna(row['Prénom']) else ""
                classe = str(row['Classe']).strip() if pd.notna(row['Classe']) else ""
                email = str(row['Email']).strip() if pd.notna(row['Email']) else ""
                
                # Vérifications de base
                if not nom or not prenom:
                    errors.append(f"Ligne {index + 2}: Nom ou prénom manquant")
                    continue
                    
                if not classe:
                    errors.append(f"Ligne {index + 2}: Classe manquante")
                    continue
                    
                # Validation email basique
                if email and '@' not in email:
                    errors.append(f"Ligne {index + 2}: Email invalide ({email})")
                    continue
                    
                # Créer l'objet élève
                student = {
                    'id': len(students) + 1,  # ID auto-incrémenté
                    'nom': nom,
                    'prenom': prenom,
                    'classe': classe,
                    'email': email,
                    'source': 'excel'  # Marqueur pour identifier la source
                }
                
                students.append(student)
                
            except Exception as e:
                errors.append(f"Ligne {index + 2}: Erreur de traitement ({str(e)})")
                
        # Afficher les erreurs s'il y en a
        if errors:
            error_msg = f"Erreurs détectées:\n\n" + "\n".join(errors[:10])
            if len(errors) > 10:
                error_msg += f"\n... et {len(errors) - 10} autres erreurs"
                
            messagebox.showwarning("Avertissements", error_msg)
            
        if not students:
            messagebox.showerror("Erreur", "Aucune donnée valide trouvée dans le fichier.")
            return []
            
        return students
        
    def get_students_data(self):
        """
        Retourne les données des élèves (Excel si chargé, sinon None)
        
        Returns:
            tuple: (students_list, is_excel_data)
        """
        if self.excel_data_loaded and self.imported_students:
            return self.imported_students, True
        else:
            return None, False
            
    def reset_to_json_data(self):
        """Remet les données JSON par défaut"""
        self.imported_students = []
        self.excel_data_loaded = False
        log_info("Retour aux données JSON par défaut")