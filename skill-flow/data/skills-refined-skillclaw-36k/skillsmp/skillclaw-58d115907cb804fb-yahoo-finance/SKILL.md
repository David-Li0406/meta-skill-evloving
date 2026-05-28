---
name: yahoo-finance
description: Use this skill when you need to fetch stock prices, quotes, fundamentals, earnings, options, dividends, and analyst ratings from Yahoo Finance using the yfinance library.
---

# Yahoo Finance CLI

A Python CLI for fetching comprehensive stock data from Yahoo Finance using yfinance.

## Requirements

- Python 3.11+
- uv (for inline script dependencies)

## Installing uv

The script requires `uv` - an extremely fast Python package manager. Check if it's installed:

```bash
uv --version
```

If not installed, install it using one of these methods:

### macOS / Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### macOS (Homebrew)
```bash
brew install uv
```

### Windows
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### pip (any platform)
```bash
pip install uv
```

After installation, restart your terminal or run:
```bash
source ~/.bashrc  # or ~/.zshrc on macOS
```

## Installation

The `yf` script uses PEP 723 inline script metadata - dependencies are auto-installed on first run.

```bash
# Make executable
chmod +x /path/to/skills/yahoo-finance/yf

# Optionally symlink to PATH for global access
ln -sf /path/to/skills/yahoo-finance/yf /usr/local/bin/yf
```

First run will install dependencies (yfinance, rich) to uv's cache. Subsequent runs are instant.

## Commands

### Price (quick check)
```bash
yf AAPL              # shorthand for price
yf price AAPL
```

### Quote (detailed)
```bash
yf quote MSFT
```

### Fundamentals
```bash
yf fundamentals NVDA
```
Shows: PE ratios, EPS, market cap, margins, ROE/ROA, analyst targets.

### Earnings
```bash
yf earnings TSLA
```
Shows: Next earnings date, EPS estimates, earnings history with surprises.

### Company Profile
```bash
yf profile GOOGL
```
Shows: Sector, industry, employees, website, address, business description.

### Dividends
```bash
yf dividends KO
```
Shows: Dividend rate/yield, ex-date, payout ratio, recent dividend history.

### Analyst Ratings
```bash
yf ratings AAPL
```
Shows: Buy/hold/sell distribution, mean rating, recent upgrades/downgrades.

### Options Chain
```bash
yf options SPY
```
Shows: Near-the-money calls and puts with strike, bid/ask, volume, OI, IV.

### History
```bash
yf history GOOGL 1mo     # 1 month history
yf history TSLA 1y       # 1 year
yf history BTC-USD 5d    # 5 days
```
Ranges: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max

### Compare
```bash
yf compare AAPL,MSFT,GOOGL
```