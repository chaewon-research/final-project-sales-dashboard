# ui/charts_view.py
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from typing import List
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import Sale

class ChartsView(ttk.Frame):
    """
    A frame to display sales charts.
    """
    def __init__(self, parent):
        super().__init__(parent)
        
        self.figure = Figure(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create two subplots
        self.ax1 = self.figure.add_subplot(211) # Sales over time
        self.ax2 = self.figure.add_subplot(212) # Sales by category

        self.figure.tight_layout(pad=3.0)

    def update_charts(self, sales_data: List[Sale], date_col: str, category_col: str, revenue_col: str):
        """
        Updates the charts with new sales data.
        """
        self.ax1.clear()
        self.ax2.clear()

        if not sales_data:
            self.ax1.set_title("Sales Over Time")
            self.ax1.text(0.5, 0.5, "No data to display", ha='center', va='center')
            self.ax2.set_title("Sales by Category")
            self.ax2.text(0.5, 0.5, "No data to display", ha='center', va='center')
            self.canvas.draw()
            return

        df = pd.DataFrame([s.__dict__ for s in sales_data])
        df[date_col] = pd.to_datetime(df[date_col])

        # Sales over time plot
        time_series = df.set_index(date_col)[revenue_col].resample('M').sum()
        self.ax1.plot(time_series.index, time_series.values, marker='o', linestyle='-')
        self.ax1.set_title("Monthly Sales Over Time")
        self.ax1.set_ylabel("Total Revenue")
        self.ax1.grid(True)

        # Sales by category plot
        category_sales = df.groupby(category_col)[revenue_col].sum().sort_values(ascending=False)
        category_sales.plot(kind='bar', ax=self.ax2)
        self.ax2.set_title("Sales by Category")
        self.ax2.set_ylabel("Total Revenue")
        self.ax2.tick_params(axis='x', rotation=45)
        self.ax2.grid(True, axis='y')

        self.figure.tight_layout(pad=3.0)
        self.canvas.draw()
