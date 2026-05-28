---
name: python-data-science
description: Data analysis, scientific computing, visualization with pandas, numpy, matplotlib
license: MIT
compatibility: opencode
metadata:
  audience: python-developers
  focus: data-science
---

## What I do

I provide guidance on data science and scientific computing in Python, including:

- pandas for data manipulation and analysis
- numpy for numerical computing
- matplotlib and seaborn for visualization
- polars for high-performance dataframes
- Data pipeline patterns (ETL, transformation, loading)
- Type hints for data science code
- Performance optimization (vectorization, chunking)
- Jupyter notebook best practices
- Machine learning data preparation

## When to use me

Use me when:
- Analyzing or transforming datasets with pandas/polads
- Performing numerical computations with numpy
- Creating data visualizations
- Building data pipelines and ETL processes
- Optimizing data science code performance
- Preparing data for machine learning
- Working with large datasets
- Integrating data science code into production

## Best Practices

### ✅ Use Polars for Large Datasets with Type Hints

```python
import polars as pl
from typing import Literal

def analyze_sales(
    df: pl.DataFrame,
    metric: Literal["revenue", "units"] = "revenue"
) -> pl.DataFrame:
    """Analyze sales data with lazy evaluation and type hints."""
    return (
        df.lazy()
        .group_by("category")
        .agg(pl.col(metric).sum())
        .sort(metric, descending=True)
        .collect()
    )

# Query optimization with polars
def filter_and_transform(data: pl.DataFrame) -> pl.DataFrame:
    """Filter and transform data efficiently."""
    return (
        data.lazy()
        .filter(pl.col("status") == "active")
        .with_columns([
            (pl.col("price") * pl.col("quantity")).alias("total")
        ])
        .collect()
    )
```

### ✅ Use Pandas for Medium-Sized Data

```python
import pandas as pd
from typing import Optional

def process_transactions(
    df: pd.DataFrame,
    min_amount: Optional[float] = None
) -> pd.DataFrame:
    """Process transactions with proper type hints."""
    if min_amount is not None:
        df = df[df["amount"] >= min_amount]

    # Use vectorized operations
    df["processed_at"] = pd.to_datetime(df["timestamp"])
    df["amount_usd"] = df["amount"] * df["exchange_rate"]

    return df.groupby("category")["amount_usd"].sum()
```

### ✅ Use Numpy for Numerical Computing

```python
import numpy as np
from typing import Tuple

def normalize_features(
    features: np.ndarray,
    method: str = "standard"
) -> Tuple[np.ndarray, dict]:
    """Normalize features with multiple methods."""
    if method == "standard":
        mean = np.mean(features, axis=0)
        std = np.std(features, axis=0)
        normalized = (features - mean) / std
        params = {"mean": mean, "std": std}

    elif method == "minmax":
        min_val = np.min(features, axis=0)
        max_val = np.max(features, axis=0)
        normalized = (features - min_val) / (max_val - min_val)
        params = {"min": min_val, "max": max_val}

    return normalized, params
```

### ✅ Vectorized Operations (Avoid Loops)

```python
# ❌ BAD: Slow loop-based operations
def bad_mean_squared_error(y_true: list, y_pred: list) -> float:
    """Calculate MSE with slow loops."""
    total = 0.0
    for true, pred in zip(y_true, y_pred):
        total += (true - pred) ** 2
    return total / len(y_true)

# ✅ GOOD: Fast vectorized operations
def good_mean_squared_error(
    y_true: np.ndarray,
    y_pred: np.ndarray
) -> float:
    """Calculate MSE with vectorized operations."""
    diff = y_true - y_pred
    return np.mean(diff ** 2)
```

### ✅ Proper Data Visualization

```python
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional

def plot_distribution(
    data: pd.Series,
    title: str,
    figsize: Tuple[int, int] = (10, 6)
) -> plt.Figure:
    """Plot data distribution with proper styling."""
    fig, ax = plt.subplots(figsize=figsize)

    sns.histplot(data=data, kde=True, ax=ax)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel("Value", fontsize=12)
    ax.set_ylabel("Frequency", fontsize=12)

    plt.tight_layout()
    return fig

# Use subplots for multiple visualizations
def plot_comparison(
    df: pd.DataFrame,
    x: str,
    y_columns: list[str]
) -> plt.Figure:
    """Compare multiple columns with subplots."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for idx, col in enumerate(y_columns):
        axes[idx].plot(df[x], df[col])
        axes[idx].set_title(f"{col} vs {x}")
        axes[idx].set_xlabel(x)
        axes[idx].set_ylabel(col)

    plt.tight_layout()
    return fig
```

### ✅ Efficient Data Loading

```python
import pandas as pd
import polars as pl
from pathlib import Path

def load_large_csv(path: Path, chunksize: int = 10000) -> pl.DataFrame:
    """Load large CSV efficiently with polars."""
    # Polars handles large files efficiently
    return pl.read_csv(path)

# For extremely large files, use chunking
def process_large_file(path: Path) -> pd.DataFrame:
    """Process extremely large files in chunks."""
    chunks = []
    for chunk in pd.read_csv(path, chunksize=10000):
        # Process chunk
        processed = transform_chunk(chunk)
        chunks.append(processed)

    return pd.concat(chunks, ignore_index=True)
```

### ✅ Type Hints for Data Science Code

```python
from typing import Protocol
import numpy as np

class DataFrameLike(Protocol):
    """Protocol for DataFrame-like objects."""
    def __getitem__(self, key) -> np.ndarray: ...
    def shape(self) -> Tuple[int, ...]: ...

def calculate_statistics(
    data: DataFrameLike,
    columns: Optional[list[str]] = None
) -> dict[str, float]:
    """Calculate statistics with type hints."""
    if columns is not None:
        data = data[columns]

    return {
        "mean": float(np.mean(data)),
        "std": float(np.std(data)),
        "min": float(np.min(data)),
        "max": float(np.max(data)),
    }
```

## Performance Optimization

### ✅ Choose the Right Tool

```python
# For small to medium datasets (< 1GB)
def medium_dataset() -> None:
    df = pd.read_csv("data.csv")
    result = df.groupby("category").sum()

# For large datasets (> 1GB)
def large_dataset() -> None:
    df = pl.read_csv("large_data.csv")
    result = df.group_by("category").agg(pl.all().sum())

# For numerical operations on arrays
def numerical_operations() -> None:
    arr = np.random.rand(1_000_000)
    result = np.fft.fft(arr)
```

### ✅ Memory Optimization

```python
import pandas as pd

def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Optimize DataFrame memory usage."""
    # Downcast numeric types
    for col in df.select_dtypes(include=['int64']):
        df[col] = pd.to_numeric(df[col], downcast='integer')

    for col in df.select_dtypes(include=['float64']):
        df[col] = pd.to_numeric(df[col], downcast='float')

    # Convert categorical strings
    for col in df.select_dtypes(include=['object']):
        if df[col].nunique() / len(df) < 0.5:
            df[col] = df[col].astype('category')

    return df
```

## Data Pipeline Patterns

### ✅ ETL Pattern

```python
from pathlib import Path
import polars as pl

def etl_pipeline(source: Path, output: Path) -> None:
    """Extract, transform, load pipeline."""
    # Extract
    raw_data = pl.read_csv(source)

    # Transform
    transformed = (
        raw_data.lazy()
        .filter(pl.col("status") == "active")
        .with_columns([
            pl.col("date").str.strptime(pl.Date, "%Y-%m-%d"),
            (pl.col("amount") * 1.1).alias("amount_with_tax")
        ])
        .collect()
    )

    # Load
    transformed.write_parquet(output)
```

### ✅ Data Validation

```python
from typing import Any, Dict
import pandas as pd

def validate_data(
    df: pd.DataFrame,
    schema: Dict[str, Any]
) -> bool:
    """Validate DataFrame against schema."""
    for col, expected_type in schema.items():
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

        if not df[col].dtype.name.startswith(expected_type):
            raise ValueError(
                f"Column {col} has type {df[col].dtype}, "
                f"expected {expected_type}"
            )

    return True
```

## Jupyter Notebook Best Practices

### ✅ Organized Notebooks

1. **Use markdown cells for documentation**
2. **Limit cell complexity (each cell does one thing)**
3. **Restart kernel regularly**
4. **Use `%timeit` for performance testing**
5. **Save important outputs to files, don't rely on notebook state**
6. **Version control .ipynb files or convert to scripts**

### ✅ Convert Notebooks to Scripts

```bash
# Convert notebook to Python script
jupyter nbconvert --to script notebook.ipynb

# Execute notebook as script
papermill notebook.ipynb output.ipynb
```

## Common Pitfalls

### ❌ Avoid Chained Indexing

```python
# BAD: Chained indexing can cause SettingWithCopyWarning
df[df["status"] == "active"]["value"] = 0

# GOOD: Use .loc or .copy()
df.loc[df["status"] == "active", "value"] = 0
```

### ❌ Don't Ignore Memory Usage

```python
# BAD: Loading entire dataset into memory
data = pd.read_csv("huge_file.csv")

# GOOD: Use chunking or polars
for chunk in pd.read_csv("huge_file.csv", chunksize=10000):
    process(chunk)
```

## References

- pandas documentation: https://pandas.pydata.org/docs/
- polars documentation: https://pola.rs/
- numpy documentation: https://numpy.org/doc/
- matplotlib documentation: https://matplotlib.org/stable/
- seaborn documentation: https://seaborn.pydata.org/
- Real Python pandas tutorials: https://realpython.com/pandas-python-explore-dataset/
