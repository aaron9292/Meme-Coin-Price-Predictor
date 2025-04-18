import praw
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

def search_reddit_posts(coin_name, subreddits=None, limit_per_sub=25):
    if subreddits is None:
        subreddits = ["CryptoCurrency", "cryptomarkets", coin_name.lower()]

    posts = []

    for sub in subreddits:
        try:
            subreddit = reddit.subreddit(sub)
            for post in subreddit.search(coin_name, sort="new", limit=limit_per_sub):
                posts.append({
                    "subreddit": sub,
                    "title": post.title,
                    "text": post.selftext,
                    "score": post.score,
                    "num_comments": post.num_comments,
                    "url": post.url
                })
        except Exception as e:
            print(f"Error scraping r/{sub}: {e}")

    return posts
