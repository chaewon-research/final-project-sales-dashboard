# repository.py
import sqlite3
from typing import List, Dict, Any, Optional, Tuple

from models import Sale

def get_distinct_values(conn: sqlite3.Connection, column_name: str, table_name: str) -> List[str]:
    """
    Gets distinct values from a specified column.
    """
    try:
        cursor = conn.cursor()
        query = f"SELECT DISTINCT {column_name} FROM {table_name} ORDER BY {column_name};"
        cursor.execute(query)
        return [row[0] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Database error in get_distinct_values: {e}")
        return []

def get_sales_data(
    conn: sqlite3.Connection,
    date_col: str,
    category_col: str,
    region_col: str,
    units_col: str,
    revenue_col: str,
    table_name: str,
    filters: Optional[Dict[str, Any]] = None
) -> List[Sale]:
    """
    Retrieves sales data based on filters.
    """
    sales = []
    try:
        cursor = conn.cursor()
        
        query = f"""
            SELECT ROWID, {date_col}, {category_col}, {region_col}, {units_col}, {revenue_col}
            FROM {table_name}
        """
        
        conditions = []
        params = []

        if filters:
            if "start_date" in filters and filters["start_date"]:
                conditions.append(f"{date_col} >= ?")
                params.append(filters["start_date"])
            if "end_date" in filters and filters["end_date"]:
                conditions.append(f"{date_col} <= ?")
                params.append(filters["end_date"])
            if "category" in filters and filters["category"] != "All":
                conditions.append(f"{category_col} = ?")
                params.append(filters["category"])
            if "region" in filters and filters["region"] != "All":
                conditions.append(f"{region_col} = ?")
                params.append(filters["region"])

        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        query += f" ORDER BY {date_col};"

        cursor.execute(query, params)
        
        for row in cursor.fetchall():
            sales.append(Sale(*row))
            
    except sqlite3.Error as e:
        print(f"Database error in get_sales_data: {e}")

    return sales

def get_kpi_data(
    conn: sqlite3.Connection,
    revenue_col: str,
    units_col: str,
    category_col: str,
    table_name: str,
    filters: Optional[Dict[str, Any]] = None
) -> Tuple[float, int, List[Tuple[str, float]]]:
    """
    Calculates KPI data based on filters.
    Returns total revenue, total units, and top categories.
    """
    base_query = f"FROM {table_name}"
    conditions = []
    params = []

    if filters:
        date_col = filters.get("date_col", "sale_date")
        if "start_date" in filters and filters["start_date"]:
            conditions.append(f"{date_col} >= ?")
            params.append(filters["start_date"])
        if "end_date" in filters and filters["end_date"]:
            conditions.append(f"{date_col} <= ?")
            params.append(filters["end_date"])
        if "category" in filters and filters["category"] != "All":
            category_col_name = filters.get("category_col", "product_category")
            conditions.append(f"{category_col_name} = ?")
            params.append(filters["category"])
        if "region" in filters and filters["region"] != "All":
            region_col_name = filters.get("region_col", "region")
            conditions.append(f"{region_col_name} = ?")
            params.append(filters["region"])

    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    try:
        cursor = conn.cursor()
        
        # Total Revenue and Units
        kpi_query = f"SELECT SUM({revenue_col}), COUNT(*) {base_query};"
        cursor.execute(kpi_query, params)
        total_revenue, total_units = cursor.fetchone()
        total_revenue = total_revenue or 0.0
        total_units = total_units or 0

        # Top Categories by Revenue
        category_query = f"""
            SELECT {category_col}, SUM({revenue_col}) as total_rev
            {base_query}
            GROUP BY {category_col}
            ORDER BY total_rev DESC
            LIMIT 5;
        """
        cursor.execute(category_query, params)
        top_categories = cursor.fetchall()
        
        return total_revenue, total_units, top_categories

    except sqlite3.Error as e:
        print(f"Database error getting KPIs: {e}")
        return 0.0, 0, []
