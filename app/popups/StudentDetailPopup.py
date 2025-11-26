import tkinter as tk
from tkinter import ttk, messagebox

class StudentDetailPopup:
    def __init__(self, parent, student_data, on_save_callback=None, styles=None):
        self.parent = parent
        self.student_data = student_data.copy()
        self.on_save_callback = on_save_callback
        self.styles = styles
        self.popup = None
        self.entries = {}
        self.events_listbox = None
        self.setup_popup()
        
    def setup_popup(self):
        """Configure la fenêtre popup"""
        self.popup = tk.Toplevel(self.parent)
        self.popup.title(f"Détails - {self.student_data.get('prenom', '')} {self.student_data.get('nom', '')}")
        self.popup.geometry("500x600")
        self.popup.resizable(False, False)
        self.popup.transient(self.parent)
        self.popup.grab_set()
        
        # Couleurs du thème existant
        if self.styles:
            self.popup.configure(bg=self.styles.colors['off_white'])
        else:
            self.popup.configure(bg='#f0f0f0')
        
        # Centrer la fenêtre
        self.center_window()
        
        # Frame principal
        main_frame = tk.Frame(self.popup, bg=self.popup.cget('bg'))
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Informations personnelles
        self.create_personal_info_section(main_frame)
        
        # Section événements
        self.create_events_section(main_frame)
        
        # Boutons
        self.create_buttons_section(main_frame)
        
    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.popup.update_idletasks()
        x = (self.popup.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.popup.winfo_screenheight() // 2) - (600 // 2)
        self.popup.geometry(f"500x600+{x}+{y}")
        
    def create_personal_info_section(self, parent):
        """Crée la section des informations personnelles"""
        info_frame = tk.LabelFrame(parent, text="Informations personnelles", 
                                  font=("Arial", 10, "bold"), 
                                  bg=parent.cget('bg'), padx=15, pady=15)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Champs
        fields = [
            ("Nom:", "nom"),
            ("Prénom:", "prenom"),
            ("Classe:", "classe"),
            ("Année:", "annee"),
            ("Option:", "option")
        ]
        
        self.entries = {}
        for i, (label, field) in enumerate(fields):
            tk.Label(info_frame, text=label, font=("Arial", 9), 
                    bg=info_frame.cget('bg')).grid(row=i, column=0, sticky=tk.W, pady=8, padx=(0, 10))
            
            entry = tk.Entry(info_frame, width=35, font=("Arial", 9))
            entry.grid(row=i, column=1, sticky="ew", pady=8)
            entry.insert(0, self.student_data.get(field, ''))
            self.entries[field] = entry
            
        info_frame.grid_columnconfigure(1, weight=1)
            
    def create_events_section(self, parent):
        """Crée la section des événements"""
        events_frame = tk.LabelFrame(parent, text="Événements assignés", 
                                   font=("Arial", 10, "bold"), 
                                   bg=parent.cget('bg'), padx=15, pady=15)
        events_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Frame pour la liste avec scrollbar
        list_frame = tk.Frame(events_frame, bg=events_frame.cget('bg'))
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Listbox avec scrollbar
        scrollbar_events = tk.Scrollbar(list_frame)
        self.events_listbox = tk.Listbox(list_frame, 
                                       yscrollcommand=scrollbar_events.set,
                                       font=("Arial", 9),
                                       height=8)
        scrollbar_events.config(command=self.events_listbox.yview)
        
        self.events_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_events.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Remplir la liste des événements
        events = self.student_data.get('evenements', [])
        for event in events:
            self.events_listbox.insert(tk.END, event)
            
        # Frame pour boutons d'événements
        events_btn_frame = tk.Frame(events_frame, bg=events_frame.cget('bg'))
        events_btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        add_event_btn = tk.Button(events_btn_frame, text="Ajouter événement", 
                                command=self.add_event, font=("Arial", 8),
                                bg="#4CAF50", fg="white")
        add_event_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        remove_event_btn = tk.Button(events_btn_frame, text="Retirer sélection", 
                                   command=self.remove_event, font=("Arial", 8),
                                   bg="#f44336", fg="white")
        remove_event_btn.pack(side=tk.LEFT)
        
    def create_buttons_section(self, parent):
        """Crée la section des boutons principaux"""
        button_frame = tk.Frame(parent, bg=parent.cget('bg'))
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        cancel_btn = tk.Button(button_frame, text="Annuler", 
                             command=self.close_popup,
                             font=("Arial", 10),
                             bg="#e0e0e0", fg="black")
        cancel_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        save_btn = tk.Button(button_frame, text="Sauvegarder", 
                           command=self.save_changes,
                           font=("Arial", 10, "bold"),
                           bg="#4A90E2", fg="white")
        save_btn.pack(side=tk.RIGHT)
        
    def add_event(self):
        """Ajoute un événement"""
        import tkinter.simpledialog
        event_name = tkinter.simpledialog.askstring("Nouvel événement", 
                                                   "Nom de l'événement:")
        if event_name and event_name.strip():
            self.events_listbox.insert(tk.END, event_name.strip())
            
    def remove_event(self):
        """Retire l'événement sélectionné"""
        selection = self.events_listbox.curselection()
        if selection:
            self.events_listbox.delete(selection[0])
            
    def save_changes(self):
        """Sauvegarde les modifications"""
        # Validation des champs obligatoires
        if not self.entries['nom'].get().strip() or not self.entries['prenom'].get().strip():
            messagebox.showerror("Erreur", "Le nom et le prénom sont obligatoires.")
            return
            
        # Préparer les données mises à jour
        updated_data = {}
        for field, entry in self.entries.items():
            updated_data[field] = entry.get().strip()
            
        # Récupérer les événements
        events = []
        for i in range(self.events_listbox.size()):
            events.append(self.events_listbox.get(i))
        updated_data['evenements'] = events
        
        # Appeler le callback de sauvegarde
        if self.on_save_callback:
            if self.on_save_callback(self.student_data.get('id'), updated_data):
                messagebox.showinfo("Succès", "Les modifications ont été sauvegardées.")
                self.close_popup()
            else:
                messagebox.showerror("Erreur", "Impossible de sauvegarder les modifications.")
        else:
            self.close_popup()
            
    def close_popup(self):
        """Ferme la popup"""
        if self.popup:
            self.popup.destroy()