import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd


class MiniApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Projet Gestion")
        self.root.geometry("700x450")

        # Style général
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))

        # Label d'accueil
        self.label = ttk.Label(root, text="Bienvenue !", font=("Helvetica", 14))
        self.label.pack(pady=10)

        # Bouton pour charger Excel
        self.btn_load = ttk.Button(root, text="Charger un fichier Excel", command=self.load_excel)
        self.btn_load.pack(pady=6)

        # Zone de status contenant le loader
        status_frame = ttk.Frame(root)
        status_frame.pack(fill="x", padx=10)

        # Progressbar (spinner) en mode indéterminé
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate', length=180)
        # On ne l'affiche pas tout de suite; on l'affichera quand on démarre le chargement

        # Label d'état à droite du spinner
        self.status_msg = ttk.Label(status_frame, text="", anchor="w")
        self.status_msg.pack(side="left", padx=(6, 0))

        # Table pour afficher Excel
        self.table = ttk.Treeview(root)
        self.table.pack(expand=True, fill="both", pady=10, padx=10)

        # Pour garder référence au thread en cours
        self._worker_thread = None

    def _start_loader(self, message="Chargement en cours..."):
        # Affiche et démarre le spinner
        try:
            self.progress.pack(side="left")
        except Exception:
            pass
        self.progress.start(10)  # intervalle en ms; plus petit = plus fluide
        self.status_msg.config(text=message)
        self.btn_load.config(state="disabled")

    def _stop_loader(self, message=""):
        # Arrête et cache le spinner
        try:
            self.progress.stop()
            self.progress.pack_forget()
        except Exception:
            pass
        self.status_msg.config(text=message)
        self.btn_load.config(state="normal")

    def load_excel(self):
        # Ouvre la boîte de dialogue (doit rester dans le thread principal)
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if not file_path:
            return

        # Démarrer le loader et lancer la tâche en arrière-plan pour ne pas bloquer l'UI
        self._start_loader("Lecture du fichier...")
        self._worker_thread = threading.Thread(target=self._load_excel_worker, args=(file_path,), daemon=True)
        self._worker_thread.start()

    def _load_excel_worker(self, file_path):
        # Code executé dans un thread séparé
        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            # Renvoyer l'erreur au thread principal
            self.root.after(0, lambda: self._on_load_error(e))
            return

        # Sur le thread principal, mettre à jour l'interface
        self.root.after(0, lambda: self._on_load_success(df))

    def _on_load_error(self, exc):
        self._stop_loader("")
        messagebox.showerror("Erreur", f"Impossible de lire le fichier Excel:\n{exc}")

    def _on_load_success(self, df):
        # Vider la table avant de remplir
        self.table.delete(*self.table.get_children())
        self.table["columns"] = list(df.columns)
        self.table["show"] = "headings"

        for col in df.columns:
            self.table.heading(col, text=col)

        for _, row in df.iterrows():
            self.table.insert("", "end", values=list(row))

        self._stop_loader(f"Fichier chargé : {len(df)} lignes")

    def loader(self):
        # méthode de compatibilité si besoin
        self._start_loader()
if __name__ == "__main__":
    root = tk.Tk()
    app = MiniApp(root)
    root.mainloop()
