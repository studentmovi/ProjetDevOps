import tkinter as tk
import tkinter.messagebox
from datetime import datetime

# Import des données depuis sample_data.py
from data.sample_data import get_students_data_source, get_available_classes, get_available_years
from data.event_data_manager import event_manager
from popups.AssignEventPopup import AssignEventPopup
from popups.CostCalculatorPopup import CostCalculatorPopup
from controller.ExeclImportController import ExcelImportController


class StudentViewController:
    """Contrôleur principal pour la gestion de la vue des élèves"""

    def __init__(self, view):
        self.view = view
        self.students_data = []  # Données JSON par défaut
        self.filtered_students = []
        self.selected_students = []
        self.event_manager = event_manager

        # Contrôleur Excel avec gestion des données
        self.excel_controller = ExcelImportController(self.view.frame)
        self._use_excel_data = False

        print(f"StudentViewController initialisé")

    # ====================== GESTION DES DONNÉES ======================
    def get_students_data(self):
        """Retourne les données des élèves (Excel si disponible, sinon JSON)"""
        excel_students, is_excel = self.excel_controller.get_students_data()

        if is_excel and excel_students:
            self._use_excel_data = True
            return excel_students
        else:
            self._use_excel_data = False
            return self.students_data

    def get_filtered_students(self):
        return self.filtered_students

    def get_selected_students(self):
        return self.selected_students

    def load_all_students_on_startup(self):
        """Charge tous les élèves au démarrage de l'application"""
        try:
            print("Début du chargement initial des élèves...")

            # Charger les données JSON par défaut
            self.students_data = get_students_data_source()
            print(f"Données JSON chargées: {len(self.students_data)} élèves")

            # Obtenir les données actuelles (Excel si disponible, sinon JSON)
            current_data = self.get_students_data()
            print(f"Données actuelles: {len(current_data)} élèves")

            # Initialiser avec tous les élèves
            self.filtered_students = current_data.copy()
            self.selected_students = []

            print(f"Filtered_students initialisé avec: {len(self.filtered_students)} élèves")

            # Mettre à jour l'affichage
            if hasattr(self.view, 'update_display'):
                self.view.update_display()
                print("update_display() appelé avec succès")

            print(f"Chargement initial terminé: {len(current_data)} élèves affichés")

        except Exception as e:
            print(f"Erreur lors du chargement initial: {e}")
            import traceback
            traceback.print_exc()

    def refresh_data(self):
        """Actualise les données"""
        if self._use_excel_data:
            current_data = self.get_students_data()
            self.students_data = current_data
        else:
            self.students_data = get_students_data_source()

        self.apply_all_filters()
        source_text = "Excel" if self._use_excel_data else "JSON"
        tkinter.messagebox.showinfo("Actualisation", f"Données {source_text} actualisées")

    def import_excel_students(self):
        """Lance le processus d'import Excel"""
        def on_import_success():
            self.refresh_data()
            if hasattr(self.view, 'refresh_view'):
                self.view.refresh_view()

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
            if hasattr(self.view, 'refresh_view'):
                self.view.refresh_view()
            tkinter.messagebox.showinfo("Données JSON", "Retour aux données JSON par défaut")

    def is_using_excel_data(self):
        return self._use_excel_data

    # ====================== GESTION DES ÉVÉNEMENTS ======================
    def get_events_for_filter(self):
        """Récupère la liste des événements disponibles"""
        try:
            # ✅ get_events() retourne une LISTE (list of dicts)
            events = self.event_manager.get_events()
            return ["Tous"] + [event.get("nom", "") for event in events if event.get("nom")]
        except Exception as e:
            print(f"Erreur get_events_for_filter: {e}")
            return ["Tous", "Sortie Théâtre", "Visite Musée", "Concert", "Voyage Paris"]

    def get_months_for_filter(self):
        """Récupère la liste des mois disponibles pour le filtrage"""
        try:
            # ✅ get_events() retourne une LISTE
            events = self.event_manager.get_events()
            months = set()
            for event in events:
                if isinstance(event, dict) and 'date' in event and event['date']:
                    try:
                        # Ton JSON est en 'YYYY-MM-DD'
                        event_date = datetime.strptime(event['date'], '%Y-%m-%d')
                        month_year = event_date.strftime('%B %Y')
                        months.add(month_year)
                    except Exception:
                        continue
            return ["Tous"] + sorted(list(months))
        except Exception as e:
            print(f"Erreur récupération mois: {e}")
            current_month = datetime.now().strftime('%B %Y')
            return ["Tous", current_month]

    def get_classes_for_event(self, event_name):
        """Récupère les classes concernées par un événement"""
        return get_available_classes()

    def get_student_events(self, student):
        """Retourne les événements d'un élève avec leurs dates"""
        try:
            student_events = self.event_manager.get_student_events(student["id"])
            if student_events:
                events_info = []
                for event_id in student_events:
                    event = self.event_manager.get_event(event_id)
                    if event:
                        event_name = event.get("nom", "")
                        event_date = event.get('date', '')
                        if event_date:
                            try:
                                date_obj = datetime.strptime(event_date, '%Y-%m-%d')
                                formatted_date = date_obj.strftime('%d/%m')
                                events_info.append(f"{event_name} ({formatted_date})")
                            except Exception:
                                events_info.append(event_name)
                        else:
                            events_info.append(event_name)
                return events_info
            return []
        except Exception as e:
            print(f"Erreur récupération événements pour {student.get('id', 'N/A')}: {e}")
            return []

    def get_student_events_names_only(self, student):
        """Retourne seulement les noms des événements d'un élève"""
        try:
            student_events = self.event_manager.get_student_events(student["id"])
            if student_events:
                events_names = []
                for event_id in student_events:
                    event = self.event_manager.get_event(event_id)
                    if event and event.get("nom"):
                        events_names.append(event["nom"])
                return events_names
            return []
        except Exception as e:
            print(f"Erreur get_student_events_names_only: {e}")
            return []

    # ====================== GESTION DES FILTRES ======================
    def apply_all_filters(self):
        """Application de tous les filtres"""
        print("Application des filtres...")

        try:
            selected_year = self.view.year_combo.get() if hasattr(self.view, 'year_combo') else "Toutes"
            selected_class = self.view.class_combo.get() if hasattr(self.view, 'class_combo') else "Toutes"
            selected_event = getattr(self.view, 'event_combo', None)
            selected_event = selected_event.get() if selected_event else "Tous"
            selected_month = getattr(self.view, 'month_combo', None)
            selected_month = selected_month.get() if selected_month else "Tous"
            sort_type = self.view.sort_combo.get() if hasattr(self.view, 'sort_combo') else "Nom A-Z"

            print(f"Filtres: année={selected_year}, classe={selected_class}, événement={selected_event}, mois={selected_month}, tri={sort_type}")

            # Recherche
            search_text = ""
            if hasattr(self.view, 'search_entry') and hasattr(self.view, 'search_var'):
                search_value = self.view.search_var.get()
                if search_value and search_value not in ["", "Nom, prénom..."]:
                    search_text = search_value.lower()
                    print(f"Recherche: '{search_text}'")
        except Exception as e:
            print(f"Erreur récupération filtres: {e}")
            selected_year = "Toutes"
            selected_class = "Toutes"
            selected_event = "Tous"
            selected_month = "Tous"
            sort_type = "Nom A-Z"
            search_text = ""

        # Utiliser les données actuelles (Excel ou JSON)
        current_data = self.get_students_data()
        print(f"Données courantes: {len(current_data)} élèves")

        # Filtrage
        self.filtered_students = []

        for student in current_data:
            # Filtre par année
            if selected_year != "Toutes":
                filter_year = selected_year.replace("ère", "").replace("ème", "").replace("e", "")
                student_year = str(student.get("annee", ""))
                if student_year != filter_year:
                    continue

            # Filtre par classe
            if selected_class != "Toutes":
                if student.get("classe", "") != selected_class:
                    continue

            # Filtre par événement
            if selected_event != "Tous":
                student_events_names = self.get_student_events_names_only(student)
                # ✅ sécurité : si pas d'events, on exclut proprement sans bug
                if not student_events_names:
                    continue
                if selected_event not in student_events_names:
                    continue

            # Filtre par mois
            if selected_month != "Tous":
                student_has_event_in_month = False
                student_events = self.event_manager.get_student_events(student["id"])
                for event_id in student_events:
                    event = self.event_manager.get_event(event_id)
                    if event and 'date' in event and event['date']:
                        try:
                            event_date = datetime.strptime(event['date'], '%Y-%m-%d')
                            event_month_year = event_date.strftime('%B %Y')
                            if event_month_year == selected_month:
                                student_has_event_in_month = True
                                break
                        except Exception:
                            continue
                if not student_has_event_in_month:
                    continue

            # Filtre par recherche
            if search_text:
                if (search_text not in student.get("nom", "").lower() and
                        search_text not in student.get("prenom", "").lower()):
                    continue

            self.filtered_students.append(student)

        print(f"Après filtrage: {len(self.filtered_students)} élèves")

        # Tri
        if sort_type == "Nom A-Z":
            self.filtered_students.sort(key=lambda x: x.get("nom", "").lower())
        elif sort_type == "Nom Z-A":
            self.filtered_students.sort(key=lambda x: x.get("nom", "").lower(), reverse=True)
        elif sort_type == "Classe":
            self.filtered_students.sort(key=lambda x: (int(x.get("annee", 0)), x.get("classe", "")))
        elif sort_type == "Année":
            self.filtered_students.sort(key=lambda x: int(x.get("annee", 0)))
        elif sort_type == "Date (Mois)":
            # Tri par date du prochain événement
            def get_next_event_date(student_obj):
                events = self.event_manager.get_student_events(student_obj["id"])
                dates = []
                for event_id in events:
                    event = self.event_manager.get_event(event_id)
                    if event and 'date' in event and event['date']:
                        try:
                            date_obj = datetime.strptime(event['date'], '%Y-%m-%d')
                            dates.append(date_obj)
                        except Exception:
                            continue
                return min(dates) if dates else datetime.max

            self.filtered_students.sort(key=get_next_event_date)

        print(f"Après tri: {len(self.filtered_students)} élèves")

        # Mettre à jour l'affichage
        if hasattr(self.view, 'update_display'):
            self.view.update_display()
            print("update_display() appelé")

    def on_year_changed(self, event=None):
        """Gestion du changement d'année"""
        try:
            selected_year = self.view.year_combo.get() if hasattr(self.view, 'year_combo') else "Toutes"

            if selected_year == "Toutes":
                available_classes = ["Toutes"] + get_available_classes()
            else:
                year_number = selected_year.replace("ère", "").replace("ème", "").replace("e", "")
                all_classes = get_available_classes()
                available_classes = ["Toutes"] + [c for c in all_classes if c.startswith(year_number)]

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

    def reset_filters(self):
        """Reset de tous les filtres"""
        try:
            print("Reset des filtres...")

            if hasattr(self.view, 'year_combo'):
                self.view.year_combo.set("Toutes")
            if hasattr(self.view, 'class_combo'):
                classes = get_available_classes()
                self.view.class_combo.configure(values=["Toutes"] + classes)
                self.view.class_combo.set("Toutes")
            if hasattr(self.view, 'event_combo'):
                events = self.get_events_for_filter()
                self.view.event_combo.configure(values=events)
                self.view.event_combo.set("Tous")
            if hasattr(self.view, 'month_combo'):
                months = self.get_months_for_filter()
                self.view.month_combo.configure(values=months)
                self.view.month_combo.set("Tous")
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
        """Bascule la sélection d'un étudiant"""
        if student_id in self.selected_students:
            self.selected_students.remove(student_id)
            return False
        else:
            self.selected_students.append(student_id)
            return True

    def select_all(self):
        """Sélectionne tous les étudiants filtrés"""
        self.selected_students = [s["id"] for s in self.filtered_students]
        self.view.update_display()

    def deselect_all(self):
        """Désélectionne tous les étudiants"""
        self.selected_students = []
        self.view.update_display()

    # ====================== POPUPS ======================
    def assign_to_event(self):
        """Ouvre le popup d'assignation d'événement"""
        if not self.selected_students:
            tkinter.messagebox.showwarning("Attention", "Aucun élève sélectionné !")
            return

        current_data = self.get_students_data()
        popup = AssignEventPopup(
            self.view.frame,
            self.selected_students,
            current_data,
            self.event_manager
        )
        popup.show()

    def calculate_event_cost(self):
        """
        ✅ Version UNIQUE (pas de copier-coller triplé)
        - l'utilisateur sélectionne des élèves
        - il choisit l'événement dans la combo
        - on convertit NOM -> ID (events_data_manager retourne une LISTE)
        - on ouvre la popup
        """
        if not self.selected_students:
            tkinter.messagebox.showwarning("Attention", "Aucun élève sélectionné")
            return

        selected_event_name = self.view.event_combo.get() if hasattr(self.view, 'event_combo') else "Tous"
        if selected_event_name in ["Tous", "", None]:
            tkinter.messagebox.showwarning("Attention", "Sélectionne un événement")
            return

        # 🔑 Nom → ID (get_events() => LISTE)
        event_id = None
        try:
            for event in self.event_manager.get_events():
                if event.get("nom") == selected_event_name:
                    event_id = event.get("id")
                    break
        except Exception as e:
            tkinter.messagebox.showerror("Erreur", f"Impossible de charger les événements: {e}")
            return

        if not event_id:
            tkinter.messagebox.showerror("Erreur", "Événement introuvable")
            return

        popup = CostCalculatorPopup(
            self.view.frame,
            event_id,
            self.selected_students
        )
        popup.show()

    # ====================== AUTRES ACTIONS ======================
    def view_student(self, student_id):
        """Affiche les détails d'un élève"""
        current_data = self.get_students_data()
        student = next((s for s in current_data if s["id"] == student_id), None)

        if student:
            events_info = self.get_student_events(student)

            info = f"Nom: {student['nom']}\n"
            info += f"Prénom: {student['prenom']}\n"
            info += f"Classe: {student['classe']}\n"
            info += f"Année: {student['annee']}\n"

            if 'email' in student:
                info += f"Email: {student['email']}\n"

            if events_info:
                info += f"Événements:\n"
                for ev in events_info:
                    info += f"  • {ev}\n"
            else:
                info += "Événements: Aucun\n"

            source = "Excel" if self.is_using_excel_data() else "JSON"
            info += f"\nSource: {source}"

            tkinter.messagebox.showinfo("Détails de l'élève", info)

    def edit_student(self, student_id):
        """Modifie un élève"""
        tkinter.messagebox.showinfo("Modification", f"Édition de l'élève {student_id}\n(À développer)")

    def delete_student(self, student_id):
        """Supprime un élève"""
        result = tkinter.messagebox.askyesno("Confirmer", f"Supprimer l'élève {student_id} ?")
        if result:
            tkinter.messagebox.showinfo("Suppression", f"Élève {student_id} supprimé\n(À développer)")

    def export_filtered_data(self):
        """Exporte les données filtrées"""
        if not self.filtered_students:
            tkinter.messagebox.showwarning("Attention", "Aucune donnée à exporter !")
            return

        tkinter.messagebox.showinfo("Export", f"Export de {len(self.filtered_students)} élèves\n(À développer)")
