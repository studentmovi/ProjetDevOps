import pandas as pd
import os
from typing import Dict, List, Tuple, Optional

class ExcelValidator:
    """Utilitaire pour valider et traiter les fichiers Excel d'import d'élèves"""
    
    # Structure attendue du fichier
    EXPECTED_COLUMNS = ["Nom", "Prénom", "Classe", "Email"]
    EXPECTED_FILENAME = "eleves.xlsx"
    
    def __init__(self):
        self.errors = []
    
    def validate_file_structure(self, file_path: str) -> Tuple[bool, List[str]]:
        """
        Valide la structure du fichier Excel
        
        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_errors)
        """
        self.errors = []
        
        try:
            # Vérifier l'extension
            if not file_path.lower().endswith('.xlsx'):
                self.errors.append("❌ Le fichier doit avoir l'extension .xlsx")
            
            # Vérifier le nom du fichier (optionnel mais recommandé)
            filename = os.path.basename(file_path)
            if filename.lower() != self.EXPECTED_FILENAME.lower():
                self.errors.append(f"⚠️ Le fichier devrait être nommé '{self.EXPECTED_FILENAME}' (recommandé)")
            
            # Lire le fichier Excel
            try:
                # Vérifier qu'il n'y a qu'une seule feuille ou utiliser la première
                xl_file = pd.ExcelFile(file_path)
                
                if len(xl_file.sheet_names) > 1:
                    self.errors.append(f"⚠️ Le fichier contient {len(xl_file.sheet_names)} feuilles. Seule la première sera utilisée.")
                
                # Lire la première feuille
                df = pd.read_excel(file_path, sheet_name=0)
                
            except Exception as e:
                self.errors.append(f"❌ Impossible de lire le fichier Excel: {str(e)}")
                return False, self.errors
            
            # Vérifier que le fichier n'est pas vide
            if df.empty:
                self.errors.append("❌ Le fichier Excel est vide")
                return False, self.errors
            
            # Vérifier les colonnes requises
            missing_columns = []
            df_columns = [col.strip() for col in df.columns]  # Nettoyer les espaces
            
            for expected_col in self.EXPECTED_COLUMNS:
                if expected_col not in df_columns:
                    missing_columns.append(expected_col)
            
            if missing_columns:
                self.errors.append(f"❌ Colonnes manquantes: {', '.join(missing_columns)}")
            
            # Vérifier les colonnes supplémentaires
            extra_columns = [col for col in df_columns if col not in self.EXPECTED_COLUMNS]
            if extra_columns:
                self.errors.append(f"⚠️ Colonnes supplémentaires ignorées: {', '.join(extra_columns)}")
            
            # Vérifier que les données ne sont pas vides
            if len(df) == 0:
                self.errors.append("❌ Aucun élève trouvé dans le fichier")
            
            # Validation des données
            self._validate_data_content(df)
            
            # Retourner le résultat
            has_critical_errors = any("❌" in error for error in self.errors)
            return not has_critical_errors, self.errors
            
        except Exception as e:
            self.errors.append(f"❌ Erreur inattendue lors de la validation: {str(e)}")
            return False, self.errors
    
    def _validate_data_content(self, df: pd.DataFrame) -> None:
        """Valide le contenu des données"""
        try:
            # Vérifier les champs obligatoires
            required_fields = ["Nom", "Prénom", "Classe"]
            
            for field in required_fields:
                if field in df.columns:
                    # Compter les valeurs nulles/vides
                    null_count = df[field].isna().sum()
                    empty_count = (df[field].astype(str).str.strip() == '').sum()
                    total_empty = null_count + empty_count
                    
                    if total_empty > 0:
                        self.errors.append(f"⚠️ {total_empty} ligne(s) avec '{field}' vide")
            
            # Validation spécifique des emails
            if "Email" in df.columns:
                invalid_emails = 0
                for email in df["Email"].dropna():
                    email_str = str(email).strip()
                    if email_str and "@" not in email_str:
                        invalid_emails += 1
                
                if invalid_emails > 0:
                    self.errors.append(f"⚠️ {invalid_emails} email(s) avec format invalide")
            
            # Vérifier les doublons
            if "Nom" in df.columns and "Prénom" in df.columns:
                duplicates = df[df.duplicated(subset=["Nom", "Prénom"], keep=False)]
                if len(duplicates) > 0:
                    self.errors.append(f"⚠️ {len(duplicates)} élève(s) en double détecté(s)")
                    
        except Exception as e:
            self.errors.append(f"⚠️ Erreur lors de la validation des données: {str(e)}")
    
    def load_students_data(self, file_path: str) -> Optional[List[Dict]]:
        """
        Charge les données d'élèves depuis le fichier Excel validé
        
        Returns:
            Optional[List[Dict]]: Liste des élèves ou None si erreur
        """
        try:
            # Lire le fichier
            df = pd.read_excel(file_path, sheet_name=0)
            
            # Nettoyer les noms de colonnes
            df.columns = [col.strip() for col in df.columns]
            
            # Convertir en liste de dictionnaires
            students_list = []
            
            for index, row in df.iterrows():
                # Nettoyer les données
                nom = str(row.get("Nom", "")).strip()
                prenom = str(row.get("Prénom", "")).strip()
                classe = str(row.get("Classe", "")).strip()
                email = str(row.get("Email", "")).strip()
                
                # Ignorer les lignes complètement vides
                if not nom and not prenom and not classe:
                    continue
                
                # Générer un ID unique
                student_id = f"STU_{len(students_list) + 1:04d}"
                
                # Extraire l'année de la classe (1A -> 1, 2B -> 2, etc.)
                annee = 1  # Valeur par défaut
                if classe and classe[0].isdigit():
                    annee = int(classe[0])
                
                student_data = {
                    "id": student_id,
                    "nom": nom,
                    "prenom": prenom,
                    "classe": classe,
                    "annee": annee,
                    "email": email if email != "nan" else ""
                }
                
                students_list.append(student_data)
            
            return students_list
            
        except Exception as e:
            print(f"Erreur lors du chargement des données: {e}")
            return None
    
    def get_file_info(self, file_path: str) -> Dict[str, any]:
        """Récupère les informations sur le fichier"""
        try:
            df = pd.read_excel(file_path, sheet_name=0)
            
            return {
                "filename": os.path.basename(file_path),
                "total_rows": len(df),
                "columns": list(df.columns),
                "file_size": f"{os.path.getsize(file_path) / 1024:.1f} KB"
            }
        except:
            return {"filename": os.path.basename(file_path), "error": "Impossible de lire le fichier"}