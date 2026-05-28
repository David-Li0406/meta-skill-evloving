---
name: analyze
description: Analyze a trading strategy's backtest results and provide improvement suggestions. Use when asked to analyze, review, or improve a strategy.
---

# Analyze Strategy

Analyze the current strategy's backtest results and provide actionable improvement suggestions.

## Instructions

### Step 1: Find the Strategy

List available strategies:
```bash
ls ~/.tradery/strategies/
```

If user specified a strategy, use that. Otherwise, find the most recently modified:
```bash
ls -t ~/.tradery/strategies/*/summary.json | head -1
```

### Step 2: Read Summary

Read the summary.json for quick overview:
```
~/.tradery/strategies/{strategyId}/summary.json
```

Key fields to examine:
- `metrics` - Overall performance (winRate, sharpeRatio, maxDrawdownPercent, etc.)
- `analysis.byPhase` - Performance breakdown by market phase
- `analysis.byHour` - Performance by hour of day (UTC)
- `analysis.byDayOfWeek` - Performance by day of week
- `analysis.suggestions` - Pre-computed suggestions

### Step 3: Analyze Trade Files

Browse trade filenames for patterns:
```bash
ls ~/.tradery/strategies/{strategyId}/trades/
```

Count outcomes:
```bash
ls ~/.tradery/strategies/{strategyId}/trades/ | grep -c "_WIN_"
ls ~/.tradery/strategies/{strategyId}/trades/ | grep -c "_LOSS_"
ls ~/.tradery/strategies/{strategyId}/trades/ | grep -c "_REJECTED"
```

### Step 4: Sample Problem Trades

Read 3-5 of the biggest losses to understand failure modes:
```bash
ls ~/.tradery/strategies/{strategyId}/trades/*_LOSS_* | sort -t_ -k4 -r | head -5
```

Then read those specific trade files to understand:
- What phases were active?
- What was the MFE before the loss? (was it ever profitable?)
- What was the exit reason?

### Step 5: Read Strategy Config

Read the strategy to understand current settings:
```
~/.tradery/strategies/{strategyId}/strategy.json
```

### Step 6: Provide Analysis

Structure your response as:

**Performance Summary**
- Key metrics in plain English
- Overall assessment (strong/weak/average)

**What's Working**
- Phases/times with above-average performance
- Good patterns identified

**What Needs Improvement**
- Phases/times with below-average performance
- Common failure patterns from losing trades

**Specific Recommendations**
For each recommendation, provide:
1. What to change (plain English)
2. Why it should help (based on data)
3. The exact JSON edit to make

Example:
```
Recommendation: Add "uptrend" as a required phase

Why: Trades during uptrend have 72% win rate vs 55% overall (based on 28 trades)

Edit strategy.json:
{
  "phaseSettings": {
    "requiredPhaseIds": ["uptrend"],  // Add this
    ...
  }
}
```

## Output Format

Always end with a summary table:

| Metric | Current | Potential |
|--------|---------|-----------|
| Win Rate | 55% | ~65% (if filtering by uptrend) |
| Sharpe | 1.2 | ~1.5 |

And ask: "Would you like me to apply any of these changes?"

## Notes

- Focus on actionable changes, not general advice
- Back every recommendation with data from the analysis
- Consider phase filters, time filters, and exit adjustments
- Don't suggest adding complexity unless data supports it
- The app auto-reloads when strategy.json is edited
