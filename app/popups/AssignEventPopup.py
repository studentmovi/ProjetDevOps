import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

class AssignEventPopup:
    """Popup pour assigner des élèves à un événement"""
    
    def __init__(self, parent, selected_students, students_data, event_manager):
        self.parent = parent
        self.selected_students = selected_students
        self.students_data = students_data
        self.event_manager = event_manager
        self.popup = None
    
    def show(self):
        """Affiche le popup"""
        # Créer la fenêtre popup
        self.popup = tk.Toplevel(self.parent)
        self.popup.title("Assigner à un événement")
        self.popup.geometry("500x400")
        self.popup.configure(bg="#f8f9fa")
        self.popup.transient(self.parent)
        self.popup.grab_set()
        
        # Centrer la fenêtre
        self._center_window()
        
        # Créer l'interface
        self._create_header()
        self._create_main_content()
    
    def _center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.popup.update_idletasks()
        x = (self.popup.winfo_screenwidth() // 2) - (self.popup.winfo_width() // 2)
        y = (self.popup.winfo_screenheight() // 2) - (self.popup.winfo_height() // 2)
        self.popup.geometry(f"+{x}+{y}")
    
    def _create_header(self):
        """Crée le header du popup"""
        title_frame = tk.Frame(self.popup, bg="#007bff", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="📅 Assignation à un événement",
                font=("Helvetica", 14, "bold"), fg="white", bg="#007bff").pack(pady=15)
    
    def _create_main_content(self):
        """Crée le contenu principal"""
        main_frame = tk.Frame(self.popup, bg="#f8f9fa")
        main_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Section élèves sélectionnés
        self._create_students_section(main_frame)
        
        # Section choix d'événement
        self._create_event_section(main_frame)
        
        # Boutons d'action
        self._create_buttons(main_frame)
    
    def _create_students_section(self, parent):
        """Crée la section des élèves sélectionnés"""
        students_frame = tk.LabelFrame(parent, text="👥 Élèves sélectionnés", 
                                      font=("Helvetica", 10, "bold"), bg="#f8f9fa")
        students_frame.pack(fill="x", pady=(0, 15))
        
        # Liste des élèves
        students_text = tk.Text(students_frame, height=6, width=50, 
                               font=("Helvetica", 9), bg="white", wrap=tk.WORD)
        scrollbar = tk.Scrollbar(students_frame, orient="vertical", command=students_text.yview)
        students_text.configure(yscrollcommand=scrollbar.set)
        
        students_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)
        
        # Remplir la liste des élèves
        selected_names = []
        for student in self.students_data:
            if student["id"] in self.selected_students:
                selected_names.append(f"• {student['prenom']} {student['nom']} ({student['classe']})")
        
        students_text.insert("1.0", "\n".join(selected_names))
        students_text.config(state="disabled")
    
    def _create_event_section(self, parent):
        """Crée la section de choix d'événement"""
        event_frame = tk.LabelFrame(parent, text="📅 Choisir un événement",
                                   font=("Helvetica", 10, "bold"), bg="#f8f9fa")
        event_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(event_frame, text="Événement:", font=("Helvetica", 9, "bold"),
                bg="#f8f9fa").pack(anchor="w", padx=10, pady=(10, 5))
        
        events_list = self._get_events_list()
        
        self.event_var = tk.StringVar()
        event_combo = ttk.Combobox(event_frame, textvariable=self.event_var, values=events_list,
                                  state="readonly", width=60, font=("Helvetica", 9))
        event_combo.pack(padx=10, pady=(0, 10), fill="x")
        
        if events_list and events_list[0] != "Aucun événement disponible":
            event_combo.set(events_list[0])
    
    def _get_events_list(self):
        """Récupère la liste des événements disponibles"""
        try:
            events = self.event_manager.get_events()
            return [f"{event['nom']} - {event['date']} ({event.get('prix', 'N/A')}€)" 
                    for event in events]
        except:
            return ["Aucun événement disponible"]
    
    def _create_buttons(self, parent):
        """Crée les boutons d'action"""
        buttons_frame = tk.Frame(parent, bg="#f8f9fa")
        buttons_frame.pack(fill="x", pady=10)
        
        tk.Button(buttons_frame, text="✅ Confirmer l'assignation", 
                 command=self._confirm_assignment,
                 bg="#28a745", fg="white", font=("Helvetica", 10, "bold"),
                 relief="flat", padx=20, pady=8).pack(side="right", padx=(5, 0))
        
        tk.Button(buttons_frame, text="❌ Annuler", 
                 command=self._cancel_assignment,
                 bg="#dc3545", fg="white", font=("Helvetica", 10, "bold"),
                 relief="flat", padx=20, pady=8).pack(side="right")
    
    def _confirm_assignment(self):
        """Confirme l'assignation"""
        if not self.event_var.get():
            tkinter.messagebox.showwarning("Attention", "Veuillez sélectionner un événement !")
            return
        
        # Ici vous pourriez sauvegarder l'assignation dans votre système
        # self.event_manager.assign_students_to_event(self.selected_students, selected_event_id)
        
        tkinter.messagebox.showinfo("Succès", 
            f"✅ {len(self.selected_students)} élèves assignés à:\n{self.event_var.get()}")
        self.popup.destroy()
    
    def _cancel_assignment(self):
        """Annule l'assignation"""
        self.popup.destroy()