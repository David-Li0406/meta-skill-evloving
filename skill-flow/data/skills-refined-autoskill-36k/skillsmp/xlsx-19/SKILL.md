---
name: xlsx
description: Work with Excel spreadsheets (XLSX/XLS/CSV) - read data, create spreadsheets, convert formats, analyze data, and generate reports. Use when the user asks to work with Excel files or spreadsheet data.
allowed-tools: Read, Bash, Write
---

# Excel (XLSX) Processing Skill

When working with Excel spreadsheets, follow these guidelines:

## 1. Reading & Extracting from XLSX

**Extract to CSV**:
```bash
# Using ssconvert (from gnumeric)
ssconvert input.xlsx output.csv

# Specific sheet
ssconvert -S input.xlsx output.csv

# Using LibreOffice
libreoffice --headless --convert-to csv input.xlsx
```

**Read with Python (recommended)**:
```python
import openpyxl

# Load workbook
wb = openpyxl.load_workbook('data.xlsx')

# Get sheet
sheet = wb.active
# or by name: sheet = wb['Sheet1']

# Read all data
for row in sheet.iter_rows(values_only=True):
    print(row)

# Read specific cell
value = sheet['A1'].value

# Read range
for row in sheet['A1:C10']:
    for cell in row:
        print(cell.value)
```

**Using pandas**:
```python
import pandas as pd

# Read entire sheet
df = pd.read_excel('data.xlsx')

# Read specific sheet
df = pd.read_excel('data.xlsx', sheet_name='Sales')

# Read all sheets
dfs = pd.read_excel('data.xlsx', sheet_name=None)

# Read with specific columns
df = pd.read_excel('data.xlsx', usecols=['Name', 'Age', 'City'])

# Skip rows
df = pd.read_excel('data.xlsx', skiprows=2)
```

## 2. Creating XLSX Files

**From CSV**:
```bash
# Using ssconvert
ssconvert input.csv output.xlsx

# Using LibreOffice
libreoffice --headless --convert-to xlsx input.csv
```

**Using Python (openpyxl)**:
```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

# Create new workbook
wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = 'Data'

# Write headers
headers = ['Name', 'Age', 'City']
sheet.append(headers)

# Style headers
for cell in sheet[1]:
    cell.font = Font(bold=True)
    cell.fill = PatternFill(start_color='366092', fill_type='solid')
    cell.font = Font(color='FFFFFF', bold=True)

# Add data
data = [
    ['John Doe', 30, 'New York'],
    ['Jane Smith', 25, 'London'],
    ['Bob Johnson', 35, 'Paris']
]

for row in data:
    sheet.append(row)

# Auto-adjust column width
for column in sheet.columns:
    max_length = 0
    column_letter = column[0].column_letter
    for cell in column:
        if cell.value:
            max_length = max(max_length, len(str(cell.value)))
    sheet.column_dimensions[column_letter].width = max_length + 2

# Save
wb.save('output.xlsx')
```

**Using pandas**:
```python
import pandas as pd

# From DataFrame
df = pd.DataFrame({
    'Name': ['John', 'Jane', 'Bob'],
    'Age': [30, 25, 35],
    'City': ['New York', 'London', 'Paris']
})

# Save to Excel
df.to_excel('output.xlsx', index=False, sheet_name='Data')

# Multiple sheets
with pd.ExcelWriter('output.xlsx') as writer:
    df1.to_excel(writer, sheet_name='Sheet1', index=False)
    df2.to_excel(writer, sheet_name='Sheet2', index=False)
```

## 3. Converting Excel Files

**XLSX to CSV**:
```bash
# All sheets to separate CSV files
ssconvert -S input.xlsx output.csv

# Specific sheet
libreoffice --headless --convert-to csv:"Text - txt - csv (StarCalc)":44,34,UTF8 input.xlsx
```

**XLSX to JSON**:
```python
import pandas as pd
import json

# Read Excel
df = pd.read_excel('data.xlsx')

# Convert to JSON
json_data = df.to_json(orient='records', indent=2)

# Save to file
with open('output.json', 'w') as f:
    f.write(json_data)
```

**XLSX to PDF**:
```bash
# Using LibreOffice
libreoffice --headless --convert-to pdf input.xlsx
```

**XLS to XLSX**:
```bash
# Using LibreOffice
libreoffice --headless --convert-to xlsx input.xls
```

## 4. Data Analysis

**Basic statistics**:
```python
import pandas as pd

df = pd.read_excel('data.xlsx')

# Summary statistics
print(df.describe())

# Column info
print(df.info())

# Value counts
print(df['Category'].value_counts())

# Group by and aggregate
summary = df.groupby('Category').agg({
    'Sales': ['sum', 'mean', 'count'],
    'Profit': 'sum'
})
print(summary)
```

**Find duplicates**:
```python
import pandas as pd

df = pd.read_excel('data.xlsx')

# Find duplicate rows
duplicates = df[df.duplicated()]
print(f"Found {len(duplicates)} duplicates")

# Find duplicates based on specific columns
duplicates = df[df.duplicated(subset=['Email'], keep=False)]
```

**Data validation**:
```python
import pandas as pd

df = pd.read_excel('data.xlsx')

# Check for missing values
missing = df.isnull().sum()
print("Missing values per column:")
print(missing[missing > 0])

# Check data types
print(df.dtypes)

# Find outliers (using IQR method)
Q1 = df['Sales'].quantile(0.25)
Q3 = df['Sales'].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df['Sales'] < Q1 - 1.5*IQR) | (df['Sales'] > Q3 + 1.5*IQR)]
```

## 5. Formulas & Calculations

**Add formulas**:
```python
import openpyxl

wb = openpyxl.load_workbook('data.xlsx')
sheet = wb.active

# Add SUM formula
sheet['D10'] = '=SUM(D2:D9)'

# Add AVERAGE
sheet['D11'] = '=AVERAGE(D2:D9)'

# Add IF statement
sheet['E2'] = '=IF(D2>100,"High","Low")'

# Add VLOOKUP
sheet['F2'] = '=VLOOKUP(A2,Sheet2!A:B,2,FALSE)'

wb.save('data.xlsx')
```

## 6. Formatting & Styling

**Cell formatting**:
```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.styles.numbers import FORMAT_NUMBER_00, FORMAT_PERCENTAGE_00

wb = openpyxl.load_workbook('data.xlsx')
sheet = wb.active

# Font styling
cell = sheet['A1']
cell.font = Font(name='Arial', size=14, bold=True, color='FF0000')

# Background color
cell.fill = PatternFill(start_color='FFFF00', fill_type='solid')

# Borders
border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)
cell.border = border

# Alignment
cell.alignment = Alignment(horizontal='center', vertical='center')

# Number format
sheet['B2'].number_format = FORMAT_NUMBER_00  # 1234.00
sheet['C2'].number_format = FORMAT_PERCENTAGE_00  # 50.00%
sheet['D2'].number_format = 'mm/dd/yyyy'  # Date

wb.save('data.xlsx')
```

**Conditional formatting**:
```python
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, DataBarRule
from openpyxl.styles import PatternFill

# Highlight cells > 100
red_fill = PatternFill(start_color='FFC7CE', fill_type='solid')
rule = CellIsRule(operator='greaterThan', formula=['100'], fill=red_fill)
sheet.conditional_formatting.add('D2:D100', rule)

# Color scale (red to green)
color_scale = ColorScaleRule(
    start_type='min', start_color='F8696B',
    mid_type='percentile', mid_value=50, mid_color='FFEB84',
    end_type='max', end_color='63BE7B'
)
sheet.conditional_formatting.add('D2:D100', color_scale)

# Data bars
data_bar = DataBarRule(start_type='min', end_type='max', color='638EC6')
sheet.conditional_formatting.add('D2:D100', data_bar)
```

## 7. Charts & Visualizations

**Create charts**:
```python
from openpyxl.chart import BarChart, LineChart, PieChart, Reference

wb = openpyxl.load_workbook('data.xlsx')
sheet = wb.active

# Bar chart
chart = BarChart()
chart.title = 'Sales by Category'
chart.x_axis.title = 'Category'
chart.y_axis.title = 'Sales'

data = Reference(sheet, min_col=2, min_row=1, max_row=10)
categories = Reference(sheet, min_col=1, min_row=2, max_row=10)

chart.add_data(data, titles_from_data=True)
chart.set_categories(categories)

sheet.add_chart(chart, 'E5')

# Line chart
line_chart = LineChart()
line_chart.title = 'Trend Over Time'
line_chart.add_data(data, titles_from_data=True)
line_chart.set_categories(categories)

# Pie chart
pie = PieChart()
pie.title = 'Market Share'
pie.add_data(data, titles_from_data=True)
pie.set_categories(categories)

wb.save('data.xlsx')
```

## 8. Working with Multiple Sheets

**Manage sheets**:
```python
import openpyxl

wb = openpyxl.load_workbook('data.xlsx')

# Create new sheet
new_sheet = wb.create_sheet('Summary')

# List all sheets
print(wb.sheetnames)

# Access specific sheet
sheet = wb['Sheet1']

# Copy sheet
source = wb['Sheet1']
target = wb.copy_worksheet(source)
target.title = 'Sheet1_Copy'

# Delete sheet
del wb['OldSheet']

# Reorder sheets
wb.move_sheet('Summary', offset=-1)

wb.save('data.xlsx')
```

## 9. Common Workflows

### Merge multiple Excel files
```python
import pandas as pd
import glob

# Read all Excel files
files = glob.glob('data/*.xlsx')

dfs = []
for file in files:
    df = pd.read_excel(file)
    dfs.append(df)

# Combine
combined = pd.concat(dfs, ignore_index=True)

# Save
combined.to_excel('merged.xlsx', index=False)
```

### Create pivot table
```python
import pandas as pd

df = pd.read_excel('sales.xlsx')

# Create pivot table
pivot = pd.pivot_table(
    df,
    values='Sales',
    index='Category',
    columns='Region',
    aggfunc='sum',
    margins=True
)

pivot.to_excel('pivot.xlsx')
```

### Generate report from template
```python
import openpyxl
from datetime import datetime

# Load template
wb = openpyxl.load_workbook('template.xlsx')
sheet = wb.active

# Fill in data
sheet['B2'] = datetime.now().strftime('%Y-%m-%d')
sheet['B3'] = 'Q1 2026'
sheet['B4'] = 'Sales Department'

# Add calculated values
sheet['D10'] = '=SUM(D2:D9)'

# Save with new name
wb.save(f'report_{datetime.now().strftime("%Y%m%d")}.xlsx')
```

## Tools Required

Install necessary tools:

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get install python3-pip libreoffice gnumeric
pip3 install openpyxl pandas xlrd xlsxwriter
```

**macOS**:
```bash
brew install libreoffice
pip3 install openpyxl pandas xlrd xlsxwriter
```

**Windows**:
```powershell
pip install openpyxl pandas xlrd xlsxwriter
# Install LibreOffice manually
```

## Security Notes

- ✅ Validate file paths and extensions
- ✅ Check file sizes before loading
- ✅ Sanitize user input in formulas (prevent formula injection)
- ✅ Be cautious with macro-enabled files (.xlsm)
- ✅ Validate data types and ranges
- ✅ Don't execute external links automatically
- ✅ Use read-only mode when just analyzing

## When to Use This Skill

Use `/xlsx` when the user:
- Wants to read data from Excel files
- Needs to create spreadsheets from data
- Wants to convert between Excel/CSV/JSON formats
- Asks to analyze or validate spreadsheet data
- Needs to generate reports from templates
- Wants to add formulas or formatting
- Asks to merge or split Excel files
- Needs to create charts or pivot tables

Always preview changes before saving over existing files.
