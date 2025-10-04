import requests
import json
import os

CACHE_FILE = "news_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

def fetch_headlines(stock_name, api_key, max_articles=5):
    cache = load_cache()
    if stock_name in cache:
        return cache[stock_name]

    url = f"https://newsapi.org/v2/everything?q={stock_name}&language=en&sortBy=publishedAt&pageSize={max_articles}&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        headlines = [article["title"] for article in articles]
        cache[stock_name] = headlines
        save_cache(cache)
        return headlines
    else:
        return [f"Error fetching news: {response.status_code}"]