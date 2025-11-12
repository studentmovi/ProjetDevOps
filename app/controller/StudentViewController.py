import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog
import pandas as pd
from datetime import datetime
import os
from data.sample_data import get_all_students, get_available_years, get_available_classes, get_classes_by_year
from data.event_data_manager import event_manager

class StudentViewController:
    """Contrôleur pour la gestion de la vue des élèves"""
    
    def __init__(self, view):
        self.view = view
        self.students_data = get_all_students()
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
        self.students_data = get_all_students()
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
            "Sortie Théâtre": ["6A", "6B"],
            "Visite Musée": ["5A", "5B", "5C"], 
            "Concert": ["4A", "3A", "3B"],
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
    def on_year_changed(self, event=None):
        selected_year = self.view.filter_panel.get_filter_value("year")
        
        if selected_year == "Toutes":
            available_classes = ["Toutes"] + get_available_classes()
        else:
            available_classes = ["Toutes"] + get_classes_by_year(selected_year)
        
        self.view.class_combo.configure(values=available_classes)
        self.view.filter_panel.set_filter_value("class", "Toutes")
        self.apply_all_filters()
    
    def on_filter_changed(self, event=None):
        self.apply_all_filters()
    
    def on_search_changed(self, *args):
        self.apply_all_filters()
    
    def on_sort_changed(self, event=None):
        self.apply_all_filters()
    
    def on_event_changed(self, event=None):
        selected_event = self.view.filter_panel.get_filter_value("event")
        
        if selected_event != "Aucun":
            concerned_classes = self.get_classes_for_event(selected_event)
            self.auto_select_students_by_classes(concerned_classes)
        
        self.apply_all_filters()
    
    def auto_select_students_by_classes(self, classes):
        if not classes:
            return
            
        self.selected_students = []
        for student in self.students_data:
            if student["classe"] in classes:
                self.selected_students.append(student["id"])
    
    def apply_all_filters(self):
        selected_year = self.view.filter_panel.get_filter_value("year")
        selected_class = self.view.filter_panel.get_filter_value("class")
        search_text = self.view.filter_panel.get_filter_value("search").lower()
        selected_event = self.view.filter_panel.get_filter_value("event")
        sort_type = self.view.filter_panel.get_filter_value("sort")
        
        self.filtered_students = []
        
        for student in self.students_data:
            if selected_year != "Toutes" and student["annee"] != selected_year:
                continue
            
            if selected_class != "Toutes" and student["classe"] != selected_class:
                continue
            
            if selected_event != "Aucun":
                concerned_classes = self.get_classes_for_event(selected_event)
                if student["classe"] not in concerned_classes:
                    continue
            
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
        
        self.view.update_display()
    
    def reset_filters(self):
        self.view.filter_panel.reset_all_filters()
        self.view.class_combo.configure(values=["Toutes"] + get_available_classes())
        self.filtered_students = self.students_data.copy()
        self.selected_students = []
        self.view.update_display()
    
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
    
    # ====================== ACTIONS PRINCIPALES ======================
    def assign_to_event(self):
        """Assigne les élèves sélectionnés à un événement"""
        if not self.selected_students:
            tkinter.messagebox.showwarning("Attention", "Aucun élève sélectionné !")
            return
        
        self.show_event_assignment_dialog()
    
    def calculate_event_cost(self):
        """Ouvre la fenêtre de gestion des coûts par événement"""
        self.show_event_management_dialog()
    
    def show_event_assignment_dialog(self):
        """Fenêtre d'assignation à un événement"""
        dialog = tk.Toplevel(self.view.parent)
        dialog.title("Assigner à un événement")
        dialog.geometry("500x400")
        dialog.transient(self.view.parent)
        dialog.grab_set()
        
        # Titre
        title_label = tk.Label(dialog, 
                             text=f"📅 Assigner {len(self.selected_students)} élève(s)",
                             font=("Helvetica", 14, "bold"),
                             fg="#2c3e50")
        title_label.pack(pady=15)
        
        main_frame = tk.Frame(dialog, bg="#f8f9fa")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Sélection d'événement
        event_frame = tk.LabelFrame(main_frame, text="Sélectionner un événement", 
                                  font=("Helvetica", 10, "bold"), bg="#f8f9fa")
        event_frame.pack(fill="x", pady=(0, 15))
        
        event_var = tk.StringVar()
        events = self.event_manager.get_events()
        
        for event in events:
            nb_participants = len(event["participants"])
            prix_actuel = event["cout_total"] / max(1, nb_participants)
            
            rb_text = f"📅 {event['nom']} ({event['date']}) - {event['cout_total']}€ total"
            if nb_participants > 0:
                rb_text += f" - {prix_actuel:.2f}€/élève actuel"
            
            rb = tk.Radiobutton(event_frame, 
                              text=rb_text,
                              variable=event_var, 
                              value=event["id"],
                              font=("Helvetica", 9),
                              bg="#f8f9fa",
                              wraplength=450)
            rb.pack(anchor="w", pady=3, padx=10)
        
        # Liste des élèves sélectionnés
        students_frame = tk.LabelFrame(main_frame, text="Élèves à assigner",
                                     font=("Helvetica", 10, "bold"), bg="#f8f9fa")
        students_frame.pack(fill="both", expand=True)
        
        students_text = tk.Text(students_frame, height=8, font=("Helvetica", 9))
        students_scrollbar = tk.Scrollbar(students_frame, orient="vertical", command=students_text.yview)
        students_text.configure(yscrollcommand=students_scrollbar.set)
        
        selected_students_info = []
        for student in self.students_data:
            if student['id'] in self.selected_students:
                selected_students_info.append(f"• {student['prenom']} {student['nom']} ({student['classe']})")
        
        students_text.insert("1.0", "\n".join(selected_students_info))
        students_text.config(state="disabled")
        
        students_text.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        students_scrollbar.pack(side="right", fill="y")
        
        # Boutons
        buttons_frame = tk.Frame(dialog, bg="#f8f9fa")
        buttons_frame.pack(pady=15)
        
        def confirm_assignment():
            selected_event_id = event_var.get()
            if selected_event_id:
                # Assigner chaque élève à l'événement
                for student_id in self.selected_students:
                    self.event_manager.assign_student_to_event(student_id, selected_event_id)
                
                tkinter.messagebox.showinfo("Succès", 
                    f"✅ {len(self.selected_students)} élève(s) assigné(s) avec succès !")
                self.view.update_display()
                dialog.destroy()
            else:
                tkinter.messagebox.showwarning("Attention", "Veuillez sélectionner un événement !")
        
        from component.Button import ActionButton
        ActionButton(buttons_frame, "Confirmer l'assignation", 
                    command=confirm_assignment, action_type='save').create().pack(side="left", padx=5)
        
        ActionButton(buttons_frame, "Annuler", 
                    command=dialog.destroy, action_type='cancel').create().pack(side="left", padx=5)
    
    def show_event_management_dialog(self):
        """Fenêtre de gestion complète des événements avec focus sur les ventes"""
        dialog = tk.Toplevel(self.view.parent)
        dialog.title("💰 Gestion des Événements et Ventes")
        dialog.geometry("900x700")
        dialog.transient(self.view.parent)
        dialog.grab_set()
        
        # Titre
        title_label = tk.Label(dialog, 
                             text="💰 Gestion des Événements, Ventes et Prix",
                             font=("Helvetica", 14, "bold"),
                             fg="#2c3e50")
        title_label.pack(pady=15)
        
        # Notebook pour onglets
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Onglet pour chaque événement avec gestion des ventes
        events = self.event_manager.get_events()
        for event in events:
            self.create_event_sales_tab(notebook, event)
        
        # Onglet résumé général
        self.create_summary_tab(notebook)
        
        # Boutons en bas
        buttons_frame = tk.Frame(dialog)
        buttons_frame.pack(pady=15)
        
        from component.Button import ActionButton
        ActionButton(buttons_frame, "💾 Sauvegarder", 
                    command=self.event_manager.save_data, action_type='save').create().pack(side="left", padx=5)
        
        ActionButton(buttons_frame, "📊 Exporter Excel", 
                    command=self.export_to_excel, action_type='export').create().pack(side="left", padx=5)
        
        ActionButton(buttons_frame, "🔄 Actualiser", 
                    command=lambda: self.refresh_event_dialog(dialog), action_type='refresh').create().pack(side="left", padx=5)
        
        ActionButton(buttons_frame, "Fermer", 
                    command=dialog.destroy, action_type='cancel').create().pack(side="left", padx=5)
    
    def create_event_sales_tab(self, notebook, event):
        """Crée un onglet dédié à la gestion des ventes d'un événement"""
        tab_frame = ttk.Frame(notebook)
        ventes_status = "🔴" if not event.get('ventes_activees', False) else "🟢"
        notebook.add(tab_frame, text=f"{ventes_status} {event['nom']} ({len(event['participants'])})")
        
        # ==================== SECTION INFORMATIONS GÉNÉRALES ====================
        info_frame = tk.LabelFrame(tab_frame, text="📋 Informations de l'événement", 
                                 font=("Helvetica", 11, "bold"))
        info_frame.pack(fill="x", padx=10, pady=5)
        
        # Container pour informations sur 2 colonnes
        info_container = tk.Frame(info_frame, bg="#f8f9fa")
        info_container.pack(fill="x", padx=10, pady=10)
        
        # Colonne gauche
        left_info = tk.Frame(info_container, bg="#f8f9fa")
        left_info.pack(side="left", fill="both", expand=True)
        
        info_left_text = f"📅 Date: {event['date']}\n"
        info_left_text += f"💰 Coût total: {event['cout_total']}€\n"
        info_left_text += f"👥 Participants: {len(event['participants'])}"
        
        tk.Label(left_info, text=info_left_text, font=("Helvetica", 10), 
                justify="left", bg="#f8f9fa").pack(anchor="w")
        
        # Colonne droite
        right_info = tk.Frame(info_container, bg="#f8f9fa")
        right_info.pack(side="right", fill="both", expand=True)
        
        if event['participants']:
            prix_base = event['cout_total'] / len(event['participants'])
            total_ventes = event.get('total_ventes', 0.0)
            reduction = total_ventes / len(event['participants']) if event.get('ventes_activees', False) else 0
            prix_final = prix_base - reduction
            
            info_right_text = f"💶 Prix de base: {prix_base:.2f}€/élève\n"
            info_right_text += f"🏪 Ventes: {total_ventes:.2f}€\n"
            info_right_text += f"🎯 Prix final: {prix_final:.2f}€/élève"
        else:
            info_right_text = "Aucun participant assigné"
        
        tk.Label(right_info, text=info_right_text, font=("Helvetica", 10), 
                justify="left", bg="#f8f9fa").pack(anchor="w")
        
        # ==================== SECTION GESTION DES VENTES ====================
        sales_frame = tk.LabelFrame(tab_frame, text="🏪 Gestion des Ventes", 
                                  font=("Helvetica", 11, "bold"))
        sales_frame.pack(fill="x", padx=10, pady=5)
        
        sales_container = tk.Frame(sales_frame, bg="#f0f8ff")
        sales_container.pack(fill="x", padx=10, pady=10)
        
        # Activation/désactivation des ventes
        ventes_activees = event.get('ventes_activees', False)
        ventes_var = tk.BooleanVar(value=ventes_activees)
        
        checkbox_frame = tk.Frame(sales_container, bg="#f0f8ff")
        checkbox_frame.pack(fill="x", pady=(0, 10))
        
        ventes_checkbox = tk.Checkbutton(checkbox_frame,
                                       text="✅ Activer les ventes pour cet événement",
                                       variable=ventes_var,
                                       font=("Helvetica", 10, "bold"),
                                       bg="#f0f8ff",
                                       command=lambda: self.toggle_event_sales(event['id'], ventes_var.get()))
        ventes_checkbox.pack(side="left")
        
        # Configuration du montant des ventes (seulement si activé)
        sales_config_frame = tk.Frame(sales_container, bg="#f0f8ff")
        sales_config_frame.pack(fill="x")
        
        tk.Label(sales_config_frame, text="💰 Total des ventes récoltées (€):",
                font=("Helvetica", 10), bg="#f0f8ff").pack(side="left")
        
        sales_var = tk.StringVar(value=str(event.get('total_ventes', 0.0)))
        sales_entry = tk.Entry(sales_config_frame, textvariable=sales_var, 
                             width=15, font=("Helvetica", 10))
        sales_entry.pack(side="left", padx=10)
        
        def update_sales():
            if not ventes_var.get():
                tkinter.messagebox.showwarning("Attention", "Activez d'abord les ventes pour cet événement !")
                return
            
            try:
                total_ventes = float(sales_var.get() or "0")
                self.event_manager.update_event_sales_total(event['id'], total_ventes)
                tkinter.messagebox.showinfo("Succès", f"Ventes mises à jour : {total_ventes}€")
                self.refresh_event_dialog(notebook.master)
            except ValueError:
                tkinter.messagebox.showerror("Erreur", "Montant invalide !")
        
        from component.Button import ActionButton
        ActionButton(sales_config_frame, "Mettre à jour", 
                    command=update_sales, action_type='save').create().pack(side="left", padx=5)
        
        # État initial des champs
        if not ventes_activees:
            sales_entry.config(state="disabled")
        
        # ==================== SECTION COÛT TOTAL ====================
        cost_frame = tk.LabelFrame(tab_frame, text="💰 Modifier le coût total",
                                 font=("Helvetica", 11, "bold"))
        cost_frame.pack(fill="x", padx=10, pady=5)
        
        cost_container = tk.Frame(cost_frame, bg="#fff3e0")
        cost_container.pack(fill="x", padx=10, pady=10)
        
        tk.Label(cost_container, text="Nouveau coût total (€):",
                font=("Helvetica", 10), bg="#fff3e0").pack(side="left")
        
        cost_var = tk.StringVar(value=str(event['cout_total']))
        cost_entry = tk.Entry(cost_container, textvariable=cost_var, width=15, font=("Helvetica", 10))
        cost_entry.pack(side="left", padx=10)
        
        def update_cost():
            try:
                new_cost = float(cost_var.get())
                event['cout_total'] = new_cost
                self.event_manager.calculate_event_prices(event['id'])
                tkinter.messagebox.showinfo("Succès", "Coût mis à jour !")
                self.refresh_event_dialog(notebook.master)
            except ValueError:
                tkinter.messagebox.showerror("Erreur", "Montant invalide !")
        
        ActionButton(cost_container, "Mettre à jour coût", 
                    command=update_cost, action_type='save').create().pack(side="left", padx=5)
        
        # ==================== TABLEAU DES PARTICIPANTS ====================
        if event['participants']:
            participants_frame = tk.LabelFrame(tab_frame, text="👥 Liste des Participants",
                                             font=("Helvetica", 11, "bold"))
            participants_frame.pack(fill="both", expand=True, padx=10, pady=5)
            
            # Tableau des participants
            columns = ("Nom", "Prénom", "Classe", "Prix de Base (€)", "Prix Final (€)", "Économie (€)")
            tree = ttk.Treeview(participants_frame, columns=columns, show="headings", height=12)
            
            # Configuration des colonnes
            tree.heading("Nom", text="👤 Nom")
            tree.heading("Prénom", text="👤 Prénom")
            tree.heading("Classe", text="🏫 Classe")
            tree.heading("Prix de Base (€)", text="💰 Prix Base")
            tree.heading("Prix Final (€)", text="🎯 Prix Final")
            tree.heading("Économie (€)", text="💸 Économie")
            
            for col in ["Prix de Base (€)", "Prix Final (€)", "Économie (€)"]:
                tree.column(col, width=100, anchor="center")
            for col in ["Nom", "Prénom", "Classe"]:
                tree.column(col, width=120)
            
            # Remplir le tableau
            for student_id, participant_data in event['participants'].items():
                student = next((s for s in self.students_data if s["id"] == int(student_id)), None)
                if student:
                    prix_base = participant_data.get('prix_base', 0)
                    prix_final = participant_data.get('prix_final', 0)
                    economie = prix_base - prix_final
                    
                    tree.insert("", "end", values=(
                        student["nom"],
                        student["prenom"], 
                        student["classe"],
                        f"{prix_base:.2f}",
                        f"{prix_final:.2f}",
                        f"{economie:.2f}"
                    ))
            
            # Scrollbar pour le tableau
            scrollbar = ttk.Scrollbar(participants_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
            scrollbar.pack(side="right", fill="y")
    
    def toggle_event_sales(self, event_id, enabled):
        """Active/désactive les ventes pour un événement"""
        self.event_manager.toggle_event_sales(event_id, enabled)
        
        # Rafraîchir l'interface
        self.refresh_event_dialog(None)  # On va recréer la fenêtre
        
        status = "activées" if enabled else "désactivées"
        tkinter.messagebox.showinfo("Ventes", f"Ventes {status} pour cet événement")
    
    def create_summary_tab(self, notebook):
        """Crée l'onglet de résumé général avec statistiques mises à jour"""
        tab_frame = ttk.Frame(notebook)
        notebook.add(tab_frame, text="📊 Résumé Général")
        
        # Statistiques générales
        stats_frame = tk.LabelFrame(tab_frame, text="Statistiques Globales",
                                  font=("Helvetica", 12, "bold"))
        stats_frame.pack(fill="x", padx=10, pady=10)
        
        events = self.event_manager.get_events()
        total_events = len(events)
        total_participants = sum(len(event['participants']) for event in events)
        total_cost = sum(event['cout_total'] for event in events)
        total_sales = sum(event.get('total_ventes', 0.0) for event in events)  # CORRIGÉ
        
        stats_text = f"🎉 Nombre total d'événements: {total_events}\n"
        stats_text += f"👥 Total des participations: {total_participants}\n"
        stats_text += f"💰 Coût total des événements: {total_cost:.2f}€\n"
        stats_text += f"🏪 Total des ventes: {total_sales:.2f}€\n"
        stats_text += f"📉 Économies réalisées: {total_sales:.2f}€"
        
        stats_label = tk.Label(stats_frame, text=stats_text, font=("Helvetica", 11),
                             justify="left", bg="#f0f8ff")
        stats_label.pack(padx=20, pady=15)
        
        # Tableau récapitulatif
        recap_frame = tk.LabelFrame(tab_frame, text="Récapitulatif par Événement",
                                  font=("Helvetica", 12, "bold"))
        recap_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("Événement", "Date", "Participants", "Coût Total", "Ventes", "Prix Final Moyen")
        tree = ttk.Treeview(recap_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            tree.heading(col, text=col)
            if col in ["Coût Total", "Ventes", "Prix Final Moyen"]:
                tree.column(col, width=120, anchor="center")
            else:
                tree.column(col, width=150)
        
        for event in events:
            nb_participants = len(event['participants'])
            total_ventes_event = event.get('total_ventes', 0.0)  # CORRIGÉ
            prix_moyen = sum(p.get('prix_final', 0) for p in event['participants'].values()) / max(1, nb_participants)
            
            tree.insert("", "end", values=(
                event['nom'],
                event['date'],
                nb_participants,
                f"{event['cout_total']:.2f}€",
                f"{total_ventes_event:.2f}€",
                f"{prix_moyen:.2f}€"
            ))
        
        tree.pack(fill="both", expand=True, padx=5, pady=5)
    
    def refresh_event_dialog(self, dialog):
        """Actualise la fenêtre de gestion des événements"""
        if dialog:
            dialog.destroy()
        self.show_event_management_dialog()
    
    def export_to_excel(self):
        """Exporte toutes les données vers Excel avec structure mise à jour"""
        try:
            # Demander où sauvegarder
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Sauvegarder les données des événements"
            )
            
            if not filename:
                return
            
            # Préparer les données
            events = self.event_manager.get_events()
            
            # Créer un dictionnaire pour chaque feuille
            excel_data = {}
            
            # Feuille de résumé général
            summary_data = []
            for event in events:
                nb_participants = len(event['participants'])
                total_ventes = event.get('total_ventes', 0.0)  # CORRIGÉ
                prix_moyen = sum(p.get('prix_final', 0) for p in event['participants'].values()) / max(1, nb_participants)
                
                summary_data.append({
                    'Événement': event['nom'],
                    'Date': event['date'],
                    'Coût Total (€)': event['cout_total'],
                    'Nombre Participants': nb_participants,
                    'Ventes Activées': "Oui" if event.get('ventes_activees', False) else "Non",
                    'Total Ventes (€)': total_ventes,
                    'Prix Final Moyen (€)': round(prix_moyen, 2)
                })
            
            excel_data['Résumé'] = pd.DataFrame(summary_data)
            
            # Une feuille par événement
            for event in events:
                event_data = []
                for student_id, participant_data in event['participants'].items():
                    student = next((s for s in self.students_data if s["id"] == int(student_id)), None)
                    if student:
                        event_data.append({
                            'Nom': student['nom'],
                            'Prénom': student['prenom'],
                            'Classe': student['classe'],
                            'Année': f"{student['annee']}ème",
                            'Prix de Base (€)': round(participant_data.get('prix_base', 0), 2),
                            'Prix Final (€)': round(participant_data.get('prix_final', 0), 2),
                            'Économie (€)': round(participant_data.get('prix_base', 0) - participant_data.get('prix_final', 0), 2)
                        })
                
                if event_data:
                    excel_data[event['nom'][:30]] = pd.DataFrame(event_data)  # Limite Excel pour noms feuilles
            
            # Écrire dans Excel
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                for sheet_name, df in excel_data.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            tkinter.messagebox.showinfo("Succès", f"✅ Données exportées vers:\n{filename}")
            
        except Exception as e:
            tkinter.messagebox.showerror("Erreur", f"Erreur lors de l'export:\n{str(e)}")
    
    def export_filtered_data(self):
        """Exporte les données filtrées"""
        tkinter.messagebox.showinfo("Export", f"Export de {len(self.filtered_students)} élèves filtrés")
    
    # ====================== ACTIONS SECONDAIRES ======================
    def view_student(self, student_id):
        student = next((s for s in self.students_data if s["id"] == student_id), None)
        if student:
            events = self.get_student_events(student)
            info = f"Élève: {student['prenom']} {student['nom']}\n"
            info += f"Classe: {student['classe']}\n"
            info += f"Année: {student['annee']}ème\n"
            info += f"Événements: {events}"
            tkinter.messagebox.showinfo("Détails de l'élève", info)
    
    def edit_student(self, student_id):
        tkinter.messagebox.showinfo("Modifier", f"Modification de l'élève ID: {student_id}")
    
    def delete_student(self, student_id):
        result = tkinter.messagebox.askyesno("Confirmation", 
            f"Êtes-vous sûr de vouloir supprimer l'élève ID: {student_id} ?")
        if result:
            tkinter.messagebox.showinfo("Suppression", f"Élève ID: {student_id} supprimé")