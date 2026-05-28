# Excel Workflow Examples

Complete working examples for common Excel tasks.

## Create Simple Report

```python
import pandas as pd

# Load data
df = pd.read_csv('sales_data.csv')

# Analyze
summary = df.pivot_table(
    values='Revenue',
    index='Region',
    columns='Product',
    aggfunc='sum'
)

# Export to Excel
with pd.ExcelWriter('sales_report.xlsx', engine='openpyxl') as writer:
    summary.to_excel(writer, sheet_name='Summary')
    df.to_excel(writer, sheet_name='Raw Data', index=False)
```

**Verify:** `python scripts/recalc.py sales_report.xlsx`

## Create Financial Model

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

wb = Workbook()
ws = wb.active
ws.title = 'Revenue Model'

# Headers
ws['A1'] = 'Year'
ws['B1'] = 'Revenue ($mm)'
ws['C1'] = 'Growth Rate'

# Assumptions (blue text, yellow background)
ws['A2'] = 'Assumptions'
ws['B2'] = 'Base Revenue'
ws['C2'] = 100
ws['C2'].font = Font(color='0000FF')
ws['C2'].fill = PatternFill(start_color='FFFF00', fill_type='solid')

ws['B3'] = 'Growth Rate'
ws['C3'] = 0.15
ws['C3'].font = Font(color='0000FF')
ws['C3'].fill = PatternFill(start_color='FFFF00', fill_type='solid')

# Projections (black text for formulas)
ws['A5'] = '2024'
ws['B5'] = '=C2'
ws['B5'].font = Font(color='000000')

ws['A6'] = '2025'
ws['B6'] = '=B5*(1+$C$3)'
ws['B6'].font = Font(color='000000')

ws['A7'] = '2026'
ws['B7'] = '=B6*(1+$C$3)'
ws['B7'].font = Font(color='000000')

# Format numbers
for row in range(5, 8):
    ws[f'B{row}'].number_format = '#,##0.0'

wb.save('revenue_model.xlsx')
```

**Verify:** `python scripts/recalc.py revenue_model.xlsx`

## Analyze Existing File

```python
from openpyxl import load_workbook
import pandas as pd

# Load with openpyxl to inspect formulas
wb = load_workbook('existing.xlsx')
ws = wb['Sales']

# Check for formulas
for row in ws.iter_rows(min_row=1, max_row=10):
    for cell in row:
        if cell.value and isinstance(cell.value, str) and cell.value.startswith('='):
            print(f'{cell.coordinate}: {cell.value}')

# Load with pandas for data analysis
df = pd.read_excel('existing.xlsx', sheet_name='Sales')
print(df.describe())
```

## Create Charts

```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference

wb = Workbook()
ws = wb.active

# Data
rows = [
    ['Product', 'Sales'],
    ['A', 100],
    ['B', 150],
    ['C', 200],
]

for row in rows:
    ws.append(row)

# Create bar chart
chart = BarChart()
chart.title = 'Sales by Product'
chart.x_axis.title = 'Product'
chart.y_axis.title = 'Sales'

data = Reference(ws, min_col=2, min_row=1, max_row=4)
cats = Reference(ws, min_col=1, min_row=2, max_row=4)

chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)

ws.add_chart(chart, 'D2')

wb.save('chart_example.xlsx')
```

**Verify:** `python scripts/recalc.py chart_example.xlsx`

## Merge Data from Multiple Sources

```python
import pandas as pd

# Read multiple files
sales = pd.read_excel('sales.xlsx')
customers = pd.read_excel('customers.xlsx')

# Merge data
merged = pd.merge(sales, customers, on='customer_id', how='left')

# Analyze
summary = merged.groupby('region').agg({
    'revenue': 'sum',
    'quantity': 'sum',
    'customer_id': 'nunique'
})

# Export
with pd.ExcelWriter('merged_report.xlsx', engine='openpyxl') as writer:
    merged.to_excel(writer, sheet_name='All Data', index=False)
    summary.to_excel(writer, sheet_name='Summary')
```

**Verify:** `python scripts/recalc.py merged_report.xlsx`

## Create Dashboard

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, Reference

wb = Workbook()
ws = wb.active
ws.title = 'Dashboard'

# Title
ws.merge_cells('A1:E1')
ws['A1'] = 'Sales Dashboard'
ws['A1'].font = Font(size=18, bold=True)
ws['A1'].alignment = Alignment(horizontal='center')

# KPIs
kpi_headers = ['Metric', 'Value', 'Target', 'Status']
for col, header in enumerate(kpi_headers, start=1):
    cell = ws.cell(row=3, column=col)
    cell.value = header
    cell.font = Font(bold=True)
    cell.fill = PatternFill(start_color='366092', fill_type='solid')

# Sample KPI data
kpis = [
    ['Total Revenue', 1250000, 1000000, '✓'],
    ['New Customers', 450, 500, '✗'],
    ['Avg Order Value', 2500, 2000, '✓'],
]

for row_idx, kpi in enumerate(kpis, start=4):
    for col_idx, value in enumerate(kpi, start=1):
        ws.cell(row=row_idx, column=col_idx, value=value)

wb.save('dashboard.xlsx')
```

**Verify:** `python scripts/recalc.py dashboard.xlsx`

## Time Series Analysis

```python
import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference

# Generate sample data
dates = pd.date_range('2024-01-01', periods=12, freq='MS')
revenue = [100, 105, 110, 108, 115, 120, 125, 130, 128, 135, 140, 145]

# Create workbook
wb = Workbook()
ws = wb.active

# Write data
ws['A1'] = 'Month'
ws['B1'] = 'Revenue'

for idx, (date, rev) in enumerate(zip(dates, revenue), start=2):
    ws[f'A{idx}'] = date
    ws[f'A{idx}'].number_format = 'yyyy-mm'
    ws[f'B{idx}'] = rev

# Create line chart
chart = LineChart()
chart.title = 'Revenue Trend'
chart.x_axis.title = 'Month'
chart.y_axis.title = 'Revenue ($000)'

data = Reference(ws, min_col=2, min_row=1, max_row=13)
dates_ref = Reference(ws, min_col=1, min_row=2, max_row=13)

chart.add_data(data, titles_from_data=True)
chart.set_categories(dates_ref)

ws.add_chart(chart, 'D2')

wb.save('time_series.xlsx')
```

**Verify:** `python scripts/recalc.py time_series.xlsx`

## Budget vs Actuals

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

wb = Workbook()
ws = wb.active
ws.title = 'Budget vs Actuals'

# Headers
headers = ['Category', 'Budget', 'Actual', 'Variance', 'Variance %']
for col, header in enumerate(headers, start=1):
    ws.cell(row=1, column=col, value=header).font = Font(bold=True)

# Sample data
categories = ['Revenue', 'COGS', 'Operating Expenses', 'Net Income']
budgets = [1000000, 400000, 300000, 300000]
actuals = [1100000, 420000, 280000, 400000]

# Write data with formulas
for row, (cat, budget, actual) in enumerate(zip(categories, budgets, actuals), start=2):
    ws[f'A{row}'] = cat
    ws[f'B{row}'] = budget
    ws[f'C{row}'] = actual
    ws[f'D{row}'] = f'=C{row}-B{row}'  # Formula for variance
    ws[f'E{row}'] = f'=IF(B{row}=0,"-",D{row}/B{row})'  # Formula for variance %

    # Format numbers
    ws[f'B{row}'].number_format = '$#,##0'
    ws[f'C{row}'].number_format = '$#,##0'
    ws[f'D{row}'].number_format = '$#,##0;[Red]($#,##0)'
    ws[f'E{row}'].number_format = '0.0%;[Red]-0.0%'

wb.save('budget_actuals.xlsx')
```

**Verify:** `python scripts/recalc.py budget_actuals.xlsx`
