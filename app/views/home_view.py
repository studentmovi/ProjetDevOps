import tkinter as tk
from tkinter import ttk
import os
import sys
import calendar
from datetime import datetime, date, timedelta

# Ajout du chemin pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class HomeView:
    """Vue d'accueil de l'application"""
    
    def __init__(self, root, styles):
        self.root = root
        self.styles = styles
        self.frame = None
        
        # Données des événements avec dates
        self.events_data = {
            "2024-09-15": {"name": "Sortie Théâtre", "classes": ["3A", "3B"], "status": "passé"},
            "2024-09-22": {"name": "Concert", "classes": ["5A", "5B", "5C"], "status": "passé"},
            "2024-10-10": {"name": "Visite Musée", "classes": ["4A", "4B"], "status": "passé"},
            "2024-11-18": {"name": "Sortie Théâtre", "classes": ["6A", "6B"], "status": "passé"},
            "2024-12-05": {"name": "Concert", "classes": ["2A", "2B"], "status": "aujourd'hui" if datetime.now().strftime("%Y-%m-%d") == "2024-12-05" else "à venir"},
            "2024-12-20": {"name": "Concert de Noël", "classes": ["1A", "1B", "2A"], "status": "à venir"},
            "2025-01-15": {"name": "Voyage Paris", "classes": ["6A", "6B", "6C"], "status": "à venir"},
            "2025-02-12": {"name": "Visite Musée", "classes": ["3A", "3B", "3C"], "status": "à venir"},
            "2025-03-08": {"name": "Sortie Théâtre", "classes": ["4A", "4B"], "status": "à venir"},
            "2025-03-25": {"name": "Concert", "classes": ["5A", "5B"], "status": "à venir"},
            "2025-04-22": {"name": "Voyage Paris", "classes": ["5A", "5B", "5C"], "status": "à venir"},
            "2025-05-10": {"name": "Visite Musée", "classes": ["1A", "1B"], "status": "à venir"},
            "2025-05-28": {"name": "Concert", "classes": ["6A", "6B"], "status": "à venir"},
            "2025-06-15": {"name": "Sortie Théâtre", "classes": ["2A", "2B", "2C"], "status": "à venir"}
        }
    
    def create_widgets(self):
        """Crée l'interface d'accueil avec calendrier et événements"""
        if self.frame:
            self.frame.destroy()
        
        self.frame = ttk.Frame(self.root)
        
        self._create_welcome_section()
        self._create_stats_section()
        
        # Nouveau layout avec calendrier et événements côte à côte
        self._create_events_and_calendar_section()
        
        self._create_quick_actions_section()
    
    def _create_welcome_section(self):
        """Crée la section de bienvenue"""
        welcome_frame = self.styles.create_header_frame(self.frame, padding="20")
        welcome_frame.pack(fill="x", pady=(0, 15))
        
        # Titre principal
        title_label = ttk.Label(
            welcome_frame,
            text="🎓 Bienvenue dans l'application de Gestion Scolaire",
            style="Header.TLabel"
        )
        title_label.pack()
        
        # Sous-titre avec date du jour
        today = datetime.now().strftime("%A %d %B %Y")
        subtitle_label = ttk.Label(
            welcome_frame,
            text=f"📅 {today} • Gérez facilement vos élèves et événements scolaires",
            style="Header.TLabel"
        )
        subtitle_label.pack(pady=(8, 0))
    
    def _create_stats_section(self):
        """Crée la section des statistiques"""
        stats_frame = ttk.Frame(self.frame)
        stats_frame.pack(fill="x", pady=(0, 15))
        
        # Titre de section
        section_title = ttk.Label(
            stats_frame,
            text="📊 Statistiques Rapides",
            style="Heading.TLabel"
        )
        section_title.pack(anchor="w", pady=(0, 8))
        
        # Container pour les cartes de stats
        cards_container = ttk.Frame(stats_frame)
        cards_container.pack(fill="x")
        
        # Calculer les stats dynamiques
        total_events = len(self.events_data)
        upcoming_events = len([e for e in self.events_data.values() if e["status"] == "à venir"])
        total_classes = len(set(classe for event in self.events_data.values() for classe in event["classes"]))
        
        # Cartes de statistiques
        self._create_stat_card(cards_container, "👥 Élèves", "48", "Total inscrits", 0)
        self._create_stat_card(cards_container, "📅 Événements", str(upcoming_events), "À venir", 1)
        self._create_stat_card(cards_container, "🏫 Classes", str(total_classes), "Classes concernées", 2)
        self._create_stat_card(cards_container, "📈 Total", str(total_events), "Événements planifiés", 3)
    
    def _create_stat_card(self, parent, icon_text, number, description, column):
        """Crée une carte de statistique"""
        card_frame = self.styles.create_card_frame(parent, padding="12")
        card_frame.grid(row=0, column=column, sticky="nsew", padx=4)
        
        # Configuration des colonnes pour répartir l'espace
        parent.grid_columnconfigure(column, weight=1)
        
        # Icône et nombre
        header_frame = ttk.Frame(card_frame)
        header_frame.pack(fill="x")
        
        icon_label = ttk.Label(
            header_frame,
            text=icon_text,
            font=("Arial", 12, "bold"),
            style="Heading.TLabel"
        )
        icon_label.pack(side="left")
        
        number_label = ttk.Label(
            header_frame,
            text=number,
            font=("Arial", 18, "bold"),
            style="Title.TLabel"
        )
        number_label.pack(side="right")
        
        # Description
        desc_label = ttk.Label(
            card_frame,
            text=description,
            style="Small.TLabel"
        )
        desc_label.pack(anchor="w", pady=(4, 0))
    
    def _create_events_and_calendar_section(self):
        """Crée la section avec événements du mois et calendrier côte à côte"""
        container = ttk.Frame(self.frame)
        container.pack(fill="both", expand=True, pady=(0, 15))
        
        # ========== ÉVÉNEMENTS DU MOIS (côté gauche) ==========
        events_frame = ttk.LabelFrame(
            container,
            text="📅 Événements de ce mois",
            style="TLabelframe",
            padding="10"
        )
        events_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))
        
        self._create_monthly_events(events_frame)
        
        # ========== CALENDRIER (côté droit) ==========
        calendar_frame = ttk.LabelFrame(
            container,
            text="🗓️ Calendrier des événements",
            style="TLabelframe",
            padding="10"
        )
        calendar_frame.pack(side="right", fill="both", expand=True, padx=(8, 0))
        
        self._create_calendar_widget(calendar_frame)
    
    def _create_monthly_events(self, parent):
        """Crée la liste des événements du mois courant"""
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Filtrer les événements du mois courant
        monthly_events = []
        for date_str, event in self.events_data.items():
            event_date = datetime.strptime(date_str, "%Y-%m-%d")
            if event_date.month == current_month and event_date.year == current_year:
                monthly_events.append((date_str, event))
        
        # Trier par date
        monthly_events.sort(key=lambda x: x[0])
        
        if not monthly_events:
            no_events_label = ttk.Label(
                parent,
                text="📭 Aucun événement prévu ce mois-ci",
                style="Small.TLabel"
            )
            no_events_label.pack(pady=20)
        else:
            # Liste des événements avec scrollbar
            list_frame = ttk.Frame(parent)
            list_frame.pack(fill="both", expand=True)
            
            # Canvas avec scrollbar pour les événements
            canvas = tk.Canvas(list_frame, height=200, bg=self.styles.colors['white'])
            scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Ajouter les événements
            for date_str, event in monthly_events:
                event_date = datetime.strptime(date_str, "%Y-%m-%d")
                
                # Frame pour chaque événement
                event_frame = self.styles.create_card_frame(scrollable_frame, padding="8")
                event_frame.pack(fill="x", pady=2)
                
                # Date et statut
                date_formatted = event_date.strftime("%d/%m")
                status_emoji = {"passé": "✅", "aujourd'hui": "🔥", "à venir": "⏳"}
                status_color = {"passé": "gray", "aujourd'hui": "red", "à venir": "blue"}
                
                header_frame = ttk.Frame(event_frame)
                header_frame.pack(fill="x")
                
                date_status_label = ttk.Label(
                    header_frame,
                    text=f"{status_emoji[event['status']]} {date_formatted}",
                    font=("Arial", 9, "bold"),
                    style="Small.TLabel"
                )
                date_status_label.pack(side="left")
                
                status_label = ttk.Label(
                    header_frame,
                    text=event["status"].upper(),
                    font=("Arial", 8),
                    style="Small.TLabel"
                )
                status_label.pack(side="right")
                
                # Nom de l'événement
                event_name_label = ttk.Label(
                    event_frame,
                    text=f"🎭 {event['name']}",
                    font=("Arial", 10, "bold"),
                    style="Heading.TLabel"
                )
                event_name_label.pack(anchor="w")
                
                # Classes concernées
                classes_text = ", ".join(event["classes"])
                classes_label = ttk.Label(
                    event_frame,
                    text=f"🏫 Classes: {classes_text}",
                    style="Small.TLabel"
                )
                classes_label.pack(anchor="w")
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
    
    def _create_calendar_widget(self, parent):
        """Crée un calendrier avec les événements marqués"""
        # En-tête avec navigation
        nav_frame = ttk.Frame(parent)
        nav_frame.pack(fill="x", pady=(0, 10))
        
        # Date actuelle pour la navigation
        self.current_date = datetime.now()
        
        # Boutons de navigation
        prev_btn = ttk.Button(
            nav_frame,
            text="◀",
            width=3,
            command=self._prev_month
        )
        prev_btn.pack(side="left")
        
        self.month_year_label = ttk.Label(
            nav_frame,
            text="",
            font=("Arial", 12, "bold"),
            style="Heading.TLabel"
        )
        self.month_year_label.pack(side="left", expand=True)
        
        next_btn = ttk.Button(
            nav_frame,
            text="▶",
            width=3,
            command=self._next_month
        )
        next_btn.pack(side="right")
        
        # Frame pour le calendrier
        self.calendar_frame = ttk.Frame(parent)
        self.calendar_frame.pack(fill="both", expand=True)
        
        # Créer le calendrier initial
        self._update_calendar()
    
    def _prev_month(self):
        """Mois précédent"""
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year-1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month-1)
        self._update_calendar()
    
    def _next_month(self):
        """Mois suivant"""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year+1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month+1)
        self._update_calendar()
    
    def _update_calendar(self):
        """Met à jour l'affichage du calendrier"""
        # Nettoyer le frame du calendrier
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        
        # Mettre à jour le titre
        month_names = [
            "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
            "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
        ]
        self.month_year_label.config(
            text=f"{month_names[self.current_date.month-1]} {self.current_date.year}"
        )
        
        # En-têtes des jours
        days = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        for i, day in enumerate(days):
            day_label = ttk.Label(
                self.calendar_frame,
                text=day,
                font=("Arial", 9, "bold"),
                style="Small.TLabel"
            )
            day_label.grid(row=0, column=i, padx=1, pady=1, sticky="nsew")
        
        # Configuration des colonnes
        for i in range(7):
            self.calendar_frame.grid_columnconfigure(i, weight=1)
        
        # Obtenir le calendrier du mois
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        
        # Créer les cases du calendrier
        for week_num, week in enumerate(cal, start=1):
            for day_num, day in enumerate(week):
                if day == 0:
                    # Jour vide
                    empty_frame = ttk.Frame(self.calendar_frame)
                    empty_frame.grid(row=week_num, column=day_num, padx=1, pady=1, sticky="nsew")
                else:
                    # Vérifier s'il y a un événement ce jour
                    date_str = f"{self.current_date.year:04d}-{self.current_date.month:02d}-{day:02d}"
                    has_event = date_str in self.events_data
                    
                    # Couleur selon le statut
                    bg_color = self.styles.colors['white']
                    if has_event:
                        event_status = self.events_data[date_str]["status"]
                        if event_status == "passé":
                            bg_color = self.styles.colors['light_gray']
                        elif event_status == "aujourd'hui":
                            bg_color = self.styles.colors['warning']
                        else:  # à venir
                            bg_color = self.styles.colors['light_blue']
                    
                    # Créer la case du jour
                    day_frame = tk.Frame(
                        self.calendar_frame,
                        bg=bg_color,
                        relief="solid",
                        borderwidth=1,
                        width=30,
                        height=30
                    )
                    day_frame.grid(row=week_num, column=day_num, padx=1, pady=1, sticky="nsew")
                    day_frame.grid_propagate(False)
                    
                    # Numéro du jour
                    day_label = tk.Label(
                        day_frame,
                        text=str(day),
                        bg=bg_color,
                        font=("Arial", 9, "bold" if has_event else "normal"),
                        fg=self.styles.colors['dark_blue'] if has_event else self.styles.colors['text_gray']
                    )
                    day_label.pack(expand=True)
                    
                    # Tooltip pour les événements
                    if has_event:
                        event = self.events_data[date_str]
                        tooltip_text = f"{event['name']}\nClasses: {', '.join(event['classes'])}"
                        self._create_tooltip(day_frame, tooltip_text)
        
        # Configuration des lignes
        for i in range(len(cal) + 1):
            self.calendar_frame.grid_rowconfigure(i, weight=1)
    
    def _create_tooltip(self, widget, text):
        """Crée un tooltip pour un widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(
                tooltip,
                text=text,
                background=self.styles.colors['dark_blue'],
                foreground=self.styles.colors['white'],
                font=("Arial", 8),
                relief="solid",
                borderwidth=1,
                padx=5,
                pady=3
            )
            label.pack()
            
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def _create_quick_actions_section(self):
        """Crée la section des actions rapides"""
        actions_frame = ttk.Frame(self.frame)
        actions_frame.pack(fill="x", pady=(0, 10))
        
        # Titre de section
        section_title = ttk.Label(
            actions_frame,
            text="⚡ Actions Rapides",
            style="Heading.TLabel"
        )
        section_title.pack(anchor="w", pady=(0, 8))
        
        # Container pour les boutons
        buttons_container = ttk.Frame(actions_frame)
        buttons_container.pack(fill="x")
        
        # Boutons d'actions rapides
        btn_students = ttk.Button(
            buttons_container,
            text="👥 Gérer les Élèves",
            style="Primary.TButton",
            command=self._open_students_view
        )
        btn_students.pack(side="left", padx=(0, 8))
        
        btn_import = ttk.Button(
            buttons_container,
            text="📊 Importer Excel",
            style="Success.TButton",
            command=self._import_excel
        )
        btn_import.pack(side="left", padx=(0, 8))
        
        btn_events = ttk.Button(
            buttons_container,
            text="📅 Nouveau Événement",
            style="Warning.TButton",
            command=self._create_event
        )
        btn_events.pack(side="left", padx=(0, 8))
        
        btn_export = ttk.Button(
            buttons_container,
            text="📤 Exporter Données",
            style="Secondary.TButton",
            command=self._export_data
        )
        btn_export.pack(side="left")
        
        # Légende du calendrier
        legend_frame = ttk.Frame(buttons_container)
        legend_frame.pack(side="right")
        
        legend_label = ttk.Label(
            legend_frame,
            text="🔍 Légende: ",
            style="Small.TLabel"
        )
        legend_label.pack(side="left")
        
        legend_items = [
            ("⬜ Passé", self.styles.colors['light_gray']),
            ("🟦 À venir", self.styles.colors['light_blue']),
            ("🟨 Aujourd'hui", self.styles.colors['warning'])
        ]
        
        for text, color in legend_items:
            legend_item = tk.Label(
                legend_frame,
                text=text,
                bg=color,
                font=("Arial", 8),
                padx=4,
                pady=2,
                relief="solid",
                borderwidth=1
            )
            legend_item.pack(side="left", padx=2)
    
    # ========== CALLBACKS ==========
    def _open_students_view(self):
        """Ouvre la vue des élèves"""
        print("🎯 Ouverture de la vue élèves...")
    
    def _import_excel(self):
        """Lance l'import Excel"""
        from tkinter import messagebox
        messagebox.showinfo("📊 Import Excel", "Fonctionnalité d'import Excel\n(À développer)")
    
    def _create_event(self):
        """Crée un nouvel événement"""
        from tkinter import messagebox
        messagebox.showinfo("📅 Nouvel Événement", "Création d'événement\n(À développer)")
    
    def _export_data(self):
        """Exporte les données"""
        from tkinter import messagebox
        messagebox.showinfo("📤 Export", "Export des données\n(À développer)")
    
    def show(self):
        """Affiche la vue"""
        if self.frame:
            self.frame.pack(fill="both", expand=True, padx=8, pady=8)
    
    def hide(self):
        """Cache la vue"""
        if self.frame:
            self.frame.pack_forget()