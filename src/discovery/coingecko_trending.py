import requests

# Toggle this to True if you want only meme-like coins from the below keywords
FILTER_MEMECOINS_ONLY = False

MEME_KEYWORDS = [
    "doge", "shiba", "inu", "pepe", "elon", "meme", "baby", "moon",
    "floki", "woof", "shit", "rug", "bonk", "milady", "turbo", "frog",
    "panda", "fart", "walrus", "sonic", "cat", "rabbit", "rocket"
]

def fetch_trending_coins():
    url = "https://api.coingecko.com/api/v3/search/trending"
    response = requests.get(url)
    response.raise_for_status()
    coins = response.json()["coins"]

    print("\n📈 Trending Coins from CoinGecko:")
    for coin in coins:
        item = coin["item"]
        print(f"- {item['name']} ({item['symbol']})")

    return coins

def is_memecoin(name, symbol):
    text = f"{name.lower()} {symbol.lower()}"
    return any(keyword in text for keyword in MEME_KEYWORDS)

def find_trending_memecoins():
    trending = fetch_trending_coins()
    memecoins = []

    for entry in trending:
        item = entry["item"]
        name = item["name"]
        symbol = item["symbol"]
        coin_id = item["id"]

        if FILTER_MEMECOINS_ONLY:
            if is_memecoin(name, symbol):
                memecoins.append({
                    "id": coin_id,
                    "name": name,
                    "symbol": symbol,
                    "score": item["score"]
                })
                print(f"✅ Included (memecoin): {name} ({symbol})")
            else:
                print(f"⛔ Skipped (not memey): {name} ({symbol})")
        else:
            memecoins.append({
                "id": coin_id,
                "name": name,
                "symbol": symbol,
                "score": item["score"]
            })

    return memecoins
