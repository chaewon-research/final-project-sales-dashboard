# ui/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

from ui.filters_view import FiltersView
from ui.kpi_view import KpiView
from ui.charts_view import ChartsView
from ui.theme import set_theme, THEME_LIGHT, THEME_DARK
from services.export import export_to_csv
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from repository import get_sales_data, get_kpi_data, get_distinct_values
from services.analytics import calculate_kpis

class MainWindow(tk.Tk):
    def __init__(self, conn: sqlite3.Connection, schema: dict):
        super().__init__()
        self.conn = conn
        self.schema = schema
        self.current_theme = THEME_LIGHT

        # --- Schema Analysis ---
        # A real app would have a more robust way to map columns
        self.table_name = list(self.schema.keys())[0] if self.schema else 'sales'
        column_map = {col[0].lower(): col[0] for col in self.schema.get(self.table_name, [])}
        
        self.date_col = column_map.get('sale_date', 'sale_date')
        self.category_col = column_map.get('product_category', 'product_category')
        self.region_col = column_map.get('region', 'region')
        self.units_col = column_map.get('units_sold', 'units_sold')
        self.revenue_col = column_map.get('total_revenue', 'total_revenue')
        
        self.title("Sales Analysis Dashboard")
        self.geometry("1200x800")
        set_theme(self, self.current_theme)

        # --- Menu Bar ---
        self.create_menu()

        # --- Main Layout ---
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # --- Filters ---
        categories = get_distinct_values(self.conn, self.category_col, self.table_name)
        regions = get_distinct_values(self.conn, self.region_col, self.table_name)
        self.filters_view = FiltersView(main_frame, self.refresh_data, categories, regions)
        self.filters_view.pack(fill="x")

        # --- Content Area (Tabs) ---
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True, pady=10, padx=10)

        self.kpi_view = KpiView(notebook)
        self.charts_view = ChartsView(notebook)
        
        # Data table tab
        data_frame = ttk.Frame(notebook)
        self.tree = self.create_data_table(data_frame)

        notebook.add(self.kpi_view, text="KPI Dashboard")
        notebook.add(self.charts_view, text="Charts")
        notebook.add(data_frame, text="Raw Data")

        self.refresh_data()

    def create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        # File Menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Export to CSV", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # View Menu
        view_menu = tk.Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        menu_bar.add_cascade(label="View", menu=view_menu)

    def create_data_table(self, parent) -> ttk.Treeview:
        cols = ["ID", "Date", "Category", "Region", "Units", "Revenue"]
        tree = ttk.Treeview(parent, columns=cols, show='headings')
        
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100)
            
        # Scrollbars
        vsb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        tree.pack(fill='both', expand=True)
        
        return tree

    def refresh_data(self):
        filters = self.filters_view.get_filters()
        
        # Add column names to filters dict for repository
        filters["date_col"] = self.date_col
        filters["category_col"] = self.category_col
        filters["region_col"] = self.region_col

        # --- Fetch Data ---
        self.sales_data = get_sales_data(
            self.conn, self.date_col, self.category_col, self.region_col, 
            self.units_col, self.revenue_col, self.table_name, filters
        )
        
        total_revenue, total_units, top_cats_data = get_kpi_data(
            self.conn, self.revenue_col, self.units_col, self.category_col, self.table_name, filters
        )

        # --- Calculate KPIs ---
        kpi_results = calculate_kpis(total_revenue, total_units, top_cats_data)
        
        # --- Update UI ---
        self.kpi_view.update_kpis(kpi_results)
        self.charts_view.update_charts(self.sales_data, self.date_col, self.category_col, self.revenue_col)
        self.update_data_table()
        
    def update_data_table(self):
        self.tree.delete(*self.tree.get_children())
        for sale in self.sales_data:
            self.tree.insert("", "end", values=(
                sale.id, sale.sale_date, sale.product_category, sale.region, sale.units_sold, f"{sale.total_revenue:.2f}"
            ))

    def export_data(self):
        if self.sales_data:
            export_to_csv(self.sales_data)
        else:
            messagebox.showinfo("Export Info", "No data available to export.")

    def toggle_theme(self):
        if self.current_theme == THEME_LIGHT:
            self.current_theme = THEME_DARK
        else:
            self.current_theme = THEME_LIGHT
        set_theme(self, self.current_theme)
