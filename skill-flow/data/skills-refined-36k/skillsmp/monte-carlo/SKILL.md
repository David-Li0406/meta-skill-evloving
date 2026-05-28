---
name: monte-carlo
description: Run Monte Carlo simulations on a trading strategy to verify robustness.
---

# Monte Carlo Simulation Skill

This skill runs a Monte Carlo simulation on a specific strategy using the `scripts/monte_carlo_v1.py` script. It validates the statistical robustness of a strategy by repeatedly sampling trade returns.

## Usage
Invoke with: `/monte-carlo <strategy_name> [limit] [iterations] [source]`

Examples:
- `/monte-carlo scalp_1m_sweep_optimized` (Default: 1000 bars, 1000 iterations, bitunix source)
- `/monte-carlo scalp_1m_sweep_optimized 5000` (5000 bars)
- `/monte-carlo scalp_1m_sweep_optimized 2000 5000 mock` (2000 bars, 5000 iters, mock data)

## Parameters
- `strategy_name` (required): Name of the strategy file in `config/strategies/` (without .json extension).
- `limit` (optional): Number of bars to backtest before simulation (Default: 1000).
- `iterations` (optional): Number of Monte Carlo iterations (Default: 1000).
- `source` (optional): Data source, 'bitunix' or 'mock' (Default: bitunix).

## Prerequisites
- The script `scripts/monte_carlo_v1.py` must exist.
- Python env must be set up.

## Steps

// turbo-all

### Step 1: Validate Script and Strategy
Ensure the tool and strategy exist.
```powershell
$scriptPath = "scripts/monte_carlo_v1.py"
$stratPath = "config/strategies/$strategyName.json"

if (-not (Test-Path $scriptPath)) {
    Write-Error "Monte Carlo script not found at $scriptPath"
    exit 1
}
if (-not (Test-Path $stratPath)) {
    Write-Error "Strategy not found at $stratPath"
    exit 1
}
Write-Host "Ready to simulate $strategyName using $scriptPath"
```

### Step 2: Run Simulation
Execute the python script.
- Defaults are applied if arguments are missing.
- `$limit` defaults to 1000 if not provided.
- `$iterations` defaults to 1000 if not provided.
- `$source` defaults to "bitunix" if not provided.

```powershell
# Set defaults if variables are null/empty
if (-not $limit) { $limit = 1000 }
if (-not $iterations) { $iterations = 1000 }
if (-not $source) { $source = "bitunix" }

Write-Host "Running Monte Carlo: Strategy=$strategyName, Source=$source, Limit=$limit, Iterations=$iterations"

$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe scripts/monte_carlo_v1.py --strategy $strategyName --limit $limit --iterations $iterations --source $source
```

### Step 3: Interpret Results
The script will output a table.
- **Pass Criteria**:
  - `Prob. of >20% DD` should be **0.00%**.
  - `95% Max Drawdown` should be acceptable for your risk tolerance (e.g., < 20%).
  - `50% Percentile` (Median) Equity should be > Starting Balance for a profitable strategy.

## On Failure
- If `Prob. of >20% DD` is high (> 0%), the strategy is too risky.
- If Median Equity is < Start, the strategy has negative expectancy.
