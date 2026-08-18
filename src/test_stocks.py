import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

stocks = [
    "RELIANCE.BSE",
    "TCS.BSE",
    "INFY.BSE"
]

url = "https://www.alphavantage.co/query"

for symbol in stocks:

    print(f"\nChecking {symbol}...")

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": API_KEY
    }

    response = requests.get(url, params=params)

    data = response.json()

    if "Time Series (Daily)" in data:
        print(f"✅ {symbol} works")

    elif "Note" in data:
        print(f"⚠️ API LIMIT for {symbol}")
        print(data["Note"])

    elif "Information" in data:
        print(f"⚠️ API INFORMATION for {symbol}")
        print(data["Information"])

    elif "Error Message" in data:
        print(f"❌ INVALID SYMBOL: {symbol}")
        print(data["Error Message"])

    else:
        print(f"❌ UNKNOWN ERROR for {symbol}")
        print(data)

    # Wait before next request
    time.sleep(15)