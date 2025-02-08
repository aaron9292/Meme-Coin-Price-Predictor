from pytrends.request import TrendReq
import pandas as pd
import os
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

def fetch_google_trends_data(keyword, timeframe="now 7-d", geo=""):
    pytrends = TrendReq(hl="en-US", tz=360)
    pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo, gprop="")

    data = pytrends.interest_over_time()

    if not data.empty:
        data = data.drop(columns=["isPartial"])
    return data

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    coin = "Dogecoin"
    timeframe = "now 7-d"

    print(f"Fetching Google Trends data for '{coin}'...")

    try:
        df = fetch_google_trends_data(coin, timeframe=timeframe)
        
        if not df.empty:
            file_name = f"data/{coin}_google_trends.csv"
            df.to_csv(file_name, index=True)
            print(f"Saved Google Trends data to {file_name}")
        else:
            print(f"No data found for '{coin}'.")
    except Exception as e:
        print(f"Error fetching Google Trends data: {e}")