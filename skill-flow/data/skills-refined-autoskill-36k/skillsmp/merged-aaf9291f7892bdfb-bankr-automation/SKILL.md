---
name: bankr-automation
description: Use this skill when you need to create and manage automated trading orders, including limit orders, stop losses, DCA, and TWAP strategies.
---

# Bankr Automation

Set up and manage automated trading orders and strategies using natural language prompts.

## Order Types

### Limit Orders
Execute trades at a specified price:
- "Set a limit order to buy `<token>` at `<price>`"
- "Limit order: sell `<token>` when it hits `<target_price>`"

### Stop Loss Orders
Automatically sell to limit losses:
- "Set stop loss for my `<token>` at `<price>`"
- "Stop loss: sell `<token>` if it drops `<percent>`"

### DCA (Dollar Cost Averaging)
Invest fixed amounts at regular intervals:
- "DCA `<amount>` into `<token>` every `<frequency>`"
- "DCA `<amount>` into `<token>` every `<frequency>` for `<duration>`"

### TWAP (Time-Weighted Average Price)
Spread large orders over time:
- "TWAP buy `<amount>` of `<token>` over `<duration>`"
- "TWAP sell `<amount>` of `<token>` over `<duration>`"

### Scheduled Commands
Run any Bankr command on a schedule:
- "Every `<frequency>`, check my portfolio"
- "At `<time>`, buy `<amount>` of `<token>`"

## Managing Automations

**View:**
- "Show my automations"
- "What limit orders do I have?"

**Cancel:**
- "Cancel automation `<id>`"
- "Cancel all my automations"

## Supported Chains

- **EVM Chains** (Base, Polygon, Ethereum): All order types supported
- **Solana**: Uses Jupiter Trigger API for limit orders, stop loss, and DCA

## Common Issues

| Issue | Resolution |
|-------|------------|
| Order not triggering | Check price threshold |
| Insufficient balance | Ensure funds available when order executes |
| Order cancelled | May expire or conflict with other orders |

## Tips

1. Start small - test with small amounts first.
2. Set alerts - get notified on execution.
3. Review regularly - update orders as market changes.
4. Combine strategies - DCA + stop loss works well.
5. Factor in fees - consider per-transaction costs for DCA.

## Usage Example

```typescript
import { execute } from "./bankr-client";

// Create limit order
await execute("Set a limit order to buy $500 of ETH at $3,000");

// Create DCA
await execute("DCA $100 into ETH every week for 3 months");

// Create TWAP
await execute("TWAP buy $5000 of ETH over 24 hours");

// View automations
await execute("Show my automations");
```

## Related Skills

- `bankr-client-patterns` - Client setup and execute function
- `bankr-api-basics` - API fundamentals
- `bankr-token-trading` - Immediate trades