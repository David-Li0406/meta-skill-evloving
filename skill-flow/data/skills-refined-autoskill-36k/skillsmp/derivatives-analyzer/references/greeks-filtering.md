# Greeks Filtering Patterns

## Why Filtering is Critical

Raw options chains often contain invalid Greeks data:
- Expired options (dte <= 0)
- Deep ITM/OTM options (delta = 0 or 1)
- Missing Greeks from certain expirations

## Standard Filter Pattern

```python
def get_valid_options(chains, min_dte=7, max_dte=60):
    """Filter options with valid Greeks data."""
    return chains[
        (chains['dte'] >= min_dte) &
        (chains['dte'] <= max_dte) &
        (chains['delta'] != 0) &
        (chains['delta'] != 1) &
        (chains['delta'] != -1)
    ]
```

## ATM Selection Pattern

```python
def get_atm_options(chains, price, pct_range=0.05):
    """Get at-the-money options within percentage range."""
    lower = price * (1 - pct_range)
    upper = price * (1 + pct_range)
    return chains[(chains['strike'] >= lower) & (chains['strike'] <= upper)]
```

## Greeks Quick Reference

| Greek | Measures | Call Range | Put Range | Max at |
|-------|----------|------------|-----------|--------|
| Delta | Price sensitivity | 0 to +1 | -1 to 0 | Deep ITM |
| Gamma | Delta change rate | + | + | ATM |
| Theta | Time decay | - | - | ATM |
| Vega | IV sensitivity | + | + | ATM, long DTE |

## Typical Delta Values

| Moneyness | Call Delta | Put Delta |
|-----------|------------|-----------|
| Deep ITM | 0.9 - 1.0 | -0.9 to -1.0 |
| ATM | ~0.5 | ~-0.5 |
| Deep OTM | 0.0 - 0.1 | -0.1 to 0.0 |
