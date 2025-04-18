import requests
import datetime
import pandas as pd
import streamlit as st

@st.cache_data(ttl=3600)
def get_coin_market_chart(coin_id, days=7, interval="daily"):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": interval
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching price for {coin_id}: {e}")
        return []
    
    prices = data.get("prices", [])
    result = []

    for timestamp, price in prices:
        date = datetime.datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
        result.append({"date": date, "price": price})

    return result

import requests
import pandas as pd

def get_coin_price_history(coin_id, days=7):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days
    }

    try:
        headers = {"User-Agent": "Mozilla/5.0"}  # optional, to avoid 429s
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        if "prices" not in data:
            print(f"⚠️ No 'prices' key found in API response for {coin_id}")
            return pd.DataFrame()

        prices = data["prices"]
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df

    except Exception as e:
        print(f"Error fetching price history for {coin_id}: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()
