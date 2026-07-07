"""
Shared query helper for every model file.

This is the ONLY place that talks to DatabaseConnection directly. Every
file in models/ (user.py, supplier.py, movement.py, purchase_order.py, ...)
imports run_query() from here instead of touching the connection pool itself.
That keeps the pooling/cursor logic in one spot - if it ever needs to change
(different pool library, retry logic, logging, etc.) you only edit this file.
"""

from database.db_connection import DatabaseConnection


def run_query(query, params=None, fetch=False, fetchone=False, commit=False):
    conn = DatabaseConnection.get_connection()
    if conn is None:
        raise Exception(
            "Could not obtain a database connection. "
            "Check config.py and that MySQL is running."
        )
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        result = None
        if fetchone:
            result = cursor.fetchone()
        elif fetch:
            result = cursor.fetchall()
        if commit:
            conn.commit()
            result = cursor.lastrowid
        return result
    finally:
        cursor.close()
        DatabaseConnection.close_connection(conn)