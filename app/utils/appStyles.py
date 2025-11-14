import tkinter as tk
from tkinter import ttk

class AppStyles:
    def __init__(self):
        # ========== PALETTE COULEURS BLEU PÂLE PROFESSIONNEL ==========
        self.colors = {
            # Bleus principaux
            'primary_blue': '#4A90E2',          # Bleu principal
            'light_blue': '#E3F2FD',            # Bleu très pâle pour fond
            'medium_blue': '#BBDEFB',           # Bleu moyen pour éléments
            'dark_blue': '#1976D2',             # Bleu foncé pour texte important
            'accent_blue': '#2196F3',           # Bleu accent pour boutons
            
            # Blancs et gris
            'white': '#FFFFFF',                 # Blanc pur
            'off_white': '#FAFAFA',             # Blanc cassé
            'light_gray': '#F5F5F5',            # Gris très clair
            'medium_gray': '#E0E0E0',           # Gris moyen
            'text_gray': '#424242',             # Gris pour texte
            'border_gray': '#BDBDBD',           # Gris pour bordures
            
            # Couleurs d'état
            'success': '#4CAF50',               # Vert pour succès
            'warning': '#FF9800',               # Orange pour avertissement  
            'error': '#F44336',                 # Rouge pour erreur
            'info': '#2196F3',                  # Bleu pour info
            
            # Couleurs spéciales
            'hover': '#E1F5FE',                 # Bleu très clair au survol
            'selected': '#B3E5FC',              # Bleu clair pour sélection
            'disabled': '#F5F5F5'               # Gris clair pour désactivé
        }
        
        # ========== POLICES ==========
        self.fonts = {
            'title': ('Segoe UI', 16, 'bold'),
            'subtitle': ('Segoe UI', 14, 'bold'),
            'heading': ('Segoe UI', 12, 'bold'),
            'body': ('Segoe UI', 10, 'normal'),
            'small': ('Segoe UI', 9, 'normal'),
            'tiny': ('Segoe UI', 8, 'normal'),
            'button': ('Segoe UI', 9, 'bold'),
            'code': ('Consolas', 9, 'normal')
        }
        
        # ========== DIMENSIONS ==========
        self.dimensions = {
            'padding_large': 15,
            'padding_medium': 10,
            'padding_small': 5,
            'margin_large': 20,
            'margin_medium': 10,
            'margin_small': 5,
            'border_width': 1,
            'button_height': 32,
            'input_height': 28
        }
    
    def configure_ttk_style(self, root):
        """Configure le style TTK avec le thème bleu professionnel"""
        style = ttk.Style(root)
        
        # ========== CONFIGURATION GÉNÉRALE ==========
        style.theme_use('clam')  # Base moderne
        
        # Configuration du fond principal
        style.configure('.',
            background=self.colors['off_white'],
            foreground=self.colors['text_gray'],
            font=self.fonts['body'],
            borderwidth=0,
            relief='flat'
        )
        
        # ========== FRAMES ==========
        style.configure('TFrame',
            background=self.colors['off_white'],
            borderwidth=0,
            relief='flat'
        )
        
        style.configure('Card.TFrame',
            background=self.colors['white'],
            borderwidth=1,
            relief='solid'
        )
        
        style.configure('Header.TFrame',
            background=self.colors['primary_blue'],
            borderwidth=0
        )
        
        # ========== LABELS ==========
        style.configure('TLabel',
            background=self.colors['off_white'],
            foreground=self.colors['text_gray'],
            font=self.fonts['body']
        )
        
        style.configure('Title.TLabel',
            background=self.colors['off_white'],
            foreground=self.colors['dark_blue'],
            font=self.fonts['title']
        )
        
        style.configure('Subtitle.TLabel',
            background=self.colors['off_white'],
            foreground=self.colors['primary_blue'],
            font=self.fonts['subtitle']
        )
        
        style.configure('Heading.TLabel',
            background=self.colors['off_white'],
            foreground=self.colors['dark_blue'],
            font=self.fonts['heading']
        )
        
        style.configure('Header.TLabel',
            background=self.colors['primary_blue'],
            foreground=self.colors['white'],
            font=self.fonts['heading']
        )
        
        style.configure('Small.TLabel',
            background=self.colors['off_white'],
            foreground=self.colors['text_gray'],
            font=self.fonts['small']
        )
        
        # ========== BOUTONS ==========
        # Bouton principal
        style.configure('Primary.TButton',
            background=self.colors['primary_blue'],
            foreground=self.colors['white'],
            font=self.fonts['button'],
            borderwidth=0,
            relief='flat',
            padding=(15, 8)
        )
        
        style.map('Primary.TButton',
            background=[
                ('active', self.colors['accent_blue']),
                ('pressed', self.colors['dark_blue']),
                ('disabled', self.colors['disabled'])
            ],
            foreground=[
                ('disabled', self.colors['text_gray'])
            ]
        )
        
        # Bouton secondaire
        style.configure('Secondary.TButton',
            background=self.colors['white'],
            foreground=self.colors['primary_blue'],
            font=self.fonts['button'],
            borderwidth=1,
            relief='solid',
            padding=(15, 8)
        )
        
        style.map('Secondary.TButton',
            background=[
                ('active', self.colors['hover']),
                ('pressed', self.colors['light_blue'])
            ]
        )
        
        # Bouton succès
        style.configure('Success.TButton',
            background=self.colors['success'],
            foreground=self.colors['white'],
            font=self.fonts['button'],
            borderwidth=0,
            relief='flat',
            padding=(15, 8)
        )
        
        # Bouton avertissement
        style.configure('Warning.TButton',
            background=self.colors['warning'],
            foreground=self.colors['white'],
            font=self.fonts['button'],
            borderwidth=0,
            relief='flat',
            padding=(15, 8)
        )
        
        # Bouton erreur
        style.configure('Error.TButton',
            background=self.colors['error'],
            foreground=self.colors['white'],
            font=self.fonts['button'],
            borderwidth=0,
            relief='flat',
            padding=(15, 8)
        )
        
        # Bouton léger
        style.configure('Light.TButton',
            background=self.colors['light_gray'],
            foreground=self.colors['text_gray'],
            font=self.fonts['button'],
            borderwidth=0,
            relief='flat',
            padding=(12, 6)
        )
        
        style.map('Light.TButton',
            background=[
                ('active', self.colors['medium_gray']),
                ('pressed', self.colors['border_gray'])
            ]
        )
        
        # ========== ENTRÉES ==========
        style.configure('TEntry',
            fieldbackground=self.colors['white'],
            foreground=self.colors['text_gray'],
            font=self.fonts['body'],
            borderwidth=1,
            relief='solid',
            insertcolor=self.colors['primary_blue'],
            padding=(8, 6)
        )
        
        style.map('TEntry',
            bordercolor=[
                ('focus', self.colors['primary_blue']),
                ('active', self.colors['accent_blue'])
            ],
            fieldbackground=[
                ('focus', self.colors['white']),
                ('active', self.colors['white'])
            ]
        )
        
        # ========== COMBOBOX ==========
        style.configure('TCombobox',
            fieldbackground=self.colors['white'],
            foreground=self.colors['text_gray'],
            font=self.fonts['body'],
            borderwidth=1,
            relief='solid',
            arrowcolor=self.colors['primary_blue'],
            padding=(8, 6)
        )
        
        style.map('TCombobox',
            bordercolor=[
                ('focus', self.colors['primary_blue']),
                ('active', self.colors['accent_blue'])
            ]
        )
        
        # ========== LABELFRAME ==========
        style.configure('TLabelframe',
            background=self.colors['off_white'],
            borderwidth=1,
            relief='solid',
            padding=(10, 10)
        )
        
        style.configure('TLabelframe.Label',
            background=self.colors['off_white'],
            foreground=self.colors['primary_blue'],
            font=self.fonts['heading']
        )
        
        # Style compact pour filtres
        style.configure('Compact.TLabelframe',
            background=self.colors['light_blue'],
            borderwidth=1,
            relief='solid',
            padding=(8, 6)
        )
        
        style.configure('Compact.TLabelframe.Label',
            background=self.colors['light_blue'],
            foreground=self.colors['dark_blue'],
            font=self.fonts['body']
        )
        
        # ========== TREEVIEW ==========
        style.configure('Treeview',
            background=self.colors['white'],
            foreground=self.colors['text_gray'],
            font=self.fonts['body'],
            borderwidth=1,
            relief='solid',
            rowheight=30
        )
        
        style.configure('Treeview.Heading',
            background=self.colors['primary_blue'],
            foreground=self.colors['white'],
            font=self.fonts['heading'],
            borderwidth=1,
            relief='flat'
        )
        
        style.map('Treeview.Heading',
            background=[('active', self.colors['accent_blue'])]
        )
        
        style.map('Treeview',
            background=[
                ('selected', self.colors['selected']),
                ('active', self.colors['hover'])
            ],
            foreground=[
                ('selected', self.colors['dark_blue'])
            ]
        )
        
        # ========== SCROLLBARS ==========
        style.configure('TScrollbar',
            background=self.colors['light_gray'],
            arrowcolor=self.colors['primary_blue'],
            troughcolor=self.colors['light_gray']
        )
        
        style.map('TScrollbar',
            background=[
                ('active', self.colors['medium_gray']),
                ('pressed', self.colors['primary_blue'])
            ]
        )
        
        # ========== CHECKBUTTON ==========
        style.configure('TCheckbutton',
            background=self.colors['off_white'],
            foreground=self.colors['text_gray'],
            font=self.fonts['body'],
            focuscolor=self.colors['primary_blue']
        )
        
        # ========== PROGRESSBAR ==========
        style.configure('TProgressbar',
            background=self.colors['primary_blue'],
            borderwidth=1,
            lightcolor=self.colors['light_blue'],
            darkcolor=self.colors['primary_blue']
        )
        
        # ========== SEPARATOR ==========
        style.configure('TSeparator',
            background=self.colors['medium_blue']
        )
        
        return style
    
    def get_button_style(self, button_type="primary"):
        """Retourne le style de bouton approprié"""
        style_map = {
            "primary": "Primary.TButton",
            "secondary": "Secondary.TButton", 
            "success": "Success.TButton",
            "warning": "Warning.TButton",
            "error": "Error.TButton",
            "light": "Light.TButton",
            "info": "Primary.TButton"
        }
        return style_map.get(button_type, "Primary.TButton")
    
    def configure_window(self, window, title="Application"):
        """Configure l'apparence d'une fenêtre"""
        window.configure(bg=self.colors['off_white'])
        window.title(title)
        
        # Icône de fenêtre (si disponible)
        try:
            # window.iconbitmap('path/to/icon.ico')
            pass
        except:
            pass
    
    def create_card_frame(self, parent, **kwargs):
        """Crée un frame avec style carte"""
        frame = ttk.Frame(parent, style='Card.TFrame', **kwargs)
        return frame
    
    def create_header_frame(self, parent, **kwargs):
        """Crée un frame d'en-tête"""
        frame = ttk.Frame(parent, style='Header.TFrame', **kwargs)
        return frame
    
    # ========== MÉTHODES MANQUANTES AJOUTÉES ==========
    def get_title_frame_config(self):
        """Retourne la configuration pour les frames de titre"""
        return {
            'bg': self.colors['primary_blue'],
            'relief': 'flat',
            'borderwidth': 0
        }
    
    def get_main_bg_color(self):
        """Retourne la couleur de fond principale"""
        return self.colors['off_white']
    
    def get_card_config(self):
        """Retourne la configuration pour les cartes"""
        return {
            'bg': self.colors['white'],
            'relief': 'solid',
            'borderwidth': 1,
            'bd': 1
        }
    
    def get_header_config(self):
        """Retourne la configuration pour l'en-tête"""
        return {
            'bg': self.colors['primary_blue'],
            'relief': 'flat',
            'borderwidth': 0
        }