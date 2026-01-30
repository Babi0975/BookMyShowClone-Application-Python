import sqlite3

DB_NAME = "bookmyshow.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        genre TEXT NOT NULL,
        theater TEXT NOT NULL,
        show_time TEXT NOT NULL,
        price REAL NOT NULL,
        total_seats INTEGER NOT NULL,
        available_seats INTEGER NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id TEXT,
        movie_id TEXT,
        seats INTEGER,
        total_amount REAL,
        FOREIGN KEY(customer_id) REFERENCES customers(id),
        FOREIGN KEY(movie_id) REFERENCES movies(id)
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized")
