"""Distribution analysis module.

Performs normality tests and prepares data for distribution visualization.
"""

from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass

import pandas as pd
import numpy as np
from scipy import stats


@dataclass
class NormalityTestResult:
    """Result of a normality test."""
    test_name: str
    statistic: float
    p_value: float
    is_normal: bool
    alpha: float = 0.05
    interpretation: str = ""


@dataclass
class HistogramData:
    """Data for histogram visualization."""
    counts: np.ndarray
    bin_edges: np.ndarray
    bin_centers: np.ndarray
    bin_width: float
    density: bool


@dataclass
class KDEData:
    """Data for kernel density estimation visualization."""
    x: np.ndarray
    y: np.ndarray
    bandwidth: float


@dataclass
class QQPlotData:
    """Data for Q-Q plot visualization."""
    theoretical: np.ndarray
    actual: np.ndarray
    slope: float
    intercept: float
    r_squared: float


def test_normality(
    series: pd.Series,
    alpha: float = 0.05
) -> Dict[str, NormalityTestResult]:
    """Perform multiple normality tests on a series.

    Args:
        series: pandas Series with numeric data
        alpha: Significance level (default: 0.05)

    Returns:
        Dictionary with test results for different normality tests
    """
    clean_series = series.dropna()
    n = len(clean_series)

    results = {}

    if n < 3:
        # Not enough data for any test
        results['shapiro'] = NormalityTestResult(
            test_name='Shapiro-Wilk',
            statistic=np.nan,
            p_value=np.nan,
            is_normal=False,
            alpha=alpha,
            interpretation='Insufficient data (need at least 3 values)'
        )
        return results

    # Shapiro-Wilk test (recommended for n < 5000)
    if n < 5000:
        try:
            stat, p_value = stats.shapiro(clean_series)
            is_normal = p_value > alpha

            if is_normal:
                interp = f'Normal distribution (p={p_value:.4f} > {alpha})'
            else:
                interp = f'Not normal (p={p_value:.4f} <= {alpha})'

            results['shapiro'] = NormalityTestResult(
                test_name='Shapiro-Wilk',
                statistic=stat,
                p_value=p_value,
                is_normal=is_normal,
                alpha=alpha,
                interpretation=interp
            )
        except Exception as e:
            results['shapiro'] = NormalityTestResult(
                test_name='Shapiro-Wilk',
                statistic=np.nan,
                p_value=np.nan,
                is_normal=False,
                alpha=alpha,
                interpretation=f'Test failed: {str(e)}'
            )
    else:
        results['shapiro'] = NormalityTestResult(
            test_name='Shapiro-Wilk',
            statistic=np.nan,
            p_value=np.nan,
            is_normal=False,
            alpha=alpha,
            interpretation=f'Sample size too large (n={n} > 5000)'
        )

    # Kolmogorov-Smirnov test (good for large samples)
    if n >= 50:
        try:
            # Compare to normal distribution with same mean and std
            stat, p_value = stats.kstest(
                clean_series,
                'norm',
                args=(clean_series.mean(), clean_series.std())
            )
            is_normal = p_value > alpha

            if is_normal:
                interp = f'Normal distribution (p={p_value:.4f} > {alpha})'
            else:
                interp = f'Not normal (p={p_value:.4f} <= {alpha})'

            results['ks'] = NormalityTestResult(
                test_name='Kolmogorov-Smirnov',
                statistic=stat,
                p_value=p_value,
                is_normal=is_normal,
                alpha=alpha,
                interpretation=interp
            )
        except Exception as e:
            results['ks'] = NormalityTestResult(
                test_name='Kolmogorov-Smirnov',
                statistic=np.nan,
                p_value=np.nan,
                is_normal=False,
                alpha=alpha,
                interpretation=f'Test failed: {str(e)}'
            )

    # Anderson-Darling test (more sensitive to tails)
    if n >= 8:
        try:
            result = stats.anderson(clean_series, dist='norm')

            # Compare to critical values
            # Use 5% significance level
            critical_value = result.critical_values[2]  # 5% level
            stat = result.statistic

            is_normal = stat < critical_value

            if is_normal:
                interp = f'Normal distribution (stat={stat:.4f} < {critical_value:.4f})'
            else:
                interp = f'Not normal (stat={stat:.4f} >= {critical_value:.4f})'

            results['anderson'] = NormalityTestResult(
                test_name='Anderson-Darling',
                statistic=stat,
                p_value=np.nan,  # Anderson-Darling doesn't give p-value directly
                is_normal=is_normal,
                alpha=alpha,
                interpretation=interp
            )
        except Exception as e:
            results['anderson'] = NormalityTestResult(
                test_name='Anderson-Darling',
                statistic=np.nan,
                p_value=np.nan,
                is_normal=False,
                alpha=alpha,
                interpretation=f'Test failed: {str(e)}'
            )

    # D'Agostino's K2 test (tests skewness and kurtosis)
    if n >= 20:
        try:
            stat, p_value = stats.normaltest(clean_series)
            is_normal = p_value > alpha

            if is_normal:
                interp = f'Normal distribution (p={p_value:.4f} > {alpha})'
            else:
                interp = f'Not normal (p={p_value:.4f} <= {alpha})'

            results['dagostino'] = NormalityTestResult(
                test_name="D'Agostino's K²",
                statistic=stat,
                p_value=p_value,
                is_normal=is_normal,
                alpha=alpha,
                interpretation=interp
            )
        except Exception as e:
            results['dagostino'] = NormalityTestResult(
                test_name="D'Agostino's K²",
                statistic=np.nan,
                p_value=np.nan,
                is_normal=False,
                alpha=alpha,
                interpretation=f'Test failed: {str(e)}'
            )

    return results


def histogram_data(
    series: pd.Series,
    bins: Union[int, str] = 'auto',
    density: bool = False
) -> HistogramData:
    """Calculate histogram data.

    Args:
        series: pandas Series with numeric data
        bins: Number of bins or binning strategy ('auto', 'fd', 'doane', 'scott', 'stone', 'rice', 'sturges', 'sqrt')
        density: If True, compute probability density

    Returns:
        HistogramData with counts, bin edges, and bin centers
    """
    clean_series = series.dropna()

    if len(clean_series) == 0:
        return HistogramData(
            counts=np.array([]),
            bin_edges=np.array([]),
            bin_centers=np.array([]),
            bin_width=0,
            density=density
        )

    counts, bin_edges = np.histogram(clean_series, bins=bins, density=density)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    bin_width = bin_edges[1] - bin_edges[0] if len(bin_edges) > 1 else 0

    return HistogramData(
        counts=counts,
        bin_edges=bin_edges,
        bin_centers=bin_centers,
        bin_width=bin_width,
        density=density
    )


def kde_data(
    series: pd.Series,
    bandwidth: str = 'scott',
    grid_points: int = 500
) -> KDEData:
    """Calculate kernel density estimation data.

    Args:
        series: pandas Series with numeric data
        bandwidth: Bandwidth selection method ('scott', 'silverman', or scalar)
        grid_points: Number of points in the grid

    Returns:
        KDEData with x and y coordinates for plotting
    """
    from scipy.stats import gaussian_kde

    clean_series = series.dropna()

    if len(clean_series) == 0:
        return KDEData(
            x=np.array([]),
            y=np.array([]),
            bandwidth=0
        )

    if len(clean_series) < 2:
        # Need at least 2 points for KDE
        return KDEData(
            x=clean_series.values,
            y=np.ones(len(clean_series)),
            bandwidth=0
        )

    try:
        kde = gaussian_kde(clean_series, bw_method=bandwidth)

        # Create a grid for evaluation
        x_min = clean_series.min()
        x_max = clean_series.max()
        padding = (x_max - x_min) * 0.1
        x = np.linspace(x_min - padding, x_max + padding, grid_points)

        y = kde(x)

        return KDEData(
            x=x,
            y=y,
            bandwidth=kde.factor
        )
    except Exception as e:
        # Fallback if KDE fails
        return KDEData(
            x=np.array([]),
            y=np.array([]),
            bandwidth=0
        )


def qqplot_data(
    series: pd.Series,
    distribution: str = 'norm'
) -> QQPlotData:
    """Calculate Q-Q plot data.

    Args:
        series: pandas Series with numeric data
        distribution: Theoretical distribution ('norm', 'uniform', etc.)

    Returns:
        QQPlotData with theoretical and actual quantiles
    """
    clean_series = series.dropna()

    if len(clean_series) == 0:
        return QQPlotData(
            theoretical=np.array([]),
            actual=np.array([]),
            slope=0,
            intercept=0,
            r_squared=0
        )

    # Sort the data
    sorted_data = np.sort(clean_series)

    # Calculate theoretical quantiles
    n = len(sorted_data)
    theoretical_quantiles = stats.norm.ppf((np.arange(n) + 0.5) / n)

    # Fit a line through the data (using robust method)
    # Use Q1 and Q3 points for robustness
    q1_idx = int(n * 0.25)
    q3_idx = int(n * 0.75)

    x1, y1 = theoretical_quantiles[q1_idx], sorted_data[q1_idx]
    x2, y2 = theoretical_quantiles[q3_idx], sorted_data[q3_idx]

    slope = (y2 - y1) / (x2 - x1) if x2 != x1 else 1
    intercept = y1 - slope * x1

    # Calculate R-squared
    if len(theoretical_quantiles) > 2:
        correlation = np.corrcoef(theoretical_quantiles, sorted_data)[0, 1]
        r_squared = correlation ** 2
    else:
        r_squared = 0

    return QQPlotData(
        theoretical=theoretical_quantiles,
        actual=sorted_data,
        slope=slope,
        intercept=intercept,
        r_squared=r_squared
    )


def optimal_bins(
    series: pd.Series,
    method: str = 'fd'
) -> int:
    """Calculate optimal number of histogram bins using various methods.

    Args:
        series: pandas Series with numeric data
        method: Binning method ('fd', 'doane', 'scott', 'stone', 'rice', 'sturges', 'sqrt', 'auto')

    Returns:
        Optimal number of bins
    """
    clean_series = series.dropna()
    n = len(clean_series)

    if n == 0:
        return 10

    data_range = clean_series.max() - clean_series.min()

    if data_range == 0:
        return 1

    if method == 'sturges':
        # Sturges' rule
        bins = int(np.ceil(np.log2(n)) + 1)

    elif method == 'fd':
        # Freedman-Diaconis rule
        q75 = clean_series.quantile(0.75)
        q25 = clean_series.quantile(0.25)
        iqr = q75 - q25
        bin_width = 2 * iqr / (n ** (1/3))
        bins = int(np.ceil(data_range / bin_width)) if bin_width > 0 else 10

    elif method == 'scott':
        # Scott's rule
        std = clean_series.std()
        bin_width = 3.5 * std / (n ** (1/3))
        bins = int(np.ceil(data_range / bin_width)) if bin_width > 0 else 10

    elif method == 'doane':
        # Doane's formula (for non-normal data)
        from .statistics import compute_shape_stats
        shape_stats = compute_shape_stats(series)
        g1 = shape_stats['skewness']

        if np.isnan(g1) or g1 == 0:
            # Fall back to Sturges if skewness is 0 or NaN
            bins = int(np.ceil(np.log2(n)) + 1)
        else:
            sigma_g1 = np.sqrt(6 * (n - 2) / ((n + 1) * (n + 3)))
            bins = int(np.ceil(1 + np.log2(n) + np.log2(1 + abs(g1) / sigma_g1)))

    elif method == 'rice':
        # Rice rule
        bins = int(np.ceil(2 * (n ** (1/3))))

    elif method == 'sqrt':
        # Square-root rule
        bins = int(np.ceil(np.sqrt(n)))

    elif method == 'auto':
        # Use matplotlib's default (maximum of Sturges and FD)
        bins_sturges = int(np.ceil(np.log2(n)) + 1)
        q75 = clean_series.quantile(0.75)
        q25 = clean_series.quantile(0.25)
        iqr = q75 - q25
        bin_width_fd = 2 * iqr / (n ** (1/3))
        bins_fd = int(np.ceil(data_range / bin_width_fd)) if bin_width_fd > 0 else 10
        bins = max(bins_sturges, bins_fd)

    else:
        # Default to Sturges
        bins = int(np.ceil(np.log2(n)) + 1)

    # Ensure reasonable bounds
    bins = max(1, min(bins, 200))

    return bins


def distribution_summary(
    series: pd.Series,
    alpha: float = 0.05
) -> Dict:
    """Get a comprehensive distribution analysis summary.

    Args:
        series: pandas Series with numeric data
        alpha: Significance level for normality tests

    Returns:
        Dictionary with distribution analysis results
    """
    from .statistics import compute_shape_stats

    clean_series = series.dropna()
    n = len(clean_series)

    # Normality tests
    normality_results = test_normality(series, alpha=alpha)

    # Shape statistics
    shape_stats = compute_shape_stats(series)

    # Optimal bins
    bins_fd = optimal_bins(series, method='fd')
    bins_sturges = optimal_bins(series, method='sturges')

    # Consensus on normality
    normal_tests = [r for r in normality_results.values() if not np.isnan(r.p_value)]
    if normal_tests:
        normal_count = sum(1 for r in normal_tests if r.is_normal)
        consensus = normal_count == len(normal_tests)
    else:
        consensus = False

    return {
        'sample_size': n,
        'normality_tests': {k: {
            'statistic': v.statistic,
            'p_value': v.p_value,
            'is_normal': v.is_normal,
            'interpretation': v.interpretation
        } for k, v in normality_results.items()},
        'shape_stats': shape_stats,
        'bins_recommendation': {
            'freedman_diaconis': bins_fd,
            'sturges': bins_sturges,
        },
        'is_normal': consensus,
    }


def empirical_cdf(series: pd.Series) -> Tuple[np.ndarray, np.ndarray]:
    """Calculate empirical cumulative distribution function.

    Args:
        series: pandas Series with numeric data

    Returns:
        Tuple of (sorted values, cumulative probabilities)
    """
    clean_series = series.dropna()

    if len(clean_series) == 0:
        return np.array([]), np.array([])

    sorted_values = np.sort(clean_series)
    n = len(sorted_values)
    cumulative_prob = (np.arange(n) + 1) / n

    return sorted_values, cumulative_prob


def percentiles(
    series: pd.Series,
    percentiles: Optional[List[float]] = None
) -> Dict[str, float]:
    """Calculate specific percentiles.

    Args:
        series: pandas Series with numeric data
        percentiles: List of percentiles to calculate (0-100). Default: [1, 5, 10, 25, 50, 75, 90, 95, 99]

    Returns:
        Dictionary mapping percentile names to values
    """
    if percentiles is None:
        percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]

    clean_series = series.dropna()

    if len(clean_series) == 0:
        return {f'p{p}': np.nan for p in percentiles}

    result = {}
    for p in percentiles:
        value = clean_series.quantile(p / 100)
        result[f'p{p}'] = value

    return result
