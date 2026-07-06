from mysql.connector import Error, pooling
import config

class DatabaseConnection:
    @classmethod
    def __init__(self):
        try:
            self.connection_pool = pooling.MySQLConnectionPool(
                pool_name="my_pool",
                pool_size=5,
                pool_reset_session=True,
                host=config.DB_HOST,
                database=config.DB_NAME,
                user=config.DB_USER,
                password=config.DB_PASSWORD
            )
        except Error as e:
            print(f"Error while creating connection pool: {e}")
            self.connection_pool = None

    @classmethod
    def get_connection(self):
        try:
            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None

    def close_connection(self, connection):
        if connection.is_connected():
            connection.close()