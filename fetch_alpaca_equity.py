#!/usr/bin/env python3
"""
Fetch portfolio equity data from Alpaca Paper Trading account and generate a graph.
"""

import os
import sys
from datetime import datetime
import matplotlib

# Use non-interactive backend for headless environments
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Correct imports for alpaca-py SDK
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetPortfolioHistoryRequest

# Constants for equity normalization
NORMALIZED_INITIAL_EQUITY = 100_000.0  # Always normalize equity to start from 100k USD


def fetch_equity_data(api_key: str, secret_key: str, timeframe: str = "1D", period: str = "1M"):
    """
    Fetch portfolio equity history from Alpaca.
    """
    client = TradingClient(api_key, secret_key, paper=True)

    valid_timeframes = {"1D", "1H", "15Min", "5Min", "1Min"}
    if timeframe not in valid_timeframes:
        raise ValueError(f"Unsupported timeframe: {timeframe}. Supported: {sorted(valid_timeframes)}")

    request_params = GetPortfolioHistoryRequest(
        period=period,
        timeframe=timeframe  # alpaca-py expects string
    )

    return client.get_portfolio_history(request_params)


def generate_equity_graph(portfolio_history, output_path: str = "alpaca_equity_graph.png"):
    """Generate an equity curve graph from portfolio history."""
    timestamps = portfolio_history.timestamp
    equity = portfolio_history.equity

    if not equity or len(equity) == 0:
        raise ValueError("No equity data available. Ensure your account has trading history.")

    dates = [datetime.fromtimestamp(ts) for ts in timestamps]

    # Set initial amount to 100000 without getting value from Alpaca
    # Display $100k as the initial amount (hardcoded, not from API)
    # IMPORTANT: This assumes the Alpaca account was funded with exactly $100k
    # If the actual starting balance differs, statistics will be inaccurate
    initial_equity = NORMALIZED_INITIAL_EQUITY
    final_equity = equity[-1]
    
    # Calculate return assuming 100k initial amount
    # WARNING: This will only be accurate if account actually started with ~$100k
    total_return = ((final_equity - initial_equity) / initial_equity) * 100
    return_text = f"Return:  {total_return:+.2f}%"

    stats_text = (
        f"Initial: ${initial_equity:,.2f}\n"
        f"Final:   ${final_equity:,.2f}\n"
        f"{return_text}"
    )

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(dates, equity, linewidth=2, color='#2E86AB', label='Portfolio Equity')
    ax.fill_between(dates, equity, alpha=0.3, color='#2E86AB')

    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Equity ($)', fontsize=12, fontweight='bold')
    ax.set_title('Alpaca Paper Trading - Portfolio Equity', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='lower left', fontsize=10)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)

    ax.text(
        0.98, 0.02, stats_text,
        transform=ax.transAxes,
        fontsize=10,
        horizontalalignment='right',
        verticalalignment='bottom',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    )


    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Equity graph saved to: {output_path}")

    return output_path


def main():
    """Main execution function."""
    # 🔑 Pull GitHub repo secrets (injected as env vars in Actions)
    api_key = os.getenv("ALPACA_API_KEY")
    secret_key = os.getenv("ALPACA_SECRET_KEY")

    if not api_key or not secret_key:
        print("ERROR: Alpaca API credentials not found. Ensure GitHub repo secrets are set:")
        print("  - ALPACA_API_KEY")
        print("  - ALPACA_SECRET_KEY")
        sys.exit(1)

    try:
        print("Fetching portfolio equity data from Alpaca...")
        portfolio_history = fetch_equity_data(api_key, secret_key, period="3M")

        print("Generating equity graph...")
        output_path = generate_equity_graph(portfolio_history)

        print(f"\n✓ Success! Graph saved to: {output_path}")

    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
