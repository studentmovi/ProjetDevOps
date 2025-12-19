import tkinter as tk


class EventsPopup:
    @staticmethod
    def show(parent, events, x, y):
        if not events or len(events) <= 3:
            return

        popup = tk.Toplevel(parent)
        popup.wm_overrideredirect(True)
        popup.configure(bg="#f9f9f9", bd=1, relief="solid")

        popup.geometry(f"+{x + 10}+{y + 10}")

        title = tk.Label(
            popup,
            text="📅 Événements",
            font=("Arial", 9, "bold"),
            bg="#f9f9f9"
        )
        title.pack(padx=8, pady=(6, 4))

        for ev in events:
            tk.Label(
                popup,
                text=f"• {ev}",
                font=("Arial", 8),
                bg="#f9f9f9",
                anchor="w"
            ).pack(fill="x", padx=10)

        tk.Label(
            popup,
            text="(clic pour fermer)",
            font=("Arial", 7, "italic"),
            bg="#f9f9f9",
            fg="#777"
        ).pack(pady=(4, 6))

        popup.after(5000, popup.destroy)
        popup.bind("<Button-1>", lambda e: popup.destroy())
        popup.bind("<FocusOut>", lambda e: popup.destroy())
