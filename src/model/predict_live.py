from src.discovery.coingecko_trending import find_trending_memecoins
from src.sentiment.duckduckgo_scraper import search_duckduckgo
from src.sentiment.reddit_scraper import search_reddit_posts
from src.pipeline.feature_engineering import compute_sentiment_features
import pandas as pd
import joblib
import os

def load_model():
    path = "model/latest_model.joblib"
    if not os.path.exists(path):
        raise FileNotFoundError("Trained model not found...")
    return joblib.load(path)

def predict_for_trending():
    model = load_model()
    coins = find_trending_memecoins()

    features = [
        "avg_sentiment", "num_positive", "num_negative", "num_neutral",
        "reddit_mentions", "google_mentions", "volatility"
    ]

    results = []
    sentiment_rows = []

    for coin in coins:
        print(f"\n🔍 Analyzing {coin['name']} ({coin['symbol']})...")

        try:
            google_results = search_duckduckgo(coin["name"])
            reddit_results = search_reddit_posts(coin["name"], limit_per_sub=5)

            text = [r["title"] for r in reddit_results] + [g["snippet"] for g in google_results]

            if not text:
                print(f"No sentiment text found for {coin['name']}. Skipping...")
                continue

            sentiment = compute_sentiment_features(text)
            if not sentiment or not isinstance(sentiment, dict):
                print(f"⚠️ Sentiment extraction failed for {coin['name']}. Skipping.")
                continue

            row = {
                "id": coin["id"],
                "coin": coin["name"],
                "symbol": coin["symbol"],
                "reddit_mentions": len(reddit_results),
                "google_mentions": len(google_results),
                **sentiment
            }

            if "volatility" not in row:
                row["volatility"] = 0

            missing = [f for f in features if f not in row]
            if missing:
                print(f"Missing features {missing} for {coin['name']}. Skipping...")
                continue

            X = pd.DataFrame([row])[features]
            predicted_pct = model.predict(X)[0]
            row["predicted_change_pct"] = round(predicted_pct, 2)
            row["prediction"] = "BUY" if predicted_pct > 3 else "SKIP"
            results.append(row)

            # Save sentiment sources
            for snippet in reddit_results:
                sentiment_rows.append({
                    "coin": coin["name"],
                    "source": "Reddit",
                    "text": snippet["title"]
                })
            for snippet in google_results:
                sentiment_rows.append({
                    "coin": coin["name"],
                    "source": "DuckDuckGo",
                    "text": snippet["snippet"]
                })

            print(f"🔮 {row['prediction']} ({row['predicted_change_pct']}% forecast)")

        except Exception as e:
            print(f"Error while processing {coin['name']}: {e}")
            continue

    if results:
        df = pd.DataFrame(results)
        os.makedirs("data", exist_ok=True)
        df.to_csv("data/predictions_live.csv", index=False)
        print(f"\n💾 Saved {len(results)} predictions to data/predictions_live.csv")

        sentiment_df = pd.DataFrame(sentiment_rows)
        sentiment_df.to_csv("data/sentiment_sources.csv", index=False)
        print(f"📰 Saved {len(sentiment_df)} sentiment sources to data/sentiment_sources.csv")
    else:
        print("\nNo predictions generated.")

if __name__ == "__main__":
    predict_for_trending()
