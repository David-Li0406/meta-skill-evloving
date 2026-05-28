---
name: xlsx
description: "Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization"
category: data
version: "1.0.0"
license: Based on Anthropic's xlsx skill (https://github.com/anthropics/skills)

# Tool configurations - this skill has no gated tools (uses general code execution)
tool_configs: []

# Resource configurations - Level 3 content
resource_configs:
  - name: examples
    description: "Detailed code examples for common spreadsheet operations"
    file: examples.md

  - name: formatting
    description: "Advanced formatting guide including styles, conditional formatting, and charts"
    file: formatting.md

  - name: recalc
    description: "Recalculation script for verifying formula results"
    file: recalc.md
---

# XLSX Skill

## Core Purpose
Create, edit, and analyze spreadsheets (.xlsx, .xlsm, .csv, .tsv) with comprehensive
support for formulas, formatting, data analysis, and visualization.

## Requirements for All Excel Files

### Zero Formula Errors
Every Excel model MUST be delivered with ZERO formula errors:
- `#REF!` - Invalid cell references
- `#DIV/0!` - Division by zero
- `#VALUE!` - Wrong data type in formula
- `#N/A` - Value not available
- `#NAME?` - Unrecognized formula name

### Preserve Existing Templates
When modifying files with established patterns:
- Study and EXACTLY match existing format, style, and conventions
- Never impose standardized formatting on files with established patterns
- Existing template conventions ALWAYS override these guidelines

## Financial Model Standards

### Color Coding Conventions
- **Blue text (RGB: 0,0,255)**: Hardcoded inputs, numbers users will change
- **Black text (RGB: 0,0,0)**: ALL formulas and calculations
- **Green text (RGB: 0,128,0)**: Links from other worksheets in same workbook
- **Red text (RGB: 255,0,0)**: External links to other files
- **Yellow background (RGB: 255,255,0)**: Key assumptions needing attention

### Number Formatting Rules
- **Years**: Format as text strings ("2024" not "2,024")
- **Currency**: Use $#,##0 format; specify units in headers ("Revenue ($mm)")
- **Zeros**: Format to display as "-"
- **Percentages**: Default to 0.0% format (one decimal)
- **Multiples**: Format as 0.0x for valuation multiples
- **Negative numbers**: Use parentheses (123) not minus -123

## CRITICAL: Use Formulas, Not Hardcoded Values

**Always use Excel formulas instead of calculating values in Python.**
This keeps spreadsheets dynamic and updateable.

### Wrong - Hardcoding:
```python
total = df['Sales'].sum()
sheet['B10'] = total  # Hardcodes value
```

### Correct - Using Formulas:
```python
sheet['B10'] = '=SUM(B2:B9)'  # Excel calculates
```

## Tool Selection

- **pandas**: Best for data analysis, bulk operations, simple data export
- **openpyxl**: Best for complex formatting, formulas, Excel-specific features

## Common Workflow

1. **Choose tool**: pandas for data, openpyxl for formulas/formatting
2. **Create/Load**: Create new workbook or load existing file
3. **Modify**: Add/edit data, formulas, and formatting
4. **Save**: Write to file
5. **Recalculate**: Run `python recalc.py output.xlsx` (MANDATORY for formulas)
6. **Verify**: Check recalc.py output for errors, fix any found

## Quick Code Examples

### Reading with pandas:
```python
import pandas as pd
df = pd.read_excel('file.xlsx')
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)
```

### Creating with openpyxl:
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active
sheet['A1'] = 'Header'
sheet['B2'] = '=SUM(A1:A10)'  # Use formulas!
sheet['A1'].font = Font(bold=True, color='FF0000')
wb.save('output.xlsx')
```

### Editing existing files:
```python
from openpyxl import load_workbook
wb = load_workbook('existing.xlsx')
sheet = wb.active
sheet['A1'] = 'New Value'
wb.save('modified.xlsx')
```

## Formula Verification Checklist

- [ ] Test 2-3 sample references before building full model
- [ ] Verify column mapping (column 64 = BL, not BK)
- [ ] Remember Excel rows are 1-indexed
- [ ] Check for NaN values with `pd.notna()`
- [ ] Handle division by zero in formulas
- [ ] Test formulas on 2-3 cells before applying broadly

## Best Practices

- Cell indices are 1-based in openpyxl
- Use `data_only=True` to read calculated values (WARNING: saves lose formulas)
- For large files: Use `read_only=True` or `write_only=True`
- Write minimal, concise Python code
- Add comments to cells with complex formulas
