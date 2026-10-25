import sqlite3

DATABASE = "sales_dashboard.db"


def create_connection():
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    return conn


conn = create_connection()
cursor = conn.cursor()


def create_tables():

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        full_name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        username TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL
    )
    """)

    # Prediction History
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prediction_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        prediction REAL,

        input_values TEXT,

        prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()


create_tables()