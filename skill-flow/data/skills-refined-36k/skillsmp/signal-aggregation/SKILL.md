---
name: signal-aggregation
description: Skill for aggregating signals from orderflow, scanner, and AI brain into unified trade recommendations.
---

# Signal Aggregation Skill

Combines signals from multiple sources into confidence-weighted trade recommendations.

## Capabilities

This skill enables the agent to:
1. Aggregate signals from orderflow (L2/footprint patterns)
2. Include technical scanner signals (RSI, MACD, moving averages)
3. Incorporate AI brain analysis (entry analysis, risk assessment)
4. Execute trades based on unified signal strength

## Signal Sources

| Source | Data | Weight |
|--------|------|--------|
| **Orderflow** | L2 imbalance, bid/ask walls | High |
| **Scanner** | RSI, MACD, SMA crossovers | Medium |
| **Brain** | Entry confidence, position sizing | High |

## Procedural Steps

### 1. Request Unified Signal

```
Call: get_aggregated_signal(symbol: str, account_size?: float)
Endpoint: POST http://localhost:8011/signal
```

### 2. Interpret Signal Strength

| Strength | Confidence | Action |
|----------|------------|--------|
| **STRONG** | >80% | Execute immediately |
| **MODERATE** | 50-80% | Consider with caution |
| **WEAK** | <50% | Wait for better setup |

### 3. Execute (if Strong Signal)

```
Call: execute_aggregated_signal(symbol: str)
Endpoint: POST http://localhost:8011/execute
```

This automatically:
- Gets unified signal
- Validates through confirmation mesh
- Routes to broker if approved

## Example Workflow

```python
# Get unified signal for AAPL
signal = await get_signal({
    "symbol": "AAPL",
    "include_orderflow": True,
    "include_scanner": True,
    "include_brain": True,
    "account_size": 100000
})

# Check strength
if signal.strength == "STRONG" and signal.confidence > 0.8:
    # Execute with confidence
    result = await execute("/execute", {
        "symbol": "AAPL",
        "account_size": 100000
    })
else:
    # Wait for better setup
    log(f"Signal too weak: {signal.strength}, {signal.confidence}")
```

## Safety Guardrails

- Never execute WEAK signals
- Always include orderflow for real-time context
- Verify all sources agree on direction before STRONG signal
- Use suggested_quantity from brain's position sizing
