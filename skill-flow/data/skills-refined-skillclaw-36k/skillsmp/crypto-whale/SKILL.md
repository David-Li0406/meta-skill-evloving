---
name: crypto-whale
description: Track whale (large holder) activity and institutional movements.
argument-hint: [asset] [timeframe]
allowed-tools:
  - mcp__plugin_cryptoquant_cryptoquant__initialize
  - mcp__plugin_cryptoquant_cryptoquant__query_data
  - mcp__plugin_cryptoquant_cryptoquant__discover_endpoints
---

# /crypto-whale Command

Monitor large holder (whale) movements using on-chain data.

## Usage

```
/crypto-whale              # BTC, 24 hours
/crypto-whale btc          # BTC, 24 hours
/crypto-whale eth 7d       # ETH, 7 days
```

## Workflow

```
1. Ensure session initialized

2. Discover available endpoints:
   - discover_endpoints(asset, category="flow-indicator", query="whale")
   - discover_endpoints(asset, category="exchange-flows")

3. Query available metrics:
   Professional:
   - Whale Ratio: /v1/{asset}/flow-indicator/exchange-whale-ratio
   - Fund Flow Ratio: /v1/{asset}/flow-indicator/fund-flow-ratio

   Free:
   - Netflow: /v1/{asset}/exchange-flows/netflow
   - Inflow: /v1/{asset}/exchange-flows/inflow
   - Outflow: /v1/{asset}/exchange-flows/outflow

4. If Pro metrics unavailable:
   - Use derived ratio: inflow_top10 / inflow_total

5. Interpret and generate report
```

## Metrics

### Whale Ratio (Professional)
| Value | Status |
|-------|--------|
| < 0.3 | Retail dominated |
| 0.3 - 0.5 | Mixed |
| 0.5 - 0.7 | Whale heavy |
| > 0.85 | Extreme (manipulation risk) |

### Combined Signal
| Whale Ratio | Netflow | Signal |
|-------------|---------|--------|
| > 0.5 | Negative | Whale accumulation (bullish) |
| > 0.5 | Positive | Whale distribution (bearish) |
| < 0.3 | Negative | Retail accumulation |
| < 0.3 | Positive | Retail panic selling |

## Output Format

### Full (Professional)

```
## Whale Activity: BTC (24h)

Whale Ratio: 0.58 (Whale Heavy)
Retail: 42% | Whales: 58%

| Metric | Value |
|--------|-------|
| Inflow | 12,450 BTC |
| Outflow | 15,200 BTC |
| Net | -2,750 BTC |

Behavior: Whales accumulating (outflow dominant)
Signal: Bullish
```

### Limited (Basic/Free)

```
## Whale Activity: BTC (Basic Plan)

| Metric | Value |
|--------|-------|
| Inflow | 12,450 BTC |
| Outflow | 15,200 BTC |
| Net | -2,750 BTC |

Derived Ratio: 0.52 (Top 10 = 52% of inflow)
Estimated: Large holder accumulation

Upgrade for full whale metrics: cryptoquant.com/pricing
```

## Warning Patterns

- Whale Ratio > 0.85 + Positive Netflow = Distribution warning
- Sudden large inflow spike = Potential dump

## Reference

- Main skill: [/crypto](../crypto/SKILL.md)
- Interpretation guide: [INTERPRETATION.md](../crypto/INTERPRETATION.md)
