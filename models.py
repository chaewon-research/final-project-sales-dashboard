# models.py
from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Any

@dataclass
class Sale:
    """
    Represents a single sales record.
    This is a placeholder and will be adapted based on the discovered schema.
    """
    id: int
    sale_date: str
    product_category: str
    region: str
    units_sold: int
    total_revenue: float

@dataclass
class Kpi:
    """
    Represents the key performance indicators.
    """
    total_revenue: float = 0.0
    total_units_sold: int = 0
    average_order_value: float = 0.0
    top_categories: List[Dict[str, Any]] = field(default_factory=list)
