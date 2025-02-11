import pandas as pd
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

BASE_PATH = "data_collection/data/"

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(text)
    return sentiment_score["compound"]

def normalize_google_trends(input_csv, output_csv):
    if not os.path.exists(input_csv):
        print(f"File not found: {input_csv}")
        return

    df = pd.read_csv(input_csv)

    if "Dogecoin" not in df.columns:
        print(f"No search interest column found in {input_csv}")
        return
    
    print(f"Processing Google Trends data for sentiment scaling...")

    df["sentiment_score"] = (df["Dogecoin"] - df["Dogecoin"].min()) / (df["Dogecoin"].max() - df["Dogecoin"].min())
    df["sentiment_score"] = (df["sentiment_score"] * 2) - 1

    df.to_csv(output_csv, index=False)
    print(f"Normalized Google Trends sentiment saved to {output_csv}")

def process_sentiment(input_csv, output_csv):
    if not os.path.exists(input_csv):
        print(f"File not found: {input_csv}")
        return

    df = pd.read_csv(input_csv)

    if "text" not in df.columns:
        print(f"No 'text' column found in {input_csv}")
        return

    print(f"Processing sentiment analysis for {input_csv}...")
    df["sentiment_score"] = df["text"].astype(str).apply(analyze_sentiment)

    df.to_csv(output_csv, index=False)
    print(f"Sentiment scores saved to {output_csv}")

if __name__ == "__main__":
    os.makedirs(BASE_PATH + "sentiment", exist_ok=True)

    text_datasets = [
        BASE_PATH + "Dogecoin_tweets.csv",
        BASE_PATH + "Dogecoin_Cryptocurrency_reddit_posts.csv",
        BASE_PATH + "Dogecoin_cryptomarkets_reddits_posts.csv"
    ]

    for dataset in text_datasets:
        output_file = dataset.replace(".csv", "_sentiment.csv").replace("data/", "data/sentiment/")
        process_sentiment(dataset, output_file)

    google_trends_dataset = BASE_PATH + "Dogecoin_google_trends.csv"
    google_trends_output = BASE_PATH + "sentiment/Dogecoin_google_trends_sentiment.csv"

    normalize_google_trends(google_trends_dataset, google_trends_output)