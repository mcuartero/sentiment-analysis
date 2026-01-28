import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "stocks.db"

# NOTE: To clear or reset the entire database, just delete the 'data/stocks.db' file.

def init_db():

    # Make sure folder exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            content TEXT UNIQUE,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Database initialised at {DB_PATH}")

def save_to_db(symbol, content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT OR IGNORE INTO tweets (symbol, content)
            VALUES (?, ?)
        ''', (symbol, content))
        conn.commit()
    except Exception as e:
        print(f"Error saving to DB: {e}")
    finally:
        conn.close()
    
if __name__ == "__main__":
    init_db()