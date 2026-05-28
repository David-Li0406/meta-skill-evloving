---
name: integrated-risk-manager
description: "Use when implementing unified position sizing, Kelly criterion, or combining GARCH+Capital+Portfolio risk systems"
author: Claude
date: 2025-01-21
version: v3.3.0
---

# Integrated Risk Manager - Unified Position Sizing (v3.3.0)

## Overview
| Item | Details |
|------|---------|
| **Date** | 2025-01-21 |
| **Goal** | Unify GARCH, Capital Manager, and Portfolio Risk into single coherent sizing system |
| **File** | `alpaca_trading/risk/integrated_risk.py` |
| **Status** | Success |

## Context
Previously, position sizing was done by three separate systems:
1. **GARCHRiskManager** - volatility-adjusted sizing
2. **CapitalManager** - 30% safety buffer, 20% position limits
3. **AdvancedRiskManager** - VaR, concentration, correlation limits

These systems were disconnected - each applied constraints independently, sometimes contradicting each other. Drawdown scaling was applied AFTER all sizing, reducing effectiveness.

## Solution: IntegratedRiskManager

### Key Components
```python
from alpaca_trading.risk.integrated_risk import IntegratedRiskManager, PortfolioState

# Initialize with existing managers
integrated_risk_mgr = IntegratedRiskManager(
    garch_manager=garch_mgr,
    capital_manager=capital_mgr,
    portfolio_risk_manager=portfolio_risk_mgr,
    max_drawdown=0.15,         # 15% max drawdown
    use_kelly_sizing=True,     # Kelly-inspired sizing
    half_kelly=True,           # Conservative half-Kelly
)

# Build portfolio state
portfolio_state = PortfolioState(
    total_value=100_000,
    cash_available=50_000,
    current_positions={'AAPL': {'qty': 100, 'price': 150.0}},
    current_drawdown_pct=0.05,  # 5% drawdown
    recent_win_rate=0.55,
    avg_win_pct=0.015,
    avg_loss_pct=0.010,
)

# Get unified position size
result = integrated_risk_mgr.calculate_position_size(
    symbol='GOOGL',
    signal_strength=0.75,
    model_size_mult=0.50,  # From 7-action space
    price=175.0,
    returns=returns_series,
    portfolio_state=portfolio_state,
)

print(f"Final value: ${result.final_value:.2f}")
print(f"Vol regime: {result.vol_regime}")
print(f"Drawdown scale: {result.drawdown_scale:.2f}")
```

### Position Sizing Pipeline
1. **Kelly-inspired base size** (if enabled)
   - Half-Kelly: `kelly_fraction * 0.5`
   - Bounded: 5% to 25% of available capital
2. **GARCH volatility adjustment**
   - Dynamic regime thresholds (percentile-based)
   - Multipliers: low_vol=1.2, normal=1.0, high_vol=0.6, extreme=0.3
3. **Correlation penalty**
   - Reduces size if correlated with existing positions
   - Uses rolling correlation from returns history
4. **Quadratic drawdown scaling**
   - Applied BEFORE other sizing (earlier = more effective)
   - Formula: `1.0 - (current_dd / max_dd)^2`
5. **Capital manager constraints**
   - 20% max per position, 30% safety buffer

## Key Insights

### Dynamic Volatility Thresholds (v3.3.0)
Old approach used static thresholds (10%, 25%, 35% annualized volatility).
New approach uses percentile-based classification:
- Looks at historical volatility distribution
- Classifies current volatility relative to history
- More adaptive to market conditions

### Graduated Profit Inclusion (Capital Manager Fix)
Old approach excluded ALL unrealized profits from conservative account value.
Problem: On winning days, available capital DECREASED despite profits.

New approach (v3.3.0):
```python
# Graduated exclusion based on profit size
if profit_ratio < 0.05:
    profit_exclusion = total_unrealized_profit * 0.50  # 50% excluded
elif profit_ratio < 0.10:
    profit_exclusion = total_unrealized_profit * 0.60  # 60% excluded
elif profit_ratio < 0.20:
    profit_exclusion = total_unrealized_profit * 0.70  # 70% excluded
else:
    profit_exclusion = total_unrealized_profit * 0.80  # 80% excluded
```

### Quadratic Drawdown Scaling
Linear scaling (`1 - dd/max_dd`) reduces size too gradually.
Quadratic scaling (`1 - (dd/max_dd)^2`) is more aggressive near max drawdown:
- At 5% DD (max 15%): scale = 0.89 (mild reduction)
- At 10% DD: scale = 0.56 (moderate reduction)
- At 14% DD: scale = 0.13 (aggressive reduction)

## Failed Attempts

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Full Kelly sizing | Too aggressive, large drawdowns | Use half-Kelly with 5-25% bounds |
| Static vol thresholds | Didn't adapt to regime changes | Use percentile-based dynamic thresholds |
| Drawdown scaling AFTER sizing | Size already computed, late reduction | Apply drawdown scaling BEFORE other calcs |
| Excluding all profits | Punished winning days | Graduated inclusion based on profit size |

## References
- arXiv 2506.04358 - Risk-Aware RL Reward for Trading
- arXiv 2508.16598 - Volatility-Adjusted ATR Sizing
- Kelly Criterion best practices for trading
