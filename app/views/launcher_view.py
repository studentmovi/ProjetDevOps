import tkinter as tk
from tkinter import ttk
import time
import os
from PIL import Image, ImageTk


class LauncherView:
    """Vue moderne animée pour le launcher TripSchool"""

    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()

        # Variables
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Initialisation...")
        self.bus_speed = 4
        self.running = True  # empêche les crash pendant destroy()

        self.setup_window()
        self.setup_styles()
        self.create_widgets()

    # -----------------------------------------------------
    #  CONFIG FENÊTRE
    # -----------------------------------------------------
    def setup_window(self):
        self.root.title("TripSchool - Launcher")

        width, height = 600, 380
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x, y = (sw - width) // 2, (sh - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

    # -----------------------------------------------------
    #  STYLES
    # -----------------------------------------------------
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(
            "Modern.Horizontal.TProgressbar",
            background="#4CAF50",
            troughcolor="#2a2a2a",
            borderwidth=0,
            lightcolor="#4CAF50",
            darkcolor="#4CAF50",
        )

    # -----------------------------------------------------
    #  UI PRINCIPALE
    # -----------------------------------------------------
    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg="#1e1e1e", padx=30, pady=15)
        main_frame.pack(fill="both", expand=True)

        # =======================
        #   CANVAS ANIMATION BUS
        # =======================
        self.canvas = tk.Canvas(
            main_frame,
            width=350,
            height=140,
            bg="#1e1e1e",
            highlightthickness=0,
        )
        self.canvas.pack(pady=(5, 10))

        # ===== CHARGEMENT + REDIMENSIONNEMENT DU BUS =====
        bus_path = os.path.join(os.path.dirname(__file__), "..", "assets", "bus.png")

        img = Image.open(bus_path)

        TARGET_WIDTH = 350
        ratio = TARGET_WIDTH / img.width
        new_height = int(img.height * ratio)
        img = img.resize((TARGET_WIDTH, new_height), Image.LANCZOS)

        self.bus_img = ImageTk.PhotoImage(img)

        self.bus = self.canvas.create_image(-TARGET_WIDTH, 70, image=self.bus_img)

        # =======================
        #  TITRE
        # =======================
        title = tk.Label(
            main_frame,
            text="TripSchool",
            font=("Segoe UI", 26, "bold"),
            fg="white",
            bg="#1e1e1e",
        )
        title.pack()

        subtitle = tk.Label(
            main_frame,
            text="Chargement de l'application...",
            font=("Segoe UI", 11),
            fg="#cccccc",
            bg="#1e1e1e",
        )
        subtitle.pack(pady=(0, 15))

        # =======================
        #  BARRE DE PROGRESSION
        # =======================
        progress_frame = tk.Frame(main_frame, bg="#1e1e1e")
        progress_frame.pack(fill="x")

        self.progress_bar = ttk.Progressbar(
            progress_frame,
            style="Modern.Horizontal.TProgressbar",
            variable=self.progress_var,
            mode="determinate",
        )
        self.progress_bar.pack(fill="x", pady=(0, 5))

        self.status_label = tk.Label(
            progress_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 10),
            fg="#cccccc",
            bg="#1e1e1e",
        )
        self.status_label.pack()

        self.percent_label = tk.Label(
            progress_frame,
            text="0%",
            font=("Segoe UI", 10, "bold"),
            fg="#4CAF50",
            bg="#1e1e1e",
        )
        self.percent_label.pack(pady=(3, 10))

        # =======================
        #   FOOTER (VERSION + CRÉDIT)
        # =======================
        footer = tk.Frame(main_frame, bg="#1e1e1e")
        footer.pack(fill="x", side="bottom")

        version = tk.Label(
            footer,
            text=f"Version {self.controller.get_local_version()}",
            font=("Segoe UI", 9),
            fg="#666",
            bg="#1e1e1e",
        )
        version.pack(side="left")

        credit = tk.Label(
            footer,
            text="By Erwan Michel - HELHa",
            font=("Segoe UI", 9),
            fg="#888",
            bg="#1e1e1e",
        )
        credit.pack(side="right")

    # -----------------------------------------------------
    #  ANIMATION DU BUS (40 FPS)
    # -----------------------------------------------------
    def animate_bus(self):
        if not self.running:
            return

        try:
            x, y = self.canvas.coords(self.bus)

            if x > 700:
                x = -350

            self.canvas.coords(self.bus, x + self.bus_speed, y)
            self.root.after(25, self.animate_bus)

        except tk.TclError:
            return

    # -----------------------------------------------------
    #  PROGRESSION
    # -----------------------------------------------------
    def update_progress(self, value, status):
        self.progress_var.set(value)
        self.status_var.set(status)
        self.percent_label.config(text=f"{int(value)}%")

        self.bus_speed = max(4, int(value / 10))

        self.root.update()

    def animate_progress(self, start, end, duration, status):
        steps = 45
        step_value = (end - start) / steps
        step_duration = duration / steps

        for i in range(steps + 1):
            self.update_progress(start + step_value * i, status)
            time.sleep(step_duration)

    def update_status(self, txt):
        self.status_var.set(txt)

    # -----------------------------------------------------
    #  ERREURS + FERMETURE
    # -----------------------------------------------------
    def show_error(self, txt):
        self.status_var.set(f"❌ {txt}")
        self.percent_label.config(text="Erreur", fg="red")

    def close_loader(self):
        self.running = False
        self.root.after(50, self.root.destroy)

    # -----------------------------------------------------
    #  RUN
    # -----------------------------------------------------
    def run(self):
        self.animate_bus()
        self.root.after(400, self.controller.start_loading_sequence)
        self.root.mainloop()
