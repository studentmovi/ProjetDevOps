import tkinter as tk
from tkinter import ttk, messagebox

from controller.StudentViewController import StudentViewController
from ui.student_treeview_renderer import StudentTreeviewRenderer


class StudentView:
    """Vue principale pour la gestion des élèves"""

    def __init__(self, root, styles):
        self.root = root
        self.styles = styles
        self.frame = None
        self.controller = None

        # Variables UI
        self.search_var = tk.StringVar()

        self.search_entry = None
        self.year_combo = None
        self.class_combo = None
        self.event_category_combo = None
        self.event_combo = None
        self.month_combo = None
        self.sort_combo = None

        self.treeview = None
        self.tree_renderer = None
        self.status_label = None

    # =========================================================
    # INITIALISATION
    # =========================================================

    def create_widgets(self):
        self.create_view()

    def create_view(self):
        if self.frame:
            self.frame.destroy()

        self.frame = ttk.Frame(self.root)
        self.controller = StudentViewController(self)

        self._create_toolbar()
        self._create_filter_panel()
        self._create_main_content()
        self._create_status_bar()

        self._initialize_default_filters()
        self.controller.load_all_students_on_startup()
        self._update_filters()

    def show(self):
        self.frame.pack(fill="both", expand=True, padx=8, pady=5)

    def hide(self):
        self.frame.pack_forget()

    # =========================================================
    # FILTRES
    # =========================================================

    def get_filters(self):
        return {
            "year": self.year_combo.get(),
            "class": self.class_combo.get(),
            "event_category": self.event_category_combo.get(),
            "event": self.event_combo.get(),
            "month": self.month_combo.get(),
            "search": self.search_var.get().strip(),
            "sort": self.sort_combo.get(),
        }

    def _initialize_default_filters(self):
        self.year_combo.set("Toutes")
        self.class_combo.set("Toutes")
        self.event_category_combo.set("Toutes")
        self.event_combo.set("Tous")
        self.month_combo.set("Tous")
        self.sort_combo.set("Nom A-Z")
        self.search_var.set("")

    # =========================================================
    # FILTRES DYNAMIQUES
    # =========================================================

    def _update_filters(self):
        try:
            self.year_combo["values"] = ["Toutes"] + self.controller.get_available_years()
            self.class_combo["values"] = ["Toutes"] + self.controller.get_available_classes()
            self.event_category_combo["values"] = ["Toutes"] + self.controller.get_event_categories()
            self.month_combo["values"] = ["Tous"] + self.controller.get_available_months()

            self._update_event_filter()

        except Exception as e:
            print(f"[StudentView] update filters error: {e}")

    def _update_event_filter(self):
        category = self.event_category_combo.get()
        events = ["Tous"] + self.controller.get_events_by_category(category)
        self.event_combo["values"] = events
        if self.event_combo.get() not in events:
            self.event_combo.set("Tous")

    # =========================================================
    # TOOLBAR
    # =========================================================

    def _create_toolbar(self):
        bar = ttk.LabelFrame(self.frame, text="Actions", padding=8)
        bar.pack(fill="x", pady=(10, 8))

        ttk.Button(
            bar,
            text="Importer Excel",
            command=self._on_import_excel
        ).pack(side="left")

        ttk.Button(
            bar,
            text="Assigner événement",
            command=self._on_assign_event
        ).pack(side="right", padx=4)

        ttk.Button(
            bar,
            text="Calculer coût",
            command=self._on_calculate_cost
        ).pack(side="right")

    def _on_import_excel(self):
        self.controller.import_excel_students()
        self.root.after(200, self._update_filters)

    # =========================================================
    # PANNEAU DE FILTRES
    # =========================================================

    def _create_filter_panel(self):
        panel = ttk.LabelFrame(self.frame, text="Filtres", padding=8)
        panel.pack(fill="x", pady=(0, 8))

        # Ligne recherche + tri
        row1 = ttk.Frame(panel)
        row1.pack(fill="x")

        ttk.Label(row1, text="Recherche").pack(side="left")
        self.search_entry = ttk.Entry(row1, textvariable=self.search_var, width=20)
        self.search_entry.pack(side="left", padx=6)

        self.sort_combo = ttk.Combobox(
            row1,
            values=["Nom A-Z", "Nom Z-A", "Classe", "Année", "Date (Mois)"],
            state="readonly",
            width=14
        )
        self.sort_combo.pack(side="right")
        self.sort_combo.set("Nom A-Z")

        # Ligne filtres principaux
        row2 = ttk.Frame(panel)
        row2.pack(fill="x", pady=6)

        def labeled_combo(parent, label, width):
            frame = ttk.Frame(parent)
            frame.pack(side="left", padx=6)
            ttk.Label(frame, text=label).pack(anchor="w")
            combo = ttk.Combobox(frame, state="readonly", width=width)
            combo.pack()
            return combo

        self.year_combo = labeled_combo(row2, "Année", 12)
        self.class_combo = labeled_combo(row2, "Classe", 12)
        self.event_category_combo = labeled_combo(row2, "Catégorie", 18)
        self.event_combo = labeled_combo(row2, "Événement", 22)
        self.month_combo = labeled_combo(row2, "Mois", 16)

        ttk.Button(
            row2,
            text="Réinitialiser",
            command=self._on_reset_filters
        ).pack(side="right", padx=10)

        self._setup_bindings()

    def _setup_bindings(self):
        self.search_var.trace_add("write", lambda *_: self.controller.apply_all_filters())

        for combo in (
            self.year_combo,
            self.class_combo,
            self.event_combo,
            self.month_combo,
            self.sort_combo,
        ):
            combo.bind("<<ComboboxSelected>>", lambda e: self.controller.apply_all_filters())

        self.event_category_combo.bind(
            "<<ComboboxSelected>>",
            lambda e: self._on_category_changed()
        )

    def _on_category_changed(self):
        self._update_event_filter()
        self.controller.apply_all_filters()

    def _on_reset_filters(self):
        self._initialize_default_filters()
        self._update_filters()
        self.controller.apply_all_filters()

    # =========================================================
    # TABLE
    # =========================================================

    def _create_main_content(self):
        frame = ttk.Frame(self.frame)
        frame.pack(fill="both", expand=True)

        columns = ("sel", "nom", "prenom", "classe", "annee", "events")

        self.treeview = ttk.Treeview(frame, columns=columns, show="headings", selectmode="none")

        self.treeview.heading("sel", text="✓")
        self.treeview.heading("nom", text="Nom")
        self.treeview.heading("prenom", text="Prénom")
        self.treeview.heading("classe", text="Classe")
        self.treeview.heading("annee", text="Année")
        self.treeview.heading("events", text="Événements")

        self.treeview.column("sel", width=40, anchor="center", stretch=False)
        self.treeview.column("classe", width=70, anchor="center", stretch=False)
        self.treeview.column("annee", width=70, anchor="center", stretch=False)

        self.treeview.pack(fill="both", expand=True)

        self.tree_renderer = StudentTreeviewRenderer(self.treeview, self.styles)
        self.tree_renderer.configure_tags()

        self.treeview.bind("<Button-1>", self._on_tree_click)
        self.treeview.bind("<Double-1>", self._on_tree_double_click)

    def update_display(self):
        rows = []
        for student in self.controller.filtered_students:
            rows.append({
                "id": student["id"],
                "nom": student.get("nom", ""),
                "prenom": student.get("prenom", ""),
                "classe": student.get("classe", ""),
                "annee": student.get("annee", ""),
                "events": " • ".join(self.controller.get_student_events(student)) or "Aucun"
            })

        self.tree_renderer.render(rows, self.controller.selected_students)
        self._update_status_bar()

    def _on_tree_click(self, event):
        item = self.treeview.identify_row(event.y)
        col = self.treeview.identify_column(event.x)
        if item and col == "#1":
            self.controller.toggle_student_selection(int(item.replace("student_", "")))

    def _on_tree_double_click(self, event):
        item = self.treeview.identify_row(event.y)
        if item:
            self.controller.open_student_details(int(item.replace("student_", "")))

    # =========================================================
    # STATUS BAR
    # =========================================================

    def _create_status_bar(self):
        bar = ttk.Frame(self.frame)
        bar.pack(fill="x")
        self.status_label = ttk.Label(bar, text="Prêt", padding=6)
        self.status_label.pack(side="left")

    def _update_status_bar(self):
        self.status_label.config(
            text=(
                f"Total: {len(self.controller.get_students_data())} | "
                f"Affichés: {len(self.controller.filtered_students)} | "
                f"Sélectionnés: {len(self.controller.selected_students)} | "
                f"Source: {'Excel' if self.controller.is_using_excel_data() else 'JSON'}"
            )
        )

    # =========================================================
    # ACTIONS
    # =========================================================

    def _on_assign_event(self):
        ok, error = self.controller.assign_to_event()
        if not ok:
            messagebox.showwarning("Attention", error)

    def _on_calculate_cost(self):
        ok, error = self.controller.calculate_event_cost()
        if not ok:
            messagebox.showwarning("Attention", error)
