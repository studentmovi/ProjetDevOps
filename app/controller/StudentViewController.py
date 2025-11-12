import tkinter as tk
import tkinter.messagebox
from data.sample_data import (
    get_students_data_source, get_classes_data_source, get_years_data_source,
    get_available_years, get_available_classes, get_classes_by_year
)
from data.event_data_manager import event_manager
from popups.AssignEventPopup import AssignEventPopup
from popups.CostCalculatorPopup import CostCalculatorPopup

class StudentViewController:
    """Contrôleur principal pour la gestion de la vue des élèves"""
    
    def __init__(self, view):
        self.view = view
        self.students_data = get_students_data_source()
        self.filtered_students = self.students_data.copy()
        self.selected_students = []
        self.event_manager = event_manager
    
    # ====================== GESTION DES DONNÉES ======================
    def get_students_data(self):
        return self.students_data
    
    def get_filtered_students(self):
        return self.filtered_students
    
    def get_selected_students(self):
        return self.selected_students
    
    def refresh_data(self):
        """Actualise les données"""
        self.students_data = get_students_data_source()
        self.apply_all_filters()
        tkinter.messagebox.showinfo("Actualisation", "Données actualisées")
    
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
        try:
            selected_year = self.view.year_combo.get() if hasattr(self.view, 'year_combo') else "Toutes"
            selected_class = self.view.class_combo.get() if hasattr(self.view, 'class_combo') else "Toutes" 
            selected_event = self.view.event_combo.get() if hasattr(self.view, 'event_combo') else "Aucun"
            sort_type = self.view.sort_combo.get() if hasattr(self.view, 'sort_combo') else "Nom A-Z"
            
            # Pour la recherche
            search_text = ""
            if hasattr(self.view, 'search_entry') and hasattr(self.view, 'search_var'):
                search_value = self.view.search_var.get()
                if search_value and search_value not in ["", "Nom, prénom..."]:
                    search_text = search_value.lower()
        except Exception as e:
            selected_year = "Toutes"
            selected_class = "Toutes"
            selected_event = "Aucun"
            sort_type = "Nom A-Z"
            search_text = ""
        
        # Filtrage
        self.filtered_students = []
        
        for student in self.students_data:
            # Filtre par année
            if selected_year != "Toutes":
                student_year = str(student["annee"])
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
        
        # Tri
        if sort_type == "Nom A-Z":
            self.filtered_students.sort(key=lambda x: x["nom"].lower())
        elif sort_type == "Nom Z-A":
            self.filtered_students.sort(key=lambda x: x["nom"].lower(), reverse=True)
        elif sort_type == "Classe":
            self.filtered_students.sort(key=lambda x: (int(x["annee"]), x["classe"]))
        elif sort_type == "Année":
            self.filtered_students.sort(key=lambda x: int(x["annee"]))
        
        # Mettre à jour l'affichage
        self.view.update_display()
    
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
        except:
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
        except:
            self.apply_all_filters()
    
    def auto_select_students_by_classes(self, classes):
        if not classes:
            return
            
        self.selected_students = []
        for student in self.students_data:
            if student["classe"] in classes:
                self.selected_students.append(student["id"])
    
    def reset_filters(self):
        """Reset de tous les filtres"""
        try:
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
            
            self.filtered_students = self.students_data.copy()
            self.selected_students = []
            self.view.update_display()
        except:
            pass
    
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
        
        popup = AssignEventPopup(self.view.frame, self.selected_students, 
                               self.students_data, self.event_manager)
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
        student = next((s for s in self.students_data if s["id"] == student_id), None)
        if student:
            info = f"Élève: {student['prenom']} {student['nom']}\n"
            info += f"Classe: {student['classe']}\n"
            info += f"Année: {student['annee']}ème\n"
            info += f"Événements: {self.get_student_events(student)}"
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
        
        tkinter.messagebox.showinfo("Export", f"Export de {len(self.filtered_students)} élèves (fonctionnalité à développer)")