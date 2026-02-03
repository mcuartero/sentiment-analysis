# pip install yfinance
import yfinance as yf

from database_connector import collection_yfinance

t = yf.Ticker("TSLA")
news = t.get_news(count=5, tab="news")

#print(len(news))
#print(news[0].keys())
#print(news)
print(news[0])
print(news[0]["content"].keys())


# Iterates through all news items and creates a list of news item dictionaries
docs = []
for item in news:
    content = item.get("content", {})
    provider = content.get("provider", {})
    canonical_url = content.get("canonicalUrl", {})
    click_url = content.get("clickThroughUrl", {})
    thumbnail = content.get("thumbnail", {})

    docs.append({
        "ticker": "TSLA",
        "news_id": content.get("id"),
        "content_type": content.get("contentType"),
        "title": content.get("title"),
        "summary": content.get("summary"),
        "pub_date": content.get("pubDate"),
        "display_time": content.get("displayTime"),
        "provider": provider.get("displayName"),
        "canonical_url": canonical_url.get("url"),
        "click_url": click_url.get("url"),
        "thumbnail_url": thumbnail.get("originalUrl"),
    })

# If there are news items fetched, insert them into the collection
if docs:
    collection_yfinance.insert_many(docs)
