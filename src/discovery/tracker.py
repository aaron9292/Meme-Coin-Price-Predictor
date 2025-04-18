import json
from pathlib import Path

TRACK_FILE = Path("data/coin_tracking.json")

def load_tracked_coins():
    if not TRACK_FILE.exists():
        return set()
    try:
        with open(TRACK_FILE, "r") as f:
            data = f.read().strip()
            if not data:
                return set()
            return set(json.loads(data))
    except (json.JSONDecodeError, IOError):
        return set()
    
def save_tracked_coins(coin_ids):
    with open(TRACK_FILE, "w") as f:
        json.dump(list(coin_ids), f)

def filter_new_coins(memecoins):
    tracked = load_tracked_coins()
    new_coins = [coin for coin in memecoins if coin["id"] not in tracked]
    return new_coins