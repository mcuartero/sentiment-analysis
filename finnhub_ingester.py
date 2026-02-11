import os
import re 
import requests
import html
from dotenv import load_dotenv
from datetime import date, timedelta, timezone, datetime
import time

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

if not FINNHUB_API_KEY:
    raise RuntimeError("Missing FINNHUB_API_KEY in environment file")

base_url = "https://finnhub.io/api/v1"

headers = {"X-Finnhub-Token": FINNHUB_API_KEY}

def clean_text(text: str) -> str:
    """Removes HTML entities and fixes encoding artifacts."""
    
    if not text:
        return ""
    
    # 1. Handle HTML escape entities 
    text = html.unescape(text)

    # 2. Fix the specific "Double Escape" apostrophe problem
    # This handles both the literal \' and the raw double-escaped versions
    text = text.replace("\\'", "'").replace("\\\"", '"')

    # 3. Sometimes finnhub adds \ when there is an apostrophe
    # We use a raw string r"\'" to catch the actual character sequence
    text = text.replace(r"\'", "'").replace(r'\"', '"')

    # 4. Remove any remaining non-printable/non-ASCII characters
    text = re.sub(r'[^\x20-\x7E]', ' ', text)

    # 5. Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def fetch_company_news(symbol: str, company_name:str, days_back: int = 365, step_days: int = 3):
    """
    Fetches financial news for a ticker of a listed company, 
    up to a specified number of days in the past. Queries until days_back is reached
    for a given step_days
    """
    # Calculate today's date and the date for a specified number of days
    end = date.today()
    start = end - timedelta(days=days_back)

    # Stores the news items 
    all_items = []
    seen = set()
    cur = start

    # Prepare lower-case versions for better matching
    l_name = company_name.lower()

    # Iterates through the dates, and for each unique news item, adds it to a list
    while cur <= end:

        # Finds the furthest date depending on end date and step_days
        chunk_to = min(cur + timedelta(days=step_days), end)

        # Make an API request to finnhub to get financial news 
        resp = requests.get(
            "https://finnhub.io/api/v1/company-news",
            params={"symbol": symbol, "from": cur.isoformat(), "to": chunk_to.isoformat()},
            headers=headers,
            timeout=30,
        )
        resp.raise_for_status()
        items = resp.json()

        # iterate through the news items in the API request 
        for it in items:
            # Check for whether the news item is unique or not
            key = it.get("id")
            if key and key not in seen:
                 # --- CLEANING STEP ---
                h_raw = it.get("headline", "")
                s_raw = it.get("summary", "")
                
                # Sometimes these can have artifacts
                it["headline"] = clean_text(h_raw)
                it["summary"] = clean_text(s_raw)
                
                # Create lower-case versions for the logic check
                h_clean = it["headline"].lower()
                s_clean = it["summary"].lower()

                # --- RELEVANCE CHECK ---
                # Check if EITHER (Company Name in BOTH) OR (Ticker in BOTH)
                name_match = (l_name in h_clean and l_name in s_clean)
                symbol_match = (symbol in it["headline"] and symbol in it["summary"])
                duo_match = (
                            (l_name in h_clean and symbol in it["summary"]) or 
                            (symbol in it["headline"] and l_name in s_clean)
                )

                # Add to the list if the ticker or company bname is in headline AND summary
                if name_match or symbol_match or duo_match:
                    seen.add(key)
                    all_items.append(it)

        cur = chunk_to + timedelta(days=1)

        # be gentle with rate limits
        time.sleep(0.25)

    if not all_items:
        print(f"No news found for {symbol}")
        return []

    # Print the dates of the newest and oldest items
    dts = [datetime.fromtimestamp(x["datetime"], tz=timezone.utc) for x in all_items]
    print(f"[{symbol}] oldest: {min(dts)} newest: {max(dts)}")
    return all_items

news = fetch_company_news("NVDA", "Nvidia", days_back=90, step_days=3)
print("NVDA total unique:", len(news))
print(news[0])
# ----> Returns 1212 unique headlines (in both headline and summary)

news_tsla = fetch_company_news("TSLA", "Tesla", days_back=90,step_days=3)
print("TSLA total unique:", len(news_tsla))
print(news_tsla[0])
# ----> Returns 1220 unique headlines (in both headline and summary)

# check for a niche ticker
news_cifr = fetch_company_news("CIFR", "Cipher Mining", days_back=90, step_days=3)
print("CIFR total unique:", len(news_cifr))
print(news_cifr[0])
# ----> Returns 37 unique headlines (in both headline and summary)
