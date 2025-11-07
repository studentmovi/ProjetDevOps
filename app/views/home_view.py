import tkinter as tk
from tkinter import ttk
from datetime import datetime
from data.sample_data import get_current_month_events, get_current_week_events, get_upcoming_trips
from component.Button import ActionButton, NavButton
from component.Cards import Card, StatCard

class HomeView:
    def __init__(self, parent, styles):
        self.parent = parent
        self.styles = styles
        self.frame = ttk.Frame(parent)
        
    def create_widgets(self):
        """Crée l'interface de la page d'accueil avec composants"""
        # Titre principal
        self.create_title_section()
        
        # Section des statistiques rapides
        self.create_quick_stats_section()
        
        # Section principale avec 3 colonnes
        main_container = tk.Frame(self.frame, bg=self.styles.colors['background'])
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Créer les 3 sections en colonnes
        self.create_month_section(main_container)
        self.create_week_section(main_container)
        self.create_trips_section(main_container)
        
        # Section des actions rapides
        self.create_quick_actions_section()
        
        return self.frame
    
    def create_title_section(self):
        """Titre avec styles"""
        title_frame_config = self.styles.get_title_frame_config('primary')
        title_frame = tk.Frame(self.frame, **title_frame_config)
        title_frame.pack(fill="x", padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        title_container = tk.Frame(title_frame, bg=title_frame_config['bg'])
        title_container.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Titre principal
        title_label_config = self.styles.get_title_label_config('primary')
        title = tk.Label(title_container, 
                        text="📊 Tableau de Bord", 
                        **title_label_config)
        title.pack()
        
        # Sous-titre avec date
        subtitle_label_config = self.styles.get_subtitle_label_config('primary')
        current_date = datetime.now().strftime("%A %d %B %Y")
        subtitle = tk.Label(title_container, 
                           text=f"Vue d'ensemble • {current_date}", 
                           **subtitle_label_config)
        subtitle.pack()
    
    def create_quick_stats_section(self):
        """Section des statistiques rapides avec cartes"""
        stats_frame = tk.Frame(self.frame, bg=self.styles.colors['background'])
        stats_frame.pack(fill="x", padx=20, pady=15)
        
        # Titre de section
        section_title = tk.Label(stats_frame,
                               text="📈 Aperçu Rapide",
                               font=("Helvetica", 12, "bold"),
                               fg=self.styles.colors['text_primary'],
                               bg=self.styles.colors['background'])
        section_title.pack(anchor="w", pady=(0, 10))
        
        # Container pour les cartes statistiques
        cards_container = tk.Frame(stats_frame, bg=self.styles.colors['background'])
        cards_container.pack(fill="x")
        
        # Statistiques
        month_events = get_current_month_events()
        week_events = get_current_week_events()
        upcoming_trips = get_upcoming_trips()
        
        # Carte événements du mois
        month_card = StatCard(
            cards_container,
            "Événements ce mois",
            len(month_events),
            f"Sur {self.get_current_month_name()}",
            "📅",
            "success"
        )
        month_card.create().pack(side="left", fill="x", expand=True, padx=5)
        
        # Carte événements cette semaine
        week_card = StatCard(
            cards_container,
            "Cette semaine",
            len(week_events),
            "Événements urgents",
            "⚡",
            "warning" if len(week_events) > 0 else "info"
        )
        week_card.create().pack(side="left", fill="x", expand=True, padx=5)
        
        # Carte voyages prévus
        trips_card = StatCard(
            cards_container,
            "Voyages prévus",
            len(upcoming_trips),
            "À organiser",
            "✈️",
            "info"
        )
        trips_card.create().pack(side="left", fill="x", expand=True, padx=5)
        
        # Carte revenus estimés
        total_revenue = sum(event.get('prix', 0) * event.get('participants', 0) 
                          for event in month_events + upcoming_trips)
        revenue_card = StatCard(
            cards_container,
            "Revenus estimés",
            f"{total_revenue:.0f}€",
            "Ce mois + voyages",
            "💰",
            "success"
        )
        revenue_card.create().pack(side="left", fill="x", expand=True, padx=5)
    
    def create_month_section(self, parent):
        """Section du mois avec composant Card"""
        # Créer la carte
        month_card = Card(parent, f"🗓️ {self.get_current_month_name()}", "success", padding=15)
        card_frame = month_card.create()
        card_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        body = month_card.get_body()
        
        events = get_current_month_events()
        
        if events:
            for i, event in enumerate(events):
                # Container pour chaque événement
                event_container = tk.Frame(body, bg=self.styles.colors['white'], 
                                         relief="solid", bd=1)
                event_container.pack(fill="x", pady=3)
                
                # Header de l'événement
                event_header = tk.Frame(event_container, 
                                      bg=self.styles.colors['success'] if event["statut"] == "effectué" 
                                      else self.styles.colors['warning'])
                event_header.pack(fill="x")
                
                # Date et statut
                date_str = event["date"].strftime("%d/%m")
                status_icon = "✅" if event["statut"] == "effectué" else "📋"
                
                date_label = tk.Label(event_header,
                                    text=f"{status_icon} {date_str}",
                                    font=("Helvetica", 8, "bold"),
                                    fg="white",
                                    bg=event_header['bg'],
                                    padx=8, pady=4)
                date_label.pack(side="left")
                
                # Prix
                price_label = tk.Label(event_header,
                                     text=f"{event['prix']}€",
                                     font=("Helvetica", 8, "bold"),
                                     fg="white",
                                     bg=event_header['bg'],
                                     padx=8, pady=4)
                price_label.pack(side="right")
                
                # Corps de l'événement
                event_body = tk.Frame(event_container, bg=self.styles.colors['white'])
                event_body.pack(fill="x", padx=10, pady=8)
                
                # Nom de l'événement
                name_label = tk.Label(event_body,
                                    text=event['nom'],
                                    font=("Helvetica", 9, "bold"),
                                    fg=self.styles.colors['text_primary'],
                                    bg=self.styles.colors['white'],
                                    wraplength=200)
                name_label.pack(anchor="w")
                
                # Informations supplémentaires
                info_label = tk.Label(event_body,
                                    text=f"👥 {event['participants']} participants • 🎯 {event['type']}",
                                    font=("Helvetica", 8),
                                    fg=self.styles.colors['text_secondary'],
                                    bg=self.styles.colors['white'])
                info_label.pack(anchor="w")
        else:
            # Message si pas d'événements
            no_events_label = tk.Label(body,
                                     text="📭 Aucun événement ce mois-ci",
                                     font=("Helvetica", 10, "italic"),
                                     fg=self.styles.colors['text_secondary'],
                                     bg=self.styles.get_card_config('success')['bg'])
            no_events_label.pack(pady=20)
    
    def create_week_section(self, parent):
        """Section de la semaine avec composant Card"""
        week_card = Card(parent, "📅 Cette Semaine", "info", padding=15)
        card_frame = week_card.create()
        card_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        body = week_card.get_body()
        
        events = get_current_week_events()
        
        if events:
            for event in events:
                # Événement urgent
                urgent_container = tk.Frame(body, bg=self.styles.colors['danger'], 
                                          relief="solid", bd=2)
                urgent_container.pack(fill="x", pady=3)
                
                # Header urgent
                urgent_header = tk.Frame(urgent_container, bg=self.styles.colors['danger'])
                urgent_header.pack(fill="x")
                
                urgent_label = tk.Label(urgent_header,
                                      text="⚡ URGENT",
                                      font=("Helvetica", 8, "bold"),
                                      fg="white",
                                      bg=self.styles.colors['danger'],
                                      padx=8, pady=2)
                urgent_label.pack(side="left")
                
                day_label = tk.Label(urgent_header,
                                   text=event["date"].strftime("%A %d"),
                                   font=("Helvetica", 8, "bold"),
                                   fg="white",
                                   bg=self.styles.colors['danger'],
                                   padx=8, pady=2)
                day_label.pack(side="right")
                
                # Corps urgent
                urgent_body = tk.Frame(urgent_container, bg=self.styles.colors['white'])
                urgent_body.pack(fill="x", padx=8, pady=6)
                
                event_name = tk.Label(urgent_body,
                                    text=event['nom'],
                                    font=("Helvetica", 9, "bold"),
                                    fg=self.styles.colors['text_primary'],
                                    bg=self.styles.colors['white'],
                                    wraplength=180)
                event_name.pack(anchor="w")
                
                event_info = tk.Label(urgent_body,
                                    text=f"💰 {event['prix']}€ • 👥 {event['participants']}",
                                    font=("Helvetica", 8),
                                    fg=self.styles.colors['text_secondary'],
                                    bg=self.styles.colors['white'])
                event_info.pack(anchor="w")
                
                # Bouton action rapide
                action_btn = ActionButton(urgent_body, "Voir détails", 
                                        command=lambda e=event: self.view_event_details(e),
                                        action_type='edit')
                action_btn.create().pack(anchor="w", pady=2)
        else:
            no_urgent_label = tk.Label(body,
                                     text="😌 Aucun événement urgent",
                                     font=("Helvetica", 10, "italic"),
                                     fg=self.styles.colors['text_secondary'],
                                     bg=self.styles.get_card_config('info')['bg'])
            no_urgent_label.pack(pady=20)
    
    def create_trips_section(self, parent):
        """Section des voyages avec composant Card"""
        trips_card = Card(parent, "✈️ Voyages Prévus", "warning", padding=15)
        card_frame = trips_card.create()
        card_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        body = trips_card.get_body()
        
        trips = get_upcoming_trips()
        
        if trips:
            for trip in trips:
                # Container voyage
                trip_container = tk.Frame(body, bg=self.styles.colors['white'],
                                        relief="raised", bd=2)
                trip_container.pack(fill="x", pady=5)
                
                # Header voyage
                trip_header = tk.Frame(trip_container, bg=self.styles.colors['warning'])
                trip_header.pack(fill="x")
                
                # Nom du voyage
                trip_name = tk.Label(trip_header,
                                   text=f"✈️ {trip['nom'][:25]}...",
                                   font=("Helvetica", 9, "bold"),
                                   fg="white",
                                   bg=self.styles.colors['warning'],
                                   padx=8, pady=5)
                trip_name.pack(side="left")
                
                # Statut
                status_text = "✅" if trip['statut'] == 'confirmé' else "⏳"
                status_label = tk.Label(trip_header,
                                      text=status_text,
                                      font=("Helvetica", 10),
                                      fg="white",
                                      bg=self.styles.colors['warning'],
                                      padx=8, pady=5)
                status_label.pack(side="right")
                
                # Corps du voyage
                trip_body = tk.Frame(trip_container, bg=self.styles.colors['white'])
                trip_body.pack(fill="x", padx=10, pady=8)
                
                # Dates
                date_range = f"{trip['date_debut'].strftime('%d/%m')} - {trip['date_fin'].strftime('%d/%m')}"
                date_label = tk.Label(trip_body,
                                    text=f"📅 {date_range}",
                                    font=("Helvetica", 8, "bold"),
                                    fg=self.styles.colors['text_primary'],
                                    bg=self.styles.colors['white'])
                date_label.pack(anchor="w")
                
                # Prix et participants
                details_frame = tk.Frame(trip_body, bg=self.styles.colors['white'])
                details_frame.pack(fill="x", pady=2)
                
                price_detail = tk.Label(details_frame,
                                      text=f"💰 {trip['prix']}€",
                                      font=("Helvetica", 8),
                                      fg=self.styles.colors['text_secondary'],
                                      bg=self.styles.colors['white'])
                price_detail.pack(side="left")
                
                participants_detail = tk.Label(details_frame,
                                             text=f"👥 {trip['participants']}",
                                             font=("Helvetica", 8),
                                             fg=self.styles.colors['text_secondary'],
                                             bg=self.styles.colors['white'])
                participants_detail.pack(side="right")
                
                # Boutons d'action
                actions_frame = tk.Frame(trip_body, bg=self.styles.colors['white'])
                actions_frame.pack(fill="x", pady=5)
                
                edit_btn = ActionButton(actions_frame, "Modifier", 
                                      command=lambda t=trip: self.edit_trip(t),
                                      action_type='edit')
                edit_btn.create().pack(side="left", padx=2)
                
                if trip['statut'] != 'confirmé':
                    confirm_btn = ActionButton(actions_frame, "Confirmer", 
                                             command=lambda t=trip: self.confirm_trip(t),
                                             action_type='save')
                    confirm_btn.create().pack(side="left", padx=2)
        else:
            no_trips_label = tk.Label(body,
                                    text="🏖️ Aucun voyage prévu",
                                    font=("Helvetica", 10, "italic"),
                                    fg=self.styles.colors['text_secondary'],
                                    bg=self.styles.get_card_config('warning')['bg'])
            no_trips_label.pack(pady=20)
    
    def create_quick_actions_section(self):
        """Section des actions rapides"""
        actions_frame = tk.Frame(self.frame, bg=self.styles.colors['background'])
        actions_frame.pack(fill="x", padx=20, pady=15)
        
        # Titre de section
        section_title = tk.Label(actions_frame,
                               text="🚀 Actions Rapides",
                               font=("Helvetica", 12, "bold"),
                               fg=self.styles.colors['text_primary'],
                               bg=self.styles.colors['background'])
        section_title.pack(anchor="w", pady=(0, 10))
        
        # Container pour les boutons
        buttons_container = tk.Frame(actions_frame, bg=self.styles.colors['background'])
        buttons_container.pack(fill="x")
        
        # Boutons d'actions rapides
        ActionButton(buttons_container, "Nouvel Événement", 
                    command=self.new_event, action_type='add').create().pack(side="left", padx=5)
        
        ActionButton(buttons_container, "Nouveau Voyage", 
                    command=self.new_trip, action_type='add').create().pack(side="left", padx=5)
        
        ActionButton(buttons_container, "Gérer Élèves", 
                    command=self.manage_students, action_type='edit').create().pack(side="left", padx=5)
        
        ActionButton(buttons_container, "Exporter Rapport", 
                    command=self.export_report, action_type='export').create().pack(side="left", padx=5)
        
        ActionButton(buttons_container, "Importer Données", 
                    command=self.import_data, action_type='import').create().pack(side="left", padx=5)
        
        # Statistiques à droite
        stats_info = tk.Label(buttons_container,
                            text=f"Dernière mise à jour: {datetime.now().strftime('%H:%M')}",
                            font=("Helvetica", 8),
                            fg=self.styles.colors['text_secondary'],
                            bg=self.styles.colors['background'])
        stats_info.pack(side="right")
    
    # Méthodes des callbacks
    def view_event_details(self, event):
        tk.messagebox.showinfo("Détails", f"Événement: {event['nom']}\nDate: {event['date'].strftime('%d/%m/%Y')}")
    
    def edit_trip(self, trip):
        tk.messagebox.showinfo("Modifier", f"Modification du voyage: {trip['nom']}")
    
    def confirm_trip(self, trip):
        tk.messagebox.showinfo("Confirmer", f"Voyage '{trip['nom']}' confirmé!")
    
    def new_event(self):
        tk.messagebox.showinfo("Nouveau", "Création d'un nouvel événement")
    
    def new_trip(self):
        tk.messagebox.showinfo("Nouveau", "Création d'un nouveau voyage")
    
    def manage_students(self):
        tk.messagebox.showinfo("Gestion", "Redirection vers la gestion des élèves")
    
    def export_report(self):
        tk.messagebox.showinfo("Export", "Export du rapport en cours...")
    
    def import_data(self):
        tk.messagebox.showinfo("Import", "Import de données en cours...")
    
    def get_current_month_name(self):
        """Retourne le nom du mois en cours"""
        months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                 "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        return f"{months[datetime.now().month - 1]} {datetime.now().year}"
    
    def show(self):
        self.frame.pack(fill="both", expand=True)
        
    def hide(self):
        self.frame.pack_forget()