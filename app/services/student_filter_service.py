from datetime import datetime


class StudentFilterService:

    @staticmethod
    def filter_students(students, filters, event_manager):
        result = students

        result = StudentFilterService._filter_year(result, filters)
        result = StudentFilterService._filter_class(result, filters)
        result = StudentFilterService._filter_event(result, filters, event_manager)
        result = StudentFilterService._filter_month(result, filters, event_manager)
        result = StudentFilterService._filter_search(result, filters)

        return StudentFilterService._sort(result, filters, event_manager)

    @staticmethod
    def _filter_year(students, filters):
        if filters["year"] == "Toutes":
            return students

        year = filters["year"].replace("ère", "").replace("ème", "").replace("e", "")
        return [s for s in students if str(s.get("annee")) == year]

    @staticmethod
    def _filter_class(students, filters):
        if filters["class"] == "Toutes":
            return students
        return [s for s in students if s.get("classe") == filters["class"]]

    @staticmethod
    def _filter_event(students, filters, event_manager):
        if filters["event"] == "Tous":
            return students

        filtered = []
        for s in students:
            events = event_manager.get_student_events(s["id"])
            for eid in events:
                ev = event_manager.get_event(eid)
                if ev and ev.get("nom") == filters["event"]:
                    filtered.append(s)
                    break
        return filtered

    @staticmethod
    def _filter_month(students, filters, event_manager):
        if filters["month"] == "Tous":
            return students

        filtered = []
        for s in students:
            for eid in event_manager.get_student_events(s["id"]):
                ev = event_manager.get_event(eid)
                if ev and ev.get("date"):
                    try:
                        d = datetime.strptime(ev["date"], "%Y-%m-%d")
                        if d.strftime("%B %Y") == filters["month"]:
                            filtered.append(s)
                            break
                    except Exception:
                        continue
        return filtered

    @staticmethod
    def _filter_search(students, filters):
        if not filters["search"]:
            return students

        text = filters["search"].lower()
        return [
            s for s in students
            if text in s.get("nom", "").lower()
            or text in s.get("prenom", "").lower()
        ]

    @staticmethod
    def _sort(students, filters, event_manager):
        sort_type = filters["sort"]

        if sort_type == "Nom A-Z":
            return sorted(students, key=lambda x: x.get("nom", "").lower())
        if sort_type == "Nom Z-A":
            return sorted(students, key=lambda x: x.get("nom", "").lower(), reverse=True)
        if sort_type == "Classe":
            return sorted(students, key=lambda x: (x.get("annee", 0), x.get("classe", "")))
        if sort_type == "Année":
            return sorted(students, key=lambda x: x.get("annee", 0))

        if sort_type == "Date (Mois)":
            def next_event_date(student):
                dates = []
                for eid in event_manager.get_student_events(student["id"]):
                    ev = event_manager.get_event(eid)
                    if ev and ev.get("date"):
                        try:
                            dates.append(datetime.strptime(ev["date"], "%Y-%m-%d"))
                        except Exception:
                            pass
                return min(dates) if dates else datetime.max

            return sorted(students, key=next_event_date)

        return students
