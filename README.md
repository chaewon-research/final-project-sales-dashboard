# Sales Analysis Dashboard

This is a modular Python desktop application for analyzing sales data from a SQLite database. The application automatically detects and introspects a SQLite database file in the project folder, and provides a GUI for filtering, visualizing, and analyzing the data.

## Features

- **Auto-detection of SQLite database:** The application automatically searches for `*.sqlite` or `*.db` files in the project directory.
- **Schema Introspection:** The application reads the database schema to identify tables and columns for analysis.
- **Fallback Schema:** If no suitable database or tables are found, a default `sales` table is created and seeded with sample data.
- **Dynamic Filtering:** Filter sales data by date range, category, and region.
- **Interactive Charts:** View sales data visualized as "Sales over time" and "Sales by category" charts using Matplotlib.
- **KPI Dashboard:** Key Performance Indicators such as Total Revenue, Total Units Sold, and Average Order Value are displayed.
- **Data Export:** Export the filtered sales data to a CSV file.
- **Theming:** Toggle between light and dark themes for the application.

## Schema Assumptions

The application makes the following assumptions about the column names in the database. If the column names are different, the application will try to find the best match, but might not work as expected.

- **Date Column:** `sale_date`
- **Category Column:** `product_category`
- **Region Column:** `region`
- **Units Sold Column:** `units_sold`
- **Revenue Column:** `total_revenue`

## How to Run

1.  **Install dependencies:**
    ```bash
    pip install pandas matplotlib
    ```

2.  **Run the application:**
    ```bash
    python app.py
    ```

### Light Theme
![Light Theme Screenshot](placeholder_light.png)

### Dark Theme
![Dark Theme Screenshot](placeholder_dark.png)