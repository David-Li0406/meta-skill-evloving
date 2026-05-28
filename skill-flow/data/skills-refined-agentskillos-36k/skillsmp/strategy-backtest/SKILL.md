---
name: strategy-backtest
description: Backtest a strategy and compare performance against the baseline
---

# Strategy Backtest Skill

This skill runs a full backtest on any named strategy and compares it against the default baseline.

## Usage
Invoke with: `/strategy-backtest <strategy_name> [bars]`

Examples:
- `/strategy-backtest scalp_1m_sweep`
- `/strategy-backtest scalp_1m_sweep 2000`

## Parameters
- `strategy_name` (required): Name of strategy file in `config/strategies/` (without `.json`)
- `bars` (optional): Number of bars to backtest (default: 1000)

## Steps

// turbo-all

### Step 1: Validate Strategy Exists
```powershell
$strategyPath = "config/strategies/$strategyName.json"
if (-not (Test-Path $strategyPath)) {
    Write-Error "Strategy not found: $strategyPath"
    exit 1
}
Write-Host "Strategy found: $strategyPath"
```

### Step 2: Run Baseline Backtest
Run `default` strategy first to establish baseline:
```powershell
$env:PYTHONPATH="src"; .\.venv\Scripts\python.exe -m src.laptop_agents.run --mode backtest --source mock --backtest $bars
```
Save metrics from `runs/latest/stats.json` as baseline.

### Step 3: Run Target Strategy Backtest
```powershell
$env:PYTHONPATH="src"; .\.venv\Scripts\python.exe -m src.laptop_agents.run --strategy $strategyName --mode backtest --source mock --backtest $bars
```

### Step 4: Extract Metrics
Parse `runs/latest/stats.json` for:
- `net_pnl`: Net Profit/Loss
- `max_drawdown`: Maximum Drawdown
- `trade_count`: Number of trades
- `win_rate`: Win percentage
- `sharpe_ratio`: Risk-adjusted return (if available)

### Step 5: Generate Comparison Report
Output a comparison table:

| Metric | Baseline (default) | Target ($strategyName) | Delta |
|:---|:---|:---|:---|
| Net PnL | $X | $Y | +/-$Z |
| Max Drawdown | X% | Y% | +/-Z% |
| Trade Count | N | M | +/-K |
| Win Rate | X% | Y% | +/-Z% |

### Step 6: Pass/Fail Determination
The strategy PASSES if:
- Net PnL > 0
- Max Drawdown < 10%
- Trade Count > 10

## Output Artifacts
- Comparison table printed to console
- Full results available in `runs/latest/`

## On Failure
- Report which criteria failed
- Suggest parameter adjustments if drawdown is too high
