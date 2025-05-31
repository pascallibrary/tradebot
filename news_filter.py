# news_filter.py
import requests
import logging
from config import NEWS_API_KEY # Ensure NEWS_API_KEY is defined in config.py

# --- Configure Logging for this module ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) # Set to INFO for general use, DEBUG for more verbosity
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# Avoid adding multiple handlers if this script is run multiple times (e.g., in tests)
if not logger.handlers:
    logger.addHandler(ch)
# --- End Logging Configuration ---

def check_for_news():
    """
    Fetches top business headlines from NewsAPI.org and checks for specific keywords.

    Returns:
        tuple: (bool, list[str])
            - True if a relevant keyword is found in any of the top 5 headlines.
            - False otherwise.
            - A list of the actual top 5 headlines (or fewer if not enough articles/error).
    """
    # NewsAPI.org endpoint for top headlines.
    # Base URL: https://newsapi.org/v2/
    url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&apiKey={NEWS_API_KEY}"

    # Keywords for financial/economic news relevant to crypto markets
    keywords = [
        "interest rate", "cpi", "inflation", "fed", "hike", "non-farm payrolls",
        "employment", "recession", "economy", "central bank", "quantitative easing",
        "bond yields", "stock market", "bear market", "bull market", "liquidity",
        "market crash", "stimulus", "tapering", "geopolitical" # Added more comprehensive keywords
    ]

    headlines_list = [] # Initialize list to store headlines

    try:
        logger.info(f"Attempting to fetch news from NewsAPI.org for business headlines...")
        # Note: It's good practice to log the URL, but be careful not to expose API_KEY in public logs.
        # url_to_log = url.split('apiKey=')[0] + "apiKey=***" # safer for logging
        # logger.info(f"Fetching from: {url_to_log}")

        response = requests.get(url, timeout=10) # Added a timeout
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        news_data = response.json()

        # NewsAPI.org has a specific 'status' field for API-level errors
        if news_data.get("status") == "error":
            error_code = news_data.get("code")
            error_message = news_data.get("message")
            logger.error(f"NewsAPI.org API Error: Code={error_code}, Message='{error_message}'")
            # Common NewsAPI errors: apiKeyMissing, apiKeyInvalid, rateLimited, etc.
            return False, [] # Return empty list on API error

        articles = news_data.get("articles", [])
        if not articles:
            logger.info("No articles found in the NewsAPI.org response.")
            return False, [] # No articles returned

        # Get top 5 headlines
        for article in articles[:5]:
            title = article.get("title")
            if title: # Ensure title exists
                headlines_list.append(title)

        # Check for keywords in fetched headlines
        has_relevant_news = False
        for title in headlines_list:
            if any(keyword.lower() in title.lower() for keyword in keywords):
                logger.info(f"Found relevant news keyword in headline: '{title}'")
                has_relevant_news = True
                break # Found at least one, no need to check further

        if not has_relevant_news:
            logger.info("No specific relevant keywords found in top headlines.")

        return has_relevant_news, headlines_list # Return bool and the list of headlines

    except requests.exceptions.Timeout:
        logger.error("NewsAPI.org request timed out.")
        return False, []
    except requests.exceptions.RequestException as e:
        logger.error(f"Network or API error when fetching news: {e}", exc_info=True)
        return False, []
    except Exception as e:
        logger.error(f"An unexpected error occurred in check_for_news: {e}", exc_info=True)
        return False, []

# Example usage (for testing this file directly)
if __name__ == "__main__":
    # For testing, ensure NEWS_API_KEY is defined in config.py or temporarily here
    # from config import NEWS_API_KEY # Uncomment if running standalone tests

    # If you run this file directly for testing, make sure to have a valid NEWS_API_KEY
    # in config.py, or you can temporarily set it here for testing:
    # NEWS_API_KEY = "YOUR_NEWS_API_KEY_HERE" # REMOVE THIS LINE IN PRODUCTION

    has_relevant_news, top_headlines = check_for_news()

    print("\n--- News Filter Check ---")
    if top_headlines:
        print("Top 5 Headlines:")
        for i, headline in enumerate(top_headlines):
            print(f"{i+1}. {headline}")
    else:
        print("No headlines fetched or an error occurred.")

    if has_relevant_news:
        print("\nSTATUS: Market-impacting news keywords detected!")
    else:
        print("\nSTATUS: No specific market-impacting news keywords found in top headlines.")