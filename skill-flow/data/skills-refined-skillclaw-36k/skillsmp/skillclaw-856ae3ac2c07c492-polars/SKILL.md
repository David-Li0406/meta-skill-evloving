---
name: polars
description: Use this skill when you need a fast in-memory DataFrame library for datasets that fit in RAM, especially when pandas is too slow.
---

# Polars

## Overview

Polars is a lightning-fast DataFrame library for Python and Rust built on Apache Arrow. It features an expression-based API, lazy evaluation framework, and high-performance data manipulation capabilities for efficient data processing, pandas migration, and data pipeline optimization.

## Quick Start

### Installation and Basic Usage

Install Polars:
```python
pip install polars
```

Basic DataFrame creation and operations:
```python
import polars as pl

# Create DataFrame
df = pl.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["NY", "LA", "SF"]
})

# Select columns
df.select("name", "age")

# Filter rows
df.filter(pl.col("age") > 25)

# Add computed columns
df.with_columns(
    age_plus_10=pl.col("age") + 10
)
```

## Core Concepts

### Expressions

Expressions are the fundamental building blocks of Polars operations. They describe transformations on data and can be composed, reused, and optimized.

**Key principles:**
- Use `pl.col("column_name")` to reference columns.
- Chain methods to build complex transformations.
- Expressions are lazy and only execute within contexts (select, with_columns, filter, group_by).

**Example:**
```python
# Expression-based computation
df.select(
    pl.col("name"),
    (pl.col("age") * 12).alias("age_in_months")
)
```

### Lazy vs Eager Evaluation

**Eager (DataFrame):** Operations execute immediately.
```python
df = pl.read_csv("file.csv")  # Reads immediately
result = df.filter(pl.col("age") > 25)  # Executes immediately
```

**Lazy (LazyFrame):** Operations build a query plan, optimized before execution.
```python
lf = pl.scan_csv("file.csv")  # Doesn't read yet
result = lf.filter(pl.col("age") > 25).select("name", "age")
df = result.collect()  # Now executes optimized query
```

**When to use lazy:**
- Working with large datasets.
- Complex query pipelines.
- When only some columns/rows are needed.
- Performance is critical.

**Benefits of lazy evaluation:**
- Automatic query optimization.
- Predicate pushdown.
- Projection pushdown.