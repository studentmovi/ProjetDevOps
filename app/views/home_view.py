import tkinter as tk
from tkinter import ttk
from datetime import datetime
from data.sample_data import get_current_month_events, get_current_week_events, get_upcoming_trips

class HomeView:
    def __init__(self, parent, styles):
        self.parent = parent
        self.styles = styles
        self.frame = ttk.Frame(parent)
        
    def create_widgets(self):
        """Crée l'interface de la page d'accueil avec styles"""
        # Titre principal avec styles séparés
        title_frame_config = self.styles.get_title_frame_config('primary')
        title_frame = tk.Frame(self.frame, **title_frame_config)
        title_frame.pack(fill="x", padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        title_container = tk.Frame(title_frame, bg=title_frame_config['bg'])
        title_container.pack(fill="both", expand=True, padx=20, pady=15)
        
        title_label_config = self.styles.get_title_label_config('primary')
        title = tk.Label(title_container, 
                        text="📊 Tableau de Bord", 
                        **title_label_config)
        title.pack()
        
        subtitle_label_config = self.styles.get_subtitle_label_config('primary')
        subtitle = tk.Label(title_container, 
                           text="Vue d'ensemble des activités culturelles", 
                           **subtitle_label_config)
        subtitle.pack()
        
        # Container principal
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Sections avec styles
        self.create_month_section(main_container)
        self.create_week_section(main_container)
        self.create_trips_section(main_container)
        
        return self.frame
    
    def create_month_section(self, parent):
        """Section du mois en cours avec styles"""
        month_frame = ttk.LabelFrame(parent, 
                                   text=f"🗓️ {self.get_current_month_name()}", 
                                   style="Success.TLabelframe",
                                   padding=15)
        month_frame.pack(fill="x", pady=8)
        
        events = get_current_month_events()
        card_config = self.styles.get_card_config('success')
        
        if events:
            for event in events:
                event_frame = tk.Frame(month_frame, bg=card_config['bg'])
                event_frame.pack(fill="x", pady=3)
                
                # Indicateur coloré
                status_color = self.styles.colors['success'] if event["statut"] == "effectué" else self.styles.colors['warning']
                indicator = tk.Label(event_frame, 
                                   text="●", 
                                   font=("Helvetica", 12),
                                   fg=status_color,
                                   bg=card_config['bg'])
                indicator.pack(side="left", padx=(0, 5))
                
                # Date et nom
                date_str = event["date"].strftime("%d/%m")
                event_label = tk.Label(event_frame, 
                                     text=f"{date_str} - {event['nom']}", 
                                     font=("Helvetica", 9),
                                     fg=self.styles.colors['text_primary'],
                                     bg=card_config['bg'])
                event_label.pack(side="left")
                
                # Prix avec badge
                badge_config = self.styles.get_badge_config('success')
                price_frame = tk.Frame(event_frame, bg=badge_config['bg'], relief="solid", bd=1)
                price_frame.pack(side="right")
                
                price_label = tk.Label(price_frame, 
                                     text=f"{event['prix']}€", 
                                     font=("Helvetica", 9, "bold"),
                                     fg=badge_config['fg'],
                                     bg=badge_config['bg'],
                                     padx=8, pady=2)
                price_label.pack()
        else:
            tk.Label(month_frame, 
                    text="Aucun événement ce mois-ci", 
                    font=("Helvetica", 9, "italic"),
                    fg=self.styles.colors['text_secondary'],
                    bg=card_config['bg']).pack()
    
    def create_week_section(self, parent):
        """Section de la semaine avec styles"""
        week_frame = ttk.LabelFrame(parent, 
                                  text="📅 Cette semaine", 
                                  style="Info.TLabelframe",
                                  padding=15)
        week_frame.pack(fill="x", pady=8)
        
        events = get_current_week_events()
        card_config = self.styles.get_card_config('info')
        
        if events:
            for event in events:
                event_frame = tk.Frame(week_frame, bg=card_config['bg'])
                event_frame.pack(fill="x", pady=3)
                
                # Indicateur urgent
                urgent_indicator = tk.Label(event_frame, 
                                          text="⚡", 
                                          font=("Helvetica", 10),
                                          fg=self.styles.colors['danger'],
                                          bg=card_config['bg'])
                urgent_indicator.pack(side="left", padx=(0, 5))
                
                day_name = event["date"].strftime("%A %d")
                event_label = tk.Label(event_frame, 
                                     text=f"{day_name} - {event['nom']}", 
                                     font=("Helvetica", 9, "bold"),
                                     fg=self.styles.colors['text_primary'],
                                     bg=card_config['bg'])
                event_label.pack(side="left")
                
                # Badge participants
                badge_config = self.styles.get_badge_config('info')
                participants_frame = tk.Frame(event_frame, bg=badge_config['bg'], relief="solid", bd=1)
                participants_frame.pack(side="right")
                
                participants_label = tk.Label(participants_frame, 
                                            text=f"👥 {event['participants']}", 
                                            font=("Helvetica", 8),
                                            fg=badge_config['fg'],
                                            bg=badge_config['bg'],
                                            padx=6, pady=1)
                participants_label.pack()
        else:
            tk.Label(week_frame, 
                    text="Aucun événement cette semaine", 
                    font=("Helvetica", 9, "italic"),
                    fg=self.styles.colors['text_secondary'],
                    bg=card_config['bg']).pack()
    
    def create_trips_section(self, parent):
        """Section des voyages avec styles"""
        trips_frame = ttk.LabelFrame(parent, 
                                   text="✈️ Voyages prévus", 
                                   style="Warning.TLabelframe",
                                   padding=15)
        trips_frame.pack(fill="both", expand=True, pady=8)
        
        trips = get_upcoming_trips()
        card_config = self.styles.get_card_config('warning')
        
        if trips:
            for trip in trips:
                # Carte de voyage
                trip_card = tk.Frame(trips_frame, bg=card_config['bg'], relief="raised", bd=2)
                trip_card.pack(fill="x", pady=5)
                
                # Header de la carte
                header_frame = tk.Frame(trip_card, bg=card_config['header_bg'])
                header_frame.pack(fill="x")
                
                # Nom du voyage
                name_label = tk.Label(header_frame, 
                                    text=f"✈️ {trip['nom']}", 
                                    font=("Helvetica", 11, "bold"),
                                    fg=self.styles.colors['white'],
                                    bg=card_config['header_bg'],
                                    padx=10, pady=5)
                name_label.pack(side="left")
                
                # Statut
                status_text = "✅ Confirmé" if trip['statut'] == 'confirmé' else "⏳ En préparation"
                status_label = tk.Label(header_frame, 
                                      text=status_text, 
                                      font=("Helvetica", 8),
                                      fg=self.styles.colors['white'],
                                      bg=card_config['header_bg'],
                                      padx=10, pady=5)
                status_label.pack(side="right")
                
                # Détails
                details_frame = tk.Frame(trip_card, bg=card_config['bg'])
                details_frame.pack(fill="x", padx=10, pady=8)
                
                date_range = f"{trip['date_debut'].strftime('%d/%m')} - {trip['date_fin'].strftime('%d/%m/%Y')}"
                
                # Dates
                date_label = tk.Label(details_frame, 
                                    text=f"📅 Dates: {date_range}", 
                                    font=("Helvetica", 9),
                                    fg=self.styles.colors['text_primary'],
                                    bg=card_config['bg'])
                date_label.pack(anchor="w")
                
                # Prix et participants
                info_frame = tk.Frame(details_frame, bg=card_config['bg'])
                info_frame.pack(fill="x", pady=2)
                
                price_label = tk.Label(info_frame, 
                                     text=f"💰 Prix: {trip['prix']}€", 
                                     font=("Helvetica", 9),
                                     fg=self.styles.colors['text_primary'],
                                     bg=card_config['bg'])
                price_label.pack(side="left")
                
                participants_label = tk.Label(info_frame, 
                                            text=f"👥 {trip['participants']} élèves", 
                                            font=("Helvetica", 9),
                                            fg=self.styles.colors['text_primary'],
                                            bg=card_config['bg'])
                participants_label.pack(side="right")
        else:
            tk.Label(trips_frame, 
                    text="Aucun voyage prévu", 
                    font=("Helvetica", 9, "italic"),
                    fg=self.styles.colors['text_secondary'],
                    bg=card_config['bg']).pack()
    
    def get_current_month_name(self):
        """Retourne le nom du mois en cours"""
        months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                 "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        return f"{months[datetime.now().month - 1]} {datetime.now().year}"
    
    def show(self):
        self.frame.pack(fill="both", expand=True)
        
    def hide(self):
        self.frame.pack_forget()