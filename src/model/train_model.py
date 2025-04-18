import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

def load_and_prepare_data(filepath):
    df = pd.read_csv(filepath)

    if "price_7d_change" not in df.columns:
        raise ValueError("Missing 'price_7d_change' column — required for regression.")

    print("\nTarget variable: 7-day price % change")
    print(df["price_7d_change"].describe())

    features = [
        "avg_sentiment", "num_positive", "num_negative", "num_neutral",
        "reddit_mentions", "google_mentions", "volatility"
    ]
    X = df[features]
    y = df["price_7d_change"]

    return X, y

def train_random_forest(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("\n✅ Regression Metrics:")
    print(f"📉 Mean Absolute Error: {mean_absolute_error(y_test, y_pred):.4f}")
    print(f"📈 R² Score: {r2_score(y_test, y_pred):.4f}")

    return model

if __name__ == "__main__":
    print("Training model using memecoin_features.csv...\n")
    X, y = load_and_prepare_data("data/memecoin_features.csv")
    model = train_random_forest(X, y)

    os.makedirs("model", exist_ok=True)
    joblib.dump(model, "model/latest_model.joblib")
    print("\nSaved trained regression model to model/latest_model.joblib")
