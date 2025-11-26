import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Ajout du chemin pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from component.FilterPanel import FilterPanel
from component.Button import StyledButton
from controller.StudentViewController import StudentViewController

class StudentView:
    """Vue principale pour la gestion des élèves"""
    
    def __init__(self, root, styles):
        self.root = root
        self.styles = styles
        self.frame = None
        self.controller = None
        
        # Variables pour les widgets
        self.search_var = tk.StringVar()
        self.search_entry = None
        self.year_combo = None
        self.class_combo = None
        self.event_combo = None
        self.month_combo = None  # NOUVEAU: Filtre par mois
        self.sort_combo = None
        
        # Conteneurs pour l'affichage
        self.treeview = None
        self.status_label = None
        self.toolbar_frame = None
        
    def create_widgets(self):
        """Méthode appelée par main.py pour créer les widgets"""
        self.create_view()
    
    def create_view(self):
        """Crée l'interface principale de la vue élèves"""
        if self.frame:
            self.frame.destroy()
        
        self.frame = ttk.Frame(self.root)
        
        # Initialiser le contrôleur avec cette vue
        self.controller = StudentViewController(self)
        
        self._create_toolbar()
        self._create_filter_panel()
        self._create_main_content()
        self._create_status_bar()
        
        # Chargement initial
        if self.controller:
            try:
                self._initialize_default_filters()
                self.controller.load_all_students_on_startup()
            except Exception as e:
                print(f"Erreur chargement initial: {e}")
    
    def _initialize_default_filters(self):
        """Initialise les filtres avec leurs valeurs par défaut"""
        try:
            if self.year_combo:
                self.year_combo.set("Toutes")
            if self.class_combo:
                self.class_combo.set("Toutes")
            if self.event_combo:
                self.event_combo.set("Tous")
            if self.month_combo:
                self.month_combo.set("Tous")
            if self.sort_combo:
                self.sort_combo.set("Nom A-Z")
            
            self.search_var.set("")
        except Exception as e:
            print(f"Erreur initialisation filtres: {e}")
    
    def _create_toolbar(self):
        """Crée la barre d'outils simplifiée"""
        self.toolbar_frame = ttk.LabelFrame(
            self.frame, 
            text="⚙️ Actions Rapides", 
            style="Compact.TLabelframe",
            padding="8"
        )
        self.toolbar_frame.pack(fill="x", pady=(10, 8))
        
        buttons_frame = ttk.Frame(self.toolbar_frame)
        buttons_frame.pack(fill="x")
        
        # Groupe Import à gauche
        import_frame = ttk.Frame(buttons_frame)
        import_frame.pack(side="left")
        
        import_excel_btn = ttk.Button(
            import_frame,
            text="📊 Importer Excel",
            command=self._on_import_excel,
            style="Primary.TButton"
        )
        import_excel_btn.pack(side="left")
        
        # Groupe Actions d'événements à droite
        events_frame = ttk.Frame(buttons_frame)
        events_frame.pack(side="right")
        
        assign_event_btn = ttk.Button(
            events_frame,
            text="📅 Assigner événement",
            command=self._safe_assign_to_event,
            style="Success.TButton"
        )
        assign_event_btn.pack(side="left", padx=(0, 5))
        
        calculate_cost_btn = ttk.Button(
            events_frame,
            text="💰 Calculer coût",
            command=self._safe_calculate_event_cost,
            style="Warning.TButton"
        )
        calculate_cost_btn.pack(side="left")
    
    def _create_filter_panel(self):
        """Crée un panneau de filtres avec tous les boutons"""
        filter_frame = ttk.LabelFrame(
            self.frame, 
            text="🔍 Filtres", 
            style="Compact.TLabelframe",
            padding="8"
        )
        filter_frame.pack(fill="x", pady=(0, 8))
        
        # LIGNE 1: RECHERCHE + TRI
        row1 = ttk.Frame(filter_frame)
        row1.pack(fill="x", pady=(0, 6))
        
        # Recherche
        search_frame = ttk.Frame(row1)
        search_frame.pack(side="left", fill="x", expand=True)
        
        ttk.Label(search_frame, text="🔍", font=("Arial", 10)).pack(side="left", padx=(0, 3))
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20, font=("Arial", 9))
        self.search_entry.pack(side="left", padx=(0, 10))
        
        # Tri - MODIFIÉ avec option Date
        sort_frame = ttk.Frame(row1)
        sort_frame.pack(side="right")
        
        ttk.Label(sort_frame, text="Tri", font=("Arial", 10)).pack(side="left", padx=(0, 3))
        self.sort_combo = ttk.Combobox(
            sort_frame, 
            values=["Nom A-Z", "Nom Z-A", "Classe", "Année", "Date (Mois)"], 
            state="readonly", 
            width=12,
            font=("Arial", 9)
        )
        self.sort_combo.set("Nom A-Z")
        self.sort_combo.pack(side="left")
        
        # LIGNE 2: FILTRES PRINCIPAUX + ÉVÉNEMENT + MOIS
        row2 = ttk.Frame(filter_frame)
        row2.pack(fill="x", pady=(3, 0))
        
        filters_container = ttk.Frame(row2)
        filters_container.pack(side="left", fill="x", expand=True)
        
        # Année
        year_frame = ttk.Frame(filters_container)
        year_frame.pack(side="left", padx=(0, 8))
        
        ttk.Label(year_frame, text="Année", font=("Arial", 9)).pack(side="left", padx=(0, 2))
        self.year_combo = ttk.Combobox(
            year_frame, 
            values=["Toutes", "1ère", "2ème", "3ème", "4ème", "5ème", "6ème"], 
            state="readonly", 
            width=7,
            font=("Arial", 9)
        )
        self.year_combo.set("Toutes")
        self.year_combo.pack(side="left")
        
        # Classe
        class_frame = ttk.Frame(filters_container)
        class_frame.pack(side="left", padx=(0, 8))
        
        ttk.Label(class_frame, text="Classe", font=("Arial", 9)).pack(side="left", padx=(0, 2))
        self.class_combo = ttk.Combobox(
            class_frame, 
            values=["Toutes", "1A", "1B", "2A", "2B", "3A", "3B", "3C", "4A", "4B", "5A", "5B", "5C", "6A", "6B", "6C"], 
            state="readonly", 
            width=7,
            font=("Arial", 9)
        )
        self.class_combo.set("Toutes")
        self.class_combo.pack(side="left")
        
        # Événement
        event_frame = ttk.Frame(filters_container)
        event_frame.pack(side="left", padx=(0, 8))
        
        ttk.Label(event_frame, text="Événement", font=("Arial", 9)).pack(side="left", padx=(0, 2))
        self.event_combo = ttk.Combobox(
            event_frame, 
            values=["Tous", "Sortie Théâtre", "Visite Musée", "Concert", "Voyage Paris"], 
            state="readonly", 
            width=10,
            font=("Arial", 9)
        )
        self.event_combo.set("Tous")
        self.event_combo.pack(side="left")
        
        # NOUVEAU: Filtre par Mois
        month_frame = ttk.Frame(filters_container)
        month_frame.pack(side="left", padx=(0, 8))
        
        ttk.Label(month_frame, text="Mois", font=("Arial", 9)).pack(side="left", padx=(0, 2))
        self.month_combo = ttk.Combobox(
            month_frame, 
            values=["Tous"], 
            state="readonly", 
            width=10,
            font=("Arial", 9)
        )
        self.month_combo.set("Tous")
        self.month_combo.pack(side="left")
        
        # Boutons d'action à droite - plus compacts
        actions_frame = ttk.Frame(row2)
        actions_frame.pack(side="right")
        
        reset_btn = ttk.Button(
            actions_frame,
            text="🔄 Reset",
            command=self._safe_reset_filters,
            style="Light.TButton",
            width=6
        )
        reset_btn.pack(side="left", padx=(0, 3))
        
        export_btn = ttk.Button(
            actions_frame,
            text="📤 Export",
            command=self._safe_export_data,
            style="Secondary.TButton",
            width=6
        )
        export_btn.pack(side="left")
        
        # LIGNE 3: BOUTONS DE SÉLECTION
        row3 = ttk.Frame(filter_frame)
        row3.pack(fill="x", pady=(6, 0))
        
        # Boutons de sélection à gauche
        selection_frame = ttk.Frame(row3)
        selection_frame.pack(side="left")
        
        select_all_btn = ttk.Button(
            selection_frame,
            text="☑️ Tout sélectionner",
            command=self._safe_select_all,
            style="Light.TButton"
        )
        select_all_btn.pack(side="left", padx=(0, 5))
        
        deselect_all_btn = ttk.Button(
            selection_frame,
            text="☐ Tout désélectionner",
            command=self._safe_deselect_all,
            style="Light.TButton"
        )
        deselect_all_btn.pack(side="left", padx=(0, 5))
        
        # Actualiser à côté
        refresh_btn = ttk.Button(
            selection_frame,
            text="🔄 Actualiser",
            command=self._on_refresh,
            style="Secondary.TButton"
        )
        refresh_btn.pack(side="left")
        
        self._setup_filter_bindings()
    
    def _setup_filter_bindings(self):
        """Configure les bindings pour les filtres"""
        try:
            self.search_var.trace('w', self._safe_on_search_changed)
            
            if self.year_combo:
                self.year_combo.bind('<<ComboboxSelected>>', self._safe_on_year_changed)
            if self.class_combo:
                self.class_combo.bind('<<ComboboxSelected>>', self._safe_on_filter_changed)
            if self.event_combo:
                self.event_combo.bind('<<ComboboxSelected>>', self._safe_on_filter_changed)
            if self.month_combo:  # NOUVEAU
                self.month_combo.bind('<<ComboboxSelected>>', self._safe_on_filter_changed)
            if self.sort_combo:
                self.sort_combo.bind('<<ComboboxSelected>>', self._safe_on_sort_changed)
                
            self._setup_search_placeholder()
            self._load_filter_options()
            
        except Exception as e:
            print(f"Erreur bindings: {e}")
    
    def _load_filter_options(self):
        """Charge les options de filtres depuis le contrôleur"""
        if self.controller:
            try:
                # Événements
                if self.event_combo:
                    events = self.controller.get_events_for_filter()
                    self.event_combo.configure(values=events)
                
                # Mois - NOUVEAU
                if self.month_combo:
                    months = self.controller.get_months_for_filter()
                    self.month_combo.configure(values=months)
                    
            except Exception as e:
                print(f"Erreur chargement options filtres: {e}")
    
    def _setup_search_placeholder(self):
        """Configure le placeholder pour la recherche"""
        placeholder_text = "Nom, prénom..."
        
        def on_focus_in(event):
            if self.search_entry.get() == placeholder_text:
                self.search_entry.delete(0, tk.END)
        
        def on_focus_out(event):
            if not self.search_entry.get():
                self.search_entry.insert(0, placeholder_text)
        
        self.search_entry.insert(0, placeholder_text)
        self.search_entry.bind('<FocusIn>', on_focus_in)
        self.search_entry.bind('<FocusOut>', on_focus_out)
    
    def _create_main_content(self):
        """Crée la zone principale avec Treeview"""
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill="both", expand=True, pady=(0, 8))
        
        columns = ("selection", "nom", "prenom", "classe", "annee", "option", "evenements", "actions")
        
        self.treeview = ttk.Treeview(
            main_frame,
            columns=columns,
            show="tree headings",
            height=15,
            selectmode="extended"
        )
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.treeview.yview)
        h_scrollbar = ttk.Scrollbar(main_frame, orient="horizontal", command=self.treeview.xview)
        
        self.treeview.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Configuration des colonnes
        self.treeview.column("#0", width=25, minwidth=25, stretch=False)
        self.treeview.column("selection", width=40, minwidth=40, stretch=False, anchor="center")
        self.treeview.column("nom", width=120, minwidth=100, stretch=True)
        self.treeview.column("prenom", width=120, minwidth=100, stretch=True)
        self.treeview.column("classe", width=50, minwidth=45, stretch=False)
        self.treeview.column("annee", width=70, minwidth=60, stretch=False)
        self.treeview.column("option", width=100, minwidth=80, stretch=False)
        self.treeview.column("evenements", width=250, minwidth=200, stretch=True)  # AUGMENTÉ
        self.treeview.column("actions", width=200, minwidth=180, stretch=False)
        
        # En-têtes
        self.treeview.heading("#0", text="", anchor="w")
        self.treeview.heading("selection", text="☑️", anchor="center")
        self.treeview.heading("nom", text="Nom", anchor="w")
        self.treeview.heading("prenom", text="Prénom", anchor="w")
        self.treeview.heading("classe", text="Classe", anchor="center")
        self.treeview.heading("annee", text="Année", anchor="center")
        self.treeview.heading("option", text="Option", anchor="center")
        self.treeview.heading("evenements", text="Événements", anchor="w")
        self.treeview.heading("actions", text="Actions", anchor="center")
        
        # Tags pour les styles
        self.treeview.tag_configure("selected", 
            background=self.styles.colors['selected'], 
            foreground=self.styles.colors['dark_blue']
        )
        self.treeview.tag_configure("odd", 
            background=self.styles.colors['off_white']
        )
        self.treeview.tag_configure("even", 
            background=self.styles.colors['white']
        )
        
        # Placement
        self.treeview.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Bindings
        self.treeview.bind("<Double-1>", self._on_treeview_double_click)
        self.treeview.bind("<Button-1>", self._on_treeview_click)
    
    def _create_status_bar(self):
        """Crée la barre de statut"""
        status_frame = self.styles.create_card_frame(self.frame)
        status_frame.pack(fill="x", side="bottom")
        
        self.status_label = ttk.Label(
            status_frame,
            text="🔄 Prêt - Chargement des données...",
            style="Small.TLabel",
            padding="8"
        )
        self.status_label.pack(side="left", fill="x", expand=True)
    
    def _format_events_display(self, events_list):
        """Formate l'affichage des événements - AMÉLIORÉ"""
        if not events_list or len(events_list) == 0:
            return "Aucun événement"
        elif len(events_list) == 1:
            return events_list[0]
        elif len(events_list) <= 3:
            return " • ".join(events_list)
        else:
            # Plus de 3 événements : afficher les 2 premiers + compteur
            return f"{events_list[0]} • {events_list[1]} (+{len(events_list)-2} autres)"
    
    def _create_events_popup(self, events_list, x, y):
        """Crée un popup pour afficher tous les événements"""
        if len(events_list) <= 3:
            return
        
        popup = tk.Toplevel(self.treeview)
        popup.wm_overrideredirect(True)
        popup.configure(bg="#f9f9f9", relief="solid", borderwidth=1)
        
        # Positionner le popup
        popup.geometry(f"+{x+10}+{y+10}")
        
        # Titre
        title_label = tk.Label(popup, text="📅 Tous les événements:", 
                              font=("Arial", 9, "bold"), 
                              bg="#f9f9f9", fg="#333")
        title_label.pack(padx=8, pady=(6, 3))
        
        # Liste des événements avec scroll si nécessaire
        max_height = min(len(events_list), 8)  # Maximum 8 événements visibles
        
        if len(events_list) > 8:
            # Frame avec scrollbar pour beaucoup d'événements
            list_frame = tk.Frame(popup, bg="#f9f9f9")
            list_frame.pack(padx=8, pady=3)
            
            canvas = tk.Canvas(list_frame, bg="#f9f9f9", width=200, height=150, highlightthickness=0)
            scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#f9f9f9")
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            for i, event in enumerate(events_list):
                event_label = tk.Label(scrollable_frame, text=f"• {event}", 
                                      font=("Arial", 8), 
                                      bg="#f9f9f9", fg="#555",
                                      anchor="w")
                event_label.pack(fill="x", padx=5, pady=1)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        else:
            # Affichage simple pour peu d'événements
            for i, event in enumerate(events_list):
                event_label = tk.Label(popup, text=f"• {event}", 
                                      font=("Arial", 8), 
                                      bg="#f9f9f9", fg="#555",
                                      anchor="w")
                event_label.pack(fill="x", padx=10, pady=1)
        
        # Note en bas
        note_label = tk.Label(popup, text="(Cliquez pour fermer)", 
                             font=("Arial", 7, "italic"), 
                             bg="#f9f9f9", fg="#888")
        note_label.pack(pady=(3, 6))
        
        # Fermer automatiquement après 5 secondes
        popup.after(5000, popup.destroy)
        
        # Fermer si on clique ailleurs
        def close_popup(event=None):
            try:
                popup.destroy()
            except:
                pass
        
        popup.bind("<Button-1>", close_popup)
        popup.bind("<FocusOut>", close_popup)
        
        # Centrer mieux le popup
        popup.update_idletasks()
        popup_width = popup.winfo_width()
        popup_height = popup.winfo_height()
        
        # Ajuster si le popup sort de l'écran
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        
        if x + popup_width > screen_width:
            x = screen_width - popup_width - 10
        if y + popup_height > screen_height:
            y = screen_height - popup_height - 10
            
        popup.geometry(f"+{x}+{y}")
    
    def update_display(self):
        """Met à jour l'affichage de la liste des étudiants"""
        if not self.controller:
            if self.status_label:
                self.status_label.config(text="❌ Erreur: Contrôleur non initialisé")
            return
        
        # Vider le treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        try:
            filtered_students = self.controller.get_filtered_students()
            selected_students = self.controller.get_selected_students()
        except Exception as e:
            print(f"Erreur récupération données: {e}")
            filtered_students = []
            selected_students = []
        
        if not filtered_students:
            self.treeview.insert("", "end", text="", values=(
                "", "🔍 Aucun étudiant trouvé", "", "", "", "", "", ""
            ))
        else:
            for i, student in enumerate(filtered_students):
                try:
                    student_id = student.get('id', '')
                    
                    # Icône de sélection
                    selection_icon = "☑️" if student_id in selected_students else "☐"
                    
                    # Événements - AMÉLIORÉ avec dates
                    events_list = self.controller.get_student_events(student)
                    formatted_events = self._format_events_display(events_list)
                    
                    # Actions avec plus d'espace
                    actions_text = "👁️ Voir détails | 🗑️ Supprimer"
                    
                    # Option
                    option_text = student.get('option', 'Aucune')
                    
                    # Couleur alternée
                    tag = "even" if i % 2 == 0 else "odd"
                    if student_id in selected_students:
                        tag = "selected"
                    
                    item = self.treeview.insert("", "end", 
                        iid=f"student_{student_id}",
                        text="", 
                        values=(
                            selection_icon,
                            student.get('nom', ''),
                            student.get('prenom', ''),
                            student.get('classe', ''),
                            f"{student.get('annee', '')}ème",
                            option_text,
                            formatted_events,
                            actions_text
                        ),
                        tags=(tag,)
                    )
                    
                    # Stocker la liste complète des événements pour le popup
                    if events_list:
                        setattr(self.treeview, f"events_{student_id}", events_list)
                    
                except Exception as e:
                    print(f"Erreur affichage étudiant {student}: {e}")
        
        # Statut
        try:
            total = len(self.controller.get_students_data())
            filtered = len(filtered_students)
            selected = len(selected_students)
            
            status_parts = [f"📊 Total: {total}"]
            if filtered != total:
                status_parts.append(f"🔍 Affichés: {filtered}")
            if selected > 0:
                status_parts.append(f"☑️ Sélectionnés: {selected}")
            
            source = "Excel" if self.controller.is_using_excel_data() else "JSON"
            status_parts.append(f"📁 {source}")
            
            if self.status_label:
                self.status_label.config(text=" | ".join(status_parts))
        except Exception as e:
            if self.status_label:
                self.status_label.config(text=f"❌ Erreur: {e}")
    
    # ========== GESTION DES CLICS ==========
    def _on_treeview_click(self, event):
        """Gère les clics sur le treeview"""
        item = self.treeview.identify_row(event.y)
        column = self.treeview.identify_column(event.x)
        
        if item and item.startswith("student_"):
            student_id = int(item.replace("student_", ""))
            
            # Clic sur la colonne de sélection
            if column == "#1":  # Colonne selection
                self._toggle_student_selection(student_id)
            # Clic sur la colonne événements - AMÉLIORÉ
            elif column == "#7":  # Colonne événements
                events_list = getattr(self.treeview, f"events_{student_id}", None)
                if events_list and len(events_list) > 3:  # Popup si plus de 3 événements
                    x = event.x_root
                    y = event.y_root
                    self._create_events_popup(events_list, x, y)
            # Clic sur la colonne actions
            elif column == "#8":  # Colonne actions
                self._handle_action_click(event, student_id)
    
    def _on_treeview_double_click(self, event):
        """Gère les double-clics (ouvre les détails)"""
        item = self.treeview.identify_row(event.y)
        if item and item.startswith("student_"):
            student_id = int(item.replace("student_", ""))
            self._safe_view_student(student_id)
    
    def _handle_action_click(self, event, student_id):
        """Gère les clics sur la colonne actions"""
        menu = tk.Menu(self.treeview, tearoff=0)
        menu.add_command(label="👁️ Voir détails", 
                        command=lambda: self._safe_view_student(student_id))
        menu.add_separator()
        menu.add_command(label="🗑️ Supprimer", 
                        command=lambda: self._safe_delete_student(student_id))
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def _toggle_student_selection(self, student_id):
        """Bascule la sélection d'un étudiant"""
        if self.controller:
            try:
                selected = self.controller.toggle_student_selection(student_id)
                self.update_display()
                return selected
            except Exception as e:
                print(f"Erreur toggle sélection: {e}")
                return False
    
    # ========== MÉTHODES SAFE ==========
    def _safe_select_all(self):
        if self.controller:
            try:
                self.controller.select_all()
                print("Tous les étudiants sélectionnés")
            except Exception as e:
                messagebox.showerror("❌ Erreur", f"Erreur sélection: {e}")
    
    def _safe_deselect_all(self):
        if self.controller:
            try:
                self.controller.deselect_all()
                print("Tous les étudiants désélectionnés")
            except Exception as e:
                messagebox.showerror("❌ Erreur", f"Erreur désélection: {e}")
    
    def _safe_assign_to_event(self):
        if self.controller:
            try:
                self.controller.assign_to_event()
            except Exception as e:
                messagebox.showerror("❌ Erreur", f"Erreur assignation: {e}")
    
    def _safe_calculate_event_cost(self):
        if self.controller:
            try:
                self.controller.calculate_event_cost()
            except Exception as e:
                messagebox.showerror("❌ Erreur", f"Erreur calcul coût: {e}")
    
    def _safe_view_student(self, student_id):
        if self.controller:
            try:
                self.controller.view_student(student_id)
            except Exception as e:
                messagebox.showerror("❌ Erreur", f"Erreur affichage détails: {e}")
    
    def _safe_delete_student(self, student_id):
        if self.controller:
            try:
                current_data = self.controller.get_students_data()
                student = next((s for s in current_data if s["id"] == student_id), None)
                if student:
                    student_name = f"{student.get('prenom', '')} {student.get('nom', '')}"
                    result = messagebox.askyesno("🗑️ Supprimer", 
                                               f"Supprimer l'étudiant {student_name} ?\n\n"
                                               "L'étudiant sera retiré de la liste mais pas supprimé définitivement.")
                    if result:
                        success = self.controller.delete_student(student_id)
                        if success:
                            messagebox.showinfo("✅ Suppression", f"{student_name} a été retiré de la liste.")
                        else:
                            messagebox.showerror("❌ Erreur", "Impossible de supprimer l'étudiant.")
            except Exception as e:
                messagebox.showerror("❌ Erreur", f"Erreur suppression: {e}")
    
    def _safe_export_data(self):
        if self.controller:
            try:
                self.controller.export_filtered_data()
            except Exception as e:
                messagebox.showerror("❌ Erreur", f"Erreur export: {e}")
    
    def _safe_reset_filters(self):
        try:
            if self.controller:
                self.controller.reset_filters()
            print("Filtres réinitialisés")
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur reset: {e}")
    
    # ========== EVENT HANDLERS ==========
    def _safe_on_search_changed(self, *args):
        if self.controller and self.search_entry:
            current_text = self.search_var.get()
            if current_text != "Nom, prénom...":
                self.controller.on_search_changed()
    
    def _safe_on_year_changed(self, event=None):
        if self.controller:
            try:
                self.controller.on_year_changed(event)
            except Exception as e:
                print(f"Erreur changement année: {e}")
    
    def _safe_on_filter_changed(self, event=None):
        if self.controller:
            try:
                self.controller.on_filter_changed(event)
            except Exception as e:
                print(f"Erreur changement filtre: {e}")
    
    def _safe_on_sort_changed(self, event=None):
        if self.controller:
            try:
                self.controller.on_sort_changed(event)
            except Exception as e:
                print(f"Erreur changement tri: {e}")
    
    # ========== AUTRES CALLBACKS ==========
    def _on_import_excel(self):
        if self.controller:
            try:
                self.controller.import_excel_students()
            except Exception as e:
                messagebox.showerror("❌ Erreur", f"Erreur import Excel: {e}")
    
    def _on_refresh(self):
        try:
            if self.controller:
                self.controller.refresh_data()
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur refresh: {e}")
    
    def refresh_view(self):
        """Rafraîchit la vue"""
        if self.controller:
            try:
                self.controller.apply_all_filters()
            except Exception as e:
                print(f"Erreur refresh vue: {e}")
    
    def show(self):
        """Affiche la vue"""
        if self.frame:
            self.frame.pack(fill="both", expand=True, padx=8, pady=5)
    
    def hide(self):
        """Cache la vue"""
        if self.frame:
            self.frame.pack_forget()