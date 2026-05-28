---
name: xlsx
description: Create, edit, and analyze Excel spreadsheets with formulas, formatting, data analysis, and visualization. Use when working with .xlsx files for professional documents, financial models, data analysis, or reporting.
allowed-tools: Bash,Read,Write,Edit,Glob,Grep
---

# Excel Spreadsheet (XLSX) Expert

Create, edit, and analyze Excel spreadsheets with professional formatting, formulas, and data analysis capabilities.

## Critical Requirements

### Zero Formula Errors

**Every Excel file must be delivered without formula errors:**
- No #REF! (invalid reference)
- No #DIV/0! (division by zero)
- No #VALUE! (wrong value type)
- No #N/A (value not available)
- No #NAME? (unrecognized name)

**Always verify:**
1. Create/edit the file
2. Run `python scripts/recalc.py <file.xlsx>`
3. Fix any errors reported
4. Re-verify until clean

### Preserve Existing Templates

When modifying existing Excel files:
- Maintain established formatting conventions
- Keep existing color schemes
- Preserve formula patterns
- Don't impose standardized patterns over established ones

## Financial Model Standards

When creating financial models, follow industry conventions:

### Color Coding

| Color | Meaning | Usage |
|-------|---------|-------|
| Blue text | Hardcoded inputs | User-changeable numbers and assumptions |
| Black text | Formulas | All calculated values and references |
| Green text | Worksheet links | References to other sheets in same file |
| Red text | External links | References to other files |
| Yellow background | Key assumptions | Important inputs requiring attention |

### Number Formatting Quick Reference

| Type | Format | Example |
|------|--------|---------|
| Currency (header units) | `#,##0.0` | Revenue ($mm): 1,234.5 |
| Zeros as dashes | `#,##0.0;-#,##0.0;"-"` | 0 displays as - |
| Percentages | `0.0%` | 15.5% |
| Multiples | `0.0x` | 3.5x |
| Negatives in parens | `#,##0;(#,##0)` | (100) |

See `references/advanced-formatting.md` for complete formatting options.

## Critical: Use Formulas, Not Hardcoded Values

Python should create **formulas** in Excel, not calculate values and hardcode them.

```python
# ❌ WRONG: Hardcoded value
sheet['B10'] = 5000  # Calculated sum hardcoded

# ✅ CORRECT: Formula
sheet['B10'] = '=SUM(B2:B9)'  # Excel will calculate
```

**Why this matters:**
- Users can update inputs and see results recalculate
- Formulas are traceable and auditable
- Hardcoded values break when inputs change

## Tool Selection

### pandas - Best for:
- Data analysis and manipulation
- Bulk operations on tabular data
- Simple exports without complex formatting
- Reading CSV/Excel into DataFrames

### openpyxl - Best for:
- Creating formulas
- Complex formatting (colors, borders, fonts)
- Excel-specific features (charts, named ranges)
- Fine-grained control over cells

## Essential Workflow

### 1. Choose Tool

Decide between pandas (data analysis) or openpyxl (formulas/formatting)

### 2. Create or Load File

```python
# openpyxl - New file
from openpyxl import Workbook
wb = Workbook()
ws = wb.active

# openpyxl - Load existing
from openpyxl import load_workbook
wb = load_workbook('existing.xlsx')
ws = wb['Sheet1']

# pandas - New file
import pandas as pd
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# pandas - Load existing
df = pd.read_excel('existing.xlsx')
```

### 3. Modify Data/Formulas/Formatting

**Add formulas (openpyxl):**
```python
ws['C1'] = '=A1+B1'
ws['C2'] = '=SUM(A:A)'

# Safe division with IF
ws['D1'] = '=IF(B1=0,"-",A1/B1)'
```

**Format cells (openpyxl):**
```python
from openpyxl.styles import Font, PatternFill

ws['A1'].font = Font(bold=True, size=14, color='0000FF')  # Blue
ws['A1'].fill = PatternFill(start_color='FFFF00', fill_type='solid')  # Yellow
ws['A1'].number_format = '#,##0.0'
```

**Manipulate data (pandas):**
```python
df['Total'] = df['A'] + df['B']
summary = df.groupby('Category')['Revenue'].sum()
```

### 4. Save File

```python
# openpyxl
wb.save('output.xlsx')

# pandas
df.to_excel('output.xlsx', index=False)
```

### 5. Recalculate & Verify

```bash
python scripts/recalc.py output.xlsx
```

**Output shows errors:**
```json
{
  "file": "output.xlsx",
  "sheets": {
    "Sheet1": {
      "error_count": 2,
      "errors": [
        {"cell": "B5", "error": "#DIV/0!", "description": "Division by zero"},
        {"cell": "C3", "error": "#REF!", "description": "Invalid cell reference"}
      ]
    }
  },
  "total_errors": 2
}
```

### 6. Fix Errors & Re-verify

Fix reported errors and run `recalc.py` again until clean.

## Common Error Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| #REF! | Reference to deleted cell/range | Update formula references |
| #DIV/0! | Division by zero | Add `=IF(B1=0,"-",A1/B1)` |
| #VALUE! | Wrong value type in formula | Check data types match formula |
| #NAME? | Unrecognized function/name | Fix spelling or define named range |
| #N/A | Value not available (VLOOKUP) | Use IFERROR or verify lookup exists |

## Quick Start Examples

### Simple Data Report (pandas)

```python
import pandas as pd

df = pd.read_csv('data.csv')
summary = df.groupby('Region')['Sales'].sum()

with pd.ExcelWriter('report.xlsx', engine='openpyxl') as writer:
    summary.to_excel(writer, sheet_name='Summary')
    df.to_excel(writer, sheet_name='Raw Data', index=False)
```

Verify: `python scripts/recalc.py report.xlsx`

### Financial Model (openpyxl)

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

wb = Workbook()
ws = wb.active

# Assumptions (blue text, yellow fill)
ws['A1'] = 'Base Revenue'
ws['B1'] = 100
ws['B1'].font = Font(color='0000FF')
ws['B1'].fill = PatternFill(start_color='FFFF00', fill_type='solid')

ws['A2'] = 'Growth Rate'
ws['B2'] = 0.15
ws['B2'].font = Font(color='0000FF')
ws['B2'].fill = PatternFill(start_color='FFFF00', fill_type='solid')

# Projections (formulas in black)
ws['A4'] = 'Year 1'
ws['B4'] = '=B1'
ws['B4'].font = Font(color='000000')

ws['A5'] = 'Year 2'
ws['B5'] = '=B4*(1+$B$2)'  # Absolute reference to growth rate
ws['B5'].font = Font(color='000000')

wb.save('model.xlsx')
```

Verify: `python scripts/recalc.py model.xlsx`

**For more examples, see:** `references/workflow-examples.md`

## Best Practices

### Formula Construction

**✅ Do:**
- Place assumptions in separate cells
- Use cell references instead of hardcoded values
- Use absolute references ($A$1) for constants
- Test formulas with edge cases (zeros, negatives)

**❌ Don't:**
- Hardcode numbers in formulas
- Create circular references
- Hide complex logic in single formulas

### Financial Models

```python
# ✅ Good: Traceable with cell references
ws['B5'] = '=B4*(1+$B$2)'  # $B$2 is growth rate assumption

# ❌ Bad: Hardcoded growth rate
ws['B5'] = '=B4*1.15'  # Where did 1.15 come from?
```

### Safe Division

```python
# Always protect against division by zero
ws['C1'] = '=IF(B1=0,"-",A1/B1)'
```

## Advanced Features

For detailed documentation, see references:

- **Advanced formatting** (fonts, colors, borders, etc.) → `references/advanced-formatting.md`
- **Complete workflow examples** → `references/workflow-examples.md`

## Quick Reference

### Common openpyxl Patterns

```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment

# Create workbook
wb = Workbook()
ws = wb.active

# Basic formatting
ws['A1'].font = Font(bold=True, size=14)
ws['A1'].fill = PatternFill(start_color='FFFF00', fill_type='solid')
ws['A1'].alignment = Alignment(horizontal='center')

# Number formatting
ws['B2'].number_format = '#,##0.0'  # Thousands with 1 decimal
ws['C2'].number_format = '0.0%'  # Percentage

# Formulas
ws['D2'] = '=SUM(A2:C2)'
ws['E2'] = '=IF(D2>100,"High","Low")'

# Save
wb.save('output.xlsx')
```

### Common pandas Patterns

```python
import pandas as pd

# Read Excel
df = pd.read_excel('input.xlsx', sheet_name='Data')

# Analysis
summary = df.groupby('Category').agg({
    'Revenue': 'sum',
    'Quantity': 'mean'
})

# Write Excel
with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Data', index=False)
    summary.to_excel(writer, sheet_name='Summary')
```

## Verification Checklist

Before delivering Excel file:
- [ ] All formulas use cell references, not hardcoded values
- [ ] Color coding follows financial model standards (if applicable)
- [ ] Number formatting is appropriate and consistent
- [ ] `python scripts/recalc.py <file.xlsx>` returns 0 errors
- [ ] All errors (#REF!, #DIV/0!, etc.) are fixed
- [ ] Complex formulas are documented (if needed)
- [ ] File opens correctly in Excel

## Important Reminders

- **ALWAYS** use formulas, not hardcoded calculated values
- **ALWAYS** run `scripts/recalc.py` to verify zero formula errors
- **ALWAYS** fix all Excel errors before delivering files
- **ALWAYS** preserve existing formatting when editing files
- **NEVER** hardcode calculations (use formulas with cell references)
- **NEVER** deliver files with #REF!, #DIV/0!, #VALUE!, #NAME?, or #N/A errors
- **NEVER** ignore recalc.py error output
- **CHECK** financial model color coding standards when applicable
- **USE** openpyxl for formulas/formatting, pandas for data analysis
- **TEST** formulas with edge cases (zeros, negatives, large numbers)
