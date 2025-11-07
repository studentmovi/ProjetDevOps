from tkinter import ttk
import tkinter as tk

class AppStyles:
    """Classe pour gérer tous les styles de l'application"""
    
    def __init__(self):
        self.colors = {
            'primary': '#3742fa',      # Bleu vif
            'success': '#2ed573',      # Vert
            'info': '#1e90ff',         # Bleu clair
            'warning': '#ffa502',      # Orange
            'danger': '#ff4757',       # Rouge
            'light': '#f1f2f6',        # Gris clair
            'dark': '#2f3542',         # Gris foncé
            'navbar': '#2c3e50',       # Bleu-gris foncé pour navbar
            'background': '#f5f6fa',   # Fond général
            'white': '#ffffff',
            'text_primary': '#2c3e50',
            'text_secondary': '#7f8c8d',
            'text_light': '#bdc3c7'
        }
    
    def setup_ttk_styles(self):
        """Configure tous les styles TTK"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Styles pour les boutons de navigation
        self._setup_navigation_styles(style)
        
        # Styles pour les LabelFrames
        self._setup_labelframe_styles(style)
        
        # Styles pour les autres composants
        self._setup_misc_styles(style)
    
    def _setup_navigation_styles(self, style):
        """Configure les styles des boutons de navigation"""
        # Bouton Accueil (Vert)
        style.configure("Nav.Home.TButton", 
                       padding=(12, 8), 
                       font=("Helvetica", 9, "bold"),
                       foreground='white',
                       background=self.colors['success'])
        
        style.map("Nav.Home.TButton",
                 background=[('active', '#27ae60')])
        
        # Bouton Élèves (Bleu)
        style.configure("Nav.Students.TButton", 
                       padding=(12, 8), 
                       font=("Helvetica", 9, "bold"),
                       foreground='white',
                       background=self.colors['primary'])
        
        style.map("Nav.Students.TButton",
                 background=[('active', '#2c3e50')])
        
        # Bouton Événements (Bleu clair)
        style.configure("Nav.Events.TButton", 
                       padding=(12, 8), 
                       font=("Helvetica", 9, "bold"),
                       foreground='white',
                       background=self.colors['info'])
        
        style.map("Nav.Events.TButton",
                 background=[('active', '#3498db')])
        
        # Bouton Import (Orange)
        style.configure("Nav.Import.TButton", 
                       padding=(12, 8), 
                       font=("Helvetica", 9, "bold"),
                       foreground='white',
                       background=self.colors['warning'])
        
        style.map("Nav.Import.TButton",
                 background=[('active', '#e67e22')])
    
    def _setup_labelframe_styles(self, style):
        """Configure les styles des LabelFrames"""
        # Style Success (Vert)
        style.configure("Success.TLabelframe", 
                       background="#d5f4e6", 
                       borderwidth=2, 
                       relief="solid",
                       bordercolor=self.colors['success'])
        
        style.configure("Success.TLabelframe.Label", 
                       font=("Helvetica", 10, "bold"), 
                       background="#d5f4e6",
                       foreground=self.colors['success'])
        
        # Style Info (Bleu)
        style.configure("Info.TLabelframe", 
                       background="#e3f2fd", 
                       borderwidth=2, 
                       relief="solid",
                       bordercolor=self.colors['info'])
        
        style.configure("Info.TLabelframe.Label", 
                       font=("Helvetica", 10, "bold"), 
                       background="#e3f2fd",
                       foreground=self.colors['info'])
        
        # Style Warning (Orange)
        style.configure("Warning.TLabelframe", 
                       background="#fff3cd", 
                       borderwidth=2, 
                       relief="solid",
                       bordercolor=self.colors['warning'])
        
        style.configure("Warning.TLabelframe.Label", 
                       font=("Helvetica", 10, "bold"), 
                       background="#fff3cd",
                       foreground=self.colors['warning'])
        
        # Style Primary (Bleu foncé)
        style.configure("Primary.TLabelframe", 
                       background="#e8eaf6", 
                       borderwidth=2, 
                       relief="solid",
                       bordercolor=self.colors['primary'])
        
        style.configure("Primary.TLabelframe.Label", 
                       font=("Helvetica", 10, "bold"), 
                       background="#e8eaf6",
                       foreground=self.colors['primary'])
    
    def _setup_misc_styles(self, style):
        """Configure les autres styles"""
        # Style pour les Treeview
        style.configure("Treeview.Heading", 
                       font=("Helvetica", 9, "bold"),
                       background=self.colors['light'],
                       foreground=self.colors['text_primary'])
        
        # Style pour les Combobox
        style.configure("TCombobox", 
                       fieldbackground=self.colors['white'],
                       font=("Helvetica", 9))
    
    def get_navbar_config(self):
        """Retourne la configuration pour la barre de navigation"""
        return {
            'bg': self.colors['navbar'],
            'height': 60
        }
    
    def get_title_frame_config(self, color_type='primary'):
        """Retourne la configuration pour les frames de titre (SANS fg)"""
        bg_colors = {
            'primary': self.colors['primary'],
            'success': self.colors['success'],
            'info': self.colors['info'],
            'warning': self.colors['warning']
        }
        
        return {
            'bg': bg_colors.get(color_type, self.colors['primary']),
            'height': 80
        }
    
    def get_title_label_config(self, color_type='primary'):
        """Retourne la configuration pour les labels de titre"""
        bg_colors = {
            'primary': self.colors['primary'],
            'success': self.colors['success'],
            'info': self.colors['info'],
            'warning': self.colors['warning']
        }
        
        return {
            'bg': bg_colors.get(color_type, self.colors['primary']),
            'fg': self.colors['white'],
            'font': ("Helvetica", 18, "bold")
        }
    
    def get_subtitle_label_config(self, color_type='primary'):
        """Retourne la configuration pour les labels de sous-titre"""
        bg_colors = {
            'primary': self.colors['primary'],
            'success': self.colors['success'],
            'info': self.colors['info'],
            'warning': self.colors['warning']
        }
        
        return {
            'bg': bg_colors.get(color_type, self.colors['primary']),
            'fg': self.colors['text_light'],
            'font': ("Helvetica", 10)
        }
    
    def get_button_config(self, button_type='default'):
        """Retourne la configuration pour les boutons"""
        configs = {
            'success': {
                'bg': self.colors['success'],
                'fg': self.colors['white'],
                'activebackground': '#27ae60',
                'font': ("Helvetica", 8, "bold"),
                'relief': 'flat',
                'padx': 10,
                'pady': 5
            },
            'danger': {
                'bg': self.colors['danger'],
                'fg': self.colors['white'],
                'activebackground': '#c0392b',
                'font': ("Helvetica", 8, "bold"),
                'relief': 'flat',
                'padx': 10,
                'pady': 5
            },
            'warning': {
                'bg': self.colors['warning'],
                'fg': self.colors['white'],
                'activebackground': '#e67e22',
                'font': ("Helvetica", 8, "bold"),
                'relief': 'flat',
                'padx': 10,
                'pady': 5
            },
            'info': {
                'bg': self.colors['info'],
                'fg': self.colors['white'],
                'activebackground': '#3498db',
                'font': ("Helvetica", 8, "bold"),
                'relief': 'flat',
                'padx': 10,
                'pady': 5
            }
        }
        
        return configs.get(button_type, configs['success'])
    
    def get_card_config(self, card_type='default'):
        """Retourne la configuration pour les cartes"""
        configs = {
            'success': {
                'bg': '#d5f4e6',
                'header_bg': self.colors['success'],
                'border_color': self.colors['success']
            },
            'info': {
                'bg': '#e3f2fd',
                'header_bg': self.colors['info'],
                'border_color': self.colors['info']
            },
            'warning': {
                'bg': '#fff3cd',
                'header_bg': self.colors['warning'],
                'border_color': self.colors['warning']
            },
            'primary': {
                'bg': '#e8eaf6',
                'header_bg': self.colors['primary'],
                'border_color': self.colors['primary']
            }
        }
        
        return configs.get(card_type, configs['primary'])
    
    def get_badge_config(self, badge_type='primary'):
        """Retourne la configuration pour les badges"""
        configs = {
            'success': {
                'bg': self.colors['success'],
                'fg': self.colors['white']
            },
            'info': {
                'bg': self.colors['info'],
                'fg': self.colors['white']
            },
            'warning': {
                'bg': self.colors['warning'],
                'fg': self.colors['white']
            },
            'primary': {
                'bg': self.colors['primary'],
                'fg': self.colors['white']
            }
        }
        
        return configs.get(badge_type, configs['primary'])