"""
generate_sample_data.py

Generates realistic-looking synthetic daily price data for a small set of
tickers, purely so this repo has something to run and demo offline (no
API key or internet connection required). When you run portfolio_dashboard.py
with an internet connection, it will fetch REAL data from Yahoo Finance via
yfinance instead, and this sample data is ignored.

This script is only needed once, to populate sample_data/.
"""

import numpy as np
import pandas as pd

np.random.seed(42)

TICKERS = {
    "AAPL": (0.00075, 0.018),   # (daily drift, daily volatility) - Apple
    "MSFT": (0.00070, 0.016),   # Microsoft
    "GOOGL": (0.00060, 0.019),  # Alphabet
    "AMZN": (0.00065, 0.022),   # Amazon
    "TSLA": (0.00080, 0.035),   # Tesla - higher volatility
}

START_PRICE = {
    "AAPL": 180.0,
    "MSFT": 340.0,
    "GOOGL": 135.0,
    "AMZN": 145.0,
    "TSLA": 240.0,
}

N_DAYS = 504  # ~2 trading years

dates = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=N_DAYS)

frames = {}
for ticker, (mu, sigma) in TICKERS.items():
    # Geometric Brownian Motion for a plausible price path
    daily_returns = np.random.normal(mu, sigma, N_DAYS)
    price_path = START_PRICE[ticker] * np.cumprod(1 + daily_returns)
    frames[ticker] = price_path

df = pd.DataFrame(frames, index=dates)
df.index.name = "Date"
df.to_csv("sample_data/sample_prices.csv")
print(f"Wrote sample_data/sample_prices.csv with {len(df)} rows for {list(TICKERS)}")
