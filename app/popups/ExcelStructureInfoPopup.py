import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from component.Button import StyledButton as Button

class ExcelStructureInfoPopup:
    def __init__(self, parent, callback=None):
        """
        Popup d'information sur la structure attendue du fichier Excel
        
        Args:
            parent: Fenêtre parent
            callback: Fonction à appeler après validation
        """
        self.parent = parent
        self.callback = callback
        self.popup = None
        
    def show(self):
        """Affiche la popup d'information"""
        self.popup = tk.Toplevel(self.parent)
        self.popup.title("Structure du fichier Excel")
        self.popup.geometry("500x400")
        self.popup.resizable(False, False)
        self.popup.transient(self.parent)
        self.popup.grab_set()
        
        # Centrer la popup
        self.popup.update_idletasks()
        x = (self.popup.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.popup.winfo_screenheight() // 2) - (400 // 2)
        self.popup.geometry(f"500x400+{x}+{y}")
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Crée les widgets de la popup"""
        main_frame = ttk.Frame(self.popup, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Titre
        title_label = ttk.Label(
            main_frame, 
            text="📋 Structure du fichier Excel pour l'import des élèves",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Frame pour les instructions
        info_frame = ttk.LabelFrame(main_frame, text="Instructions", padding="15")
        info_frame.pack(fill="x", pady=(0, 20))
        
        # Instructions détaillées
        instructions = [
            "📁 Nom du fichier : eleves.xlsx",
            "📄 Le fichier doit contenir une seule feuille Excel",
            "📊 Colonnes obligatoires (dans cet ordre) :"
        ]
        
        for instruction in instructions:
            label = ttk.Label(info_frame, text=instruction, font=("Arial", 10))
            label.pack(anchor="w", pady=2)
            
        # Frame pour les colonnes
        columns_frame = ttk.Frame(info_frame)
        columns_frame.pack(fill="x", pady=(10, 0))
        
        columns = ["1. Nom", "2. Prénom", "3. Classe", "4. Email"]
        for i, col in enumerate(columns):
            col_label = ttk.Label(columns_frame, text=f"   • {col}", font=("Arial", 10))
            col_label.pack(anchor="w", pady=1)
            
        # Exemple
        example_frame = ttk.LabelFrame(main_frame, text="Exemple", padding="15")
        example_frame.pack(fill="x", pady=(0, 20))
        
        example_text = """Nom      | Prénom  | Classe | Email
Dupont   | Pierre  | 3A     | pierre.dupont@email.com
Martin   | Sophie  | 2B     | sophie.martin@email.com"""
        
        example_label = ttk.Label(
            example_frame, 
            text=example_text, 
            font=("Courier", 9),
            justify="left"
        )
        example_label.pack(anchor="w")
        
        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side="bottom", fill="x")
        
        cancel_btn = Button(
            button_frame,
            text="Annuler",
            command=self._on_cancel,
            style="secondary"
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        continue_btn = Button(
            button_frame,
            text="Continuer l'import",
            command=self._on_continue,
            style="primary"
        )
        continue_btn.pack(side="right")
        
    def _on_cancel(self):
        """Annule l'opération"""
        self.popup.destroy()
        
    def _on_continue(self):
        """Continue vers la sélection de fichier"""
        self.popup.destroy()
        if self.callback:
            self.callback()