import sqlite3
import os

# Create folder for DB if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

def get_connection():
    return sqlite3.connect('data/stocks.db')

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT, 
            content TEXT UNIQUE,
            score REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized.")

def save_to_db(symbol, content, score):
    """
    Look closely at the line below. 
    The names inside the (parentheses) must match the variables in the execute line.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # We are passing the values into the SQL query here.
        # Everything inside the tuple (symbol, content, score) must be defined.
        cursor.execute('''
            INSERT OR IGNORE INTO tweets (symbol, content, score) 
            VALUES (?, ?, ?)
        ''', (symbol, content, score)) 
        
        conn.commit()
    except Exception as e:
        print(f"Error saving to DB: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()