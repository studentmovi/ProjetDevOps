import tkinter as tk
from tkinter import ttk
from data.sample_data import get_all_students, get_available_years, get_available_classes, get_classes_by_year

class StudentsView:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.students_data = get_all_students()
        self.filtered_students = self.students_data.copy()
        
        # Variables pour les filtres
        self.year_var = tk.StringVar()
        self.class_var = tk.StringVar()
        
    def create_widgets(self):
        """Crée l'interface de la vue des élèves"""
        # Titre
        title_frame = ttk.Frame(self.frame)
        title_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(title_frame, 
                 text="👥 Gestion des Élèves", 
                 font=("Helvetica", 16, "bold")).pack()
        
        # Zone de filtres
        self.create_filter_section()
        
        # Zone d'affichage des résultats
        self.create_results_section()
        
        # Charger les données initiales
        self.update_results()
        
        return self.frame
    
    def create_filter_section(self):
        """Crée la section des filtres"""
        filter_frame = ttk.LabelFrame(self.frame, text="🔍 Filtres", padding=10)
        filter_frame.pack(fill="x", padx=20, pady=5)
        
        # Première ligne de filtres
        filter_row1 = ttk.Frame(filter_frame)
        filter_row1.pack(fill="x", pady=5)
        
        # Filtre par année
        ttk.Label(filter_row1, text="Année:").pack(side="left", padx=(0, 5))
        
        year_combo = ttk.Combobox(filter_row1, 
                                 textvariable=self.year_var, 
                                 values=["Toutes"] + get_available_years(),
                                 state="readonly", 
                                 width=10)
        year_combo.pack(side="left", padx=(0, 20))
        year_combo.set("Toutes")
        year_combo.bind("<<ComboboxSelected>>", self.on_year_changed)
        
        # Filtre par classe
        ttk.Label(filter_row1, text="Classe:").pack(side="left", padx=(0, 5))
        
        self.class_combo = ttk.Combobox(filter_row1, 
                                       textvariable=self.class_var, 
                                       values=["Toutes"] + get_available_classes(),
                                       state="readonly", 
                                       width=10)
        self.class_combo.pack(side="left", padx=(0, 20))
        self.class_combo.set("Toutes")
        self.class_combo.bind("<<ComboboxSelected>>", self.on_filter_changed)
        
        # Boutons d'action
        button_frame = ttk.Frame(filter_row1)
        button_frame.pack(side="right")
        
        ttk.Button(button_frame, 
                  text="🔄 Réinitialiser", 
                  command=self.reset_filters).pack(side="left", padx=2)
        
        ttk.Button(button_frame, 
                  text="📊 Statistiques", 
                  command=self.show_statistics).pack(side="left", padx=2)
        
    def create_results_section(self):
        """Crée la section d'affichage des résultats"""
        results_frame = ttk.LabelFrame(self.frame, text="📋 Liste des élèves", padding=10)
        results_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Informations sur les résultats
        self.info_frame = ttk.Frame(results_frame)
        self.info_frame.pack(fill="x", pady=(0, 10))
        
        self.info_label = ttk.Label(self.info_frame, 
                                   text="", 
                                   font=("Helvetica", 9))
        self.info_label.pack(side="left")
        
        # Tableau des élèves avec scrollbar
        table_frame = ttk.Frame(results_frame)
        table_frame.pack(fill="both", expand=True)
        
        # Treeview pour afficher les élèves
        columns = ("ID", "Nom", "Prénom", "Année", "Classe")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Configuration des colonnes
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Prénom", text="Prénom")
        self.tree.heading("Année", text="Année")
        self.tree.heading("Classe", text="Classe")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nom", width=120)
        self.tree.column("Prénom", width=120)
        self.tree.column("Année", width=60, anchor="center")
        self.tree.column("Classe", width=80, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Placement
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def on_year_changed(self, event=None):
        """Gère le changement de l'année sélectionnée"""
        selected_year = self.year_var.get()
        
        if selected_year == "Toutes":
            # Réinitialiser les classes disponibles
            self.class_combo.configure(values=["Toutes"] + get_available_classes())
        else:
            # Mettre à jour les classes pour l'année sélectionnée
            available_classes = get_classes_by_year(selected_year)
            self.class_combo.configure(values=["Toutes"] + available_classes)
        
        # Réinitialiser la sélection de classe
        self.class_var.set("Toutes")
        
        # Mettre à jour les résultats
        self.on_filter_changed()
    
    def on_filter_changed(self, event=None):
        """Gère les changements de filtres"""
        selected_year = self.year_var.get()
        selected_class = self.class_var.get()
        
        # Filtrer les données
        self.filtered_students = []
        
        for student in self.students_data:
            # Filtre par année
            if selected_year != "Toutes" and student["annee"] != selected_year:
                continue
            
            # Filtre par classe
            if selected_class != "Toutes" and student["classe"] != selected_class:
                continue
            
            self.filtered_students.append(student)
        
        # Mettre à jour l'affichage
        self.update_results()
    
    def update_results(self):
        """Met à jour l'affichage des résultats"""
        # Vider le tableau
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Ajouter les élèves filtrés
        for student in self.filtered_students:
            self.tree.insert("", "end", values=(
                student["id"],
                student["nom"],
                student["prenom"],
                student["annee"],
                student["classe"]
            ))
        
        # Mettre à jour les informations
        count = len(self.filtered_students)
        total = len(self.students_data)
        self.info_label.config(text=f"Affichage: {count} élève(s) sur {total} total")
    
    def reset_filters(self):
        """Réinitialise tous les filtres"""
        self.year_var.set("Toutes")
        self.class_var.set("Toutes")
        self.class_combo.configure(values=["Toutes"] + get_available_classes())
        self.filtered_students = self.students_data.copy()
        self.update_results()
    
    def show_statistics(self):
        """Affiche les statistiques des élèves filtrés"""
        if not self.filtered_students:
            tk.messagebox.showinfo("Statistiques", "Aucun élève sélectionné")
            return
        
        # Calculer les statistiques
        stats_by_year = {}
        stats_by_class = {}
        
        for student in self.filtered_students:
            year = student["annee"]
            classe = student["classe"]
            
            stats_by_year[year] = stats_by_year.get(year, 0) + 1
            stats_by_class[classe] = stats_by_class.get(classe, 0) + 1
        
        # Créer le message des statistiques
        message = f"Statistiques pour {len(self.filtered_students)} élève(s):\n\n"
        
        message += "Par année:\n"
        for year in sorted(stats_by_year.keys()):
            message += f"  • {year}ème année: {stats_by_year[year]} élève(s)\n"
        
        message += "\nPar classe:\n"
        for classe in sorted(stats_by_class.keys()):
            message += f"  • {classe}: {stats_by_class[classe]} élève(s)\n"
        
        tk.messagebox.showinfo("Statistiques", message)
    
    def show(self):
        """Affiche la vue"""
        self.frame.pack(fill="both", expand=True)
        
    def hide(self):
        """Cache la vue"""
        self.frame.pack_forget()