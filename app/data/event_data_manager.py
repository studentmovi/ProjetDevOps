import json
import os
from datetime import datetime
from utils.data_path_resolver import DataPathResolver

class EventDataManager:
    def __init__(self):
        resolver = DataPathResolver()
        self.data_file = resolver.get_file("events_assignments.json")
        self.events_data = self.load_data()
    
    def load_data(self):
        """Charge les données depuis le fichier JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Migration des données existantes vers le nouveau format
                    return self.migrate_data_format(data)
            except:
                return self.get_default_data()
        return self.get_default_data()
    
    def migrate_data_format(self, data):
        """Migre les anciennes données vers le nouveau format avec ventes"""
        if "events" in data:
            for event_id, event in data["events"].items():
                # Ajouter les nouveaux champs s'ils n'existent pas
                if "ventes_activees" not in event:
                    event["ventes_activees"] = False
                if "total_ventes" not in event:
                    event["total_ventes"] = 0.0
                
                # Migrer l'ancien format des participants si nécessaire
                if "participants" in event:
                    for student_id, participant_data in event["participants"].items():
                        # Ancienne structure : {"vente": 0, "prix_final": 0}
                        # Nouvelle structure : {"prix_base": 0, "prix_final": 0}
                        if "vente" in participant_data and "prix_base" not in participant_data:
                            # Supprimer l'ancien champ "vente" au niveau individuel
                            participant_data.pop("vente", None)
                        if "prix_base" not in participant_data:
                            participant_data["prix_base"] = 0.0
                        if "prix_final" not in participant_data:
                            participant_data["prix_final"] = 0.0
        
        return data
    
    def get_default_data(self):
        """Structure de données par défaut"""
        return {
            "events": {
                "sortie_theatre": {
                    "id": "sortie_theatre",
                    "nom": "Sortie Théâtre",
                    "date": "15/11/2024",
                    "cout_total": 450.0,
                    "ventes_activees": False,  # Si les ventes sont activées pour cet événement
                    "total_ventes": 0.0,       # Total des ventes pour l'événement
                    "participants": {},  # student_id: {prix_base: 0, prix_final: 0}
                    "description": "Sortie au théâtre municipal"
                },
                "visite_musee": {
                    "id": "visite_musee", 
                    "nom": "Visite Musée",
                    "date": "20/11/2024",
                    "cout_total": 320.0,
                    "ventes_activees": False,
                    "total_ventes": 0.0,
                    "participants": {},
                    "description": "Visite du musée d'histoire"
                },
                "concert": {
                    "id": "concert",
                    "nom": "Concert",
                    "date": "25/11/2024", 
                    "cout_total": 600.0,
                    "ventes_activees": False,
                    "total_ventes": 0.0,
                    "participants": {},
                    "description": "Concert de musique classique"
                }
            },
            "student_events": {}  # student_id: [event_ids]
        }
    
    def save_data(self):
        """Sauvegarde les données dans le fichier JSON"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.events_data, f, ensure_ascii=False, indent=2)
    
    def get_events(self):
        """Retourne la liste des événements"""
        return list(self.events_data["events"].values())
    
    def get_event(self, event_id):
        """Retourne un événement spécifique"""
        return self.events_data["events"].get(event_id)
    
    def assign_student_to_event(self, student_id, event_id):
        """Assigne un élève à un événement"""
        # Ajouter à la liste des événements de l'élève
        if str(student_id) not in self.events_data["student_events"]:
            self.events_data["student_events"][str(student_id)] = []
        
        if event_id not in self.events_data["student_events"][str(student_id)]:
            self.events_data["student_events"][str(student_id)].append(event_id)
        
        # Ajouter aux participants de l'événement
        if event_id in self.events_data["events"]:
            self.events_data["events"][event_id]["participants"][str(student_id)] = {
                "prix_base": 0.0,
                "prix_final": 0.0
            }
        
        self.calculate_event_prices(event_id)
        self.save_data()
    
    def remove_student_from_event(self, student_id, event_id):
        """Retire un élève d'un événement"""
        # Retirer de la liste des événements de l'élève
        if str(student_id) in self.events_data["student_events"]:
            if event_id in self.events_data["student_events"][str(student_id)]:
                self.events_data["student_events"][str(student_id)].remove(event_id)
        
        # Retirer des participants de l'événement
        if event_id in self.events_data["events"]:
            if str(student_id) in self.events_data["events"][event_id]["participants"]:
                del self.events_data["events"][event_id]["participants"][str(student_id)]
        
        self.calculate_event_prices(event_id)
        self.save_data()
    
    def toggle_event_sales(self, event_id, enabled):
        """Active/désactive les ventes pour un événement"""
        if event_id in self.events_data["events"]:
            self.events_data["events"][event_id]["ventes_activees"] = enabled
            if not enabled:
                # Si on désactive les ventes, remettre le total à 0
                self.events_data["events"][event_id]["total_ventes"] = 0.0
            self.calculate_event_prices(event_id)
            self.save_data()
    
    def update_event_sales_total(self, event_id, total_ventes):
        """Met à jour le total des ventes pour un événement"""
        if event_id in self.events_data["events"]:
            self.events_data["events"][event_id]["total_ventes"] = float(total_ventes)
            self.calculate_event_prices(event_id)
            self.save_data()
    
    def calculate_event_prices(self, event_id):
        """Calcule les prix pour tous les participants d'un événement"""
        if event_id not in self.events_data["events"]:
            return
        
        event = self.events_data["events"][event_id]
        participants = event["participants"]
        
        if not participants:
            return
        
        # Calcul du prix de base par personne (toujours le même)
        cout_total = event["cout_total"]
        nb_participants = len(participants)
        prix_base = cout_total / nb_participants
        
        # Calcul de la réduction si les ventes sont activées
        reduction_par_personne = 0.0
        # Utiliser get() pour éviter les KeyError
        if event.get("ventes_activees", False) and event.get("total_ventes", 0.0) > 0:
            reduction_par_personne = event.get("total_ventes", 0.0) / nb_participants
        
        # Mise à jour des prix pour chaque participant
        for student_id, data in participants.items():
            data["prix_base"] = prix_base
            data["prix_final"] = max(0, prix_base - reduction_par_personne)
    
    def get_student_events(self, student_id):
        """Retourne les événements d'un élève"""
        return self.events_data["student_events"].get(str(student_id), [])
    
    def get_event_participants(self, event_id):
        """Retourne les participants d'un événement"""
        if event_id in self.events_data["events"]:
            return self.events_data["events"][event_id]["participants"]
        return {}
    def create_event(self, event_data):
        event_id = event_data["id"]

        if event_id in self.events_data["events"]:
            raise ValueError("Un événement avec cet ID existe déjà")

        # Sécurisation des champs obligatoires
        event_data.setdefault("participants", {})
        event_data.setdefault("ventes_activees", False)
        event_data.setdefault("total_ventes", 0.0)
        event_data.setdefault("description", "")

        self.events_data["events"][event_id] = event_data
        self.save_data()

    def update_event(self, event_id, updated_data):
        if event_id not in self.events_data["events"]:
            raise ValueError("Événement introuvable")

        event = self.events_data["events"][event_id]

        # Champs modifiables uniquement
        allowed_fields = [
            "nom",
            "date",
            "categorie",
            "cout_total",
            "description",
            "ventes_activees"
        ]

        for field in allowed_fields:
            if field in updated_data:
                event[field] = updated_data[field]

        self.calculate_event_prices(event_id)
        self.save_data()

# Instance globale
event_manager = EventDataManager()