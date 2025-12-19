import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from data.sample_data import get_students_data_source
from data.event_data_manager import event_manager
from popups.AssignEventPopup import AssignEventPopup
from popups.CostCalculatorPopup import CostCalculatorPopup
from controller.ExeclImportController import ExcelImportController


class StudentViewController:
    """
    Contrôleur principal pour la gestion de la vue des élèves
    - orchestre les données
    - applique les filtres
    - gère les sélections
    - ouvre les popups
    """

    def __init__(self, view):
        self.view = view

        # Données
        self.students_data = []
        self.filtered_students = []
        self.selected_students = []

        # Managers
        self.event_manager = event_manager
        self.excel_controller = ExcelImportController(self.view.frame)

        self._use_excel_data = False

        print("StudentViewController initialisé")

    # =========================================================
    # DONNÉES
    # =========================================================

    def get_students_data(self):
        """Retourne les données actives (Excel si présent, sinon JSON)"""
        excel_students, is_excel = self.excel_controller.get_students_data()

        if is_excel and excel_students:
            self._use_excel_data = True
            return excel_students

        self._use_excel_data = False
        return self.students_data

    def is_using_excel_data(self):
        return self._use_excel_data

    def load_all_students_on_startup(self):
        """Chargement initial"""
        try:
            self.students_data = get_students_data_source()

            data = self.get_students_data()
            self.filtered_students = data.copy()
            self.selected_students = []

            self._refresh_view()
        except Exception as e:
            print(f"Erreur chargement initial: {e}")

    def refresh_data(self):
        """Recharge les données depuis la source active"""
        if self._use_excel_data:
            self.students_data = self.get_students_data()
        else:
            self.students_data = get_students_data_source()

        self.apply_all_filters()

        source = "Excel" if self._use_excel_data else "JSON"
        messagebox.showinfo("Actualisation", f"Données {source} actualisées")

    # =========================================================
    # IMPORT EXCEL
    # =========================================================

    def import_excel_students(self):
        """Démarre l'import Excel"""

        def on_success():
            self.refresh_data()
            self._refresh_view()

        self.excel_controller.on_import_success_callback = on_success
        self.excel_controller.start_import_process()

    # =========================================================
    # FILTRES
    # =========================================================

    def apply_all_filters(self):
        """Point d'entrée unique pour appliquer tous les filtres"""
        data = self.get_students_data()
        filters = self.view.get_filters()

        data = self._filter_by_year(data, filters)
        data = self._filter_by_class(data, filters)
        data = self._filter_by_event(data, filters)
        data = self._filter_by_month(data, filters)
        data = self._filter_by_search(data, filters)

        self.filtered_students = self._sort_students(data, filters["sort"])
        self._refresh_view()

    def _filter_by_year(self, students, filters):
        if filters["year"] == "Toutes":
            return students

        year = filters["year"].replace("ère", "").replace("ème", "").replace("e", "")
        return [s for s in students if str(s.get("annee")) == year]

    def _filter_by_class(self, students, filters):
        if filters["class"] == "Toutes":
            return students
        return [s for s in students if s.get("classe") == filters["class"]]

    def _filter_by_event(self, students, filters):
        if filters["event"] == "Tous":
            return students

        result = []
        for student in students:
            events = self.get_student_events_names_only(student)
            if filters["event"] in events:
                result.append(student)
        return result

    def _filter_by_month(self, students, filters):
        if filters["month"] == "Tous":
            return students

        result = []
        for student in students:
            for event_id in self.event_manager.get_student_events(student["id"]):
                event = self.event_manager.get_event(event_id)
                if event and event.get("date"):
                    try:
                        date_obj = datetime.strptime(event["date"], "%Y-%m-%d")
                        if date_obj.strftime("%B %Y") == filters["month"]:
                            result.append(student)
                            break
                    except Exception:
                        continue
        return result

    def _filter_by_search(self, students, filters):
        search = filters["search"]
        if not search:
            return students

        search = search.lower()
        return [
            s for s in students
            if search in s.get("nom", "").lower()
            or search in s.get("prenom", "").lower()
        ]

    def _sort_students(self, students, sort_type):
        if sort_type == "Nom A-Z":
            return sorted(students, key=lambda x: x.get("nom", "").lower())

        if sort_type == "Nom Z-A":
            return sorted(students, key=lambda x: x.get("nom", "").lower(), reverse=True)

        if sort_type == "Classe":
            return sorted(
                students,
                key=lambda x: (int(x.get("annee", 0)), x.get("classe", ""))
            )

        if sort_type == "Année":
            return sorted(students, key=lambda x: int(x.get("annee", 0)))

        if sort_type == "Date (Mois)":

            def next_event_date(student):
                dates = []
                for event_id in self.event_manager.get_student_events(student["id"]):
                    event = self.event_manager.get_event(event_id)
                    if event and event.get("date"):
                        try:
                            dates.append(datetime.strptime(event["date"], "%Y-%m-%d"))
                        except Exception:
                            pass
                return min(dates) if dates else datetime.max

            return sorted(students, key=next_event_date)

        return students

    def reset_filters(self):
        """Reset logique (la view reset l’UI)"""
        self.selected_students = []
        self.filtered_students = self.get_students_data().copy()
        self._refresh_view()

    # =========================================================
    # SÉLECTION
    # =========================================================

    def toggle_student_selection(self, student_id):
        if student_id in self.selected_students:
            self.selected_students.remove(student_id)
        else:
            self.selected_students.append(student_id)

        self._refresh_view()

    def select_all(self):
        self.selected_students = [s["id"] for s in self.filtered_students]
        self._refresh_view()

    def deselect_all(self):
        self.selected_students = []
        self._refresh_view()

    # =========================================================
    # POPUPS / ACTIONS
    # =========================================================

    def assign_to_event(self):
        if not self.selected_students:
            return False, "Aucun élève sélectionné"

        popup = AssignEventPopup(
            self.view.frame,
            self.selected_students,
            self.get_students_data(),
            self.event_manager
        )
        popup.show()
        return True, None

    def calculate_event_cost(self):
        if not self.selected_students:
            return False, "Aucun élève sélectionné"

        event_name = self.view.get_filters()["event"]
        if event_name in ["Tous", None, ""]:
            return False, "Sélectionne un événement"

        event_id = None
        for event in self.event_manager.get_events():
            if event.get("nom") == event_name:
                event_id = event.get("id")
                break

        if not event_id:
            return False, "Événement introuvable"

        popup = CostCalculatorPopup(
            self.view.frame,
            event_id,
            self.selected_students
        )
        popup.show()
        return True, None

    # =========================================================
    # DONNÉES ÉVÉNEMENTS
    # =========================================================

    def get_student_events(self, student):
        """Retourne les événements formatés pour affichage"""
        events_info = []

        for event_id in self.event_manager.get_student_events(student["id"]):
            event = self.event_manager.get_event(event_id)
            if event:
                name = event.get("nom", "")
                date = event.get("date")
                if date:
                    try:
                        d = datetime.strptime(date, "%Y-%m-%d")
                        name += f" ({d.strftime('%d/%m')})"
                    except Exception:
                        pass
                events_info.append(name)

        return events_info

    def get_student_events_names_only(self, student):
        """Retourne uniquement les noms des événements"""
        names = []
        for eid in self.event_manager.get_student_events(student["id"]):
            event = self.event_manager.get_event(eid)
            if event and event.get("nom"):
                names.append(event["nom"])
        return names

    # =========================================================
    # DETAILS ÉLÈVES
    # =========================================================

    def open_student_details(self, student_id):
        from popups.StudentDetailPopup import StudentDetailPopup

        if not isinstance(student_id, int):
            return

        student = next(
            (s for s in self.get_students_data() if s["id"] == student_id),
            None
        )

        if not student:
            messagebox.showerror("Erreur", "Élève introuvable")
            return

        def on_student_updated(updated_student):
            # Choisir la bonne source (JSON ou Excel)
            data_source = self.students_data
            if self._use_excel_data:
                data_source = self.excel_controller.get_students_data()[0]

            for i, s in enumerate(data_source):
                if s["id"] == updated_student["id"]:
                    data_source[i] = updated_student
                    break

            self.apply_all_filters()

        popup = StudentDetailPopup(
            parent=self.view.frame,
            student=student,
            on_save_callback=on_student_updated,
            styles=self.view.styles
        )
        popup.show()

    # =========================================================
    # HELPERS
    # =========================================================

    def _refresh_view(self):
        if hasattr(self.view, "update_display"):
            self.view.update_display()
