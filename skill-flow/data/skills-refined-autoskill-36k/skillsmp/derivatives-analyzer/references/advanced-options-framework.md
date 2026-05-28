# Advanced Options Analysis Framework

Based on Greeks.live methodology (AntonLaVay/Manchurius Hao).

## Overview

This framework addresses three core limitations of basic ATM IV analysis:
1. **Skew blindness** - Missing tail risk signals from OTM options
2. **Greeks gap** - No practical risk management system
3. **Position sizing absence** - No capital allocation guidance

## Part 1: Enhanced Skew Analysis

### The Three-Chart System

Upgrade from basic 2-chart (ATM IV + Term Structure) to 3-chart analysis:

| Chart | Data | Signal |
|-------|------|--------|
| ATM IV + HV | IV vs 30-day RV | VRP opportunity |
| Term Structure | ATM IV across expirations | Calendar/Contango trades |
| **25Δ Skew** | Put IV - Call IV at 25-delta | Directional bias + tail risk |

### 25-Delta Risk Reversal

```python
def calculate_25d_risk_reversal(chains, expiration):
    """
    25Δ RR = 25Δ Call IV - 25Δ Put IV
    Positive: Market favors upside
    Negative: Market hedging downside
    """
    exp_chains = chains[chains['expiration'] == expiration]

    # Find 25-delta options
    calls = exp_chains[exp_chains['option_type'] == 'call']
    puts = exp_chains[exp_chains['option_type'] == 'put']

    call_25d = calls.iloc[(calls['delta'] - 0.25).abs().argsort()[:1]]
    put_25d = puts.iloc[(puts['delta'].abs() - 0.25).abs().argsort()[:1]]

    rr = call_25d['implied_volatility'].values[0] - put_25d['implied_volatility'].values[0]

    return {
        'risk_reversal': rr,
        'call_25d_iv': call_25d['implied_volatility'].values[0],
        'put_25d_iv': put_25d['implied_volatility'].values[0],
        'signal': 'BULLISH' if rr > 0.02 else 'BEARISH' if rr < -0.02 else 'NEUTRAL'
    }
```

### 25-Delta Butterfly (Smile Convexity)

```python
def calculate_25d_butterfly(chains, expiration):
    """
    Butterfly = (25Δ Call IV + 25Δ Put IV) / 2 - ATM IV
    High Fly: Market expects tail moves, vol premium available
    Low Fly: Flat smile, low vol-of-vol
    """
    exp_chains = chains[chains['expiration'] == expiration]

    atm_iv = get_atm_iv(exp_chains)
    call_25d_iv = get_25d_call_iv(exp_chains)
    put_25d_iv = get_25d_put_iv(exp_chains)

    fly = (call_25d_iv + put_25d_iv) / 2 - atm_iv

    return {
        'butterfly': fly,
        'atm_iv': atm_iv,
        'wing_avg_iv': (call_25d_iv + put_25d_iv) / 2,
        'signal': 'HIGH_VOL_PREMIUM' if fly > 0.03 else 'LOW_PREMIUM' if fly < 0.01 else 'NORMAL'
    }
```

### Skew Term Structure

```python
def skew_term_structure(chains):
    """
    Track how 25Δ RR evolves across expirations.
    Steep negative slope: Near-term fear
    Flat: Stable expectations
    """
    expirations = chains['expiration'].unique()
    skew_curve = []

    for exp in sorted(expirations):
        rr = calculate_25d_risk_reversal(chains, exp)
        dte = (exp - datetime.now()).days
        skew_curve.append({
            'expiration': exp,
            'dte': dte,
            'risk_reversal': rr['risk_reversal']
        })

    return pd.DataFrame(skew_curve)
```

## Part 2: Greeks Risk Management

### Portfolio-Level Greeks Dashboard

```python
class GreeksDashboard:
    """
    Real-time portfolio Greeks aggregation.
    """

    def __init__(self, positions):
        self.positions = positions

    def calculate_net_greeks(self):
        """
        Aggregate Greeks across all positions.
        """
        net = {
            'delta': 0,
            'gamma': 0,
            'theta': 0,
            'vega': 0
        }

        for pos in self.positions:
            multiplier = pos['quantity'] * pos['contract_size']
            net['delta'] += pos['delta'] * multiplier
            net['gamma'] += pos['gamma'] * multiplier
            net['theta'] += pos['theta'] * multiplier
            net['vega'] += pos['vega'] * multiplier

        return net

    def risk_assessment(self):
        """
        Flag risk conditions.
        """
        net = self.calculate_net_greeks()
        alerts = []

        # Delta exposure check
        if abs(net['delta']) > 50:  # BTC equivalent
            alerts.append({
                'type': 'DELTA_EXPOSURE',
                'severity': 'HIGH' if abs(net['delta']) > 100 else 'MEDIUM',
                'message': f"Net Delta: {net['delta']:.2f} - Consider hedging"
            })

        # Short Gamma warning
        if net['gamma'] < -0.001:
            alerts.append({
                'type': 'SHORT_GAMMA',
                'severity': 'HIGH',
                'message': "Short Gamma position - vulnerable to large moves"
            })

        # Vega exposure check
        if abs(net['vega']) > 1000:
            alerts.append({
                'type': 'VEGA_EXPOSURE',
                'severity': 'MEDIUM',
                'message': f"High Vega exposure: {net['vega']:.0f}"
            })

        return {'net_greeks': net, 'alerts': alerts}
```

### Greeks Management Matrix

| Greek | Risk Profile | Management Action |
|-------|-------------|-------------------|
| **+Delta** | Long underlying exposure | Hedge with short futures/spot |
| **-Delta** | Short underlying exposure | Hedge with long futures/spot |
| **+Gamma** | Profit from moves | Gamma scalp opportunities |
| **-Gamma** | Hurt by moves | Set stop-loss, reduce near ATM short options |
| **+Theta** | Time decay income | Monitor Gamma risk trade-off |
| **-Theta** | Time decay cost | Ensure sufficient move expectation |
| **+Vega** | Long volatility | Profit if IV rises |
| **-Vega** | Short volatility | Profit if IV falls, risk on IV spike |

### Dynamic Delta Hedging

```python
def smart_delta_hedge(current_delta, hedge_band=0.1, urgency_threshold=0.3):
    """
    Zakamouline-inspired bandwidth hedging.
    Only hedge when delta exceeds threshold to reduce transaction costs.

    Parameters:
    - hedge_band: Trigger threshold (default 0.1 = 10% of position)
    - urgency_threshold: Critical level requiring immediate action
    """
    abs_delta = abs(current_delta)

    if abs_delta <= hedge_band:
        return {
            'action': 'HOLD',
            'hedge_size': 0,
            'reason': 'Delta within acceptable band'
        }

    urgency = 'CRITICAL' if abs_delta > urgency_threshold else 'NORMAL'

    return {
        'action': 'HEDGE',
        'hedge_size': -current_delta,
        'urgency': urgency,
        'reason': f'Delta {current_delta:.3f} exceeds band {hedge_band}'
    }
```

### Greeks Strategies by Scenario

| Scenario | Strategy | Greeks Profile |
|----------|----------|----------------|
| Expect large move, direction unknown | Long Straddle | +Gamma, +Vega, -Theta |
| Expect sideways market | Short Strangle | -Gamma, -Vega, +Theta |
| Pure long volatility | Buy far-month options | +Vega dominant |
| Volatility crush expected | Sell options post-event | -Vega, +Theta |
| Directional with vol protection | Long Call + Long Put Spread | +Delta, +Gamma |

## Part 3: Position Sizing Framework

### Account-Level Risk Controls

```python
class PositionSizer:
    """
    Multi-layer position sizing system.
    """

    def __init__(self, account_value, risk_tolerance='moderate'):
        self.account_value = account_value
        self.risk_params = self._get_risk_params(risk_tolerance)

    def _get_risk_params(self, tolerance):
        params = {
            'conservative': {
                'max_single_loss': 0.01,  # 1% per trade
                'max_options_allocation': 0.10,  # 10% in options
                'max_single_asset': 0.30  # 30% concentration
            },
            'moderate': {
                'max_single_loss': 0.02,
                'max_options_allocation': 0.20,
                'max_single_asset': 0.50
            },
            'aggressive': {
                'max_single_loss': 0.05,
                'max_options_allocation': 0.40,
                'max_single_asset': 0.70
            }
        }
        return params.get(tolerance, params['moderate'])

    def max_position_size(self, option_price, max_loss_per_contract):
        """
        Calculate max contracts based on single trade risk limit.
        """
        max_risk = self.account_value * self.risk_params['max_single_loss']
        max_contracts = max_risk / max_loss_per_contract
        return int(max_contracts)

    def delta_based_sizing(self, underlying_price, target_delta_exposure=0.10):
        """
        Size position based on desired delta exposure.

        target_delta_exposure: Fraction of account at risk to 1σ move
        """
        target_delta = (self.account_value * target_delta_exposure) / underlying_price
        return target_delta
```

### IV Percentile Dynamic Adjustment

```python
def iv_adjusted_sizing(base_size, current_iv, iv_percentile):
    """
    Adjust position size based on IV regime.

    Low IV: Increase size (options cheap)
    High IV: Decrease size (options expensive)
    """
    adjustments = {
        'very_low': 1.5,    # IV < 25th percentile
        'low': 1.25,        # 25-40th percentile
        'normal': 1.0,      # 40-60th percentile
        'high': 0.75,       # 60-75th percentile
        'very_high': 0.5    # > 75th percentile
    }

    if iv_percentile < 25:
        regime = 'very_low'
    elif iv_percentile < 40:
        regime = 'low'
    elif iv_percentile < 60:
        regime = 'normal'
    elif iv_percentile < 75:
        regime = 'high'
    else:
        regime = 'very_high'

    adjusted_size = base_size * adjustments[regime]

    return {
        'base_size': base_size,
        'adjusted_size': adjusted_size,
        'iv_percentile': iv_percentile,
        'regime': regime,
        'multiplier': adjustments[regime]
    }
```

### Position Sizing Decision Tree

```
1. Account Risk Check
   ├── Max single trade loss ≤ 2% account value
   ├── Total options allocation ≤ 20% account value
   └── Single asset concentration ≤ 50%

2. Delta-Based Sizing
   └── Target Delta = Account × Risk% ÷ Underlying Price

3. IV Regime Adjustment
   ├── IV < 25th pctl → Size × 1.5 (options cheap)
   ├── IV 25-75th pctl → Size × 1.0 (normal)
   └── IV > 75th pctl → Size × 0.5 (options expensive)

4. Margin Mode Selection
   ├── Isolated: Beginners, single strategies
   └── Cross: Experienced, portfolio hedging
```

### Example Sizing Calculation

```python
# Scenario: $100,000 account, BTC at $100,000, moderate risk

account = 100000
btc_price = 100000
risk_fraction = 0.10  # 10% directional exposure

# Step 1: Calculate target delta
target_delta = (account * risk_fraction) / btc_price
# = $10,000 / $100,000 = 0.1 BTC equivalent delta

# Step 2: If buying 0.5 delta calls
contracts_needed = target_delta / 0.5
# = 0.1 / 0.5 = 0.2 contracts

# Step 3: IV adjustment (assume IV at 80th percentile)
adjusted_contracts = 0.2 * 0.5  # High IV, reduce by 50%
# = 0.1 contracts
```

## Quick Reference: Upgraded Analysis System

### Before (2-Chart Basic)

| Chart | Data |
|-------|------|
| ATM IV | Single point IV |
| Term Structure | ATM IV by expiration |

### After (3-Chart Enhanced)

| Chart | Data | New Insight |
|-------|------|-------------|
| ATM IV + HV overlay | IV vs 30-day RV | VRP magnitude |
| Term Structure + Forward IV | ATM IV + implied forward | Calendar opportunity |
| 25Δ Skew + Historical percentile | RR with 90-day range | Directional edge + tail risk |

## Integration Checklist

- [ ] Calculate 25Δ Risk Reversal for all key expirations
- [ ] Track Butterfly for vol-of-vol premium
- [ ] Maintain real-time Greeks dashboard
- [ ] Apply delta hedging with bandwidth optimization
- [ ] Use IV percentile for position sizing adjustment
- [ ] Set account-level risk limits before trading

## References

- [Greeks.live Position Sizing](https://learn.greeks.live/area/position-sizing-techniques)
- [Analyzing Volatility Skew](https://learn.greeks.live/area/analyzing-volatility-skew)
- [25-Delta Risk Reversal](https://learn.greeks.live/path/how-does-the-25-delta-risk-reversal-differ-from-other-quotes)
- [Options Greeks - Amberdata](https://blog.amberdata.io/options-greeks-explained-managing-risk-in-crypto-derivatives)
