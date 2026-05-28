---
name: adaptive-predator-prey
description: "Use when tuning predator-prey dynamics, regime detection coefficients, or cooldown mechanisms"
author: Claude
date: 2025-01-21
version: v3.3.0
---

# Adaptive Predator-Prey Dynamics (v3.3.0)

## Overview
| Item | Details |
|------|---------|
| **Date** | 2025-01-21 |
| **Goal** | Make Lotka-Volterra predator-prey coefficients adaptive to market conditions |
| **File** | `alpaca_trading/signals/predator_prey.py` |
| **Status** | Success |

## Context
The predator-prey Markov model uses Lotka-Volterra dynamics to detect regime transitions:
- **Predator (P)**: Represents trend followers / momentum traders
- **Prey (N)**: Represents value / mean-reversion traders

Previously, coefficients were fixed:
- `a = 0.8` (predator growth rate)
- `b = 0.05` (interaction rate)
- Cooldown was binary (0 or 1)

This didn't adapt to changing market conditions.

## Solution: Adaptive Coefficients

### Predator Coefficient (a) - Adapts to Volatility
```python
# Higher volatility = faster predator growth (momentum strategies thrive)
# vol_ratio = current_vol / baseline_vol
a = 0.8 + 0.3 * max(0, vol_ratio_local - 1.0)
a = min(1.1, a)  # Cap at 1.1

# Effect:
# - vol_ratio = 1.0: a = 0.8 (baseline)
# - vol_ratio = 1.5: a = 0.95 (faster growth)
# - vol_ratio = 2.0+: a = 1.1 (capped)
```

### Interaction Coefficient (b) - Adapts to Momentum
```python
# Stronger momentum = stronger interaction (more decisive regime shifts)
# momentum_strength = abs(returns[-5:].mean())
b = 0.05 + 0.1 * min(0.3, momentum_strength)

# Effect:
# - momentum = 0: b = 0.05 (baseline)
# - momentum = 0.15: b = 0.065 (moderate)
# - momentum = 0.30+: b = 0.08 (strong interaction)
```

### Exponential Decay Cooldown
```python
# OLD: Binary gate (either 0% or 100% allowed)
if bars_since_flat < cooldown_bars:
    entry_allowed = 0
else:
    entry_allowed = 1

# NEW: Exponential decay (gradual unlock)
cooldown_factor = min(1.0, bars_since_flat / cooldown_bars)
effective_edge = edge * cooldown_factor

# Effect:
# - Just exited (0 bars): cooldown_factor = 0.0
# - Halfway (cooldown/2): cooldown_factor = 0.5
# - Full cooldown: cooldown_factor = 1.0
```

## Code Location
```python
# predator_prey.py - _compute_edge method (~line 240)
def _compute_edge(
    self,
    N: float,
    P: float,
    N_prime: float,
    P_prime: float,
    bars_since_flat: int,
    cooldown_bars: int,
    vol_ratio_local: float = 1.0,
    momentum_strength: float = 0.0,
) -> Tuple[float, int, float, float]:
    """Compute trading edge with adaptive dynamics."""

    # v3.3.0: Adaptive predator coefficient based on volatility
    a = 0.8 + 0.3 * max(0, vol_ratio_local - 1.0)
    a = min(1.1, a)

    # v3.3.0: Adaptive interaction coefficient based on momentum
    b = 0.05 + 0.1 * min(0.3, momentum_strength)

    # v3.3.0: Exponential decay cooldown (was binary gate)
    cooldown_factor = min(1.0, bars_since_flat / cooldown_bars)
    effective_edge = edge * cooldown_factor
```

## Macro Regime Influence (v3.3.0)

### Increased Influence Weight
```python
# harmonized_gpu.py (~line 362)
# OLD: Weak influence (12%)
bull_trend_boost = p_bull * 0.12
bear_trend_boost = p_bear * 0.12

# NEW: Stronger influence (30%)
bull_trend_boost = p_bull * 0.30
bear_trend_boost = p_bear * 0.30
```

This makes macro regime (bull/sideways/bear) have 2.5x more influence on fine-scale chains.

### Dynamic Volatility Gate
```python
# OLD: Static threshold
vol_gate_threshold = 0.6

# NEW: Dynamic threshold based on current volatility
vol_gate_base = 0.3      # Minimum threshold
vol_gate_scale = 0.5     # Scaling factor
vol_gate_threshold = vol_gate_base + vol_gate_scale * (current_vol / vol_p90)
```

## Key Insights

### Why Adaptive Coefficients?
Fixed coefficients assume market conditions are constant. In reality:
- **High volatility**: Momentum strategies work better, predators should grow faster
- **Strong momentum**: Regime transitions are more decisive, interaction should be stronger
- **After exits**: Need time to reassess, but binary cooldown is too restrictive

### Exponential vs Binary Cooldown
Binary cooldown: "No trading for N bars, then full trading"
- Problem: Misses opportunities near the end of cooldown
- Problem: No gradual re-entry based on confidence

Exponential decay: "Gradually increase position sizes as cooldown expires"
- Advantage: Can take partial positions during cooldown
- Advantage: Smooth transition from cautious to normal trading

### Macro Influence Strength
The 4-chain hierarchy (macro → vol/trend/momentum) was too weakly coupled.
Increasing macro influence from 12% to 30% makes:
- Bull macro regime → trend chain more likely to show "up"
- Bear macro regime → trend chain more likely to show "down"

## Failed Attempts

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Fixed a=0.8, b=0.05 | Didn't adapt to changing conditions | Make coefficients functions of market state |
| Binary cooldown | Too restrictive, missed opportunities | Use exponential decay for gradual unlock |
| 12% macro influence | Fine-scale chains operated nearly independently | Increase to 30% for stronger hierarchy |
| a coefficient unbounded | Could grow infinitely in high vol | Cap at reasonable max (1.1) |

## References
- Lotka-Volterra equations (predator-prey dynamics)
- Hierarchical Markov Models for regime detection
- arXiv 2508.01173 - MARS Meta-Adaptive Framework
