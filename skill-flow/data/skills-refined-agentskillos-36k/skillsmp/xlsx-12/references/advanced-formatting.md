# Advanced Excel Formatting

Detailed formatting options for professional Excel spreadsheets.

## Cell Styles

### Font Styling

```python
from openpyxl.styles import Font

# Basic font
ws['A1'].font = Font(
    name='Calibri',
    size=14,
    bold=True,
    italic=False,
    color='FF0000'  # Red (hex without #)
)

# Financial model color coding
ws['B2'].font = Font(color='0000FF')  # Blue for inputs
ws['C2'].font = Font(color='000000')  # Black for formulas
ws['D2'].font = Font(color='00FF00')  # Green for worksheet links
ws['E2'].font = Font(color='FF0000')  # Red for external links
```

### Alignment

```python
from openpyxl.styles import Alignment

ws['A1'].alignment = Alignment(
    horizontal='center',   # left, center, right
    vertical='center',     # top, center, bottom
    wrap_text=True
)
```

### Borders

```python
from openpyxl.styles import Border, Side

thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)

ws['A1'].border = thin_border
```

### Fill (Background Color)

```python
from openpyxl.styles import PatternFill

# Solid fill
ws['A1'].fill = PatternFill(
    start_color='FFFF00',  # Yellow
    fill_type='solid'
)

# Financial model: yellow background for key assumptions
ws['B2'].fill = PatternFill(start_color='FFFF00', fill_type='solid')
```

## Number Formatting

### Currency

```python
# With currency symbol
ws['B2'].number_format = '$#,##0.00'

# Without symbol (use units in header)
ws['B1'] = 'Revenue ($mm)'
ws['B2'].number_format = '#,##0.0'
```

### Percentages

```python
ws['C2'].number_format = '0.0%'  # 15.5%
ws['C3'].number_format = '0.00%'  # 15.50%
```

### Multiples

```python
ws['D2'].number_format = '0.0x'  # 3.5x
```

### Negative Numbers in Parentheses

```python
ws['E2'].number_format = '#,##0;(#,##0)'  # -100 displays as (100)
ws['E3'].number_format = '#,##0.00;(#,##0.00)'  # With decimals
```

### Zeros as Dashes

```python
ws['F2'].number_format = '#,##0.0;-#,##0.0;"-"'  # 0 displays as -
```

### Dates

```python
ws['G2'].number_format = 'yyyy-mm-dd'
ws['G3'].number_format = 'mm/dd/yyyy'
ws['G4'].number_format = 'mmmm d, yyyy'  # January 1, 2024
```

## Column & Row Sizing

```python
from openpyxl.utils import get_column_letter

# Set column width
ws.column_dimensions['A'].width = 20
ws.column_dimensions[get_column_letter(2)].width = 15

# Set row height
ws.row_dimensions[1].height = 30

# Auto-size (approximate)
for column in ws.columns:
    max_length = 0
    column_letter = column[0].column_letter
    for cell in column:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(cell.value)
        except:
            pass
    adjusted_width = (max_length + 2)
    ws.column_dimensions[column_letter].width = adjusted_width
```

## Named Ranges

```python
from openpyxl.workbook.defined_name import DefinedName

# Create named range
wb.defined_names.add(DefinedName('GrowthRate', attr_text='Sheet1!$B$2'))

# Use in formula
ws['B5'] = '=B4*(1+GrowthRate)'

# Multi-cell range
wb.defined_names.add(DefinedName('DataRange', attr_text='Sheet1!$A$2:$C$10'))
```

## Conditional Formatting

```python
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule
from openpyxl.styles import PatternFill

# Highlight cells > 100 in green
green_fill = PatternFill(start_color='00FF00', fill_type='solid')
ws.conditional_formatting.add(
    'B2:B10',
    CellIsRule(operator='greaterThan', formula=['100'], fill=green_fill)
)

# Color scale (red to green)
ws.conditional_formatting.add(
    'C2:C10',
    ColorScaleRule(
        start_type='min', start_color='FF0000',
        end_type='max', end_color='00FF00'
    )
)
```

## Data Validation

```python
from openpyxl.worksheet.datavalidation import DataValidation

# Dropdown list
dv = DataValidation(type='list', formula1='"Yes,No,Maybe"')
ws.add_data_validation(dv)
dv.add('B2:B10')

# Number range
dv2 = DataValidation(type='whole', operator='between', formula1='1', formula2='100')
dv2.error = 'Value must be between 1 and 100'
dv2.errorTitle = 'Invalid Entry'
ws.add_data_validation(dv2)
dv2.add('C2:C10')

# Date range
dv3 = DataValidation(type='date', operator='greaterThan', formula1='2024-01-01')
ws.add_data_validation(dv3)
dv3.add('D2:D10')
```

## Freeze Panes

```python
# Freeze top row
ws.freeze_panes = 'A2'

# Freeze first column
ws.freeze_panes = 'B1'

# Freeze top row and first column
ws.freeze_panes = 'B2'
```

## Merge Cells

```python
# Merge cells
ws.merge_cells('A1:D1')

# Set value in merged cell
ws['A1'] = 'Title Spanning Multiple Columns'
ws['A1'].alignment = Alignment(horizontal='center')

# Unmerge cells
ws.unmerge_cells('A1:D1')
```

## Print Settings

```python
from openpyxl.worksheet.page import PageMargins, PrintPageSetup

# Set page margins
ws.page_margins = PageMargins(left=0.5, right=0.5, top=0.75, bottom=0.75)

# Page setup
ws.print_options.horizontalCentered = True
ws.print_options.verticalCentered = True

# Fit to one page
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 1

# Orientation
ws.page_setup.orientation = 'landscape'  # or 'portrait'
```

## Protection

```python
from openpyxl.styles import Protection

# Protect sheet
ws.protection.sheet = True
ws.protection.password = 'password123'

# Lock specific cells
ws['A1'].protection = Protection(locked=True)

# Unlock cells (user can edit)
ws['B2'].protection = Protection(locked=False)
```
