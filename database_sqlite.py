"Database layer - next time use SQLAlchemy"
import sqlite3
#import config

class Product:
    def __init__(self, id, designation, price, quantity, category):
        self.id = id
        self.designation = designation
        self.price = price
        self.quantity = quantity
        self.category = category

def get_database_connection():
    connection = sqlite3.connect("catalogue.db")
    connection.row_factory =  lambda cursor, row: Product(*row)
    return connection

def create_table_products():
    "Create an products table to the database"
    conn = get_database_connection()
    cursor = conn.cursor()
    query = """ CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                designation NVARCHAR(80) NOT NULL,
                price NUMERIC NOT NULL,
                quantity NUMERIC NOT NULL,
                category NVARCHAR(200) NOT NULL,
                created_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_datetime DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def list_products():
    "Select all the products from the database"
    conn = get_database_connection()
    cursor = conn.cursor()
    query = """ SELECT id, designation, price, quantity, category
                FROM products
                ORDER BY designation asc"""
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def load_product(product_id):
    "Select one the product from the database"
    conn = get_database_connection()
    cursor = conn.cursor()
    query = """ SELECT id, designation, price, quantity, category
                FROM products
                WHERE id = ?;"""
    cursor.execute(query, (product_id))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def add_product(designation, price, quantity, category):
    "Add an product to the database"
    conn = get_database_connection()
    cursor = conn.cursor()
    query = """INSERT INTO products (designation, price, quantity, category)
                VALUES (?,?,?,?);"""
    cursor.execute(query, (str(designation), float(price), float(quantity), str(category)))
    conn.commit()
    cursor.close()
    conn.close()

def update_product(product_id, designation, price, quantity, category):
    "Update an product to the database"
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("""
            UPDATE products SET
            designation=?, price=?, quantity=?, category=?
            WHERE id = ?;
         """, (str(designation), float(price), float(quantity), str(category), int(product_id)))

    conn.commit()
    cursor.close()
    conn.close()

def delete_product(product_id):
    "Delete an product."
    conn = get_database_connection()
    cursor = conn.cursor()
    query = """ DELETE FROM products
                WHERE id = ?;"""
    cursor.execute(query, (product_id))
    conn.commit()
    cursor.close()
    conn.close()
