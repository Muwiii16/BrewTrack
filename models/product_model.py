from models.db_utils import run_query


def add_product(product_name, selling_price, product_status='Active'):
    """
    Inserts a new product into the products_menu table.
    """
    query = """
        INSERT INTO products_menu (product_name, selling_price, product_status)
        VALUES (%s, %s, %s)
    """
    params = (product_name, selling_price, product_status)
    
    # Passing commit=True automatically commits the transaction 
    # and returns cursor.lastrowid, which is exactly what we need.
    return run_query(query, params=params, commit=True)