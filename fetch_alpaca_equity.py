#!/usr/bin/env python3
"""
Fetch portfolio equity data from Alpaca Paper Trading account and generate a graph.
"""

import os
import sys
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for headless environments
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetPortfolioHistoryRequest
from alpaca.trading.enums import TimeFrame


def fetch_equity_data(api_key: str, secret_key: str, timeframe: str = "1D", period: str = "1M"):
    """
    Fetch portfolio equity history from Alpaca.
    
    Args:
        api_key: Alpaca API key
        secret_key: Alpaca secret key
        timeframe: Timeframe for data points (1D, 1H, 15Min, 5Min, 1Min)
        period: Period to fetch (1M, 3M, 1Y, etc.)
    
    Returns:
        dict: Portfolio history data
    """
    # Initialize client for paper trading
    client = TradingClient(api_key, secret_key, paper=True)
    
    # Map timeframe string to TimeFrame enum
    timeframe_map = {
        "1D": TimeFrame.ONE_DAY,
        "1H": TimeFrame.ONE_HOUR,
        "15Min": TimeFrame.FIFTEEN_MIN,
        "5Min": TimeFrame.FIVE_MIN,
        "1Min": TimeFrame.ONE_MIN,
    }
    
    if timeframe not in timeframe_map:
        raise ValueError(f"Unsupported timeframe: {timeframe}. Supported values: {list(timeframe_map.keys())}")
    
    # Create request for portfolio history
    request_params = GetPortfolioHistoryRequest(
        period=period,
        timeframe=timeframe_map[timeframe]
    )
    
    # Get portfolio history
    portfolio_history = client.get_portfolio_history(request_params)
    
    return portfolio_history


def generate_equity_graph(portfolio_history, output_path: str = "alpaca_equity_graph.png"):
    """
    Generate an equity curve graph from portfolio history.
    
    Args:
        portfolio_history: Portfolio history object from Alpaca
        output_path: Path to save the graph image
    """
    # Extract data
    timestamps = portfolio_history.timestamp
    equity = portfolio_history.equity
    
    # Validate data
    if not equity or len(equity) == 0:
        raise ValueError("No equity data available from Alpaca. Ensure your account has trading history.")
    
    # Convert timestamps to datetime objects
    dates = [datetime.fromtimestamp(ts) for ts in timestamps]
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot equity curve
    ax.plot(dates, equity, linewidth=2, color='#2E86AB', label='Portfolio Equity')
    ax.fill_between(dates, equity, alpha=0.3, color='#2E86AB')
    
    # Format the plot
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Equity ($)', fontsize=12, fontweight='bold')
    ax.set_title('Alpaca Paper Trading - Portfolio Equity', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left', fontsize=10)
    
    # Format x-axis dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45, ha='right')
    
    # Add statistics
    initial_equity = equity[0]
    final_equity = equity[-1]
    total_return = ((final_equity - initial_equity) / initial_equity) * 100
    
    stats_text = f'Initial: ${initial_equity:,.2f}\nFinal: ${final_equity:,.2f}\nReturn: {total_return:+.2f}%'
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Tight layout and save
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Equity graph saved to: {output_path}")
    
    return output_path


def main():
    """Main execution function."""
    # Get API credentials from environment variables
    api_key = os.getenv('ALPACA_API_KEY')
    secret_key = os.getenv('ALPACA_SECRET_KEY')
    
    if not api_key or not secret_key:
        print("ERROR: Alpaca API credentials not found!")
        print("Please set the following environment variables:")
        print("  - ALPACA_API_KEY")
        print("  - ALPACA_SECRET_KEY")
        sys.exit(1)
    
    try:
        print("Fetching portfolio equity data from Alpaca...")
        portfolio_history = fetch_equity_data(api_key, secret_key, period="3M")
        
        print("Generating equity graph...")
        output_path = generate_equity_graph(portfolio_history)
        
        print(f"\n✓ Success! Graph saved to: {output_path}")
        print("You can now reference this image in your markdown report.")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
