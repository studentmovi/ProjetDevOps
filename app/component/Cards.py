import tkinter as tk
from tkinter import ttk

class Card:
    """Composant Card réutilisable"""
    
    def __init__(self, parent, title="", card_type='default', padding=10):
        self.parent = parent
        self.title = title
        self.card_type = card_type
        self.padding = padding
        
        # Styles des cartes
        self.card_styles = {
            'default': {
                'bg': '#ffffff',
                'header_bg': '#f8f9fa',
                'border_color': '#dee2e6',
                'text_color': '#2c3e50'
            },
            'primary': {
                'bg': '#e8eaf6',
                'header_bg': '#3742fa',
                'border_color': '#3742fa',
                'text_color': '#1a237e'
            },
            'success': {
                'bg': '#d5f4e6',
                'header_bg': '#2ed573',
                'border_color': '#2ed573',
                'text_color': '#155724'
            },
            'info': {
                'bg': '#e3f2fd',
                'header_bg': '#1e90ff',
                'border_color': '#1e90ff',
                'text_color': '#0c5460'
            },
            'warning': {
                'bg': '#fff3cd',
                'header_bg': '#ffa502',
                'border_color': '#ffa502',
                'text_color': '#856404'
            },
            'danger': {
                'bg': '#f8d7da',
                'header_bg': '#ff4757',
                'border_color': '#ff4757',
                'text_color': '#721c24'
            }
        }
    
    def create(self):
        """Crée et retourne la carte"""
        style = self.card_styles.get(self.card_type, self.card_styles['default'])
        
        # Frame principal de la carte
        self.card_frame = tk.Frame(
            self.parent,
            bg=style['bg'],
            relief='raised',
            bd=1,
            highlightbackground=style['border_color'],
            highlightthickness=1
        )
        
        # Header si titre fourni
        if self.title:
            self.header_frame = tk.Frame(
                self.card_frame,
                bg=style['header_bg'],
                height=40
            )
            self.header_frame.pack(fill='x')
            self.header_frame.pack_propagate(False)
            
            self.title_label = tk.Label(
                self.header_frame,
                text=self.title,
                bg=style['header_bg'],
                fg='white',
                font=('Helvetica', 11, 'bold'),
                padx=self.padding,
                pady=8
            )
            self.title_label.pack(side='left')
        
        # Body de la carte
        self.body_frame = tk.Frame(
            self.card_frame,
            bg=style['bg']
        )
        self.body_frame.pack(fill='both', expand=True, padx=self.padding, pady=self.padding)
        
        return self.card_frame
    
    def get_body(self):
        """Retourne le frame body pour ajouter du contenu"""
        return self.body_frame
    
    def add_content(self, widget):
        """Ajoute un widget au body de la carte"""
        widget.pack(in_=self.body_frame, fill='x', pady=2)
        return widget

class StatCard(Card):
    """Carte spécialisée pour afficher des statistiques"""
    
    def __init__(self, parent, title, value, subtitle="", icon="📊", card_type='info'):
        super().__init__(parent, title, card_type)
        self.value = value
        self.subtitle = subtitle
        self.icon = icon
    
    def create(self):
        """Crée une carte de statistique"""
        # Vérifier que le card_type existe, sinon utiliser 'default'
        if self.card_type not in self.card_styles:
            self.card_type = 'default'
        
        # Utiliser la méthode parent pour créer la structure de base
        card_frame = super().create()
        body = self.get_body()
        
        # Container principal
        content_frame = tk.Frame(body, bg=self.card_styles[self.card_type]['bg'])
        content_frame.pack(fill='both', expand=True)
        
        # Icône à gauche
        icon_label = tk.Label(
            content_frame,
            text=self.icon,
            font=('Helvetica', 24),
            bg=self.card_styles[self.card_type]['bg']
        )
        icon_label.pack(side='left', padx=(0, 15))
        
        # Contenu à droite
        text_frame = tk.Frame(content_frame, bg=self.card_styles[self.card_type]['bg'])
        text_frame.pack(side='left', fill='both', expand=True)
        
        # Valeur principale
        value_label = tk.Label(
            text_frame,
            text=str(self.value),
            font=('Helvetica', 18, 'bold'),
            fg=self.card_styles[self.card_type]['text_color'],
            bg=self.card_styles[self.card_type]['bg']
        )
        value_label.pack(anchor='w')
        
        # Sous-titre si fourni
        if self.subtitle:
            subtitle_label = tk.Label(
                text_frame,
                text=self.subtitle,
                font=('Helvetica', 9),
                fg='#6c757d',
                bg=self.card_styles[self.card_type]['bg']
            )
            subtitle_label.pack(anchor='w')
        
        return card_frame