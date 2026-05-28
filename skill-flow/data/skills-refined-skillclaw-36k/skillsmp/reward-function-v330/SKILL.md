---
name: reward-function-v330
description: "Use when tuning RL reward function weights, fixing reward hacking, or addressing P&L gradient issues"
author: Claude
date: 2025-01-21
version: v3.3.0
---

# Reward Function v3.3.0 - Risk-Aware Composite Reward

## Overview
| Item | Details |
|------|---------|
| **Date** | 2025-01-21 |
| **Goal** | Fix reward hacking and P&L gradient saturation |
| **Files** | `alpaca_trading/gpu/vectorized_env.py`, `alpaca_trading/gpu/ppo_trainer_native.py` |
| **Status** | Success |

## Context
v2.5.0 introduced `trading_incentive` (+0.02 for non-HOLD actions) to fix HOLD bias.
However, this created the opposite problem: **reward hacking via overtrading**.

Additional issues:
- Direction weight (40%) dominated despite being binary (+1/-1)
- P&L weight (25%) too low despite being the actual objective
- P&L saturated via `tanh(pnl * 10)` - destroyed gradient signal beyond ±0.1% moves
- Exploration was limited due to low entropy coefficient (0.005)

## Solution: Rebalanced Risk-Aware Reward

### Weight Changes
| Component | v2.5.0 | v3.3.0 | Rationale |
|-----------|--------|--------|-----------|
| direction_weight | 0.40 | **0.15** | Binary signal, shouldn't dominate |
| pnl_weight | 0.25 | **0.40** | Primary trading objective |
| magnitude_weight | 0.05 | 0.05 | Unchanged |
| exploration_weight | 0.15 | 0.15 | Unchanged |
| slippage_cost | 0.02 | 0.02 | Unchanged |
| drawdown_penalty | 0.03 | 0.03 | Unchanged |
| stop_tp_weight | 0.10 | 0.10 | Unchanged |
| **trading_incentive** | **0.02** | **REMOVED** | Caused reward hacking |

### P&L Reward Fix
```python
# OLD (v2.5.0) - saturates quickly, destroys gradients
pnl_reward = torch.tanh(pnl * 10)  # Clips at ±1 for |pnl| > 0.1%

# NEW (v3.3.0) - linear with wider range, preserves gradients
pnl_reward = torch.clamp(pnl * 100, -2.0, 2.0)  # Linear until ±2% move
```

Why this matters:
- `tanh(pnl * 10)` reaches 0.999 at pnl=0.3% - no gradient for larger moves
- `clamp(pnl * 100, -2, 2)` preserves linear gradient until ±2% moves
- Larger moves still get proportionally larger rewards

### PPO Hyperparameters
| Parameter | v2.5.0 | v3.3.0 | Rationale |
|-----------|--------|--------|-----------|
| gamma | 0.995 | **0.991** | Shorter horizon for hourly trading |
| ent_coef | 0.005 | **0.015** | 3x increase for exploration |

## Code Location
```python
# vectorized_env.py - GPUEnvConfig dataclass (~line 479)
@dataclass
class GPUEnvConfig:
    # v3.3.0: Risk-Aware Composite Reward weights
    direction_weight: float = 0.15       # Reduced from 0.40
    magnitude_weight: float = 0.05       # Unchanged
    pnl_weight: float = 0.40             # Increased from 0.25
    exploration_weight: float = 0.15     # Unchanged
    slippage_cost_equity: float = 0.001  # Unchanged
    slippage_cost_crypto: float = 0.002  # Unchanged
    drawdown_penalty: float = 0.03       # Unchanged
    stop_tp_weight: float = 0.10         # Unchanged
    # REMOVED: trading_incentive (caused reward hacking)
```

```python
# ppo_trainer_native.py - NativePPOConfig dataclass (~line 120)
@dataclass
class NativePPOConfig:
    gamma: float = 0.991      # v3.3.0: Reduced from 0.995
    ent_coef: float = 0.015   # v3.3.0: 3x increase from 0.005
```

## Failed Attempts

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| trading_incentive = 0.02 | Created overtrading, model collected bonus constantly | Remove entirely, use proper P&L weighting |
| tanh(pnl * 10) | Gradients vanish at ±0.1%, couldn't learn from larger moves | Use linear clamp with wider range |
| direction_weight = 0.40 | Binary signal dominated continuous P&L | Reduce to 0.15, prioritize P&L |
| ent_coef = 0.005 | Insufficient exploration, model converged to local optima | 3x increase to 0.015 |
| gamma = 0.995 | Too long horizon for hourly trading decisions | Reduce to 0.991 for shorter horizon |

## Key Insights

### Trading Incentive Creates Reward Hacking
The model learned: "Any trade gives +0.02, slippage penalty is ~0.02, so trade constantly and hope for winners."
This is classic reward hacking - optimizing the surrogate (incentive) rather than the true objective (P&L).

### P&L Should Be Primary Objective
Direction is a weak proxy - being "right" about direction but wrong about magnitude loses money.
P&L directly measures what we want: profit.

### Entropy Coefficient Balances Exploration
- Too low (0.005): Model converges quickly but to local optima
- Too high (>0.05): Model explores randomly, never converges
- Sweet spot (0.015): Enough exploration to find good strategies

### Gamma Affects Time Horizon
- gamma=0.995 means 50% credit at step 139 (hourly = 6+ days)
- gamma=0.991 means 50% credit at step 77 (hourly = 3+ days)
- Shorter horizon more appropriate for hourly trading

## Related Skills
- `reward-function-hold-bias` - Historical context on HOLD bias fix
- `reward-scaling-calibration` - reward_scale=0.001 calibration
- `training-improvements-v245` - LR warmup and validation improvements
