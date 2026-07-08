"""
Everything related to the `users` table: login/auth and user management.

Passwords are hashed with bcrypt before they ever touch the database.
Important: because bcrypt salts every hash differently, you CANNOT do
`WHERE password=%s` in SQL anymore - the same password hashes to a
different string every time. So authenticate() now fetches the user by
username only, then compares in Python with bcrypt.checkpw().
"""

import bcrypt
from models.db_utils import run_query


def hash_password(plain_password):
    """Turns a plain-text password into a salted bcrypt hash (as a str, so
    it fits in the existing VARCHAR(255) `password` column)."""
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password, stored_hash):
    """Compares a plain-text password against a stored bcrypt hash.
    Returns False (instead of raising) if stored_hash isn't a valid bcrypt
    hash at all - e.g. a leftover plain-text password from before this
    change. See the migration note in the README about rehashing those."""
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), stored_hash.encode("utf-8"))
    except (ValueError, AttributeError):
        return False


def authenticate(identifier, password):
    """identifier can be a username OR an email - matches whichever the
    login form collects (older login.py uses username, the card-style
    login_view.py uses email)."""
    user = run_query(
        "SELECT * FROM users WHERE (username=%s OR email=%s) AND status='Active'",
        (identifier, identifier),
        fetchone=True,
    )
    if user and verify_password(password, user["password"]):
        return user
    return None


def register_user(full_name, email, username, password, role="Staff", contact_number=None):
    return run_query(
        """INSERT INTO users (full_name, email, username, password, role, contact_number)
           VALUES (%s,%s,%s,%s,%s,%s)""",
        (full_name, email, username, hash_password(password), role, contact_number),
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
        (full_name, email, username, hash_password(password), role, contact_number),
        commit=True,
    )


def update_user(user_id, full_name, email, role, contact_number, status):
    """Does NOT touch the password - use change_password() for that."""
    run_query(
        """UPDATE users SET full_name=%s, email=%s, role=%s, contact_number=%s, status=%s
           WHERE user_id=%s""",
        (full_name, email, role, contact_number, status, user_id),
        commit=True,
    )


def change_password(user_id, new_password):
    run_query(
        "UPDATE users SET password=%s WHERE user_id=%s",
        (hash_password(new_password), user_id),
        commit=True,
    )


def delete_user(user_id):
    run_query("DELETE FROM users WHERE user_id=%s", (user_id,), commit=True)