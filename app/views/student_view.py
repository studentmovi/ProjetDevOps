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
        self.month_combo = None
        self.sort_combo = None
        
        # Conteneurs pour l'affichage
        self.treeview = None
        self.status_label = None
        self.toolbar_frame = None
        self.filter_panel = None
        
        # Données des événements par mois
        self.events_by_month = {
            "Tous": "Tous les mois",
            "Septembre": ["Sortie Théâtre", "Concert"],
            "Octobre": ["Visite Musée"],
            "Novembre": ["Sortie Théâtre"],
            "Décembre": ["Concert"],
            "Janvier": ["Voyage Paris"],
            "Février": ["Visite Musée"],
            "Mars": ["Sortie Théâtre", "Concert"],
            "Avril": ["Voyage Paris"],
            "Mai": ["Visite Musée", "Concert"],
            "Juin": ["Sortie Théâtre"]
        }
        
    def create_widgets(self):
        """Méthode appelée par main.py pour créer les widgets"""
        self.create_view()
    
    def create_view(self):
        """Crée l'interface principale de la vue élèves"""
        if self.frame:
            self.frame.destroy()
        
        self.frame = ttk.Frame(self.root)
        
        # CORRECTION : Ne pas utiliser configure(bg=...) sur root ici
        # self.root.configure(bg=self.styles.colors['off_white'])  # ❌ SUPPRIMÉ
        
        # Initialiser le contrôleur avec cette vue
        self.controller = StudentViewController(self)
        
        self._create_header()
        self._create_toolbar()
        self._create_compact_filter_panel()
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
    
    def _create_header(self):
        """Crée l'en-tête avec le nouveau style bleu"""
        header_frame = self.styles.create_header_frame(self.frame, padding="15")
        header_frame.pack(fill="x", pady=(0, 10))
        
        title_label = ttk.Label(
            header_frame, 
            text="🎓 Gestion des Élèves", 
            style="Header.TLabel"
        )
        title_label.pack(side="left")
        
        self.data_source_label = ttk.Label(
            header_frame, 
            text="📄 Données JSON", 
            style="Header.TLabel"
        )
        self.data_source_label.pack(side="right")
        
    def _create_toolbar(self):
        """Crée la barre d'outils avec le nouveau style"""
        self.toolbar_frame = ttk.LabelFrame(
            self.frame, 
            text="⚙️ Actions Rapides", 
            style="Compact.TLabelframe",
            padding="8"
        )
        self.toolbar_frame.pack(fill="x", pady=(0, 8))
        
        buttons_frame = ttk.Frame(self.toolbar_frame)
        buttons_frame.pack(fill="x")
        
        # Groupe Import/Export à gauche
        import_frame = ttk.Frame(buttons_frame)
        import_frame.pack(side="left", fill="x", expand=True)
        
        import_excel_btn = ttk.Button(
            import_frame,
            text="📊 Importer Excel",
            command=self._on_import_excel,
            style="Primary.TButton"
        )
        import_excel_btn.pack(side="left", padx=(0, 5))
        
        refresh_btn = ttk.Button(
            import_frame,
            text="🔄 Actualiser",
            command=self._on_refresh,
            style="Secondary.TButton"
        )
        refresh_btn.pack(side="left", padx=(5, 0))
        
        # Groupe Actions à droite
        selection_frame = ttk.Frame(buttons_frame)
        selection_frame.pack(side="right")
        
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
        deselect_all_btn.pack(side="left", padx=(0, 8))
        
        assign_event_btn = ttk.Button(
            selection_frame,
            text="📅 Assigner événement",
            command=self._safe_assign_to_event,
            style="Success.TButton"
        )
        assign_event_btn.pack(side="left", padx=(0, 5))
        
        calculate_cost_btn = ttk.Button(
            selection_frame,
            text="💰 Calculer coût",
            command=self._safe_calculate_event_cost,
            style="Warning.TButton"
        )
        calculate_cost_btn.pack(side="left")
    
    def _create_compact_filter_panel(self):
        """Crée un panneau de filtres COMPACT avec événements et mois"""
        filter_frame = ttk.LabelFrame(
            self.frame, 
            text="🔍 Filtres", 
            style="Compact.TLabelframe",
            padding="8"
        )
        filter_frame.pack(fill="x", pady=(0, 8))
        
        # LIGNE 1: RECHERCHE + TRI (horizontal)
        row1 = ttk.Frame(filter_frame)
        row1.pack(fill="x", pady=(0, 6))
        
        # Recherche
        search_frame = ttk.Frame(row1)
        search_frame.pack(side="left", fill="x", expand=True)
        
        ttk.Label(search_frame, text="🔍", font=("Arial", 10)).pack(side="left", padx=(0, 3))
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20, font=("Arial", 9))
        self.search_entry.pack(side="left", padx=(0, 10))
        
        # Tri
        sort_frame = ttk.Frame(row1)
        sort_frame.pack(side="right")
        

        
        ttk.Label(sort_frame, text="Tri", font=("Arial", 10)).pack(side="left", padx=(0, 3))
        self.sort_combo = ttk.Combobox(
            sort_frame, 
            values=["Nom A-Z", "Nom Z-A", "Classe", "Année"], 
            state="readonly", 
            width=12,
            font=("Arial", 9)
        )
        self.sort_combo.set("Nom A-Z")
        self.sort_combo.pack(side="left")
        
        # LIGNE 2: FILTRES PRINCIPAUX
        row2 = ttk.Frame(filter_frame)
        row2.pack(fill="x", pady=(3, 0))
        
        filters_container = ttk.Frame(row2)
        filters_container.pack(side="left", fill="x", expand=True)
        
        # Année
        year_frame = ttk.Frame(filters_container)
        year_frame.pack(side="left", padx=(0, 12))
        
        ttk.Label(year_frame, text="Année", font=("Arial", 9)).pack(side="left", padx=(0, 2))
        self.year_combo = ttk.Combobox(
            year_frame, 
            values=["Toutes", "1ère", "2ème", "3ème", "4ème", "5ème", "6ème"], 
            state="readonly", 
            width=8,
            font=("Arial", 9)
        )
        self.year_combo.set("Toutes")
        self.year_combo.pack(side="left")
        
        # Classe
        class_frame = ttk.Frame(filters_container)
        class_frame.pack(side="left", padx=(0, 12))
        
        ttk.Label(class_frame, text="Classe", font=("Arial", 9)).pack(side="left", padx=(0, 2))
        self.class_combo = ttk.Combobox(
            class_frame, 
            values=["Toutes", "1A", "1B", "2A", "2B", "3A", "3B", "3C", "4A", "4B", "5A", "5B", "5C", "6A", "6B", "6C"], 
            state="readonly", 
            width=8,
            font=("Arial", 9)
        )
        self.class_combo.set("Toutes")
        self.class_combo.pack(side="left")
        
        # Mois
        month_frame = ttk.Frame(filters_container)
        month_frame.pack(side="left", padx=(0, 12))
        
        ttk.Label(month_frame, text="Mois", font=("Arial", 9)).pack(side="left", padx=(0, 2))
        self.month_combo = ttk.Combobox(
            month_frame, 
            values=["Tous", "Septembre", "Octobre", "Novembre", "Décembre", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin"], 
            state="readonly", 
            width=10,
            font=("Arial", 9)
        )
        self.month_combo.set("Tous")
        self.month_combo.pack(side="left")
        
        # Événement
        event_frame = ttk.Frame(filters_container)
        event_frame.pack(side="left", padx=(0, 12))
        
        ttk.Label(event_frame, text="Événements", font=("Arial", 9)).pack(side="left", padx=(0, 2))
        self.event_combo = ttk.Combobox(
            event_frame, 
            values=["Tous", "Sortie Théâtre", "Visite Musée", "Concert", "Voyage Paris"], 
            state="readonly", 
            width=12,
            font=("Arial", 9)
        )
        self.event_combo.set("Tous")
        self.event_combo.pack(side="left")
        
        # Boutons d'action
        actions_frame = ttk.Frame(row2)
        actions_frame.pack(side="right", padx=(10, 0))
        
        reset_btn = ttk.Button(
            actions_frame,
            text="🔄 Reset",
            command=self._safe_reset_filters,
            style="Light.TButton",
            width=8
        )
        reset_btn.pack(side="left", padx=(0, 5))
        
        export_btn = ttk.Button(
            actions_frame,
            text="📤 Export",
            command=self._safe_export_data,
            style="Secondary.TButton",
            width=8
        )
        export_btn.pack(side="left")
        
        self._setup_filter_bindings()
        self.filter_panel = filter_frame
    
    def _setup_filter_bindings(self):
        """Configure les bindings pour les filtres"""
        try:
            self.search_var.trace('w', self._safe_on_search_changed)
            
            if self.year_combo:
                self.year_combo.bind('<<ComboboxSelected>>', self._safe_on_year_changed)
            if self.class_combo:
                self.class_combo.bind('<<ComboboxSelected>>', self._safe_on_filter_changed)
            if self.month_combo:
                self.month_combo.bind('<<ComboboxSelected>>', self._safe_on_month_changed)
            if self.event_combo:
                self.event_combo.bind('<<ComboboxSelected>>', self._safe_on_event_changed)
            if self.sort_combo:
                self.sort_combo.bind('<<ComboboxSelected>>', self._safe_on_sort_changed)
                
            self._setup_search_placeholder()
            
        except Exception as e:
            print(f"Erreur bindings: {e}")
    
    def _safe_on_month_changed(self, event=None):
        """Gestion du changement de mois - met à jour les événements"""
        try:
            selected_month = self.month_combo.get()
            
            if selected_month == "Tous":
                events = ["Tous", "Sortie Théâtre", "Visite Musée", "Concert", "Voyage Paris"]
            else:
                events = ["Tous"] + self.events_by_month.get(selected_month, [])
            
            current_event = self.event_combo.get()
            self.event_combo.configure(values=events)
            
            if current_event not in events:
                self.event_combo.set("Tous")
            
            if self.controller:
                self.controller.on_month_changed(event)
                
        except Exception as e:
            print(f"Erreur changement mois: {e}")
    
    def _setup_search_placeholder(self):
        """Configure le placeholder pour la recherche"""
        placeholder_text = "Nom, prénom..."
        
        def on_focus_in(event):
            if self.search_entry.get() == placeholder_text:
                self.search_entry.delete(0, tk.END)
                # CORRECTION : Utiliser les couleurs des styles
                # self.search_entry.config(foreground=self.styles.colors['text_gray'])  # Pas besoin
        
        def on_focus_out(event):
            if not self.search_entry.get():
                self.search_entry.insert(0, placeholder_text)
                # CORRECTION : Pas de config foreground direct
                # self.search_entry.config(foreground=self.styles.colors['medium_gray'])
        
        self.search_entry.insert(0, placeholder_text)
        # self.search_entry.config(foreground=self.styles.colors['medium_gray'])  # SUPPRIMÉ
        
        self.search_entry.bind('<FocusIn>', on_focus_in)
        self.search_entry.bind('<FocusOut>', on_focus_out)
    
    def _create_main_content(self):
        """Crée la zone principale avec Treeview"""
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill="both", expand=True, pady=(0, 8))
        
        columns = ("selection", "nom", "classe", "annee", "source", "evenements", "actions")
        
        self.treeview = ttk.Treeview(
            main_frame,
            columns=columns,
            show="tree headings",
            height=12,
            selectmode="extended"
        )
        
        v_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.treeview.yview)
        h_scrollbar = ttk.Scrollbar(main_frame, orient="horizontal", command=self.treeview.xview)
        
        self.treeview.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Configuration des colonnes
        self.treeview.column("#0", width=25, minwidth=25, stretch=False)
        self.treeview.column("selection", width=40, minwidth=40, stretch=False, anchor="center")
        self.treeview.column("nom", width=180, minwidth=120, stretch=True)
        self.treeview.column("classe", width=70, minwidth=60, stretch=False)
        self.treeview.column("annee", width=70, minwidth=60, stretch=False)
        self.treeview.column("email", width=200, minwidth=120, stretch=True)
        self.treeview.column("source", width=70, minwidth=60, stretch=False)
        self.treeview.column("evenements", width=110, minwidth=90, stretch=False)
        self.treeview.column("actions", width=160, minwidth=140, stretch=False)
        
        # En-têtes
        self.treeview.heading("#0", text="", anchor="w")
        self.treeview.heading("selection", text="☑️", anchor="center")
        self.treeview.heading("nom", text="👤 Nom", anchor="w")
        self.treeview.heading("classe", text="🏫 Classe", anchor="center")
        self.treeview.heading("annee", text="📚 Année", anchor="center")
        self.treeview.heading("email", text="📧 Email", anchor="w")
        self.treeview.heading("source", text="📊 Source", anchor="center")
        self.treeview.heading("evenements", text="📅 Événements", anchor="center")
        self.treeview.heading("actions", text="⚙️ Actions", anchor="center")
        
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
        self.treeview.bind("<Button-3>", self._on_treeview_right_click)
        self.treeview.bind("<<TreeviewSelect>>", self._on_treeview_select)
    
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
    
    def update_display(self):
        """Met à jour l'affichage"""
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
                "", "🔍 Aucun élève trouvé", "", "", "", "", "", ""
            ))
        else:
            for i, student in enumerate(filtered_students):
                try:
                    is_selected = student["id"] in selected_students
                    
                    year_text = f"{student.get('annee', '?')}ème"
                    email_text = student.get('email', '')[:30] + "..." if len(student.get('email', '')) > 30 else student.get('email', '')
                    source_text = "📊" if student.get('source') == 'excel' else "📄"
                    nom_complet = f"{student['prenom']} {student['nom'].upper()}"
                    selection_text = "☑️" if is_selected else "☐"
                    
                    item_id = self.treeview.insert("", "end", 
                        text="👤",
                        values=(
                            selection_text, nom_complet, student['classe'], 
                            year_text, email_text, source_text, 
                            "📅 Aucun", "👁️ Voir | 🗑️ Suppr."
                        ),
                        tags=("selected" if is_selected else ("odd" if i % 2 else "even"),)
                    )
                    
                    self.treeview.set(item_id, "student_id", student["id"])
                    
                except Exception as e:
                    print(f"Erreur création ligne: {e}")
        
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
    
    # ========== MÉTHODES SAFE ==========
    def _safe_select_all(self):
        if self.controller:
            try:
                self.controller.select_all()
                messagebox.showinfo("✅ Sélection", "Tous les élèves sélectionnés")
            except Exception as e:
                messagebox.showerror("❌ Erreur", f"Erreur sélection: {e}")
    
    def _safe_deselect_all(self):
        if self.controller:
            try:
                self.controller.deselect_all()
                messagebox.showinfo("☐ Désélection", "Tous les élèves désélectionnés")
            except Exception as e:
                messagebox.showerror("❌ Erreur", f"Erreur désélection: {e}")
    
    def _safe_assign_to_event(self):
        if self.controller:
            try:
                selected_count = len(self.controller.get_selected_students())
                if selected_count == 0:
                    messagebox.showwarning("⚠️ Attention", "Aucun élève sélectionné")
                    return
                messagebox.showinfo("📅 Événement", f"Assignation pour {selected_count} élèves\n(À développer)")
            except Exception as e:
                messagebox.showerror("❌ Erreur", f"Erreur assignation: {e}")
    
    def _safe_calculate_event_cost(self):
        if self.controller:
            try:
                selected_count = len(self.controller.get_selected_students())
                if selected_count == 0:
                    messagebox.showwarning("⚠️ Attention", "Aucun élève sélectionné")
                    return
                messagebox.showinfo("💰 Coût", f"Calcul pour {selected_count} élèves\n(À développer)")
            except Exception as e:
                messagebox.showerror("❌ Erreur", f"Erreur calcul: {e}")
    
    # ========== CALLBACKS SIMPLIFIÉS ==========
    def _safe_toggle_student_selection(self, student_id):
        if self.controller:
            try:
                self.controller.toggle_student_selection(student_id)
                self.update_display()
            except Exception as e:
                print(f"Erreur toggle: {e}")
    
    def _safe_view_student(self, student_id):
        messagebox.showinfo("👁️ Voir", f"Détails élève ID: {student_id}\n(À développer)")
    
    def _safe_delete_student(self, student_id):
        result = messagebox.askyesno("🗑️ Supprimer", f"Supprimer l'élève ID: {student_id} ?")
        if result:
            messagebox.showinfo("🗑️ Suppression", "Suppression effectuée\n(À développer)")
    
    def _safe_export_data(self):
        messagebox.showinfo("📤 Export", "Export des données\n(À développer)")
    
    def _safe_reset_filters(self):
        try:
            self._initialize_default_filters()
            if self.controller:
                self.controller.reset_filters()
            messagebox.showinfo("🔄 Reset", "Filtres réinitialisés")
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur reset: {e}")
    
    # ========== EVENT HANDLERS ==========
    def _safe_on_search_changed(self, *args):
        if self.controller and self.search_entry:
            current_text = self.search_var.get()
            if current_text != "Nom, prénom...":
                try:
                    self.controller.on_search_changed(*args)
                except Exception as e:
                    print(f"Erreur recherche: {e}")
    
    def _safe_on_year_changed(self, event=None):
        if self.controller:
            try:
                self.controller.on_year_changed(event)
            except Exception as e:
                print(f"Erreur année: {e}")
    
    def _safe_on_filter_changed(self, event=None):
        if self.controller:
            try:
                self.controller.on_filter_changed(event)
            except Exception as e:
                print(f"Erreur filtre: {e}")
    
    def _safe_on_event_changed(self, event=None):
        if self.controller:
            try:
                self.controller.on_event_changed(event)
            except Exception as e:
                print(f"Erreur événement: {e}")
    
    def _safe_on_sort_changed(self, event=None):
        if self.controller:
            try:
                self.controller.on_sort_changed(event)
            except Exception as e:
                print(f"Erreur tri: {e}")
    
    # ========== TREEVIEW EVENTS ==========
    def _on_treeview_double_click(self, event):
        item = self.treeview.selection()[0] if self.treeview.selection() else None
        if item:
            try:
                student_id = self.treeview.set(item, "student_id")
                if student_id:
                    self._safe_view_student(student_id)
            except:
                pass
    
    def _on_treeview_right_click(self, event):
        item = self.treeview.identify_row(event.y)
        if item:
            self.treeview.selection_set(item)
    
    def _on_treeview_select(self, event):
        pass
    
    # ========== AUTRES CALLBACKS ==========
    def _on_import_excel(self):
        messagebox.showinfo("📊 Import", "Import Excel\n(À développer)")
    
    def _on_reset_json(self):
        messagebox.showinfo("🔄 Reset", "Reset vers JSON\n(À développer)")
    
    def _on_refresh(self):
        try:
            if self.controller:
                self.controller.refresh_data()
                self.update_display()
        except Exception as e:
            messagebox.showerror("❌ Erreur", f"Erreur refresh: {e}")
    
    def refresh_view(self):
        """Rafraîchit la vue"""
        if self.controller:
            try:
                self.controller.apply_all_filters()
                self.update_display()
            except Exception as e:
                print(f"Erreur refresh: {e}")
    
    def show(self):
        """Affiche la vue"""
        if self.frame:
            self.frame.pack(fill="both", expand=True, padx=8, pady=5)
    
    def hide(self):
        """Cache la vue"""
        if self.frame:
            self.frame.pack_forget()


# Classe d'alias pour maintenir la compatibilité
class StudentsView(StudentView):
    """Alias pour maintenir la compatibilité avec l'ancien nom"""
    pass