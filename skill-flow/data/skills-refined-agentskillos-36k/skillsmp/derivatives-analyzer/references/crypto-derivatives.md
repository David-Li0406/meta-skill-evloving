# Crypto Derivatives Guide (Deribit)

## Supported Symbols

| Asset | Perpetual | Options |
|-------|-----------|---------|
| BTC | BTC-PERPETUAL | ✓ |
| ETH | ETH-PERPETUAL | ✓ |
| SOL | SOL_USDC-PERPETUAL | ✓ |
| XRP | XRP_USDC-PERPETUAL | - |
| BNB | BNB_USDC-PERPETUAL | - |
| PAXG | PAXG_USDC-PERPETUAL | - |

## Perpetual Contracts

### Get Current Stats

```python
from openbb import obb
obb.user.preferences.output_type = "dataframe"

# Single symbol
info = obb.derivatives.futures.info(provider='deribit', symbol='BTC')

# Multiple symbols
info = obb.derivatives.futures.info(provider='deribit', symbol='BTC,ETH,SOL')
```

### Key Metrics

| Metric | Description |
|--------|-------------|
| last_price | Current trading price |
| mark_price | Fair value for liquidations |
| index_price | Spot index price |
| current_funding | Current funding rate |
| funding_8h | 8-hour funding rate |
| open_interest | Total open contracts (USD) |
| volume_usd | 24h volume in USD |
| change_percent | 24h price change % |

### List All Instruments

```python
instruments = obb.derivatives.futures.instruments(provider='deribit')
# Filter perpetuals
perps = instruments[instruments['symbol'].str.contains('PERPETUAL')]
```

## Crypto Options

### Get Options Chains

```python
chains = obb.derivatives.options.chains(symbol='BTC', provider='deribit')
```

### Filter Parameters

| Param | Type | Description |
|-------|------|-------------|
| delay | eod/realtime/delayed | Data freshness |
| date | YYYY-MM-DD | Specific EOD date |
| option_type | call/put | Filter by type |
| moneyness | otm/itm/all | Filter by moneyness |
| strike_gt/lt | int | Strike range filter |
| volume_gt/lt | int | Volume filter |
| oi_gt/lt | int | Open interest filter |
| model | black_scholes/bjerk | Pricing model |

### Example: High Volume BTC Calls

```python
chains = obb.derivatives.options.chains(
    symbol='BTC',
    provider='deribit',
    option_type='call',
    moneyness='otm',
    volume_gt=100
)
```

## Funding Rate Analysis

Positive funding = longs pay shorts (bullish sentiment)
Negative funding = shorts pay longs (bearish sentiment)

```python
info = obb.derivatives.futures.info(provider='deribit', symbol='BTC,ETH,SOL')
funding = info[['symbol', 'current_funding', 'funding_8h', 'open_interest']]
```
