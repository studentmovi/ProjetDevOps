import tkinter as tk
from tkinter import ttk
from datetime import datetime
import calendar
from data.sample_data import get_current_month_events, get_current_week_events, get_upcoming_trips

class HomeView:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        
    def create_widgets(self):
        """Crée l'interface de la page d'accueil"""
        # Titre principal
        title_frame = ttk.Frame(self.frame)
        title_frame.pack(fill="x", padx=20, pady=10)
        
        title = ttk.Label(title_frame, 
                         text="Gestion Sorties Culturelles", 
                         font=("Helvetica", 16, "bold"))
        title.pack()
        
        subtitle = ttk.Label(title_frame, 
                           text="Collège Notre-Dame - Tournai", 
                           font=("Helvetica", 10, "italic"))
        subtitle.pack()
        
        # Container principal avec 3 sections
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Section 1: Mois en cours
        self.create_month_section(main_container)
        
        # Section 2: Semaine en cours  
        self.create_week_section(main_container)
        
        # Section 3: Voyages prévus
        self.create_trips_section(main_container)
        
        return self.frame
    
    def create_month_section(self, parent):
        """Section du mois en cours"""
        month_frame = ttk.LabelFrame(parent, text=f"📅 {self.get_current_month_name()}", padding=10)
        month_frame.pack(fill="x", pady=5)
        
        events = get_current_month_events()
        
        if events:
            for event in events:
                event_frame = ttk.Frame(month_frame)
                event_frame.pack(fill="x", pady=2)
                
                # Date et nom
                date_str = event["date"].strftime("%d/%m")
                status_icon = "✅" if event["statut"] == "effectué" else "📋"
                
                ttk.Label(event_frame, 
                         text=f"{status_icon} {date_str} - {event['nom']}", 
                         font=("Helvetica", 9)).pack(side="left")
                
                # Prix
                ttk.Label(event_frame, 
                         text=f"{event['prix']}€", 
                         font=("Helvetica", 9, "bold")).pack(side="right")
        else:
            ttk.Label(month_frame, text="Aucun événement ce mois-ci", 
                     font=("Helvetica", 9, "italic")).pack()
    
    def create_week_section(self, parent):
        """Section de la semaine en cours"""
        week_frame = ttk.LabelFrame(parent, text="📆 Cette semaine", padding=10)
        week_frame.pack(fill="x", pady=5)
        
        events = get_current_week_events()
        
        if events:
            for event in events:
                event_frame = ttk.Frame(week_frame)
                event_frame.pack(fill="x", pady=2)
                
                day_name = event["date"].strftime("%A %d")
                status_icon = "✅" if event["statut"] == "effectué" else "🔔"
                
                ttk.Label(event_frame, 
                         text=f"{status_icon} {day_name} - {event['nom']}", 
                         font=("Helvetica", 9)).pack(side="left")
                
                ttk.Label(event_frame, 
                         text=f"{event['participants']} élèves", 
                         font=("Helvetica", 8)).pack(side="right")
        else:
            ttk.Label(week_frame, text="Aucun événement cette semaine", 
                     font=("Helvetica", 9, "italic")).pack()
    
    def create_trips_section(self, parent):
        """Section des voyages prévus"""
        trips_frame = ttk.LabelFrame(parent, text="✈️ Voyages prévus", padding=10)
        trips_frame.pack(fill="both", expand=True, pady=5)
        
        trips = get_upcoming_trips()
        
        if trips:
            for trip in trips:
                trip_frame = ttk.Frame(trips_frame)
                trip_frame.pack(fill="x", pady=3)
                
                # Nom du voyage
                name_frame = ttk.Frame(trip_frame)
                name_frame.pack(fill="x")
                
                ttk.Label(name_frame, 
                         text=trip['nom'], 
                         font=("Helvetica", 10, "bold")).pack(side="left")
                
                status_text = "Confirmé" if trip['statut'] == 'confirmé' else "En préparation"
                ttk.Label(name_frame, 
                         text=status_text, 
                         font=("Helvetica", 8)).pack(side="right")
                
                # Détails
                details_frame = ttk.Frame(trip_frame)
                details_frame.pack(fill="x")
                
                date_range = f"{trip['date_debut'].strftime('%d/%m')} - {trip['date_fin'].strftime('%d/%m/%Y')}"
                ttk.Label(details_frame, 
                         text=f"📅 {date_range}", 
                         font=("Helvetica", 8)).pack(side="left")
                
                ttk.Label(details_frame, 
                         text=f"{trip['prix']}€ - {trip['participants']} élèves", 
                         font=("Helvetica", 8)).pack(side="right")
                
                # Séparateur
                ttk.Separator(trips_frame, orient="horizontal").pack(fill="x", pady=2)
        else:
            ttk.Label(trips_frame, text="Aucun voyage prévu", 
                     font=("Helvetica", 9, "italic")).pack()
    
    def get_current_month_name(self):
        """Retourne le nom du mois en cours en français"""
        months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                 "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        return f"{months[datetime.now().month - 1]} {datetime.now().year}"
    
    def show(self):
        """Affiche la vue"""
        self.frame.pack(fill="both", expand=True)
        
    def hide(self):
        """Cache la vue"""
        self.frame.pack_forget()