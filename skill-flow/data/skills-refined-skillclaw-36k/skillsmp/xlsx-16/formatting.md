# XLSX Formatting Guide

## Color Codes (RGB)

| Purpose | Color | RGB Code | Hex |
|---------|-------|----------|-----|
| Hardcoded inputs | Blue | 0, 0, 255 | 0000FF |
| Formulas/calculations | Black | 0, 0, 0 | 000000 |
| Internal links (same workbook) | Green | 0, 128, 0 | 008000 |
| External links (other files) | Red | 255, 0, 0 | FF0000 |
| Key assumptions (background) | Yellow | 255, 255, 0 | FFFF00 |

## Number Formats

| Type | Format Code | Example | Notes |
|------|-------------|---------|-------|
| Currency | $#,##0 | $1,234 | No decimals |
| Currency (with cents) | $#,##0.00 | $1,234.56 | Two decimals |
| Currency (negative) | $#,##0;($#,##0) | ($1,234) | Parentheses for negative |
| Percentage | 0.0% | 12.5% | One decimal |
| Multiple | 0.0x | 2.5x | Valuation multiples |
| Date | YYYY-MM-DD | 2024-12-29 | ISO format |
| Text Year | @ | 2024 | Prevents comma formatting |
| Thousands | #,##0 | 1,234 | With comma separator |
| Millions | #,##0,, | 1 | Value in millions |
| Accounting | _($* #,##0_) | $ 1,234 | Aligned with space |

## openpyxl Formatting Code

### Font Styling

```python
from openpyxl.styles import Font

# Basic font
cell.font = Font(
    name='Calibri',        # Font family
    size=11,               # Point size
    bold=True,             # Bold text
    italic=False,          # Italic text
    underline='single',    # none, single, double
    strike=False,          # Strikethrough
    color='0000FF'         # RGB hex color (blue)
)

# Common presets
blue_input = Font(color='0000FF')       # Hardcoded input
green_link = Font(color='008000')       # Internal link
red_external = Font(color='FF0000')     # External link
header_bold = Font(bold=True, size=12)  # Header
```

### Fill (Background)

```python
from openpyxl.styles import PatternFill

# Solid fill
cell.fill = PatternFill(
    start_color='FFFF00',  # Yellow
    end_color='FFFF00',
    fill_type='solid'
)

# Common presets
yellow_highlight = PatternFill(start_color='FFFF00', fill_type='solid')
light_gray = PatternFill(start_color='D3D3D3', fill_type='solid')
light_blue = PatternFill(start_color='DAEEF3', fill_type='solid')
error_red = PatternFill(start_color='FFCCCC', fill_type='solid')
```

### Alignment

```python
from openpyxl.styles import Alignment

cell.alignment = Alignment(
    horizontal='center',    # left, center, right, justify
    vertical='center',      # top, center, bottom
    wrap_text=True,         # Wrap text in cell
    shrink_to_fit=False,    # Shrink text to fit
    indent=0,               # Left indent
    text_rotation=0         # Degrees (0-180)
)

# Common presets
center_align = Alignment(horizontal='center', vertical='center')
right_align = Alignment(horizontal='right')
wrap_text = Alignment(wrap_text=True)
```

### Borders

```python
from openpyxl.styles import Border, Side

# Side styles: thin, medium, thick, double, hair, dotted, dashed
thin = Side(style='thin', color='000000')
thick = Side(style='thick', color='000000')

# Full border
cell.border = Border(
    left=thin,
    right=thin,
    top=thin,
    bottom=thin
)

# Bottom border only (for headers)
header_border = Border(bottom=Side(style='medium', color='000000'))

# Box border
box_border = Border(
    left=thick,
    right=thick,
    top=thick,
    bottom=thick
)
```

## Column Width & Row Height

```python
# Set column width (character units)
ws.column_dimensions['A'].width = 20

# Set row height (points)
ws.row_dimensions[1].height = 30

# Auto-fit columns (approximate)
from openpyxl.utils import get_column_letter

for column_cells in ws.columns:
    max_length = 0
    column = column_cells[0].column_letter
    for cell in column_cells:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
        except:
            pass
    adjusted_width = (max_length + 2) * 1.2
    ws.column_dimensions[column].width = adjusted_width

# Hide column
ws.column_dimensions['C'].hidden = True

# Hide row
ws.row_dimensions[5].hidden = True
```

## Freeze Panes

```python
# Freeze top row
ws.freeze_panes = 'A2'

# Freeze first column
ws.freeze_panes = 'B1'

# Freeze top row and first column
ws.freeze_panes = 'B2'

# Unfreeze
ws.freeze_panes = None
```

## Conditional Formatting

```python
from openpyxl.formatting.rule import ColorScaleRule, FormulaRule
from openpyxl.styles import PatternFill

# Color scale (heat map)
rule = ColorScaleRule(
    start_type='min', start_color='FF0000',  # Red
    mid_type='percentile', mid_value=50, mid_color='FFFF00',  # Yellow
    end_type='max', end_color='00FF00'  # Green
)
ws.conditional_formatting.add('B2:B100', rule)

# Highlight cells > 100
red_fill = PatternFill(start_color='FFCCCC', fill_type='solid')
rule = FormulaRule(
    formula=['B2>100'],
    fill=red_fill
)
ws.conditional_formatting.add('B2:B100', rule)
```

## Print Settings

```python
# Page orientation
ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE

# Paper size (Letter = 1, A4 = 9)
ws.page_setup.paperSize = ws.PAPERSIZE_LETTER

# Fit to page
ws.page_setup.fitToPage = True
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 0  # 0 = as many pages as needed

# Print area
ws.print_area = 'A1:D50'

# Print titles (repeat rows/columns)
ws.print_title_rows = '1:1'  # Repeat row 1
ws.print_title_cols = 'A:A'  # Repeat column A

# Margins (inches)
ws.page_margins.left = 0.5
ws.page_margins.right = 0.5
ws.page_margins.top = 0.75
ws.page_margins.bottom = 0.75
```
