#news_filter.py
import requests
from config import NEWS_API_KEY

def check_for_news():
    url = f"https://news.api.org/v2/top-headlines?category=business&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    news = response.json()
    
    headlines = [article["title"] for article in news["articles"][:5]]
    keywords = ["interest rate", "CPI", "inflation", "Fed", "hike", "non-farm", "employment"]
    
    for title in headlines:
        if any(keyword.lower() in title.lower() for keyword in keywords):
            return True, headlines
    return False, headlines



