import tkinter as tk
from tkinter import ttk, messagebox
from data.event_data_manager import event_manager


class CostCalculatorPopup:
    """Popup pour calculer et enregistrer les coûts d'un événement"""

    def __init__(self, parent, event_id, selected_students):
        self.parent = parent
        self.event_id = event_id
        self.selected_students = selected_students

        # 🔑 Chargement événement
        self.event = event_manager.get_event(event_id)
        if not self.event:
            raise ValueError("Événement introuvable")

        self.popup = None

        # Variables UI
        self.money_enabled_var = tk.BooleanVar(value=self.event.get("ventes_activees", False))
        self.money_amount_var = tk.StringVar(value=str(self.event.get("total_ventes", 0.0)))
        self.money_validated = tk.BooleanVar(value=False)

        # Labels résultats
        self.label_total = None
        self.label_money = None
        self.label_final = None
        self.label_per_student = None

    # =====================================================
    def show(self):
        self.popup = tk.Toplevel(self.parent)
        self.popup.title("Calculateur de Coûts d'Événement")
        self.popup.geometry("600x520")
        self.popup.transient(self.parent)
        self.popup.grab_set()
        self.popup.resizable(False, False)

        self._create_header()
        self._create_content()
        self._calculate_costs()

    # =====================================================
    def _create_header(self):
        header = tk.Frame(self.popup, bg="#2c3e50", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        content = tk.Frame(header, bg="#2c3e50")
        content.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(
            content,
            text="💰 Calculateur de Coûts",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(anchor="w")

        subtitle = f"{self.event['nom']} • {self.event.get('date', '')}"

        tk.Label(
            content,
            text=subtitle,
            font=("Segoe UI", 10),
            fg="#bdc3c7",
            bg="#2c3e50"
        ).pack(anchor="w")

        tk.Label(
            content,
            text=f"{len(self.selected_students)} élèves sélectionnés",
            font=("Segoe UI", 9),
            fg="#95a5a6",
            bg="#2c3e50"
        ).pack(anchor="e")

    # =====================================================
    def _create_content(self):
        container = ttk.Frame(self.popup, padding=20)
        container.pack(fill="both", expand=True)

        # ---------- Coût ----------
        cost_frame = ttk.LabelFrame(container, text="💵 Coût de l'événement")
        cost_frame.pack(fill="x", pady=10)

        ttk.Label(
            cost_frame,
            text=f"Coût total déclaré : {self.event['cout_total']:.2f} €"
        ).pack(anchor="w", padx=10, pady=5)

        # ---------- Argent récolté ----------
        money_frame = ttk.LabelFrame(container, text="💸 Argent récolté")
        money_frame.pack(fill="x", pady=10)

        ttk.Checkbutton(
            money_frame,
            text="Les élèves ont récolté de l'argent",
            variable=self.money_enabled_var,
            command=self._toggle_money_input
        ).pack(anchor="w", padx=10)

        self.money_entry = ttk.Entry(money_frame, textvariable=self.money_amount_var)
        self.validate_btn = ttk.Button(
            money_frame,
            text="Valider",
            command=self._validate_money
        )

        if self.money_enabled_var.get():
            self.money_entry.pack(fill="x", padx=10, pady=5)
            self.validate_btn.pack(pady=5)

        # ---------- Résultats ----------
        result_frame = ttk.LabelFrame(container, text="📊 Résultats")
        result_frame.pack(fill="x", pady=10)

        self.label_total = ttk.Label(result_frame)
        self.label_money = ttk.Label(result_frame)
        self.label_final = ttk.Label(result_frame, font=("Segoe UI", 11, "bold"))
        self.label_per_student = ttk.Label(result_frame)

        self.label_total.pack(anchor="w", padx=10)
        self.label_money.pack(anchor="w", padx=10)
        self.label_final.pack(anchor="w", padx=10, pady=5)
        self.label_per_student.pack(anchor="w", padx=10)

        ttk.Button(
            container,
            text="💾 Enregistrer",
            command=self._save_costs
        ).pack(pady=(15, 5))

        ttk.Button(
            container,
            text="Fermer",
            command=self.popup.destroy
        ).pack()

    # =====================================================
    def _toggle_money_input(self):
        if self.money_enabled_var.get():
            self.money_entry.pack(fill="x", padx=10, pady=5)
            self.validate_btn.pack(pady=5)
        else:
            self.money_entry.pack_forget()
            self.validate_btn.pack_forget()
            self.money_amount_var.set("0.00")
            self.money_validated.set(False)
            self._calculate_costs()

    def _validate_money(self):
        try:
            value = float(self.money_amount_var.get())
            if value < 0:
                raise ValueError
            self.money_validated.set(True)
            self._calculate_costs()
        except ValueError:
            messagebox.showerror("Erreur", "Montant invalide")

    # =====================================================
    def _calculate_costs(self):
        count = len(self.selected_students)
        if count == 0:
            return

        cout_total = float(self.event["cout_total"])
        money = float(self.money_amount_var.get()) if self.money_enabled_var.get() else 0.0

        final_total = max(0, cout_total - money)
        per_student = final_total / count

        self.label_total.config(text=f"Coût total : {cout_total:.2f} €")
        self.label_money.config(text=f"Argent récolté : -{money:.2f} €")
        self.label_final.config(text=f"TOTAL FINAL : {final_total:.2f} €")
        self.label_per_student.config(text=f"Par élève : {per_student:.2f} €")

    # =====================================================
    def _save_costs(self):
        """Enregistre les calculs dans events_assignments.json"""

        total_ventes = float(self.money_amount_var.get()) if self.money_enabled_var.get() else 0.0

        # Mise à jour ventes globales
        event_manager.toggle_event_sales(self.event_id, self.money_enabled_var.get())
        event_manager.update_event_sales_total(self.event_id, total_ventes)

        # Assurer que tous les élèves sont bien participants
        for student_id in self.selected_students:
            if str(student_id) not in self.event["participants"]:
                event_manager.assign_student_to_event(student_id, self.event_id)

        event_manager.calculate_event_prices(self.event_id)
        event_manager.save_data()

        messagebox.showinfo("✅ Succès", "Coûts enregistrés avec succès")
        self.popup.destroy()
