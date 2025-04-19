# Meme-Coin Price Predictor

**Live Prediction Dashboard for Trending Memecoins using Real-Time Sentiment and Price Data**
## 📈 Live Demo  
🎯 Check it out here: [https://meme-coin-price-predictor.streamlit.app/](https://meme-coin-price-predictor.streamlit.app/)
---

## Overview
This project is a full-stack AI-powered application that predicts the short-term price direction of trending memecoins (like $DOGE, $PEPE, $FARTCOIN, etc.) using:

- Real-time price data from CoinGecko
- Machine learning model trained on sentiment and volatility
- Live scraping of Reddit + Google News (via DuckDuckGo)
- Forecasted price chart + sentiment source evidence

It features a sleek **Streamlit UI** for displaying top memecoins, predictions, confidence scores, and underlying sentiment.

---

## 🧠 Tech Stack

- **Frontend**: Streamlit
- **NLP**: VADER SentimentIntensityAnalyzer
- **Data Sources**: Reddit (PRAW), Twitter API, DuckDuckGo scraping
- **Model**: Custom ML model trained on historical sentiment + price data
- **Deployment**: Streamlit Cloud

## Live Features
- Trending Coin Detection – via CoinGecko's trending API
- Sentiment Scraping – Reddit and DuckDuckGo news snippets
- Feature Engineering – sentiment scores, mentions, volatility
- Regression-based Price Prediction – predicts 7-day price % change
- Forecast Chart – smooth price forecast with realistic compounding
- Confidence Score – customizable buy threshold (default: 3%)
- Source Transparency – displays relevant Reddit/News posts per coin

---

## Machine Learning
- Model: Random Forest Regressor
- Target: 7-day % price change
- Labeling: Based on actual price history
- Cutoff Logic: `BUY` if predicted change > 3%, else `SKIP`
- Training Data: Automatically built from historical features

---

## Project Structure
```
Meme-Coin-Price-Predictor/
├── app.py                      # Main Streamlit app
├── src/
│   ├── model/
│   │   ├── train_model.py     # ML training logic
│   │   └── predict_live.py    # Live prediction and scraping pipeline
│   ├── discovery/             # Trending coin discovery
│   ├── price_data/            # CoinGecko historical prices
│   ├── pipeline/              # Feature engineering, future labeling
│   └── sentiment/             # Reddit + DuckDuckGo scrapers + sentiment model
├── data/
│   ├── predictions_live.csv   # Output predictions used by app
│   └── sentiment_sources.csv  # Scraped sources per coin
├── model/
│   └── latest_model.joblib    # Saved ML model
└── README.md
```

---

## Local Development

### Requirements
```bash
Python >= 3.8
```
Install dependencies:
```bash
pip install -r requirements.txt
```

Run the app:
```bash
streamlit run app.py
```
---

## Example Output
- BUY signal: `Dogecoin` – 5.8% expected increase
- SKIP signal: `Shibabot` – 1.3% expected increase

Chart:
- Historical 7-day price
- Forecast line for 5 days based on ML prediction

Sentiment Snippets:
- Reddit: "DOGE back to the moon after Elon tweet!"
- News: "Memecoins showing early signs of reversal"

---

## Future Features
- Confidence bands on forecast chart
- Telegram/Twitter alerts for top coins
- Multi-model ensembling
- Ethereum gas cost & tokenomics overlay
- DEX volume or whale address activity integration

---

## Author
**Aaron Xu**  
[github.com/aaron9292](https://github.com/aaron9292)

Feel free to star the repo or suggest improvements via issues or PRs!

---

## License
MIT License

