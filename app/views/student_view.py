import tkinter as tk
from tkinter import ttk
from controller.StudentViewController import StudentViewController
from component.Button import ActionButton
from component.Cards import Card
from component.FilterPanel import FilterPanel

class StudentsView:
    def __init__(self, parent, styles):
        self.parent = parent
        self.styles = styles
        self.frame = ttk.Frame(parent)
        
        # Initialiser le contrôleur
        self.controller = StudentViewController(self)
        
    def create_widgets(self):
        """Crée l'interface complète"""
        # Section titre avec actions simplifiées
        self.create_title_section()
        
        # Section filtres
        self.create_filter_section()
        
        # Section résultats avec tableau
        self.create_results_section()
        
        # Section pagination
        self.create_pagination_section()
        
        # Mise à jour initiale
        self.update_display()
        
        return self.frame
    
    def create_title_section(self):
        """Section titre avec actions simplifiées"""
        title_frame_config = self.styles.get_title_frame_config('primary')
        title_frame = tk.Frame(self.frame, **title_frame_config)
        title_frame.pack(fill="x", padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        title_container = tk.Frame(title_frame, bg=title_frame_config['bg'])
        title_container.pack(fill="both", expand=True, padx=20, pady=12)
        
        # Container gauche : Titre + Sous-titre
        left_container = tk.Frame(title_container, bg=title_frame_config['bg'])
        left_container.pack(side="left")
        
        title_label_config = self.styles.get_title_label_config('primary')
        title = tk.Label(left_container, 
                        text="👥 Gestion des Élèves", 
                        **title_label_config)
        title.pack(side="left")
        
        subtitle_label_config = self.styles.get_subtitle_label_config('primary')
        subtitle = tk.Label(left_container, 
                           text="Assignation événements & calculs", 
                           **subtitle_label_config)
        subtitle.pack(side="left", padx=(15, 0))
        
        # Container centre : Actions Rapides SIMPLIFIÉES
        center_container = tk.Frame(title_container, bg=title_frame_config['bg'])
        center_container.pack(side="left", padx=(40, 0))
        
        actions_label = tk.Label(center_container,
                               text="⚡ Actions:",
                               font=("Helvetica", 9, "bold"),
                               fg="white",
                               bg=title_frame_config['bg'])
        actions_label.pack(side="left")
        
        actions_buttons = tk.Frame(center_container, bg=title_frame_config['bg'])
        actions_buttons.pack(side="left", padx=(8, 0))
        
        # SEULEMENT 2 ACTIONS
        ActionButton(actions_buttons, "→ Événement", 
                    command=self.controller.assign_to_event, 
                    action_type='save').create().pack(side="left", padx=2)
        
        ActionButton(actions_buttons, "💰 Calculer Prix", 
                    command=self.controller.calculate_event_cost, 
                    action_type='warning').create().pack(side="left", padx=2)
        
        # Container droite : Statistiques + Informations
        right_container = tk.Frame(title_container, bg=title_frame_config['bg'])
        right_container.pack(side="right")
        
        # Statistiques
        stats_frame = tk.Frame(right_container, bg=title_frame_config['bg'])
        stats_frame.pack(side="top")
        
        students_data = self.controller.get_students_data()
        classes_count = len(set(student["classe"] for student in students_data))
        
        total_label = tk.Label(stats_frame,
                             text=f"📊 {len(students_data)} élèves",
                             font=("Helvetica", 10, "bold"),
                             fg="white",
                             bg=title_frame_config['bg'])
        total_label.pack(side="left", padx=(0, 10))
        
        classes_label = tk.Label(stats_frame,
                               text=f"🏫 {classes_count} classes",
                               font=("Helvetica", 10, "bold"),
                               fg="white",
                               bg=title_frame_config['bg'])
        classes_label.pack(side="left")
        
        # Informations dynamiques
        info_frame = tk.Frame(right_container, bg=title_frame_config['bg'])
        info_frame.pack(side="top", pady=(3, 0))
        
        self.header_filter_info = tk.Label(info_frame,
                                         text="",
                                         font=("Helvetica", 8),
                                         fg="#e8eaf6",
                                         bg=title_frame_config['bg'])
        self.header_filter_info.pack(side="left", padx=(0, 10))
        
        self.header_selection_info = tk.Label(info_frame,
                                            text="",
                                            font=("Helvetica", 8),
                                            fg="#e8eaf6",
                                            bg=title_frame_config['bg'])
        self.header_selection_info.pack(side="left")
    
    def create_filter_section(self):
        """Section filtres avec événements"""
        self.filter_panel = FilterPanel(self.frame, "Filtres Avancés")
        panel_frame = self.filter_panel.create()
        panel_frame.pack(fill="x", padx=20, pady=8)
        
        # Filtres standard
        from data.sample_data import get_available_years, get_available_classes
        
        self.year_var, self.year_combo = self.filter_panel.add_combobox_filter(
            "year", "Année", ["Toutes"] + get_available_years(),
            callback=self.controller.on_year_changed
        )
        
        self.class_var, self.class_combo = self.filter_panel.add_combobox_filter(
            "class", "Classe", ["Toutes"] + get_available_classes(),
            callback=self.controller.on_filter_changed
        )
        
        self.search_var, self.search_entry = self.filter_panel.add_entry_filter(
            "search", "Recherche", placeholder="Nom, prénom...",
            callback=self.controller.on_search_changed
        )
        
        # Filtre par événement
        events_list = self.controller.get_events_for_filter()
        self.event_var, self.event_combo = self.filter_panel.add_combobox_filter(
            "event", "Événement", ["Aucun"] + events_list,
            callback=self.controller.on_event_changed
        )
        
        # Filtre de tri
        self.sort_var, self.sort_combo = self.filter_panel.add_combobox_filter(
            "sort", "Tri", ["Nom A-Z", "Nom Z-A", "Classe", "Année"],
            default="Nom A-Z", callback=self.controller.on_sort_changed
        )
        
        # Boutons du panel
        self.filter_panel.add_action_buttons(
            reset_callback=self.controller.reset_filters,
            export_callback=self.controller.export_filtered_data
        )
    
    def create_results_section(self):
        """Section des résultats avec tableau"""
        results_card = Card(self.frame, "📋 Liste des Élèves", "success", padding=12)
        results_frame = results_card.create()
        results_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        body = results_card.get_body()
        
        # Container pour le tableau
        table_container = tk.Frame(body, bg=self.styles.get_card_config('success')['bg'])
        table_container.pack(fill="both", expand=True)
        
        # Tableau
        columns = ("Sél", "ID", "Nom", "Prénom", "Année", "Classe", "Événements", "Actions")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=28)
        
        headers = {
            "Sél": "☑️", "ID": "🆔 ID", "Nom": "👤 Nom", "Prénom": "👤 Prénom",
            "Année": "📚 Année", "Classe": "🏫 Classe", "Événements": "📅 Événements", "Actions": "⚙️ Actions"
        }
        
        for col in columns:
            self.tree.heading(col, text=headers[col])
        
        # Largeurs des colonnes
        self.tree.column("Sél", width=50, anchor="center")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nom", width=130)
        self.tree.column("Prénom", width=130)
        self.tree.column("Année", width=80, anchor="center")
        self.tree.column("Classe", width=90, anchor="center")
        self.tree.column("Événements", width=150)
        self.tree.column("Actions", width=120, anchor="center")
        
        # Style
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        
        # Événements
        self.tree.bind("<Button-1>", self.on_tree_click)
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)
    
    def create_pagination_section(self):
        """Section pagination"""
        pagination_frame = tk.Frame(self.frame, bg=self.styles.colors['background'])
        pagination_frame.pack(fill="x", padx=20, pady=3)
        
        self.detail_info = tk.Label(pagination_frame,
                                  text="",
                                  font=("Helvetica", 8),
                                  fg=self.styles.colors['text_secondary'],
                                  bg=self.styles.colors['background'])
        self.detail_info.pack(side="left")
        
        view_actions = tk.Frame(pagination_frame, bg=self.styles.colors['background'])
        view_actions.pack(side="right")
        
        ActionButton(view_actions, "Tout Sélectionner",
                    command=self.controller.select_all, action_type='search').create().pack(side="left", padx=2)
        
        ActionButton(view_actions, "Tout Désélectionner",
                    command=self.controller.deselect_all, action_type='cancel').create().pack(side="left", padx=2)
        
        ActionButton(view_actions, "Actualiser",
                    command=self.controller.refresh_data, action_type='refresh').create().pack(side="left", padx=2)
    
    # ====================== ÉVÉNEMENTS DU TABLEAU ======================
    def on_tree_click(self, event):
        """Gère les clics sur le tableau"""
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        
        if item and column:
            col_index = int(column.replace('#', '')) - 1
            if col_index == 0:  # Colonne sélection
                values = self.tree.item(item)['values']
                student_id = int(values[1])
                
                is_selected = self.controller.toggle_student_selection(student_id)
                self.tree.set(item, "Sél", "☑️" if is_selected else "☐")
                self.update_info_labels()
                
            elif col_index == 7:  # Colonne actions
                self.show_student_actions(item, event)
    
    def on_tree_double_click(self, event):
        """Gère les double-clics pour voir les détails"""
        item = self.tree.identify_row(event.y)
        if item:
            values = self.tree.item(item)['values']
            student_id = values[1]
            self.controller.view_student(student_id)
    
    def show_student_actions(self, item, event):
        """Affiche le menu contextuel des actions"""
        values = self.tree.item(item)['values']
        student_id = int(values[1])
        
        menu = tk.Menu(self.tree, tearoff=0)
        menu.add_command(label="👁️ Voir détails", 
                        command=lambda: self.controller.view_student(student_id))
        menu.add_command(label="📝 Modifier", 
                        command=lambda: self.controller.edit_student(student_id))
        menu.add_separator()
        menu.add_command(label="📅 Assigner à événement", 
                        command=lambda: self.assign_single_to_event(student_id))
        menu.add_separator()
        menu.add_command(label="🗑️ Supprimer", 
                        command=lambda: self.controller.delete_student(student_id))
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def assign_single_to_event(self, student_id):
        """Assigne un seul élève à un événement"""
        self.controller.selected_students = [student_id]
        self.controller.assign_to_event()
    
    # ====================== MISE À JOUR DE L'AFFICHAGE ======================
    def update_display(self):
        """Met à jour l'affichage complet (appelé par le contrôleur)"""
        # Vider le tableau
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Remplir avec les données filtrées
        filtered_students = self.controller.get_filtered_students()
        selected_students = self.controller.get_selected_students()
        
        for i, student in enumerate(filtered_students):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            selected_mark = "☑️" if student["id"] in selected_students else "☐"
            
            student_events = self.controller.get_student_events(student)
            
            self.tree.insert("", "end", values=(
                selected_mark,
                student["id"],
                student["nom"],
                student["prenom"],
                f"{student['annee']}ème",
                student["classe"],
                student_events,
                "👁️ 📝 🗑️"
            ), tags=(tag,))
        
        # Couleurs alternées
        self.tree.tag_configure('evenrow', background='#f8f9fa')
        self.tree.tag_configure('oddrow', background='#ffffff')
        
        # Mettre à jour les informations
        self.update_info_labels()
    
    def update_info_labels(self):
        """Met à jour les labels d'information"""
        filtered_students = self.controller.get_filtered_students()
        students_data = self.controller.get_students_data()
        selected_students = self.controller.get_selected_students()
        
        count = len(filtered_students)
        total = len(students_data)
        selected = len(selected_students)
        
        # Informations dans le header
        if count == total:
            self.header_filter_info.config(text=f"✅ Tous affichés ({count})")
        else:
            self.header_filter_info.config(text=f"🔍 {count}/{total} filtrés")
        
        if selected > 0:
            self.header_selection_info.config(text=f"🔸 {selected} sélectionnés")
        else:
            self.header_selection_info.config(text="")
        
        # Informations détaillées en bas
        if count > 0:
            years_in_results = set(student["annee"] for student in filtered_students)
            classes_in_results = set(student["classe"] for student in filtered_students)
            self.detail_info.config(
                text=f"Années: {', '.join(sorted(years_in_results))} • "
                     f"Classes: {', '.join(sorted(classes_in_results))}"
            )
        else:
            self.detail_info.config(text="Aucun résultat à afficher")
    
    def show(self):
        self.frame.pack(fill="both", expand=True)
        
    def hide(self):
        self.frame.pack_forget()