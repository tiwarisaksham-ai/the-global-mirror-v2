import feedparser
import hashlib
import threading
import time
from bs4 import BeautifulSoup

# List of categorized RSS feeds
RSS_FEEDS = [
    "https://www.indiatoday.in/rss/home",                # India Today
    "https://www.aajtak.in/rssfeed/career-news.xml",     # Aaj Tak Career
    "https://www.aajtak.in/rssfeed/education-news.xml",  # Aaj Tak Education
    "https://www.indiatvnews.com/rssfeed/sports.xml",    # India TV Sports
    "https://www.bbc.com/news/10628494",                 # BBC World
    "https://rss.ndtv.com/rss/technology.xml",           # NDTV Tech
    "https://rss.cnn.com/rss/edition.rss",               # CNN International
    "https://www.moneycontrol.com/rss/latestnews.xml",   # MoneyControl
    "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",  # TOI India
    "https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml", # Hindustan Times
    "https://www.business-standard.com/rss/home_page_top_stories.rss", # Business Standard
    "https://economictimes.indiatimes.com/rssfeedsdefault.cms" # Economic Times
]

# Global storage
news_data = []
existing_ids = set()

# Generate unique ID for each article
def generate_id(title, link):
    return hashlib.sha256((title + link).encode()).hexdigest()

# News fetching function with image fix
def fetch_news():
    global news_data
    print(f"🔄 Fetching news at {time.strftime('%H:%M:%S')}")

    new_articles = []

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.get('title', '')
            link = entry.get('link', '')
            summary = entry.get('summary', '')
            published = entry.get('published', 'No Date')

            # ✅ Updated image extraction
            image = ""
            if "media_content" in entry:
                image = entry.media_content[0].get("url", "")
            elif "media_thumbnail" in entry:
                image = entry.media_thumbnail[0].get("url", "")
            elif "enclosures" in entry and entry.enclosures:
                image = entry.enclosures[0].get("href", "")
            elif "summary" in entry:
                soup = BeautifulSoup(entry.summary, 'html.parser')
                img_tag = soup.find('img')
                if img_tag and img_tag.get('src'):
                    image = img_tag.get('src')

            article_id = generate_id(title, link)

            if article_id not in existing_ids:
                existing_ids.add(article_id)
                new_articles.append({
                    "title": title,
                    "link": link,
                    "summary": summary,
                    "published": published,
                    "image": image
                })

    if new_articles:
        news_data = (new_articles + news_data)[:100]
        print(f"✅ {len(new_articles)} new articles added.")
    else:
        print("⚠️ No new articles found.")

# Background thread for auto-fetching
def background_fetch():
    while True:
        fetch_news()
        time.sleep(60)  # Fetch every 60 seconds

# Start the background fetcher thread
def start_background_fetch():
    thread = threading.Thread(target=background_fetch)
    thread.daemon = True
    thread.start()

# Return current news data
def get_all_news():
    return news_data
