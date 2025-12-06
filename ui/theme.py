# ui/theme.py
from tkinter import ttk
import matplotlib.pyplot as plt

THEME_LIGHT = "default"
THEME_DARK = "clam" 

def set_theme(root, theme_name):
    """
    Sets the ttk theme and matplotlib style.
    """
    style = ttk.Style(root)
    style.theme_use(theme_name)

    if theme_name == THEME_DARK:
        # Dark theme settings
        style.configure("TFrame", background="#333")
        style.configure("TLabel", background="#333", foreground="#FFF")
        style.configure("TButton", background="#555", foreground="#FFF")
        style.map("TButton", background=[('active', '#666')])
        style.configure("TNotebook", background="#333", borderwidth=1)
        style.configure("TNotebook.Tab", background="#555", foreground="#FFF", padding=[5, 2])
        style.map("TNotebook.Tab", background=[("selected", "#333"), ("active", "#666")])
        
        plt.style.use('dark_background')
    else:
        # Light theme settings (or reset to default)
        style.configure("TFrame", background="#F0F0F0")
        style.configure("TLabel", background="#F0F0F0", foreground="#000")
        style.configure("TButton", background="#E1E1E1", foreground="#000")
        style.map("TButton", background=[('active', '#DADADA')])
        style.configure("TNotebook", background="#F0F0F0", borderwidth=1)
        style.configure("TNotebook.Tab", background="#E1E1E1", foreground="#000", padding=[5, 2])
        style.map("TNotebook.Tab", background=[("selected", "#F0F0F0"), ("active", "#DADADA")])
        
        plt.style.use('default')
