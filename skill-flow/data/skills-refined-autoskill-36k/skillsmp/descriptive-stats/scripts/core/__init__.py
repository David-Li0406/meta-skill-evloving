"""Core analysis modules for descriptive statistics."""

from .data_loader import load_data, detect_column_types, validate_data, ColumnType
from .statistics import compute_basic_stats, compute_quantiles, compute_shape_stats
from .distribution import test_normality, histogram_data, kde_data, qqplot_data
from .outliers import detect_outliers_iqr, detect_outliers_zscore, consensus_outliers
from .group_analysis import (
    group_statistics_by_category,
    anova_test,
    kruskal_wallis_test as kruskal_test,
    compare_groups,
    group_comparison_table,
    mann_whitney_test,
    t_test_ind,
    levenes_test,
    tukey_hsd,
)

__all__ = [
    # Data loader
    'load_data',
    'detect_column_types',
    'validate_data',
    'ColumnType',
    # Statistics
    'compute_basic_stats',
    'compute_quantiles',
    'compute_shape_stats',
    # Distribution
    'test_normality',
    'histogram_data',
    'kde_data',
    'qqplot_data',
    # Outliers
    'detect_outliers_iqr',
    'detect_outliers_zscore',
    'consensus_outliers',
    # Group analysis
    'group_statistics_by_category',
    'anova_test',
    'kruskal_test',
    'compare_groups',
    'group_comparison_table',
    'mann_whitney_test',
    't_test_ind',
    'levenes_test',
    'tukey_hsd',
]
