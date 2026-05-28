# Casino Math Balancer

Expert skill for calculating and balancing casino game mathematics.

## Expertise

This skill provides deep knowledge in:

- **Probability Theory**: Expected values, variance, standard deviation
- **RTP Calculations**: Return-to-player percentages for various game types
- **House Edge Design**: Balancing profitability with player satisfaction
- **Volatility Tuning**: High/medium/low variance game design
- **Payout Tables**: Creating mathematically sound reward structures
- **Meta-Pot Systems**: Multi-tier progressive jackpot math

## When to Use

Invoke this skill when you need to:

- Design betting mechanics for a game
- Calculate odds and probabilities
- Balance RTP across multiple game features
- Create payout tables that feel fair but remain profitable
- Validate game economy math
- Design progressive/meta-pot systems

## Key Concepts

### RTP (Return to Player)

```
RTP = (Total Returns to Players / Total Bets) × 100

Example: 96% RTP means players get back $96 for every $100 wagered
```

### House Edge

```
House Edge = 100% - RTP

Example: 4% house edge on 96% RTP game
```

### Volatility

| Level | Description | Hit Frequency | Max Win |
|-------|-------------|---------------|---------|
| Low | Frequent small wins | High | Low |
| Medium | Balanced | Medium | Medium |
| High | Rare big wins | Low | High |

## Example Calculations

### Simple Slot Math

```
Symbols: Cherry, Lemon, Seven
Reels: 3 reels, 10 stops each
Total combinations: 10 × 10 × 10 = 1,000

Cherry-Cherry-Cherry: 2/10 × 2/10 × 2/10 = 0.008 (0.8%)
Payout: 50x

Contribution to RTP: 0.008 × 50 = 0.40 (40%)
```

### Meta-Pot Progressive

```
Base Game RTP: 92%
Meta-Pot Contribution: 4%
Progressive Seed: 2%
Total RTP: 98%

House Edge: 2%
```

## Integration

This skill works alongside:

- `game-concept-advisor` - For mechanic ideation
- `fun-advisor` - To ensure math doesn't hurt fun
- `game-systems-doc` - For documenting final math

## Usage in Claude Code

```
/casino-math-balancer

"Calculate RTP for a 5-reel slot with these symbol frequencies..."
"Design a meta-pot system with 3 tiers..."
"What house edge balances profitability with player retention?"
```
