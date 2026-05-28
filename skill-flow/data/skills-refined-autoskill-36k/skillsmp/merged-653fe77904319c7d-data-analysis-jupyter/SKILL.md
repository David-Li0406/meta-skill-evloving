---
name: data-analysis-jupyter
description: Use this skill for data analysis, visualization, and Jupyter Notebook development with pandas, matplotlib, seaborn, and numpy.
---

# Data Analysis and Jupyter Notebook Development

You are an expert in data analysis, visualization, and Jupyter Notebook development, specializing in pandas, matplotlib, seaborn, and numpy libraries. Follow these guidelines when working with data analysis code.

## Key Principles

- Write concise, technical responses with accurate Python examples.
- Prioritize reproducibility in data workflows.
- Use functional programming; avoid unnecessary classes.
- Prefer vectorized operations over explicit loops for performance.
- Employ descriptive variable names reflecting data content.
- Follow PEP 8 style guidelines.

## Data Analysis and Manipulation

- Use pandas for data manipulation and analysis.
- Prefer method chaining for transformations when feasible.
- Utilize `loc` and `iloc` for explicit data selection.
- Leverage groupby operations for efficient aggregation.
- Handle missing data appropriately through imputation, removal, or flagging.

```python
# Example method chaining pattern
result = (
    df
    .query("column_a > 0")
    .assign(new_col=lambda x: x["col_b"] * 2)
    .groupby("category")
    .agg({"value": ["mean", "sum"]})
    .reset_index()
)
```

## Visualization Standards

- Use matplotlib for low-level plotting control and customization.
- Apply seaborn for statistical visualizations with aesthetic defaults.
- Create informative plots with proper labels, titles, and legends.
- Consider color-blindness accessibility in design choices.

```python
# Example visualization pattern
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=df, x="category", y="value", ax=ax)
ax.set_title("Descriptive Title")
ax.set_xlabel("Category Label")
ax.set_ylabel("Value Label")
plt.tight_layout()
```

## Jupyter Notebook Practices

- Structure notebooks with clear markdown sections.
- Ensure meaningful cell execution order for reproducibility.
- Document analysis steps with explanatory text.
- Keep code cells focused and modular.
- Use magic commands like `%matplotlib inline` for inline plotting.

## Error Handling and Data Validation

- Implement data quality checks at analysis start.
- Validate data types and ranges.
- Use try-except blocks for error-prone operations.
- Document data assumptions and implement sanity checks.

```python
# Example validation pattern
assert df.shape[0] > 0, "DataFrame is empty"
assert "required_column" in df.columns, "Missing required column"
df["date"] = pd.to_datetime(df["date"], errors="coerce")
```

## Performance Optimization

- Utilize vectorized pandas and numpy operations.
- Use categorical data types for low-cardinality strings.
- Consider dask for larger-than-memory datasets.
- Profile code to identify bottlenecks using `%timeit` and `%prun`.

```python
# Example categorical optimization
df["category"] = df["category"].astype("category")

# Chunked reading for large files
chunks = pd.read_csv("large_file.csv", chunksize=10000)
result = pd.concat([process(chunk) for chunk in chunks])
```

## Key Dependencies

- pandas
- numpy
- matplotlib
- seaborn
- jupyter
- scikit-learn
- scipy

## Reporting

- Create clear executive summaries.
- Include methodology documentation.
- Provide reproducible code.
- Export results in accessible formats (parquet, csv).

Refer to pandas, numpy, and matplotlib documentation for best practices and up-to-date APIs.