# src/sentiment/google_scraper.py

import requests
from bs4 import BeautifulSoup
import time
import random

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
     "Accept-Language": "en-US,en;q=0.9",
     "Referer": "https://www.google.com/"
}

def search_google(coin_name, num_results=10):
    query = f"{coin_name} crypto"
    url = f"https://www.google.com/search?q={query}&num={num_results}"
    
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Google request failed: {e}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for result in soup.select("div.g"):
        title = result.select_one("h3")
        snippet = result.select_one(".VwiC3b") or result.select_one(".IsZvec")

        if title and snippet:
            results.append({
                "title": title.get_text(strip=True),
                "snippet": snippet.get_text(strip=True)
            })

    time.sleep(random.uniform(2.0, 4.0))

    return results