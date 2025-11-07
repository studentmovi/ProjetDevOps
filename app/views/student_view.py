import tkinter as tk
from tkinter import ttk
from data.sample_data import get_all_students, get_available_years, get_available_classes, get_classes_by_year
from component.Button import ActionButton, NavButton
from component.Cards import Card, StatCard
from component.FilterPanel import FilterPanel

class StudentsView:
    def __init__(self, parent, styles):
        self.parent = parent
        self.styles = styles
        self.frame = ttk.Frame(parent)
        self.students_data = get_all_students()
        self.filtered_students = self.students_data.copy()
        
        # État des sélections
        self.selected_students = []
        
    def create_widgets(self):
        """Crée l'interface complète avec composants"""
        # Section titre
        self.create_title_section()
        
        # Section filtres avec composant
        self.create_filter_section()
        
        # Section actions de groupe
        self.create_bulk_actions_section()
        
        # Section résultats avec tableau
        self.create_results_section()
        
        # Section pagination et informations
        self.create_pagination_section()
        
        # Mise à jour initiale
        self.update_results()
        
        return self.frame
    
    def create_title_section(self):
        """Section titre avec compteurs"""
        title_frame_config = self.styles.get_title_frame_config('primary')
        title_frame = tk.Frame(self.frame, **title_frame_config)
        title_frame.pack(fill="x", padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        title_container = tk.Frame(title_frame, bg=title_frame_config['bg'])
        title_container.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Titre principal
        title_label_config = self.styles.get_title_label_config('primary')
        title = tk.Label(title_container, 
                        text="👥 Gestion des Élèves", 
                        **title_label_config)
        title.pack(side="left")
        
        # Compteurs à droite
        counters_frame = tk.Frame(title_container, bg=title_frame_config['bg'])
        counters_frame.pack(side="right")
        
        total_label = tk.Label(counters_frame,
                             text=f"Total: {len(self.students_data)} élèves",
                             font=("Helvetica", 10, "bold"),
                             fg="white",
                             bg=title_frame_config['bg'])
        total_label.pack()
        
        # Sous-titre avec date
        subtitle_label_config = self.styles.get_subtitle_label_config('primary')
        subtitle = tk.Label(title_container, 
                           text="Recherche, filtrage et gestion des élèves", 
                           **subtitle_label_config)
        subtitle.pack(side="left", padx=(20, 0))
    
    def create_statistics_section(self):
        """Section des statistiques avec cartes"""
        stats_frame = tk.Frame(self.frame, bg=self.styles.colors['background'])
        stats_frame.pack(fill="x", padx=20, pady=15)
        
        # Titre de section
        section_title = tk.Label(stats_frame,
                               text="📊 Statistiques Rapides",
                               font=("Helvetica", 12, "bold"),
                               fg=self.styles.colors['text_primary'],
                               bg=self.styles.colors['background'])
        section_title.pack(anchor="w", pady=(0, 10))
        
        # Container pour les cartes
        cards_container = tk.Frame(stats_frame, bg=self.styles.colors['background'])
        cards_container.pack(fill="x")
        
        # Calcul des statistiques
        years_count = len(set(student["annee"] for student in self.students_data))
        classes_count = len(set(student["classe"] for student in self.students_data))
        
        # Trouver l'année avec le plus d'élèves
        year_counts = {}
        for student in self.students_data:
            year = student["annee"]
            year_counts[year] = year_counts.get(year, 0) + 1
        most_populated_year = max(year_counts.items(), key=lambda x: x[1]) if year_counts else ("N/A", 0)
        
        # Cartes statistiques
        total_card = StatCard(
            cards_container, "Total Élèves", len(self.students_data),
            "Dans l'établissement", "👥", "primary"
        )
        total_card.create().pack(side="left", fill="x", expand=True, padx=3)
        
        self.filtered_card = StatCard(
            cards_container, "Affichés", len(self.filtered_students),
            "Après filtrage", "🔍", "success"
        )
        self.filtered_card_widget = self.filtered_card.create()
        self.filtered_card_widget.pack(side="left", fill="x", expand=True, padx=3)
        
        years_card = StatCard(
            cards_container, "Années", years_count,
            "Niveaux scolaires", "📚", "info"
        )
        years_card.create().pack(side="left", fill="x", expand=True, padx=3)
        
        classes_card = StatCard(
            cards_container, "Classes", classes_count,
            "Au total", "🏫", "warning"
        )
        classes_card.create().pack(side="left", fill="x", expand=True, padx=3)
        
        popular_card = StatCard(
            cards_container, f"{most_populated_year[0]}ème année", most_populated_year[1],
            "Année la plus peuplée", "👑", "success"
        )
        popular_card.create().pack(side="left", fill="x", expand=True, padx=3)
    
    def create_filter_section(self):
        """Section filtres avec composant FilterPanel"""
        # Créer le panneau de filtres
        self.filter_panel = FilterPanel(self.frame, "Recherche et Filtres")
        panel_frame = self.filter_panel.create()
        panel_frame.pack(fill="x", padx=20, pady=10)
        
        # Configuration du style du panel
        panel_frame.configure(style="Info.TLabelframe")
        
        # Ajouter les filtres
        self.year_var, self.year_combo = self.filter_panel.add_combobox_filter(
            "year", "Année", ["Toutes"] + get_available_years(),
            callback=self.on_year_changed
        )
        
        self.class_var, self.class_combo = self.filter_panel.add_combobox_filter(
            "class", "Classe", ["Toutes"] + get_available_classes(),
            callback=self.on_filter_changed
        )
        
        self.search_var, self.search_entry = self.filter_panel.add_entry_filter(
            "search", "Recherche", placeholder="Nom, prénom...",
            callback=self.on_search_changed
        )
        
        # Ajouter des filtres supplémentaires
        self.gender_var, self.gender_combo = self.filter_panel.add_combobox_filter(
            "sort", "Tri", ["Nom A-Z", "Nom Z-A", "Classe", "Année"],
            default="Nom A-Z", callback=self.on_sort_changed
        )
        
        # Boutons d'action du panel
        self.filter_panel.add_action_buttons(
            reset_callback=self.reset_filters,
            export_callback=self.export_filtered_data
        )
    
    def create_bulk_actions_section(self):
        """Section des actions en lot"""
        actions_frame = tk.Frame(self.frame, bg=self.styles.colors['background'])
        actions_frame.pack(fill="x", padx=20, pady=5)
        
        # Titre
        actions_title = tk.Label(actions_frame,
                               text="⚡ Actions Rapides",
                               font=("Helvetica", 10, "bold"),
                               fg=self.styles.colors['text_primary'],
                               bg=self.styles.colors['background'])
        actions_title.pack(side="left")
        
        # Séparateur
        separator = tk.Label(actions_frame, text="•",
                           fg=self.styles.colors['text_secondary'],
                           bg=self.styles.colors['background'])
        separator.pack(side="left", padx=10)
        
        # Boutons d'actions
        ActionButton(actions_frame, "Ajouter Élève", 
                    command=self.add_student, action_type='add').create().pack(side="left", padx=2)
        
        ActionButton(actions_frame, "Import Excel", 
                    command=self.import_excel, action_type='import').create().pack(side="left", padx=2)
        
        ActionButton(actions_frame, "Exporter Tout", 
                    command=self.export_all, action_type='export').create().pack(side="left", padx=2)
        
        # Informations à droite
        self.selection_info = tk.Label(actions_frame,
                                     text="",
                                     font=("Helvetica", 9),
                                     fg=self.styles.colors['text_secondary'],
                                     bg=self.styles.colors['background'])
        self.selection_info.pack(side="right")
    
    def create_results_section(self):
        """Section des résultats avec tableau avancé"""
        # Carte pour les résultats
        results_card = Card(self.frame, "📋 Liste des Élèves", "success", padding=15)
        results_frame = results_card.create()
        results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        body = results_card.get_body()
        
        # Barre d'outils du tableau
        toolbar_frame = tk.Frame(body, bg=self.styles.get_card_config('success')['bg'])
        toolbar_frame.pack(fill="x", pady=(0, 10))
        
        # Informations sur les résultats
        self.results_info = tk.Label(toolbar_frame,
                                   text="",
                                   font=("Helvetica", 9, "bold"),
                                   fg=self.styles.colors['success'],
                                   bg=self.styles.get_card_config('success')['bg'])
        self.results_info.pack(side="left")
        
        # Actions sur sélection
        selection_actions = tk.Frame(toolbar_frame, bg=self.styles.get_card_config('success')['bg'])
        selection_actions.pack(side="right")
        
        self.edit_selected_btn = ActionButton(selection_actions, "Modifier Sélection",
                                            command=self.edit_selected, action_type='edit')
        self.edit_selected_btn.create().pack(side="left", padx=2)
        self.edit_selected_btn.create().config(state="disabled")
        
        self.delete_selected_btn = ActionButton(selection_actions, "Supprimer Sélection",
                                              command=self.delete_selected, action_type='delete')
        self.delete_selected_btn.create().pack(side="left", padx=2)
        self.delete_selected_btn.create().config(state="disabled")
        
        # Container pour le tableau
        table_container = tk.Frame(body, bg=self.styles.get_card_config('success')['bg'])
        table_container.pack(fill="both", expand=True)
        
        # Tableau avec colonnes étendues
        columns = ("Sél", "ID", "Nom", "Prénom", "Année", "Classe", "Actions")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=15)
        
        # Configuration des colonnes
        headers = {
            "Sél": "☑️", "ID": "🆔 ID", "Nom": "👤 Nom", "Prénom": "👤 Prénom",
            "Année": "📚 Année", "Classe": "🏫 Classe", "Actions": "⚙️ Actions"
        }
        
        for col in columns:
            self.tree.heading(col, text=headers[col])
        
        # Largeurs des colonnes
        self.tree.column("Sél", width=40, anchor="center")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nom", width=120)
        self.tree.column("Prénom", width=120)
        self.tree.column("Année", width=80, anchor="center")
        self.tree.column("Classe", width=80, anchor="center")
        self.tree.column("Actions", width=100, anchor="center")
        
        # Événements du tableau
        self.tree.bind("<Button-1>", self.on_tree_click)
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Placement du tableau et scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)
    
    def create_pagination_section(self):
        """Section pagination et informations"""
        pagination_frame = tk.Frame(self.frame, bg=self.styles.colors['background'])
        pagination_frame.pack(fill="x", padx=20, pady=10)
        
        # Informations détaillées
        self.detail_info = tk.Label(pagination_frame,
                                  text="",
                                  font=("Helvetica", 8),
                                  fg=self.styles.colors['text_secondary'],
                                  bg=self.styles.colors['background'])
        self.detail_info.pack(side="left")
        
        # Actions d'affichage
        view_actions = tk.Frame(pagination_frame, bg=self.styles.colors['background'])
        view_actions.pack(side="right")
        
        ActionButton(view_actions, "Tout Sélectionner",
                    command=self.select_all, action_type='search').create().pack(side="left", padx=2)
        
        ActionButton(view_actions, "Tout Désélectionner",
                    command=self.deselect_all, action_type='cancel').create().pack(side="left", padx=2)
        
        ActionButton(view_actions, "Actualiser",
                    command=self.refresh_data, action_type='refresh').create().pack(side="left", padx=2)
    
    # Méthodes de gestion des événements
    def on_year_changed(self, event=None):
        """Gère le changement d'année"""
        selected_year = self.filter_panel.get_filter_value("year")
        
        if selected_year == "Toutes":
            self.class_combo.configure(values=["Toutes"] + get_available_classes())
        else:
            available_classes = get_classes_by_year(selected_year)
            self.class_combo.configure(values=["Toutes"] + available_classes)
        
        self.filter_panel.set_filter_value("class", "Toutes")
        self.apply_all_filters()
    
    def on_filter_changed(self, event=None):
        """Applique les filtres"""
        self.apply_all_filters()
    
    def on_search_changed(self, *args):
        """Recherche en temps réel"""
        self.apply_all_filters()
    
    def on_sort_changed(self, event=None):
        """Gère le changement de tri"""
        self.apply_all_filters()
    
    def apply_all_filters(self):
        """Applique tous les filtres et le tri"""
        selected_year = self.filter_panel.get_filter_value("year")
        selected_class = self.filter_panel.get_filter_value("class")
        search_text = self.filter_panel.get_filter_value("search").lower()
        sort_type = self.filter_panel.get_filter_value("sort")
        
        # Filtrage
        self.filtered_students = []
        
        for student in self.students_data:
            # Filtre par année
            if selected_year != "Toutes" and student["annee"] != selected_year:
                continue
            
            # Filtre par classe
            if selected_class != "Toutes" and student["classe"] != selected_class:
                continue
            
            # Filtre par recherche
            if search_text and search_text not in "nom, prénom...":
                if (search_text not in student["nom"].lower() and 
                    search_text not in student["prenom"].lower()):
                    continue
            
            self.filtered_students.append(student)
        
        # Tri
        if sort_type == "Nom A-Z":
            self.filtered_students.sort(key=lambda x: x["nom"])
        elif sort_type == "Nom Z-A":
            self.filtered_students.sort(key=lambda x: x["nom"], reverse=True)
        elif sort_type == "Classe":
            self.filtered_students.sort(key=lambda x: x["classe"])
        elif sort_type == "Année":
            self.filtered_students.sort(key=lambda x: x["annee"])
        
        self.update_results()
    
    def update_results(self):
        """Met à jour l'affichage complet"""
        # Vider le tableau
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Remplir avec les données filtrées
        for i, student in enumerate(self.filtered_students):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            selected_mark = "☑️" if student["id"] in self.selected_students else "☐"
            
            self.tree.insert("", "end", values=(
                selected_mark,
                student["id"],
                student["nom"],
                student["prenom"],
                f"{student['annee']}ème",
                student["classe"],
                "👁️ 📝 🗑️"
            ), tags=(tag,))
        
        # Couleurs alternées
        self.tree.tag_configure('evenrow', background='#f8f9fa')
        self.tree.tag_configure('oddrow', background='#ffffff')
        
        # Mettre à jour les informations
        self.update_info_labels()
        self.update_filtered_card()
    
    def update_info_labels(self):
        """Met à jour les labels d'information"""
        count = len(self.filtered_students)
        total = len(self.students_data)
        selected = len(self.selected_students)
        
        # Informations résultats
        self.results_info.config(text=f"📊 Affichage: {count} élève(s) sur {total}")
        
        # Informations sélection
        if selected > 0:
            self.selection_info.config(text=f"🔸 {selected} élève(s) sélectionné(s)")
            # Activer les boutons d'action
            # self.edit_selected_btn.create().config(state="normal")
            # self.delete_selected_btn.create().config(state="normal")
        else:
            self.selection_info.config(text="")
            # self.edit_selected_btn.create().config(state="disabled")
            # self.delete_selected_btn.create().config(state="disabled")
        
        # Informations détaillées
        if count > 0:
            years_in_results = set(student["annee"] for student in self.filtered_students)
            classes_in_results = set(student["classe"] for student in self.filtered_students)
            self.detail_info.config(
                text=f"Années: {', '.join(sorted(years_in_results))} • "
                     f"Classes: {', '.join(sorted(classes_in_results))}"
            )
        else:
            self.detail_info.config(text="Aucun résultat à afficher")
    
    def update_filtered_card(self):
        """Met à jour la carte des statistiques filtrées"""
        self.filtered_card_widget.destroy()
        
        stats_frame = self.filtered_card_widget.master
        self.filtered_card = StatCard(
            stats_frame, "Affichés", len(self.filtered_students),
            "Après filtrage", "🔍", "success"
        )
        self.filtered_card_widget = self.filtered_card.create()
        self.filtered_card_widget.pack(side="left", fill="x", expand=True, padx=3)
    
    # Méthodes d'événements du tableau
    def on_tree_click(self, event):
        """Gère les clics sur le tableau"""
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        
        if item and column:
            col_index = int(column.replace('#', '')) - 1
            if col_index == 0:  # Colonne sélection
                self.toggle_student_selection(item)
            elif col_index == 6:  # Colonne actions
                self.show_student_actions(item, event)
    
    def on_tree_double_click(self, event):
        """Gère les double-clics pour éditer"""
        item = self.tree.identify_row(event.y)
        if item:
            values = self.tree.item(item)['values']
            student_id = values[1]
            self.edit_student(student_id)
    
    def toggle_student_selection(self, item):
        """Bascule la sélection d'un élève"""
        values = self.tree.item(item)['values']
        student_id = int(values[1])
        
        if student_id in self.selected_students:
            self.selected_students.remove(student_id)
            self.tree.set(item, "Sél", "☐")
        else:
            self.selected_students.append(student_id)
            self.tree.set(item, "Sél", "☑️")
        
        self.update_info_labels()
    
    # Méthodes d'actions
    def add_student(self):
        tk.messagebox.showinfo("Ajouter", "Ajout d'un nouvel élève")
    
    def edit_student(self, student_id):
        tk.messagebox.showinfo("Modifier", f"Modification de l'élève ID: {student_id}")
    
    def delete_student(self, student_id):
        tk.messagebox.showinfo("Supprimer", f"Suppression de l'élève ID: {student_id}")
    
    def edit_selected(self):
        tk.messagebox.showinfo("Modifier", f"Modification de {len(self.selected_students)} élèves")
    
    def delete_selected(self):
        tk.messagebox.showinfo("Supprimer", f"Suppression de {len(self.selected_students)} élèves")
    
    def import_excel(self):
        tk.messagebox.showinfo("Import", "Import Excel en cours...")
    
    def export_all(self):
        tk.messagebox.showinfo("Export", f"Export de {len(self.students_data)} élèves")
    
    def export_filtered_data(self):
        tk.messagebox.showinfo("Export", f"Export de {len(self.filtered_students)} élèves filtrés")
    
    def select_all(self):
        """Sélectionne tous les élèves affichés"""
        self.selected_students = [s["id"] for s in self.filtered_students]
        self.update_results()
    
    def deselect_all(self):
        """Désélectionne tous les élèves"""
        self.selected_students = []
        self.update_results()
    
    def refresh_data(self):
        """Actualise les données"""
        self.students_data = get_all_students()
        self.apply_all_filters()
        tk.messagebox.showinfo("Actualisation", "Données actualisées")
    
    def reset_filters(self):
        """Remet à zéro tous les filtres"""
        self.filter_panel.reset_all_filters()
        self.class_combo.configure(values=["Toutes"] + get_available_classes())
        self.filtered_students = self.students_data.copy()
        self.selected_students = []
        self.update_results()
    
    def show_student_actions(self, item, event):
        """Affiche le menu contextuel des actions"""
        values = self.tree.item(item)['values']
        student_id = int(values[1])
        
        # Menu contextuel simple
        menu = tk.Menu(self.tree, tearoff=0)
        menu.add_command(label="👁️ Voir détails", command=lambda: self.view_student(student_id))
        menu.add_command(label="📝 Modifier", command=lambda: self.edit_student(student_id))
        menu.add_separator()
        menu.add_command(label="🗑️ Supprimer", command=lambda: self.delete_student(student_id))
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def view_student(self, student_id):
        student = next((s for s in self.students_data if s["id"] == student_id), None)
        if student:
            info = f"Élève: {student['prenom']} {student['nom']}\n"
            info += f"Classe: {student['classe']}\n"
            info += f"Année: {student['annee']}ème"
            tk.messagebox.showinfo("Détails de l'élève", info)
    
    def show(self):
        self.frame.pack(fill="both", expand=True)
        
    def hide(self):
        self.frame.pack_forget()