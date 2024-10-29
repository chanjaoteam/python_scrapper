# import mysql.connector
# from mysql.connector import Error
# from config import DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME

# class DatabaseManager:
#     def __init__(self):
#         self.connection = None

#     def create_connection(self):
#         """Create a database connection."""
#         try:
#             self.connection = mysql.connector.connect(
#                 host=DATABASE_HOST,
#                 user=DATABASE_USER,
#                 password=DATABASE_PASSWORD,
#                 database=DATABASE_NAME,
#                 port=3306
#             )
#             if self.connection.is_connected():
#                 print("Connection to the database was successful.")
#         except Error as e:
#             print(f"Error: '{e}'")

#     def create_tables(self):
#         """Create necessary tables in the database."""
#         create_table_query = """
#         CREATE TABLE IF NOT EXISTS products_in_list (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             html_content TEXT NOT NULL,
#             image_urls TEXT NOT NULL
#         );
#         """
#         cursor = self.connection.cursor()
#         cursor.execute(create_table_query)
#         self.connection.commit()
#         cursor.close()

#     def check_existing_record(self, product_id):
#         """Check if a product record already exists."""
#         cursor = self.connection.cursor()
#         cursor.execute("SELECT COUNT(*) FROM products_in_list WHERE id = %s", (product_id,))
#         count = cursor.fetchone()[0]
#         cursor.close()
#         return count > 0

#     def insert_product(self, html_content, product_link, name=None, price=None, sold_count=None, category=None, description=None, product_detail_id=None):
#         """Insert a new product record into the database."""
#         insert_query = """
#         INSERT INTO products_in_list (html_content, product_link, name, price, sold_count, category, description, product_detail_id)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
#         """
#         try:
#             cursor = self.connection.cursor()
#             cursor.execute(insert_query, (html_content, product_link, name, price, sold_count, category, description, product_detail_id))
#             self.connection.commit()
#             print("Product inserted successfully.")
#         except Error as e:
#             print(f"Error: '{e}'")
#         finally:
#             cursor.close()


import mysql.connector
from mysql.connector import Error
from config import DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME

class DatabaseManager:
    """Class to manage database connections and operations for MySQL."""

    def __init__(self):
        """Initialize the DatabaseManager with connection parameters."""
        self.connection = None

    def connect(self):
        """Establish a connection to the MySQL database."""
        try:
            self.connection = mysql.connector.connect(
                host=DATABASE_HOST,
                user=DATABASE_USER,
                password=DATABASE_PASSWORD,
                database=DATABASE_NAME,
                port=3306
            )
            if self.connection.is_connected():
                print("Successfully connected to the database.")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.connection = None

    def close(self):
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")

    def insert_record(self, table, data, unique_column=''):
        """
        Insert a record into the specified table if it does not already exist.
        
        Parameters:
        - table (str): The name of the table to insert data into.
        - data (dict): A dictionary containing the column names and values to insert.
        - unique_column (str): The name of the column that should be unique to avoid duplicates.
        """
        if not self.connection or not self.connection.is_connected():
            self.connect()

        # Check if the record already exists
        value_to_check = data.get(unique_column)
        if unique_column != "" :
            if self.record_exists(table, unique_column, value_to_check):
                print(f"Record with {unique_column} = {value_to_check} already exists. Skipping insert.")
                return  # Skip the insertion if the record exists

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, list(data.values()))
            self.connection.commit()
            print("Record inserted successfully.")
        except Error as e:
            print(f"Error inserting record: {e}")
        finally:
            cursor.close()

    def record_exists(self, table, unique_column, value):
        """
        Check if a record exists in the specified table to avoid duplicates.
        
        Parameters:
        - table (str): The name of the table to check.
        - unique_column (str): The name of the column that should be unique.
        - value: The value to check for existence in the unique column.
        
        Returns:
        - bool: True if the record exists, False otherwise.
        """
        if not self.connection or not self.connection.is_connected():
            self.connect()

        query = f"SELECT COUNT(*) FROM {table} WHERE {unique_column} = %s"
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (value,))
            count = cursor.fetchone()[0]
            return count > 0
        except Error as e:
            print(f"Error checking for existing record: {e}")
            return False
        finally:
            cursor.close()

# Example usage
if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.connect()
    
    # Check if a record exists
    exists = db_manager.record_exists('your_table', 'unique_column_name', 'value_to_check')
    print(f"Record exists: {exists}")
    
    # Insert a record
    if not exists:
        db_manager.insert_record('your_table', {
            'column1': 'value1',
            'column2': 'value2',
            # Add more columns as needed
        })

    db_manager.close()
