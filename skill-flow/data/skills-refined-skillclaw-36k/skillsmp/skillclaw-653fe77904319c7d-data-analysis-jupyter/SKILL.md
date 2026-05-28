---
name: data-analysis-jupyter
description: Use this skill when you need expert guidance for data analysis, visualization, and Jupyter Notebook development using pandas, matplotlib, seaborn, and numpy.
---

# Skill body

## Key Principles

- Write concise, technical responses with accurate Python examples.
- Prioritize reproducibility in data workflows.
- Favor functional programming approaches; minimize class-based solutions.
- Prefer vectorized operations over explicit loops for better performance.
- Employ descriptive variable names reflecting data content.
- Follow PEP 8 style guidelines for Python code.

## Data Analysis and Manipulation

- Leverage pandas for data manipulation and analytical tasks.
- Prefer method chaining for data transformations when possible.
- Use `loc` and `iloc` for explicit data selection.
- Utilize `groupby` operations for efficient data aggregation.
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
- Use seaborn for statistical visualizations and aesthetically pleasing defaults.
- Craft plots with informative labels, titles, and legends.
- Apply accessible color schemes considering color-blindness.
- Set appropriate figure sizes for the output medium.

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
- Maintain meaningful cell execution order ensuring reproducibility.
- Document analysis steps through explanatory markdown cells.
- Keep code cells focused and modular.
- Use magic commands like `%matplotlib inline` for inline plotting.
- Restart kernel and run all before sharing to verify reproducibility.

## Performance Optimization

- Profile slow operations to identify bottlenecks.
- Use categorical data types for low-cardinality strings.
- Consider chunked processing for large datasets.
- Cache intermediate results for efficiency.
- Utilize vectorized operations in pandas and numpy.

## Error Handling and Data Validation

- Implement data quality checks at the start of analysis.
- Validate data types and ranges.
- Use try-except blocks for error-prone operations.
- Document data assumptions and implement sanity checks.