# US Equity Options Analysis

## Complete Workflow

```python
from openbb import obb
obb.user.preferences.output_type = "dataframe"

symbol = "AAPL"
chains = obb.derivatives.options.chains(symbol, provider='cboe')
price = chains['underlying_price'].iloc[0]

# Step 1: Filter valid options
valid = chains[(chains['dte'] >= 7) & (chains['dte'] <= 60) & (chains['delta'] != 0)]

# Step 2: Select expiration
expirations = sorted(valid['expiration'].unique())
selected = valid[valid['expiration'] == expirations[0]]

# Step 3: Separate calls/puts
calls = selected[selected['option_type'] == 'call']
puts = selected[selected['option_type'] == 'put']

# Step 4: Filter ATM range
atm_calls = calls[(calls['strike'] >= price * 0.95) & (calls['strike'] <= price * 1.05)]
atm_puts = puts[(puts['strike'] >= price * 0.95) & (puts['strike'] <= price * 1.05)]

# Step 5: Display Greeks
print(atm_calls[['strike', 'delta', 'gamma', 'theta', 'vega', 'bid', 'ask']])
```

## Key Columns

| Column | Description |
|--------|-------------|
| strike | Strike price |
| expiration | Expiration date |
| dte | Days to expiration |
| option_type | 'call' or 'put' |
| bid/ask | Current prices |
| delta/gamma/theta/vega | Greeks |
| implied_volatility | IV |
| open_interest | OI |
| volume | Daily volume |
| underlying_price | Current stock price |

## Providers

| Provider | Coverage | Data Quality |
|----------|----------|--------------|
| cboe | US equities, ETFs | Real-time, comprehensive |
| yfinance | US equities | Delayed, free |
| tradier | US equities | Real-time (API key) |

## Implied Move Calculation

```python
# Using straddle method (requires OBBject output)
obb.user.preferences.output_type = "OBBject"
options = obb.derivatives.options.chains(symbol, provider="cboe")

straddle = options.results.straddle(days=options.results.expirations[1])
straddle_price = straddle.loc["Cost"].values[0]
dte = straddle.loc["DTE"].values[0]
last_price = options.results.underlying_price[0]

implied_daily_move = ((1 + straddle_price / last_price) ** (1 / dte) - 1) * 100
```
