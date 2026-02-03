import os

# Load the environment variables
from dotenv import load_dotenv
load_dotenv()

# pip install pymongo
from pymongo import MongoClient
'''
Heyyyy BUSSSSSSSS this is the skeleton for pre much adding stuff to the database.
Youre pre much gonna dump everything you scraped onto here and then ill set up a 
Postgre to sort everything properly. Change the collection into whatever you want
but split it up to wherever you were scraping from. Loveee you twin <3. You
getting it tn... 🫦
'''

# Link to Docker
username = os.environ["MONGO_INITDB_ROOT_USERNAME"]
password = os.environ["MONGO_INITDB_ROOT_PASSWORD"]
CLIENT = MongoClient(f"mongodb://{username}:{password}@localhost:27017/?authSource=admin")
DB = CLIENT['sentiment_db']
collection = DB['reddit_raw']
collection_yfinance = DB['yahoo_raw']

""" ---> To Push an individual item
collection.insert_one({
    "ticker": "TSLA",
    "author": "elonmusk",
    "article": "Tesla's stock soars after earnings beat",
})
"""

def get_collection(name: str):
    return DB[name]
