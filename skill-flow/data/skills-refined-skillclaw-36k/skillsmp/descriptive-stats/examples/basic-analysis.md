# Basic Analysis Examples

Step-by-step examples of basic statistical analysis workflows.

## Example 1: Quick Data Exploration

**Scenario:** You just received a CSV file and want to quickly understand the data.

### Steps

1. **Load and preview the data:**
```python
import pandas as pd

# Load data
df = pd.read_csv('data.csv')

# Preview
print(df.head())
print(df.info())
```

2. **Get data summary:**
```python
from scripts.core.data_loader import get_data_summary

summary = get_data_summary(df)
print(f"Rows: {summary['shape'][0]}")
print(f"Columns: {summary['shape'][1]}")
print(f"Numeric columns: {summary['numeric_columns']}")
print(f"Categorical columns: {summary['categorical_columns']}")
```

3. **Compute basic statistics:**
```python
from scripts.core.statistics import compute_summary_table

# Get summary for all numeric columns
summary_table = compute_summary_table(df)
print(summary_table)
```

### Expected Output

```
Basic Information
┏━━━━━━━━━━━━━━━━┓
┃ Metric          ┃
┡━━━━━━━━━━━━━━━━┩
│ Rows           │ 1,000    │
│ Columns        │ 5        │
│ Numeric Cols   │ 3        │
│ Categorical    │ 2        │
└────────────────┘

Summary Statistics
┌─────────────┬─────────┬─────────┬─────────┬─────────┐
│ Statistic   │ age     │ income  │ score   │         │
├─────────────┼─────────┼─────────┼─────────┼─────────┤
│ Count       │ 1,000   │ 1,000   │ 1,000   │         │
│ Mean        │ 35.2    │ 50,000  │ 75.3    │         │
│ Median      │ 34.0    │ 48,000  │ 76.0    │         │
│ Std         │ 8.5     │ 12,000  │ 12.1    │         │
│ Min         │ 18.0    │ 20,000  │ 45.0    │         │
│ Max         │ 65.0    │ 95,000  │ 99.0    │         │
└─────────────┴─────────┴─────────┴─────────┴─────────┘
```

## Example 2: Single Variable Distribution Analysis

**Scenario:** Analyze the distribution of test scores.

### Steps

1. **Compute distribution statistics:**
```python
from scripts.core.distribution import distribution_summary

results = distribution_summary(df['score'])

print(f"Skewness: {results['shape_stats']['skewness']:.4f}")
print(f"Kurtosis: {results['shape_stats']['kurtosis']:.4f}")
print(f"Interpretation: {results['shape_stats']['skewness_interpretation']}")
```

2. **Test for normality:**
```python
from scripts.core.distribution import test_normality

normality = test_normality(df['score'])

for test_name, result in normality.items():
    print(f"{test_name}: p = {result.p_value:.4f}")
    print(f"  Result: {result.interpretation}")
```

3. **Create visualization:**
```python
from scripts.visualization.plotly_charts import create_histogram, create_qqplot

# Histogram
hist_fig = create_histogram(df['score'], title="Score Distribution")
hist_fig.write_html('score_histogram.html')

# Q-Q plot
qq_fig = create_qqplot(df['score'], title="Score Q-Q Plot")
qq_fig.write_html('score_qqplot.html')
```

### Interpreting Results

**Skewness:**
- -0.5 < skewness < 0.5: Approximately symmetric ✓
- skewness ≥ 0.5: Right-skewed (tail to the right)
- skewness ≤ -0.5: Left-skewed (tail to the left)

**Kurtosis (excess):**
- -0.5 < kurtosis < 0.5: Normal-like ✓
- kurtosis > 0.5: Heavy-tailed, peaked (leptokurtic)
- kurtosis < -0.5: Light-tailed, flat (platykurtic)

**Normality Tests:**
- p < 0.05: Data is NOT normally distributed
- p ≥ 0.05: Data may be normally distributed

## Example 3: Outlier Detection

**Scenario:** Identify and analyze outliers in salary data.

### Steps

1. **Detect outliers using IQR method:**
```python
from scripts.core.outliers import detect_outliers_iqr

outliers = detect_outliers_iqr(df['salary'], multiplier=1.5)

print(f"Method: {outliers.method}")
print(f"Outliers found: {outliers.outlier_count}")
print(f"Percentage: {outliers.outlier_percentage:.2f}%")
print(f"Bounds: [{outliers.lower_bound:.2f}, {outliers.upper_bound:.2f}]")
```

2. **Get outlier details:**
```python
if outliers.outlier_count > 0:
    print("\nOutlier values:")
    for idx, val in zip(outliers.outlier_indices, outliers.outlier_values):
        print(f"  Index {idx}: ${val:,.2f}")
```

3. **Create outlier plot:**
```python
from scripts.visualization.plotly_charts import create_outlier_plot

fig = create_outlier_plot(df['salary'], outliers.outlier_indices, title="Salary Outliers")
fig.write_html('salary_outliers.html')
```

4. **Use consensus method (multiple methods):**
```python
from scripts.core.outliers import consensus_outliers

# Requires agreement from both methods
consensus = consensus_outliers(df['salary'], methods=['iqr', 'zscore'], require_all=True)

print(f"Consensus outliers: {consensus.outlier_count}")
print("These values are flagged by both IQR and Z-score methods")
```

### Handling Outliers

**Options:**
1. **Keep them:** If they're legitimate values
2. **Remove them:** If they're data entry errors
3. **Transform:** Apply log transformation for skewed data
4. **Winsorize:** Cap extreme values at a percentile

```python
# Example: Remove outliers
from scripts.core.outliers import remove_outliers
clean_data = remove_outliers(df['salary'], method='iqr')

# Example: Winsorize (cap at 5th and 95th percentile)
from scripts.core.outliers import winsorize
winsorized_data = winsorize(df['salary'], limits=(0.05, 0.05))
```

## Example 4: Comparing Multiple Columns

**Scenario:** Compare statistics across multiple numerical variables.

### Steps

1. **Compute statistics for all columns:**
```python
from scripts.core.statistics import compute_summary_table

# Analyze specific columns
columns = ['age', 'income', 'score', 'experience']
summary_table = compute_summary_table(df[columns])

print(summary_table)
```

2. **Compare variability (CV):**
```python
# Sort by coefficient of variation
print("\nVariability Comparison (CV %):")
print(summary_table['CV %'].sort_values(ascending=False))
```

3. **Create correlation heatmap:**
```python
from scripts.visualization.plotly_charts import create_correlation_heatmap

corr_fig = create_correlation_heatmap(df[columns], method='pearson')
corr_fig.write_html('correlation_heatmap.html')
```

4. **Generate HTML report:**
```python
from scripts.reporting.html_report import generate_html_report
from scripts.core import *

# Prepare analysis results
results = {'num_analyzed': len(columns)}

# Add statistics
stats_dict = {}
for col in columns:
    stats_dict[col] = compute_basic_stats(df[col])

stats_df = pd.DataFrame(stats_dict).T
results['summary_stats_table'] = stats_df.to_html()

# Add correlation
results['correlation'] = {
    'chart': figure_to_html(corr_fig)
}

# Generate report
generate_html_report(df, results, 'comparison_report.html')
```

## Example 5: Working with Different Data Types

### CSV Files

```python
# Load CSV
df = pd.read_csv('data.csv')

# Specify encoding if needed
df = pd.read_csv('data.csv', encoding='utf-8')

# Handle different delimiters
df = pd.read_csv('data.csv', sep=';')
```

### Excel Files

```python
# Load Excel (first sheet)
df = pd.read_excel('data.xlsx')

# Load specific sheet
df = pd.read_excel('data.xlsx', sheet_name='Sheet2')

# Load sheet by index
df = pd.read_excel('data.xlsx', sheet_name=0)
```

### Data Cleaning

```python
# Remove whitespace from column names
df.columns = df.columns.str.strip()

# Handle missing values
df_clean = df.dropna()  # Remove rows with missing values
df_filled = df.fillna(df.mean())  # Fill with mean

# Convert column types
df['date_column'] = pd.to_datetime(df['date_column'])
df['numeric_column'] = pd.to_numeric(df['numeric_column'], errors='coerce')
```

## Common Workflows

### Workflow 1: Data Quality Check

```python
# 1. Load data
df = pd.read_csv('data.csv')

# 2. Validate data
from scripts.core.data_loader import validate_data
validation = validate_data(df)

# 3. Check for issues
if validation.has_issues():
    print("⚠️  Data quality issues found:")
    for warning in validation.warnings:
        print(f"  - {warning}")
    for error in validation.errors:
        print(f"  ✗ {error}")
else:
    print("✓ No data quality issues detected")
```

### Workflow 2: Complete Single Column Analysis

```python
# Analyze one column comprehensively
from scripts.reporting.html_report import create_single_column_report

create_single_column_report(
    series=df['target_column'],
    output_path='target_column_analysis.html',
    column_name='Target Column'
)
```

### Workflow 3: Batch Analysis

```python
# Analyze multiple columns and save individual reports
numeric_cols = get_numeric_columns(df)

for col in numeric_cols:
    output_name = f'analysis_{col}.html'
    create_single_column_report(
        series=df[col],
        output_path=output_name,
        column_name=col
    )
    print(f"✓ Generated: {output_name}")
```

## Tips and Best Practices

1. **Always start with data exploration:**
   - Check data types
   - Look for missing values
   - Verify data ranges

2. **Choose appropriate statistics:**
   - Use mean + std for normal distributions
   - Use median + IQR for skewed distributions

3. **Visualize your data:**
   - Histograms for distribution
   - Box plots for outliers
   - Q-Q plots for normality assessment

4. **Check assumptions before tests:**
   - Normality for parametric tests
   - Variance homogeneity for ANOVA

5. **Report both p-values and effect sizes:**
   - Statistical significance ≠ practical significance
   - Always include effect size interpretation
