import statistics
from src.sentiment.sentiment_model import analyze_sentiment, get_sentiment_label

def compute_sentiment_features(text_list):
    if not text_list or not isinstance(text_list, list):
        return {
            "avg_sentiment": 0,
            "num_positive": 0,
            "num_negative": 0,
            "num_neutral": 0
        }
    
    compound_scores = []
    pos, neg, neu = 0, 0, 0

    for text in text_list:
        score = analyze_sentiment(text)["compound"]
        compound_scores.append(score)
        label = get_sentiment_label(score)

        if label == "positive":
            pos += 1
        elif label == "negative":
            neg += 1
        else:
            neu += 1

    avg_sentiment = sum(compound_scores) / len(compound_scores)

    return {
        "avg_sentiment": avg_sentiment,
        "num_positive": pos,
        "num_negative": neg,
        "num_neutral": neu
    }

def compute_price_features(price_data):
    prices = [entry["price"] for entry in price_data]

    if len(prices) < 2:
        return {"price_7d_change": 0, "volatility": 0}
    
    price_change = ((prices[-1] - prices[0]) / prices[0]) * 100
    volatility = statistics.stdev(prices) if len(prices) > 1 else 0

    return {
        "price_7d_change": price_change,
        "volatility": volatility
    }  # ✅ <--- You were missing this line
