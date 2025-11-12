import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog
import pandas as pd
from datetime import datetime
import os
from data.sample_data import (
    get_students_data_source, get_classes_data_source, get_years_data_source,
    get_available_years, get_available_classes, get_classes_by_year
)
from data.event_data_manager import event_manager

class StudentViewController:
    """Contrôleur pour la gestion de la vue des élèves"""
    
    def __init__(self, view):
        self.view = view
        self.students_data = get_students_data_source()
        self.filtered_students = self.students_data.copy()
        self.selected_students = []
        self.event_manager = event_manager
    
    # ====================== GESTION DES DONNÉES ======================
    def get_students_data(self):
        return self.students_data
    
    def get_filtered_students(self):
        return self.filtered_students
    
    def get_selected_students(self):
        return self.selected_students
    
    def refresh_data(self):
        """Actualise les données"""
        self.students_data = get_students_data_source()
        self.apply_all_filters()
        tkinter.messagebox.showinfo("Actualisation", "Données actualisées")
    
    # ====================== GESTION DES ÉVÉNEMENTS ======================
    def get_events_for_filter(self):
        """Récupère la liste des événements disponibles"""
        events = self.event_manager.get_events()
        return [f"{event['nom']} ({event['date']})" for event in events]
    
    def get_classes_for_event(self, event_name):
        """Récupère les classes concernées par un événement"""
        event_classes_mapping = {
            "Sortie Théâtre": ["1A", "1B", "2A"],
            "Visite Musée": ["3A", "3B", "3C", "4A"], 
            "Concert": ["5A", "5B", "6A", "6B"],
            "Voyage Paris": ["5A", "5B", "5C", "6A", "6B", "6C"],
        }
        
        event_key = event_name.split(" (")[0] if " (" in event_name else event_name
        return event_classes_mapping.get(event_key, [])
    
    def get_student_events(self, student):
        """Récupère les événements d'un élève"""
        student_events = self.event_manager.get_student_events(student["id"])
        if not student_events:
            return "Aucun"
        
        events = self.event_manager.get_events()
        event_names = []
        for event in events:
            if event["id"] in student_events:
                event_names.append(event["nom"])
        
        return ", ".join(event_names) if event_names else "Aucun"
    
    # ====================== GESTION DES FILTRES ======================
    def apply_all_filters(self):
        """Application de tous les filtres"""
        try:
            selected_year = self.view.year_combo.get() if hasattr(self.view, 'year_combo') else "Toutes"
            selected_class = self.view.class_combo.get() if hasattr(self.view, 'class_combo') else "Toutes" 
            selected_event = self.view.event_combo.get() if hasattr(self.view, 'event_combo') else "Aucun"
            sort_type = self.view.sort_combo.get() if hasattr(self.view, 'sort_combo') else "Nom A-Z"
            
            # Pour la recherche
            search_text = ""
            if hasattr(self.view, 'search_entry') and hasattr(self.view, 'search_var'):
                search_value = self.view.search_var.get()
                if search_value and search_value not in ["", "Nom, prénom..."]:
                    search_text = search_value.lower()
        except Exception as e:
            selected_year = "Toutes"
            selected_class = "Toutes"
            selected_event = "Aucun"
            sort_type = "Nom A-Z"
            search_text = ""
        
        # Filtrage
        self.filtered_students = []
        
        for student in self.students_data:
            # Filtre par année
            if selected_year != "Toutes":
                student_year = str(student["annee"])
                filter_year = selected_year.replace("ère", "").replace("ème", "").replace("e", "")
                if student_year != filter_year:
                    continue
            
            # Filtre par classe
            if selected_class != "Toutes":
                if student["classe"] != selected_class:
                    continue
            
            # Filtre par événement
            if selected_event != "Aucun":
                concerned_classes = self.get_classes_for_event(selected_event)
                if student["classe"] not in concerned_classes:
                    continue
            
            # Filtre par recherche
            if search_text:
                if (search_text not in student["nom"].lower() and 
                    search_text not in student["prenom"].lower()):
                    continue
            
            self.filtered_students.append(student)
        
        # Tri
        if sort_type == "Nom A-Z":
            self.filtered_students.sort(key=lambda x: x["nom"].lower())
        elif sort_type == "Nom Z-A":
            self.filtered_students.sort(key=lambda x: x["nom"].lower(), reverse=True)
        elif sort_type == "Classe":
            self.filtered_students.sort(key=lambda x: (int(x["annee"]), x["classe"]))
        elif sort_type == "Année":
            self.filtered_students.sort(key=lambda x: int(x["annee"]))
        
        # Mettre à jour l'affichage
        self.view.update_display()
    
    def on_year_changed(self, event=None):
        """Gestion du changement d'année"""
        try:
            selected_year = self.view.year_combo.get() if hasattr(self.view, 'year_combo') else "Toutes"
            
            if selected_year == "Toutes":
                available_classes = ["Toutes"] + get_classes_data_source()
            else:
                year_number = selected_year.replace("ère", "").replace("ème", "").replace("e", "")
                available_classes = ["Toutes"] + get_classes_by_year(year_number)
            
            if hasattr(self.view, 'class_combo'):
                self.view.class_combo.configure(values=available_classes)
                self.view.class_combo.set("Toutes")
            
            self.apply_all_filters()
        except:
            self.apply_all_filters()
    
    def on_filter_changed(self, event=None):
        self.apply_all_filters()
    
    def on_search_changed(self, *args):
        self.apply_all_filters()
    
    def on_sort_changed(self, event=None):
        self.apply_all_filters()
    
    def on_event_changed(self, event=None):
        try:
            selected_event = self.view.event_combo.get() if hasattr(self.view, 'event_combo') else "Aucun"
            
            if selected_event != "Aucun":
                concerned_classes = self.get_classes_for_event(selected_event)
                self.auto_select_students_by_classes(concerned_classes)
            
            self.apply_all_filters()
        except:
            self.apply_all_filters()
    
    def auto_select_students_by_classes(self, classes):
        if not classes:
            return
            
        self.selected_students = []
        for student in self.students_data:
            if student["classe"] in classes:
                self.selected_students.append(student["id"])
    
    def reset_filters(self):
        """Reset de tous les filtres"""
        try:
            if hasattr(self.view, 'year_combo'):
                self.view.year_combo.set("Toutes")
            if hasattr(self.view, 'class_combo'):
                self.view.class_combo.configure(values=["Toutes"] + get_classes_data_source())
                self.view.class_combo.set("Toutes")
            if hasattr(self.view, 'event_combo'):
                self.view.event_combo.set("Aucun")
            if hasattr(self.view, 'search_var'):
                self.view.search_var.set("")
            if hasattr(self.view, 'sort_combo'):
                self.view.sort_combo.set("Nom A-Z")
            
            self.filtered_students = self.students_data.copy()
            self.selected_students = []
            self.view.update_display()
        except:
            pass
    
    # ====================== GESTION DES SÉLECTIONS ======================
    def toggle_student_selection(self, student_id):
        if student_id in self.selected_students:
            self.selected_students.remove(student_id)
            return False
        else:
            self.selected_students.append(student_id)
            return True
    
    def select_all(self):
        self.selected_students = [s["id"] for s in self.filtered_students]
        self.view.update_display()
    
    def deselect_all(self):
        self.selected_students = []
        self.view.update_display()
    
    # ====================== POPUPS POUR ÉVÉNEMENTS ET CALCULS ======================
    def assign_to_event(self):
        """POPUP pour assigner les élèves sélectionnés à un événement"""
        if not self.selected_students:
            tkinter.messagebox.showwarning("Attention", "Aucun élève sélectionné !")
            return
        
        # Créer la fenêtre popup
        popup = tk.Toplevel(self.view.frame)
        popup.title("Assigner à un événement")
        popup.geometry("500x400")
        popup.configure(bg="#f8f9fa")
        popup.transient(self.view.frame)
        popup.grab_set()
        
        # Centrer la fenêtre
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
        y = (popup.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")
        
        # Titre
        title_frame = tk.Frame(popup, bg="#007bff", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="📅 Assignation à un événement",
                font=("Helvetica", 14, "bold"), fg="white", bg="#007bff").pack(pady=15)
        
        # Corps principal
        main_frame = tk.Frame(popup, bg="#f8f9fa")
        main_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Section élèves sélectionnés
        students_frame = tk.LabelFrame(main_frame, text="👥 Élèves sélectionnés", 
                                      font=("Helvetica", 10, "bold"), bg="#f8f9fa")
        students_frame.pack(fill="x", pady=(0, 15))
        
        # Liste des élèves
        students_text = tk.Text(students_frame, height=6, width=50, 
                               font=("Helvetica", 9), bg="white", wrap=tk.WORD)
        scrollbar = tk.Scrollbar(students_frame, orient="vertical", command=students_text.yview)
        students_text.configure(yscrollcommand=scrollbar.set)
        
        students_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)
        
        # Remplir la liste des élèves
        selected_names = []
        for student in self.students_data:
            if student["id"] in self.selected_students:
                selected_names.append(f"• {student['prenom']} {student['nom']} ({student['classe']})")
        
        students_text.insert("1.0", "\n".join(selected_names))
        students_text.config(state="disabled")
        
        # Section choix d'événement
        event_frame = tk.LabelFrame(main_frame, text="📅 Choisir un événement",
                                   font=("Helvetica", 10, "bold"), bg="#f8f9fa")
        event_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(event_frame, text="Événement:", font=("Helvetica", 9, "bold"),
                bg="#f8f9fa").pack(anchor="w", padx=10, pady=(10, 5))
        
        events_list = []
        try:
            events = self.event_manager.get_events()
            events_list = [f"{event['nom']} - {event['date']} ({event.get('prix', 'N/A')}€)" 
                          for event in events]
        except:
            events_list = ["Aucun événement disponible"]
        
        event_var = tk.StringVar()
        event_combo = ttk.Combobox(event_frame, textvariable=event_var, values=events_list,
                                  state="readonly", width=60, font=("Helvetica", 9))
        event_combo.pack(padx=10, pady=(0, 10), fill="x")
        
        if events_list and events_list[0] != "Aucun événement disponible":
            event_combo.set(events_list[0])
        
        # Boutons d'action
        buttons_frame = tk.Frame(main_frame, bg="#f8f9fa")
        buttons_frame.pack(fill="x", pady=10)
        
        def confirm_assignment():
            if not event_var.get():
                tkinter.messagebox.showwarning("Attention", "Veuillez sélectionner un événement !")
                return
            
            # Ici vous pourriez sauvegarder l'assignation dans votre système
            # self.event_manager.assign_students_to_event(self.selected_students, selected_event_id)
            
            tkinter.messagebox.showinfo("Succès", 
                f"✅ {len(self.selected_students)} élèves assignés à:\n{event_var.get()}")
            popup.destroy()
        
        def cancel_assignment():
            popup.destroy()
        
        tk.Button(buttons_frame, text="✅ Confirmer l'assignation", command=confirm_assignment,
                 bg="#28a745", fg="white", font=("Helvetica", 10, "bold"),
                 relief="flat", padx=20, pady=8).pack(side="right", padx=(5, 0))
        
        tk.Button(buttons_frame, text="❌ Annuler", command=cancel_assignment,
                 bg="#dc3545", fg="white", font=("Helvetica", 10, "bold"),
                 relief="flat", padx=20, pady=8).pack(side="right")
    
    def calculate_event_cost(self):
        """POPUP MODERNE pour calculer les coûts - TAILLE AGRANDIE"""
        if not self.selected_students:
            tkinter.messagebox.showwarning("Attention", "Aucun élève sélectionné !")
            return
        
        # Créer la fenêtre popup avec style moderne - PLUS GRANDE
        popup = tk.Toplevel(self.view.frame)
        popup.title("Calculateur de Coûts d'Événement")
        popup.geometry("600x650")  # ✅ AGRANDI de 550x480 à 600x650
        popup.configure(bg="#ffffff")
        popup.transient(self.view.frame)
        popup.grab_set()
        popup.resizable(False, False)
        
        # Centrer la fenêtre
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
        y = (popup.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")
        
        # ===== HEADER MODERNE =====
        header_frame = tk.Frame(popup, bg="#2c3e50", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg="#2c3e50")
        header_content.pack(fill="both", expand=True, padx=20, pady=15)
        
        tk.Label(header_content, text="💰 Calculateur de Coûts",
                font=("Segoe UI", 16, "bold"), fg="white", bg="#2c3e50").pack(side="left")
        
        student_count_label = tk.Label(header_content, 
                                      text=f"{len(self.selected_students)} élèves sélectionnés",
                                      font=("Segoe UI", 10), fg="#bdc3c7", bg="#2c3e50")
        student_count_label.pack(side="right")
        
        # ===== FRAME AVEC SCROLLBAR POUR LE CONTENU =====
        # Créer un canvas avec scrollbar pour gérer le contenu débordant
        canvas_frame = tk.Frame(popup, bg="#ffffff")
        canvas_frame.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(canvas_frame, bg="#ffffff", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # ===== CORPS PRINCIPAL (dans le frame scrollable) =====
        main_container = tk.Frame(scrollable_frame, bg="#ffffff")
        main_container.pack(fill="both", expand=True, padx=25, pady=20)
        
        # ===== SECTION COÛT DE BASE =====
        cost_card = tk.Frame(main_container, bg="#f8f9fa", relief="flat", bd=1)
        cost_card.pack(fill="x", pady=(0, 15))
        
        cost_header = tk.Frame(cost_card, bg="#3498db", height=35)
        cost_header.pack(fill="x")
        cost_header.pack_propagate(False)
        
        tk.Label(cost_header, text="💵 Coût par Élève", 
                font=("Segoe UI", 11, "bold"), fg="white", bg="#3498db").pack(pady=8)
        
        cost_body = tk.Frame(cost_card, bg="#f8f9fa")
        cost_body.pack(fill="x", padx=15, pady=15)
        
        cost_input_frame = tk.Frame(cost_body, bg="#f8f9fa")
        cost_input_frame.pack(fill="x")
        
        tk.Label(cost_input_frame, text="Coût de base:", 
                font=("Segoe UI", 10), bg="#f8f9fa", fg="#2c3e50").pack(side="left")
        
        base_cost_var = tk.StringVar(value="15.50")
        cost_entry = tk.Entry(cost_input_frame, textvariable=base_cost_var, 
                             font=("Segoe UI", 11), width=10, justify="center",
                             relief="flat", bd=5, bg="white")
        cost_entry.pack(side="right")
        
        tk.Label(cost_input_frame, text="€", 
                font=("Segoe UI", 11, "bold"), bg="#f8f9fa", fg="#27ae60").pack(side="right", padx=(5, 10))
        
        # ===== SECTION ARGENT RÉCOLTÉ =====
        money_card = tk.Frame(main_container, bg="#f8f9fa", relief="flat", bd=1)
        money_card.pack(fill="x", pady=(0, 20))  # ✅ Plus d'espace
        
        money_header = tk.Frame(money_card, bg="#27ae60", height=35)
        money_header.pack(fill="x")
        money_header.pack_propagate(False)
        
        tk.Label(money_header, text="💸 Argent Récolté", 
                font=("Segoe UI", 11, "bold"), fg="white", bg="#27ae60").pack(pady=8)
        
        money_body = tk.Frame(money_card, bg="#f8f9fa")
        money_body.pack(fill="x", padx=15, pady=15)
        
        # Checkbox moderne
        money_enabled_var = tk.BooleanVar()
        money_checkbox = tk.Checkbutton(money_body, 
                                       text="Les élèves ont récolté de l'argent (ventes, dons, etc.)",
                                       variable=money_enabled_var, 
                                       font=("Segoe UI", 10), bg="#f8f9fa", fg="#2c3e50",
                                       activebackground="#f8f9fa", activeforeground="#2c3e50",
                                       command=lambda: toggle_money_input())
        money_checkbox.pack(anchor="w", pady=(0, 10))
        
        # Frame pour l'input d'argent
        money_input_frame = tk.Frame(money_body, bg="#f8f9fa")
        
        money_label_frame = tk.Frame(money_input_frame, bg="#f8f9fa")
        money_label_frame.pack(fill="x", pady=(0, 5))
        
        tk.Label(money_label_frame, text="Montant total récolté:", 
                font=("Segoe UI", 10), bg="#f8f9fa", fg="#2c3e50").pack(side="left")
        
        # Container pour l'input et le bouton de validation
        money_controls_frame = tk.Frame(money_input_frame, bg="#f8f9fa")
        money_controls_frame.pack(fill="x", pady=(5, 0))
        
        money_amount_var = tk.StringVar(value="0.00")
        money_entry = tk.Entry(money_controls_frame, textvariable=money_amount_var,
                              font=("Segoe UI", 11), width=12, justify="center",
                              relief="flat", bd=5, bg="white")
        money_entry.pack(side="left")
        
        tk.Label(money_controls_frame, text="€", 
                font=("Segoe UI", 11, "bold"), bg="#f8f9fa", fg="#27ae60").pack(side="left", padx=(5, 10))
        
        # Bouton de validation avec statut
        money_validated = tk.BooleanVar(value=False)
        
        def validate_money():
            try:
                amount = float(money_amount_var.get())
                if amount < 0:
                    tkinter.messagebox.showerror("Erreur", "Le montant ne peut pas être négatif !")
                    return
                
                money_validated.set(True)
                validate_btn.config(text="✓ Validé", bg="#27ae60", state="disabled")
                money_entry.config(state="disabled", bg="#f8f9fa")
                
                # Message de confirmation
                status_label.config(text=f"✅ Argent validé: {amount:.2f}€", fg="#27ae60")
                status_label.pack(fill="x", pady=(5, 0))
                
                calculate_costs()
                
            except ValueError:
                tkinter.messagebox.showerror("Erreur", "Veuillez entrer un montant valide !")
        
        def reset_money_validation():
            money_validated.set(False)
            validate_btn.config(text="✓ Valider", bg="#007bff", state="normal")
            money_entry.config(state="normal", bg="white")
            status_label.pack_forget()
            calculate_costs()
        
        validate_btn = tk.Button(money_controls_frame, text="✓ Valider", 
                                command=validate_money,
                                bg="#007bff", fg="white", font=("Segoe UI", 9, "bold"),
                                relief="flat", padx=15, pady=5, cursor="hand2")
        validate_btn.pack(side="right")
        
        # Bouton reset
        reset_btn = tk.Button(money_controls_frame, text="↻ Modifier", 
                             command=reset_money_validation,
                             bg="#6c757d", fg="white", font=("Segoe UI", 8),
                             relief="flat", padx=10, pady=5, cursor="hand2")
        
        # Label de statut
        status_label = tk.Label(money_input_frame, text="", 
                               font=("Segoe UI", 9), bg="#f8f9fa")
        
        def toggle_money_input():
            if money_enabled_var.get():
                money_input_frame.pack(fill="x", pady=(5, 0))
                money_entry.focus()
                reset_money_validation()
            else:
                money_input_frame.pack_forget()
                money_amount_var.set("0.00")
                reset_money_validation()
        
        # Callback pour afficher le bouton reset
        def on_money_validated(*args):
            if money_validated.get():
                reset_btn.pack(side="right", padx=(5, 0))
            else:
                reset_btn.pack_forget()
        
        money_validated.trace('w', on_money_validated)
        
        # ===== RÉSULTATS MODERNES - PLUS D'ESPACE =====
        results_card = tk.Frame(main_container, bg="#f8f9fa", relief="flat", bd=1)
        results_card.pack(fill="x", pady=(0, 20))
        
        results_header = tk.Frame(results_card, bg="#e74c3c", height=35)
        results_header.pack(fill="x")
        results_header.pack_propagate(False)
        
        tk.Label(results_header, text="📊 Résultats du Calcul", 
                font=("Segoe UI", 11, "bold"), fg="white", bg="#e74c3c").pack(pady=8)
        
        results_body = tk.Frame(results_card, bg="white")
        results_body.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Zone de résultats - PLUS D'ESPACE
        results_display = tk.Frame(results_body, bg="white")
        results_display.pack(fill="both", expand=True)
        
        # Variables pour les résultats avec plus d'espace
        self.base_total_label = tk.Label(results_display, text="", 
                                        font=("Segoe UI", 12), bg="white", fg="#2c3e50", anchor="w")
        self.base_total_label.pack(fill="x", pady=5)  # ✅ Plus d'espace
        
        self.money_collected_label = tk.Label(results_display, text="", 
                                             font=("Segoe UI", 12), bg="white", fg="#27ae60", anchor="w")
        
        # Séparateur
        separator = tk.Frame(results_display, height=3, bg="#ecf0f1")  # ✅ Plus épais
        separator.pack(fill="x", pady=15)  # ✅ Plus d'espace
        
        self.final_total_label = tk.Label(results_display, text="", 
                                         font=("Segoe UI", 14, "bold"), bg="white", fg="#e74c3c", anchor="w")
        self.final_total_label.pack(fill="x", pady=8)  # ✅ Plus d'espace
        
        self.per_student_label = tk.Label(results_display, text="", 
                                         font=("Segoe UI", 12), bg="white", fg="#7f8c8d", anchor="w")
        self.per_student_label.pack(fill="x", pady=5)  # ✅ Plus d'espace
        
        # Zone pour message spécial
        self.special_message_label = tk.Label(results_display, text="", 
                                             font=("Segoe UI", 12, "bold"), bg="white", fg="#27ae60", anchor="w",
                                             wraplength=500)  # ✅ Wrapping pour texte long
        self.special_message_label.pack(fill="x", pady=(15, 0))  # ✅ Plus d'espace
        
        def calculate_costs():
            try:
                base_cost = float(base_cost_var.get())
                num_students = len(self.selected_students)
                
                # Utiliser l'argent seulement si validé
                money_collected = 0.0
                if money_enabled_var.get() and money_validated.get():
                    money_collected = float(money_amount_var.get())
                
                # Calculs
                total_base_cost = num_students * base_cost
                final_cost = total_base_cost - money_collected
                cost_per_student = final_cost / num_students if num_students > 0 else 0
                
                # Mise à jour des labels avec plus de clarté
                self.base_total_label.config(text=f"💵 Coût total de base: {total_base_cost:.2f}€")
                
                if money_enabled_var.get() and money_validated.get() and money_collected > 0:
                    self.money_collected_label.config(text=f"💸 Argent récolté: -{money_collected:.2f}€")
                    self.money_collected_label.pack(fill="x", pady=5)
                else:
                    self.money_collected_label.pack_forget()
                
                # Couleur selon le résultat
                if final_cost <= 0:
                    color = "#27ae60"  # Vert
                    self.final_total_label.config(fg=color)
                    self.special_message_label.config(text="🎉 Excellent ! L'argent récolté couvre entièrement les coûts !")
                    self.special_message_label.pack(fill="x", pady=(15, 0))
                elif final_cost < total_base_cost:
                    color = "#f39c12"  # Orange
                    self.final_total_label.config(fg=color)
                    savings = total_base_cost - final_cost
                    self.special_message_label.config(text=f"💰 Économie réalisée: {savings:.2f}€ grâce aux ventes !", fg="#f39c12")
                    self.special_message_label.pack(fill="x", pady=(15, 0))
                else:
                    color = "#e74c3c"  # Rouge
                    self.final_total_label.config(fg=color)
                    self.special_message_label.pack_forget()
                
                self.final_total_label.config(text=f"🏷️ COÛT FINAL TOTAL: {max(0, final_cost):.2f}€")
                self.per_student_label.config(text=f"👤 Coût par élève: {max(0, cost_per_student):.2f}€")
                
            except ValueError:
                self.base_total_label.config(text="❌ Veuillez entrer des valeurs numériques valides")
                self.money_collected_label.pack_forget()
                self.final_total_label.config(text="")
                self.per_student_label.config(text="")
                self.special_message_label.pack_forget()
        
        # Callback pour calcul automatique
        base_cost_var.trace('w', lambda *args: calculate_costs())
        
        # ===== BOUTONS D'ACTION =====
        buttons_frame = tk.Frame(main_container, bg="#ffffff")
        buttons_frame.pack(fill="x", pady=(20, 0))
        
        # Bouton Fermer
        close_btn = tk.Button(buttons_frame, text="✓ Fermer", command=popup.destroy,
                             bg="#95a5a6", fg="white", font=("Segoe UI", 11, "bold"),
                             relief="flat", padx=25, pady=10, cursor="hand2",
                             activebackground="#7f8c8d", activeforeground="white")
        close_btn.pack(side="right")
        
        # ===== FINALISER LE CANVAS =====
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Binding pour la molette de la souris
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Calcul initial
        calculate_costs()
        
        # Focus sur le canvas pour permettre le scroll
        canvas.focus_set()
    
    # ====================== AUTRES ACTIONS ======================
    def view_student(self, student_id):
        """Affiche les détails d'un élève"""
        student = next((s for s in self.students_data if s["id"] == student_id), None)
        if student:
            info = f"Élève: {student['prenom']} {student['nom']}\n"
            info += f"Classe: {student['classe']}\n"
            info += f"Année: {student['annee']}ème\n"
            info += f"Événements: {self.get_student_events(student)}"
            tkinter.messagebox.showinfo("Détails de l'élève", info)
    
    def edit_student(self, student_id):
        """Modifie un élève"""
        tkinter.messagebox.showinfo("Info", f"Fonction de modification élève ID {student_id} à développer")
    
    def delete_student(self, student_id):
        """Supprime un élève"""
        result = tkinter.messagebox.askyesno("Confirmation", f"Supprimer l'élève ID {student_id} ?")
        if result:
            tkinter.messagebox.showinfo("Info", "Fonction de suppression à développer")
    
    def export_filtered_data(self):
        """Exporte les données filtrées"""
        if not self.filtered_students:
            tkinter.messagebox.showwarning("Attention", "Aucune donnée à exporter !")
            return
        
        tkinter.messagebox.showinfo("Export", f"Export de {len(self.filtered_students)} élèves (fonctionnalité à développer)")