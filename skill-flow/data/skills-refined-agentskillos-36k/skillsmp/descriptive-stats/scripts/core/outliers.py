"""Outlier detection module.

Implements multiple methods for detecting outliers in numerical data.
"""

from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass

import pandas as pd
import numpy as np
from scipy import stats


@dataclass
class OutlierResult:
    """Result of outlier detection."""
    method: str
    outlier_count: int
    outlier_indices: np.ndarray
    outlier_values: np.ndarray
    lower_bound: float
    upper_bound: float
    outlier_percentage: float
    parameters: Dict


@dataclass
class OutlierSummary:
    """Summary of outlier detection using multiple methods."""
    column_name: str
    total_count: int
    iqr_outliers: int
    zscore_outliers: int
    consensus_outliers: int
    consensus_indices: np.ndarray
    consensus_values: np.ndarray


def detect_outliers_iqr(
    series: pd.Series,
    multiplier: float = 1.5
) -> OutlierResult:
    """Detect outliers using the IQR (Interquartile Range) method.

    Outliers are values below Q1 - multiplier*IQR or above Q3 + multiplier*IQR.

    Args:
        series: pandas Series with numeric data
        multiplier: IQR multiplier (default 1.5, use 3.0 for extreme outliers)

    Returns:
        OutlierResult with detected outliers
    """
    clean_series = series.dropna()

    if len(clean_series) == 0:
        return OutlierResult(
            method='IQR',
            outlier_count=0,
            outlier_indices=np.array([]),
            outlier_values=np.array([]),
            lower_bound=np.nan,
            upper_bound=np.nan,
            outlier_percentage=0,
            parameters={'multiplier': multiplier}
        )

    q1 = clean_series.quantile(0.25)
    q3 = clean_series.quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - multiplier * iqr
    upper_bound = q3 + multiplier * iqr

    # Find outliers
    outlier_mask = (clean_series < lower_bound) | (clean_series > upper_bound)
    outlier_values = clean_series[outlier_mask]

    # Get original indices
    outlier_indices = clean_series[outlier_mask].index.values

    outlier_count = len(outlier_values)
    outlier_pct = (outlier_count / len(clean_series)) * 100

    return OutlierResult(
        method='IQR',
        outlier_count=outlier_count,
        outlier_indices=outlier_indices,
        outlier_values=outlier_values.values,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        outlier_percentage=outlier_pct,
        parameters={
            'multiplier': multiplier,
            'q1': q1,
            'q3': q3,
            'iqr': iqr
        }
    )


def detect_outliers_zscore(
    series: pd.Series,
    threshold: float = 3.0
) -> OutlierResult:
    """Detect outliers using the Z-score method.

    Outliers are values with |Z-score| > threshold.
    Z-score = (x - mean) / std

    Args:
        series: pandas Series with numeric data
        threshold: Z-score threshold (default 3.0, corresponds to ~99.7% confidence)

    Returns:
        OutlierResult with detected outliers
    """
    clean_series = series.dropna()

    if len(clean_series) == 0:
        return OutlierResult(
            method='Z-score',
            outlier_count=0,
            outlier_indices=np.array([]),
            outlier_values=np.array([]),
            lower_bound=np.nan,
            upper_bound=np.nan,
            outlier_percentage=0,
            parameters={'threshold': threshold}
        )

    mean = clean_series.mean()
    std = clean_series.std()

    if std == 0:
        # All values are the same, no outliers
        return OutlierResult(
            method='Z-score',
            outlier_count=0,
            outlier_indices=np.array([]),
            outlier_values=np.array([]),
            lower_bound=mean,
            upper_bound=mean,
            outlier_percentage=0,
            parameters={'threshold': threshold, 'mean': mean, 'std': std}
        )

    # Calculate Z-scores
    z_scores = np.abs((clean_series - mean) / std)

    # Find outliers
    outlier_mask = z_scores > threshold
    outlier_values = clean_series[outlier_mask]

    # Get original indices
    outlier_indices = clean_series[outlier_mask].index.values

    outlier_count = len(outlier_values)
    outlier_pct = (outlier_count / len(clean_series)) * 100

    lower_bound = mean - threshold * std
    upper_bound = mean + threshold * std

    return OutlierResult(
        method='Z-score',
        outlier_count=outlier_count,
        outlier_indices=outlier_indices,
        outlier_values=outlier_values.values,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        outlier_percentage=outlier_pct,
        parameters={
            'threshold': threshold,
            'mean': mean,
            'std': std
        }
    )


def detect_outliers_modified_zscore(
    series: pd.Series,
    threshold: float = 3.5
) -> OutlierResult:
    """Detect outliers using the Modified Z-score method.

    Uses median and MAD (Median Absolute Deviation) instead of mean and std.
    More robust to outliers than standard Z-score.

    Modified Z-score = 0.6745 * (x - median) / MAD

    Args:
        series: pandas Series with numeric data
        threshold: Modified Z-score threshold (default 3.5)

    Returns:
        OutlierResult with detected outliers
    """
    clean_series = series.dropna()

    if len(clean_series) == 0:
        return OutlierResult(
            method='Modified Z-score',
            outlier_count=0,
            outlier_indices=np.array([]),
            outlier_values=np.array([]),
            lower_bound=np.nan,
            upper_bound=np.nan,
            outlier_percentage=0,
            parameters={'threshold': threshold}
        )

    median = clean_series.median()
    mad = np.median(np.abs(clean_series - median))

    if mad == 0:
        # All values are the same, no outliers
        return OutlierResult(
            method='Modified Z-score',
            outlier_count=0,
            outlier_indices=np.array([]),
            outlier_values=np.array([]),
            lower_bound=median,
            upper_bound=median,
            outlier_percentage=0,
            parameters={'threshold': threshold, 'median': median, 'mad': mad}
        )

    # Calculate modified Z-scores
    modified_z_scores = np.abs(0.6745 * (clean_series - median) / mad)

    # Find outliers
    outlier_mask = modified_z_scores > threshold
    outlier_values = clean_series[outlier_mask]

    # Get original indices
    outlier_indices = clean_series[outlier_mask].index.values

    outlier_count = len(outlier_values)
    outlier_pct = (outlier_count / len(clean_series)) * 100

    # Calculate approximate bounds
    lower_bound = median - (threshold / 0.6745) * mad
    upper_bound = median + (threshold / 0.6745) * mad

    return OutlierResult(
        method='Modified Z-score',
        outlier_count=outlier_count,
        outlier_indices=outlier_indices,
        outlier_values=outlier_values.values,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        outlier_percentage=outlier_pct,
        parameters={
            'threshold': threshold,
            'median': median,
            'mad': mad
        }
    )


def consensus_outliers(
    series: pd.Series,
    methods: Optional[List[str]] = None,
    iqr_multiplier: float = 1.5,
    zscore_threshold: float = 3.0,
    require_all: bool = False
) -> OutlierResult:
    """Detect outliers using consensus of multiple methods.

    By default, uses both IQR and Z-score methods and returns outliers
    detected by at least one method. Set require_all=True to only
    return outliers detected by all methods.

    Args:
        series: pandas Series with numeric data
        methods: List of methods to use ('iqr', 'zscore', 'modified_zscore')
                 Default: ['iqr', 'zscore']
        iqr_multiplier: Multiplier for IQR method
        zscore_threshold: Threshold for Z-score methods
        require_all: If True, outlier must be detected by ALL methods
                     If False, outlier detected by ANY method

    Returns:
        OutlierResult with consensus outliers
    """
    clean_series = series.dropna()

    if len(clean_series) == 0:
        return OutlierResult(
            method='Consensus',
            outlier_count=0,
            outlier_indices=np.array([]),
            outlier_values=np.array([]),
            lower_bound=np.nan,
            upper_bound=np.nan,
            outlier_percentage=0,
            parameters={
                'methods': methods,
                'require_all': require_all
            }
        )

    if methods is None:
        methods = ['iqr', 'zscore']

    # Run selected methods
    results = {}
    for method in methods:
        if method == 'iqr':
            results['iqr'] = detect_outliers_iqr(series, multiplier=iqr_multiplier)
        elif method == 'zscore':
            results['zscore'] = detect_outliers_zscore(series, threshold=zscore_threshold)
        elif method == 'modified_zscore':
            results['modified_zscore'] = detect_outliers_modified_zscore(
                series, threshold=zscore_threshold
            )

    if not results:
        return OutlierResult(
            method='Consensus',
            outlier_count=0,
            outlier_indices=np.array([]),
            outlier_values=np.array([]),
            lower_bound=np.nan,
            upper_bound=np.nan,
            outlier_percentage=0,
            parameters={'methods': methods, 'error': 'No valid methods provided'}
        )

    # Collect outlier indices
    all_indices = set()
    method_indices = {method: set(result.outlier_indices) for method, result in results.items()}

    if require_all:
        # Outlier must be detected by ALL methods
        if len(method_indices) > 0:
            consensus_indices = set.intersection(*method_indices.values())
        else:
            consensus_indices = set()
    else:
        # Outlier detected by ANY method
        for indices in method_indices.values():
            all_indices.update(indices)
        consensus_indices = all_indices

    if not consensus_indices:
        return OutlierResult(
            method='Consensus',
            outlier_count=0,
            outlier_indices=np.array([]),
            outlier_values=np.array([]),
            lower_bound=np.nan,
            upper_bound=np.nan,
            outlier_percentage=0,
            parameters={
                'methods': list(results.keys()),
                'require_all': require_all,
                'individual_results': {
                    method: {
                        'count': result.outlier_count,
                        'percentage': result.outlier_percentage
                    }
                    for method, result in results.items()
                }
            }
        )

    # Get outlier values
    consensus_indices_list = sorted(consensus_indices)
    outlier_values = clean_series.loc[consensus_indices_list].values

    outlier_count = len(consensus_indices)
    outlier_pct = (outlier_count / len(clean_series)) * 100

    # Use bounds from the most conservative method
    lower_bounds = [r.lower_bound for r in results.values() if not np.isnan(r.lower_bound)]
    upper_bounds = [r.upper_bound for r in results.values() if not np.isnan(r.upper_bound)]

    lower_bound = min(lower_bounds) if lower_bounds else np.nan
    upper_bound = max(upper_bounds) if upper_bounds else np.nan

    return OutlierResult(
        method='Consensus',
        outlier_count=outlier_count,
        outlier_indices=np.array(consensus_indices_list),
        outlier_values=outlier_values,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        outlier_percentage=outlier_pct,
        parameters={
            'methods': list(results.keys()),
            'require_all': require_all,
            'individual_results': {
                method: {
                    'count': result.outlier_count,
                    'percentage': result.outlier_percentage
                }
                for method, result in results.items()
            }
        }
    )


def outlier_summary(
    series: pd.Series,
    column_name: str = 'value'
) -> OutlierSummary:
    """Generate a comprehensive outlier summary using multiple methods.

    Args:
        series: pandas Series with numeric data
        column_name: Name of the column for the summary

    Returns:
        OutlierSummary with comprehensive outlier information
    """
    clean_series = series.dropna()
    total_count = len(clean_series)

    # Detect outliers using different methods
    iqr_result = detect_outliers_iqr(series, multiplier=1.5)
    zscore_result = detect_outliers_zscore(series, threshold=3.0)
    consensus_result = consensus_outliers(
        series,
        methods=['iqr', 'zscore'],
        require_all=False
    )

    return OutlierSummary(
        column_name=column_name,
        total_count=total_count,
        iqr_outliers=iqr_result.outlier_count,
        zscore_outliers=zscore_result.outlier_count,
        consensus_outliers=consensus_result.outlier_count,
        consensus_indices=consensus_result.outlier_indices,
        consensus_values=consensus_result.outlier_values
    )


def flag_outliers(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    method: str = 'iqr',
    **method_params
) -> pd.DataFrame:
    """Flag outliers in a DataFrame by adding boolean outlier columns.

    Args:
        df: Input DataFrame
        columns: List of columns to check for outliers
        method: Outlier detection method ('iqr', 'zscore', 'modified_zscore', 'consensus')
        **method_params: Parameters for the outlier detection method

    Returns:
        DataFrame with added outlier flag columns (named '{col}_is_outlier')
    """
    result_df = df.copy()

    if columns is None:
        from .data_loader import get_numeric_columns
        columns = get_numeric_columns(df)

    for col in columns:
        if col not in df.columns:
            continue

        series = df[col]

        if method == 'iqr':
            outlier_result = detect_outliers_iqr(series, **method_params)
        elif method == 'zscore':
            outlier_result = detect_outliers_zscore(series, **method_params)
        elif method == 'modified_zscore':
            outlier_result = detect_outliers_modified_zscore(series, **method_params)
        elif method == 'consensus':
            outlier_result = consensus_outliers(series, **method_params)
        else:
            raise ValueError(f"Unknown method: {method}")

        # Add outlier flag column
        flag_col = f'{col}_is_outlier'
        result_df[flag_col] = False
        result_df.loc[outlier_result.outlier_indices, flag_col] = True

    return result_df


def remove_outliers(
    series: pd.Series,
    method: str = 'iqr',
    **method_params
) -> pd.Series:
    """Remove outliers from a series.

    Args:
        series: pandas Series with numeric data
        method: Outlier detection method ('iqr', 'zscore', 'modified_zscore', 'consensus')
        **method_params: Parameters for the outlier detection method

    Returns:
        Series with outliers removed
    """
    if method == 'iqr':
        outlier_result = detect_outliers_iqr(series, **method_params)
    elif method == 'zscore':
        outlier_result = detect_outliers_zscore(series, **method_params)
    elif method == 'modified_zscore':
        outlier_result = detect_outliers_modified_zscore(series, **method_params)
    elif method == 'consensus':
        outlier_result = consensus_outliers(series, **method_params)
    else:
        raise ValueError(f"Unknown method: {method}")

    # Return series without outliers
    return series.drop(outlier_result.outlier_indices)


def winsorize(
    series: pd.Series,
    limits: Tuple[float, float] = (0.05, 0.05)
) -> pd.Series:
    """Winsorize data by replacing extreme values with less extreme values.

    Instead of removing outliers, replaces them with the value at the
    specified percentile.

    Args:
        series: pandas Series with numeric data
        limits: Tuple of (lower_limit, upper_limit) as proportions
                e.g., (0.05, 0.05) replaces bottom 5% and top 5%

    Returns:
        Series with winsorized values
    """
    from scipy.stats.mstats import winsorize as scipy_winsorize

    clean_series = series.dropna()

    if len(clean_series) == 0:
        return series

    winsorized_values = scipy_winsorize(clean_series, limits=limits)

    result = series.copy()
    result[clean_series.index] = winsorized_values

    return result
