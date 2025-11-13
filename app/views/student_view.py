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
        self.treeview = None  # Remplace students_container
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
        """Crée la zone principale avec un Treeview (solution native)"""
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # ========== TREEVIEW AVEC SCROLLBARS ==========
        # Définir les colonnes
        columns = ("selection", "nom", "classe", "annee", "email", "source", "evenements", "actions")
        
        self.treeview = ttk.Treeview(
            main_frame,
            columns=columns,
            show="tree headings",  # Afficher l'arbre + en-têtes
            height=15,
            selectmode="extended"  # Sélection multiple
        )
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.treeview.yview)
        h_scrollbar = ttk.Scrollbar(main_frame, orient="horizontal", command=self.treeview.xview)
        
        self.treeview.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Configuration des colonnes
        self.treeview.column("#0", width=30, minwidth=30, stretch=False)  # Icône arbre
        self.treeview.column("selection", width=50, minwidth=50, stretch=False, anchor="center")
        self.treeview.column("nom", width=200, minwidth=150, stretch=True)
        self.treeview.column("classe", width=80, minwidth=60, stretch=False)
        self.treeview.column("annee", width=80, minwidth=60, stretch=False)
        self.treeview.column("email", width=250, minwidth=150, stretch=True)
        self.treeview.column("source", width=80, minwidth=60, stretch=False)
        self.treeview.column("evenements", width=120, minwidth=100, stretch=False)
        self.treeview.column("actions", width=200, minwidth=180, stretch=False)
        
        # En-têtes des colonnes
        self.treeview.heading("#0", text="", anchor="w")
        self.treeview.heading("selection", text="☑️", anchor="center")
        self.treeview.heading("nom", text="👤 Nom et Prénom", anchor="w")
        self.treeview.heading("classe", text="🏫 Classe", anchor="center")
        self.treeview.heading("annee", text="📚 Année", anchor="center")
        self.treeview.heading("email", text="📧 Email", anchor="w")
        self.treeview.heading("source", text="📊 Source", anchor="center")
        self.treeview.heading("evenements", text="📅 Événements", anchor="center")
        self.treeview.heading("actions", text="⚙️ Actions", anchor="center")
        
        # Style pour les lignes alternées
        self.treeview.tag_configure("selected", background="#e3f2fd")
        self.treeview.tag_configure("odd", background="#f8f9fa")
        self.treeview.tag_configure("even", background="white")
        
        # Placement des widgets
        self.treeview.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configuration du grid
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Bindings pour les actions
        self.treeview.bind("<Double-1>", self._on_treeview_double_click)
        self.treeview.bind("<Button-3>", self._on_treeview_right_click)  # Menu contextuel
        self.treeview.bind("<<TreeviewSelect>>", self._on_treeview_select)
        
        # Navigation clavier native déjà disponible ! 🎉
        # Up/Down, Page Up/Down, Home/End, etc. fonctionnent automatiquement
    
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
        """Met à jour l'affichage des élèves dans le Treeview"""
        print("DEBUG: Début de update_display() avec Treeview")
        
        if not self.controller:
            print("DEBUG: Contrôleur non initialisé!")
            self.status_label.config(text="Erreur: Contrôleur non initialisé")
            return
        
        # Vider le treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        try:
            filtered_students = self.controller.get_filtered_students()
            selected_students = self.controller.get_selected_students()
            print(f"DEBUG: Récupéré {len(filtered_students)} élèves filtrés")
        except Exception as e:
            print(f"DEBUG: Erreur récupération données: {e}")
            filtered_students = []
            selected_students = []
        
        if not filtered_students:
            # Ajouter une ligne indiquant qu'il n'y a pas de données
            self.treeview.insert("", "end", text="", values=(
                "", "🔍 Aucun élève ne correspond aux critères", "", "", "", "", "", ""
            ))
        else:
            for i, student in enumerate(filtered_students):
                try:
                    is_selected = student["id"] in selected_students
                    
                    # Calcul de l'année
                    if 'annee' in student:
                        year_text = f"{student['annee']}ème"
                    else:
                        classe = student.get("classe", "")
                        year = ''.join(filter(str.isdigit, classe))
                        year_text = f"{year}ème" if year else "N/A"
                    
                    # Email
                    email_text = ""
                    if 'email' in student and student['email'] and student['email'] != 'nan':
                        email_text = student['email']
                        if len(email_text) > 35:
                            email_text = email_text[:32] + "..."
                    
                    # Source
                    source_text = "📊 Excel" if student.get('source') == 'excel' else "📄 JSON"
                    
                    # Nom complet
                    nom_complet = f"{student['prenom']} {student['nom'].upper()}"
                    if is_selected:
                        nom_complet += " ✓"
                    
                    # Sélection
                    selection_text = "☑️" if is_selected else "☐"
                    
                    # Actions (on mettra des boutons plus tard)
                    actions_text = "👁️ Voir | 🗑️ Supprimer"
                    
                    # Insérer la ligne
                    item_id = self.treeview.insert("", "end", 
                        text="👤",  # Icône dans la première colonne
                        values=(
                            selection_text,
                            nom_complet,
                            student['classe'],
                            year_text,
                            email_text,
                            source_text,
                            "📅 Aucun",
                            actions_text
                        ),
                        tags=("selected" if is_selected else ("odd" if i % 2 else "even"),)
                    )
                    
                    # Stocker l'ID de l'étudiant pour référence
                    self.treeview.set(item_id, "student_id", student["id"])
                    
                except Exception as e:
                    print(f"DEBUG: Erreur création ligne {i+1}: {e}")
        
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
        except Exception as e:
            self.status_label.config(text=f"❌ Erreur de statut: {e}")
        
        self._update_toolbar_buttons()
        print("DEBUG: Fin de update_display() avec Treeview")
    
    # ========== ÉVÉNEMENTS TREEVIEW ==========
    def _on_treeview_double_click(self, event):
        """Double-clic sur une ligne du treeview"""
        item = self.treeview.selection()[0] if self.treeview.selection() else None
        if item:
            try:
                student_id = self.treeview.set(item, "student_id")
                if student_id:
                    self._safe_view_student(student_id)
            except:
                pass
    
    def _on_treeview_right_click(self, event):
        """Clic droit sur une ligne du treeview - Menu contextuel"""
        item = self.treeview.identify_row(event.y)
        if item:
            self.treeview.selection_set(item)
            
            # Créer le menu contextuel
            context_menu = tk.Menu(self.root, tearoff=0)
            context_menu.add_command(label="👁️ Voir détails", command=lambda: self._context_view_student(item))
            context_menu.add_separator()
            context_menu.add_command(label="☑️ Sélectionner", command=lambda: self._context_toggle_selection(item))
            context_menu.add_separator()
            context_menu.add_command(label="🗑️ Supprimer", command=lambda: self._context_delete_student(item))
            
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
    
    def _on_treeview_select(self, event):
        """Sélection d'une ligne dans le treeview"""
        # Ici on peut gérer la sélection si nécessaire
        pass
    
    def _context_view_student(self, item):
        """Voir un étudiant depuis le menu contextuel"""
        try:
            student_id = self.treeview.set(item, "student_id")
            if student_id:
                self._safe_view_student(student_id)
        except:
            pass
    
    def _context_toggle_selection(self, item):
        """Toggle sélection depuis le menu contextuel"""
        try:
            student_id = self.treeview.set(item, "student_id")
            if student_id:
                self._safe_toggle_student_selection(student_id)
        except:
            pass
    
    def _context_delete_student(self, item):
        """Supprimer un étudiant depuis le menu contextuel"""
        try:
            student_id = self.treeview.set(item, "student_id")
            if student_id:
                self._safe_delete_student(student_id)
        except:
            pass
    
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