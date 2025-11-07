from datetime import datetime, timedelta
from typing import List, Dict, Any

def get_current_month_events() -> List[Dict[str, Any]]:
    """Retourne les événements du mois en cours"""
    base_date = datetime.now()
    return [
        {
            "id": 1,
            "nom": "Visite Musée Royal de l'Armée",
            "date": base_date.replace(day=15),
            "prix": 12.50,
            "statut": "planifié",
            "participants": 25,
            "type": "musée"
        },
        {
            "id": 2,
            "nom": "Théâtre Royal de la Monnaie",
            "date": base_date.replace(day=8),
            "prix": 18.00,
            "statut": "effectué",
            "participants": 30,
            "type": "théâtre"
        },
        {
            "id": 3,
            "nom": "Château de Beloeil",
            "date": base_date.replace(day=22),
            "prix": 15.75,
            "statut": "planifié",
            "participants": 28,
            "type": "château"
        }
    ]

def get_current_week_events() -> List[Dict[str, Any]]:
    """Retourne les événements de la semaine en cours"""
    now = datetime.now()
    start_week = now - timedelta(days=now.weekday())
    
    events = get_current_month_events()
    week_events = []
    
    for event in events:
        event_date = event["date"]
        if start_week <= event_date <= start_week + timedelta(days=7):
            week_events.append(event)
    
    return week_events

def get_upcoming_trips() -> List[Dict[str, Any]]:
    """Retourne les voyages à venir"""
    base_date = datetime.now()
    return [
        {
            "id": 10,
            "nom": "Voyage à Paris - Louvre & Tour Eiffel",
            "date_debut": base_date + timedelta(days=20),
            "date_fin": base_date + timedelta(days=22),
            "prix": 285.00,
            "statut": "confirmé",
            "participants": 45,
            "type": "voyage"
        },
        {
            "id": 11,
            "nom": "Séjour Londres - British Museum",
            "date_debut": base_date + timedelta(days=45),
            "date_fin": base_date + timedelta(days=48),
            "prix": 420.00,
            "statut": "en_preparation",
            "participants": 38,
            "type": "voyage"
        }
    ]

def get_all_students() -> List[Dict[str, Any]]:
    """Retourne tous les élèves (données hardcodées)"""
    return [
        # 1ère année
        {"id": 1, "nom": "Dubois", "prenom": "Alice", "annee": "1", "classe": "1A"},
        {"id": 2, "nom": "Martin", "prenom": "Pierre", "annee": "1", "classe": "1A"},
        {"id": 3, "nom": "Bernard", "prenom": "Sophie", "annee": "1", "classe": "1A"},
        {"id": 4, "nom": "Petit", "prenom": "Lucas", "annee": "1", "classe": "1B"},
        {"id": 5, "nom": "Robert", "prenom": "Emma", "annee": "1", "classe": "1B"},
        {"id": 6, "nom": "Richard", "prenom": "Hugo", "annee": "1", "classe": "1B"},
        
        # 2ème année
        {"id": 7, "nom": "Durand", "prenom": "Léa", "annee": "2", "classe": "2A"},
        {"id": 8, "nom": "Moreau", "prenom": "Thomas", "annee": "2", "classe": "2A"},
        {"id": 9, "nom": "Laurent", "prenom": "Camille", "annee": "2", "classe": "2A"},
        {"id": 10, "nom": "Simon", "prenom": "Maxime", "annee": "2", "classe": "2B"},
        {"id": 11, "nom": "Michel", "prenom": "Clara", "annee": "2", "classe": "2B"},
        {"id": 12, "nom": "Leroy", "prenom": "Nathan", "annee": "2", "classe": "2B"},
        
        # 3ème année
        {"id": 13, "nom": "Roux", "prenom": "Inès", "annee": "3", "classe": "3A"},
        {"id": 14, "nom": "David", "prenom": "Antoine", "annee": "3", "classe": "3A"},
        {"id": 15, "nom": "Bertrand", "prenom": "Sarah", "annee": "3", "classe": "3A"},
        {"id": 16, "nom": "Morel", "prenom": "Julien", "annee": "3", "classe": "3B"},
        {"id": 17, "nom": "Fournier", "prenom": "Manon", "annee": "3", "classe": "3B"},
        
        # 4ème année
        {"id": 18, "nom": "Girard", "prenom": "Louis", "annee": "4", "classe": "4A"},
        {"id": 19, "nom": "Bonnet", "prenom": "Zoé", "annee": "4", "classe": "4A"},
        {"id": 20, "nom": "Dupont", "prenom": "Gabriel", "annee": "4", "classe": "4A"},
        {"id": 21, "nom": "Lambert", "prenom": "Chloé", "annee": "4", "classe": "4B"},
        {"id": 22, "nom": "Fontaine", "prenom": "Adam", "annee": "4", "classe": "4B"},
        
        # 5ème année
        {"id": 23, "nom": "Rousseau", "prenom": "Jade", "annee": "5", "classe": "5A"},
        {"id": 24, "nom": "Vincent", "prenom": "Ethan", "annee": "5", "classe": "5A"},
        {"id": 25, "nom": "Muller", "prenom": "Lola", "annee": "5", "classe": "5A"},
        {"id": 26, "nom": "Lefevre", "prenom": "Noah", "annee": "5", "classe": "5B"},
        
        # 6ème année (Rhéto)
        {"id": 27, "nom": "Garnier", "prenom": "Eva", "annee": "6", "classe": "6A"},
        {"id": 28, "nom": "Chevalier", "prenom": "Théo", "annee": "6", "classe": "6A"},
        {"id": 29, "nom": "François", "prenom": "Lily", "annee": "6", "classe": "6B"},
        {"id": 30, "nom": "Blanc", "prenom": "Mathis", "annee": "6", "classe": "6B"},
        {"id": 31, "nom": "Guerin", "prenom": "Alice", "annee": "6", "classe": "6B"},
        {"id": 32, "nom": "Boyer", "prenom": "Ryan", "annee": "6", "classe": "6B"},
    ]

def get_available_years() -> List[str]:
    """Retourne les années disponibles"""
    return ["1", "2", "3", "4", "5", "6"]

def get_available_classes() -> List[str]:
    """Retourne toutes les classes disponibles"""
    students = get_all_students()
    classes = sorted(list(set(student["classe"] for student in students)))
    return classes

def get_classes_by_year(year: str) -> List[str]:
    """Retourne les classes pour une année donnée"""
    students = get_all_students()
    classes = sorted(list(set(student["classe"] for student in students if student["annee"] == year)))
    return classes