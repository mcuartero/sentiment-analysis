
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
client = MongoClient("mongodb://admin:pass@localhost:27017/")
db = client['sentiment_db']
collection = db['reddit_raw']

# Push something
collection.insert_one({
    "ticker": "TSLA",
    "author": "elonmusk",
    "article": "Tesla's stock soars after earnings beat",
})

