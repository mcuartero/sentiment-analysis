import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from database import save_to_db

BASE_DIR = Path(__file__).parent
AUTH_DIR = (BASE_DIR / "data" / ".auth").resolve()

async def scrape_stock(symbol):

    async with async_playwright() as p:
        # 1. Open the broswer using saved login sessionjo.
        # Setting headless=False for debugging purposes
        context = await p.chromium.launch_persistent_context(
            user_data_dir=str(AUTH_DIR),
            headless=False,
            viewport={"width": 1280, "height": 800}
        )

        page = await context.new_page()

        # 2. Go to the Latest search result for the stock symbol
        search_url = f"https://www.x.com/search?q=%24{symbol}&src=typed_query&f=live"
        print(f"Searching for ${symbol}...")

        await page.goto(search_url)

        # 3. Wait for the tweets to load
        # Wait for the 'article' tag which represents a single tweet
        try: 
            await page.wait_for_selector('article[data-testid="tweet"]', timeout=10000)
        except Exception:
            print(f"No tweets found for {symbol} or page took too long to load.")
            await context.close()
            return
        
        # 4. Extract tweet content
        # Use a locator to find all tweet containers
        tweet_locator = page.locator('article[data-testid="tweet"]')
        tweet_count = await tweet_locator.count()

        print(f"Found {tweet_count} tweets on page. Saving...")

        for i in range(tweet_count):
            try:
                # Find the text inside each specific tweet
                text_element = tweet_locator.nth(i).locator('div[data-testid="tweetText"]')
                content = await text_element.inner_text()

                # Send to database.py
                save_to_db(symbol, content)
            except Exception as e:
                continue
        
        # 5. Cleanup
        await context.close()
        print(f"Finished scraping ${symbol}.")
    
if __name__ == "__main__":
    # Test with one symbol
    asyncio.run(scrape_stock("NVDA"))


