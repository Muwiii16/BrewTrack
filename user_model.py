"""
Data Access Layer (DAL) for the `users` table.
Handles all database operations related to user accounts.
"""

import bcrypt
from db_connection import DatabaseConnection

class UserModel:

    @staticmethod
    def authenticate(username, password):
        """
        Validates credentials. Returns the user dictionary (without the password) 
        if valid and Active, else returns None.
        """
        conn = DatabaseConnection.get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            # Match exactly the columns from your schema
            query = "SELECT * FROM users WHERE username = %s AND status = 'Active'"
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            # Verify password using bcrypt
            # Note: your schema named the column 'password', not 'password_hash'
            if user and bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
                # Remove the password from the returned dictionary for security
                user.pop('password', None)
                return user
                
            return None
        except Exception as e:
            print(f"Authentication error: {e}")
            return None
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            DatabaseConnection.close_connection(conn)

    @staticmethod
    def create_user(full_name, email, username, raw_password, role, contact_number=None):
        """
        Hashes the password and inserts a new user into the database.
        Returns True if successful, False otherwise.
        """
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        conn = DatabaseConnection.get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO users (full_name, email, username, password, role, contact_number, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'Active')
            """
            values = (full_name, email, username, hashed_password, role, contact_number)
            cursor.execute(query, values)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            DatabaseConnection.close_connection(conn)

    @staticmethod
    def get_all():
        """
        Retrieves all users for the management table.
        """
        conn = DatabaseConnection.get_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            # Select specific fields for the UI, omitting the password
            query = "SELECT user_id, full_name, email, username, role, contact_number, status FROM users"
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            DatabaseConnection.close_connection(conn)

    @staticmethod
    def set_status(user_id, status):
        """
        Updates a user's status (e.g., 'Active' or 'Inactive').
        """
        conn = DatabaseConnection.get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            query = "UPDATE users SET status = %s WHERE user_id = %s"
            cursor.execute(query, (status, user_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating status: {e}")
            return False
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            DatabaseConnection.close_connection(conn)

    @staticmethod
    def update_role(user_id, role):
        """
        Updates a user's role.
        """
        conn = DatabaseConnection.get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            query = "UPDATE users SET role = %s WHERE user_id = %s"
            cursor.execute(query, (role, user_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating role: {e}")
            return False
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            DatabaseConnection.close_connection(conn)