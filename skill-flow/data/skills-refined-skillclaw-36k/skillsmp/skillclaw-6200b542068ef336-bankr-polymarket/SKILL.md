---
name: bankr-polymarket
description: Use this skill when you want to interact with Polymarket prediction markets, including searching for markets, checking odds, placing bets, and managing your positions.
---

# Polymarket Capability

Interact with Polymarket prediction markets via natural language prompts.

## What You Can Do

| Operation | Example Prompt |
|-----------|----------------|
| Search markets | `Search Polymarket for election` |
| Trending markets | `What prediction markets are trending?` |
| Check odds | `What are the odds Trump wins?` |
| Market details | `Show details for the Super Bowl market` |
| Bet Yes | `Bet $10 on Yes for the election market` |
| Bet No | `Bet $5 on No for Bitcoin hitting 100k` |
| View positions | `Show my Polymarket positions` |
| Redeem winnings | `Redeem my Polymarket positions` |

## How Betting Works

- You buy shares of "Yes" or "No" outcomes.
- Share price reflects market probability (e.g., $0.60 = 60% chance).
- If your outcome wins, shares pay $1 each.
- Profit = $1 - purchase price (per share).

**Example**: Bet $10 on "Yes" at $0.60 = ~16.67 shares. If Yes wins, get $16.67 (profit $6.67).

## Auto-Bridging

If you don't have USDC on Polygon, Bankr automatically bridges from another chain.

## Common Issues

| Issue | Resolution |
|-------|------------|
| Market not found | Try different search terms |
| Insufficient USDC | Add USDC or let auto-bridge |
| Market closed | Can't bet on resolved markets |

## Prompt Patterns

```
Search Polymarket for {query}
What are the odds {event}?
Bet {amount} on {Yes|No} for {market}
Show my Polymarket positions
Redeem my Polymarket positions
```

## Usage

```typescript
import { execute } from "./bankr-client";

// Check odds
await execute("What are the odds Trump wins the election?");

// Place a bet
await execute("Bet $10 on Yes for Presidential Election 2024");

// View positions
await execute("Show my Polymarket positions");
```

## Tips

- Search and check odds before betting.
- Start with small amounts to test.
- Check market liquidity for best prices.
- Redeem promptly after markets resolve.

## Related Skills

- `bankr-client-patterns` - Client setup and execute function
- `bankr-api-basics` - API fundamentals
- `bankr-portfolio` - Check USDC balance for betting