# services/export.py
import pandas as pd
from typing import List
from models import Sale
from tkinter import filedialog

def export_to_csv(sales_data: List[Sale]):
    """
    Exports a list of Sale objects to a CSV file.
    """
    if not sales_data:
        print("No data to export.")
        return

    # Convert list of dataclasses to a list of dicts
    data_dicts = [
        {
            "ID": sale.id,
            "Date": sale.sale_date,
            "Category": sale.product_category,
            "Region": sale.region,
            "UnitsSold": sale.units_sold,
            "TotalRevenue": sale.total_revenue,
        }
        for sale in sales_data
    ]
    
    df = pd.DataFrame(data_dicts)

    filepath = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        title="Save Exported Data"
    )

    if filepath:
        try:
            df.to_csv(filepath, index=False)
            print(f"Data successfully exported to {filepath}")
        except Exception as e:
            print(f"Error exporting data: {e}")
