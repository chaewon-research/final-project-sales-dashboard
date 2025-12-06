# ui/kpi_view.py
import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import Kpi

class KpiView(ttk.Frame):
    """
    A frame to display Key Performance Indicators.
    """
    def __init__(self, parent):
        super().__init__(parent, padding="10")

        self.kpi_vars = {
            "total_revenue": tk.StringVar(value="Total Revenue: N/A"),
            "total_units_sold": tk.StringVar(value="Total Units Sold: N/A"),
            "average_order_value": tk.StringVar(value="Avg. Order Value: N/A"),
        }

        # Create labels for each KPI
        ttk.Label(self, textvariable=self.kpi_vars["total_revenue"], font=("Helvetica", 14, "bold")).pack(pady=5, anchor="w")
        ttk.Label(self, textvariable=self.kpi_vars["total_units_sold"], font=("Helvetica", 14, "bold")).pack(pady=5, anchor="w")
        ttk.Label(self, textvariable=self.kpi_vars["average_order_value"], font=("Helvetica", 14, "bold")).pack(pady=5, anchor="w")

        # Frame for top categories
        self.top_categories_frame = ttk.Frame(self, padding="10")
        self.top_categories_frame.pack(pady=10, fill="x", expand=True)
        ttk.Label(self.top_categories_frame, text="Top 5 Categories by Revenue", font=("Helvetica", 12, "bold")).pack(anchor="w")


    def update_kpis(self, kpi_data: Kpi):
        """
        Updates the KPI display with new data.
        """
        self.kpi_vars["total_revenue"].set(f"Total Revenue: ${kpi_data.total_revenue:,.2f}")
        self.kpi_vars["total_units_sold"].set(f"Total Units Sold: {kpi_data.total_units_sold:,}")
        self.kpi_vars["average_order_value"].set(f"Avg. Order Value: ${kpi_data.average_order_value:,.2f}")

        # Clear previous category list
        for widget in self.top_categories_frame.winfo_children():
            if isinstance(widget, ttk.Label) and "Top 5" not in widget.cget("text"):
                 widget.destroy()
        
        # Display new top categories
        for category_info in kpi_data.top_categories:
            cat_name, cat_rev = category_info
            label_text = f"{cat_name}: ${cat_rev:,.2f}"
            ttk.Label(self.top_categories_frame, text=label_text).pack(anchor="w")
