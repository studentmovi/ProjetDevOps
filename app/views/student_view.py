import tkinter as tk
from tkinter import ttk
from data.sample_data import get_all_students, get_available_years, get_available_classes, get_classes_by_year

class StudentsView:
    def __init__(self, parent, styles):
        self.parent = parent
        self.styles = styles
        self.frame = ttk.Frame(parent)
        self.students_data = get_all_students()
        self.filtered_students = self.students_data.copy()
        
        # Variables pour les filtres
        self.year_var = tk.StringVar()
        self.class_var = tk.StringVar()
        
    def create_widgets(self):
        """Crée l'interface avec styles corrigés"""
        # Titre avec styles séparés
        title_frame_config = self.styles.get_title_frame_config('primary')
        title_frame = tk.Frame(self.frame, **title_frame_config)
        title_frame.pack(fill="x", padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        title_container = tk.Frame(title_frame, bg=title_frame_config['bg'])
        title_container.pack(fill="both", expand=True, padx=20, pady=15)
        
        title_label_config = self.styles.get_title_label_config('primary')
        title = tk.Label(title_container, 
                        text="👥 Gestion des Élèves", 
                        **title_label_config)
        title.pack()
        
        subtitle_label_config = self.styles.get_subtitle_label_config('primary')
        subtitle = tk.Label(title_container, 
                           text="Filtrage et consultation des élèves", 
                           **subtitle_label_config)
        subtitle.pack()
        
        # Sections avec styles
        self.create_filter_section()
        self.create_results_section()
        self.update_results()
        
        return self.frame
    
    def create_filter_section(self):
        """Section des filtres avec styles"""
        filter_frame = ttk.LabelFrame(self.frame, text="🔍 Filtres de recherche", 
                                     style="Info.TLabelframe", padding=15)
        filter_frame.pack(fill="x", padx=20, pady=10)
        
        card_config = self.styles.get_card_config('info')
        filter_row1 = tk.Frame(filter_frame, bg=card_config['bg'])
        filter_row1.pack(fill="x", pady=8)
        
        # Filtre année
        year_container = tk.Frame(filter_row1, bg=card_config['bg'])
        year_container.pack(side="left", padx=(0, 30))
        
        tk.Label(year_container, text="📚 Année:", 
                font=("Helvetica", 9, "bold"),
                fg=self.styles.colors['text_primary'], 
                bg=card_config['bg']).pack()
        
        year_combo = ttk.Combobox(year_container, 
                                 textvariable=self.year_var, 
                                 values=["Toutes"] + get_available_years(),
                                 state="readonly", width=12, font=("Helvetica", 9))
        year_combo.pack(pady=2)
        year_combo.set("Toutes")
        year_combo.bind("<<ComboboxSelected>>", self.on_year_changed)
        
        # Filtre classe
        class_container = tk.Frame(filter_row1, bg=card_config['bg'])
        class_container.pack(side="left", padx=(0, 30))
        
        tk.Label(class_container, text="🏫 Classe:", 
                font=("Helvetica", 9, "bold"),
                fg=self.styles.colors['text_primary'], 
                bg=card_config['bg']).pack()
        
        self.class_combo = ttk.Combobox(class_container, 
                                       textvariable=self.class_var, 
                                       values=["Toutes"] + get_available_classes(),
                                       state="readonly", width=12, font=("Helvetica", 9))
        self.class_combo.pack(pady=2)
        self.class_combo.set("Toutes")
        self.class_combo.bind("<<ComboboxSelected>>", self.on_filter_changed)
        
        # Boutons avec styles
        button_frame = tk.Frame(filter_row1, bg=card_config['bg'])
        button_frame.pack(side="right")
        
        reset_config = self.styles.get_button_config('danger')
        reset_btn = tk.Button(button_frame, text="🔄 Réinitialiser", 
                             command=self.reset_filters, **reset_config)
        reset_btn.pack(side="left", padx=2)
        
        stats_config = self.styles.get_button_config('warning')
        stats_btn = tk.Button(button_frame, text="📊 Statistiques", 
                             command=self.show_statistics, **stats_config)
        stats_btn.pack(side="left", padx=2)
        
    def create_results_section(self):
        """Section des résultats avec styles"""
        results_frame = ttk.LabelFrame(self.frame, text="📋 Liste des élèves", 
                                     style="Success.TLabelframe", padding=15)
        results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        card_config = self.styles.get_card_config('success')
        
        # Info avec styles
        self.info_frame = tk.Frame(results_frame, bg=card_config['bg'])
        self.info_frame.pack(fill="x", pady=(0, 10))
        
        self.info_label = tk.Label(self.info_frame, text="", 
                                  font=("Helvetica", 9, "bold"),
                                  fg=self.styles.colors['success'],
                                  bg=card_config['bg'])
        self.info_label.pack(side="left")
        
        # Tableau
        table_frame = tk.Frame(results_frame, bg=card_config['bg'])
        table_frame.pack(fill="both", expand=True)
        
        columns = ("ID", "Nom", "Prénom", "Année", "Classe")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Configuration des colonnes
        self.tree.heading("ID", text="🆔 ID")
        self.tree.heading("Nom", text="👤 Nom")
        self.tree.heading("Prénom", text="👤 Prénom")
        self.tree.heading("Année", text="📚 Année")
        self.tree.heading("Classe", text="🏫 Classe")
        
        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Nom", width=120)
        self.tree.column("Prénom", width=120)
        self.tree.column("Année", width=80, anchor="center")
        self.tree.column("Classe", width=90, anchor="center")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def on_year_changed(self, event=None):
        selected_year = self.year_var.get()
        if selected_year == "Toutes":
            self.class_combo.configure(values=["Toutes"] + get_available_classes())
        else:
            available_classes = get_classes_by_year(selected_year)
            self.class_combo.configure(values=["Toutes"] + available_classes)
        self.class_var.set("Toutes")
        self.on_filter_changed()
    
    def on_filter_changed(self, event=None):
        selected_year = self.year_var.get()
        selected_class = self.class_var.get()
        self.filtered_students = []
        for student in self.students_data:
            if selected_year != "Toutes" and student["annee"] != selected_year:
                continue
            if selected_class != "Toutes" and student["classe"] != selected_class:
                continue
            self.filtered_students.append(student)
        self.update_results()
    
    def update_results(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i, student in enumerate(self.filtered_students):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=(
                student["id"], student["nom"], student["prenom"],
                f"{student['annee']}ème", student["classe"]
            ), tags=(tag,))
        self.tree.tag_configure('evenrow', background='#f8f9fa')
        self.tree.tag_configure('oddrow', background='#ffffff')
        count = len(self.filtered_students)
        total = len(self.students_data)
        self.info_label.config(text=f"📊 Résultats: {count} élève(s) sur {total} total")
    
    def reset_filters(self):
        self.year_var.set("Toutes")
        self.class_var.set("Toutes")
        self.class_combo.configure(values=["Toutes"] + get_available_classes())
        self.filtered_students = self.students_data.copy()
        self.update_results()
    
    def show_statistics(self):
        if not self.filtered_students:
            tk.messagebox.showinfo("Statistiques", "Aucun élève sélectionné")
            return
        stats_by_year = {}
        stats_by_class = {}
        for student in self.filtered_students:
            year = student["annee"]
            classe = student["classe"]
            stats_by_year[year] = stats_by_year.get(year, 0) + 1
            stats_by_class[classe] = stats_by_class.get(classe, 0) + 1
        message = f"📊 Statistiques pour {len(self.filtered_students)} élève(s):\n\n"
        message += "📚 Par année:\n"
        for year in sorted(stats_by_year.keys()):
            message += f"   • {year}ème année: {stats_by_year[year]} élève(s)\n"
        message += "\n🏫 Par classe:\n"
        for classe in sorted(stats_by_class.keys()):
            message += f"   • {classe}: {stats_by_class[classe]} élève(s)\n"
        tk.messagebox.showinfo("📊 Statistiques détaillées", message)
    
    def show(self):
        self.frame.pack(fill="both", expand=True)
        
    def hide(self):
        self.frame.pack_forget()