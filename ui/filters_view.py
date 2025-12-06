# ui/filters_view.py
import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Optional, Dict, Any

class FiltersView(ttk.Frame):
    """
    A frame containing all the filtering widgets.
    """
    def __init__(self, parent, on_filter_change: Callable, available_categories: List[str], available_regions: List[str]):
        super().__init__(parent, padding="10")
        self.on_filter_change = on_filter_change
        
        # --- Filter Widgets ---
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()
        self.category_var = tk.StringVar(value="All")
        self.region_var = tk.StringVar(value="All")

        # Date filters
        ttk.Label(self, text="Start Date:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.start_date_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="End Date:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(self, textvariable=self.end_date_var).grid(row=1, column=1, padx=5, pady=5)

        # Category filter
        ttk.Label(self, text="Category:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        category_menu = ttk.Combobox(self, textvariable=self.category_var, values=["All"] + available_categories)
        category_menu.grid(row=0, column=3, padx=5, pady=5)

        # Region filter
        ttk.Label(self, text="Region:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        region_menu = ttk.Combobox(self, textvariable=self.region_var, values=["All"] + available_regions)
        region_menu.grid(row=1, column=3, padx=5, pady=5)
        
        # Apply button
        apply_button = ttk.Button(self, text="Apply Filters", command=self.on_filter_change)
        apply_button.grid(row=1, column=4, padx=10, pady=10)

    def get_filters(self) -> Dict[str, Any]:
        """
        Returns the current state of the filter widgets.
        """
        return {
            "start_date": self.start_date_var.get(),
            "end_date": self.end_date_var.get(),
            "category": self.category_var.get(),
            "region": self.region_var.get(),
        }
