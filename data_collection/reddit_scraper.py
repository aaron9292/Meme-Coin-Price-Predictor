import praw
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
USER_AGENT = "MemecoinSentimentScraper"

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD,
    user_agent=USER_AGENT
)

def scrape_reddit(subreddit_name, query, num_posts=100):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []

    for post in subreddit.hot(limit=num_posts):
        posts.append([
            post.created_utc,
            post.title,
            post.selftext,
            post.score,
            post.num_comments,
            post.url
        ])

    df = pd.DataFrame(posts, columns=["timestamp", "title", "text", "score", "num_comments", "url"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

    return df

if __name__ == "__main__":
    coin = "Dogecoin"
    subreddits = ["CryptoCurrency", "cryptomarkets", "dogecoin"]

    os.makedirs("data", exist_ok=True)

    for sub in subreddits:
        print(f"Scraping posts from r/{sub} for '{coin}'...")
        df = scrape_reddit(sub, coin, num_posts=100)

        if not df.empty:
            file_name = f"data/{coin}_{sub}_reddit_posts.csv"
            df.to_csv(file_name, index=False)
            print(f"Saved {coin} posts from r/{sub} to {file_name}")
        else:
            print(f"No posts found for {coin} in r/{sub}")