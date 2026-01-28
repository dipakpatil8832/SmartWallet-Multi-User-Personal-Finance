import sqlite3

DB_NAME = "wallet.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        type TEXT,
        note TEXT,
        amount REAL,
        balance REAL
    )
    """)

    conn.commit()
    conn.close()
