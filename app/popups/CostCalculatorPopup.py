import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

class CostCalculatorPopup:
    """Popup moderne pour calculer les coûts d'événement"""
    
    def __init__(self, parent, selected_students):
        self.parent = parent
        self.selected_students = selected_students
        self.popup = None
        
        # Variables de l'interface
        self.base_cost_var = None
        self.money_enabled_var = None
        self.money_amount_var = None
        self.money_validated = None
        
        # Labels de résultats
        self.base_total_label = None
        self.money_collected_label = None
        self.final_total_label = None
        self.per_student_label = None
        self.special_message_label = None
    
    def show(self):
        """Affiche le popup"""
        # Créer la fenêtre popup
        self.popup = tk.Toplevel(self.parent)
        self.popup.title("Calculateur de Coûts d'Événement")
        self.popup.geometry("600x650")
        self.popup.configure(bg="#ffffff")
        self.popup.transient(self.parent)
        self.popup.grab_set()
        self.popup.resizable(False, False)
        
        # Centrer la fenêtre
        self._center_window()
        
        # Créer l'interface
        self._create_header()
        self._create_scrollable_content()
    
    def _center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.popup.update_idletasks()
        x = (self.popup.winfo_screenwidth() // 2) - (self.popup.winfo_width() // 2)
        y = (self.popup.winfo_screenheight() // 2) - (self.popup.winfo_height() // 2)
        self.popup.geometry(f"+{x}+{y}")
    
    def _create_header(self):
        """Crée le header moderne"""
        header_frame = tk.Frame(self.popup, bg="#2c3e50", height=60)
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
    
    def _create_scrollable_content(self):
        """Crée le contenu avec scrollbar"""
        # Frame avec scrollbar
        canvas_frame = tk.Frame(self.popup, bg="#ffffff")
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
        
        # Contenu principal
        main_container = tk.Frame(scrollable_frame, bg="#ffffff")
        main_container.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Créer les sections
        self._create_cost_section(main_container)
        self._create_money_section(main_container)
        self._create_results_section(main_container)
        self._create_buttons_section(main_container)
        
        # Finaliser le canvas
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Binding pour la molette
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Focus et calcul initial
        canvas.focus_set()
        self._calculate_costs()
    
    def _create_cost_section(self, parent):
        """Crée la section coût de base"""
        cost_card = tk.Frame(parent, bg="#f8f9fa", relief="flat", bd=1)
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
        
        self.base_cost_var = tk.StringVar(value="15.50")
        cost_entry = tk.Entry(cost_input_frame, textvariable=self.base_cost_var, 
                             font=("Segoe UI", 11), width=10, justify="center",
                             relief="flat", bd=5, bg="white")
        cost_entry.pack(side="right")
        
        tk.Label(cost_input_frame, text="€", 
                font=("Segoe UI", 11, "bold"), bg="#f8f9fa", fg="#27ae60").pack(side="right", padx=(5, 10))
        
        # Callback pour calcul automatique
        self.base_cost_var.trace('w', lambda *args: self._calculate_costs())
    
    def _create_money_section(self, parent):
        """Crée la section argent récolté"""
        money_card = tk.Frame(parent, bg="#f8f9fa", relief="flat", bd=1)
        money_card.pack(fill="x", pady=(0, 20))
        
        money_header = tk.Frame(money_card, bg="#27ae60", height=35)
        money_header.pack(fill="x")
        money_header.pack_propagate(False)
        
        tk.Label(money_header, text="💸 Argent Récolté", 
                font=("Segoe UI", 11, "bold"), fg="white", bg="#27ae60").pack(pady=8)
        
        money_body = tk.Frame(money_card, bg="#f8f9fa")
        money_body.pack(fill="x", padx=15, pady=15)
        
        # Checkbox
        self.money_enabled_var = tk.BooleanVar()
        money_checkbox = tk.Checkbutton(money_body, 
                                       text="Les élèves ont récolté de l'argent (ventes, dons, etc.)",
                                       variable=self.money_enabled_var, 
                                       font=("Segoe UI", 10), bg="#f8f9fa", fg="#2c3e50",
                                       activebackground="#f8f9fa", activeforeground="#2c3e50",
                                       command=self._toggle_money_input)
        money_checkbox.pack(anchor="w", pady=(0, 10))
        
        # Frame pour l'input (caché par défaut)
        self.money_input_frame = tk.Frame(money_body, bg="#f8f9fa")
        
        money_label_frame = tk.Frame(self.money_input_frame, bg="#f8f9fa")
        money_label_frame.pack(fill="x", pady=(0, 5))
        
        tk.Label(money_label_frame, text="Montant total récolté:", 
                font=("Segoe UI", 10), bg="#f8f9fa", fg="#2c3e50").pack(side="left")
        
        # Controls pour montant + validation
        money_controls_frame = tk.Frame(self.money_input_frame, bg="#f8f9fa")
        money_controls_frame.pack(fill="x", pady=(5, 0))
        
        self.money_amount_var = tk.StringVar(value="0.00")
        self.money_entry = tk.Entry(money_controls_frame, textvariable=self.money_amount_var,
                                   font=("Segoe UI", 11), width=12, justify="center",
                                   relief="flat", bd=5, bg="white")
        self.money_entry.pack(side="left")
        
        tk.Label(money_controls_frame, text="€", 
                font=("Segoe UI", 11, "bold"), bg="#f8f9fa", fg="#27ae60").pack(side="left", padx=(5, 10))
        
        # Boutons de validation
        self.money_validated = tk.BooleanVar(value=False)
        
        self.validate_btn = tk.Button(money_controls_frame, text="✓ Valider", 
                                     command=self._validate_money,
                                     bg="#007bff", fg="white", font=("Segoe UI", 9, "bold"),
                                     relief="flat", padx=15, pady=5, cursor="hand2")
        self.validate_btn.pack(side="right")
        
        self.reset_btn = tk.Button(money_controls_frame, text="↻ Modifier", 
                                  command=self._reset_money_validation,
                                  bg="#6c757d", fg="white", font=("Segoe UI", 8),
                                  relief="flat", padx=10, pady=5, cursor="hand2")
        
        # Label de statut
        self.status_label = tk.Label(self.money_input_frame, text="", 
                                    font=("Segoe UI", 9), bg="#f8f9fa")
        
        # Callback pour afficher le bouton reset
        self.money_validated.trace('w', self._on_money_validated)
    
    def _create_results_section(self, parent):
        """Crée la section des résultats"""
        results_card = tk.Frame(parent, bg="#f8f9fa", relief="flat", bd=1)
        results_card.pack(fill="x", pady=(0, 20))
        
        results_header = tk.Frame(results_card, bg="#e74c3c", height=35)
        results_header.pack(fill="x")
        results_header.pack_propagate(False)
        
        tk.Label(results_header, text="📊 Résultats du Calcul", 
                font=("Segoe UI", 11, "bold"), fg="white", bg="#e74c3c").pack(pady=8)
        
        results_body = tk.Frame(results_card, bg="white")
        results_body.pack(fill="both", expand=True, padx=15, pady=15)
        
        results_display = tk.Frame(results_body, bg="white")
        results_display.pack(fill="both", expand=True)
        
        # Labels de résultats
        self.base_total_label = tk.Label(results_display, text="", 
                                        font=("Segoe UI", 12), bg="white", fg="#2c3e50", anchor="w")
        self.base_total_label.pack(fill="x", pady=5)
        
        self.money_collected_label = tk.Label(results_display, text="", 
                                             font=("Segoe UI", 12), bg="white", fg="#27ae60", anchor="w")
        
        # Séparateur
        separator = tk.Frame(results_display, height=3, bg="#ecf0f1")
        separator.pack(fill="x", pady=15)
        
        self.final_total_label = tk.Label(results_display, text="", 
                                         font=("Segoe UI", 14, "bold"), bg="white", fg="#e74c3c", anchor="w")
        self.final_total_label.pack(fill="x", pady=8)
        
        self.per_student_label = tk.Label(results_display, text="", 
                                         font=("Segoe UI", 12), bg="white", fg="#7f8c8d", anchor="w")
        self.per_student_label.pack(fill="x", pady=5)
        
        self.special_message_label = tk.Label(results_display, text="", 
                                             font=("Segoe UI", 12, "bold"), bg="white", fg="#27ae60", anchor="w",
                                             wraplength=500)
        self.special_message_label.pack(fill="x", pady=(15, 0))
    
    def _create_buttons_section(self, parent):
        """Crée la section des boutons"""
        buttons_frame = tk.Frame(parent, bg="#ffffff")
        buttons_frame.pack(fill="x", pady=(20, 0))
        
        close_btn = tk.Button(buttons_frame, text="✓ Fermer", command=self.popup.destroy,
                             bg="#95a5a6", fg="white", font=("Segoe UI", 11, "bold"),
                             relief="flat", padx=25, pady=10, cursor="hand2",
                             activebackground="#7f8c8d", activeforeground="white")
        close_btn.pack(side="right")
    
    # ====================== MÉTHODES D'INTERACTION ======================
    def _toggle_money_input(self):
        """Active/désactive l'input d'argent"""
        if self.money_enabled_var.get():
            self.money_input_frame.pack(fill="x", pady=(5, 0))
            self.money_entry.focus()
            self._reset_money_validation()
        else:
            self.money_input_frame.pack_forget()
            self.money_amount_var.set("0.00")
            self._reset_money_validation()
    
    def _validate_money(self):
        """Valide le montant d'argent saisi"""
        try:
            amount = float(self.money_amount_var.get())
            if amount < 0:
                tkinter.messagebox.showerror("Erreur", "Le montant ne peut pas être négatif !")
                return
            
            self.money_validated.set(True)
            self.validate_btn.config(text="✓ Validé", bg="#27ae60", state="disabled")
            self.money_entry.config(state="disabled", bg="#f8f9fa")
            
            self.status_label.config(text=f"✅ Argent validé: {amount:.2f}€", fg="#27ae60")
            self.status_label.pack(fill="x", pady=(5, 0))
            
            self._calculate_costs()
            
        except ValueError:
            tkinter.messagebox.showerror("Erreur", "Veuillez entrer un montant valide !")
    
    def _reset_money_validation(self):
        """Reset la validation du montant"""
        self.money_validated.set(False)
        self.validate_btn.config(text="✓ Valider", bg="#007bff", state="normal")
        self.money_entry.config(state="normal", bg="white")
        self.status_label.pack_forget()
        self._calculate_costs()
    
    def _on_money_validated(self, *args):
        """Callback quand le montant est validé"""
        if self.money_validated.get():
            self.reset_btn.pack(side="right", padx=(5, 0))
        else:
            self.reset_btn.pack_forget()
    
    def _calculate_costs(self):
        """Calcule et affiche les coûts"""
        try:
            base_cost = float(self.base_cost_var.get())
            num_students = len(self.selected_students)
            
            # Utiliser l'argent seulement si validé
            money_collected = 0.0
            if self.money_enabled_var.get() and self.money_validated.get():
                money_collected = float(self.money_amount_var.get())
            
            # Calculs
            total_base_cost = num_students * base_cost
            final_cost = total_base_cost - money_collected
            cost_per_student = final_cost / num_students if num_students > 0 else 0
            
            # Mise à jour des labels
            self.base_total_label.config(text=f"💵 Coût total de base: {total_base_cost:.2f}€")
            
            if self.money_enabled_var.get() and self.money_validated.get() and money_collected > 0:
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