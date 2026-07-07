"""
Everything related to `products_menu`, `product_ingredients`,
`sales_stock_out`, and `sales_stock_out_details` - ringing up a sale and
auto-deducting the ingredients it consumes.
"""

from models.db_utils import run_query
from models import  inventory_model


def get_products():
    return run_query(
        "SELECT * FROM products_menu WHERE product_status='Active' ORDER BY product_name", fetch=True
    )


def get_product_ingredients(product_id):
    return run_query(
        """SELECT pi.*, s.item_name FROM product_ingredients pi
           JOIN ingredients_supplies s ON pi.item_id = s.item_id WHERE pi.product_id=%s""",
        (product_id,),
        fetch=True,
    )


def record_sale(product_id, quantity_sold, selling_price, user_id):
    sales_id = run_query(
        "INSERT INTO sales_stock_out (user_id, transaction_type, remarks) VALUES (%s,'Daily Sales','')",
        (user_id,),
        commit=True,
    )
    line_total = quantity_sold * selling_price
    run_query(
        """INSERT INTO sales_stock_out_details
           (sales_id, product_id, quantity_sold, selling_price, line_total)
           VALUES (%s,%s,%s,%s,%s)""",
        (sales_id, product_id, quantity_sold, selling_price, line_total),
        commit=True,
    )
    # deduct the ingredients this product consumes
    for ing in get_product_ingredients(product_id):
        used_qty = float(ing["quantity_required"]) * quantity_sold
        inventory_model.stock_out(
            ing["item_id"], used_qty, user_id,
            reference_type="Sales", reference_id=sales_id, remarks="Sale deduction",
        )
    return sales_id


def get_recent_sales(limit=5):
    return run_query(
        """SELECT s.sales_date, d.quantity_sold, d.line_total, p.product_name, u.full_name
           FROM sales_stock_out_details d
           JOIN sales_stock_out s ON d.sales_id = s.sales_id
           JOIN products_menu p ON d.product_id = p.product_id
           JOIN users u ON s.user_id = u.user_id
           WHERE s.transaction_type='Daily Sales'
           ORDER BY s.sales_date DESC LIMIT %s""",
        (limit,),
        fetch=True,
    )


def get_daily_sales_total():
    row = run_query(
        """SELECT COALESCE(SUM(d.line_total), 0) AS total FROM sales_stock_out_details d
           JOIN sales_stock_out s ON d.sales_id = s.sales_id
           WHERE DATE(s.sales_date) = CURDATE() AND s.transaction_type='Daily Sales'""",
        fetchone=True,
    )
    return float(row["total"])