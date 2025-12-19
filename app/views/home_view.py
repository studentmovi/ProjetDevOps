import tkinter as tk
from tkinter import ttk
import os
import sys
import calendar
from datetime import datetime, date, timedelta

# Ajout du chemin pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import des vraies données
from data.event_data_manager import event_manager
from data.sample_data import get_students_data_source

class HomeView:
    """Vue d'accueil de l'application"""
    
    def __init__(self, root, styles, app_controller):
        self.root = root
        self.styles = styles
        self.app_controller = app_controller
        self.frame = None
        self.event_manager = event_manager

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
    
    def _get_real_events_data(self):
        """Récupère les vrais événements depuis le gestionnaire"""
        try:
            events_data = self.event_manager.get_events()
            
            # Gérer les différents formats de retour
            if isinstance(events_data, dict):
                events_list = list(events_data.values())
            else:
                events_list = events_data if events_data else []
            
            # Convertir au format attendu par la vue
            formatted_events = {}
            for event in events_list:
                if isinstance(event, dict) and 'date' in event and 'nom' in event:
                    try:
                        event_date = datetime.strptime(event['date'], '%Y-%m-%d')
                        current_date = datetime.now()
                        
                        # Déterminer le statut
                        if event_date.date() < current_date.date():
                            status = "passé"
                        elif event_date.date() == current_date.date():
                            status = "aujourd'hui"
                        else:
                            status = "à venir"
                        
                        # Récupérer les classes des participants
                        participants = event.get('participants', {})
                        students_data = get_students_data_source()
                        classes_set = set()
                        
                        if isinstance(participants, dict):
                            for student_id in participants.keys():
                                student = next((s for s in students_data if str(s.get('id')) == str(student_id)), None)
                                if student and 'classe' in student:
                                    classes_set.add(student['classe'])
                        
                        # Si aucune classe trouvée, utiliser les classes par défaut ou celles de l'événement
                        if not classes_set:
                            if 'classes_concernees' in event:
                                classes_set = set(event['classes_concernees'])
                            else:
                                classes_set = {"Toutes classes"}
                        
                        formatted_events[event['date']] = {
                            "name": event['nom'],
                            "classes": list(classes_set),
                            "status": status,
                            "participants_count": len(participants) if isinstance(participants, dict) else 0
                        }
                    except Exception as e:
                        print(f"Erreur parsing événement: {e}")
                        continue
            
            return formatted_events
            
        except Exception as e:
            print(f"Erreur récupération événements: {e}")
            return {}

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
        
        # Calculer les stats dynamiques avec les vraies données
        events_data = self._get_real_events_data()
        students_data = get_students_data_source()
        
        total_students = len(students_data) if students_data else 0
        total_events = len(events_data)
        upcoming_events = len([e for e in events_data.values() if e["status"] == "à venir"])
        
        # Classes concernées (uniques)
        all_classes = set()
        for event in events_data.values():
            all_classes.update(event["classes"])
        # Enlever "Toutes classes" du comptage
        all_classes.discard("Toutes classes")
        total_classes = len(all_classes) if all_classes else len(set([s.get('classe', '') for s in students_data if s.get('classe')]))
        
        # Cartes de statistiques
        self._create_stat_card(cards_container, "👥 Élèves", str(total_students), "Total inscrits", 0)
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
        
        # Récupérer les vrais événements
        events_data = self._get_real_events_data()
        
        # Filtrer les événements du mois courant
        monthly_events = []
        for date_str, event in events_data.items():
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
                
                # Classes concernées et participants
                classes_text = ", ".join(event["classes"]) if event["classes"] else "Toutes classes"
                participants_text = f" • {event['participants_count']} participants" if event['participants_count'] > 0 else ""
                
                classes_label = ttk.Label(
                    event_frame,
                    text=f"🏫 Classes: {classes_text}{participants_text}",
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
        
        # Récupérer les vrais événements
        events_data = self._get_real_events_data()
        
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
                    has_event = date_str in events_data
                    
                    # Couleur selon le statut
                    bg_color = self.styles.colors.get('white', '#ffffff')
                    if has_event:
                        event_status = events_data[date_str]["status"]
                        if event_status == "passé":
                            bg_color = self.styles.colors.get('light_gray', '#E0E0E0')
                        elif event_status == "aujourd'hui":
                            bg_color = self.styles.colors.get('warning', '#FFE082')
                        else:  # à venir
                            bg_color = self.styles.colors.get('light_blue', '#BBDEFB')
                    
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
                        fg=self.styles.colors.get('dark_blue', '#2E86AB') if has_event else self.styles.colors.get('text_gray', '#666666')
                    )
                    day_label.pack(expand=True)
                    
                    # Tooltip pour les événements
                    if has_event:
                        event = events_data[date_str]
                        participants_info = f"\nParticipants: {event['participants_count']}" if event['participants_count'] > 0 else ""
                        classes_info = ', '.join(event['classes']) if event['classes'] else 'Toutes classes'
                        tooltip_text = f"{event['name']}\nClasses: {classes_info}{participants_info}"
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
                background=self.styles.colors.get('dark_blue', '#2E86AB'),
                foreground=self.styles.colors.get('white', '#ffffff'),
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
            ("⬜ Passé", self.styles.colors.get('light_gray', '#E0E0E0')),
            ("🟦 À venir", self.styles.colors.get('light_blue', '#BBDEFB')),
            ("🟨 Aujourd'hui", self.styles.colors.get('warning', '#FFE082'))
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
        self.app_controller.open_students_from_home()
        print("🎯 Ouverture de la vue élèves...")
    
    def _import_excel(self):
        from popups.ExcelImportChoicePopup import ExcelImportChoicePopup
        from tkinter import messagebox
        ExcelImportChoicePopup(
            self.root,
            on_students=self.app_controller.import_students_excel,
            on_events=lambda: messagebox.showinfo(
                "Info",
                "L'import des participants se fait depuis la page événements"
            )
        )

    def _create_event(self):
        """Crée un nouvel événement"""
        self.app_controller.create_event_from_home()
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