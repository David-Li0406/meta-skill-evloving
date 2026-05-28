---
name: excel-analysis
description: Use this skill when you need to analyze Excel files, create pivot tables, generate charts, or perform data analysis on spreadsheets and tabular data.
---

# Skill body

## Quick start

Read Excel files with pandas:

```python
import pandas as pd

# Read Excel file
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")

# Display first few rows
print(df.head())

# Basic statistics
print(df.describe())
```

## Reading multiple sheets

Process all sheets in a workbook:

```python
import pandas as pd

# Read all sheets
excel_file = pd.ExcelFile("workbook.xlsx")

for sheet_name in excel_file.sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    print(f"\n{sheet_name}:")
    print(df.head())
```

## Data analysis

Perform common analysis tasks:

```python
import pandas as pd

df = pd.read_excel("sales.xlsx")

# Group by and aggregate
sales_by_region = df.groupby("region")["sales"].sum()
print(sales_by_region)

# Filter data
high_sales = df[df["sales"] > 10000]

# Calculate metrics
df["profit_margin"] = (df["revenue"] - df["cost"]) / df["revenue"]

# Sort by column
df_sorted = df.sort_values("sales", ascending=False)
```

## Creating Excel files

Write data to Excel with formatting:

```python
import pandas as pd

df = pd.DataFrame({
    "Product": ["A", "B", "C"],
    "Sales": [100, 200, 150],
    "Profit": [20, 40, 30]
})

# Write to Excel
writer = pd.ExcelWriter("output.xlsx", engine="openpyxl")
df.to_excel(writer, sheet_name="Sales", index=False)

# Get worksheet for formatting
worksheet = writer.sheets["Sales"]

# Auto-adjust column widths
for column in worksheet.columns:
    max_length = 0
    column_letter = column[0].column_letter
    for cell in column:
        if len(str(cell.value)) > max_length:
            max_length = len(str(cell.value))
    worksheet.column_dimensions[column_letter].width = max_length + 2

writer.close()
```

## Pivot tables

Create pivot tables programmatically:

```python
import pandas as pd

df = pd.read_excel("sales_data.xlsx")

# Create pivot table
pivot = pd.pivot_table(
    df,
    values="sales",
    index="region",
    columns="product",
    aggfunc="sum",
    fill_value=0
)

print(pivot)

# Save pivot table
pivot.to_excel("pivot_report.xlsx")
```

## Charts and visualization

Generate charts from Excel data:

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("data.xlsx")

# Create bar chart
df.plot(x="category", kind="bar")
plt.show()
```