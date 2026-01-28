from database import init_db, save_to_db
import sqlite3
from pathlib import Path

# Define the path again to check if the file actually exists
DB_PATH = Path(__file__).parent / "data" / "stocks.db"

def run_test():
    print("--- Starting Database Test ---")

    # 1. Initialise the database
    init_db()

    # 2. Try to save sample stock data
    print("Inserting test data...")
    save_to_db("TSLA", "New Tesla model announced.")
    save_to_db("AAPL", "Apple announces new division.")

    # 3. Verify the data 
    if DB_PATH.exists():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tweets")
        results = cursor.fetchall()

        print(f"\nSuccess! Found {len(results)} rows in {DB_PATH.name}:")
        for row in results:
            print(f" -> [{row[1]}] {row[2][:50]}... (Saved at: {row[3]})")
        
        conn.close()
    else:
        print("Error: Database file was not find in data folder.")

if __name__ == "__main__":
    run_test()