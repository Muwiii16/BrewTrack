from mysql.connector import Error, pooling
import config

class DatabaseConnection:
    # Class-level variable to store the pool
    _connection_pool = None

    @classmethod
    def initialize_pool(cls):
        """Creates the connection pool if it doesn't already exist."""
        if cls._connection_pool is None:
            try:
                cls._connection_pool = pooling.MySQLConnectionPool(
                    pool_name="supply_pool",
                    pool_size=5,
                    pool_reset_session=True,
                    host=config.DB_HOST,
                    database=config.DB_NAME,
                    user=config.DB_USER,
                    password=config.DB_PASSWORD
                )
                print("Database connection pool initialized.")
            except Error as e:
                print(f"Error while creating connection pool: {e}")
                cls._connection_pool = None

    @classmethod
    def get_connection(cls):
        """Fetches a connection from the pool."""
        # Ensure the pool exists before trying to get a connection
        if cls._connection_pool is None:
            cls.initialize_pool()
            
        try:
            if cls._connection_pool:
                connection = cls._connection_pool.get_connection()
                if connection.is_connected():
                    return connection
        except Error as e:
            print(f"Error while getting connection from pool: {e}")
            
        return None

    @classmethod
    def close_connection(cls, connection):
        """Returns the connection back to the pool."""
        if connection and connection.is_connected():
            # For pooled connections, .close() doesn't sever the connection to the DB; 
            # it returns it to the pool for reuse.
            connection.close()