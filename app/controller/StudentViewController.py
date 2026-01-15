import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from data.StudentDataManager import StudentDataManager
from data.event_data_manager import event_manager

from popups.AssignEventPopup import AssignEventPopup
from popups.CostCalculatorPopup import CostCalculatorPopup
from controller.ExcelImportController import ExcelImportController

from utils.date_utils import parse_event_date


class StudentViewController:
    """
    Contrôleur principal pour la gestion des élèves
    - Source de vérité : JSON (StudentDataManager)
    - Import Excel possible
    - Filtres dynamiques (année, classe, catégorie, événement, mois)
    - Sélection d'élèves + actions (assign event, calculate cost, details)
    """

    def __init__(self, view):
        self.view = view

        self.student_manager = StudentDataManager()
        self.event_manager = event_manager  # OK pour les filtres/assign

        root = self.view.frame.winfo_toplevel()
        self.excel_controller = ExcelImportController(root)

        self.students_data = []
        self.filtered_students = []
        self.selected_students = []  # IDs int

        self._using_excel_data = False

        print("StudentViewController initialisé")

    # =========================================================
    # DONNÉES
    # =========================================================

    def load_all_students_on_startup(self):
        try:
            self.students_data = self.student_manager.get_all_students()
            self.filtered_students = self.students_data.copy()
            self.selected_students = []
            self._refresh_view()
        except Exception as e:
            print(f"Erreur chargement initial: {e}")

    def refresh_data(self):
        self.students_data = self.student_manager.get_all_students()
        self.apply_all_filters()

    def get_students_data(self):
        return self.students_data

    def is_using_excel_data(self):
        return self._using_excel_data

    # =========================================================
    # OPTIONS DE FILTRES
    # =========================================================

    def get_available_years(self):
        years = {
            str(s.get("annee"))
            for s in self.students_data
            if s.get("annee") is not None
        }
        return sorted(years, key=lambda x: int(x) if str(x).isdigit() else 999)

    def get_available_classes(self):
        return sorted({
            str(s.get("classe"))
            for s in self.students_data
            if s.get("classe")
        })

    def get_event_categories(self):
        return sorted({
            e.get("categorie")
            for e in self.event_manager.get_events()
            if e.get("categorie")
        })

    def get_events_by_category(self, category):
        if category == "Toutes":
            return sorted({
                e.get("nom")
                for e in self.event_manager.get_events()
                if e.get("nom")
            })

        return sorted({
            e.get("nom")
            for e in self.event_manager.get_events()
            if e.get("categorie") == category and e.get("nom")
        })

    def get_available_months(self):
        months = set()
        for student in self.students_data:
            for eid in self.event_manager.get_student_events(student["id"]):
                event = self.event_manager.get_event(eid)
                d = parse_event_date(event.get("date")) if event else None
                if d:
                    months.add(d.strftime("%B %Y"))
        return sorted(months)

    # =========================================================
    # IMPORT EXCEL
    # =========================================================

    def import_excel_students(self):
        def on_success():
            students, _ = self.excel_controller.get_students_data()
            if not students:
                return

            self._using_excel_data = True
            self.student_manager.students = students
            self.student_manager.save_data()

            self.students_data = self.student_manager.get_all_students()
            self._using_excel_data = False

            self.apply_all_filters()

            messagebox.showinfo(
                "Import Excel",
                "Les données Excel ont été importées et sauvegardées."
            )

        self.excel_controller.on_import_success_callback = on_success
        self.excel_controller.start_import_process()

    # =========================================================
    # FILTRES
    # =========================================================

    def apply_all_filters(self):
        data = self.students_data
        filters = self.view.get_filters()

        data = self._filter_by_year(data, filters)
        data = self._filter_by_class(data, filters)
        data = self._filter_by_event_category(data, filters)
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

    def _filter_by_event_category(self, students, filters):
        category = filters.get("event_category")
        if not category or category == "Toutes":
            return students

        result = []
        for student in students:
            for eid in self.event_manager.get_student_events(student["id"]):
                event = self.event_manager.get_event(eid)
                if event and event.get("categorie") == category:
                    result.append(student)
                    break
        return result

    def _filter_by_event(self, students, filters):
        if filters["event"] == "Tous":
            return students
        return [
            s for s in students
            if filters["event"] in self.get_student_events_names_only(s)
        ]

    def _filter_by_month(self, students, filters):
        if filters["month"] == "Tous":
            return students

        result = []
        for student in students:
            for eid in self.event_manager.get_student_events(student["id"]):
                event = self.event_manager.get_event(eid)
                d = parse_event_date(event.get("date")) if event else None
                if d and d.strftime("%B %Y") == filters["month"]:
                    result.append(student)
                    break
        return result

    def _filter_by_search(self, students, filters):
        search = (filters.get("search") or "").lower().strip()
        if not search:
            return students

        return [
            s for s in students
            if search in s.get("nom", "").lower()
            or search in s.get("prenom", "").lower()
        ]

    # =========================================================
    # TRI
    # =========================================================

    def _sort_students(self, students, sort_type):
        if sort_type == "Nom A-Z":
            return sorted(students, key=lambda x: x.get("nom", "").lower())

        if sort_type == "Nom Z-A":
            return sorted(students, key=lambda x: x.get("nom", "").lower(), reverse=True)

        if sort_type == "Classe":
            return sorted(students, key=lambda x: (int(x.get("annee", 0)), x.get("classe", "")))

        if sort_type == "Année":
            return sorted(students, key=lambda x: int(x.get("annee", 0)))

        if sort_type == "Date (Mois)":
            def next_event_date(student):
                dates = []
                for eid in self.event_manager.get_student_events(student["id"]):
                    event = self.event_manager.get_event(eid)
                    d = parse_event_date(event.get("date")) if event else None
                    if d:
                        dates.append(d)
                return min(dates) if dates else datetime.max

            return sorted(students, key=next_event_date)

        return students

    # =========================================================
    # ÉVÉNEMENTS ÉLÈVES
    # =========================================================

    def get_student_events(self, student):
        events_info = []
        for eid in self.event_manager.get_student_events(student["id"]):
            event = self.event_manager.get_event(eid)
            if event:
                name = event.get("nom", "")
                d = parse_event_date(event.get("date"))
                if d:
                    name += f" ({d.strftime('%d/%m')})"
                events_info.append(name)
        return events_info

    def get_student_events_names_only(self, student):
        names = []
        for eid in self.event_manager.get_student_events(student["id"]):
            ev = self.event_manager.get_event(eid)
            if ev and ev.get("nom"):
                names.append(ev["nom"])
        return names

    # =========================================================
    # HELPERS : nom -> id robuste
    # =========================================================

    def _resolve_event_id_by_name(self, event_name: str):
        if not event_name:
            return None

        # ✅ robuste : si jamais id absent, on prend la clé dict
        try:
            events_dict = self.event_manager.events_data.get("events", {})
            for key, ev in events_dict.items():
                if ev.get("nom") == event_name:
                    return ev.get("id") or key
        except Exception:
            pass

        # fallback
        for ev in self.event_manager.get_events():
            if ev.get("nom") == event_name:
                return ev.get("id")

        return None

    def _get_selected_event_id_from_filters(self):
        filters = self.view.get_filters()
        selected_event_name = filters.get("event", "Tous")

        if not selected_event_name or selected_event_name == "Tous":
            return None, "Choisis d'abord un événement précis (pas 'Tous')."

        event_id = self._resolve_event_id_by_name(selected_event_name)
        if not event_id:
            return None, f"Événement introuvable (nom: {selected_event_name})"

        if not self.event_manager.get_event(event_id):
            return None, f"Événement introuvable (id: {event_id})"

        return event_id, None

    # =========================================================
    # MÉTHODES APPELÉES PAR LA VUE
    # =========================================================

    def toggle_student_selection(self, student_id: int):
        try:
            sid = int(student_id)
        except ValueError:
            return

        if sid in self.selected_students:
            self.selected_students.remove(sid)
        else:
            self.selected_students.append(sid)

        self._refresh_view()

    def open_student_details(self, student_id: int):
        try:
            sid = int(student_id)
        except ValueError:
            return

        student = next((s for s in self.students_data if int(s.get("id", -1)) == sid), None)
        if not student:
            messagebox.showwarning("Élève", "Élève introuvable.")
            return

        events = self.get_student_events(student)
        txt = (
            f"Nom : {student.get('nom','')}\n"
            f"Prénom : {student.get('prenom','')}\n"
            f"Classe : {student.get('classe','')}\n"
            f"Année : {student.get('annee','')}\n\n"
            f"Événements :\n- " + ("\n- ".join(events) if events else "Aucun")
        )
        messagebox.showinfo("Détails élève", txt)

    def assign_to_event(self):
        if not self.selected_students:
            return False, "Sélectionne au moins un élève."

        try:
            popup = AssignEventPopup(
                self.view.frame.winfo_toplevel(),
                self.selected_students,
                self.students_data,
                self.event_manager
            )
        except TypeError as e:
            return False, f"AssignEventPopup: signature invalide: {e}"
        except Exception as e:
            return False, f"Erreur ouverture popup: {e}"

        if hasattr(popup, "show"):
            try:
                popup.show()
            except Exception:
                pass

        self.apply_all_filters()
        return True, None

    def calculate_event_cost(self):
        """
        ✅ FIX FINAL :
        CostCalculatorPopup(parent, event_id, selected_students)
        """
        if not self.selected_students:
            return False, "Sélectionne au moins un élève."

        event_id, error = self._get_selected_event_id_from_filters()
        if error:
            return False, error

        parent = self.view.frame.winfo_toplevel()

        try:
            popup = CostCalculatorPopup(parent, event_id, self.selected_students)
            popup.show()
        except Exception as e:
            return False, f"Erreur ouverture calculateur: {e}"

        return True, None

    # =========================================================
    # HELPER
    # =========================================================

    def _refresh_view(self):
        if hasattr(self.view, "update_display"):
            self.view.update_display()
