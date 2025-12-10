# Quick Start Guide: Alpaca Equity Graph Integration

## What Was Added

This PR adds live equity graph tracking from your Alpaca paper trading account to the RainDrop markdown report.

## Files Added/Modified

1. **fetch_alpaca_equity.py** - Main script to fetch and visualize equity data
2. **requirements.txt** - Python dependencies (alpaca-py, matplotlib)
3. **README.md** - Complete setup and usage documentation
4. **.gitignore** - Excludes Python cache and sensitive files
5. **report.md** - Updated with live equity graph section
6. **.github/workflows/update_equity_graph.yml** - Optional automated updates
7. **alpaca_equity_graph.png** - Sample placeholder graph

## How to Use

### Step 1: Get Your Alpaca API Credentials

1. Sign up for a free account at https://alpaca.markets/
2. Navigate to your dashboard
3. Generate **Paper Trading** API keys
4. Save your API Key and Secret Key

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Set Environment Variables

**Option A: Using export (Linux/Mac)**
```bash
export ALPACA_API_KEY="your_api_key_here"
export ALPACA_SECRET_KEY="your_secret_key_here"
```

**Option B: Using .env file**
Create a `.env` file in the repository root:
```
ALPACA_API_KEY=your_api_key_here
ALPACA_SECRET_KEY=your_secret_key_here
```

Then load it before running the script:
```bash
source .env  # or: export $(cat .env | xargs)
```

**Option C: Inline (for one-time use)**
```bash
ALPACA_API_KEY="your_key" ALPACA_SECRET_KEY="your_secret" python fetch_alpaca_equity.py
```

### Step 4: Generate the Equity Graph

```bash
python fetch_alpaca_equity.py
```

This will:
- Connect to your Alpaca paper trading account
- Fetch the last 3 months of equity history
- Generate a professional graph with statistics
- Save it as `alpaca_equity_graph.png`

### Step 5: View the Report

Open `report.md` to see your live equity graph integrated into the report!

## Customization

### Change the Time Period

Edit `fetch_alpaca_equity.py` and modify line ~122:
```python
portfolio_history = fetch_equity_data(api_key, secret_key, period="6M")  # 1M, 3M, 6M, 1Y, etc.
```

### Change the Timeframe Granularity

```python
portfolio_history = fetch_equity_data(api_key, secret_key, timeframe="1H", period="1M")
# Options: "1D", "1H", "15Min", "5Min", "1Min"
```

## Automated Updates (Optional)

### Using GitHub Actions

1. Go to your GitHub repository settings
2. Navigate to: Settings → Secrets and variables → Actions
3. Add two secrets:
   - `ALPACA_API_KEY`
   - `ALPACA_SECRET_KEY`

The workflow will automatically:
- Run every weekday at 6 PM UTC (after US market close)
- Fetch fresh equity data
- Update the graph
- Commit the changes

You can also trigger it manually:
- Go to Actions tab → "Update Alpaca Equity Graph" → Run workflow

## Security Notes

✓ API credentials are never committed to git
✓ .gitignore prevents accidental commits of .env files
✓ All secrets handled via environment variables
✓ CodeQL security scan passed with no vulnerabilities

## Troubleshooting

**Error: "No equity data available"**
- Ensure you have some trading activity in your Alpaca paper account
- Try a longer time period (e.g., "6M" instead of "1M")

**Error: "Alpaca API credentials not found"**
- Make sure environment variables are set correctly
- Try the inline method: `ALPACA_API_KEY="..." python fetch_alpaca_equity.py`

**Error: "ModuleNotFoundError"**
- Install dependencies: `pip install -r requirements.txt`

## Support

For issues with:
- The script: Check the error message and README.md
- Alpaca API: Visit https://alpaca.markets/docs/
- This repository: Open an issue on GitHub

---

**Note**: This integration uses Alpaca's **Paper Trading** environment, which is free and requires no real money. It's perfect for testing strategies!
