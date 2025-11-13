import tkinter as tk
import tkinter.messagebox
import sys
import os

from data.sample_data import (
    get_students_data_source, get_classes_data_source, get_years_data_source,
    get_available_years, get_available_classes, get_classes_by_year
)
from data.event_data_manager import event_manager
from popups.AssignEventPopup import AssignEventPopup
from popups.CostCalculatorPopup import CostCalculatorPopup
from controller.ExeclImportController import ExcelImportController
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class StudentViewController:
    """Contrôleur principal pour la gestion de la vue des élèves"""
    
    def __init__(self, view):
        self.view = view
        self.students_data = get_students_data_source()
        self.filtered_students = []
        self.selected_students = []
        self.event_manager = event_manager
        
        # Ajout du contrôleur Excel avec gestion des données
        self.excel_controller = ExcelImportController(self.view.frame)
        self._use_excel_data = False
        
        print(f"StudentViewController initialisé avec {len(self.students_data)} élèves")
    
    # ====================== GESTION DES DONNÉES ======================
    def get_students_data(self):
        """
        Retourne les données des élèves (Excel si disponible, sinon JSON)
        
        Returns:
            list: Liste des élèves
        """
        # Vérifier d'abord si des données Excel sont disponibles
        excel_students, is_excel = self.excel_controller.get_students_data()
        
        if is_excel and excel_students:
            self._use_excel_data = True
            return excel_students
        else:
            self._use_excel_data = False
            # Retourner les données JSON par défaut
            return self.students_data
    
    def get_filtered_students(self):
        return self.filtered_students
    
    def get_selected_students(self):
        return self.selected_students
    
    def load_all_students_on_startup(self):
        """Charge tous les élèves au démarrage de l'application"""
        try:
            print("Début du chargement initial des élèves...")
            
            # Obtenir les données actuelles (Excel ou JSON)
            current_data = self.get_students_data()
            print(f"Données récupérées: {len(current_data)} élèves")
            
            # Initialiser avec tous les élèves
            self.filtered_students = current_data.copy()
            self.selected_students = []
            
            print(f"Filtered_students initialisé avec: {len(self.filtered_students)} élèves")
            
            # Mettre à jour l'affichage
            if hasattr(self.view, 'update_display'):
                self.view.update_display()
                print("update_display() appelé avec succès")
            else:
                print("ERREUR: view.update_display() non trouvé")
            
            print(f"Chargement initial terminé: {len(current_data)} élèves affichés")
            
        except Exception as e:
            print(f"Erreur lors du chargement initial: {e}")
            import traceback
            traceback.print_exc()
            
            # En cas d'erreur, essayer un chargement basique
            try:
                self.students_data = get_students_data_source()
                self.filtered_students = self.students_data.copy()
                self.selected_students = []
                print(f"Chargement de secours: {len(self.students_data)} élèves")
                
                if hasattr(self.view, 'update_display'):
                    self.view.update_display()
            except Exception as e2:
                print(f"Erreur dans le chargement de secours: {e2}")
    
    def refresh_data(self):
        """Actualise les données"""
        if self._use_excel_data:
            # Si on utilise des données Excel, on garde ces données
            current_data = self.get_students_data()
            self.students_data = current_data
        else:
            # Sinon on recharge depuis les sources JSON
            self.students_data = get_students_data_source()
        
        self.apply_all_filters()
        source_text = "Excel" if self._use_excel_data else "JSON"
        tkinter.messagebox.showinfo("Actualisation", f"Données {source_text} actualisées")
    
    def import_excel_students(self):
        """Lance le processus d'import Excel"""
        # Callback pour rafraîchir après import réussi
        def on_import_success():
            # Mettre à jour les données après import
            self.students_data = self.get_students_data()
            self.apply_all_filters()
            # Notifier la vue pour qu'elle se rafraîchisse
            if hasattr(self.view, 'refresh_view'):
                self.view.refresh_view()
        
        # Passer le callback au contrôleur Excel
        self.excel_controller.on_import_success_callback = on_import_success
        self.excel_controller.start_import_process()
        
    def reset_to_json_data(self):
        """Remet les données JSON par défaut"""
        result = tkinter.messagebox.askyesno(
            "Confirmer",
            "Voulez-vous revenir aux données JSON par défaut ?\n\n"
            "Les données Excel importées seront perdues."
        )
        if result:
            self.excel_controller.reset_to_json_data()
            self._use_excel_data = False
            self.students_data = get_students_data_source()
            self.apply_all_filters()
            # Notifier la vue pour qu'elle se rafraîchisse
            if hasattr(self.view, 'refresh_view'):
                self.view.refresh_view()
            tkinter.messagebox.showinfo("Données JSON", "Retour aux données JSON par défaut")
        
    def is_using_excel_data(self):
        """
        Vérifie si des données Excel sont actuellement utilisées
        
        Returns:
            bool: True si données Excel actives
        """
        _, is_excel = self.excel_controller.get_students_data()
        return is_excel and self._use_excel_data
    
    # ====================== GESTION DES ÉVÉNEMENTS ======================
    def get_events_for_filter(self):
        """Récupère la liste des événements disponibles"""
        events = self.event_manager.get_events()
        return [f"{event['nom']} ({event['date']})" for event in events]
    
    def get_classes_for_event(self, event_name):
        """Récupère les classes concernées par un événement"""
        event_classes_mapping = {
            "Sortie Théâtre": ["1A", "1B", "2A"],
            "Visite Musée": ["3A", "3B", "3C", "4A"], 
            "Concert": ["5A", "5B", "6A", "6B"],
            "Voyage Paris": ["5A", "5B", "5C", "6A", "6B", "6C"],
        }
        
        event_key = event_name.split(" (")[0] if " (" in event_name else event_name
        return event_classes_mapping.get(event_key, [])
    
    def get_student_events(self, student):
        """Récupère les événements d'un élève"""
        student_events = self.event_manager.get_student_events(student["id"])
        if not student_events:
            return "Aucun"
        
        events = self.event_manager.get_events()
        event_names = []
        for event in events:
            if event["id"] in student_events:
                event_names.append(event["nom"])
        
        return ", ".join(event_names) if event_names else "Aucun"
    
    # ====================== GESTION DES FILTRES ======================
    def apply_all_filters(self):
        """Application de tous les filtres"""
        print("Application des filtres...")
        
        try:
            selected_year = self.view.year_combo.get() if hasattr(self.view, 'year_combo') else "Toutes"
            selected_class = self.view.class_combo.get() if hasattr(self.view, 'class_combo') else "Toutes" 
            selected_event = self.view.event_combo.get() if hasattr(self.view, 'event_combo') else "Aucun"
            sort_type = self.view.sort_combo.get() if hasattr(self.view, 'sort_combo') else "Nom A-Z"
            
            print(f"Filtres: année={selected_year}, classe={selected_class}, événement={selected_event}, tri={sort_type}")
            
            # Pour la recherche - correction du placeholder
            search_text = ""
            if hasattr(self.view, 'search_entry') and hasattr(self.view, 'search_var'):
                search_value = self.view.search_var.get()
                # Correction: utiliser le bon placeholder
                if search_value and search_value not in ["", "Rechercher par nom ou prénom..."]:
                    search_text = search_value.lower()
                    print(f"Recherche: '{search_text}'")
        except Exception as e:
            print(f"Erreur récupération filtres: {e}")
            selected_year = "Toutes"
            selected_class = "Toutes"
            selected_event = "Aucun"
            sort_type = "Nom A-Z"
            search_text = ""
        
        # Utiliser les données actuelles (Excel ou JSON)
        current_data = self.get_students_data()
        print(f"Données courantes: {len(current_data)} élèves")
        
        # Filtrage
        self.filtered_students = []
        
        for student in current_data:
            # Filtre par année - adaptation pour les données Excel
            if selected_year != "Toutes":
                # Pour les données Excel, on essaie d'extraire l'année de la classe
                if 'annee' in student:
                    student_year = str(student["annee"])
                else:
                    # Extraction de l'année depuis la classe (ex: "3A" -> "3")
                    classe = student.get("classe", "")
                    student_year = ''.join(filter(str.isdigit, classe))
                
                filter_year = selected_year.replace("ère", "").replace("ème", "").replace("e", "")
                if student_year != filter_year:
                    continue
            
            # Filtre par classe
            if selected_class != "Toutes":
                if student["classe"] != selected_class:
                    continue
            
            # Filtre par événement
            if selected_event != "Aucun":
                concerned_classes = self.get_classes_for_event(selected_event)
                if student["classe"] not in concerned_classes:
                    continue
            
            # Filtre par recherche
            if search_text:
                if (search_text not in student["nom"].lower() and 
                    search_text not in student["prenom"].lower()):
                    continue
            
            self.filtered_students.append(student)
        
        print(f"Après filtrage: {len(self.filtered_students)} élèves")
        
        # Tri
        if sort_type == "Nom A-Z":
            self.filtered_students.sort(key=lambda x: x["nom"].lower())
        elif sort_type == "Nom Z-A":
            self.filtered_students.sort(key=lambda x: x["nom"].lower(), reverse=True)
        elif sort_type == "Classe":
            # Adaptation pour les données Excel
            def get_sort_key(x):
                if 'annee' in x:
                    return (int(x["annee"]), x["classe"])
                else:
                    # Extraction de l'année depuis la classe
                    classe = x.get("classe", "")
                    year = ''.join(filter(str.isdigit, classe))
                    return (int(year) if year else 0, classe)
            
            self.filtered_students.sort(key=get_sort_key)
        elif sort_type == "Année":
            # Adaptation pour les données Excel
            def get_year_key(x):
                if 'annee' in x:
                    return int(x["annee"])
                else:
                    classe = x.get("classe", "")
                    year = ''.join(filter(str.isdigit, classe))
                    return int(year) if year else 0
            
            self.filtered_students.sort(key=get_year_key)
        
        print(f"Après tri: {len(self.filtered_students)} élèves")
        
        # Mettre à jour l'affichage
        if hasattr(self.view, 'update_display'):
            self.view.update_display()
            print("update_display() appelé")
        else:
            print("ERREUR: update_display() introuvable")
    
    def on_year_changed(self, event=None):
        """Gestion du changement d'année"""
        try:
            selected_year = self.view.year_combo.get() if hasattr(self.view, 'year_combo') else "Toutes"
            
            if selected_year == "Toutes":
                available_classes = ["Toutes"] + get_classes_data_source()
            else:
                year_number = selected_year.replace("ère", "").replace("ème", "").replace("e", "")
                available_classes = ["Toutes"] + get_classes_by_year(year_number)
            
            if hasattr(self.view, 'class_combo'):
                self.view.class_combo.configure(values=available_classes)
                self.view.class_combo.set("Toutes")
            
            self.apply_all_filters()
        except Exception as e:
            print(f"Erreur changement année: {e}")
            self.apply_all_filters()
    
    def on_filter_changed(self, event=None):
        self.apply_all_filters()
    
    def on_search_changed(self, *args):
        self.apply_all_filters()
    
    def on_sort_changed(self, event=None):
        self.apply_all_filters()
    
    def on_event_changed(self, event=None):
        try:
            selected_event = self.view.event_combo.get() if hasattr(self.view, 'event_combo') else "Aucun"
            
            if selected_event != "Aucun":
                concerned_classes = self.get_classes_for_event(selected_event)
                self.auto_select_students_by_classes(concerned_classes)
            
            self.apply_all_filters()
        except Exception as e:
            print(f"Erreur changement événement: {e}")
            self.apply_all_filters()
    
    def auto_select_students_by_classes(self, classes):
        if not classes:
            return
            
        self.selected_students = []
        current_data = self.get_students_data()
        for student in current_data:
            if student["classe"] in classes:
                self.selected_students.append(student["id"])
    
    def reset_filters(self):
        """Reset de tous les filtres"""
        try:
            print("Reset des filtres...")
            
            if hasattr(self.view, 'year_combo'):
                self.view.year_combo.set("Toutes")
            if hasattr(self.view, 'class_combo'):
                self.view.class_combo.configure(values=["Toutes"] + get_classes_data_source())
                self.view.class_combo.set("Toutes")
            if hasattr(self.view, 'event_combo'):
                self.view.event_combo.set("Aucun")
            if hasattr(self.view, 'search_var'):
                self.view.search_var.set("")
            if hasattr(self.view, 'sort_combo'):
                self.view.sort_combo.set("Nom A-Z")
            
            current_data = self.get_students_data()
            self.filtered_students = current_data.copy()
            self.selected_students = []
            
            print(f"Reset terminé: {len(self.filtered_students)} élèves")
            
            if hasattr(self.view, 'update_display'):
                self.view.update_display()
                
        except Exception as e:
            print(f"Erreur reset filtres: {e}")
    
    # ====================== GESTION DES SÉLECTIONS ======================
    def toggle_student_selection(self, student_id):
        if student_id in self.selected_students:
            self.selected_students.remove(student_id)
            return False
        else:
            self.selected_students.append(student_id)
            return True
    
    def select_all(self):
        self.selected_students = [s["id"] for s in self.filtered_students]
        self.view.update_display()
    
    def deselect_all(self):
        self.selected_students = []
        self.view.update_display()
    
    # ====================== POPUPS (délégués aux classes spécialisées) ======================
    def assign_to_event(self):
        """Ouvre le popup d'assignation d'événement"""
        if not self.selected_students:
            tkinter.messagebox.showwarning("Attention", "Aucun élève sélectionné !")
            return
        
        current_data = self.get_students_data()
        popup = AssignEventPopup(self.view.frame, self.selected_students, 
                               current_data, self.event_manager)
        popup.show()
    
    def calculate_event_cost(self):
        """Ouvre le popup de calcul des coûts"""
        if not self.selected_students:
            tkinter.messagebox.showwarning("Attention", "Aucun élève sélectionné !")
            return
        
        popup = CostCalculatorPopup(self.view.frame, self.selected_students)
        popup.show()
    
    # ====================== AUTRES ACTIONS ======================
    def view_student(self, student_id):
        """Affiche les détails d'un élève"""
        current_data = self.get_students_data()
        student = next((s for s in current_data if s["id"] == student_id), None)
        if student:
            info = f"Élève: {student['prenom']} {student['nom']}\n"
            info += f"Classe: {student['classe']}\n"
            
            # Adaptation pour les données Excel
            if 'annee' in student:
                info += f"Année: {student['annee']}ème\n"
            else:
                # Extraction de l'année depuis la classe
                classe = student.get("classe", "")
                year = ''.join(filter(str.isdigit, classe))
                if year:
                    info += f"Année: {year}ème\n"
            
            if 'email' in student and student['email']:
                info += f"Email: {student['email']}\n"
            
            info += f"Événements: {self.get_student_events(student)}\n"
            
            # Indication de la source des données
            source = "Excel" if self.is_using_excel_data() else "JSON"
            info += f"\nSource: {source}"
            
            tkinter.messagebox.showinfo("Détails de l'élève", info)
    
    def edit_student(self, student_id):
        """Modifie un élève"""
        tkinter.messagebox.showinfo("Info", f"Fonction de modification élève ID {student_id} à développer")
    
    def delete_student(self, student_id):
        """Supprime un élève"""
        result = tkinter.messagebox.askyesno("Confirmation", f"Supprimer l'élève ID {student_id} ?")
        if result:
            tkinter.messagebox.showinfo("Info", "Fonction de suppression à développer")
    
    def export_filtered_data(self):
        """Exporte les données filtrées"""
        if not self.filtered_students:
            tkinter.messagebox.showwarning("Attention", "Aucune donnée à exporter !")
            return
        
        source = "Excel" if self.is_using_excel_data() else "JSON"
        tkinter.messagebox.showinfo("Export", f"Export de {len(self.filtered_students)} élèves depuis {source} (fonctionnalité à développer)")