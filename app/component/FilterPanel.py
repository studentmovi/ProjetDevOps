import tkinter as tk
from tkinter import ttk
from component.Button import ActionButton

class FilterPanel:
    """Composant réutilisable pour les panneaux de filtres"""
    
    def __init__(self, parent, title="Filtres"):
        self.parent = parent
        self.title = title
        self.filters = {}
        self.callbacks = {}
        
    def create(self):
        """Crée le panneau de filtres"""
        # Frame principal avec style
        self.panel_frame = ttk.LabelFrame(
            self.parent,
            text=f"🔍 {self.title}",
            padding=15
        )
        
        # Container pour les filtres
        self.filters_container = tk.Frame(self.panel_frame, bg='#e3f2fd')
        self.filters_container.pack(fill='x', pady=5)
        
        # Container pour les boutons
        self.buttons_container = tk.Frame(self.panel_frame, bg='#e3f2fd')
        self.buttons_container.pack(fill='x', pady=(10, 0))
        
        return self.panel_frame
    
    def add_combobox_filter(self, name, label, values, default="Toutes", callback=None):
        """Ajoute un filtre combobox"""
        # Container pour ce filtre
        filter_container = tk.Frame(self.filters_container, bg='#e3f2fd')
        filter_container.pack(side='left', padx=(0, 20))
        
        # Label
        label_widget = tk.Label(
            filter_container,
            text=f"📋 {label}:",
            font=('Helvetica', 9, 'bold'),
            fg='#2c3e50',
            bg='#e3f2fd'
        )
        label_widget.pack()
        
        # Variable et combobox
        var = tk.StringVar()
        combobox = ttk.Combobox(
            filter_container,
            textvariable=var,
            values=values,
            state='readonly',
            width=12,
            font=('Helvetica', 9)
        )
        combobox.pack(pady=2)
        combobox.set(default)
        
        # Callback si fourni
        if callback:
            combobox.bind("<<ComboboxSelected>>", callback)
            self.callbacks[name] = callback
        
        # Stocker la référence
        self.filters[name] = {'var': var, 'widget': combobox}
        
        return var, combobox
    
    def add_entry_filter(self, name, label, placeholder="", callback=None):
        """Ajoute un filtre de saisie de texte"""
        filter_container = tk.Frame(self.filters_container, bg='#e3f2fd')
        filter_container.pack(side='left', padx=(0, 20))
        
        # Label
        label_widget = tk.Label(
            filter_container,
            text=f"✏️ {label}:",
            font=('Helvetica', 9, 'bold'),
            fg='#2c3e50',
            bg='#e3f2fd'
        )
        label_widget.pack()
        
        # Entry
        var = tk.StringVar()
        entry = tk.Entry(
            filter_container,
            textvariable=var,
            width=15,
            font=('Helvetica', 9)
        )
        entry.pack(pady=2)
        
        # Placeholder
        if placeholder:
            entry.insert(0, placeholder)
            entry.config(fg='gray')
            
            def on_focus_in(event):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg='black')
            
            def on_focus_out(event):
                if entry.get() == "":
                    entry.insert(0, placeholder)
                    entry.config(fg='gray')
            
            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)
        
        # Callback
        if callback:
            var.trace('w', callback)
            self.callbacks[name] = callback
        
        self.filters[name] = {'var': var, 'widget': entry}
        return var, entry
    
    def add_action_buttons(self, reset_callback=None, export_callback=None):
        """Ajoute les boutons d'action standard"""
        try:
            if reset_callback:
                reset_btn = ActionButton(
                    self.buttons_container,
                    "Réinitialiser",
                    command=reset_callback,
                    action_type='danger'
                ).create()
                reset_btn.pack(side='left', padx=2)
            
            if export_callback:
                export_btn = ActionButton(
                    self.buttons_container,
                    "Exporter",
                    command=export_callback,
                    action_type='export'
                ).create()
                export_btn.pack(side='left', padx=2)
        
        except Exception as e:
            print(f"Erreur ActionButton: {e}")
            # Fallback avec boutons tkinter standard
            if reset_callback:
                reset_btn = tk.Button(
                    self.buttons_container,
                    text="🔄 Réinitialiser",
                    command=reset_callback,
                    bg='#ff4757',
                    fg='white',
                    font=('Helvetica', 8, 'bold'),
                    relief='flat',
                    padx=10,
                    pady=5
                )
                reset_btn.pack(side='left', padx=2)
            
            if export_callback:
                export_btn = tk.Button(
                    self.buttons_container,
                    text="📤 Exporter",
                    command=export_callback,
                    bg='#ffa502',
                    fg='white',
                    font=('Helvetica', 8, 'bold'),
                    relief='flat',
                    padx=10,
                    pady=5
                )
                export_btn.pack(side='left', padx=2)
    
    def get_filter_value(self, name):
        """Récupère la valeur d'un filtre"""
        if name in self.filters:
            return self.filters[name]['var'].get()
        return None
    
    def set_filter_value(self, name, value):
        """Définit la valeur d'un filtre"""
        if name in self.filters:
            self.filters[name]['var'].set(value)
    
    def reset_all_filters(self):
        """Remet à zéro tous les filtres"""
        for name, filter_data in self.filters.items():
            widget_type = str(type(filter_data['widget']))
            if 'Combobox' in widget_type:
                filter_data['var'].set("Toutes")
            else:
                filter_data['var'].set("")