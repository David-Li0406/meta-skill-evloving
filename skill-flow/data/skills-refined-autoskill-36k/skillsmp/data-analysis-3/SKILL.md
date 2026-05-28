---
name: data-analysis
description: Data analysis workflows and patterns for processing, analyzing, and visualizing data using Python data science libraries.
version: 1.0.0
author: AIECS Team
tags:
  - data
  - analysis
  - pandas
  - visualization
  - statistics
dependencies: []
recommended_tools:
  - python
  - pandas
  - numpy
  - matplotlib
scripts:
  validate-data:
    path: scripts/validate-data.py
    mode: native
    description: Validates data file format and structure
    parameters:
      file_path:
        type: string
        required: true
        description: Path to the data file to validate
      format:
        type: string
        required: false
        description: Expected data format (csv, json, parquet)
---

# Data Analysis Skill

This skill provides guidance and tools for data analysis workflows using Python's data science ecosystem.

## When to Use This Skill

Use this skill when you need to:

- Load and explore datasets from various file formats
- Clean and preprocess data for analysis
- Perform statistical analysis and compute metrics
- Create visualizations to understand data patterns
- Transform and aggregate data for reporting

## Supported Data Formats

This skill supports the following data formats:

| Format | Extension | Library |
|--------|-----------|---------|
| CSV | `.csv` | pandas |
| JSON | `.json` | pandas |
| Parquet | `.parquet` | pandas + pyarrow |
| Excel | `.xlsx`, `.xls` | pandas + openpyxl |
| SQL | Database connection | pandas + sqlalchemy |

## Analysis Workflow Overview

A typical data analysis workflow follows these steps:

1. **Data Loading**: Read data from files or databases into pandas DataFrames
2. **Data Inspection**: Explore structure, types, and basic statistics
3. **Data Cleaning**: Handle missing values, duplicates, and outliers
4. **Data Transformation**: Reshape, aggregate, and derive new features
5. **Statistical Analysis**: Compute descriptive and inferential statistics
6. **Visualization**: Create charts and plots to communicate insights
7. **Export Results**: Save processed data and analysis outputs

## Quick Start

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('data.csv')

# Explore
print(df.info())
print(df.describe())

# Visualize
df.plot(kind='hist')
plt.show()
```

## Available Scripts

- **validate-data**: Validates data file format and structure before analysis

