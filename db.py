# db.py
import sqlite3
import logging
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def find_db_file() -> Optional[Path]:
    """
    Find the most likely SQLite database file in the project directory.

    Searches for files with .sqlite, .sqlite3, or .db extensions.
    Prefers 'sales_db.sqlite' if it exists.

    Returns:
        Optional[Path]: The path to the database file, or None if not found.
    """
    project_dir = Path('.')
    preferred_files = ['sales_db.sqlite']
    supported_extensions = ['*.sqlite', '*.sqlite3', '*.db']

    for filename in preferred_files:
        if (project_dir / filename).exists():
            logging.info(f"Found preferred database file: {filename}")
            return project_dir / filename

    for ext in supported_extensions:
        files = list(project_dir.glob(ext))
        if files:
            # Pick the first one found if preferred is not available
            logging.info(f"Found database file by extension {ext}: {files[0]}")
            return files[0]

    logging.warning("No suitable database file found.")
    return None

def get_connection(db_path: Path) -> sqlite3.Connection:
    """
    Get a connection to the SQLite database.

    Args:
        db_path (Path): The path to the database file.

    Returns:
        sqlite3.Connection: A database connection object.
    """
    try:
        conn = sqlite3.connect(db_path, check_same_thread=False)
        # Enable foreign key support
        conn.execute("PRAGMA foreign_keys = ON;")
        logging.info(f"Successfully connected to {db_path}")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database at {db_path}: {e}")
        raise

def introspect_schema(conn: sqlite3.Connection) -> Dict[str, List[Tuple[str, str]]]:
    """
    Introspect the database schema to get tables and their columns.

    Args:
        conn (sqlite3.Connection): The database connection.

    Returns:
        Dict[str, List[Tuple[str, str]]]: A dictionary mapping table names to a list of (column_name, column_type) tuples.
    """
    schema = {}
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if not tables:
            logging.warning("No tables found in the database.")
            return {}

        for table_name_tuple in tables:
            table_name = table_name_tuple[0]
            if table_name.startswith('sqlite_'):
                continue
            cursor.execute(f"PRAGMA table_info('{table_name}');")
            columns = cursor.fetchall()
            # We care about column name (index 1) and type (index 2)
            schema[table_name] = [(col[1], col[2]) for col in columns]
        
        logging.info(f"Introspected schema: {schema}")
        return schema
    except sqlite3.Error as e:
        logging.error(f"Error introspecting schema: {e}")
        return {}

def ensure_schema_and_seed(conn: sqlite3.Connection):
    """
    Ensures that a 'sales' table exists and seeds it with data if it's empty.
    This function is called as a fallback if introspection finds nothing suitable.

    Args:
        conn (sqlite3.Connection): The database connection.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sales'")
    if cursor.fetchone():
        cursor.execute("SELECT COUNT(*) FROM sales")
        if cursor.fetchone()[0] > 0:
            logging.info("'sales' table already exists and is not empty. Skipping creation and seeding.")
            return
        else:
            logging.info("'sales' table is empty. Seeding data.")
    else:
        logging.info("'sales' table not found. Creating and seeding.")
        try:
            cursor.execute("""
                CREATE TABLE sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sale_date DATE NOT NULL,
                    product_category TEXT NOT NULL,
                    region TEXT NOT NULL,
                    units_sold INTEGER NOT NULL,
                    unit_price REAL NOT NULL,
                    total_revenue REAL GENERATED ALWAYS AS (units_sold * unit_price) STORED
                );
            """)
            logging.info("Created 'sales' table.")
        except sqlite3.Error as e:
            logging.error(f"Failed to create 'sales' table: {e}")
            return

    # Seed data
    seed_data = [
        ('2023-01-15', 'Electronics', 'North America', 10, 299.99),
        ('2023-01-20', 'Books', 'Europe', 50, 15.50),
        ('2023-02-10', 'Apparel', 'Asia', 100, 25.00),
        ('2023-02-15', 'Electronics', 'Europe', 5, 1200.00),
        ('2023-03-05', 'Books', 'North America', 20, 22.99),
        ('2023-03-25', 'Home Goods', 'Asia', 30, 45.75),
        ('2024-04-01', 'Apparel', 'North America', 75, 30.00),
        ('2024-04-10', 'Electronics', 'Asia', 15, 89.99),
        ('2024-05-18', 'Home Goods', 'Europe', 25, 120.50),
        ('2024-05-22', 'Books', 'Europe', 40, 12.00),
    ]

    try:
        cursor.executemany("""
            INSERT INTO sales (sale_date, product_category, region, units_sold, unit_price)
            VALUES (?, ?, ?, ?, ?)
        """, seed_data)
        conn.commit()
        logging.info(f"Seeded {len(seed_data)} rows into 'sales' table.")
    except sqlite3.Error as e:
        logging.error(f"Failed to seed data: {e}")
        conn.rollback()

if __name__ == '__main__':
    # Example usage for verification
    db_file = find_db_file()
    if db_file:
        connection = get_connection(db_file)
        schema_info = introspect_schema(connection)
        if not schema_info:
            ensure_schema_and_seed(connection)
            schema_info = introspect_schema(connection)
            logging.info(f"Final schema after creation: {schema_info}")
        connection.close()
    else:
        # Create a new DB if none is found
        logging.info("Creating a new database 'sales_db.sqlite' as none was found.")
        db_file = Path("sales_db.sqlite")
        connection = get_connection(db_file)
        ensure_schema_and_seed(connection)
        schema_info = introspect_schema(connection)
        logging.info(f"Schema of newly created database: {schema_info}")
        connection.close()
