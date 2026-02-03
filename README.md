# Stock Sentiment Analysis

We're using **Docker** to run a MongoDB instance to store raw files from scraping. This makes sure that data is saved even if the computer restarts and is isolated from your system files.

---

## Dependencies
1. Docker
2. yfinance
3. python-dotenv 

## 1. Set Up (Docker)

1. Install Docker Desktop
2. I will add the '.env' file into the discord server. Make sure you have it in your root directory.
3. Run this in the termina:
```bash
docker-compose up -d
```

It'll probably take awhile to set everything up.

---

## 2. Manually Messing Up the Data
To manage data manually via the terminal, you have to enter the **MongoDBShell**.

### **Logging into the shell:**
```bash
docker exec -it sentiment_analysis_mongodb mongosh -u [username] -p [password]
```

### **Commands**
```bash
use sentiment_analysis_db # Switch Database
db.reddit_raw.find() # Lists all documents saved in 'reddit_raw' collection.
db.reddit_raw.drop() # Deletes all data within 'reddit_raw' folder.
db.yahoo_raw.find() # Lists all documents saved in 'yahoo_raw' 
db.yahoo_raw.drop() # Deletes all data within the 'yahoo_raw' folder.
db.dropDatabase() # Nuke everything. Deletes entire database.
```