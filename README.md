# Portfolio Analytics Terminal

An interactive stock portfolio risk & return dashboard, styled after the Bloomberg Terminal — black background, amber accents, monospace type, multi-panel "workstation" layout. Built with Python, pandas, and Plotly.

<img width="1600" height="1000" alt="dashboard_screenshot" src="https://github.com/user-attachments/assets/6173263d-db69-43d7-945c-11f8d0f23ee2" />


## What it does

Given a list of stock tickers, the dashboard:

- Fetches historical daily closing prices (via [`yfinance`](https://pypi.org/project/yfinance/))
- Computes annualised return, annualised volatility, Sharpe ratio, and maximum drawdown for each holding
- Renders four linked panels in a single self-contained HTML file:
  1. **Cumulative return** over time, one line per holding
  2. **Risk vs. return** scatter, bubble size scaled by Sharpe ratio
  3. **Correlation matrix** heatmap across holdings
  4. **Summary table** of return, volatility, Sharpe ratio, and max drawdown

The output is a single `.html` file with the Plotly chart engine embedded, so it opens and works fully offline in any browser — no server required.

## Quick start

```bash
pip install -r requirements.txt
python portfolio_dashboard.py
```

This builds a dashboard for the default portfolio (`AAPL MSFT GOOGL AMZN TSLA`) and writes it to `output/dashboard.html`. Open that file in a browser.

To analyse a different set of tickers:

```bash
python portfolio_dashboard.py NVDA JPM V KO DIS
```

### Running offline / without an API

If there's no internet connection (or Yahoo Finance is unreachable), the script automatically falls back to a bundled synthetic sample dataset (`sample_data/sample_prices.csv`) so the dashboard always has something to render. This is what the screenshot above was generated from. Regenerate that sample data with:

```bash
python generate_sample_data.py
```

## Project structure

```
portfolio_dashboard.py   # entry point — run this
portfolio_metrics.py     # data fetching + risk/return calculations
dashboard.py             # Plotly figure construction and Bloomberg-style theming
generate_sample_data.py  # builds the offline demo dataset
sample_data/              # bundled synthetic price data for offline use
output/                   # generated dashboard.html lands here
assets/                   # README screenshot
```

## Metrics explained

| Metric | Meaning |
|---|---|
| Annual Return | Mean daily return, annualised (× 252 trading days) |
| Annual Volatility | Standard deviation of daily returns, annualised (× √252) |
| Sharpe Ratio | (Annual Return − risk-free rate) / Annual Volatility. Risk-free rate assumed at 4%. |
| Max Drawdown | Largest peak-to-trough decline in cumulative value over the period |

## Possible extensions

- Add a benchmark index (e.g. S&P 500) overlaid on the cumulative return chart
- Add position sizing and portfolio-level (not just per-stock) return/volatility
- Add a date-range selector
- Deploy as a live Streamlit or Dash app instead of a static HTML export

## License

Free to use and modify.

