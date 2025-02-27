import mysql.connector

class DatabaseConnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def activate_connection(self):
        """Establish a connection to the database."""
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()

    def close_connection(self):
        """Close the connection and cursor."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_query(self, query):
        """Execute a query."""
        if self.conn is None or self.cursor is None:
            self.activate_connection()
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def show_tables(self):
        """Show all tables in the database."""
        return self.execute_query("SHOW TABLES;")

# Usage example
db = DatabaseConnection('localhost', 'root', 'Ritam@9966', 'Infoledge')

# Show tables
print(db.show_tables())

# Close the connection after use
db.close_connection()




import mysql.connector
from mysql.connector import pooling

dbconfig = {
    "host": "localhost",
    "user": "root",
    "password": "Ritam@9966",
    "database": "Infoledge"
}

# Create a pool of database connections
pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **dbconfig)

def show_tables():
    conn = pool.get_connection()  # Get a connection from the pool
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    cursor.close()
    conn.close()  # Return the connection to the pool
    return tables

print(show_tables())
