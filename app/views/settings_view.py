import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font as tkfont
from controller.Settings_Controller import SettingsController


class SettingsView:
    def __init__(self, parent, styles, app):
        self.parent = parent
        self.styles = styles
        self.app = app  # 🔑 accès au FontManager
        self.controller = SettingsController()

        self.frame = ttk.Frame(parent)

        # Vars
        self.data_path_var = tk.StringVar()
        self.font_family_var = tk.StringVar()
        self.font_size_var = tk.IntVar()
        self.auto_update_var = tk.BooleanVar()

        self.preview_label = None

    # ====================================================
    # NAVIGATION
    # ====================================================
    def show(self):
        self._load_settings()
        self.create_widgets()
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()

    # ====================================================
    # LOAD SETTINGS
    # ====================================================
    def _load_settings(self):
        settings = self.controller.get_settings()
        font_cfg = self.app.font_manager.get_font()

        self.data_path_var.set(settings["data_path"])
        self.font_family_var.set(font_cfg["family"])
        self.font_size_var.set(font_cfg["size"])
        self.auto_update_var.set(settings["auto_update"])

    # ====================================================
    # UI
    # ====================================================
    def create_widgets(self):
        for w in self.frame.winfo_children():
            w.destroy()

        container = ttk.Frame(self.frame, padding=30)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="⚙️ Paramètres", style="Title.TLabel").pack(anchor="w", pady=(0, 30))

        # ===============================
        # Dossier data
        # ===============================
        ttk.Label(container, text="Dossier de stockage", style="Subtitle.TLabel").pack(anchor="w")

        path_frame = ttk.Frame(container)
        path_frame.pack(fill="x", pady=10)

        ttk.Entry(path_frame, textvariable=self.data_path_var, state="readonly").pack(
            side="left", fill="x", expand=True
        )

        ttk.Button(
            path_frame,
            text="Parcourir",
            style="Secondary.TButton",
            command=self._choose_folder
        ).pack(side="left", padx=10)

        # ===============================
        # Police
        # ===============================
        ttk.Label(container, text="Police d’écriture", style="Subtitle.TLabel").pack(anchor="w", pady=(25, 5))

        font_row = ttk.Frame(container)
        font_row.pack(fill="x")

        ttk.Combobox(
            font_row,
            textvariable=self.font_family_var,
            state="readonly",
            values=sorted(tkfont.families())
        ).pack(side="left", fill="x", expand=True)

        ttk.Label(font_row, text="Taille").pack(side="left", padx=10)

        ttk.Spinbox(
            font_row,
            from_=8,
            to=24,
            textvariable=self.font_size_var,
            width=5
        ).pack(side="left")

        # ===============================
        # Aperçu
        # ===============================
        preview = ttk.LabelFrame(container, text="Aperçu", padding=12)
        preview.pack(fill="x", pady=15)

        self.preview_label = ttk.Label(
            preview,
            text="TripSchool – aperçu de la police (élèves, événements, etc.)"
        )
        self.preview_label.pack(anchor="w")

        # Bind live preview
        self.font_family_var.trace_add("write", lambda *_: self._apply_font_live())
        self.font_size_var.trace_add("write", lambda *_: self._apply_font_live())

        # ===============================
        # Updates
        # ===============================
        ttk.Checkbutton(
            container,
            text="Activer les mises à jour automatiques",
            variable=self.auto_update_var
        ).pack(anchor="w", pady=20)

        # ===============================
        # Boutons
        # ===============================
        btns = ttk.Frame(container)
        btns.pack(fill="x", pady=30)

        ttk.Button(btns, text="Enregistrer", style="Primary.TButton", command=self._save).pack(side="right", padx=10)
        ttk.Button(btns, text="Annuler", style="Light.TButton", command=self._cancel).pack(side="right")

        self._apply_font_live()

    # ====================================================
    # ACTIONS
    # ====================================================
    def _apply_font_live(self):
        family = self.font_family_var.get()
        size = self.font_size_var.get()

        if not family or not size:
            return

        # 🔥 APPLY GLOBAL
        self.app.font_manager.set_font(family, size)

        # Aperçu local
        self.preview_label.configure(font=(family, size))

    def _choose_folder(self):
        folder = filedialog.askdirectory(title="Choisir le dossier de données")
        if folder:
            self.data_path_var.set(folder)

    def _save(self):
        self.controller.save_settings(
            self.data_path_var.get(),
            self.font_family_var.get(),
            self.auto_update_var.get()
        )
        messagebox.showinfo("Paramètres", "Paramètres enregistrés.")

    def _cancel(self):
        self._load_settings()
        self.create_widgets()
