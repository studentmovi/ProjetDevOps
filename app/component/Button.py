import tkinter as tk
from tkinter import ttk


class StyledButton:
    """
    Bouton custom basé sur tk.Button
    - Supporte button_type OU style (compatibilité)
    - Ne transmet JAMAIS d'options invalides à tk.Button
    """

    def __init__(
        self,
        parent,
        text,
        command=None,
        button_type="primary",
        icon="",
        **kwargs
    ):
        # ====================================================
        #  COMPATIBILITÉ : style=xxx → button_type
        # ====================================================
        if "style" in kwargs:
            button_type = kwargs.pop("style")

        self.parent = parent
        self.text = text
        self.command = command
        self.button_type = button_type
        self.icon = icon

        # Styles prédéfinis
        self.styles = {
            "primary": {
                "bg": "#3742fa",
                "fg": "white",
                "activebackground": "#2c3e50",
                "font": ("Helvetica", 9, "bold"),
                "relief": "flat",
                "padx": 12,
                "pady": 6,
                "cursor": "hand2"
            },
            "success": {
                "bg": "#2ed573",
                "fg": "white",
                "activebackground": "#27ae60",
                "font": ("Helvetica", 9, "bold"),
                "relief": "flat",
                "padx": 12,
                "pady": 6,
                "cursor": "hand2"
            },
            "danger": {
                "bg": "#ff4757",
                "fg": "white",
                "activebackground": "#c0392b",
                "font": ("Helvetica", 9, "bold"),
                "relief": "flat",
                "padx": 12,
                "pady": 6,
                "cursor": "hand2"
            },
            "warning": {
                "bg": "#ffa502",
                "fg": "white",
                "activebackground": "#e67e22",
                "font": ("Helvetica", 9, "bold"),
                "relief": "flat",
                "padx": 12,
                "pady": 6,
                "cursor": "hand2"
            },
            "info": {
                "bg": "#1e90ff",
                "fg": "white",
                "activebackground": "#3498db",
                "font": ("Helvetica", 9, "bold"),
                "relief": "flat",
                "padx": 12,
                "pady": 6,
                "cursor": "hand2"
            },
            "light": {
                "bg": "#f1f2f6",
                "fg": "#2c3e50",
                "activebackground": "#dfe4ea",
                "font": ("Helvetica", 9),
                "relief": "flat",
                "padx": 12,
                "pady": 6,
                "cursor": "hand2"
            }
        }

        # Fusion finale des configs
        style_config = self.styles.get(self.button_type, self.styles["primary"])
        self.config = {**style_config, **kwargs}

        self.widget = self._create_widget()

    # ====================================================
    #  CRÉATION DU WIDGET TK
    # ====================================================
    def _create_widget(self):
        display_text = f"{self.icon} {self.text}".strip()

        btn = tk.Button(
            self.parent,
            text=display_text,
            command=self.command,
            **self.config
        )

        self._add_hover_effects(btn)
        return btn

    # ====================================================
    #  EFFETS HOVER
    # ====================================================
    def _add_hover_effects(self, button):
        normal_bg = self.config.get("bg")
        hover_bg = self.config.get("activebackground", normal_bg)

        def on_enter(_):
            button.config(bg=hover_bg)

        def on_leave(_):
            button.config(bg=normal_bg)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    # ====================================================
    #  PROXY PACK / GRID / PLACE
    # ====================================================
    def pack(self, *args, **kwargs):
        self.widget.pack(*args, **kwargs)

    def grid(self, *args, **kwargs):
        self.widget.grid(*args, **kwargs)

    def place(self, *args, **kwargs):
        self.widget.place(*args, **kwargs)

    def destroy(self):
        self.widget.destroy()


class NavButton(StyledButton):
    """Bouton spécialisé pour la navigation"""
    
    def __init__(self, parent, text, command=None, nav_type='home', **kwargs):
        # Mapping des types de navigation vers les styles et icônes
        nav_configs = {
            'home': {'button_type': 'success', 'icon': '🏠'},
            'students': {'button_type': 'primary', 'icon': '👥'},
            'events': {'button_type': 'info', 'icon': '📊'},
            'import': {'button_type': 'warning', 'icon': '📁'},
            'export': {'button_type': 'info', 'icon': '💾'},
            'settings': {'button_type': 'light', 'icon': '⚙️'}
        }
        
        config = nav_configs.get(nav_type, nav_configs['home'])
        
        super().__init__(
            parent, 
            text, 
            command, 
            button_type=config['button_type'],
            icon=config['icon'],
            **kwargs
        )

class ActionButton(StyledButton):
    """Bouton spécialisé pour les actions"""
    
    def __init__(self, parent, text, command=None, action_type='save', **kwargs):
        # Mapping des types d'actions
        action_configs = {
            'save': {'button_type': 'success', 'icon': '💾'},
            'delete': {'button_type': 'danger', 'icon': '🗑️'},
            'edit': {'button_type': 'info', 'icon': '✏️'},
            'add': {'button_type': 'success', 'icon': '➕'},
            'cancel': {'button_type': 'light', 'icon': '❌'},
            'refresh': {'button_type': 'info', 'icon': '🔄'},
            'search': {'button_type': 'primary', 'icon': '🔍'},
            'export': {'button_type': 'warning', 'icon': '📤'},
            'import': {'button_type': 'warning', 'icon': '📥'},
            'print': {'button_type': 'light', 'icon': '🖨️'}
        }
        
        config = action_configs.get(action_type, action_configs['save'])
        
        super().__init__(
            parent, 
            text, 
            command, 
            button_type=config['button_type'],
            icon=config['icon'],
            **kwargs
        )