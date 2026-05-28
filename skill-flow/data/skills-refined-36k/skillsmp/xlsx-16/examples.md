# XLSX Code Examples

## 1. Create Financial Model

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = Workbook()
ws = wb.active
ws.title = "Financial Model"

# Headers with formatting
headers = ["", "2024", "2025", "2026"]
for col, header in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col, value=header)
    cell.font = Font(bold=True)
    cell.alignment = Alignment(horizontal='center')

# Revenue row (blue for inputs)
ws['A2'] = "Revenue ($mm)"
ws['B2'] = 100  # Input
ws['B2'].font = Font(color='0000FF')  # Blue for input
ws['C2'] = '=B2*1.1'  # 10% growth formula
ws['D2'] = '=C2*1.1'

# Costs row
ws['A3'] = "Costs ($mm)"
ws['B3'] = '=B2*0.6'  # 60% of revenue
ws['C3'] = '=C2*0.6'
ws['D3'] = '=D2*0.6'

# Profit row
ws['A4'] = "Profit ($mm)"
ws['B4'] = '=B2-B3'
ws['C4'] = '=C2-C3'
ws['D4'] = '=D2-D3'

wb.save('financial_model.xlsx')
```

## 2. Data Analysis with pandas

```python
import pandas as pd

# Read and analyze
df = pd.read_excel('sales_data.xlsx')
print(df.describe())

# Pivot table
pivot = df.pivot_table(
    values='Amount',
    index='Region',
    columns='Quarter',
    aggfunc='sum'
)

# Save with multiple sheets
with pd.ExcelWriter('analysis.xlsx') as writer:
    df.to_excel(writer, sheet_name='Raw Data', index=False)
    pivot.to_excel(writer, sheet_name='Pivot')
```

## 3. Format Existing File

```python
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Border, Side

wb = load_workbook('data.xlsx')
ws = wb.active

# Apply currency format
for row in ws.iter_rows(min_row=2, min_col=2, max_col=4):
    for cell in row:
        cell.number_format = '$#,##0'

# Highlight negative values
red_fill = PatternFill(start_color='FFCCCC', fill_type='solid')
for row in ws.iter_rows(min_row=2):
    for cell in row:
        if isinstance(cell.value, (int, float)) and cell.value < 0:
            cell.fill = red_fill

wb.save('formatted_data.xlsx')
```

## 4. Conditional Formulas

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

# Sample data
ws['A1'] = 'Score'
ws['B1'] = 'Grade'
for i, score in enumerate([95, 82, 67, 55, 88], 2):
    ws[f'A{i}'] = score
    # Nested IF for grading
    ws[f'B{i}'] = f'=IF(A{i}>=90,"A",IF(A{i}>=80,"B",IF(A{i}>=70,"C",IF(A{i}>=60,"D","F"))))'

wb.save('grades.xlsx')
```

## 5. Charts

```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference

wb = Workbook()
ws = wb.active

# Data
data = [
    ['Month', 'Sales'],
    ['Jan', 100],
    ['Feb', 120],
    ['Mar', 140],
    ['Apr', 130],
]
for row in data:
    ws.append(row)

# Create chart
chart = BarChart()
chart.title = "Monthly Sales"
chart.x_axis.title = "Month"
chart.y_axis.title = "Sales ($)"

data = Reference(ws, min_col=2, min_row=1, max_row=5)
categories = Reference(ws, min_col=1, min_row=2, max_row=5)
chart.add_data(data, titles_from_data=True)
chart.set_categories(categories)

ws.add_chart(chart, "D2")
wb.save('chart_example.xlsx')
```

## 6. Data Validation

```python
from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation

wb = Workbook()
ws = wb.active

# Create dropdown
dv = DataValidation(
    type="list",
    formula1='"Yes,No,Maybe"',
    allow_blank=True
)
dv.error = "Please select from the dropdown"
dv.errorTitle = "Invalid Input"

ws.add_data_validation(dv)
dv.add('B2:B100')  # Apply to range

ws['A1'] = 'Response'
ws['B1'] = 'Select One'
wb.save('validation_example.xlsx')
```

## 7. Merge and Style Headers

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill

wb = Workbook()
ws = wb.active

# Merge cells for header
ws.merge_cells('A1:D1')
ws['A1'] = 'Quarterly Sales Report'
ws['A1'].font = Font(bold=True, size=16)
ws['A1'].alignment = Alignment(horizontal='center')
ws['A1'].fill = PatternFill(start_color='366092', fill_type='solid')

wb.save('merged_header.xlsx')
```

## 8. Working with Named Ranges

```python
from openpyxl import Workbook
from openpyxl.workbook.defined_name import DefinedName

wb = Workbook()
ws = wb.active

# Create data
ws['A1'] = 'Rate'
ws['B1'] = 0.05

# Define named range
ref = f"'{ws.title}'!$B$1"
defn = DefinedName("InterestRate", attr_text=ref)
wb.defined_names.add(defn)

# Use in formula
ws['A3'] = 'Principal'
ws['B3'] = 1000
ws['A4'] = 'Interest'
ws['B4'] = '=B3*InterestRate'

wb.save('named_ranges.xlsx')
```
