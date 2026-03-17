from flask import Flask, render_template
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "rootpassword"),
    "database": os.getenv("DB_NAME", "products_db")
}

def get_products():
    connection = None
    cursor = None
    products = []
    error_message = None

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, name, description FROM products")
        products = cursor.fetchall()
    except Error as e:
        error_message = f"Database error: {e}"
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return products, error_message

@app.route("/")
def index():
    products, error_message = get_products()
    return render_template("index.html", products=products, error_message=error_message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)