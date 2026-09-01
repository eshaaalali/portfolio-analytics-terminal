"""
portfolio_dashboard.py

Entry point. Fetches price data for a portfolio of tickers, computes
risk/return metrics, and renders a Bloomberg Terminal-styled interactive
dashboard to output/dashboard.html.

Usage:
    python portfolio_dashboard.py
    python portfolio_dashboard.py AAPL MSFT NVDA TSLA JPM

If no tickers are passed on the command line, a default portfolio is used.
"""

import sys

from portfolio_metrics import fetch_price_data, compute_metrics
from dashboard import build_dashboard

DEFAULT_TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]


def main():
    tickers = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_TICKERS
    print(f"Building portfolio dashboard for: {', '.join(tickers)}")

    prices = fetch_price_data(tickers)
    metrics = compute_metrics(prices)

    print("\nPortfolio summary:")
    print(metrics["summary"])

    build_dashboard(metrics, tickers)


if __name__ == "__main__":
    main()
