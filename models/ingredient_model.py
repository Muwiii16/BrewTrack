"""
Everything related to the `ingredients_supplies` table (the master list of
raw materials). Inventory *levels* live in inventory.py - this file is just
the catalog: name, category, unit, cost, reorder level, supplier.
"""

from models.db_utils import run_query


def get_ingredients():
    return run_query(
        """SELECT s.*, sup.supplier_name FROM ingredients_supplies s
           LEFT JOIN suppliers sup ON s.supplier_id = sup.supplier_id
           ORDER BY s.item_name""",
        fetch=True,
    )


def get_ingredient_by_id(item_id):
    return run_query(
        """SELECT s.*, sup.supplier_name FROM ingredients_supplies s
           LEFT JOIN suppliers sup ON s.supplier_id = sup.supplier_id
           WHERE s.item_id=%s""",
        (item_id,),
        fetchone=True,
    )


def get_total_ingredients():
    row = run_query("SELECT COUNT(*) AS c FROM ingredients_supplies", fetchone=True)
    return row["c"]


def add_ingredient(supplier_id, item_name, category, uom, cost, reorder_level):
    item_id = run_query(
        """INSERT INTO ingredients_supplies
           (supplier_id,item_name,category,unit_of_measurement,cost_per_unit,reorder_level)
           VALUES (%s,%s,%s,%s,%s,%s)""",
        (supplier_id, item_name, category, uom, cost, reorder_level),
        commit=True,
    )
    # every ingredient needs a matching inventory row to start at 0 on hand
    run_query("INSERT INTO inventory (item_id, current_quantity) VALUES (%s, 0)", (item_id,), commit=True)
    return item_id


def delete_ingredient(item_id):
    run_query("DELETE FROM ingredients_supplies WHERE item_id=%s", (item_id,), commit=True)