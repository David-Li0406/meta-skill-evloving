---
name: data-visualization-and-inspection
description: Use this skill when you need to create visualizations from data files or inspect DataFrames by displaying their contents.
---

# Skill body

## Purpose

This skill **directly executes** visualizations. The calling agent provides a visualization specification along with data context, and the skill:
1. Infers the data loading code from the provided context.
2. Generates the complete plotting script.
3. Executes it via the `viz_runner.py` helper.
4. Returns artifact paths for the caller to reference.

**Key pattern:**
```
Caller (with data context) → Skill (infers data loading, generates script, executes) → Plot appears
```

The caller does NOT need to write any execution code. The skill handles everything.

## Input Specification

The calling agent should provide:

### Required
- **Visualization spec**: What to plot (chart type, axes, title, special features).

### Data Context (one of these forms)
- **Database + query**: "Data from `/full/path/to/operational_forecast.ddb`, table `forecast`, columns month, members".
- **SQL query**: "Run this SQL: `SELECT * FROM forecast WHERE year >= 2024`".
- **Code snippet**: "Load data like this: `df = pd.read_parquet('/full/path/to/data.parquet')`".
- **File path**: "CSV at `/tmp/data.csv` with columns X, Y, Z".

**CRITICAL: Absolute Paths Required**

The `viz_runner.py` executes scripts from `/tmp/viz/`, NOT the caller's working directory. All file paths in generated scripts MUST be absolute paths. The calling agent should:
1. Determine the absolute path to any data files before invoking the skill.
2. Pass the full absolute path in the data context.
3. Never use relative paths like `./data.ddb` or `data.parquet`.

Example - WRONG:
```python
con = duckdb.connect('operational_forecast.ddb')  # Will fail!
```

Example - CORRECT:
```python
con = duckdb.connect('/Users/rob/projects/forecast/operational_forecast.ddb')
```

### Optional
- **Suggested ID**: A name hint (e.g., `pop_bar`, `churn_trend`). The runner ensures uniqueness.

## Intent Detection

**Before generating any code, analyze the user's request to determine the appropriate mode.**

### Inspection Mode (use `--show`)
Use when the user wants to display the data, such as showing the first N rows, column names, and dtypes.