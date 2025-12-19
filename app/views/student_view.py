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

    def show(self):
        self.frame.pack(fill="both", expand=True, padx=8, pady=5)

    def hide(self):
        self.frame.pack_forget()

    # =========================================================
    # FILTRES (INTERFACE)
    # =========================================================

    def get_filters(self):
        """⚠️ Seule méthode lue par le controller"""
        return {
            "year": self.year_combo.get(),
            "class": self.class_combo.get(),
            "event": self.event_combo.get(),
            "month": self.month_combo.get(),
            "search": (
                self.search_var.get()
                if self.search_var.get() != "Nom, prénom..."
                else ""
            ),
            "sort": self.sort_combo.get(),
        }

    def _initialize_default_filters(self):
        self.year_combo.set("Toutes")
        self.class_combo.set("Toutes")
        self.event_combo.set("Tous")
        self.month_combo.set("Tous")
        self.sort_combo.set("Nom A-Z")
        self.search_var.set("")

    # =========================================================
    # TOOLBAR
    # =========================================================

    def _create_toolbar(self):
        bar = ttk.LabelFrame(self.frame, text="⚙️ Actions", padding=8)
        bar.pack(fill="x", pady=(10, 8))

        ttk.Button(
            bar,
            text="📊 Importer Excel",
            command=self.controller.import_excel_students
        ).pack(side="left")

        ttk.Button(
            bar,
            text="📅 Assigner événement",
            command=self._on_assign_event
        ).pack(side="right", padx=4)

        ttk.Button(
            bar,
            text="💰 Calculer coût",
            command=self._on_calculate_cost
        ).pack(side="right")

    # =========================================================
    # PANNEAU DE FILTRES
    # =========================================================

    def _create_filter_panel(self):
        panel = ttk.LabelFrame(self.frame, text="🔍 Filtres", padding=8)
        panel.pack(fill="x", pady=(0, 8))

        # Ligne 1
        row1 = ttk.Frame(panel)
        row1.pack(fill="x")

        ttk.Label(row1, text="🔍").pack(side="left")
        self.search_entry = ttk.Entry(row1, textvariable=self.search_var, width=20)
        self.search_entry.pack(side="left", padx=5)

        self.sort_combo = ttk.Combobox(
            row1,
            values=["Nom A-Z", "Nom Z-A", "Classe", "Année", "Date (Mois)"],
            state="readonly",
            width=12
        )
        self.sort_combo.pack(side="right")
        self.sort_combo.set("Nom A-Z")

        # Ligne 2
        row2 = ttk.Frame(panel)
        row2.pack(fill="x", pady=4)

        self.year_combo = ttk.Combobox(
            row2,
            values=["Toutes", "1ère", "2ème", "3ème", "4ème", "5ème", "6ème"],
            state="readonly",
            width=7
        )
        self.year_combo.pack(side="left", padx=4)

        self.class_combo = ttk.Combobox(
            row2,
            values=["Toutes"],
            state="readonly",
            width=7
        )
        self.class_combo.pack(side="left", padx=4)

        self.event_combo = ttk.Combobox(
            row2,
            values=["Tous"],
            state="readonly",
            width=12
        )
        self.event_combo.pack(side="left", padx=4)

        self.month_combo = ttk.Combobox(
            row2,
            values=["Tous"],
            state="readonly",
            width=12
        )
        self.month_combo.pack(side="left", padx=4)

        ttk.Button(
            row2,
            text="🔄 Reset",
            command=self.controller.reset_filters
        ).pack(side="right")

        self._setup_bindings()

    def _setup_bindings(self):
        self.search_var.trace_add(
            "write",
            lambda *_: self.controller.apply_all_filters()
        )

        for combo in (
            self.year_combo,
            self.class_combo,
            self.event_combo,
            self.month_combo,
            self.sort_combo,
        ):
            combo.bind(
                "<<ComboboxSelected>>",
                lambda e: self.controller.apply_all_filters()
            )

    # =========================================================
    # TABLE (TREEVIEW)
    # =========================================================

    def _create_main_content(self):
        frame = ttk.Frame(self.frame)
        frame.pack(fill="both", expand=True)

        columns = ("sel", "nom", "prenom", "classe", "annee", "events")

        self.treeview = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            selectmode="none"
        )

        self.treeview.heading("sel", text="☑️")
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

        # Clic simple → sélection
        self.treeview.bind("<Button-1>", self._on_tree_click)
        # Double clic → détails élève
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
                "events": " • ".join(
                    self.controller.get_student_events(student)
                ) or "Aucun"
            })

        self.tree_renderer.render(
            rows,
            self.controller.selected_students
        )

        self._update_status_bar()

    def _on_tree_click(self, event):
        item = self.treeview.identify_row(event.y)
        col = self.treeview.identify_column(event.x)

        if not item or col != "#1":
            return

        student_id = int(item.replace("student_", ""))
        self.controller.toggle_student_selection(student_id)

    def _on_tree_double_click(self, event):
        item = self.treeview.identify_row(event.y)
        if not item:
            return

        student_id = int(item.replace("student_", ""))
        self.controller.open_student_details(student_id)

    # =========================================================
    # STATUS BAR
    # =========================================================

    def _create_status_bar(self):
        bar = ttk.Frame(self.frame)
        bar.pack(fill="x")

        self.status_label = ttk.Label(bar, text="Prêt", padding=6)
        self.status_label.pack(side="left")

    def _update_status_bar(self):
        total = len(self.controller.get_students_data())
        shown = len(self.controller.filtered_students)
        selected = len(self.controller.selected_students)

        source = "Excel" if self.controller.is_using_excel_data() else "JSON"
        self.status_label.config(
            text=(
                f"Total: {total} | "
                f"Affichés: {shown} | "
                f"Sélectionnés: {selected} | "
                f"Source: {source}"
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
# ====================================================