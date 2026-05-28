---
name: spreadsheet-toolkit
description: Use this skill when creating, editing, or analyzing spreadsheets (.xlsx, .xlsm, .csv, etc.) to ensure proper formatting, formula integrity, and data visualization.
---

# Skill body

## Requirements for Outputs

### All Excel Files

#### Zero Formula Errors
- Every Excel model MUST be delivered with ZERO formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?).

#### Preserve Existing Templates (when updating templates)
- Study and EXACTLY match existing format, style, and conventions when modifying files.
- Never impose standardized formatting on files with established patterns.
- Existing template conventions ALWAYS override these guidelines.

### Financial Models

#### Color Coding Standards
Unless otherwise stated by the user or existing template:
- **Blue text (RGB: 0,0,255)**: Hardcoded inputs and numbers users will change for scenarios.
- **Black text (RGB: 0,0,0)**: ALL formulas and calculations.
- **Green text (RGB: 0,128,0)**: Links pulling from other worksheets within the same workbook.
- **Red text (RGB: 255,0,0)**: External links to other files.
- **Yellow background (RGB: 255,255,0)**: Key assumptions needing attention or cells that need to be updated.

#### Number Formatting Standards
- **Years**: Format as text strings (e.g., "2024" not "2,024").
- **Currency**: Use $#,##0 format; ALWAYS specify units in headers (e.g., "Revenue ($mm)").
- **Zeros**: Use number formatting to make all zeros "-", including percentages (e.g., "$#,##0;($#,##0);-").
- **Percentages**: Default to 0.0% format (one decimal).
- **Multiples**: Format as 0.0x for valuation multiples (EV/EBITDA, P/E).
- **Negative numbers**: Use parentheses (123) not minus -123.

### Formula Construction Rules

#### Assumptions Placement
- Place ALL assumptions (growth rates, margins, multiples, etc.) in separate assumption cells.
- Use cell references instead of hardcoded values in formulas (e.g., use `=B5*(1+$B$6)` instead of `=B5*1.05`).

#### Formula Error Prevention
- Verify all cell references are correct.
- Check for off-by-one errors in ranges.
- Ensure consistent formulas across all projection periods.
- Test with edge cases (zero values, negative numbers).
- Verify no unintended circular references.

#### Documentation Requirements for Hardcodes
- Comment or in cells beside (if end of table). Format: "Source: [System/Document], [Date], [Specific Reference], [URL if applicable]".

## Best Practices for Spreadsheet Processing

### Reading and Analyzing Data
```python
import pandas as pd

# Read Excel
df = pd.read_excel('file.xlsx')  # Default: first sheet
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # All sheets as dict

# Analyze
df.head()      # Preview data
df.info()      # Column info
df.describe()  # Statistics

# Write Excel
df.to_excel('output.xlsx', index=False)
```

### Creating Excel Files with openpyxl
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

# Add data
sheet['A1'] = 'Hello'
sheet['B1'] = 'World'
sheet.append(['Row', 'of', 'data'])

# Add formula - ALWAYS use formulas, not hardcoded values
sheet['B2'] = '=SUM(A1:A10)'

# Formatting
sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')

# Column width
sheet.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

### Editing Existing Files
```python
from openpyxl import load_workbook

wb = load_workbook('existing.xlsx')
sheet = wb.active

# Modify cells
sheet['A1'] = 'New Value'
sheet.insert_rows(2)
sheet.delete_cols(3)

# Add new sheet
new_sheet = wb.create_sheet('NewSheet')
new_sheet['A1'] = 'Data'

wb.save('modified.xlsx')
```

### Critical: Use Formulas, Not Hardcoded Values
```python
# BAD - Hardcoding calculated values
total = df['Sales'].sum()
sheet['B10'] = total  # Hardcodes 5000

# GOOD - Using Excel formulas
sheet['B10'] = '=SUM(B2:B9)'
sheet['C5'] = '=(C4-C2)/C2'  # Growth rate
sheet['D20'] = '=AVERAGE(D2:D19)'
```