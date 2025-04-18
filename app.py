import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from src.model.predict_live import predict_for_trending
from src.price_data.coingecko_prices import get_coin_price_history

st.set_page_config(page_title="Memecoin Forecast", layout="wide")

# --- Custom Styling ---
st.markdown("""
<style>
.big-font {
    font-size: 36px;
    color: #F0B90B;
    text-align: center;
}
.price-box {
    background-color: #0f1117;
    border: 1px solid #333;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown('<div class="big-font">🪙 Memecoin Forecast Dashboard</div>', unsafe_allow_html=True)

# --- Run Prediction ---
if st.button("🔮 Analyze Trending Memecoins"):
    with st.spinner("Predicting memecoin movement..."):
        predict_for_trending()

# --- Load Prediction Results ---
try:
    df = pd.read_csv("data/predictions_live.csv").sort_values("predicted_change_pct", ascending=False)

    # --- Leaderboard ---
    st.markdown("### 🏆 Top 7 Predicted Memecoins by Predicted Change")

    top7 = df.head(7).copy()
    top7["Model Verdict"] = top7["prediction"].apply(lambda x: "🟢 BUY" if x == "BUY" else "🔴 SKIP")

    display_df = top7[["coin", "symbol", "predicted_change_pct", "Model Verdict"]]
    display_df.columns = ["Coin", "Symbol", "Predicted % Change", "Model Verdict"]
    display_df = display_df.reset_index(drop=True)

    st.markdown(f"""
    <div style='text-align: center;'>
        <div style='display: inline-block; padding: 1rem; background-color: #0f1117; border-radius: 10px'>
            {display_df.to_html(index=False, escape=False)}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # --- Individual Coin Detail View ---
    coin = st.selectbox("🔎 Select a memecoin to view details:", df["coin"].unique())
    selected = df[df["coin"] == coin].iloc[0]
    predicted_pct = selected["predicted_change_pct"]
    label = selected["prediction"]

    st.markdown(f"""
    <div class='price-box'>
        <h2>{coin} Prediction</h2>
        <h1 style='color: {"#00FF99" if label == "BUY" else "#FF6666"}'>{label}</h1>
        <p><strong>Expected Change:</strong> {predicted_pct:.2f}% over 7 days</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Fetch real price history and simulate forecast ---
    coin_id = selected.get("id", selected["symbol"].lower())
    price_df = get_coin_price_history(coin_id, days=7)

    if not price_df.empty:
        last_price = price_df["price"].iloc[-1]
        clamped_pct = max(min(predicted_pct, 10), -10)  # adjust range if needed
        daily_pct = clamped_pct / 5 / 100  # spread over 5 days
        forecast_prices = [last_price * (1 + daily_pct) ** (i + 1) for i in range(5)]
        forecast_dates = pd.date_range(start=price_df["timestamp"].iloc[-1] + pd.Timedelta(days=1), periods=5)

        forecast_df = pd.DataFrame({
            "timestamp": forecast_dates,
            "price": forecast_prices,
            "type": "Forecast"
        })

        price_df["type"] = "History"
        combined_df = pd.concat([price_df, forecast_df])

        st.markdown("### 📈 7-Day Price History + Forecast")
        fig = px.line(
            combined_df, x="timestamp", y="price", color="type",
            markers=True, title=f"{coin} Price Trend (USD)",
            template="plotly_dark"
        )
        fig.update_layout(height=400, xaxis_title="Time", yaxis_title="Price (USD)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Could not retrieve price data for this coin.")

    # --- Display contributing posts/snippets ---
    st.markdown("---")
    st.markdown("### 📰 Sentiment Sources")
    st.info("These are some of the recent Reddit/News snippets that contributed to the prediction:")

    try:
        sources_df = pd.read_csv("data/sentiment_sources.csv")
        coin_sources = sources_df[sources_df["coin"] == coin]

        for _, row in coin_sources.head(5).iterrows():
            st.markdown(f"- **{row['source']}**: {row['text'][:200]}...")
    except Exception as e:
        st.warning("⚠️ Could not load sentiment source data.")

except FileNotFoundError:
    st.warning("⚠️ No prediction data found. Please run a prediction first.")
