"""
Everything related to the `suppliers` table.
"""

from models.db_utils import run_query


def get_suppliers():
    return run_query("SELECT * FROM suppliers ORDER BY supplier_name", fetch=True)


def get_supplier_by_id(supplier_id):
    return run_query("SELECT * FROM suppliers WHERE supplier_id=%s", (supplier_id,), fetchone=True)


def add_supplier(name, contact_person, contact_number, address, email):
    return run_query(
        """INSERT INTO suppliers (supplier_name, contact_person, contact_number, address, email)
           VALUES (%s,%s,%s,%s,%s)""",
        (name, contact_person, contact_number, address, email),
        commit=True,
    )


def update_supplier(supplier_id, name, contact_person, contact_number, address, email, status):
    run_query(
        """UPDATE suppliers SET supplier_name=%s, contact_person=%s, contact_number=%s,
           address=%s, email=%s, supplier_status=%s WHERE supplier_id=%s""",
        (name, contact_person, contact_number, address, email, status, supplier_id),
        commit=True,
    )


def delete_supplier(supplier_id):
    run_query("DELETE FROM suppliers WHERE supplier_id=%s", (supplier_id,), commit=True)