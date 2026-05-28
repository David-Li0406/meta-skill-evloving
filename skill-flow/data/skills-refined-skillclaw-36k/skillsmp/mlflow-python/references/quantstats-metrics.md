**Skill**: [MLflow Python](../SKILL.md)

# QuantStats Metrics Reference

Complete list of 70+ trading metrics available via QuantStats integration.

## Metrics Logged by log_backtest.py

The `log_backtest.py` script calculates and logs these metrics:

### Core Ratios

| Metric          | Function             | Description                          |
| --------------- | -------------------- | ------------------------------------ |
| `sharpe_ratio`  | `qs.stats.sharpe()`  | Risk-adjusted return (vs risk-free)  |
| `sortino_ratio` | `qs.stats.sortino()` | Downside risk-adjusted return        |
| `calmar_ratio`  | `qs.stats.calmar()`  | Return vs max drawdown               |
| `omega_ratio`   | `qs.stats.omega()`   | Probability-weighted gain/loss ratio |

### Returns Metrics

| Metric         | Function                | Description                 |
| -------------- | ----------------------- | --------------------------- |
| `cagr`         | `qs.stats.cagr()`       | Compound Annual Growth Rate |
| `total_return` | `qs.stats.comp()`       | Total cumulative return     |
| `avg_return`   | `qs.stats.avg_return()` | Average daily return        |
| `avg_win`      | `qs.stats.avg_win()`    | Average winning day return  |
| `avg_loss`     | `qs.stats.avg_loss()`   | Average losing day return   |
| `best_day`     | `qs.stats.best()`       | Best single day return      |
| `worst_day`    | `qs.stats.worst()`      | Worst single day return     |

### Drawdown Metrics

| Metric              | Function                       | Description                    |
| ------------------- | ------------------------------ | ------------------------------ |
| `max_drawdown`      | `qs.stats.max_drawdown()`      | Maximum peak-to-trough decline |
| `avg_drawdown`      | `qs.stats.avg_drawdown()`      | Average drawdown               |
| `avg_drawdown_days` | `qs.stats.avg_drawdown_days()` | Average days in drawdown       |

### Trade Metrics

| Metric               | Function                        | Description                  |
| -------------------- | ------------------------------- | ---------------------------- |
| `win_rate`           | `qs.stats.win_rate()`           | Percentage of winning days   |
| `profit_factor`      | `qs.stats.profit_factor()`      | Gross profit / gross loss    |
| `payoff_ratio`       | `qs.stats.payoff_ratio()`       | Avg win / avg loss           |
| `consecutive_wins`   | `qs.stats.consecutive_wins()`   | Max consecutive winning days |
| `consecutive_losses` | `qs.stats.consecutive_losses()` | Max consecutive losing days  |

### Risk Metrics

| Metric        | Function                 | Description                          |
| ------------- | ------------------------ | ------------------------------------ |
| `volatility`  | `qs.stats.volatility()`  | Annualized standard deviation        |
| `var`         | `qs.stats.var()`         | Value at Risk (95%)                  |
| `cvar`        | `qs.stats.cvar()`        | Conditional VaR (Expected Shortfall) |
| `ulcer_index` | `qs.stats.ulcer_index()` | Ulcer Index (drawdown stress)        |

### Advanced Metrics

| Metric               | Function                        | Description                          |
| -------------------- | ------------------------------- | ------------------------------------ |
| `kelly_criterion`    | `qs.stats.kelly_criterion()`    | Optimal bet size                     |
| `recovery_factor`    | `qs.stats.recovery_factor()`    | Return / max drawdown                |
| `risk_of_ruin`       | `qs.stats.risk_of_ruin()`       | Probability of total loss            |
| `tail_ratio`         | `qs.stats.tail_ratio()`         | Right tail / left tail               |
| `common_sense_ratio` | `qs.stats.common_sense_ratio()` | Profit factor × tail ratio           |
| `cpc_index`          | `qs.stats.cpc_index()`          | Gain ratio × win rate × payoff ratio |
| `outlier_win_ratio`  | `qs.stats.outlier_win_ratio()`  | Outlier wins vs normal wins          |
| `outlier_loss_ratio` | `qs.stats.outlier_loss_ratio()` | Outlier losses vs normal losses      |

### Distribution Metrics

| Metric     | Function              | Description                        |
| ---------- | --------------------- | ---------------------------------- |
| `skew`     | `qs.stats.skew()`     | Return distribution asymmetry      |
| `kurtosis` | `qs.stats.kurtosis()` | Return distribution tail thickness |

## Additional QuantStats Functions

These are available but not logged by default:

```python
# Benchmark comparison
qs.stats.information_ratio(returns, benchmark)
qs.stats.treynor_ratio(returns, benchmark)
qs.stats.alpha(returns, benchmark)
qs.stats.beta(returns, benchmark)
qs.stats.r_squared(returns, benchmark)

# Rolling metrics
qs.stats.rolling_sharpe(returns, window=252)
qs.stats.rolling_sortino(returns, window=252)
qs.stats.rolling_volatility(returns, window=252)

# Monthly/yearly aggregations
qs.stats.monthly_returns(returns)
qs.stats.yearly_returns(returns)
```

## Interpreting Key Metrics

| Metric          | Good Value | Excellent Value | Notes                          |
| --------------- | ---------- | --------------- | ------------------------------ |
| Sharpe Ratio    | > 1.0      | > 2.0           | Risk-adjusted, annualized      |
| Sortino Ratio   | > 1.5      | > 3.0           | Only penalizes downside        |
| Max Drawdown    | < -20%     | < -10%          | Lower (less negative) = better |
| Win Rate        | > 50%      | > 60%           | Combined with payoff ratio     |
| Profit Factor   | > 1.5      | > 2.0           | Must be > 1.0 to profit        |
| Kelly Criterion | 0.1 - 0.3  | -               | Optimal allocation %           |
