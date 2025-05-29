# market_checker.py

import requests

def get_btc_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    response = requests.get(url)
    data = response.json()
    return float(data["price"])

def generate_trade_signal(price):
    if price < 115000:
        return f"BTC/USD Signal\nAction: BUY\nPrice: {price:.2f}\nTP: {price + 500}\nSL: {price - 300}"
    else:
        return f"BTC/USD Signal\nAction: SELL\nPrice: {price:.2f}\nTP: {price - 500}\nSL: {price + 300}"
    
    