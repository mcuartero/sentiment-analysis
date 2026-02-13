import os

# Load the environment variables
from dotenv import load_dotenv
load_dotenv()

# pip install pymongo
from pymongo import MongoClient

# Link to Docker
username = os.environ["MONGO_INITDB_ROOT_USERNAME"]
password = os.environ["MONGO_INITDB_ROOT_PASSWORD"]
CLIENT = MongoClient(f"mongodb://{username}:{password}@localhost:27017/?authSource=admin")
DB = CLIENT['sentiment_db']
collection_reddit = DB['reddit_raw']
collection_yfinance = DB['yahoo_raw']

collection_finnhub = DB['finnhub_raw']

""" ---> To Push an individual item
collection.insert_one({
    "ticker": "TSLA",
    "author": "elonmusk",
    "article": "Tesla's stock soars after earnings beat",
})
"""

def get_collection(name: str):
    return DB[name]
