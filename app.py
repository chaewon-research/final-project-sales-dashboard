# app.py
import tkinter as tk
from tkinter import messagebox
import db
import models
import repository
from services import analytics, export
from ui.main_window import MainWindow

def main():
    """
    Main function to initialize and run the application.
    """
    # 1. Find and connect to the database
    db_path = db.find_db_file()
    conn = None
    
    if db_path:
        try:
            conn = db.get_connection(db_path)
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not connect to {db_path}.\n{e}")
            return
    else:
        # If no DB is found, create a new one.
        db_path = "sales_db.sqlite"
        try:
            conn = db.get_connection(db_path)
            db.ensure_schema_and_seed(conn)
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not create and seed a new database.\n{e}")
            return

    # 2. Introspect the schema
    schema = db.introspect_schema(conn)
    if not schema:
        # Fallback to create/seed if DB was empty or tables were unsuitable
        db.ensure_schema_and_seed(conn)
        schema = db.introspect_schema(conn)
        if not schema:
            messagebox.showerror("Schema Error", "Could not find or create a valid database schema.")
            conn.close()
            return

    # 3. Create and run the application window
    app = MainWindow(conn, schema)
    app.protocol("WM_DELETE_WINDOW", lambda: on_closing(conn, app))
    app.mainloop()

def on_closing(conn, app):
    """
    Handle the window closing event to ensure the database connection is closed.
    """
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        conn.close()
        app.destroy()

if __name__ == "__main__":
    main()
