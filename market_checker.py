# market_checker.py

import requests

def get_btc_price():
    url = "https://www.bitstamp.net/api/v2/ticker/btcusd/"
    try:
        response = requests.get(url, timeout=5) # added a timeout
        response.raise_for_status() # raise an exception for http errors
        data = response.json()
        price = float(data['last']) # the last key holds the last traded price
        return price
    except requests.exceptions.RequestException as e:
        print(f"Error fetching BTC price from Bitstamp: {e}")
        return None 
    
def generate_trade_signal(price):
    """Generate a trade signal based on the BTC price"""

    if price is None:
       return "Price not available to generate signal." 
    elif price < 90000:
       return "Price is low!"
    elif price > 90000:
       return "Price is high!"
  
    else: 
       return "HOLD: Price is stable"       
    