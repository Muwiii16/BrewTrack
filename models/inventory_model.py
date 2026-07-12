"""
Everything related to the `inventory` table (current on-hand quantities)
and the stock-in / stock-out operations that change them.

Every quantity change here also calls models.movement.log_movement() so the
audit trail (inventory_movements) always stays in sync with actual stock.
"""

from models.db_utils import run_query
from models import stock_movement_model


def get_inventory_overview():
    return run_query(
        """SELECT s.item_id, s.item_name, s.category, sup.supplier_id, sup.supplier_name, i.current_quantity,
           s.unit_of_measurement, s.reorder_level, s.cost_per_unit,
           (i.current_quantity * s.cost_per_unit) AS value,
           (SELECT COUNT(DISTINCT po.po_id) 
            FROM purchase_order_details pod 
            JOIN purchase_orders po ON po.po_id = pod.po_id 
            WHERE pod.item_id = s.item_id AND po.po_status = 'Pending') AS pending_po_count
           FROM inventory i
           JOIN ingredients_supplies s ON i.item_id = s.item_id
           LEFT JOIN suppliers sup ON s.supplier_id = sup.supplier_id
           ORDER BY s.item_name""",
        fetch=True,
    )


def get_low_stock_items(limit=None):
    q = """SELECT s.item_id, s.item_name, i.current_quantity, s.reorder_level, s.unit_of_measurement,
           sup.supplier_name, s.cost_per_unit
           FROM inventory i JOIN ingredients_supplies s ON i.item_id = s.item_id
           LEFT JOIN suppliers sup ON s.supplier_id = sup.supplier_id
           WHERE i.current_quantity <= s.reorder_level
           ORDER BY (i.current_quantity / s.reorder_level) ASC"""
    if limit:
        q += f" LIMIT {int(limit)}"
    return run_query(q, fetch=True)


def get_low_stock_count():
    row = run_query(
        """SELECT COUNT(*) AS c FROM inventory i
           JOIN ingredients_supplies s ON i.item_id = s.item_id
           WHERE i.current_quantity <= s.reorder_level""",
        fetchone=True,
    )
    return row["c"]


def get_current_quantity(item_id):
    row = run_query("SELECT current_quantity FROM inventory WHERE item_id=%s", (item_id,), fetchone=True)
    return row["current_quantity"]


def stock_in(item_id, qty, user_id, reference_type=None, reference_id=None, remarks=""):
    run_query(
        "UPDATE inventory SET current_quantity = current_quantity + %s WHERE item_id=%s",
        (qty, item_id),
        commit=True,
    )
    resulting_stock = get_current_quantity(item_id)
    stock_movement_model.log_movement(item_id, user_id, "Stock-In", qty, resulting_stock,
                           reference_type, reference_id, remarks)


def manual_stock_in(item_id, qty, user_id, source_ref):
    stock_in(item_id, qty, user_id, reference_type="Manual", reference_id=None, remarks=source_ref)


def stock_out(item_id, qty, user_id, reference_type=None, reference_id=None, remarks=""):
    run_query(
        "UPDATE inventory SET current_quantity = current_quantity - %s WHERE item_id=%s",
        (qty, item_id),
        commit=True,
    )
    resulting_stock = get_current_quantity(item_id)
    stock_movement_model.log_movement(item_id, user_id, "Stock-Out", qty, resulting_stock,
                           reference_type, reference_id, remarks)