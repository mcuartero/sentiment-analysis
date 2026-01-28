from database import init_db, save_to_db, get_connection

init_db() 

# Using 'symbol' as the first argument
print("Saving test data with symbol $NVDA...")
save_to_db("$NVDA", "Nvidia is leading the AI race!", 0.85)

conn = get_connection()
cursor = conn.cursor()

# Check if the data is there
cursor.execute("SELECT * FROM tweets")
row = cursor.fetchone()
conn.close()

if row:
    print(f"✅ Success! Found data: {row}")
else:
    print("❌ Fail: Database is still empty.")