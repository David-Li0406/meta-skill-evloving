"""Group comparison analysis module.

Performs statistical analysis for comparing groups, including ANOVA and non-parametric tests.
"""

from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum

import pandas as pd
import numpy as np
from scipy import stats


class TestType(Enum):
    """Types of statistical tests for group comparison."""
    ANOVA = "anova"  # Parametric test for normal distributions
    KRUSKAL = "kruskal"  # Non-parametric test
    MANN_WHITNEY = "mann_whitney"  # Two groups, non-parametric
    T_TEST = "t_test"  # Two groups, parametric
    LEVENE = "levene"  # Test for equal variances
    BARTLETT = "bartlett"  # Test for equal variances (requires normality)


@dataclass
class GroupStatistics:
    """Statistics for a single group."""
    group_name: str
    count: int
    mean: float
    median: float
    std: float
    variance: float
    min: float
    max: float
    q1: float
    q3: float
    iqr: float
    cv: float  # Coefficient of variation


@dataclass
class TestResult:
    """Result of a statistical test."""
    test_name: str
    statistic: float
    p_value: float
    is_significant: bool
    alpha: float = 0.05
    interpretation: str = ""
    effect_size: Optional[float] = None
    effect_size_interpretation: str = ""


@dataclass
class GroupComparisonResult:
    """Complete result of group comparison analysis."""
    group_col: str
    value_col: str
    num_groups: int
    total_sample_size: int
    group_statistics: Dict[str, GroupStatistics]
    test_result: Optional[TestResult] = None
    variance_test_result: Optional[TestResult] = None
    post_hoc_results: Optional[Dict[str, TestResult]] = None


def group_statistics_by_category(
    df: pd.DataFrame,
    group_col: str,
    value_col: str
) -> Dict[str, GroupStatistics]:
    """Calculate statistics for each group.

    Args:
        df: Input DataFrame
        group_col: Column name for grouping (categorical)
        value_col: Column name for values (numeric)

    Returns:
        Dictionary mapping group names to GroupStatistics
    """
    result = {}

    # Group by the categorical column
    grouped = df.groupby(group_col, observed=True)[value_col]

    for group_name, group_data in grouped:
        # Remove NaN values
        clean_data = group_data.dropna()

        if len(clean_data) == 0:
            continue

        # Calculate statistics
        count = len(clean_data)
        mean_val = clean_data.mean()
        median_val = clean_data.median()
        std_val = clean_data.std()
        variance_val = clean_data.var()
        min_val = clean_data.min()
        max_val = clean_data.max()
        q1 = clean_data.quantile(0.25)
        q3 = clean_data.quantile(0.75)
        iqr = q3 - q1
        cv = (std_val / abs(mean_val) * 100) if mean_val != 0 else np.nan

        result[str(group_name)] = GroupStatistics(
            group_name=str(group_name),
            count=count,
            mean=mean_val,
            median=median_val,
            std=std_val,
            variance=variance_val,
            min=min_val,
            max=max_val,
            q1=q1,
            q3=q3,
            iqr=iqr,
            cv=cv
        )

    return result


def anova_test(
    groups: List[pd.Series],
    alpha: float = 0.05
) -> TestResult:
    """Perform one-way ANOVA test.

    Tests whether the means of multiple groups are significantly different.
    Assumptions:
    - Groups are normally distributed
    - Groups have equal variances (homoscedasticity)
    - Observations are independent

    Args:
        groups: List of pandas Series, one for each group
        alpha: Significance level (default 0.05)

    Returns:
        TestResult with ANOVA test results
    """
    # Remove NaN values from each group
    clean_groups = [g.dropna() for g in groups]

    # Filter out empty groups
    clean_groups = [g for g in clean_groups if len(g) > 0]

    if len(clean_groups) < 2:
        return TestResult(
            test_name='One-way ANOVA',
            statistic=np.nan,
            p_value=np.nan,
            is_significant=False,
            alpha=alpha,
            interpretation='Need at least 2 groups with data'
        )

    try:
        statistic, p_value = stats.f_oneway(*clean_groups)

        is_significant = p_value < alpha

        if is_significant:
            interp = f'Significant difference detected (p={p_value:.4f} < {alpha})'
        else:
            interp = f'No significant difference (p={p_value:.4f} >= {alpha})'

        # Calculate effect size (eta-squared)
        # eta² = SS_between / SS_total
        all_values = np.concatenate(clean_groups)
        grand_mean = np.mean(all_values)

        # Sum of squares between groups
        ss_between = sum(len(g) * (np.mean(g) - grand_mean)**2 for g in clean_groups)

        # Sum of squares total
        ss_total = sum((x - grand_mean)**2 for x in all_values)

        eta_squared = ss_between / ss_total if ss_total > 0 else 0

        # Interpret effect size
        if eta_squared < 0.01:
            effect_interp = 'Negligible'
        elif eta_squared < 0.06:
            effect_interp = 'Small'
        elif eta_squared < 0.14:
            effect_interp = 'Medium'
        else:
            effect_interp = 'Large'

        return TestResult(
            test_name='One-way ANOVA',
            statistic=statistic,
            p_value=p_value,
            is_significant=is_significant,
            alpha=alpha,
            interpretation=interp,
            effect_size=eta_squared,
            effect_size_interpretation=effect_interp
        )

    except Exception as e:
        return TestResult(
            test_name='One-way ANOVA',
            statistic=np.nan,
            p_value=np.nan,
            is_significant=False,
            alpha=alpha,
            interpretation=f'Test failed: {str(e)}'
        )


def kruskal_wallis_test(
    groups: List[pd.Series],
    alpha: float = 0.05
) -> TestResult:
    """Perform Kruskal-Wallis H-test (non-parametric alternative to ANOVA).

    Tests whether multiple groups have the same distribution.
    Does not assume normality.

    Args:
        groups: List of pandas Series, one for each group
        alpha: Significance level (default 0.05)

    Returns:
        TestResult with Kruskal-Wallis test results
    """
    # Remove NaN values from each group
    clean_groups = [g.dropna() for g in groups]

    # Filter out empty groups
    clean_groups = [g for g in clean_groups if len(g) > 0]

    if len(clean_groups) < 2:
        return TestResult(
            test_name='Kruskal-Wallis',
            statistic=np.nan,
            p_value=np.nan,
            is_significant=False,
            alpha=alpha,
            interpretation='Need at least 2 groups with data'
        )

    try:
        statistic, p_value = stats.kruskal(*clean_groups)

        is_significant = p_value < alpha

        if is_significant:
            interp = f'Significant difference detected (p={p_value:.4f} < {alpha})'
        else:
            interp = f'No significant difference (p={p_value:.4f} >= {alpha})'

        # Calculate effect size (eta-squared based on H statistic)
        # eta² = H / (n - 1) where H is the Kruskal-Wallis H statistic
        n = sum(len(g) for g in clean_groups)
        eta_squared = statistic / (n - 1) if n > 1 else 0

        # Interpret effect size (same thresholds as ANOVA eta²)
        if eta_squared < 0.01:
            effect_interp = 'Negligible'
        elif eta_squared < 0.06:
            effect_interp = 'Small'
        elif eta_squared < 0.14:
            effect_interp = 'Medium'
        else:
            effect_interp = 'Large'

        return TestResult(
            test_name='Kruskal-Wallis',
            statistic=statistic,
            p_value=p_value,
            is_significant=is_significant,
            alpha=alpha,
            interpretation=interp,
            effect_size=eta_squared,
            effect_size_interpretation=effect_interp
        )

    except Exception as e:
        return TestResult(
            test_name='Kruskal-Wallis',
            statistic=np.nan,
            p_value=np.nan,
            is_significant=False,
            alpha=alpha,
            interpretation=f'Test failed: {str(e)}'
        )


def mann_whitney_test(
    group1: pd.Series,
    group2: pd.Series,
    alpha: float = 0.05
) -> TestResult:
    """Perform Mann-Whitney U test (non-parametric test for two groups).

    Tests whether two groups have the same distribution.
    Does not assume normality.

    Args:
        group1: First group data
        group2: Second group data
        alpha: Significance level (default 0.05)

    Returns:
        TestResult with Mann-Whitney U test results
    """
    # Remove NaN values
    clean_group1 = group1.dropna()
    clean_group2 = group2.dropna()

    if len(clean_group1) == 0 or len(clean_group2) == 0:
        return TestResult(
            test_name="Mann-Whitney U",
            statistic=np.nan,
            p_value=np.nan,
            is_significant=False,
            alpha=alpha,
            interpretation='Both groups must have data'
        )

    try:
        statistic, p_value = stats.mannwhitneyu(clean_group1, clean_group2, alternative='two-sided')

        is_significant = p_value < alpha

        if is_significant:
            interp = f'Significant difference detected (p={p_value:.4f} < {alpha})'
        else:
            interp = f'No significant difference (p={p_value:.4f} >= {alpha})'

        # Calculate effect size (r)
        # r = Z / sqrt(N) where Z is approximated from U
        n1, n2 = len(clean_group1), len(clean_group2)
        N = n1 + n2

        # Approximate Z from U (for large samples)
        mean_u = n1 * n2 / 2
        std_u = np.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
        z_score = (statistic - mean_u) / std_u if std_u > 0 else 0

        r = abs(z_score) / np.sqrt(N) if N > 0 else 0

        # Interpret effect size (r)
        if r < 0.1:
            effect_interp = 'Negligible'
        elif r < 0.3:
            effect_interp = 'Small'
        elif r < 0.5:
            effect_interp = 'Medium'
        else:
            effect_interp = 'Large'

        return TestResult(
            test_name="Mann-Whitney U",
            statistic=statistic,
            p_value=p_value,
            is_significant=is_significant,
            alpha=alpha,
            interpretation=interp,
            effect_size=r,
            effect_size_interpretation=effect_interp
        )

    except Exception as e:
        return TestResult(
            test_name="Mann-Whitney U",
            statistic=np.nan,
            p_value=np.nan,
            is_significant=False,
            alpha=alpha,
            interpretation=f'Test failed: {str(e)}'
        )


def t_test_ind(
    group1: pd.Series,
    group2: pd.Series,
    equal_var: bool = True,
    alpha: float = 0.05
) -> TestResult:
    """Perform independent t-test for two groups.

    Tests whether the means of two groups are significantly different.
    Assumes normality.

    Args:
        group1: First group data
        group2: Second group data
        equal_var: If True, use Student's t-test (equal variances)
                   If False, use Welch's t-test (unequal variances)
        alpha: Significance level (default 0.05)

    Returns:
        TestResult with t-test results
    """
    # Remove NaN values
    clean_group1 = group1.dropna()
    clean_group2 = group2.dropna()

    if len(clean_group1) == 0 or len(clean_group2) == 0:
        return TestResult(
            test_name="Independent t-test",
            statistic=np.nan,
            p_value=np.nan,
            is_significant=False,
            alpha=alpha,
            interpretation='Both groups must have data'
        )

    try:
        statistic, p_value = stats.ttest_ind(clean_group1, clean_group2, equal_var=equal_var)

        is_significant = p_value < alpha

        test_type = "Student's t-test" if equal_var else "Welch's t-test"

        if is_significant:
            interp = f'Significant difference detected (p={p_value:.4f} < {alpha})'
        else:
            interp = f'No significant difference (p={p_value:.4f} >= {alpha})'

        # Calculate Cohen's d effect size
        n1, n2 = len(clean_group1), len(clean_group2)
        mean1, mean2 = clean_group1.mean(), clean_group2.mean()
        var1, var2 = clean_group1.var(), clean_group2.var()

        # Pooled standard deviation
        pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))

        cohens_d = abs(mean1 - mean2) / pooled_std if pooled_std > 0 else 0

        # Interpret Cohen's d
        if cohens_d < 0.2:
            effect_interp = 'Negligible'
        elif cohens_d < 0.5:
            effect_interp = 'Small'
        elif cohens_d < 0.8:
            effect_interp = 'Medium'
        else:
            effect_interp = 'Large'

        return TestResult(
            test_name=f"Independent t-test ({test_type})",
            statistic=statistic,
            p_value=p_value,
            is_significant=is_significant,
            alpha=alpha,
            interpretation=interp,
            effect_size=cohens_d,
            effect_size_interpretation=effect_interp
        )

    except Exception as e:
        return TestResult(
            test_name="Independent t-test",
            statistic=np.nan,
            p_value=np.nan,
            is_significant=False,
            alpha=alpha,
            interpretation=f'Test failed: {str(e)}'
        )


def levenes_test(
    groups: List[pd.Series],
    alpha: float = 0.05
) -> TestResult:
    """Perform Levene's test for equality of variances.

    Tests whether groups have equal variances.
    More robust to non-normality than Bartlett's test.

    Args:
        groups: List of pandas Series, one for each group
        alpha: Significance level (default 0.05)

    Returns:
        TestResult with Levene's test results
    """
    # Remove NaN values from each group
    clean_groups = [g.dropna() for g in groups]

    # Filter out empty groups
    clean_groups = [g for g in clean_groups if len(g) > 0]

    if len(clean_groups) < 2:
        return TestResult(
            test_name="Levene's test",
            statistic=np.nan,
            p_value=np.nan,
            is_significant=False,
            alpha=alpha,
            interpretation='Need at least 2 groups with data'
        )

    try:
        statistic, p_value = stats.levene(*clean_groups)

        # For Levene's test, significant result means variances are NOT equal
        is_significant = p_value < alpha

        if is_significant:
            interp = f'Variances are significantly different (p={p_value:.4f} < {alpha})'
        else:
            interp = f'Variances are equal (p={p_value:.4f} >= {alpha})'

        return TestResult(
            test_name="Levene's test",
            statistic=statistic,
            p_value=p_value,
            is_significant=is_significant,
            alpha=alpha,
            interpretation=interp
        )

    except Exception as e:
        return TestResult(
            test_name="Levene's test",
            statistic=np.nan,
            p_value=np.nan,
            is_significant=False,
            alpha=alpha,
            interpretation=f'Test failed: {str(e)}'
        )


def bartletts_test(
    groups: List[pd.Series],
    alpha: float = 0.05
) -> TestResult:
    """Perform Bartlett's test for equality of variances.

    Tests whether groups have equal variances.
    Assumes normality (more powerful than Levene's if assumptions met).

    Args:
        groups: List of pandas Series, one for each group
        alpha: Significance level (default 0.05)

    Returns:
        TestResult with Bartlett's test results
    """
    # Remove NaN values from each group
    clean_groups = [g.dropna() for g in groups]

    # Filter out empty groups
    clean_groups = [g for g in clean_groups if len(g) > 0]

    if len(clean_groups) < 2:
        return TestResult(
            test_name="Bartlett's test",
            statistic=np.nan,
            p_value=np.nan,
            is_significant=False,
            alpha=alpha,
            interpretation='Need at least 2 groups with data'
        )

    try:
        statistic, p_value = stats.bartlett(*clean_groups)

        # For Bartlett's test, significant result means variances are NOT equal
        is_significant = p_value < alpha

        if is_significant:
            interp = f'Variances are significantly different (p={p_value:.4f} < {alpha})'
        else:
            interp = f'Variances are equal (p={p_value:.4f} >= {alpha})'

        return TestResult(
            test_name="Bartlett's test",
            statistic=statistic,
            p_value=p_value,
            is_significant=is_significant,
            alpha=alpha,
            interpretation=interp
        )

    except Exception as e:
        return TestResult(
            test_name="Bartlett's test",
            statistic=np.nan,
            p_value=np.nan,
            is_significant=False,
            alpha=alpha,
            interpretation=f'Test failed: {str(e)}'
        )


def compare_groups(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
    test_type: Optional[TestType] = None,
    alpha: float = 0.05
) -> GroupComparisonResult:
    """Perform comprehensive group comparison analysis.

    Calculates group statistics and performs appropriate statistical tests.

    Args:
        df: Input DataFrame
        group_col: Column name for grouping (categorical)
        value_col: Column name for values (numeric)
        test_type: Type of test to perform (None to auto-select)
        alpha: Significance level (default 0.05)

    Returns:
        GroupComparisonResult with complete analysis
    """
    # Get groups
    grouped = df.groupby(group_col, observed=True)[value_col]
    group_names = list(grouped.groups.keys())
    group_series = [grouped.get_group(name) for name in group_names]

    # Calculate group statistics
    group_stats = group_statistics_by_category(df, group_col, value_col)

    # Auto-select test if not specified
    if test_type is None:
        num_groups = len(group_series)

        if num_groups == 2:
            # For 2 groups, use Mann-Whitney (non-parametric) by default
            test_type = TestType.MANN_WHITNEY
        else:
            # For 3+ groups, use Kruskal-Wallis (non-parametric) by default
            test_type = TestType.KRUSKAL

    # Perform main test
    test_result = None

    if test_type == TestType.ANOVA:
        test_result = anova_test(group_series, alpha=alpha)
        # Also test variance equality for ANOVA
        variance_result = levenes_test(group_series, alpha=alpha)
    elif test_type == TestType.KRUSKAL:
        test_result = kruskal_wallis_test(group_series, alpha=alpha)
        variance_result = None
    elif test_type == TestType.MANN_WHITNEY:
        if len(group_series) >= 2:
            test_result = mann_whitney_test(group_series[0], group_series[1], alpha=alpha)
        variance_result = None
    elif test_type == TestType.T_TEST:
        if len(group_series) >= 2:
            test_result = t_test_ind(group_series[0], group_series[1], alpha=alpha)
        # Also test variance equality
        variance_result = levenes_test(group_series, alpha=alpha)
    else:
        test_result = None
        variance_result = None

    return GroupComparisonResult(
        group_col=group_col,
        value_col=value_col,
        num_groups=len(group_names),
        total_sample_size=sum(len(g.dropna()) for g in group_series),
        group_statistics=group_stats,
        test_result=test_result,
        variance_test_result=variance_result
    )


def group_comparison_table(
    df: pd.DataFrame,
    group_col: str,
    value_col: str
) -> pd.DataFrame:
    """Create a summary table for group comparison.

    Args:
        df: Input DataFrame
        group_col: Column name for grouping
        value_col: Column name for values

    Returns:
        DataFrame with group comparison statistics
    """
    result = compare_groups(df, group_col, value_col)

    rows = []
    for group_name, stats in result.group_statistics.items():
        rows.append({
            'Group': group_name,
            'Count': stats.count,
            'Mean': stats.mean,
            'Median': stats.median,
            'Std': stats.std,
            'Min': stats.min,
            'Max': stats.max,
            'Q1': stats.q1,
            'Q3': stats.q3,
            'IQR': stats.iqr,
            'CV (%)': stats.cv
        })

    comparison_df = pd.DataFrame(rows)

    if len(comparison_df) > 0:
        comparison_df = comparison_df.set_index('Group')

    return comparison_df


def tukey_hsd(
    groups: List[pd.Series],
    group_names: List[str],
    alpha: float = 0.05
) -> pd.DataFrame:
    """Perform Tukey's Honest Significant Difference (HSD) post-hoc test.

    Performs pairwise comparisons between all groups with p-value adjustment.

    Note: Requires scipy >= 1.10.0 or statsmodels.

    Args:
        groups: List of pandas Series, one for each group
        group_names: Names of the groups
        alpha: Significance level (default 0.05)

    Returns:
        DataFrame with pairwise comparison results
    """
    # Remove NaN values
    clean_groups = [g.dropna() for g in groups]

    # Prepare data for Tukey HSD
    values = []
    group_labels = []

    for name, group in zip(group_names, clean_groups):
        values.extend(group.values)
        group_labels.extend([name] * len(group))

    # Try using scipy.stats.tukey_hsd if available (scipy >= 1.10.0)
    try:
        result = stats.tukey_hsd(*clean_groups)

        # Extract results
        comparisons = []
        n_groups = len(group_names)

        for i in range(n_groups):
            for j in range(i + 1, n_groups):
                comparisons.append({
                    'Group 1': group_names[i],
                    'Group 2': group_names[j],
                    'Mean Diff': result.statistic[i, j],
                    'p-value': result.pvalue[i, j],
                    'Reject': result.pvalue[i, j] < alpha
                })

        return pd.DataFrame(comparisons)

    except AttributeError:
        # Fall back: return message about needing newer scipy or statsmodels
        return pd.DataFrame({
            'Note': ['Tukey HSD requires scipy >= 1.10.0 or statsmodels. '
                    'Install with: pip3 install statsmodels']
        })


def recommended_test(
    groups: List[pd.Series],
    alpha: float = 0.05
) -> str:
    """Recommend the appropriate statistical test based on data characteristics.

    Args:
        groups: List of pandas Series, one for each group
        alpha: Significance level

    Returns:
        String describing the recommended test
    """
    num_groups = len(groups)

    if num_groups < 2:
        return "Need at least 2 groups for comparison"

    # Check sample sizes
    group_sizes = [len(g.dropna()) for g in groups]
    total_size = sum(group_sizes)

    # For 2 groups
    if num_groups == 2:
        if total_size < 30:
            return "Mann-Whitney U test (small sample, non-parametric)"
        else:
            return "Independent t-test or Mann-Whitney U test (check normality first)"

    # For 3+ groups
    if num_groups >= 3:
        if total_size < 30:
            return "Kruskal-Wallis test (small sample, non-parametric)"
        else:
            return "ANOVA or Kruskal-Wallis test (check normality and variance equality first)"

    return "Unknown test"
