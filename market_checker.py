# market_checker.py

import requests

def get_btc_price():
    """Fetches the current BTC/USD price from Bitstamp."""
    url = "https://www.bitstamp.net/api/v2/ticker/btcusd/"
    try:
        response = requests.get(url, timeout=5) # added a timeout
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        data = response.json()
        price = float(data['last']) # 'last' key holds the last traded price
        return price
    except requests.exceptions.RequestException as e:
        print(f"Error fetching BTC price from Bitstamp: {e}")
        return None # Return None to indicate failure

def generate_trade_signal(price):
    """
    Generates a trade signal and includes the current price,
    along with a more nuanced "volatile" state.
    """
    if price is None:
        return "Current price: N/A. Price not available to generate signal."

    # Define your price thresholds for signals
    # These are example values; adjust them based on your strategy
    low_price_threshold = 90000
    high_price_threshold = 150000
    # Volatility range around the "stable" zone. You'd typically calculate volatility
    # based on recent price changes, but for simplicity, we'll use a range for now.
    volatile_lower = 100000
    volatile_upper = 120000

    signal_message = ""
    status = ""

    if price < low_price_threshold:
        status = "very low"
        signal_message = "BUY: Consider buying, price is very low!"
    elif price > high_price_threshold:
        status = "very high"
        signal_message = "SELL: Consider selling, price is very high!"
    elif volatile_lower < price < volatile_upper:
        status = "volatile"
        signal_message = "WATCH: Price is highly volatile right now."
    else:
        status = "stable"
        signal_message = "HOLD: Price is currently stable."

    # Combine current price with the signal message
    return f"Current price: ${price:,.2f}. Price is {status}. {signal_message}"

