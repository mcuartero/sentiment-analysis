# pip install yfinance
import yfinance as yf

from database_connector import collection_yfinance
from datetime import datetime, timedelta, timezone
import time

t = yf.Ticker("NVDA")

# Calculates the date 30 days ago in the format of yahoo dates
date_cutoff = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat().replace("+00:00", "Z")

#print(t.get_news(count=500, tab="news")[-1].get("content", {}).get("pubDate"))
#print(len(t.get_news(count=500, tab="news")))

news_all = t.get_news(count=500, tab="all")
print(len(news_all), news_all[-1].get("content", {}).get("pubDate"))

'''
while True:
    news = t.get_news(count=10, tab="news")

    # Iterates through all news items and creates a list of news item dictionaries
    docs = []
    for item in news:
        content = item.get("content", {})
        provider = content.get("provider", {})
        canonical_url = content.get("canonicalUrl", {})
        thumbnail = content.get("thumbnail", {})

        docs.append({
            "ticker": "TSLA",
            "news_id": content.get("id"),
            "content_type": content.get("contentType"),
            "title": content.get("title"),
            "summary": content.get("summary"),
            "pub_date": content.get("pubDate"),
            "provider": provider.get("displayName"),    
            "canonical_url": canonical_url.get("url"),
            "thumbnail_url": thumbnail.get("originalUrl"),
        })
    
    # after building docs
    dates = [doc["pub_date"] for doc in docs if doc.get("pub_date")]
    if not dates:
        break

    oldest_article_date = min(dates)

    # Deduplicate by news_id before insert
    ids = [doc["news_id"] for doc in docs if doc.get("news_id")]
    if ids:
        existing_ids = set(
            collection_yfinance.distinct("news_id", {"news_id": {"$in": ids}})
        )
        docs = [doc for doc in docs if doc.get("news_id") not in existing_ids]

    # If there are news items fetched, insert them into the collection
    if docs:
        collection_yfinance.insert_many(docs)

    # If the oldest article is less than the cutoff, then break out
    if oldest_article_date < date_cutoff:
        break
    
    # Reduces hammering requests 
    time.sleep(60)


    

'''

