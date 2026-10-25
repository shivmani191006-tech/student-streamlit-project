import sqlite3

DB_NAME = "sales_dashboard.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    return conn


conn = get_connection()
cursor = conn.cursor()


def create_tables():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prediction_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        prediction REAL,
        input_values TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()


def add_prediction(username, prediction, inputs):
    cursor.execute("""
    INSERT INTO prediction_history(username,prediction,input_values)
    VALUES(?,?,?)
    """, (username, prediction, inputs))
    conn.commit()


def get_predictions(username):
    cursor.execute("""
    SELECT * FROM prediction_history
    WHERE username=?
    ORDER BY created_at DESC
    """, (username,))
    return cursor.fetchall()


create_tables()