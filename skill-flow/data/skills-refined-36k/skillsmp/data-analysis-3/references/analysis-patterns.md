# Data Analysis Patterns

This reference covers common data analysis patterns using Python's data science libraries.

## Data Loading and Inspection

### Loading Data

```python
import pandas as pd

# CSV files
df = pd.read_csv('data.csv')
df = pd.read_csv('data.csv', encoding='utf-8', sep=',', header=0)

# JSON files
df = pd.read_json('data.json')
df = pd.read_json('data.json', orient='records')

# Parquet files
df = pd.read_parquet('data.parquet')

# Excel files
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')
```

### Inspecting Data

```python
# Basic info
df.shape          # (rows, columns)
df.info()         # Column types and memory usage
df.dtypes         # Data types

# Preview data
df.head(10)       # First 10 rows
df.tail(5)        # Last 5 rows
df.sample(5)      # Random sample

# Summary statistics
df.describe()                    # Numeric columns
df.describe(include='all')       # All columns
df['column'].value_counts()      # Frequency counts
```

## Data Cleaning

### Handling Missing Values

```python
# Detect missing values
df.isnull().sum()              # Count per column
df.isnull().sum().sum()        # Total count

# Remove missing values
df.dropna()                    # Drop rows with any NaN
df.dropna(subset=['col1'])     # Drop rows where col1 is NaN

# Fill missing values
df.fillna(0)                   # Fill with constant
df.fillna(df.mean())           # Fill with column means
df['col'].fillna(method='ffill')  # Forward fill
```

### Handling Duplicates

```python
# Detect duplicates
df.duplicated().sum()          # Count duplicates
df[df.duplicated()]            # View duplicates

# Remove duplicates
df.drop_duplicates()
df.drop_duplicates(subset=['col1', 'col2'], keep='first')
```

### Data Type Conversion

```python
# Convert types
df['col'] = df['col'].astype(int)
df['col'] = df['col'].astype('category')
df['date'] = pd.to_datetime(df['date'])
df['num'] = pd.to_numeric(df['num'], errors='coerce')
```

## Statistical Analysis

### Descriptive Statistics

```python
import numpy as np

# Central tendency
df['col'].mean()
df['col'].median()
df['col'].mode()

# Dispersion
df['col'].std()
df['col'].var()
df['col'].min(), df['col'].max()

# Quantiles
df['col'].quantile([0.25, 0.5, 0.75])
```

### Correlation Analysis

```python
# Correlation matrix
df.corr()
df.corr(method='spearman')

# Specific correlation
df['col1'].corr(df['col2'])
```

### Grouping and Aggregation

```python
# Group by single column
df.groupby('category').mean()
df.groupby('category')['value'].sum()

# Multiple aggregations
df.groupby('category').agg({
    'value': ['mean', 'sum', 'count'],
    'quantity': 'sum'
})

# Group by multiple columns
df.groupby(['cat1', 'cat2']).mean()
```

## Visualization Patterns

### Basic Plots

```python
import matplotlib.pyplot as plt

# Histogram
df['col'].hist(bins=30)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Distribution')
plt.show()

# Bar chart
df['category'].value_counts().plot(kind='bar')
plt.show()

# Line plot
df.plot(x='date', y='value', kind='line')
plt.show()
```

### Statistical Plots

```python
# Box plot
df.boxplot(column='value', by='category')
plt.show()

# Scatter plot
df.plot.scatter(x='col1', y='col2')
plt.show()

# Correlation heatmap
import seaborn as sns
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.show()
```

### Saving Figures

```python
plt.savefig('output.png', dpi=300, bbox_inches='tight')
plt.savefig('output.pdf', format='pdf')
```

