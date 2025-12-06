# services/analytics.py
from typing import List, Dict, Any
from models import Kpi

def calculate_kpis(
    total_revenue: float, 
    total_units: int, 
    top_categories_data: List[Dict[str, Any]]
) -> Kpi:
    """
    Calculates KPI values from raw data.
    """
    if total_units > 0:
        avg_order_value = total_revenue / total_units
    else:
        avg_order_value = 0.0

    return Kpi(
        total_revenue=total_revenue,
        total_units_sold=total_units,
        average_order_value=avg_order_value,
        top_categories=top_categories_data
    )
