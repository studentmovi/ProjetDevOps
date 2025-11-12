import tkinter as tk
from tkinter import ttk

class FilterPanel:
    """Panel de filtres réutilisable avec gestion des widgets"""
    
    def __init__(self, parent, title="Filtres"):
        self.parent = parent
        self.title = title
        self.filters = {}
        self.frame = None
        self.body = None
    
    def create(self):
        """Crée le panel principal"""
        self.frame = tk.LabelFrame(self.parent, text=f"🔍 {self.title}",
                                  font=("Helvetica", 11, "bold"),
                                  bg="#e3f2fd", fg="#1565c0", bd=2, relief="groove")
        
        # Body pour les filtres
        self.body = tk.Frame(self.frame, bg="#e3f2fd")
        self.body.pack(fill="x", padx=10, pady=8)
        
        return self.frame
    
    def add_combobox_filter(self, name, label, values, default=None, callback=None):
        """Ajoute un filtre combobox"""
        container = tk.Frame(self.body, bg="#e3f2fd")
        container.pack(side="left", padx=8, pady=2)
        
        # Label
        label_widget = tk.Label(container, text=f"{label}:",
                               font=("Helvetica", 9, "bold"),
                               bg="#e3f2fd", fg="#1565c0")
        label_widget.pack(anchor="w")
        
        # Variable et widget
        var = tk.StringVar()
        if default:
            var.set(default)
        elif values:
            var.set(values[0])
        
        combo = ttk.Combobox(container, textvariable=var, values=values,
                            state="readonly", width=14, font=("Helvetica", 9))
        combo.pack()
        
        # Callback
        if callback:
            combo.bind("<<ComboboxSelected>>", callback)
        
        # Stockage
        self.filters[name] = {
            'var': var,
            'widget': combo,
            'type': 'combobox',
            'container': container
        }
        
        return var, combo
    
    def add_entry_filter(self, name, label, placeholder="", callback=None):
        """Ajoute un filtre entry avec placeholder"""
        container = tk.Frame(self.body, bg="#e3f2fd")
        container.pack(side="left", padx=8, pady=2)
        
        # Label
        label_widget = tk.Label(container, text=f"{label}:",
                               font=("Helvetica", 9, "bold"),
                               bg="#e3f2fd", fg="#1565c0")
        label_widget.pack(anchor="w")
        
        # Variable et widget
        var = tk.StringVar()
        entry = tk.Entry(container, textvariable=var, width=16,
                        font=("Helvetica", 9))
        entry.pack()
        
        # Placeholder
        if placeholder:
            entry.insert(0, placeholder)
            entry.config(fg='gray')
            
            def on_focus_in(event):
                if var.get() == placeholder:
                    var.set("")
                    entry.config(fg='black')
            
            def on_focus_out(event):
                if var.get() == "":
                    var.set(placeholder)
                    entry.config(fg='gray')
            
            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)
        
        # Callback
        if callback:
            var.trace('w', callback)
        
        # Stockage
        self.filters[name] = {
            'var': var,
            'widget': entry,
            'type': 'entry',
            'container': container,
            'placeholder': placeholder
        }
        
        return var, entry
    
    def get_filter_value(self, name):
        """Récupère la valeur d'un filtre"""
        if name in self.filters:
            value = self.filters[name]['var'].get()
            
            filter_data = self.filters[name]
            
            # Pour les Entry avec placeholder
            if filter_data['type'] == 'entry':
                placeholder = filter_data.get('placeholder', '')
                if value == placeholder:
                    return ""
                
                # Vérifier si le texte est en gris (placeholder actif)
                try:
                    widget = filter_data['widget']
                    if hasattr(widget, 'cget') and widget.cget('fg') == 'gray':
                        return ""
                except:
                    pass
            
            return value
        return None
    
    def set_filter_value(self, name, value):
        """Définit la valeur d'un filtre"""
        if name in self.filters:
            filter_data = self.filters[name]
            filter_data['var'].set(value)
            
            # Pour les Entry, gérer le placeholder
            if filter_data['type'] == 'entry':
                widget = filter_data['widget']
                placeholder = filter_data.get('placeholder', '')
                
                if value == "" and placeholder:
                    widget.delete(0, tk.END)
                    widget.insert(0, placeholder)
                    widget.config(fg='gray')
                else:
                    widget.config(fg='black')
    
    def reset_all_filters(self):
        """Remet à zéro tous les filtres"""
        for name, filter_data in self.filters.items():
            if filter_data['type'] == 'combobox':
                combo = filter_data['widget']
                values = combo.cget('values')
                if values:
                    if name in ["year", "class"]:
                        filter_data['var'].set("Toutes")
                    elif name == "event":
                        filter_data['var'].set("Aucun")
                    elif name == "sort":
                        filter_data['var'].set("Nom A-Z")
                    else:
                        filter_data['var'].set(values[0])
            
            elif filter_data['type'] == 'entry':
                placeholder = filter_data.get('placeholder', '')
                filter_data['var'].set("")
                widget = filter_data['widget']
                widget.delete(0, tk.END)
                if placeholder:
                    widget.insert(0, placeholder)
                    widget.config(fg='gray')
    
    def add_action_buttons(self, reset_callback=None, export_callback=None):
        """Ajoute les boutons d'action"""
        actions_frame = tk.Frame(self.body, bg="#e3f2fd")
        actions_frame.pack(side="right", padx=10)
        
        if reset_callback:
            reset_btn = tk.Button(actions_frame, text="🔄 Reset",
                                 command=lambda: [self.reset_all_filters(), reset_callback()],
                                 bg="#ff7043", fg="white", font=("Helvetica", 8),
                                 relief="flat", padx=8, pady=3)
            reset_btn.pack(side="left", padx=2)
        
        if export_callback:
            export_btn = tk.Button(actions_frame, text="📤 Export",
                                  command=export_callback,
                                  bg="#4caf50", fg="white", font=("Helvetica", 8),
                                  relief="flat", padx=8, pady=3)
            export_btn.pack(side="left", padx=2)
    
    def get_body(self):
        """Retourne le body pour ajouter des éléments personnalisés"""
        return self.body