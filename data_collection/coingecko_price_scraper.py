import requests
import pandas as pd

def get_historical_prices(coin_id, days="30", currency="usd"):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"

    params = {
        "vs_currency": currency,
        "days": days,
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "prices" not in data:
        print("Error fetching data: ", data)
        return None
    
    df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    return df

if __name__ == "__main__":
    coin = "dogecoin" # example dogecoin
    df = get_historical_prices(coin, days="30")

    if df is not None:
        df.to_csv(f"data/{coin}_price_history.csv", index=False)
        print(f"Saved {coin} price data successfully!")
