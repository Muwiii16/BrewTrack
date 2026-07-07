"""
Everything related to the `users` table: login/auth and user management.
"""

from models.db_utils import run_query


def authenticate(username, password):
    """NOTE: plain-text comparison for now - swap for bcrypt.checkpw() later."""
    return run_query(
        "SELECT * FROM users WHERE username=%s AND password=%s AND status='Active'",
        (username, password),
        fetchone=True,
    )


def register_user(full_name, email, username, password, role="Staff", contact_number=None):
    return run_query(
        """INSERT INTO users (full_name, email, username, password, role, contact_number)
           VALUES (%s,%s,%s,%s,%s,%s)""",
        (full_name, email, username, password, role, contact_number),
        commit=True,
    )


def get_users():
    return run_query("SELECT * FROM users ORDER BY user_id", fetch=True)


def get_user_by_id(user_id):
    return run_query("SELECT * FROM users WHERE user_id=%s", (user_id,), fetchone=True)


def add_user(full_name, email, username, password, role, contact_number):
    return run_query(
        """INSERT INTO users (full_name,email,username,password,role,contact_number)
           VALUES (%s,%s,%s,%s,%s,%s)""",
        (full_name, email, username, password, role, contact_number),
        commit=True,
    )


def update_user(user_id, full_name, email, role, contact_number, status):
    run_query(
        """UPDATE users SET full_name=%s, email=%s, role=%s, contact_number=%s, status=%s
           WHERE user_id=%s""",
        (full_name, email, role, contact_number, status, user_id),
        commit=True,
    )


def delete_user(user_id):
    run_query("DELETE FROM users WHERE user_id=%s", (user_id,), commit=True)