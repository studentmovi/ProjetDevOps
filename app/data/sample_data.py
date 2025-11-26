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
    """Retourne tous les élèves (données hardcodées pour test - à remplacer par DB)"""
    return [
        # 1ère année - Toutes les classes
        {"id": 1, "nom": "Dubois", "prenom": "Alice", "annee": "1", "classe": "1A","option": "Sciences"},
        {"id": 2, "nom": "Martin", "prenom": "Pierre", "annee": "1", "classe": "1A"},
        {"id": 3, "nom": "Bernard", "prenom": "Sophie", "annee": "1", "classe": "1A"},
        {"id": 4, "nom": "Petit", "prenom": "Lucas", "annee": "1", "classe": "1B"},
        {"id": 5, "nom": "Robert", "prenom": "Emma", "annee": "1", "classe": "1B"},
        {"id": 6, "nom": "Richard", "prenom": "Hugo", "annee": "1", "classe": "1B"},
        {"id": 7, "nom": "Garcia", "prenom": "Maria", "annee": "1", "classe": "1C"},
        {"id": 8, "nom": "Lopez", "prenom": "Diego", "annee": "1", "classe": "1C"},
        
        # 2ème année - Toutes les classes
        {"id": 9, "nom": "Durand", "prenom": "Léa", "annee": "2", "classe": "2A"},
        {"id": 10, "nom": "Moreau", "prenom": "Thomas", "annee": "2", "classe": "2A"},
        {"id": 11, "nom": "Laurent", "prenom": "Camille", "annee": "2", "classe": "2A"},
        {"id": 12, "nom": "Simon", "prenom": "Maxime", "annee": "2", "classe": "2B"},
        {"id": 13, "nom": "Michel", "prenom": "Clara", "annee": "2", "classe": "2B"},
        {"id": 14, "nom": "Leroy", "prenom": "Nathan", "annee": "2", "classe": "2B"},
        {"id": 15, "nom": "Andre", "prenom": "Julie", "annee": "2", "classe": "2C"},
        {"id": 16, "nom": "Roche", "prenom": "Alex", "annee": "2", "classe": "2C"},
        
        # 3ème année - Toutes les classes
        {"id": 17, "nom": "Roux", "prenom": "Inès", "annee": "3", "classe": "3A"},
        {"id": 18, "nom": "David", "prenom": "Antoine", "annee": "3", "classe": "3A"},
        {"id": 19, "nom": "Bertrand", "prenom": "Sarah", "annee": "3", "classe": "3A"},
        {"id": 20, "nom": "Morel", "prenom": "Julien", "annee": "3", "classe": "3B"},
        {"id": 21, "nom": "Fournier", "prenom": "Manon", "annee": "3", "classe": "3B"},
        {"id": 22, "nom": "Joly", "prenom": "Kevin", "annee": "3", "classe": "3B"},
        {"id": 23, "nom": "Meunier", "prenom": "Elise", "annee": "3", "classe": "3C"},
        {"id": 24, "nom": "Brun", "prenom": "Florian", "annee": "3", "classe": "3C"},
        
        # 4ème année - Toutes les classes
        {"id": 25, "nom": "Girard", "prenom": "Louis", "annee": "4", "classe": "4A"},
        {"id": 26, "nom": "Bonnet", "prenom": "Zoé", "annee": "4", "classe": "4A"},
        {"id": 27, "nom": "Dupont", "prenom": "Gabriel", "annee": "4", "classe": "4A"},
        {"id": 28, "nom": "Lambert", "prenom": "Chloé", "annee": "4", "classe": "4B"},
        {"id": 29, "nom": "Fontaine", "prenom": "Adam", "annee": "4", "classe": "4B"},
        {"id": 30, "nom": "Roy", "prenom": "Océane", "annee": "4", "classe": "4B"},
        {"id": 31, "nom": "Noel", "prenom": "Bastien", "annee": "4", "classe": "4C"},
        {"id": 32, "nom": "Meyer", "prenom": "Anaïs", "annee": "4", "classe": "4C"},
        
        # 5ème année - Toutes les classes
        {"id": 33, "nom": "Rousseau", "prenom": "Jade", "annee": "5", "classe": "5A"},
        {"id": 34, "nom": "Vincent", "prenom": "Ethan", "annee": "5", "classe": "5A"},
        {"id": 35, "nom": "Muller", "prenom": "Lola", "annee": "5", "classe": "5A"},
        {"id": 36, "nom": "Lefevre", "prenom": "Noah", "annee": "5", "classe": "5B"},
        {"id": 37, "nom": "Perrin", "prenom": "Lily", "annee": "5", "classe": "5B"},
        {"id": 38, "nom": "Colin", "prenom": "Ryan", "annee": "5", "classe": "5B"},
        {"id": 39, "nom": "Vidal", "prenom": "Mia", "annee": "5", "classe": "5C"},
        {"id": 40, "nom": "Caron", "prenom": "Owen", "annee": "5", "classe": "5C"},
        
        # 6ème année (Rhéto) - Toutes les classes
        {"id": 41, "nom": "Garnier", "prenom": "Eva", "annee": "6", "classe": "6A"},
        {"id": 42, "nom": "Chevalier", "prenom": "Théo", "annee": "6", "classe": "6A"},
        {"id": 43, "nom": "François", "prenom": "Lily", "annee": "6", "classe": "6B"},
        {"id": 44, "nom": "Blanc", "prenom": "Mathis", "annee": "6", "classe": "6B"},
        {"id": 45, "nom": "Guerin", "prenom": "Alice", "annee": "6", "classe": "6B"},
        {"id": 46, "nom": "Boyer", "prenom": "Ryan", "annee": "6", "classe": "6B"},
        {"id": 47, "nom": "Henry", "prenom": "Léna", "annee": "6", "classe": "6C"},
        {"id": 48, "nom": "Barbier", "prenom": "Tom", "annee": "6", "classe": "6C"},
    ]

def get_available_years() -> List[str]:
    """Retourne les années disponibles"""
    return ["1", "2", "3", "4", "5", "6"]

def get_available_classes() -> List[str]:
    """Retourne TOUTES les classes possibles (même si pas d'élèves actuellement)"""
    # ✅ TOUTES les classes pour chaque année - prêt pour DB
    all_possible_classes = [
        "1A", "1B", "1C",
        "2A", "2B", "2C", 
        "3A", "3B", "3C",
        "4A", "4B", "4C",
        "5A", "5B", "5C",
        "6A", "6B", "6C"
    ]
    return sorted(all_possible_classes)

def get_classes_by_year(year: str) -> List[str]:
    """Retourne TOUTES les classes pour une année donnée (même si vides)"""
    classes_mapping = {
        "1": ["1A", "1B", "1C"],
        "2": ["2A", "2B", "2C"],
        "3": ["3A", "3B", "3C"],
        "4": ["4A", "4B", "4C"],
        "5": ["5A", "5B", "5C"],
        "6": ["6A", "6B", "6C"]
    }
    return classes_mapping.get(year, [])

# ====================== PRÉPARATION POUR BASE DE DONNÉES ======================

class StudentDatabase:
    """Classe pour préparer l'intégration future avec une base de données"""
    
    @staticmethod
    def get_students_from_db():
        """
        Méthode future pour récupérer les élèves depuis la DB
        TODO: Remplacer par une vraie connexion DB
        """
        # Actuellement utilise les données hardcodées
        return get_all_students()
    
    @staticmethod
    def get_classes_from_db():
        """
        Méthode future pour récupérer les classes depuis la DB
        TODO: Remplacer par SELECT DISTINCT classe FROM students
        """
        return get_available_classes()
    
    @staticmethod
    def get_years_from_db():
        """
        Méthode future pour récupérer les années depuis la DB  
        TODO: Remplacer par SELECT DISTINCT annee FROM students
        """
        return get_available_years()

# Fonction de transition pour faciliter le passage vers DB
def get_students_data_source():
    """
    Point d'entrée unique pour les données d'élèves
    À modifier quand on passera à la DB
    """
    # Pour l'instant: données hardcodées
    return StudentDatabase.get_students_from_db()
    
    # Plus tard avec DB:
    # return fetch_students_from_database()

def get_classes_data_source():
    """Point d'entrée unique pour les données de classes"""
    return StudentDatabase.get_classes_from_db()

def get_years_data_source():
    """Point d'entrée unique pour les données d'années"""
    return StudentDatabase.get_years_from_db()