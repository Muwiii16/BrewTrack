"""
Everything related to `purchase_orders` and `purchase_order_details`.
"""

from models.db_utils import run_query


def create_purchase_order(supplier_id, user_id, expected_date, line_items):
    """line_items: list of dicts {item_id, qty, unit_cost}"""
    po_id = run_query(
        """INSERT INTO purchase_orders (supplier_id, user_id, expected_delivery_date, po_status)
           VALUES (%s,%s,%s,'Pending')""",
        (supplier_id, user_id, expected_date),
        commit=True,
    )
    for li in line_items:
        run_query(
            """INSERT INTO purchase_order_details (po_id, item_id, ordered_quantity, unit_cost)
               VALUES (%s,%s,%s,%s)""",
            (po_id, li["item_id"], li["qty"], li["unit_cost"]),
            commit=True,
        )
    return po_id


def get_purchase_orders():
    pos = run_query(
        """SELECT po.*, sup.supplier_name FROM purchase_orders po
           JOIN suppliers sup ON po.supplier_id = sup.supplier_id
           ORDER BY po.po_date DESC""",
        fetch=True,
    )
    for po in pos:
        po["items"] = get_po_details(po["po_id"])
    return pos


def get_recent_purchase_orders(limit=3):
    return run_query(
        """SELECT po.po_id, po.po_status,
           (SELECT COALESCE(SUM(line_total),0) FROM purchase_order_details WHERE po_id=po.po_id) AS total
           FROM purchase_orders po
           ORDER BY po.po_date DESC LIMIT %s""",
        (limit,),
        fetch=True,
    )


def get_pending_orders_count():
    row = run_query("SELECT COUNT(*) AS c FROM purchase_orders WHERE po_status='Pending'", fetchone=True)
    return row["c"]


def get_open_orders_count():
    row = run_query(
        "SELECT COUNT(*) AS c FROM purchase_orders WHERE po_status IN ('Pending','Approved')", fetchone=True
    )
    return row["c"]


def get_po_details(po_id):
    return run_query(
        """SELECT d.*, s.item_name FROM purchase_order_details d
           JOIN ingredients_supplies s ON d.item_id = s.item_id WHERE d.po_id=%s""",
        (po_id,),
        fetch=True,
    )


def get_approved_pos():
    return run_query(
        """SELECT po.*, sup.supplier_name FROM purchase_orders po
           JOIN suppliers sup ON po.supplier_id = sup.supplier_id
           WHERE po_status='Approved'
           ORDER BY po.po_date DESC""",
        fetch=True,
    )


def approve_po(po_id):
    run_query("UPDATE purchase_orders SET po_status='Approved' WHERE po_id=%s", (po_id,), commit=True)


def cancel_po(po_id):
    run_query("UPDATE purchase_orders SET po_status='Cancelled' WHERE po_id=%s", (po_id,), commit=True)


def mark_received(po_id):
    run_query("UPDATE purchase_orders SET po_status='Received' WHERE po_id=%s", (po_id,), commit=True)