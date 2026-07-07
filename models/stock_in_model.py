"""
Everything related to `receiving` and `receiving_details` - verifying a
delivery against its purchase order and adding it into inventory.
"""

from models.db_utils import run_query
from models import inventory_model
from models import purchase_order_model


def receive_delivery(po_id, user_id, received_items, remarks=""):
    """received_items: list of dicts {item_id, ordered_qty, received_qty}"""
    receiving_id = run_query(
        "INSERT INTO receiving (po_id, user_id, delivery_status, remarks) VALUES (%s,%s,'Received',%s)",
        (po_id, user_id, remarks),
        commit=True,
    )
    for ri in received_items:
        discrepancy = ri["received_qty"] - ri["ordered_qty"]
        run_query(
            """INSERT INTO receiving_details (receiving_id, item_id, received_quantity, discrepancy_quantity)
               VALUES (%s,%s,%s,%s)""",
            (receiving_id, ri["item_id"], ri["received_qty"], discrepancy),
            commit=True,
        )
        inventory_model.stock_in(
            ri["item_id"],
            ri["received_qty"],
            user_id,
            reference_type="Purchase Order",
            reference_id=po_id,
            remarks=f"PO-{po_id} received",
        )
    purchase_order_model.mark_received(po_id)
    return receiving_id