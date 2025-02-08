import tweepy
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

client = tweepy.Client(bearer_token=BEARER_TOKEN)

def fetch_tweets(query, num_tweets=100):
    tweets = []

    response = client.search_recent_tweets(
        query=query,
        tweet_fields=["created_at", "text", "public_metrics", "author_id"],
        max_results=min(num_tweets, 100)
    )

    if response.data:
        for tweet in response.data:
            tweets.append([
                tweet.created_at,
                tweet.text,
                tweet.author_id,
                tweet.public_metrics["like_count"],
                tweet.public_metrics["retweet_count"]
            ])

    df = pd.DataFrame(tweets, columns=["timestamp", "text", "user_id", "likes", "retweets"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df

if __name__ == "__main__":
    coin = "DogeCoin"
    df = fetch_tweets(coin, num_tweets=100)

    if not df.empty:
        os.makedirs("data", exist_ok=True)
        df.to_csv(f"data/{coin}_tweets.csv", index=False)
        print(f"Saved {coin} tweets successfully")
    else:
        print("No tweets found.")