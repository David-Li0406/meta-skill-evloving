---
name: ai-data-analyst
description: Use this skill when you need to perform comprehensive data analysis, statistical modeling, and data visualization through self-contained Python scripts.
---

# Skill body

## Purpose

Perform comprehensive data analysis, statistical modeling, and data visualization by writing and executing self-contained Python scripts. Generate publication-quality charts, statistical reports, and actionable insights from data files or databases.

## When to use this skill

- You need to **analyze datasets** to understand patterns, trends, or relationships.
- You want to perform **statistical tests** or build predictive models.
- You need **data visualizations** (charts, graphs, dashboards) to communicate findings.
- You're doing **exploratory data analysis** (EDA) to understand data structure and quality.
- You need to **clean, transform, or merge** datasets for analysis.
- You want **reproducible analysis** with documented methodology and code.
- You are performing **Convex Backend Engineering** (schema design, query optimization, log analysis).

## Key capabilities

Unlike point-solution data analysis tools:

- **Convex Engineering Integration**: Native support for Convex MCP tools (`mcp_convex`) and CLI.
- **Full Python ecosystem**: Access to pandas, numpy, scikit-learn, statsmodels, matplotlib, seaborn, plotly, and more.
- **Runs locally**: Your data stays on your machine; no uploads to third-party services.
- **Reproducible**: All analysis is code-based and version controllable.
- **Customizable**: Extend with any Python library or custom analysis logic.
- **Publication-quality output**: Generate professional charts and reports.
- **Statistical rigor**: Access to comprehensive statistical and ML libraries.

## Inputs

- **Data sources**: CSV files, Excel files, JSON, Parquet, or database connections.
- **Analysis goals**: Questions to answer or hypotheses to test.
- **Variables of interest**: Specific columns, metrics, or dimensions to focus on.
- **Output preferences**: Chart types, report format, statistical tests needed.
- **Context**: Business domain, data dictionary, or known data quality issues.

## Out of scope

- Real-time streaming data analysis (use appropriate streaming tools).
- Extremely large datasets requiring distributed computing (use Spark/Dask instead).