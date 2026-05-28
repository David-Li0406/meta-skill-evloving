---
name: empirical-config-builder
description: "Derive selection thresholds from market data instead of hardcoding. Trigger when: (1) reviewing hardcoded parameters, (2) volume/price thresholds seem arbitrary, (3) selection returns too many/few candidates."
author: Claude Code
date: 2026-01-08
---

# Empirical Config Builder - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2026-01-08 |
| **Goal** | Replace hardcoded selection thresholds with data-driven values |
| **Environment** | Python 3.10+, SymbolDatabase, numpy |
| **Status** | Success |

## Context

Universe selection had many hardcoded "magic numbers":
- `MIN_VOLUME_USD_EQUITY = 1_000_000` - why $1M?
- `MIN_PRICE_EQUITY = 5.0` - why $5?
- `SECTOR_TOP_PCT = 0.30` - why 30%?

These values were originally guessed and never validated against actual market data. The empirical config builder derives these from the SymbolDatabase using percentiles.

## Parameters Analysis

### Can Be Data-Driven (6 parameters)

| Parameter | Derivation Method | Code |
|-----------|-------------------|------|
| min_volume_equity | P50 of daily volume | `volume_pct[50]` |
| min_price | P5 of equity prices | `price_pct[5]` |
| max_price | P99 of equity prices | `price_pct[99]` |
| sector_top_pct | `target_candidates / equities_passing_volume` | Calculated |
| min_per_sector | `median_sector_size / 10` | Calculated |
| max_per_sector | `median_sector_size` | Calculated |

### Should Stay Hardcoded (Theory-Based)

| Parameter | Value | Why Fixed |
|-----------|-------|-----------|
| hurst_short_target | (0.30, 0.50) | Literature: H<0.5 = mean-reverting |
| hurst_long_target | (0.50, 0.70) | Literature: H>0.5 = trending |
| half_life_target_hours | (4, 24) | Trading frequency constraint |
| regime_duration_target | (5, 20) | Markov model requirement |
| scoring weights | Sum to 1.0 | Design decision |

## Verified Workflow

### 1. Basic Usage (Notebook)

```python
# In training notebook cell-14:
USE_EMPIRICAL_THRESHOLDS = True   # Enable empirical mode
TARGET_CANDIDATES = 1500          # Target candidate count

# Thresholds are automatically derived in cell-16
```

### 2. Programmatic Usage

```python
from alpaca_trading.selection import SymbolDatabase
from alpaca_trading.selection.empirical_config import build_config_from_database

db = SymbolDatabase(db_path='data/symbol_database.db')
result = build_config_from_database(
    db=db,
    target_candidates=1500,       # How many candidates you want
    volume_percentile=50,         # P50 = median (top 50% by volume)
    price_percentile_low=5,       # Exclude bottom 5% (penny stocks)
    price_percentile_high=99,     # Exclude top 1% (too expensive)
)

# Use the derived config
config = result.config

# See what was derived
print(result.describe())
# Output:
# ======================================================================
# EMPIRICAL CONFIGURATION (derived from market data)
# ======================================================================
#
# DERIVED THRESHOLDS:
#   min_volume_equity             : $180,432  [P50 of equity volume]
#   min_price                     : 1.25  [P5 of equity price]
#   max_price                     : 892.50  [P99 of equity price]
#   sector_top_pct                : 41.67%  [calculated for 1500 target candidates]
#   min_per_sector                : 45  [median_sector_size / 10]
#   max_per_sector                : 450  [median_sector_size]
```

### 3. With Correlation Estimation (Advanced)

```python
from alpaca_trading.selection.empirical_config import build_full_empirical_config

result = build_full_empirical_config(
    db=db,
    data_fetcher=fetcher,         # Required for correlation
    target_candidates=1500,
    estimate_correlations=True,   # Compute actual correlations
)

# max_correlation is now derived from P75 of pairwise correlations
print(f"max_correlation: {result.config.max_correlation:.2f}")
```

## Output Structure

```python
@dataclass
class EmpiricalConfigResult:
    config: SelectionConfig       # Ready-to-use config
    thresholds: Dict[str, Any]    # All derived values
    derivation_method: Dict[str, str]  # How each was derived
    data_summary: Dict[str, Any]  # Market stats used
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Fetching snapshots directly | Redundant API calls when DB exists | Use SymbolDatabase |
| Fixed percentiles for all | Different markets need different P values | Crypto uses P25 for volume |
| Using mean instead of median | Outliers skew mean significantly | Always use median (P50) |
| Deriving Hurst targets | Theory-based, not market-dependent | Keep as hardcoded |
| Same min_per_sector everywhere | Small sectors need protection | Use median_sector_size / 10 |

## Key Insights

1. **Volume percentile choice matters:**
   - P25: Very inclusive (~7000 candidates)
   - P50: Balanced (~3600 candidates)
   - P75: Selective (~1800 candidates)

2. **Price percentiles:**
   - P5 excludes penny stocks without guessing "$5"
   - P99 excludes extremely expensive stocks naturally

3. **Sector filtering auto-calculation:**
   - `sector_top_pct = target_candidates / equities_passing_volume`
   - Clamped to [0.15, 0.50] to prevent extremes
   - min/max per sector derived from actual sector sizes

4. **Correlation threshold:**
   - P75 of pairwise correlations is a reasonable threshold
   - Computing this requires historical data (expensive)
   - Optional - default 0.60 is usually fine

## Files Modified

| File | Changes |
|------|---------|
| `alpaca_trading/selection/empirical_config.py` | Added `build_config_from_database()`, `EmpiricalConfigResult` |
| `notebooks/training.ipynb` | Added `USE_EMPIRICAL_THRESHOLDS` option |
| `CLAUDE.md` | Added empirical config documentation |

## Typical Results

| Parameter | Hardcoded | Empirical (P50) |
|-----------|-----------|-----------------|
| min_volume_equity | $1,000,000 | $180,432 |
| min_price | $5.00 | $1.25 |
| max_price | $10,000 | $892.50 |
| sector_top_pct | 30% | 42% |

**Observation:** Hardcoded values were MORE restrictive than P50 (median). This explains why selection sometimes returned fewer candidates than expected.

## References

- Skill: `symbol-database-selection` - SymbolDatabase infrastructure
- Skill: `per-sector-candidate-filtering` - Sector filtering parameters
- Skill: `symbol-selection-statistical` - Statistical selection theory
