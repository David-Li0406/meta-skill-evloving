# Advanced Analysis Examples

Complex analytical workflows and advanced techniques.

## Table of Contents

- [Group Comparison Analysis](#group-comparison-analysis)
- [Advanced Outlier Analysis](#advanced-outlier-analysis)
- [Multi-Variable Analysis](#multi-variable-analysis)
- [Custom Report Generation](#custom-report-generation)

## Group Comparison Analysis

### Example 1: Comparing Groups with Different Tests

**Scenario:** Compare test scores across different teaching methods.

```python
import pandas as pd
from scripts.core.group_analysis import compare_groups
from scripts.core.distribution import test_normality
from scripts.reporting.terminal import display_group_comparison

# Load data
df = pd.read_csv('education_data.csv')

# Check normality for each group
for method in df['teaching_method'].unique():
    group_scores = df[df['teaching_method'] == method]['test_score']
    normality = test_normality(group_scores)

    print(f"\n{method}:")
    for test_name, result in normality.items():
        if result.p_value:
            print(f"  {test_name}: p = {result.p_value:.4f}")

# Choose appropriate test based on normality
# If all groups are normal: use ANOVA
# If not all normal: use Kruskal-Wallis

# Run comparison
comparison = compare_groups(
    df=df,
    group_col='teaching_method',
    value_col='test_score',
    test_type=None  # Auto-select based on data
)

# Display results
display_group_comparison(comparison)
```

### Example 2: Pairwise Group Comparisons

```python
import pandas as pd
from scripts.core.group_analysis import t_test_ind, mann_whitney_test
from itertools import combinations

# Get all groups
groups = df['category'].unique()

# Compare all pairs
for group1, group2 in combinations(groups, 2):
    data1 = df[df['category'] == group1]['value']
    data2 = df[df['category'] == group2]['value']

    # Check normality for both groups
    from scripts.core.distribution import test_normality
    norm1 = test_normality(data1)
    norm2 = test_normality(data2)

    # Use appropriate test
    shapiro_p1 = norm1.get('shapiro')
    shapiro_p2 = norm2.get('shapiro')

    if (shapiro_p1 and shapiro_p1.p_value > 0.05 and
        shapiro_p2 and shapiro_p2.p_value > 0.05):
        # Both normal: use t-test
        result = t_test_ind(data1, data2)
        test_used = "t-test"
    else:
        # At least one not normal: use Mann-Whitney
        result = mann_whitney_test(data1, data2)
        test_used = "Mann-Whitney"

    print(f"\n{group1} vs {group2}:")
    print(f"  Test: {test_used}")
    print(f"  p-value: {result.p_value:.4f}")
    print(f"  Result: {'Significant' if result.is_significant else 'Not significant'}")
    if result.effect_size:
        print(f"  Effect size: {result.effect_size:.4f} ({result.effect_size_interpretation})")
```

### Example 3: Group Comparison with Visualization

```python
import pandas as pd
from scripts.core.group_analysis import compare_groups, group_comparison_table
from scripts.visualization.plotly_charts import create_boxplot, create_violinplot
from scripts.reporting.html_report import generate_html_report

# Load data
df = pd.read_csv('sales_data.csv')

# Compare sales across regions
comparison = compare_groups(
    df=df,
    group_col='region',
    value_col='sales_amount',
    test_type=None  # Auto-select
)

# Create visualizations
box_fig = create_boxplot(
    df=df,
    x_col='region',
    y_col='sales_amount',
    title="Sales by Region"
)

violin_fig = create_violinplot(
    df=df,
    x_col='region',
    y_col='sales_amount',
    title="Sales Distribution by Region"
)

# Prepare results for HTML report
results = {
    'num_analyzed': 1,
    'group_comparison': {
        'group_col': 'region',
        'value_col': 'sales_amount',
        'num_groups': comparison.num_groups,
        'test_result': {
            'test_name': comparison.test_result.test_name if comparison.test_result else None,
            'statistic': comparison.test_result.statistic if comparison.test_result else None,
            'p_value': comparison.test_result.p_value if comparison.test_result else None,
            'is_significant': comparison.test_result.is_significant if comparison.test_result else None,
            'interpretation': comparison.test_result.interpretation if comparison.test_result else None,
        } if comparison.test_result else None,
        'chart': box_fig.to_html(include_plotlyjs=False, div_id="boxplot") +
                violin_fig.to_html(include_plotlyjs=False, div_id="violinplot")
    },
    'group_stats_table': group_comparison_table(df, 'region', 'sales_amount').to_html()
}

# Generate report
generate_html_report(
    df=df,
    results=results,
    output_path='group_comparison_report.html',
    title='Sales by Region Analysis'
)
```

## Advanced Outlier Analysis

### Example 1: Multiple Methods Comparison

```python
import pandas as pd
from scripts.core.outliers import (
    detect_outliers_iqr,
    detect_outliers_zscore,
    detect_outliers_modified_zscore,
    consensus_outliers
)

# Load data
df = pd.read_csv('financial_data.csv')
column = 'transaction_amount'

# Detect outliers using different methods
iqr_outliers = detect_outliers_iqr(df[column], multiplier=1.5)
z_outliers = detect_outliers_zscore(df[column], threshold=3.0)
modified_z_outliers = detect_outliers_modified_zscore(df[column], threshold=3.5)

# Compare results
print(f"IQR method: {iqr_outliers.outlier_count} outliers")
print(f"Z-score method: {z_outliers.outlier_count} outliers")
print(f"Modified Z-score: {modified_z_outliers.outlier_count} outliers")

# Find consensus (agreement from all methods)
consensus = consensus_outliers(
    df[column],
    methods=['iqr', 'zscore', 'modified_zscore'],
    require_all=True  # Only values flagged by ALL methods
)

print(f"\nConsensus outliers (all methods agree): {consensus.outlier_count}")
print(f"These are the most definitive outliers")

# Alternative: outliers flagged by ANY method
consensus_any = consensus_outliers(
    df[column],
    methods=['iqr', 'zscore', 'modified_zscore'],
    require_all=False
)

print(f"\nPotential outliers (any method): {consensus_any.outlier_count}")
```

### Example 2: Outlier Investigation Workflow

```python
import pandas as pd
import numpy as np
from scripts.core.outliers import detect_outliers_iqr, consensus_outliers
from scripts.core.statistics import compute_basic_stats
from scripts.visualization.plotly_charts import create_outlier_plot

# Load data
df = pd.read_csv('data.csv')
column = 'salary'

# Detect outliers
outliers = detect_outliers_iqr(df[column], multiplier=1.5)

if outliers.outlier_count > 0:
    print(f"Found {outliers.outlier_count} outliers")

    # Get outlier rows
    outlier_rows = df.loc[outliers.outlier_indices]

    # Compare outlier vs non-outlier statistics
    is_outlier = df.index.isin(outliers.outlier_indices)

    print("\nNon-outlier statistics:")
    non_outlier_stats = compute_basic_stats(df[~is_outlier][column])
    print(f"  Mean: ${non_outlier_stats['mean']:,.2f}")
    print(f"  Median: ${non_outlier_stats['median']:,.2f}")
    print(f"  Std: ${non_outlier_stats['std']:,.2f}")

    print("\nOutlier statistics:")
    outlier_stats = compute_basic_stats(df[is_outlier][column])
    print(f"  Mean: ${outlier_stats['mean']:,.2f}")
    print(f"  Median: ${outlier_stats['median']:,.2f}")
    print(f"  Std: ${outlier_stats['std']:,.2f}")

    # Check if outliers might be legitimate (e.g., executives)
    # by examining other columns
    if 'position' in df.columns:
        print("\nOutlier positions:")
        print(outlier_rows['position'].value_counts())

    # Create visualization
    fig = create_outlier_plot(df[column], outliers.outlier_indices)
    fig.write_html('outlier_investigation.html')

    # Recommendation logic
    outlier_pct = outliers.outlier_percentage
    if outlier_pct > 10:
        print("\n⚠️  High percentage of outliers detected.")
        print("   Consider if data is heavily skewed rather than having true outliers.")
        print("   A transformation (e.g., log) might be appropriate.")
    elif outlier_pct > 5:
        print("\n⚠️  Moderate outlier percentage.")
        print("   Investigate context before removing.")
    else:
        print("\n✓ Outlier percentage is within expected range.")
```

### Example 3: Outlier Removal and Impact Analysis

```python
from scripts.core.outliers import remove_outliers
from scripts.core.statistics import compute_basic_stats
from scripts.core.distribution import test_normality

# Compare with and without outliers
column = 'income'

# Original statistics
original_stats = compute_basic_stats(df[column])
original_normality = test_normality(df[column])

print("Original data:")
print(f"  Mean: {original_stats['mean']:.2f}")
print(f"  Std: {original_stats['std']:.2f}")
print(f"  Skewness: {original_stats['skewness']:.4f}")

# Check normality
if 'shapiro' in original_normality:
    shapiro_result = original_normality['shapiro']
    print(f"  Normality (Shapiro-Wilk): p = {shapiro_result.p_value:.4f}")
    print(f"  {'✓ Normal' if shapiro_result.p_value > 0.05 else '✗ Not normal'}")

# Remove outliers
clean_series = remove_outliers(df[column], method='iqr')

# Clean statistics
clean_stats = compute_basic_stats(clean_series)
clean_normality = test_normality(clean_series)

print("\nAfter removing outliers:")
print(f"  Mean: {clean_stats['mean']:.2f}")
print(f"  Std: {clean_stats['std']:.2f}")
print(f"  Skewness: {clean_stats['skewness']:.4f}")

if 'shapiro' in clean_normality:
    shapiro_result = clean_normality['shapiro']
    print(f"  Normality (Shapiro-Wilk): p = {shapiro_result.p_value:.4f}")
    print(f"  {'✓ Normal' if shapiro_result.p_value > 0.05 else '✗ Not normal'}")

# Calculate impact
mean_change = abs(clean_stats['mean'] - original_stats['mean']) / original_stats['mean'] * 100
std_change = abs(clean_stats['std'] - original_stats['std']) / original_stats['std'] * 100

print(f"\nImpact:")
print(f"  Mean changed by: {mean_change:.2f}%")
print(f"  Std changed by: {std_change:.2f}%")
print(f"  Data points removed: {len(df[column]) - len(clean_series)}")
```

## Multi-Variable Analysis

### Example 1: Correlation Analysis

```python
import pandas as pd
from scripts.visualization.plotly_charts import create_correlation_heatmap
import numpy as np

# Load data
df = pd.read_csv('data.csv')

# Select numeric columns
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

# Create correlation heatmap
pearson_fig = create_correlation_heatmap(
    df=df[numeric_cols],
    method='pearson',
    title="Pearson Correlation Matrix"
)

spearman_fig = create_correlation_heatmap(
    df=df[numeric_cols],
    method='spearman',
    title="Spearman Correlation Matrix"
)

pearson_fig.write_html('correlation_pearson.html')
spearman_fig.write_html('correlation_spearman.html')

# Find strong correlations
corr_matrix = df[numeric_cols].corr()

print("Strong correlations (|r| > 0.7):")
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        corr_val = corr_matrix.iloc[i, j]
        if abs(corr_val) > 0.7:
            print(f"  {corr_matrix.columns[i]} ↔ {corr_matrix.columns[j]}: r = {corr_val:.3f}")
```

### Example 2: Pair Plot for Multiple Variables

```python
from scripts.visualization.plotly_charts import create_pairplot

# Select variables for pair plot
vars_to_plot = ['age', 'income', 'score', 'experience']

# Create pair plot
pair_fig = create_pairplot(
    df=df[vars_to_plot],
    color_col='category' if 'category' in df.columns else None
)

pair_fig.write_html('pairplot.html')

print("✓ Pair plot generated")
```

### Example 3: Subset Analysis

```python
# Analyze subsets based on categorical variable
category_col = 'department'

for category in df[category_col].unique():
    subset = df[df[category_col] == category]

    print(f"\n{'='*50}")
    print(f"Department: {category}")
    print(f"{'='*50}")

    # Get numeric columns
    numeric_cols = subset.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        stats = compute_basic_stats(subset[col])
        print(f"\n{col}:")
        print(f"  Count: {stats['count']}")
        print(f"  Mean: {stats['mean']:.2f}")
        print(f"  Median: {stats['median']:.2f}")
        print(f"  Std: {stats['std']:.2f}")
```

## Custom Report Generation

### Example 1: Comprehensive Analysis Report

```python
import pandas as pd
from scripts.core import *
from scripts.visualization.plotly_charts import *
from scripts.reporting.html_report import generate_html_report
from scripts.reporting.terminal import display_data_summary

# Load data
df = pd.read_csv('comprehensive_data.csv')

# Get data summary
summary = get_data_summary(df)

# Display in terminal
display_data_summary(summary)

# Select numeric columns for analysis
numeric_cols = summary['numeric_columns']

# Prepare results dictionary
results = {'num_analyzed': len(numeric_cols)}

# 1. Summary statistics
stats_dict = {}
for col in numeric_cols:
    stats_dict[col] = compute_basic_stats(df[col])

stats_df = pd.DataFrame(stats_dict).T
results['summary_stats_table'] = stats_df.to_html(classes='table table-striped')

# 2. Distribution analysis
distribution_results = {}
for col in numeric_cols:
    dist_summary = distribution_summary(df[col])
    hist_fig = create_histogram(df[col], title=f"Distribution: {col}")
    qq_fig = create_qqplot(df[col], title=f"Q-Q Plot: {col}")

    distribution_results[col] = {
        'shape_stats': dist_summary['shape_stats'],
        'normality_tests': {
            k: {
                'statistic': v.statistic,
                'p_value': v.p_value,
                'is_normal': v.is_normal,
                'interpretation': v.interpretation
            } for k, v in dist_summary['normality_tests'].items()
        },
        'chart': figure_to_html(hist_fig) + figure_to_html(qq_fig),
    }

results['distribution'] = distribution_results

# 3. Outlier detection
outlier_results = {}
for col in numeric_cols:
    outliers = consensus_outliers(df[col])
    outlier_fig = create_outlier_plot(df[col], outliers.outlier_indices)

    outlier_results[col] = {
        'method': outliers.method,
        'outlier_count': outliers.outlier_count,
        'outlier_percentage': outliers.outlier_percentage,
        'lower_bound': outliers.lower_bound,
        'upper_bound': outliers.upper_bound,
        'chart': figure_to_html(outlier_fig),
    }

results['outliers'] = outlier_results

# 4. Correlation analysis (if multiple columns)
if len(numeric_cols) > 1:
    corr_fig = create_correlation_heatmap(df[numeric_cols])
    results['correlation'] = {
        'chart': figure_to_html(corr_fig)
    }

# Add warnings if any
warnings = []
if summary['has_issues']:
    warnings.extend(summary['warnings'])

results['warnings'] = warnings

# Generate comprehensive report
generate_html_report(
    df=df,
    results=results,
    output_path='comprehensive_analysis_report.html',
    title='Comprehensive Statistical Analysis Report',
    metadata={
        'analyst': 'Data Analyst',
        'project': 'Analysis Project',
    }
)

print("✓ Comprehensive analysis report generated")
```

### Example 2: Dashboard-Style Report

```python
from jinja2 import Template

dashboard_template = Template('''
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .card h3 { margin-top: 0; color: #667eea; }
        .metric { font-size: 2em; font-weight: bold; color: #764ba2; }
        .label { font-size: 0.9em; color: #666; }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>
    <div class="dashboard">
        {% for item in dashboard_items %}
        <div class="card">
            <h3>{{ item.title }}</h3>
            {% if item.type == 'metric' %}
            <div class="metric">{{ item.value }}</div>
            <div class="label">{{ item.label }}</div>
            {% elif item.type == 'chart' %}
            {{ item.content | safe }}
            {% endif %}
        </div>
        {% endfor %}
    </div>
</body>
</html>
''')

# Prepare dashboard items
dashboard_items = []

# Add key metrics
dashboard_items.append({
    'type': 'metric',
    'title': 'Total Records',
    'value': f"{len(df):,}",
    'label': 'Number of observations'
})

dashboard_items.append({
    'type': 'metric',
    'title': 'Variables Analyzed',
    'value': len(numeric_cols),
    'label': 'Numeric columns'
})

# Add charts
for col in numeric_cols[:4]:  # Limit to 4 charts
    fig = create_histogram(df[col], title=col)
    dashboard_items.append({
        'type': 'chart',
        'title': col,
        'content': figure_to_html(fig)
    })

# Render dashboard
html = dashboard_template.render(
    title='Analysis Dashboard',
    dashboard_items=dashboard_items
)

with open('dashboard.html', 'w') as f:
    f.write(html)

print("✓ Dashboard generated")
```

## Best Practices

1. **Always validate assumptions** before applying tests
2. **Document your analysis steps** for reproducibility
3. **Use appropriate visualizations** for your data type
4. **Report both statistics and practical significance**
5. **Check data quality** before running complex analyses
6. **Handle outliers thoughtfully** - don't automatically remove them
7. **Consider transformation** for heavily skewed data
8. **Use multiple methods** for robustness
