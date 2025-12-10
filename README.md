# RainDrop Quantitative Strategy

This repository contains the RainDrop quantitative equity strategy and its performance reports.

## Features

- Historical backtest results (2018-2025)
- Live Numerai Signals performance tracking
- **Live Alpaca Paper Trading equity graph integration**

## Setup

### Prerequisites

- Python 3.7 or higher
- Alpaca Paper Trading account (free at https://alpaca.markets/)

### Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Alpaca API credentials:

Create a `.env` file or set environment variables:
```bash
export ALPACA_API_KEY="your_api_key_here"
export ALPACA_SECRET_KEY="your_secret_key_here"
```

To get your Alpaca API credentials:
1. Sign up for a free account at https://alpaca.markets/
2. Go to your dashboard and generate Paper Trading API keys
3. Copy the API Key and Secret Key

### Generate Alpaca Equity Graph

Run the script to fetch your portfolio equity data and generate a graph:

```bash
python fetch_alpaca_equity.py
```

This will:
- Connect to your Alpaca Paper Trading account
- Fetch the last 3 months of portfolio equity data
- Generate a graph saved as `alpaca_equity_graph.png`
- Display portfolio statistics (initial equity, final equity, return %)

### Update Report

After generating the graph, the `report.md` file will automatically reference the equity graph image.

## Usage

### Customizing the Equity Graph

You can customize the graph generation by modifying the parameters in `fetch_alpaca_equity.py`:

- **Period**: Change `period="3M"` to `"1M"`, `"6M"`, `"1Y"`, etc.
- **Timeframe**: Modify the timeframe for data granularity
- **Output path**: Change the filename and location

### Automatic Updates

You can set up a cron job or GitHub Actions workflow to automatically update the equity graph on a schedule.

## Report

The main performance report is available in [report.md](report.md), which includes:

- Strategy overview and methodology
- Historical backtest results
- Numerai Signals live performance
- **Live Alpaca paper trading equity curve**

## Security

⚠️ **Important**: Never commit your API keys to the repository. Always use environment variables or a `.env` file (which is git-ignored).

## License

This project is for personal/research use.
