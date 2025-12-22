import tkinter as tk
from tkinter import ttk

# ====================================================
#  POPUP MISE À JOUR
# ====================================================
def update_popup_custom(root, local_version, remote_version, force_update=False):
    result = {"action": "later"}

    popup = tk.Toplevel(root)
    popup.title("Mise à jour disponible")
    popup.resizable(False, False)
    popup.transient(root)
    popup.grab_set()

    w, h = 460, 260
    x = (popup.winfo_screenwidth() - w) // 2
    y = (popup.winfo_screenheight() - h) // 2
    popup.geometry(f"{w}x{h}+{x}+{y}")

    BG = "#f8fafc"
    BLUE = "#2563eb"
    DARK = "#0f172a"
    MUTED = "#475569"

    popup.configure(bg=BG)

    def close_later():
        popup.destroy()

    popup.protocol("WM_DELETE_WINDOW", close_later)

    frame = tk.Frame(popup, bg=BG, padx=24, pady=20)
    frame.pack(fill="both", expand=True)

    # ===== Titre =====
    tk.Label(
        frame,
        text="Une nouvelle version est disponible",
        font=("Segoe UI", 14, "bold"),
        fg=DARK,
        bg=BG
    ).pack(anchor="w", pady=(0, 10))

    # ===== Versions =====
    tk.Label(
        frame,
        text=f"Version actuelle : {local_version}",
        font=("Segoe UI", 10),
        fg=MUTED,
        bg=BG
    ).pack(anchor="w")

    tk.Label(
        frame,
        text=f"Nouvelle version : {remote_version}",
        font=("Segoe UI", 10, "bold"),
        fg=BLUE,
        bg=BG
    ).pack(anchor="w", pady=(0, 15))

    if force_update:
        tk.Label(
            frame,
            text="⚠️ Cette mise à jour est obligatoire",
            font=("Segoe UI", 10, "bold"),
            fg="#dc2626",
            bg=BG
        ).pack(anchor="w", pady=(0, 10))

    # ===== Boutons =====
    btns = tk.Frame(frame, bg=BG)
    btns.pack(fill="x", pady=(20, 0))

    def do_update():
        result["action"] = "update"
        popup.destroy()

    ttk.Button(
        btns,
        text="⏰ Me le rappeler plus tard",
        command=close_later
    ).pack(side="left")

    ttk.Button(
        btns,
        text="⏫ Mettre à jour maintenant",
        command=do_update
    ).pack(side="right")

    tk.Label(
        frame,
        text="TripSchool • Mise à jour sécurisée",
        font=("Segoe UI", 9),
        fg="#94a3b8",
        bg=BG
    ).pack(side="bottom", pady=(15, 0))

    root.wait_window(popup)
    return result["action"]
