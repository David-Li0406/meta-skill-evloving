---
name: crypto
description: |
  On-chain analytics for Bitcoin, Ethereum, and crypto markets.
  Triggers: bitcoin outlook, price analysis, market valuation, overvalued, undervalued,
  whale activity, exchange flows, trading signal, MVRV, SOPR, NVT, funding rate,
  market cycle, bull market, bear market, on-chain analysis, smart money.
allowed-tools:
  - mcp__plugin_cryptoquant_cryptoquant__initialize
  - mcp__plugin_cryptoquant_cryptoquant__query_data
  - mcp__plugin_cryptoquant_cryptoquant__discover_endpoints
  - mcp__plugin_cryptoquant_cryptoquant__describe_metric
  - mcp__plugin_cryptoquant_cryptoquant__list_assets
  - mcp__plugin_cryptoquant_cryptoquant__get_endpoint_info
---

# CryptoQuant On-Chain Analytics

Access CryptoQuant's on-chain data for cryptocurrency market analysis.

## Response Language

**Always respond in the same language as the user's prompt.** If the user asks in Korean, respond in Korean. If in English, respond in English.

---

## Quick Start

```
/crypto                   # Initialize session (run first!)
/crypto-market            # Quick market summary
/crypto-signal btc        # Get buy/sell/hold signal
/crypto-whale             # Track whale activity
```

---

## Session Initialization

**MUST run `/crypto` before any data request.**

```
/crypto
    ↓
┌─────────────────────────────────────┐
│ Check for API key:                  │
│ 1. Environment variable             │
│ 2. Stored credentials               │
│    (~/.cryptoquant/credentials)     │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ No key found?                       │
│ → Browser opens automatically       │
│ → User enters API key               │
│ → Key saved locally                 │
└─────────────────────────────────────┘
    ↓
Authenticated → Shows plan/permissions
```

---

## Available Commands

| Command | Description |
|---------|-------------|
| `/crypto` | Initialize session, show status |
| `/crypto-market [asset]` | Quick 30-second market summary |
| `/crypto-signal [asset]` | Buy/Sell/Hold trading signal |
| `/crypto-whale [asset]` | Whale activity tracker |

---

## Available Agents

| Agent | Trigger | Description |
|-------|---------|-------------|
| `market-analyst` | "full analysis", "market report" | Comprehensive multi-metric analysis |
| `whale-tracker` | "whale tracking", "smart money" | Deep whale movement monitoring |

---

## Intent-to-Metric Quick Reference

| User Question | Intent | Primary Metric | Free? |
|---------------|--------|----------------|-------|
| "Is BTC overvalued?" | VALUATION | mvrv | Yes |
| "Network utility vs price?" | NETWORK_VALUATION | nvt | Yes |
| "Profit taking happening?" | PROFIT_BEHAVIOR | sopr | Yes |
| "Exchange accumulation?" | EXCHANGE_FLOWS | netflow | Yes |
| "Coins on exchanges?" | EXCHANGE_RESERVE | reserve | Yes |
| "Whale activity?" | WHALE_ACTIVITY | whale-ratio | No |
| "Funding rate?" | LEVERAGE_SENTIMENT | funding-rates | No |
| "Open positions?" | OPEN_INTEREST | open-interest | No |
| "Old coins moving?" | COIN_AGE | cdd | Yes |
| "HODL behavior?" | HODL_BEHAVIOR | mean-coin-age | Yes |
| "Stablecoin buying power?" | STABLECOIN_LIQUIDITY | ssr | No |
| "Miners selling?" | MINER_ACTIVITY | mpi | No |
| "Miner profitability?" | MINER_PROFITABILITY | puell-multiple | Yes |
| "US institutional buying?" | COINBASE_PREMIUM | coinbase-premium | No |
| "Korean retail FOMO?" | KIMCHI_PREMIUM | korea-premium | No |
| "ETF inflows?" | ETF_FLOWS | etf-netflow | No |
| "Bull or bear market?" | MARKET_CYCLE | mvrv + sopr | Partial |

See [INTENT_MAP.md](INTENT_MAP.md) for full routing details.

---

## Interpretation Quick Reference

### Valuation Metrics

| Metric | 🟢 Bullish | 🟡 Neutral | 🔴 Bearish |
|--------|------------|------------|------------|
| MVRV | < 1.5 | 1.5 - 2.5 | > 3.5 |
| NVT | < 50 | 50 - 90 | > 120 |
| Puell | < 0.5 | 0.5 - 1.0 | > 2.0 |

### Behavior Metrics

| Metric | 🟢 Bullish | 🟡 Neutral | 🔴 Bearish |
|--------|------------|------------|------------|
| SOPR | < 0.95 (capitulation) | 0.95 - 1.05 | > 1.10 |
| CDD | Baseline | Normal | Major spike |
| MCA | Rising | Stable | Declining |

### Flow Metrics

| Metric | 🟢 Bullish | 🟡 Neutral | 🔴 Bearish |
|--------|------------|------------|------------|
| Netflow | < -1,000 BTC | ±1,000 | > +5,000 BTC |
| Reserve | Decreasing | Stable | Increasing |
| Whale Ratio | < 0.3 | 0.3 - 0.5 | > 0.7 |

### Derivatives Metrics

| Metric | 🟢 Bullish | 🟡 Neutral | 🔴 Bearish |
|--------|------------|------------|------------|
| Funding | < -0.01% | ±0.01% | > 0.05% |
| OI + Price | Both rising | Mixed | OI up, Price down |

### Miner & Liquidity

| Metric | 🟢 Bullish | 🟡 Neutral | 🔴 Bearish |
|--------|------------|------------|------------|
| MPI | < 0.5 | 0.5 - 1.0 | > 2.0 |
| SSR | < 10 | 10 - 20 | > 20 |

### Premium & ETF Metrics

| Metric | 🟢 Bullish | 🟡 Neutral | 🔴 Bearish |
|--------|------------|------------|------------|
| Coinbase Premium | > +$20 | ±$20 | < -$100 |
| Kimchi Premium | < -2% | ±2% | > +10% (FOMO) |
| ETF Netflow | > +$100M/day | ±$100M | < -$500M/day |

See [INTERPRETATION.md](INTERPRETATION.md) for detailed thresholds and definitions.

---

## MCP Tools Reference

### Authentication
| Tool | Description |
|------|-------------|
| `initialize()` | **MUST CALL FIRST** - Initialize session |
| `reset_session(clear_stored?)` | Clear session/credentials |

### Data Access
| Tool | Description |
|------|-------------|
| `list_assets()` | List supported assets (btc, eth) |
| `discover_endpoints(asset?, category?)` | Find available endpoints |
| `query_data(endpoint, params)` | Query raw data |
| `describe_metric(metric_id)` | Get metric description |

### Typical Workflow
```
1. initialize()              # Authenticate
2. INTENT_MAP.md 참조        # Get EXACT endpoint path & required params
3. query_data()              # Query with correct path and params
4. Interpret using INTERPRETATION.md
```

**CRITICAL**: Do NOT guess endpoint paths. Always check INTENT_MAP.md for:
- Exact endpoint path (e.g., `/v1/btc/market-indicator/sopr`, NOT `network-indicator`)
- Required parameters (e.g., `exchange` for netflow)

---

## Plan Information

| Plan | Data Range | Key Features |
|------|------------|--------------|
| Premium | Unlimited | All metrics, real-time |
| Professional | 3 years | Most metrics |
| Basic | Limited | Core metrics only |

### Free vs Professional Metrics

**Free Plan (Basic)**:
- MVRV, NVT, SOPR, Puell Multiple
- Netflow, Reserve, Inflow, Outflow
- CDD, Mean Coin Age

**Professional Plan Required**:
- Whale Ratio, Fund Flow Ratio
- Funding Rates, Open Interest
- SSR, MPI, NUPL
- aSOPR, STH-SOPR, LTH-SOPR

---

## Error Handling

### Not Initialized
```
Run /crypto first to connect.
Get API key at: https://cryptoquant.com/settings/api
```

### Access Denied
```
[Metric] requires [Plan] plan.
Your plan: [Current]
Alternative: [Free metric suggestion]
```

---

## Reference Files

- **Intent routing**: [INTENT_MAP.md](INTENT_MAP.md)
- **Value interpretation**: [INTERPRETATION.md](INTERPRETATION.md)
