"""Basic descriptive statistics calculation module.

Computes measures of central tendency, dispersion, and distribution shape.
"""

from typing import Dict, List, Optional, Union
from dataclasses import dataclass

import pandas as pd
import numpy as np
from scipy import stats


@dataclass
class StatisticsResult:
    """Container for statistical results."""
    count: int
    mean: Optional[float]
    median: Optional[float]
    mode: Optional[float]
    std: Optional[float]
    variance: Optional[float]
    min: Optional[float]
    max: Optional[float]
    range: Optional[float]
    q1: Optional[float]
    q2: Optional[float]
    q3: Optional[float]
    iqr: Optional[float]
    skewness: Optional[float]
    kurtosis: Optional[float]
    cv: Optional[float]  # Coefficient of variation
    missing_count: int
    missing_percentage: float


def compute_basic_stats(series: pd.Series) -> Dict[str, Union[float, int]]:
    """Compute basic descriptive statistics for a numeric series.

    Args:
        series: pandas Series with numeric data

    Returns:
        Dictionary with computed statistics
    """
    # Remove NaN values for calculations
    clean_series = series.dropna()

    if len(clean_series) == 0:
        return {
            'count': 0,
            'mean': np.nan,
            'median': np.nan,
            'mode': np.nan,
            'std': np.nan,
            'variance': np.nan,
            'min': np.nan,
            'max': np.nan,
            'range': np.nan,
            'q1': np.nan,
            'q2': np.nan,
            'q3': np.nan,
            'iqr': np.nan,
            'skewness': np.nan,
            'kurtosis': np.nan,
            'cv': np.nan,
            'missing_count': series.isna().sum(),
            'missing_percentage': (series.isna().sum() / len(series) * 100) if len(series) > 0 else 0,
        }

    # Basic count
    count = len(clean_series)
    missing_count = series.isna().sum()
    missing_pct = (missing_count / len(series) * 100) if len(series) > 0 else 0

    # Central tendency
    mean = clean_series.mean()
    median = clean_series.median()

    # Mode (can be multiple, take first)
    try:
        mode_result = clean_series.mode()
        mode = mode_result.iloc[0] if len(mode_result) > 0 else np.nan
    except Exception:
        mode = np.nan

    # Dispersion
    std = clean_series.std(ddof=1)  # Sample standard deviation
    variance = clean_series.var(ddof=1)  # Sample variance
    min_val = clean_series.min()
    max_val = clean_series.max()
    data_range = max_val - min_val

    # Quantiles
    q1 = clean_series.quantile(0.25)
    q2 = clean_series.quantile(0.50)  # Same as median
    q3 = clean_series.quantile(0.75)
    iqr = q3 - q1

    # Distribution shape (using scipy for skewness and kurtosis)
    skewness = stats.skew(clean_series)
    # Fisher's kurtosis (normal = 0.0, excess kurtosis)
    kurtosis = stats.kurtosis(clean_series, fisher=True)

    # Coefficient of variation (only if mean != 0)
    cv = (std / abs(mean) * 100) if mean != 0 else np.nan

    return {
        'count': count,
        'mean': mean,
        'median': median,
        'mode': mode,
        'std': std,
        'variance': variance,
        'min': min_val,
        'max': max_val,
        'range': data_range,
        'q1': q1,
        'q2': q2,
        'q3': q3,
        'iqr': iqr,
        'skewness': skewness,
        'kurtosis': kurtosis,
        'cv': cv,
        'missing_count': missing_count,
        'missing_percentage': missing_pct,
    }


def compute_quantiles(
    series: pd.Series,
    quantiles: Optional[List[float]] = None
) -> Dict[str, float]:
    """Compute specific quantiles.

    Args:
        series: pandas Series with numeric data
        quantiles: List of quantiles to compute (0-1). Default: [0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]

    Returns:
        Dictionary mapping quantile names to values
    """
    if quantiles is None:
        quantiles = [0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]

    clean_series = series.dropna()

    if len(clean_series) == 0:
        return {f'q{int(q*100)}': np.nan for q in quantiles}

    result = {}
    for q in quantiles:
        value = clean_series.quantile(q)
        result[f'p{int(q*100)}'] = value

    return result


def compute_shape_stats(series: pd.Series) -> Dict[str, float]:
    """Compute distribution shape statistics.

    Args:
        series: pandas Series with numeric data

    Returns:
        Dictionary with shape statistics and interpretations
    """
    clean_series = series.dropna()

    if len(clean_series) < 3:
        return {
            'skewness': np.nan,
            'kurtosis': np.nan,
            'skewness_interpretation': 'Insufficient data',
            'kurtosis_interpretation': 'Insufficient data',
        }

    skewness = stats.skew(clean_series)
    kurtosis = stats.kurtosis(clean_series, fisher=True)  # Excess kurtosis

    # Interpret skewness
    if abs(skewness) < 0.5:
        skew_interp = 'Approximately symmetric'
    elif skewness >= 0.5:
        skew_interp = 'Right-skewed (positive)'
    else:
        skew_interp = 'Left-skewed (negative)'

    # Interpret kurtosis (using excess kurtosis where normal=0)
    if abs(kurtosis) < 0.5:
        kurt_interp = 'Mesokurtic (normal-like)'
    elif kurtosis > 0.5:
        kurt_interp = 'Leptokurtic (heavy-tailed, peaked)'
    else:
        kurt_interp = 'Platykurtic (light-tailed, flat)'

    return {
        'skewness': skewness,
        'kurtosis': kurtosis,
        'skewness_interpretation': skew_interp,
        'kurtosis_interpretation': kurt_interp,
    }


def compute_summary_table(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """Compute summary statistics table for multiple columns.

    Args:
        df: Input DataFrame
        columns: List of columns to analyze. If None, uses all numeric columns

    Returns:
        DataFrame with summary statistics for each column
    """
    from .data_loader import get_numeric_columns

    if columns is None:
        columns = get_numeric_columns(df)

    results = []

    for col in columns:
        if col not in df.columns:
            continue

        stats = compute_basic_stats(df[col])
        stats['column'] = col
        results.append(stats)

    if not results:
        return pd.DataFrame()

    summary_df = pd.DataFrame(results)
    summary_df = summary_df.set_index('column')

    # Reorder columns for better presentation
    column_order = [
        'count', 'missing_count', 'missing_percentage',
        'mean', 'median', 'mode',
        'std', 'variance', 'cv',
        'min', 'q1', 'q2', 'q3', 'max', 'range', 'iqr',
        'skewness', 'kurtosis'
    ]

    # Only include columns that exist
    column_order = [col for col in column_order if col in summary_df.columns]

    return summary_df[column_order]


def five_number_summary(series: pd.Series) -> Dict[str, float]:
    """Calculate the five-number summary (min, Q1, median, Q3, max).

    Args:
        series: pandas Series with numeric data

    Returns:
        Dictionary with five-number summary values
    """
    clean_series = series.dropna()

    if len(clean_series) == 0:
        return {
            'min': np.nan,
            'q1': np.nan,
            'median': np.nan,
            'q3': np.nan,
            'max': np.nan,
        }

    return {
        'min': clean_series.min(),
        'q1': clean_series.quantile(0.25),
        'median': clean_series.median(),
        'q3': clean_series.quantile(0.75),
        'max': clean_series.max(),
    }


def geometric_mean(series: pd.Series) -> float:
    """Calculate geometric mean (all values must be positive).

    Args:
        series: pandas Series with numeric data

    Returns:
        Geometric mean or NaN if invalid
    """
    clean_series = series.dropna()

    if len(clean_series) == 0:
        return np.nan

    # All values must be positive for geometric mean
    if (clean_series <= 0).any():
        return np.nan

    return stats.gmean(clean_series)


def harmonic_mean(series: pd.Series) -> float:
    """Calculate harmonic mean.

    Args:
        series: pandas Series with numeric data

    Returns:
        Harmonic mean or NaN if invalid
    """
    clean_series = series.dropna()

    if len(clean_series) == 0:
        return np.nan

    # All values must be non-zero for harmonic mean
    if (clean_series == 0).any():
        return np.nan

    return stats.hmean(clean_series)


def trimmed_mean(series: pd.Series, proportion: float = 0.1) -> float:
    """Calculate trimmed mean (removes outliers from both ends).

    Args:
        series: pandas Series with numeric data
        proportion: Proportion to trim from each end (default: 0.1 for 10%)

    Returns:
        Trimmed mean
    """
    clean_series = series.dropna()

    if len(clean_series) < 2:
        return np.nan

    # scipy trim_mean takes proportion to cut from EACH end
    # So proportion=0.1 removes 10% from bottom and 10% from top (total 20%)
    from scipy import stats as scipy_stats
    return scipy_stats.trim_mean(clean_series, proportiontocut=proportion)


def standard_error(series: pd.Series) -> float:
    """Calculate standard error of the mean.

    Args:
        series: pandas Series with numeric data

    Returns:
        Standard error or NaN if insufficient data
    """
    clean_series = series.dropna()

    if len(clean_series) < 2:
        return np.nan

    std = clean_series.std(ddof=1)
    n = len(clean_series)

    return std / np.sqrt(n)


def confidence_interval(
    series: pd.Series,
    confidence: float = 0.95
) -> Dict[str, float]:
    """Calculate confidence interval for the mean.

    Args:
        series: pandas Series with numeric data
        confidence: Confidence level (default: 0.95 for 95% CI)

    Returns:
        Dictionary with lower and upper bounds
    """
    clean_series = series.dropna()

    if len(clean_series) < 2:
        return {
            'lower': np.nan,
            'upper': np.nan,
            'confidence': confidence,
        }

    mean = clean_series.mean()
    se = standard_error(clean_series)

    # Use t-distribution for small samples
    alpha = 1 - confidence
    dof = len(clean_series) - 1
    t_critical = stats.t.ppf(1 - alpha/2, dof)

    margin_of_error = t_critical * se

    return {
        'lower': mean - margin_of_error,
        'upper': mean + margin_of_error,
        'confidence': confidence,
        'margin_of_error': margin_of_error,
    }


def outlier_boundaries(
    series: pd.Series,
    method: str = 'iqr',
    multiplier: float = 1.5
) -> Dict[str, float]:
    """Calculate boundaries for outlier detection.

    Args:
        series: pandas Series with numeric data
        method: 'iqr' or 'zscore'
        multiplier: IQR multiplier (default 1.5) or Z-score threshold (default 3.0)

    Returns:
        Dictionary with lower and upper boundaries
    """
    clean_series = series.dropna()

    if len(clean_series) == 0:
        return {
            'lower': np.nan,
            'upper': np.nan,
            'method': method,
        }

    if method == 'iqr':
        q1 = clean_series.quantile(0.25)
        q3 = clean_series.quantile(0.75)
        iqr = q3 - q1

        return {
            'lower': q1 - multiplier * iqr,
            'upper': q3 + multiplier * iqr,
            'method': method,
            'multiplier': multiplier,
            'q1': q1,
            'q3': q3,
            'iqr': iqr,
        }

    elif method == 'zscore':
        mean = clean_series.mean()
        std = clean_series.std()

        return {
            'lower': mean - multiplier * std,
            'upper': mean + multiplier * std,
            'method': method,
            'multiplier': multiplier,
            'mean': mean,
            'std': std,
        }

    else:
        raise ValueError(f"Unknown method: {method}")


def describe_df(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """Enhanced describe function with more statistics.

    Args:
        df: Input DataFrame
        columns: List of columns to describe

    Returns:
        DataFrame with comprehensive statistics
    """
    from .data_loader import get_numeric_columns

    if columns is None:
        columns = get_numeric_columns(df)

    results = []
    for col in columns:
        if col not in df.columns:
            continue

        series = df[col]
        clean_series = series.dropna()

        if len(clean_series) == 0:
            continue

        stats = {
            'Column': col,
            'Count': len(clean_series),
            'Missing': series.isna().sum(),
            'Mean': clean_series.mean(),
            'Median': clean_series.median(),
            'Std': clean_series.std(),
            'Min': clean_series.min(),
            'Q1': clean_series.quantile(0.25),
            'Q3': clean_series.quantile(0.75),
            'Max': clean_series.max(),
            'Skew': stats.skew(clean_series),
            'Kurtosis': stats.kurtosis(clean_series),
        }

        results.append(stats)

    return pd.DataFrame(results).set_index('Column')
