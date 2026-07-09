"""
Aggregate queries for the Reports page. Nothing here duplicates a query
that already exists elsewhere (e.g. low-stock count still lives in
models.inventory) - this file is just the report-specific rollups.
"""

from models.db_utils import run_query


def get_inventory_value_total():
    row = run_query(
        """SELECT COALESCE(SUM(i.current_quantity * s.cost_per_unit), 0) AS total
           FROM inventory i JOIN ingredients_supplies s ON i.item_id = s.item_id""",
        fetchone=True,
    )
    return float(row["total"])


def get_inventory_value_by_category():
    """Powers the 'Inventory Value' bar chart - current on-hand value grouped by category."""
    return run_query(
        """SELECT COALESCE(s.category, 'Uncategorized') AS category,
           SUM(i.current_quantity * s.cost_per_unit) AS value
           FROM inventory i JOIN ingredients_supplies s ON i.item_id = s.item_id
           GROUP BY category ORDER BY value DESC""",
        fetch=True,
    )


def get_total_sales_revenue():
    row = run_query(
        """SELECT COALESCE(SUM(d.line_total), 0) AS total FROM sales_stock_out_details d
           JOIN sales_stock_out s ON d.sales_id = s.sales_id
           WHERE s.transaction_type='Daily Sales'""",
        fetchone=True,
    )
    return float(row["total"])


def get_revenue_by_day(days=7):
    """Powers the 'Revenue and Sales Performance' chart - daily revenue + units sold."""
    return run_query(
        """SELECT DATE(s.sales_date) AS day,
           COALESCE(SUM(d.line_total), 0) AS revenue,
           COALESCE(SUM(d.quantity_sold), 0) AS units
           FROM sales_stock_out s JOIN sales_stock_out_details d ON d.sales_id = s.sales_id
           WHERE s.transaction_type='Daily Sales' AND s.sales_date >= (CURDATE() - INTERVAL %s DAY)
           GROUP BY DATE(s.sales_date) ORDER BY day""",
        (days,),
        fetch=True,
    )


def get_receiving_accuracy():
    """% of received quantities that matched what was ordered (100% if nothing received yet)."""
    row = run_query(
        """SELECT AVG(
               CASE WHEN received_quantity = 0 THEN 1
                    ELSE 1 - (ABS(discrepancy_quantity) / received_quantity) END
           ) AS accuracy
           FROM receiving_details""",
        fetchone=True,
    )
    accuracy = row["accuracy"]
    return round(float(accuracy) * 100, 1) if accuracy is not None else 100.0