---
name: execute-trade
description: Skill for executing confirmed trades with pre-flight checks, confirmation mesh validation, and post-execution logging.
---

# Execute Trade Skill

Handles the full trade execution lifecycle with multi-layer safety validation.

## Capabilities

This skill enables the agent to:
1. Validate trade signals through confirmation mesh
2. Check L2 liquidity before execution
3. Route orders to appropriate broker adapters
4. Log execution results and update positions
5. Handle failures with circuit breaker logic

## Prerequisites

- Confirmed signal from orderflow-analysis skill
- Broker adapter configured (Alpaca, Zerodha, Upstox)
- Risk parameters defined (max position size, max slippage)

## Procedural Steps

### 1. Pre-Flight Liquidity Check

Before any execution request:
```
Call: estimate_slippage(symbol: str, side: "buy" | "sell", quantity: float)
Returns: (avg_price: float, slippage_pct: float) or None if insufficient liquidity
```

### 2. Confirmation Mesh Validation

Submit signal through validation pipeline:
```
Call: validate_execution(
    signal: FootprintSignal,
    symbol: str,
    side: "buy" | "sell", 
    quantity: float,
    max_slippage_pct: float = 0.5
) -> ConfirmationResult
```

The mesh validates:
- Footprint pattern confirmation
- L2 liquidity sufficiency
- Risk management rules
- Circuit breaker status

### 3. Execute if Approved

Only if `result.approved == True`:
```
Call: execute_order(
    symbol: str,
    side: "buy" | "sell",
    quantity: float,
    order_type: "market" | "limit",
    limit_price: float | None,
    broker: "alpaca" | "zerodha" | "upstox" | "paper"
) -> ExecutionResult
```

### 4. Post-Execution Logging

After execution:
```
Call: log_execution(
    execution_result: ExecutionResult,
    signal: FootprintSignal,
    confirmation: ConfirmationResult
)
```

This updates:
- Position ledger
- Trade history
- Performance metrics
- Alert notifications

## Safety Guardrails

> [!CAUTION]
> These rules are NON-NEGOTIABLE for autonomous execution:

1. **Never bypass confirmation mesh** - All trades must pass validation
2. **Respect circuit breakers** - If tripped, halt all execution for symbol
3. **Verify tick-by-tick data** - Cross-reference 3 data sources before execution
4. **Max position limits** - Never exceed configured max_position_size
5. **Slippage protection** - Abort if estimated slippage > max_slippage_pct

## Risk Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| max_position_size | 10,000 | Max shares per position |
| max_notional_value | $100,000 | Max $ value per trade |
| max_slippage_pct | 0.5% | Abort if exceeds |
| min_liquidity_ratio | 2x | Need 2x quantity in book |
| circuit_breaker_cooldown | 5 min | Time after trip |

## Execution Modes

### Paper Trading (Safe)
```
execute_order(..., broker="paper")
```
Uses simulated broker with realistic slippage/commission modeling.

### Live Trading (Requires Confirmation)
```
execute_order(..., broker="alpaca")  # or zerodha, upstox
```
Routes to real broker API. Agent must log confidence justification.

## Example Complete Flow

```python
# 1. Receive confirmed signal from orderflow analysis
signal = await analyze_footprint("RELIANCE", 60)

# 2. Pre-flight check
slippage = await estimate_slippage("RELIANCE", "buy", 500)
if slippage and slippage[1] > 0.5:
    logger.warning("Slippage too high, aborting")
    return

# 3. Confirmation mesh
confirmation = await validate_execution(
    signal=signal,
    symbol="RELIANCE",
    side="buy",
    quantity=500,
    max_slippage_pct=0.5
)

# 4. Execute only if approved
if confirmation.approved:
    result = await execute_order(
        symbol="RELIANCE",
        side="buy",
        quantity=500,
        order_type="limit",
        limit_price=confirmation.recommended_price,
        broker="zerodha"
    )
    
    # 5. Log execution
    await log_execution(result, signal, confirmation)
else:
    logger.warning(f"Rejected: {confirmation.rejection_reason}")
```

## Failure Recovery

If execution fails:
1. Log failure with full context
2. Increment consecutive failure counter
3. If counter >= 5, trip circuit breaker for symbol
4. Alert via configured notification channels (Telegram/Email)
5. Wait for manual review or cooldown expiry
