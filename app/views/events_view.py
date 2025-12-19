import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from data.event_data_manager import event_manager
from controller.EventExcelImportController import EventExcelImportController
from popups.EventFormPopup import EventFormPopup


class EventsView:
    def __init__(self, parent, styles):
        self.parent = parent
        self.styles = styles
        self.frame = ttk.Frame(parent)

        # Controller Excel EVENTS
        self.excel_importer = EventExcelImportController(self.frame)
        self.excel_importer.on_import_success_callback = self.refresh_events

    # ====================================================
    #  CRÉATION UI
    # ====================================================
    def create_widgets(self):
        self.frame.pack(fill="both", expand=True)

        # ---------- HEADER ----------
        header = self.styles.create_card_frame(self.frame, padding="15")
        header.pack(fill="x", pady=(10, 15))

        ttk.Label(
            header,
            text="📅 Gestion des Événements",
            style="Title.TLabel"
        ).pack(side="left")

        ttk.Button(
            header,
            text="➕ Nouvel événement",
            style="Primary.TButton",
            command=self.create_event_popup
        ).pack(side="right")

        # ---------- LISTE DES ÉVÉNEMENTS ----------
        content = self.styles.create_card_frame(self.frame, padding="10")
        content.pack(fill="both", expand=True)

        columns = ("nom", "date", "categorie", "participants", "ventes")

        self.tree = ttk.Treeview(
            content,
            columns=columns,
            show="headings",
            height=15
        )

        self.tree.heading("nom", text="Nom")
        self.tree.heading("date", text="Date")
        self.tree.heading("categorie", text="Catégorie")
        self.tree.heading("participants", text="Participants")
        self.tree.heading("ventes", text="Ventes")

        self.tree.column("nom", width=300)
        self.tree.column("date", width=120, anchor="center")
        self.tree.column("categorie", width=140, anchor="center")
        self.tree.column("participants", width=120, anchor="center")
        self.tree.column("ventes", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(content, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Double-clic = modification
        self.tree.bind("<Double-1>", self.edit_selected_event)

        self.refresh_events()

        # ---------- ACTIONS ----------
        actions = self.styles.create_card_frame(self.frame, padding="10")
        actions.pack(fill="x", pady=10)

        ttk.Button(
            actions,
            text="✏️ Modifier",
            style="Secondary.TButton",
            command=self.edit_selected_event
        ).pack(side="left", padx=5)

        ttk.Button(
            actions,
            text="📥 Import Excel",
            style="Secondary.TButton",
            command=self.import_excel
        ).pack(side="left", padx=5)

        ttk.Button(
            actions,
            text="📤 Export Excel",
            style="Secondary.TButton",
            command=self.export_selected_event
        ).pack(side="left", padx=5)

    # ====================================================
    #  DONNÉES
    # ====================================================
    def refresh_events(self):
        self.tree.delete(*self.tree.get_children())

        for event in event_manager.get_events():
            self.tree.insert(
                "",
                "end",
                iid=event["id"],
                values=(
                    event["nom"],
                    event["date"],
                    event.get("categorie", "—"),
                    len(event.get("participants", {})),
                    "✔️" if event.get("ventes_activees") else "❌"
                )
            )

    # ====================================================
    #  ACTIONS ÉVÉNEMENTS
    # ====================================================
    def create_event_popup(self):
        """Création d'un nouvel événement"""
        EventFormPopup(
            parent=self.frame,
            on_save_callback=self.refresh_events
        )

    def edit_selected_event(self, event=None):
        """Modification d'un événement existant"""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Attention", "Sélectionne un événement")
            return

        event_data = event_manager.get_event(selected)
        if not event_data:
            messagebox.showerror("Erreur", "Événement introuvable")
            return

        EventFormPopup(
            parent=self.frame,
            on_save_callback=self.refresh_events,
            event=event_data
        )

    # ====================================================
    #  IMPORT / EXPORT
    # ====================================================
    def import_excel(self):
        self.excel_importer.start_import_process()
    def export_selected_event(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Attention", "Sélectionne un événement")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")]
        )
        if not file_path:
            return

        ok = event_manager.export_event_to_excel(selected, file_path)
        if ok:
            messagebox.showinfo("Export", "Export terminé avec succès")
        else:
            messagebox.showerror("Erreur", "Impossible d’exporter")

    # ====================================================
    #  NAVIGATION
    # ====================================================
    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()
