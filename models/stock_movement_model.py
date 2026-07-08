"""
Everything related to the `inventory_movements` table (the audit trail).

log_movement() is called by inventory.py, purchase_order.py/receiving.py, and
sales.py whenever a quantity changes, so every stock change is logged the
same way in one place.
"""

from models.db_utils import run_query


def log_movement(item_id, user_id, movement_type, quantity, resulting_stock,
                 reference_type=None, reference_id=None, remarks=""):
    run_query(
        """INSERT INTO inventory_movements
           (item_id,user_id,movement_type,quantity,resulting_stock,reference_type,reference_id,remarks)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
        (item_id, user_id, movement_type, quantity,
         resulting_stock, reference_type, reference_id, remarks),
        commit=True,
    )


def get_recent_stock_in(limit=5):
    return run_query(
        """SELECT m.*, s.item_name, s.unit_of_measurement, u.full_name, u.role FROM inventory_movements m
           JOIN ingredients_supplies s ON m.item_id = s.item_id
           JOIN users u ON m.user_id = u.user_id
           WHERE m.movement_type='Stock-In'
           ORDER BY m.movement_date DESC LIMIT %s""",
        (limit,),
        fetch=True,
    )


def get_recent_stock_in(limit=5):
    return run_query(
        """SELECT m.*, s.item_name, u.full_name FROM inventory_movements m
           JOIN ingredients_supplies s ON m.item_id = s.item_id
           JOIN users u ON m.user_id = u.user_id
           WHERE m.movement_type='Stock-In'
           ORDER BY m.movement_date DESC LIMIT %s""",
        (limit,),
        fetch=True,
    )


def get_recent_stock_out(limit=5):
    return run_query(
        """SELECT m.*, s.item_name, u.full_name FROM inventory_movements m
           JOIN ingredients_supplies s ON m.item_id = s.item_id
           JOIN users u ON m.user_id = u.user_id
           WHERE m.movement_type='Stock-Out'
           ORDER BY m.movement_date DESC LIMIT %s""",
        (limit,),
        fetch=True,
    )


def get_movement_history(search=None):
    q = """SELECT m.*, s.item_name, u.full_name FROM inventory_movements m
           JOIN ingredients_supplies s ON m.item_id = s.item_id
           JOIN users u ON m.user_id = u.user_id"""
    params = ()
    if search:
        q += " WHERE s.item_name LIKE %s"
        params = (f"%{search}%",)
    q += " ORDER BY m.movement_date DESC"
    return run_query(q, params, fetch=True)
