#!/usr/bin/env python3
"""Compute range bar evaluation metrics from predictions and actuals.

Usage:
    python compute_metrics.py --predictions preds.npy --actuals actuals.npy --timestamps ts.npy
    python compute_metrics.py --results folds.jsonl --aggregate

Reference: quant-research:rangebar-eval-metrics skill

Dependencies:
    numpy>=1.24.0
    pandas>=2.0.0
    scipy>=1.10.0
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import norm, spearmanr

logger = logging.getLogger(__name__)


# =============================================================================
# Daily Aggregation (Canonical)
# =============================================================================


def _group_by_day(pnl: np.ndarray, timestamps: np.ndarray) -> np.ndarray:
    """Aggregate bar-level PnL to daily."""
    df = pd.DataFrame({"pnl": pnl, "ts": pd.to_datetime(timestamps, utc=True)})
    df["date"] = df["ts"].dt.date
    return df.groupby("date")["pnl"].sum().values


# =============================================================================
# Primary Metrics (Tier 1)
# =============================================================================


def compute_weekly_sharpe(
    pnl: np.ndarray, timestamps: np.ndarray, days_per_week: int = 7
) -> float:
    """Daily-aggregated Sharpe scaled to weekly."""
    daily_pnl = _group_by_day(pnl, timestamps)
    if len(daily_pnl) < 2:
        return 0.0
    std = np.std(daily_pnl, ddof=1)
    if std < 1e-10:
        return 0.0
    return float(np.mean(daily_pnl) / std * np.sqrt(days_per_week))


def compute_hit_rate(predictions: np.ndarray, actuals: np.ndarray) -> float:
    """Directional accuracy."""
    return float(np.mean(np.sign(predictions) == np.sign(actuals)))


def compute_cumulative_pnl(pnl: np.ndarray) -> float:
    """Total PnL."""
    return float(np.sum(pnl))


# =============================================================================
# Secondary Metrics (Tier 2)
# =============================================================================


def compute_max_drawdown(pnl: np.ndarray) -> float:
    """Maximum drawdown from cumulative PnL."""
    cumsum = np.cumsum(pnl)
    peak = np.maximum.accumulate(cumsum)
    drawdown = cumsum - peak
    return float(np.min(drawdown))


def compute_return_per_bar(pnl: np.ndarray) -> float:
    """Average return per bar."""
    if len(pnl) == 0:
        return float("nan")
    return float(np.mean(pnl))


def compute_profit_factor(
    pnl: np.ndarray, timestamps: np.ndarray, min_days: int = 5
) -> float:
    """Profit factor with daily aggregation.

    REMEDIATION (2026-01-19 audit):
    - Added min_days parameter to avoid unreliable values with too few samples.
    - Return NaN when n_days < min_days.

    Source: Multi-agent audit finding (robustness-analyst subagent)
    """
    daily_pnl = _group_by_day(pnl, timestamps)

    # REMEDIATION: Minimum sample size check
    if len(daily_pnl) < min_days:
        return float("nan")

    gains = daily_pnl[daily_pnl > 0].sum()
    losses = abs(daily_pnl[daily_pnl < 0].sum())
    if losses < 1e-10:
        return float("inf") if gains > 0 else 1.0
    return float(gains / losses)


def compute_ic(predictions: np.ndarray, actuals: np.ndarray) -> float:
    """Spearman rank IC."""
    if len(predictions) < 10:
        return float("nan")
    ic, _ = spearmanr(predictions, actuals)
    return float(ic)


def compute_prediction_autocorr(predictions: np.ndarray, lag: int = 1) -> float:
    """Lag-1 autocorrelation of predictions.

    Healthy range: 0.3 - 0.7

    WARNING signs:
    - >0.9: Predictions barely change ("sticky LSTM")
    - =1.0: Constant predictions (model collapsed to mean)
    - <0.1: Predictions are noise (no memory)

    REMEDIATION (2026-01-19 audit):
    - Return 1.0 for constant predictions (std < 1e-10)
    - NaN from corrcoef division-by-zero is incorrect semantically

    Source: Multi-agent audit finding (model-expert subagent)
    """
    if len(predictions) < lag + 2:
        return float("nan")

    # REMEDIATION: Check for constant predictions (std ≈ 0)
    if np.std(predictions) < 1e-10:
        return 1.0  # Constant predictions have perfect autocorrelation

    return float(np.corrcoef(predictions[:-lag], predictions[lag:])[0, 1])


def detect_model_collapse(
    predictions: np.ndarray, threshold: float = 1e-6
) -> dict:
    """Detect if model has collapsed to constant predictions.

    REMEDIATION (2026-01-19 audit):
    - Check prediction standard deviation
    - Log warning when detected
    - Continue recording for diagnostics

    Source: Multi-agent audit finding (model-expert subagent)
    """
    pred_std = np.std(predictions)
    is_collapsed = pred_std < threshold

    if is_collapsed:
        logger.warning(
            f"Model collapse detected: std(predictions)={pred_std:.2e}. "
            "Check architecture/hyperparameters."
        )

    return {
        "is_collapsed": is_collapsed,
        "prediction_std": float(pred_std),
        "prediction_mean": float(np.mean(predictions)),
        "prediction_range": float(np.ptp(predictions)),  # max - min
    }


# =============================================================================
# Statistical Validation (Tier 3 - Diagnostic)
# =============================================================================


def compute_sharpe_se(
    sharpe: float, n: int, skewness: float, kurtosis: float
) -> float:
    """Mertens (2002) SE with non-normality adjustment."""
    if n < 2:
        return float("nan")
    excess_kurt = kurtosis - 3.0
    variance_term = 1.0 + 0.5 * sharpe**2 - skewness * sharpe + (excess_kurt / 4.0) * sharpe**2
    if variance_term < 0:
        return float("nan")
    return float(np.sqrt(variance_term / (n - 1)))


def compute_psr(sharpe: float, se: float, benchmark: float = 0.0) -> float:
    """Probabilistic Sharpe Ratio."""
    if se <= 1e-10:
        return float("nan")
    return float(norm.cdf((sharpe - benchmark) / se))


def compute_dsr(sharpe: float, se: float, n_trials: int) -> float:
    """Deflated Sharpe Ratio."""
    if n_trials < 1 or se <= 1e-10:
        return float("nan")
    gamma = 0.5772156649
    if n_trials == 1:
        sr_expected = 0.0
    else:
        q1 = norm.ppf(1.0 - 1.0 / n_trials)
        q2 = norm.ppf(1.0 - 1.0 / (n_trials * np.e))
        sr_expected = se * ((1 - gamma) * q1 + gamma * q2)
    return float(norm.cdf((sharpe - sr_expected) / se))


# =============================================================================
# Extended Risk Metrics (Tier 5 - Optional)
# =============================================================================


def compute_var_cvar(
    pnl: np.ndarray, timestamps: np.ndarray, confidence: float = 0.95
) -> tuple[float, float]:
    """Value at Risk and Conditional VaR on daily-aggregated PnL.

    Reference: Risk Metrics Technical Document (1996)

    Args:
        pnl: Bar-level PnL
        timestamps: Bar timestamps
        confidence: Confidence level (0.95 = 95%)

    Returns:
        (VaR, CVaR) tuple - both are negative values representing loss
    """
    daily_pnl = _group_by_day(pnl, timestamps)

    if len(daily_pnl) < 5:
        return float("nan"), float("nan")

    alpha = 1 - confidence
    var = float(np.percentile(daily_pnl, alpha * 100))

    tail = daily_pnl[daily_pnl <= var]
    cvar = float(np.mean(tail)) if len(tail) > 0 else var

    return var, cvar


def compute_omega(
    pnl: np.ndarray, timestamps: np.ndarray, threshold: float = 0.0, min_days: int = 5
) -> float:
    """Omega ratio with daily aggregation.

    Omega = sum(gains above threshold) / sum(losses below threshold)

    Reference: Keating & Shadwick (2002)

    REMEDIATION (2026-01-19 audit):
    - Added min_days parameter to avoid unreliable values with too few samples.
    - Return NaN when n_days < min_days.

    Source: Multi-agent audit finding (robustness-analyst subagent)
    """
    daily_pnl = _group_by_day(pnl, timestamps)

    # REMEDIATION: Minimum sample size check
    if len(daily_pnl) < min_days:
        return float("nan")

    excess = daily_pnl - threshold
    gains = excess[excess > 0].sum()
    losses = (-excess[excess < 0]).sum()

    if losses < 1e-10:
        return float("nan")  # No losses

    return float(gains / losses)


def compute_sortino(
    pnl: np.ndarray,
    timestamps: np.ndarray,
    mar: float = 0.0,
    annualization: int = 365,
) -> float:
    """Sortino ratio using downside deviation only.

    Preferred over Sharpe for crypto (asymmetric returns).

    Reference: Sortino & Price (1994)

    Args:
        pnl: Bar-level PnL
        timestamps: Bar timestamps
        mar: Minimum Acceptable Return
        annualization: 365 for crypto, 252 for equities
    """
    daily_pnl = _group_by_day(pnl, timestamps)

    if len(daily_pnl) < 5:
        return float("nan")

    # Downside returns only
    downside = daily_pnl[daily_pnl < mar]
    if len(downside) == 0:
        return float("inf")  # No downside

    downside_std = np.std(downside, ddof=1)
    if downside_std < 1e-10:
        return float("nan")

    excess_return = np.mean(daily_pnl) - mar
    sortino = (excess_return / downside_std) * np.sqrt(annualization)

    return float(sortino)


def compute_ulcer_index(
    pnl: np.ndarray, timestamps: np.ndarray, initial_equity: float = 10000.0
) -> float:
    """Ulcer Index from equity curve.

    Ulcer = sqrt(mean(drawdown_pct^2))

    Reference: Peter Martin (1987)

    REMEDIATION (2026-01-19 audit):
    - Guard against division by zero when peak equity = 0.
    - Can happen if initial_equity + early losses < 0.

    Source: Multi-agent audit finding (risk-analyst subagent)
    """
    daily_pnl = _group_by_day(pnl, timestamps)

    if len(daily_pnl) < 2:
        return float("nan")

    # Build equity curve (NOT just cumsum)
    equity = initial_equity + np.cumsum(daily_pnl)

    # Percentage drawdowns from peak
    peak = np.maximum.accumulate(equity)

    # REMEDIATION: Guard against division by zero when peak = 0
    with np.errstate(divide="ignore", invalid="ignore"):
        drawdown_pct = np.where(peak > 1e-10, (equity - peak) / peak, 0.0)

    return float(np.sqrt((drawdown_pct**2).mean()))


def compute_calmar_ratio(
    pnl: np.ndarray, timestamps: np.ndarray, annualization: int = 365
) -> float:
    """Calmar Ratio = annualized return / max drawdown.

    Reference: Terry W. Young (1991)
    """
    daily_pnl = _group_by_day(pnl, timestamps)

    if len(daily_pnl) < 10:
        return float("nan")

    # Annualized return
    total_return = np.sum(daily_pnl)
    n_days = len(daily_pnl)
    annual_return = total_return * (annualization / n_days)

    # Max drawdown
    cumsum = np.cumsum(daily_pnl)
    peak = np.maximum.accumulate(cumsum)
    drawdown = cumsum - peak
    max_dd = abs(np.min(drawdown))

    if max_dd < 1e-10:
        return float("nan")

    return float(annual_return / max_dd)


# =============================================================================
# Full Evaluation
# =============================================================================


def evaluate_fold(
    predictions: np.ndarray,
    actuals: np.ndarray,
    timestamps: np.ndarray,
    n_trials: int = 1,
    days_per_week: int = 7,
    include_extended: bool = True,
    annualization: int = 365,
) -> dict:
    """Compute all metrics for a single fold.

    Args:
        predictions: Model predictions (signed magnitude)
        actuals: Actual returns
        timestamps: Bar close timestamps (UTC)
        n_trials: Number of strategy trials (for DSR calculation)
        days_per_week: 7 for crypto (24/7), 5 for equities
        include_extended: Whether to include extended risk metrics
        annualization: 365 for crypto, 252 for equities

    Returns:
        Dictionary with all computed metrics
    """
    pnl = predictions * actuals
    n_bars = len(pnl)

    if n_bars == 0:
        return {"error": "no_data"}

    # Primary (Tier 1)
    weekly_sharpe = compute_weekly_sharpe(pnl, timestamps, days_per_week)
    hit_rate = compute_hit_rate(predictions, actuals)
    cumulative_pnl = compute_cumulative_pnl(pnl)

    # Secondary/Risk (Tier 2)
    max_drawdown = compute_max_drawdown(pnl)
    profit_factor = compute_profit_factor(pnl, timestamps)
    bar_sharpe = float(np.mean(pnl) / np.std(pnl)) if np.std(pnl) > 0 else 0.0
    return_per_bar = compute_return_per_bar(pnl)

    # ML Quality (Tier 3)
    ic = compute_ic(predictions, actuals)
    autocorr = compute_prediction_autocorr(predictions)
    collapse_info = detect_model_collapse(predictions)

    # Statistical validation (Tier 4)
    daily_pnl = _group_by_day(pnl, timestamps)
    n_days = len(daily_pnl)
    skewness = float(stats.skew(daily_pnl)) if n_days > 2 else 0.0
    kurtosis = float(stats.kurtosis(daily_pnl) + 3) if n_days > 3 else 3.0

    sharpe_se = compute_sharpe_se(weekly_sharpe, n_days, skewness, kurtosis)
    psr = compute_psr(weekly_sharpe, sharpe_se) if not np.isnan(sharpe_se) else None
    dsr = compute_dsr(weekly_sharpe, sharpe_se, n_trials) if not np.isnan(sharpe_se) else None

    result = {
        # Primary (Tier 1)
        "weekly_sharpe": weekly_sharpe,
        "hit_rate": hit_rate,
        "cumulative_pnl": cumulative_pnl,
        "n_bars": n_bars,
        # Secondary/Risk (Tier 2)
        "max_drawdown": max_drawdown,
        "bar_sharpe": bar_sharpe,
        "return_per_bar": return_per_bar,
        "profit_factor": float(min(profit_factor, 1e6)) if not np.isnan(profit_factor) else None,
        # ML Quality (Tier 3)
        "ic": ic if not np.isnan(ic) else None,
        "prediction_autocorr": autocorr if not np.isnan(autocorr) else None,
        "is_collapsed": collapse_info["is_collapsed"],
        # Statistical validation (Tier 4)
        "sharpe_se": sharpe_se if not np.isnan(sharpe_se) else None,
        "psr": psr,
        "dsr": dsr,
        "skewness": skewness,
        "kurtosis": kurtosis,
        "n_days": n_days,
    }

    # Extended Risk (Tier 5 - Optional)
    if include_extended:
        var_95, cvar_95 = compute_var_cvar(pnl, timestamps, confidence=0.95)
        omega = compute_omega(pnl, timestamps)
        sortino = compute_sortino(pnl, timestamps, annualization=annualization)
        ulcer = compute_ulcer_index(pnl, timestamps)
        calmar = compute_calmar_ratio(pnl, timestamps, annualization=annualization)

        result.update({
            "var_95": var_95 if not np.isnan(var_95) else None,
            "cvar_95": cvar_95 if not np.isnan(cvar_95) else None,
            "omega_ratio": omega if not np.isnan(omega) else None,
            "sortino_ratio": sortino if not np.isnan(sortino) else None,
            "ulcer_index": ulcer if not np.isnan(ulcer) else None,
            "calmar_ratio": calmar if not np.isnan(calmar) else None,
        })

    return result


def compute_aggregate_metrics(fold_metrics: list[dict]) -> dict:
    """Aggregate metrics across folds.

    Computes cross-fold statistics including cv_fold_returns for stability analysis.
    """
    sharpes = [f["weekly_sharpe"] for f in fold_metrics if f.get("weekly_sharpe") is not None]
    returns = [f["cumulative_pnl"] for f in fold_metrics if f.get("cumulative_pnl") is not None]

    if not sharpes:
        return {"error": "no_valid_folds"}

    positive_rate = np.mean([s > 0 for s in sharpes])

    # Binomial test
    n_positive = sum(1 for s in sharpes if s > 0)
    n_total = len(sharpes)
    binomial_pvalue = float(1 - stats.binom.cdf(n_positive - 1, n_total, 0.5))

    # Autocorrelation of fold Sharpes
    autocorr_lag1 = float(np.corrcoef(sharpes[:-1], sharpes[1:])[0, 1]) if len(sharpes) > 2 else 0.0
    if np.isnan(autocorr_lag1):
        autocorr_lag1 = 0.0

    # Effective N (autocorrelation adjusted)
    rho = max(0, min(autocorr_lag1, 0.99))
    effective_n = n_total * (1 - rho) / (1 + rho)

    # CV of fold returns (coefficient of variation)
    # Lower is better: < 1.5 is acceptable, < 1.0 is good
    mean_return = np.mean(returns) if returns else 0.0
    std_return = np.std(returns) if returns else 0.0
    cv_fold_returns = float(std_return / abs(mean_return)) if abs(mean_return) > 1e-10 else float("nan")

    # Hit rates and ICs
    hit_rates = [f["hit_rate"] for f in fold_metrics if f.get("hit_rate") is not None]
    ics = [f["ic"] for f in fold_metrics if f.get("ic") is not None]

    # Collapse detection across folds
    collapse_count = sum(1 for f in fold_metrics if f.get("is_collapsed", False))

    return {
        # Primary aggregates
        "mean_weekly_sharpe": float(np.mean(sharpes)),
        "std_weekly_sharpe": float(np.std(sharpes)),
        "median_weekly_sharpe": float(np.median(sharpes)),
        "positive_sharpe_rate": float(positive_rate),
        "n_folds": n_total,
        # Secondary aggregates
        "total_cumulative_pnl": float(sum(returns)) if returns else 0.0,
        "cv_fold_returns": cv_fold_returns if not np.isnan(cv_fold_returns) else None,
        "mean_hit_rate": float(np.mean(hit_rates)) if hit_rates else None,
        "mean_ic": float(np.mean(ics)) if ics else None,
        # Diagnostic
        "binomial_pvalue": binomial_pvalue,
        "autocorr_lag1": autocorr_lag1,
        "effective_n": float(effective_n),
        # Model health
        "collapse_count": collapse_count,
        "collapse_rate": float(collapse_count / n_total) if n_total > 0 else 0.0,
    }


# =============================================================================
# CLI
# =============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Compute range bar evaluation metrics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single fold evaluation (crypto)
  python compute_metrics.py --predictions preds.npy --actuals actuals.npy --timestamps ts.npy

  # Single fold evaluation (equity - sqrt(5) scaling)
  python compute_metrics.py --predictions preds.npy --actuals actuals.npy --timestamps ts.npy \\
      --days-per-week 5 --annualization 252

  # Aggregate across folds
  python compute_metrics.py --results folds.jsonl --aggregate

  # Skip extended risk metrics for faster computation
  python compute_metrics.py --predictions preds.npy --actuals actuals.npy --timestamps ts.npy \\
      --no-extended

Reference: quant-research:rangebar-eval-metrics skill
        """,
    )
    parser.add_argument("--predictions", type=Path, help="Path to predictions .npy")
    parser.add_argument("--actuals", type=Path, help="Path to actuals .npy")
    parser.add_argument("--timestamps", type=Path, help="Path to timestamps .npy")
    parser.add_argument("--results", type=Path, help="Path to fold results .jsonl")
    parser.add_argument("--aggregate", action="store_true", help="Compute aggregate metrics")
    parser.add_argument("--output", type=Path, help="Output path (default: stdout)")
    parser.add_argument(
        "--days-per-week",
        type=int,
        default=7,
        choices=[5, 7],
        help="7 for crypto (24/7), 5 for equity markets",
    )
    parser.add_argument(
        "--annualization",
        type=int,
        default=365,
        choices=[252, 365],
        help="365 for crypto, 252 for equities",
    )
    parser.add_argument(
        "--no-extended",
        action="store_true",
        help="Skip extended risk metrics (VaR, Sortino, Omega, etc.)",
    )
    parser.add_argument(
        "--n-trials",
        type=int,
        default=1,
        help="Number of strategy trials for DSR calculation",
    )

    args = parser.parse_args()

    if args.results and args.aggregate:
        # Aggregate mode
        fold_metrics = []
        with open(args.results) as f:
            for line in f:
                fold_metrics.append(json.loads(line))
        result = compute_aggregate_metrics(fold_metrics)
    elif args.predictions and args.actuals and args.timestamps:
        # Single fold mode
        predictions = np.load(args.predictions)
        actuals = np.load(args.actuals)
        timestamps = np.load(args.timestamps)
        result = evaluate_fold(
            predictions,
            actuals,
            timestamps,
            n_trials=args.n_trials,
            days_per_week=args.days_per_week,
            include_extended=not args.no_extended,
            annualization=args.annualization,
        )
    else:
        parser.print_help()
        sys.exit(1)

    output = json.dumps(result, indent=2)
    if args.output:
        args.output.write_text(output)
    else:
        print(output)


if __name__ == "__main__":
    main()
