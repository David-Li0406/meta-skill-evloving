---
name: derivatives-analyzer
description: |
  OpenBB-based derivatives trading analysis toolkit covering crypto perpetual contracts, crypto options, and US equity options. Use when analyzing: (1) Crypto perpetuals - funding rates, open interest, mark price via Deribit; (2) BTC/ETH/SOL options - Greeks, IV surface, option chains; (3) US stock options - SPY/AAPL/NVDA chains, Greeks visualization, unusual activity detection; (4) Any derivatives Greeks analysis (delta, gamma, theta, vega); (5) Implied volatility and options pricing; (6) Volatility trading strategies - VRP, term structure, skew, fly, straddle delta hedge, calendar spreads, smile carry. Triggers: "analyze BTC perpetual", "show ETH options", "SPY options chain", "Greeks analysis", "IV surface", "funding rate", "options Greeks", "straddle price", "vol signals", "VRP analysis", "term structure", "skew analysis", "volatility trading".
---

# Derivatives Analyzer

OpenBB-powered derivatives analysis for crypto and equity markets.

## Prerequisites

```bash
pip install openbb openbb-deribit
```

## Quick Start

```python
from openbb import obb
obb.user.preferences.output_type = "dataframe"
```

## Supported Assets

| Category | Symbols | Provider |
|----------|---------|----------|
| Crypto Perpetuals | BTC, ETH, SOL, XRP, BNB | Deribit |
| Crypto Options | BTC, ETH, SOL | Deribit |
| US Equity Options | Any US stock | CBOE, yfinance |

## Core Workflows

### 1. Crypto Perpetual Analysis

```python
# Get perpetual stats
info = obb.derivatives.futures.info(provider='deribit', symbol='BTC')
# Returns: last_price, funding_rate, open_interest, volume, mark_price

# List all instruments
instruments = obb.derivatives.futures.instruments(provider='deribit')
```

Key metrics: `current_funding`, `funding_8h`, `open_interest`, `mark_price`, `volume_usd`

### 2. Crypto Options Analysis

```python
chains = obb.derivatives.options.chains(symbol='BTC', provider='deribit')
# Filter params: option_type, moneyness, strike_gt/lt, oi_gt, volume_gt
```

For Greeks filtering pattern, see [references/greeks-filtering.md](references/greeks-filtering.md).

### 3. US Equity Options Analysis

```python
chains = obb.derivatives.options.chains(symbol='SPY', provider='cboe')
price = chains['underlying_price'].iloc[0]

# Filter valid Greeks (critical step)
valid = chains[(chains['dte'] >= 7) & (chains['dte'] <= 60) & (chains['delta'] != 0)]
```

For complete workflow, see [references/equity-options.md](references/equity-options.md).

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/perpetual_analysis.py` | Crypto perpetual funding & OI analysis |
| `scripts/options_greeks.py` | Options Greeks analysis & visualization |
| `scripts/iv_surface.py` | Implied volatility surface plotting |
| `scripts/vol_signals.py` | Volatility trading signals (TS, Skew, Fly, VRP) |

## References

- [greeks-filtering.md](references/greeks-filtering.md) - Greeks data filtering patterns
- [equity-options.md](references/equity-options.md) - US equity options workflow
- [crypto-derivatives.md](references/crypto-derivatives.md) - Crypto derivatives guide
- [volatility-trading-strategies.md](references/volatility-trading-strategies.md) - Vol trading strategies (Jeff Liang methodology)
- [advanced-options-framework.md](references/advanced-options-framework.md) - Enhanced skew analysis, Greeks management, position sizing (Greeks.live methodology)

## Volatility Trading Framework

### Core PnL Formula
```
Vol Trade PnL = Vega PnL + Gamma Carry + Residuals - Fees
Smile Carry = Volga Carry + Vanna Carry
```

### Key Indicators

| Indicator | Formula | Signal |
|-----------|---------|--------|
| Term Structure | Far IV - Near IV | Contango = sell calendar |
| Fly | (25D Call + Put IV)/2 - ATM IV | High = more vol premium |
| Skew | 25D Put IV - Call IV | Right turn = bullish |
| VRP | IV - RV | Positive = sell vol |

For complete strategy guide, see [volatility-trading-strategies.md](references/volatility-trading-strategies.md).

## Common Patterns

### Filter ATM Options (±5%)

```python
atm = chains[(chains['strike'] >= price * 0.95) & (chains['strike'] <= price * 1.05)]
calls = atm[atm['option_type'] == 'call']
puts = atm[atm['option_type'] == 'put']
```

### Calculate Straddle Cost

```python
straddle = options.results.straddle(days=expiry)
cost = straddle.loc["Cost"].values[0]
dte = straddle.loc["DTE"].values[0]
implied_move = ((1 + cost / price) ** (1 / dte) - 1) * 100
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `No data found` | Invalid symbol | Verify symbol format (e.g., 'BTC' not 'BTC-USD') |
| `Provider not available` | Missing extension | Run `pip install openbb-deribit` |
| `Empty DataFrame` | Market closed | Check market hours; try different expiration |
| `KeyError: 'delta'` | Greeks unavailable | Use provider with Greeks (cboe > yfinance) |

## Rate Limits

| Provider | Limit | Notes |
|----------|-------|-------|
| Deribit | 20 req/sec | No API key for public data |
| CBOE | Generous | No explicit limit |
| yfinance | ~2000/hour | May throttle on heavy use |

## Advanced Analysis Framework

### Three-Chart System (Greeks.live Methodology)

| Chart | Purpose | Key Metric |
|-------|---------|------------|
| ATM IV + HV | VRP identification | IV - RV spread |
| Term Structure | Calendar opportunities | Contango/Backwardation |
| 25Δ Skew | Directional bias + tail risk | Risk Reversal |

### 25-Delta Indicators

```python
# Risk Reversal: Directional bias
rr = call_25d_iv - put_25d_iv  # Positive = bullish

# Butterfly: Tail risk premium
fly = (call_25d_iv + put_25d_iv) / 2 - atm_iv  # High = more premium
```

### Position Sizing Rules

| Rule | Threshold |
|------|-----------|
| Max single trade loss | ≤ 2% account |
| Total options allocation | ≤ 20% account |
| Single asset concentration | ≤ 50% options |

### IV Regime Adjustment

| IV Percentile | Size Multiplier | Rationale |
|---------------|-----------------|-----------|
| < 25% | 1.5x | Options cheap |
| 25-75% | 1.0x | Normal |
| > 75% | 0.5x | Options expensive |

For complete framework, see [advanced-options-framework.md](references/advanced-options-framework.md).
