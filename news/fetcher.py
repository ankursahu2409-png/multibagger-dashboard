import requests

def fetch_headlines(stock_name, api_key, max_articles=5):
    url = f"https://newsapi.org/v2/everything?q={stock_name}&language=en&sortBy=publishedAt&pageSize={max_articles}&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return [article["title"] for article in articles]
    else:
        return [f"Error fetching news: {response.status_code}"]