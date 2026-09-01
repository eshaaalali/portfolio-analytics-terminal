"""
portfolio_metrics.py

Fetches historical price data for a list of tickers and computes the core
risk/return metrics used by the dashboard: daily returns, cumulative
returns, annualised return, annualised volatility, Sharpe ratio, maximum
drawdown, and the correlation matrix across holdings.

If yfinance cannot reach the internet (no connection, or running in a
sandboxed environment), this module falls back to the bundled sample
dataset in sample_data/sample_prices.csv so the dashboard always has
something to render.
"""

import numpy as np
import pandas as pd

TRADING_DAYS_PER_YEAR = 252
RISK_FREE_RATE = 0.04  # annualised, used for Sharpe ratio


def fetch_price_data(tickers, period="2y"):
    """
    Try to fetch real historical closing prices via yfinance.
    Falls back to the bundled sample CSV on any failure (no internet,
    rate limit, etc.) so the project remains runnable offline.
    """
    try:
        import yfinance as yf

        data = yf.download(tickers, period=period, progress=False)["Close"]
        if isinstance(data, pd.Series):
            data = data.to_frame(name=tickers[0])
        if data.empty or data.isna().all().all():
            raise ValueError("Empty response from Yahoo Finance")
        return data.dropna(how="all")
    except Exception as exc:
        print(f"[portfolio_metrics] Live fetch failed ({exc}). "
              f"Falling back to bundled sample_data/sample_prices.csv")
        sample = pd.read_csv("sample_data/sample_prices.csv", index_col="Date", parse_dates=True)
        return sample[[t for t in tickers if t in sample.columns]]


def compute_metrics(prices: pd.DataFrame) -> dict:
    """
    Given a DataFrame of daily closing prices (columns = tickers),
    return a dict of computed series/frames used across the dashboard.
    """
    daily_returns = prices.pct_change().dropna()
    cumulative_returns = (1 + daily_returns).cumprod() - 1

    annualised_return = daily_returns.mean() * TRADING_DAYS_PER_YEAR
    annualised_vol = daily_returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR)
    sharpe_ratio = (annualised_return - RISK_FREE_RATE) / annualised_vol

    running_max = (1 + cumulative_returns).cummax()
    drawdown = (1 + cumulative_returns) / running_max - 1
    max_drawdown = drawdown.min()

    correlation_matrix = daily_returns.corr()

    summary = pd.DataFrame({
        "Annual Return": annualised_return,
        "Annual Volatility": annualised_vol,
        "Sharpe Ratio": sharpe_ratio,
        "Max Drawdown": max_drawdown,
    }).round(4)

    return {
        "prices": prices,
        "daily_returns": daily_returns,
        "cumulative_returns": cumulative_returns,
        "correlation_matrix": correlation_matrix,
        "summary": summary,
    }
