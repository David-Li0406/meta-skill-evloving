---
name: comprehensive-xlsx
description: Use this skill for comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization when working with spreadsheets (.xlsx, .xlsm, .csv, .tsv, etc).
---

# Requirements for Outputs

## All Excel files

### Zero Formula Errors
- Every Excel model MUST be delivered with ZERO formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?).

### Preserve Existing Templates (when updating templates)
- Study and EXACTLY match existing format, style, and conventions when modifying files.
- Never impose standardized formatting on files with established patterns.
- Existing template conventions ALWAYS override these guidelines.

## Financial Models

### Color Coding Standards
Unless otherwise stated by the user or existing template:
- **Blue text (RGB: 0,0,255)**: Hardcoded inputs, and numbers users will change for scenarios.
- **Black text (RGB: 0,0,0)**: ALL formulas and calculations.
- **Green text (RGB: 0,128,0)**: Links pulling from other worksheets within the same workbook.
- **Red text (RGB: 255,0,0)**: External links to other files.
- **Yellow background (RGB: 255,255,0)**: Key assumptions needing attention or cells that need to be updated.

### Number Formatting Standards
- **Years**: Format as text strings (e.g., "2024" not "2,024").
- **Currency**: Use $#,##0 format; ALWAYS specify units in headers (e.g., "Revenue ($mm)").
- **Zeros**: Use number formatting to make all zeros "-", including percentages (e.g., "$#,##0;($#,##0);-").
- **Percentages**: Default to 0.0% format (one decimal).
- **Multiples**: Format as 0.0x for valuation multiples (EV/EBITDA, P/E).
- **Negative numbers**: Use parentheses (123) not minus -123.

### Formula Construction Rules
- Place ALL assumptions (growth rates, margins, multiples, etc.) in separate assumption cells.
- Use cell references instead of hardcoded values in formulas (e.g., use `=B5*(1+$B$6)` instead of `=B5*1.05`).
- Verify all cell references are correct and check for off-by-one errors in ranges.
- Ensure consistent formulas across all projection periods and test with edge cases (zero values, negative numbers).
- Document hardcoded values with comments in cells beside them.

## Overview of XLSX Creation, Editing, and Analysis

### Reading and Analyzing Data
For data analysis, visualization, and basic operations, use **pandas** which provides powerful data manipulation capabilities:

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

### Recalculating Formulas
Excel files created or modified by openpyxl contain formulas as strings but not calculated values. Use the provided `recalc.py` script to recalculate formulas:

```bash
python recalc.py <excel_file> [timeout_seconds]
```

Example:
```bash
python recalc.py output.xlsx 30
```

The script:
- Automatically sets up LibreOffice macro on first run.
- Recalculates all formulas in all sheets.
- Scans ALL cells for Excel errors (#REF!, #DIV/0!, etc.).
- Returns JSON with detailed error locations and counts.

## Best Practices
- Always use Excel formulas instead of calculating values in Python and hardcoding them.
- Use `data_only=True` to read calculated values.
- For large files: Use `read_only=True` or `write_only=True`.
- Formulas are preserved but not evaluated by openpyxl.

## Formula Verification Checklist
- Test 2-3 sample references to verify they pull correct values before building the full model.
- Confirm Excel columns match (e.g., column 64 = BL, not BK).
- Remember Excel rows are 1-indexed (DataFrame row 5 = Excel row 6).
- Check for null values with `pd.notna()`.
- Verify all cell references point to intended cells (#REF!).
- Use correct format (Sheet1!A1) for linking sheets.