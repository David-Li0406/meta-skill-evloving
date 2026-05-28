# Volatility Trading Strategies

Based on Jeff Liang (@JeffLia12309881) methodology.

## Core PnL Framework

### Basic Formula
```
Vol Trade PnL = Vega PnL + Gamma Carry + Residuals - Fees
```

### Advanced Decomposition
```
Vega PnL = Vega PnL dSigma0 + VegaFly PnL + VegaSkew PnL + Smile Carry

Smile Carry = Volga Carry + Vanna Carry
```

**Key Insight**: Carry = Alpha. Extract Carry effectively = become the house.

## Target Greeks Configuration

| Greek | Target | Rationale |
|-------|--------|-----------|
| Theta | Positive (180+) | Time decay income |
| Gamma | Positive (~0.00007) | Profit from volatility |
| Vega | Near zero | Neutral IV exposure |
| Net Delta | ~0 | Dynamic hedge balanced |
| Long/Short Size | Balanced | Tail risk immunity |

## Strategy Tiers

### Tier 1: Volatility Premium (Entry)
- Sell options when IV > RV
- Delta hedge to isolate vol premium
- 7-day VRP average: +6.7 points (BTC)

### Tier 2: Curvature Premium (Advanced)
- Trade the smile surface
- Calendar spreads in Contango
- Fly arbitrage

### Tier 3: Smile Carry (Expert)
- Volga Carry: Vol-of-Vol premium
- Vanna Carry: Delta-Vega correlation premium
- Requires second-order Greeks

## Key Market Indicators

### Term Structure (TS)
```python
# Contango: Far IV > Near IV
ts_spread = far_month_iv - near_month_iv

# Trading signal
if ts_spread > 0:  # Contango
    # Sell calendar: +Theta, +Gamma
    pass
if ts_at_3month_low:
    # High VRP opportunity
    pass
```

### Butterfly (Fly)
```python
# Fly = Vol-of-Vol proxy
fly = (call_25d_iv + put_25d_iv) / 2 - atm_iv

# High Fly: More premium from selling options
# Low Fly (3-month low): Market expects stable IV
```

### Skew
```python
skew = put_25d_iv - call_25d_iv

# Skew turning right (less negative): Bullish
# Skew turning left (more negative): Bearish, OTM call buying
```

### VRP (Variance Risk Premium)
```python
vrp = iv - rv  # Ex-post

# 7-day VRP using 5-min data: avg +6.7 points
# Negative VRP sustained: Pause selling strategies
```

## Specific Strategies

### 1. Straddle Sell + Delta Hedge
```python
# QQQ backtest (Sinclair):
# - Annual return: 20%
# - Sharpe ratio: 1.3
# BTC market: Higher premium, more optimization potential

def straddle_delta_hedge(symbol, expiry):
    chains = obb.derivatives.options.chains(symbol)
    atm_strike = find_atm_strike(chains)

    # Sell ATM straddle
    sell_call = chains[(chains['strike'] == atm_strike) &
                       (chains['option_type'] == 'call')]
    sell_put = chains[(chains['strike'] == atm_strike) &
                      (chains['option_type'] == 'put')]

    straddle_premium = sell_call['bid'] + sell_put['bid']
    net_delta = sell_call['delta'] + sell_put['delta']

    # Delta hedge with underlying
    hedge_size = -net_delta * 100  # shares to hedge

    return {
        'premium': straddle_premium,
        'initial_delta': net_delta,
        'hedge_size': hedge_size,
        'gamma': sell_call['gamma'] + sell_put['gamma'],
        'theta': sell_call['theta'] + sell_put['theta']
    }
```

### 2. Calendar Spread (Contango)
```python
# Sell near-term, buy far-term
# Result: +Theta, +Gamma
# Caveat: Consider Volga time cost for true premium

def calendar_spread_signal(chains):
    near_expiry = get_nearest_expiry(chains, min_dte=7)
    far_expiry = get_expiry_by_dte(chains, target_dte=30)

    near_iv = chains[chains['expiration'] == near_expiry]['implied_volatility'].mean()
    far_iv = chains[chains['expiration'] == far_expiry]['implied_volatility'].mean()

    contango = far_iv > near_iv
    spread = far_iv - near_iv

    return {
        'contango': contango,
        'spread': spread,
        'signal': 'SELL_CALENDAR' if contango and spread > 0.02 else 'WAIT'
    }
```

### 3. Dynamic Delta Hedge
```python
# Zakamouline: Smart Trading can have negative transaction costs
# Key: Optimize hedge bandwidth vs delta change risk

def hedge_decision(current_delta, hedge_band=0.1):
    """
    Hedge only when delta exceeds band.
    Reduces transaction costs while managing risk.
    """
    if abs(current_delta) > hedge_band:
        return {
            'action': 'HEDGE',
            'size': -current_delta,
            'urgency': 'HIGH' if abs(current_delta) > 0.3 else 'NORMAL'
        }
    return {'action': 'HOLD', 'size': 0}
```

## Signal Interpretation

| Indicator | Reading | Signal |
|-----------|---------|--------|
| TS at 3-month low | Short-long IV spread minimal | VRP extremely high, buy vol |
| Fly at 3-month low | Smile flat | Market expects no action |
| Skew turning right | Put premium decreasing | Bullish sentiment |
| VRP negative 2 months | RV > IV sustained | Pause vol selling |
| 0DTE IV spike to 44% | RV was 33% | Premium opportunity |

## Risk Management

### Position Sizing
- Balance Long/Short sizes to immunize tail risk
- Net Delta dynamically hedged to ~0

### When to Pause
- Sustained negative VRP
- Extreme realized volatility environment
- Major event risk (earnings, FOMC, etc.)

## Reference Materials

| Author | Topic |
|--------|-------|
| Sinclair | Straddle Delta Hedge backtests |
| Derman | Volatility Smile |
| Hagan | SABR Model - Managing Smile Risk |
| Zakamouline | Optimal Hedging with Transaction Costs |

## Key Quotes

> "波动率交易是一个窄门，参与者不足5-10%。但如果你有BTC、有数学基础，希望掌握不需要判断行情涨跌的BTC生息策略，那波动率交易就是最佳选择。"

> "入门时套Volatility溢价，进阶阶段是套曲面的溢价。"

> "Carry就是超额收益，就是alpha。"
