import tkinter as tk
from tkinter import ttk, messagebox
from component.FilterPanel import FilterPanel
from component.Button import StyledButton
from controller.StudentViewController import StudentViewController
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
        self.sort_combo = None
        
        # Conteneurs pour l'affichage
        self.students_container = None
        self.canvas = None  # Ajout pour pouvoir configurer la largeur
        self.status_label = None
        self.toolbar_frame = None
        self.filter_panel = None
        
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
        
        self._create_header()
        self._create_toolbar()
        self._create_filter_panel()
        self._create_main_content()
        self._create_status_bar()
        
        # Chargement initial - Afficher TOUS les élèves au démarrage
        if self.controller:
            try:
                # S'assurer que tous les filtres sont à leurs valeurs par défaut
                self._initialize_default_filters()
                # Charger tous les élèves
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
                self.event_combo.set("Aucun")
            if self.sort_combo:
                self.sort_combo.set("Nom A-Z")
            
            # Initialiser la recherche vide
            self.search_var.set("")
        except Exception as e:
            print(f"Erreur initialisation filtres: {e}")
    
    def _create_header(self):
        """Crée l'en-tête avec titre et indicateur de source"""
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill="x", pady=(0, 10))
        
        title_label = ttk.Label(
            header_frame, 
            text="🎓 Gestion des Élèves", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(side="left")
        
        self.data_source_label = ttk.Label(
            header_frame, 
            text="📄 Données JSON", 
            font=("Arial", 9, "italic"),
            foreground="gray"
        )
        self.data_source_label.pack(side="right")
        
    def _create_toolbar(self):
        """Crée la barre d'outils avec les boutons d'action"""
        self.toolbar_frame = ttk.LabelFrame(self.frame, text="Actions", padding="10")
        self.toolbar_frame.pack(fill="x", pady=(0, 10))
        
        buttons_frame = ttk.Frame(self.toolbar_frame)
        buttons_frame.pack(fill="x")
        
        # Groupe Import/Export
        import_frame = ttk.Frame(buttons_frame)
        import_frame.pack(side="left", fill="x", expand=True)
        
        # Bouton d'import Excel
        import_excel_styled = StyledButton(
            import_frame,
            text="Importer Excel",
            command=self._on_import_excel,
            button_type="primary",
            icon="📊"
        )
        self.import_excel_btn = import_excel_styled.create()
        self.import_excel_btn.pack(side="left", padx=(0, 5))
        
        self.reset_json_btn = None
        
        # Bouton d'actualisation
        refresh_styled = StyledButton(
            import_frame,
            text="Actualiser",
            command=self._on_refresh,
            button_type="info",
            icon="🔄"
        )
        refresh_btn = refresh_styled.create()
        refresh_btn.pack(side="left", padx=(5, 0))
        
        # Groupe Actions
        selection_frame = ttk.Frame(buttons_frame)
        selection_frame.pack(side="right")
        
        select_all_styled = StyledButton(
            selection_frame,
            text="Tout sélectionner",
            command=self._safe_select_all,
            button_type="light",
            icon="☑️"
        )
        select_all_btn = select_all_styled.create()
        select_all_btn.pack(side="left", padx=(0, 5))
        
        deselect_all_styled = StyledButton(
            selection_frame,
            text="Tout désélectionner",
            command=self._safe_deselect_all,
            button_type="light",
            icon="☐"
        )
        deselect_all_btn = deselect_all_styled.create()
        deselect_all_btn.pack(side="left", padx=(0, 10))
        
        assign_event_styled = StyledButton(
            selection_frame,
            text="Assigner événement",
            command=self._safe_assign_to_event,
            button_type="success",
            icon="📅"
        )
        assign_event_btn = assign_event_styled.create()
        assign_event_btn.pack(side="left", padx=(0, 5))
        
        calculate_cost_styled = StyledButton(
            selection_frame,
            text="Calculer coût",
            command=self._safe_calculate_event_cost,
            button_type="warning",
            icon="💰"
        )
        calculate_cost_btn = calculate_cost_styled.create()
        calculate_cost_btn.pack(side="left")
        
    def _update_toolbar_buttons(self):
        """Met à jour les boutons selon la source de données"""
        if self.reset_json_btn:
            self.reset_json_btn.destroy()
            self.reset_json_btn = None
        
        if self.controller and self.controller.is_using_excel_data():
            import_frame = self.toolbar_frame.winfo_children()[0].winfo_children()[0]
            
            reset_styled = StyledButton(
                import_frame,
                text="Données par défaut",
                command=self._on_reset_json,
                button_type="light",
                icon="🔄"
            )
            self.reset_json_btn = reset_styled.create()
            self.reset_json_btn.pack(side="left", padx=(5, 0))
        
        if self.controller and self.controller.is_using_excel_data():
            self.data_source_label.config(text="📊 Données Excel", foreground="blue")
        else:
            self.data_source_label.config(text="📄 Données JSON", foreground="gray")
    
    def _create_filter_panel(self):
        """Crée le panneau de filtres"""
        print("Création du panneau de filtres...")
        
        filter_frame = ttk.LabelFrame(self.frame, text="🔍 Filtres et Recherche", padding="15")
        filter_frame.pack(fill="x", pady=(0, 15))
        
        # Ligne 1: Recherche et tri
        row1 = ttk.Frame(filter_frame)
        row1.pack(fill="x", pady=(0, 10))
        
        # Recherche
        search_frame = ttk.Frame(row1)
        search_frame.pack(side="left", fill="x", expand=True)
        
        ttk.Label(search_frame, text="🔍 Rechercher:", font=("Arial", 9, "bold")).pack(side="left", padx=(0, 5))
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=25, font=("Arial", 9))
        self.search_entry.pack(side="left", padx=(0, 15))
        
        # Tri
        sort_frame = ttk.Frame(row1)
        sort_frame.pack(side="right")
        
        ttk.Label(sort_frame, text="📊 Trier par:", font=("Arial", 9, "bold")).pack(side="left", padx=(0, 5))
        self.sort_combo = ttk.Combobox(
            sort_frame, 
            values=["Nom A-Z", "Nom Z-A", "Classe", "Année"], 
            state="readonly", 
            width=15,
            font=("Arial", 9)
        )
        self.sort_combo.set("Nom A-Z")
        self.sort_combo.pack(side="left")
        
        # Ligne 2: Filtres
        row2 = ttk.Frame(filter_frame)
        row2.pack(fill="x", pady=(5, 0))
        
        left_filters = ttk.Frame(row2)
        left_filters.pack(side="left", fill="x", expand=True)
        
        # Année
        year_frame = ttk.Frame(left_filters)
        year_frame.pack(side="left", padx=(0, 20))
        
        ttk.Label(year_frame, text="📚 Année:", font=("Arial", 9, "bold")).pack(side="top", anchor="w")
        self.year_combo = ttk.Combobox(
            year_frame, 
            values=["Toutes", "1ère", "2ème", "3ème", "4ème", "5ème", "6ème"], 
            state="readonly", 
            width=12,
            font=("Arial", 9)
        )
        self.year_combo.set("Toutes")
        self.year_combo.pack(side="top")
        
        # Classe
        class_frame = ttk.Frame(left_filters)
        class_frame.pack(side="left", padx=(0, 20))
        
        ttk.Label(class_frame, text="🏫 Classe:", font=("Arial", 9, "bold")).pack(side="top", anchor="w")
        self.class_combo = ttk.Combobox(
            class_frame, 
            values=["Toutes", "1A", "1B", "2A", "2B", "3A", "3B", "3C", "4A", "4B", "5A", "5B", "5C", "6A", "6B", "6C"], 
            state="readonly", 
            width=12,
            font=("Arial", 9)
        )
        self.class_combo.set("Toutes")
        self.class_combo.pack(side="top")
        
        # Événement
        event_frame = ttk.Frame(left_filters)
        event_frame.pack(side="left", padx=(0, 20))
        
        ttk.Label(event_frame, text="📅 Événement:", font=("Arial", 9, "bold")).pack(side="top", anchor="w")
        self.event_combo = ttk.Combobox(
            event_frame, 
            values=["Aucun", "Sortie Théâtre", "Visite Musée", "Concert", "Voyage Paris"], 
            state="readonly", 
            width=15,
            font=("Arial", 9)
        )
        self.event_combo.set("Aucun")
        self.event_combo.pack(side="top")
        
        # Boutons d'action
        actions_frame = ttk.Frame(row2)
        actions_frame.pack(side="right", padx=(20, 0))
        
        reset_styled = StyledButton(
            actions_frame,
            text="Reset Filtres",
            command=self._safe_reset_filters,
            button_type="light",
            icon="🔄"
        )
        reset_btn = reset_styled.create()
        reset_btn.pack(pady=(0, 5))
        
        export_styled = StyledButton(
            actions_frame,
            text="Exporter",
            command=self._safe_export_data,
            button_type="info",
            icon="📤"
        )
        export_btn = export_styled.create()
        export_btn.pack()
        
        self._setup_filter_bindings()
        self.filter_panel = filter_frame
        print("Panneau de filtres créé avec succès!")
    
    def _setup_filter_bindings(self):
        """Configure les bindings pour les filtres"""
        try:
            self.search_var.trace('w', self._safe_on_search_changed)
            
            if self.year_combo:
                self.year_combo.bind('<<ComboboxSelected>>', self._safe_on_year_changed)
            if self.class_combo:
                self.class_combo.bind('<<ComboboxSelected>>', self._safe_on_filter_changed)
            if self.event_combo:
                self.event_combo.bind('<<ComboboxSelected>>', self._safe_on_event_changed)
            if self.sort_combo:
                self.sort_combo.bind('<<ComboboxSelected>>', self._safe_on_sort_changed)
                
            self._setup_search_placeholder()
            
        except Exception as e:
            print(f"Erreur lors de la configuration des bindings: {e}")
    
    def _setup_search_placeholder(self):
        """Configure le placeholder pour la recherche"""
        placeholder_text = "Rechercher par nom ou prénom..."
        
        def on_focus_in(event):
            if self.search_entry.get() == placeholder_text:
                self.search_entry.delete(0, tk.END)
                self.search_entry.config(foreground='black')
        
        def on_focus_out(event):
            if not self.search_entry.get():
                self.search_entry.insert(0, placeholder_text)
                self.search_entry.config(foreground='gray')
        
        self.search_entry.insert(0, placeholder_text)
        self.search_entry.config(foreground='gray')
        
        self.search_entry.bind('<FocusIn>', on_focus_in)
        self.search_entry.bind('<FocusOut>', on_focus_out)
    
    def _create_main_content(self):
        """Crée la zone principale d'affichage des élèves"""
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Canvas avec configuration pour largeur complète
        self.canvas = tk.Canvas(main_frame, bg="#f8f9fa", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        
        self.students_container = ttk.Frame(self.canvas)
        
        # Configuration pour s'adapter à la largeur du canvas
        def configure_canvas_width(event=None):
            canvas_width = self.canvas.winfo_width()
            self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        
        def configure_scroll_region(event=None):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        # Créer la fenêtre dans le canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.students_container, anchor="nw")
        
        # Bindings pour adapter la largeur
        self.canvas.bind('<Configure>', configure_canvas_width)
        self.students_container.bind('<Configure>', configure_scroll_region)
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.canvas.bind("<MouseWheel>", _on_mousewheel)
    
    def _create_status_bar(self):
        """Crée la barre de statut"""
        status_frame = ttk.Frame(self.frame)
        status_frame.pack(fill="x", side="bottom")
        
        self.status_label = ttk.Label(
            status_frame,
            text="Prêt - Chargement des données...",
            relief="sunken",
            padding="5",
            font=("Arial", 9)
        )
        self.status_label.pack(side="left", fill="x", expand=True)
    
    def update_display(self):
        """Met à jour l'affichage des élèves"""
        print("DEBUG: Début de update_display()")
        
        if not self.controller:
            print("DEBUG: Contrôleur non initialisé!")
            self.status_label.config(text="Erreur: Contrôleur non initialisé")
            return
        
        print("DEBUG: Nettoyage des widgets existants...")
        for widget in self.students_container.winfo_children():
            widget.destroy()
        
        try:
            filtered_students = self.controller.get_filtered_students()
            selected_students = self.controller.get_selected_students()
            print(f"DEBUG: Récupéré {len(filtered_students)} élèves filtrés")
            print(f"DEBUG: Récupéré {len(selected_students)} élèves sélectionnés")
        except Exception as e:
            print(f"DEBUG: Erreur récupération données: {e}")
            filtered_students = []
            selected_students = []
        
        if not filtered_students:
            print("DEBUG: Aucun élève filtré - affichage message vide")
            no_data_frame = ttk.Frame(self.students_container)
            no_data_frame.pack(fill="both", expand=True, pady=50)
            
            no_data_label = ttk.Label(
                no_data_frame,
                text="🔍 Aucun élève ne correspond aux critères de filtrage",
                font=("Arial", 14),
                foreground="#6c757d"
            )
            no_data_label.pack(expand=True)
        else:
            print(f"DEBUG: Création de {len(filtered_students)} cartes d'élèves")
            for i, student in enumerate(filtered_students):
                if i < 5:  # Log seulement les 5 premiers pour éviter le spam
                    print(f"DEBUG: Création carte {i+1} pour {student.get('prenom', 'Unknown')} {student.get('nom', 'Unknown')}")
                try:
                    is_selected = student["id"] in selected_students
                    card = self._create_full_width_student_row(
                        self.students_container,
                        student,
                        is_selected
                    )
                    # CORRECTION CRUCIALE: utiliser sticky="ew" pour étendre horizontalement
                    card.pack(fill="x", padx=0, pady=1, expand=True)
                    if i < 5:
                        print(f"DEBUG: Carte {i+1} créée et packée avec succès")
                except Exception as e:
                    print(f"DEBUG: Erreur création carte {i+1}: {e}")
                    import traceback
                    traceback.print_exc()
        
        print("DEBUG: Mise à jour du statut...")
        # Mettre à jour le statut
        try:
            total_students = len(self.controller.get_students_data())
            filtered_count = len(filtered_students)
            selected_count = len(selected_students)
            
            status_text = f"📊 Total: {total_students} élèves"
            if filtered_count != total_students:
                status_text += f" | ✅ Affichés: {filtered_count}"
            if selected_count > 0:
                status_text += f" | ☑️ Sélectionnés: {selected_count}"
            
            source = "Excel" if self.controller.is_using_excel_data() else "JSON"
            status_text += f" | 📁 Source: {source}"
            
            self.status_label.config(text=status_text)
            print(f"DEBUG: Statut mis à jour: {status_text}")
        except Exception as e:
            print(f"DEBUG: Erreur mise à jour statut: {e}")
            self.status_label.config(text=f"❌ Erreur de statut: {e}")
        
        self._update_toolbar_buttons()
        print("DEBUG: Fin de update_display()")
        
        # Forcer la mise à jour de la largeur après ajout des widgets
        self.root.after(10, self._update_canvas_width)
    
    def _update_canvas_width(self):
        """Force la mise à jour de la largeur du canvas"""
        try:
            if hasattr(self, 'canvas') and hasattr(self, 'canvas_window'):
                canvas_width = self.canvas.winfo_width()
                if canvas_width > 1:  # S'assurer que le canvas est bien dimensionné
                    self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        except Exception as e:
            print(f"Erreur mise à jour largeur canvas: {e}")
    
    def _create_full_width_student_row(self, parent, student, is_selected):
        """Crée une ligne d'élève qui prend VRAIMENT toute la largeur"""
        
        # Frame principale qui s'étend sur toute la largeur
        main_frame = ttk.Frame(parent, padding="4")
        if is_selected:
            main_frame.configure(relief="solid", borderwidth=2)
        else:
            main_frame.configure(relief="ridge", borderwidth=1)
        
        # ========== LIGNE PRINCIPALE avec Grid pour plus de contrôle ==========
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True)
        
        # Configuration des colonnes pour qu'elles s'étendent
        content_frame.grid_columnconfigure(0, weight=0, minsize=40)   # Checkbox
        content_frame.grid_columnconfigure(1, weight=2, minsize=180)  # Nom
        content_frame.grid_columnconfigure(2, weight=1, minsize=80)   # Classe
        content_frame.grid_columnconfigure(3, weight=1, minsize=70)   # Année
        content_frame.grid_columnconfigure(4, weight=3, minsize=200)  # Email/Info
        content_frame.grid_columnconfigure(5, weight=1, minsize=100)  # Événements
        content_frame.grid_columnconfigure(6, weight=0, minsize=240)  # Boutons
        
        # ========== CHECKBOX ==========
        var = tk.BooleanVar(value=is_selected)
        checkbox = ttk.Checkbutton(
            content_frame,
            variable=var,
            command=lambda: self._safe_toggle_student_selection(student["id"])
        )
        checkbox.grid(row=0, column=0, sticky="w", padx=(5, 10))
        
        # ========== NOM ET PRÉNOM ==========
        name_text = f"👤 {student['prenom']} {student['nom'].upper()}"
        if is_selected:
            name_text += " ✓"
            
        name_label = ttk.Label(
            content_frame,
            text=name_text,
            font=("Arial", 10, "bold"),
            foreground="#2c3e50" if not is_selected else "#1565c0"
        )
        name_label.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        
        # ========== CLASSE ==========
        class_label = ttk.Label(
            content_frame,
            text=f"🏫 {student['classe']}",
            font=("Arial", 9, "bold"),
            foreground="#495057"
        )
        class_label.grid(row=0, column=2, sticky="ew", padx=(0, 10))
        
        # ========== ANNÉE ==========
        if 'annee' in student:
            year_text = f"📚 {student['annee']}ème"
        else:
            classe = student.get("classe", "")
            year = ''.join(filter(str.isdigit, classe))
            year_text = f"📚 {year}ème" if year else "📚 N/A"
        
        year_label = ttk.Label(
            content_frame,
            text=year_text,
            font=("Arial", 9),
            foreground="#6c757d"
        )
        year_label.grid(row=0, column=3, sticky="ew", padx=(0, 10))
        
        # ========== EMAIL ET INFORMATIONS ==========
        info_frame = ttk.Frame(content_frame)
        info_frame.grid(row=0, column=4, sticky="ew", padx=(0, 10))
        
        if 'email' in student and student['email'] and student['email'] != 'nan':
            email_text = student['email']
            if len(email_text) > 35:
                email_text = email_text[:32] + "..."
                
            email_label = ttk.Label(
                info_frame,
                text=f"📧 {email_text}",
                font=("Arial", 8),
                foreground="#6c757d"
            )
            email_label.pack(anchor="w")
        
        # Source des données
        if 'source' in student and student['source'] == 'excel':
            source_text = "📊 Excel"
            source_color = "#007bff"
        else:
            source_text = "📄 JSON"
            source_color = "#6c757d"
            
        source_label = ttk.Label(
            info_frame,
            text=source_text,
            font=("Arial", 7, "italic"),
            foreground=source_color
        )
        source_label.pack(anchor="w")
        
        # ========== ÉVÉNEMENTS ==========
        events_label = ttk.Label(
            content_frame,
            text="📅 Aucun",
            font=("Arial", 8),
            foreground="#6c757d"
        )
        events_label.grid(row=0, column=5, sticky="ew", padx=(0, 15))
        
        # ========== BOUTONS D'ACTION ==========
        buttons_frame = ttk.Frame(content_frame)
        buttons_frame.grid(row=0, column=6, sticky="e")
        
        # Boutons compacts
        view_btn = ttk.Button(
            buttons_frame,
            text="👁️ Voir",
            width=8,
            command=lambda: self._safe_view_student(student["id"])
        )
        view_btn.pack(side="left", padx=(0, 2))
        
        edit_btn = ttk.Button(
            buttons_frame,
            text="✏️ Éditer",
            width=8,
            command=lambda: self._safe_edit_student(student["id"])
        )
        edit_btn.pack(side="left", padx=(0, 2))
        
        delete_btn = ttk.Button(
            buttons_frame,
            text="🗑️ Suppr.",
            width=9,
            command=lambda: self._safe_delete_student(student["id"])
        )
        delete_btn.pack(side="left")
        
        return main_frame
    
    def refresh_view(self):
        """Rafraîchit complètement la vue"""
        if self.controller:
            try:
                self.controller.apply_all_filters()
                self.update_display()
                print("Vue rafraîchie avec succès")
            except Exception as e:
                print(f"Erreur refresh: {e}")
                self.status_label.config(text=f"❌ Erreur refresh: {e}")
    
    # ====================== MÉTHODES SAFE ======================
    def _safe_select_all(self):
        if self.controller:
            try:
                self.controller.select_all()
                messagebox.showinfo("✅ Sélection", "Tous les élèves ont été sélectionnés")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur sélection: {e}")
    
    def _safe_deselect_all(self):
        if self.controller:
            try:
                self.controller.deselect_all()
                messagebox.showinfo("☐ Désélection", "Tous les élèves ont été désélectionnés")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur désélection: {e}")
    
    def _safe_assign_to_event(self):
        if self.controller:
            try:
                selected_count = len(self.controller.get_selected_students())
                if selected_count == 0:
                    messagebox.showwarning("⚠️ Attention", "Aucun élève sélectionné pour l'assignation d'événement")
                    return
                self.controller.assign_to_event()
            except Exception as e:
                selected_count = len(self.controller.get_selected_students()) if self.controller else 0
                messagebox.showinfo("📅 Info", f"Assignation d'événement pour {selected_count} élèves (fonctionnalité à développer)")
    
    def _safe_calculate_event_cost(self):
        if self.controller:
            try:
                selected_count = len(self.controller.get_selected_students())
                if selected_count == 0:
                    messagebox.showwarning("⚠️ Attention", "Aucun élève sélectionné pour le calcul de coût")
                    return
                self.controller.calculate_event_cost()
            except Exception as e:
                selected_count = len(self.controller.get_selected_students()) if self.controller else 0
                messagebox.showinfo("💰 Info", f"Calcul de coût pour {selected_count} élèves (fonctionnalité à développer)")
    
    def _safe_toggle_student_selection(self, student_id):
        if self.controller:
            try:
                self.controller.toggle_student_selection(student_id)
                self.update_display()
            except Exception as e:
                print(f"Erreur toggle sélection: {e}")
    
    def _safe_view_student(self, student_id):
        if self.controller:
            try:
                self.controller.view_student(student_id)
            except Exception as e:
                messagebox.showinfo("👁️ Voir Élève", f"Affichage des détails pour l'élève ID: {student_id}\n\n(Fonctionnalité à développer)")
    
    def _safe_edit_student(self, student_id):
        if self.controller:
            try:
                self.controller.edit_student(student_id)
            except Exception as e:
                messagebox.showinfo("✏️ Éditer Élève", f"Édition de l'élève ID: {student_id}\n\n(Fonctionnalité à développer)")
    
    def _safe_delete_student(self, student_id):
        if self.controller:
            try:
                result = messagebox.askyesno(
                    "🗑️ Confirmation de suppression", 
                    f"⚠️ Êtes-vous sûr de vouloir supprimer cet élève ?\n\n"
                    f"ID: {student_id}\n\n"
                    f"Cette action est irréversible !"
                )
                if result:
                    self.controller.delete_student(student_id)
            except Exception as e:
                messagebox.showinfo("🗑️ Suppression", f"Suppression de l'élève ID: {student_id}\n\n(Fonctionnalité à développer)")
    
    def _safe_export_data(self):
        """Export des données filtrées"""
        if self.controller:
            try:
                filtered_count = len(self.controller.get_filtered_students())
                messagebox.showinfo("📤 Export", f"Export de {filtered_count} élèves\n\n(Fonctionnalité à développer)")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur export: {e}")
    
    def _safe_on_search_changed(self, *args):
        if self.controller and self.search_entry:
            try:
                current_text = self.search_var.get()
                if current_text == "Rechercher par nom ou prénom...":
                    return
                self.controller.on_search_changed(*args)
            except Exception as e:
                print(f"Erreur recherche: {e}")
    
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
    
    def _safe_on_event_changed(self, event=None):
        if self.controller:
            try:
                self.controller.on_event_changed(event)
            except Exception as e:
                print(f"Erreur changement événement: {e}")
    
    def _safe_on_sort_changed(self, event=None):
        if self.controller:
            try:
                self.controller.on_sort_changed(event)
            except Exception as e:
                print(f"Erreur changement tri: {e}")
    
    def _safe_reset_filters(self):
        if self.controller:
            try:
                self._initialize_default_filters()
                self.controller.reset_filters()
                messagebox.showinfo("🔄 Reset", "Tous les filtres ont été remis à zéro")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur reset filtres: {e}")
    
    # ====================== CALLBACKS ======================
    def _on_import_excel(self):
        if self.controller:
            try:
                self.controller.import_excel_students()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur import Excel: {e}")
    
    def _on_reset_json(self):
        if self.controller:
            try:
                self.controller.reset_to_json_data()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur reset JSON: {e}")
        
    def _on_refresh(self):
        if self.controller:
            try:
                self.controller.refresh_data()
                self.refresh_view()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur actualisation: {e}")
    
    def show(self):
        """Affiche la vue"""
        if self.frame:
            self.frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    def hide(self):
        """Cache la vue"""
        if self.frame:
            self.frame.pack_forget()


# Classe d'alias pour maintenir la compatibilité
class StudentsView(StudentView):
    """Alias pour maintenir la compatibilité avec l'ancien nom"""
    pass