"""
dashboard.py

Builds a single self-contained interactive HTML dashboard (Plotly) styled
after the Bloomberg Terminal: black background, amber/orange primary
accent, a monospace font, and a multi-panel "workstation" layout.

Panels:
  1. Cumulative returns over time, one line per holding
  2. Risk vs. return scatter (annualised volatility vs. annualised return),
     bubble size scaled by Sharpe ratio
  3. Correlation heatmap across holdings
  4. Summary metrics table (return, volatility, Sharpe, max drawdown)

Run `python portfolio_dashboard.py` to generate output/dashboard.html.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ---- Bloomberg Terminal inspired palette ----
BG_BLACK = "#000000"
PANEL_BLACK = "#0a0a0a"
AMBER = "#FF9900"
CYAN = "#00E5FF"
GREEN = "#00FF66"
YELLOW = "#FFE600"
MAGENTA = "#FF3EC9"
WHITE = "#E8E8E8"
GRID_GREY = "#262626"

SERIES_COLORS = [AMBER, CYAN, GREEN, YELLOW, MAGENTA, "#8C8CFF", "#FF6E40"]

FONT_FAMILY = "'Consolas', 'IBM Plex Mono', 'Courier New', monospace"


def build_dashboard(metrics: dict, tickers: list[str], output_path: str = "output/dashboard.html"):
    cumulative_returns = metrics["cumulative_returns"]
    summary = metrics["summary"]
    correlation_matrix = metrics["correlation_matrix"]

    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "xy"}, {"type": "xy"}],
               [{"type": "xy"}, {"type": "table"}]],
        subplot_titles=(
            "CUMULATIVE RETURN (%)",
            "RISK vs RETURN  (bubble size = Sharpe Ratio)",
            "CORRELATION MATRIX",
            "PORTFOLIO SUMMARY",
        ),
        horizontal_spacing=0.13,
        vertical_spacing=0.20,
        row_heights=[0.55, 0.45],
    )

    # ---- Panel 1: cumulative returns ----
    for i, ticker in enumerate(tickers):
        color = SERIES_COLORS[i % len(SERIES_COLORS)]
        fig.add_trace(
            go.Scatter(
                x=cumulative_returns.index,
                y=cumulative_returns[ticker] * 100,
                mode="lines",
                name=ticker,
                line=dict(color=color, width=1.6),
                legendgroup=ticker,
            ),
            row=1, col=1,
        )

    # ---- Panel 2: risk vs return bubble scatter ----
    for i, ticker in enumerate(tickers):
        color = SERIES_COLORS[i % len(SERIES_COLORS)]
        row = summary.loc[ticker]
        fig.add_trace(
            go.Scatter(
                x=[row["Annual Volatility"] * 100],
                y=[row["Annual Return"] * 100],
                mode="markers+text",
                text=[ticker],
                textposition="top center",
                textfont=dict(color=color, size=11),
                marker=dict(
                    size=max(14, abs(row["Sharpe Ratio"]) * 26),
                    color=color,
                    line=dict(color=WHITE, width=1),
                ),
                name=ticker,
                legendgroup=ticker,
                showlegend=False,
            ),
            row=1, col=2,
        )
    fig.update_xaxes(title_text="Annualised Volatility (%)", row=1, col=2)
    fig.update_yaxes(title_text="Annualised Return (%)", row=1, col=2)

    # ---- Panel 3: correlation heatmap ----
    fig.add_trace(
        go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.index,
            colorscale=[[0, "#1a1a1a"], [0.5, "#7a4a00"], [1, AMBER]],
            zmin=-1, zmax=1,
            text=correlation_matrix.round(2).values,
            texttemplate="%{text}",
            textfont=dict(color=WHITE, size=10),
            colorbar=dict(
                title=dict(text="ρ", font=dict(color=WHITE)),
                tickfont=dict(color=WHITE),
                outlinecolor=GRID_GREY,
                x=0.455, y=0.16, len=0.36, thickness=13,
            ),
            showscale=True,
        ),
        row=2, col=1,
    )

    # ---- Panel 4: summary table ----
    display_summary = summary.copy()
    display_summary["Annual Return"] = (display_summary["Annual Return"] * 100).map("{:.2f}%".format)
    display_summary["Annual Volatility"] = (display_summary["Annual Volatility"] * 100).map("{:.2f}%".format)
    display_summary["Sharpe Ratio"] = display_summary["Sharpe Ratio"].map("{:.2f}".format)
    display_summary["Max Drawdown"] = (display_summary["Max Drawdown"] * 100).map("{:.2f}%".format)

    fig.add_trace(
        go.Table(
            header=dict(
                values=["TICKER", "RETURN", "VOL", "SHARPE", "MAX DD"],
                fill_color=PANEL_BLACK,
                font=dict(color=AMBER, family=FONT_FAMILY, size=13),
                align="left",
                line_color=GRID_GREY,
                height=32,
            ),
            cells=dict(
                values=[
                    display_summary.index,
                    display_summary["Annual Return"],
                    display_summary["Annual Volatility"],
                    display_summary["Sharpe Ratio"],
                    display_summary["Max Drawdown"],
                ],
                fill_color=BG_BLACK,
                font=dict(color=WHITE, family=FONT_FAMILY, size=12.5),
                align="left",
                line_color=GRID_GREY,
                height=34,
            ),
        ),
        row=2, col=2,
    )

    fig.update_xaxes(title_text="", row=1, col=1)
    fig.update_yaxes(title_text="Return (%)", row=1, col=1)

    # ---- Global layout / theme ----
    fig.update_layout(
        title=dict(
            text="PORTFOLIO ANALYTICS TERMINAL &nbsp;&nbsp;|&nbsp;&nbsp; "
                 + " · ".join(tickers),
            font=dict(color=AMBER, family=FONT_FAMILY, size=21),
            x=0.01,
        ),
        paper_bgcolor=BG_BLACK,
        plot_bgcolor=PANEL_BLACK,
        font=dict(family=FONT_FAMILY, color=WHITE, size=12),
        legend=dict(
            bgcolor=PANEL_BLACK,
            bordercolor=GRID_GREY,
            borderwidth=1,
            font=dict(color=WHITE, size=12),
            orientation="h",
            yanchor="bottom", y=1.05,
            xanchor="right", x=1.0,
        ),
        margin=dict(l=70, r=60, t=130, b=50),
        width=1600,
        height=950,
    )

    fig.update_xaxes(showgrid=True, gridcolor=GRID_GREY, zerolinecolor=GRID_GREY, color=WHITE)
    fig.update_yaxes(showgrid=True, gridcolor=GRID_GREY, zerolinecolor=GRID_GREY, color=WHITE)

    # style subplot titles (amber, monospace)
    for annotation in fig["layout"]["annotations"]:
        annotation["font"] = dict(color=AMBER, family=FONT_FAMILY, size=14)

    fig.write_html(
        output_path,
        config={"displaylogo": False, "responsive": True},
        include_plotlyjs=True,
    )
    print(f"Dashboard written to {output_path}")
