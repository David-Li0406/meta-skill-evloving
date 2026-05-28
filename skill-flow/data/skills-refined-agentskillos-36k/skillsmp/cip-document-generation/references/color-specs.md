# Color Specifications

## Risk Level Colors

| Risk Level | Symbol | Hex | RGB | Usage |
|------------|--------|-----|-----|-------|
| CRITICAL | 🔴 | #C00000 | 192, 0, 0 | Highest risk, immediate attention |
| HIGH | 🟠 | #ED7D31 | 237, 125, 49 | Significant risk, priority attention |
| MODERATE | 🔵 | #2E75B6 | 46, 117, 182 | Notable risk, should address |
| LOW | 🟢 | #00B050 | 0, 176, 80 | Minor risk, acceptable |

---

## Redline Colors

| Change Type | Hex | RGB | Format |
|-------------|-----|-----|--------|
| Deletion | #FF0000 | 255, 0, 0 | Strikethrough |
| Addition | #00B050 | 0, 176, 80 | Bold |

---

## Document Styling

### Header

| Element | Hex | RGB |
|---------|-----|-----|
| Background | #1F4E79 | 31, 78, 121 |
| Text | #FFFFFF | 255, 255, 255 |

### Accent Colors

| Purpose | Hex | RGB |
|---------|-----|-----|
| Section headers | #2E75B6 | 46, 117, 182 |
| Table borders | #D0CECE | 208, 206, 206 |
| Alternate rows | #F2F2F2 | 242, 242, 242 |

---

## Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Title | Arial | 24pt | Bold |
| Subtitle | Arial | 16pt | Bold |
| Section Header | Arial | 14pt | Bold |
| Body | Arial | 11pt | Regular |
| Table Header | Arial | 10pt | Bold |
| Table Body | Arial | 10pt | Regular |

---

## docx-js Color Implementation

```javascript
// Risk level colors
const COLORS = {
    CRITICAL: 'C00000',
    HIGH: 'ED7D31',
    MODERATE: '2E75B6',
    LOW: '00B050',
    HEADER_BG: '1F4E79',
    HEADER_TEXT: 'FFFFFF',
    DELETION: 'FF0000',
    ADDITION: '00B050'
};

// Example: Risk indicator
new TextRun({
    text: '●',
    color: COLORS.CRITICAL,
    size: 24
});

// Example: Deletion
new TextRun({
    text: 'deleted text',
    strike: true,
    color: COLORS.DELETION
});

// Example: Addition
new TextRun({
    text: 'added text',
    bold: true,
    color: COLORS.ADDITION
});

// Example: Header cell
new TableCell({
    shading: {
        fill: COLORS.HEADER_BG,
        type: ShadingType.SOLID
    },
    children: [
        new Paragraph({
            children: [
                new TextRun({
                    text: 'Header Text',
                    color: COLORS.HEADER_TEXT,
                    bold: true
                })
            ]
        })
    ]
});
```

---

## python-docx Color Implementation

```python
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# Risk level colors
COLORS = {
    'CRITICAL': RGBColor(192, 0, 0),
    'HIGH': RGBColor(237, 125, 49),
    'MODERATE': RGBColor(46, 117, 182),
    'LOW': RGBColor(0, 176, 80),
    'HEADER_BG': RGBColor(31, 78, 121),
    'DELETION': RGBColor(255, 0, 0),
    'ADDITION': RGBColor(0, 176, 80)
}

# Example: Colored text
run = paragraph.add_run('●')
run.font.color.rgb = COLORS['CRITICAL']

# Example: Strikethrough deletion
run = paragraph.add_run('deleted text')
run.font.strike = True
run.font.color.rgb = COLORS['DELETION']

# Example: Bold addition
run = paragraph.add_run('added text')
run.bold = True
run.font.color.rgb = COLORS['ADDITION']

# Example: Cell shading
def set_cell_shading(cell, color_hex):
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), color_hex)
    cell._tc.get_or_add_tcPr().append(shading)

set_cell_shading(cell, '1F4E79')  # Navy header
```

---

## Unicode Symbols

| Symbol | Unicode | Description |
|--------|---------|-------------|
| 🔴 | U+1F534 | Red circle (CRITICAL) |
| 🟠 | U+1F7E0 | Orange circle (HIGH) |
| 🔵 | U+1F535 | Blue circle (MODERATE) |
| 🟢 | U+1F7E2 | Green circle (LOW) |
| ▲ | U+25B2 | Up triangle (increased) |
| ▼ | U+25BC | Down triangle (decreased) |
| ● | U+25CF | Filled circle (unchanged) |

**Note:** For .docx, use colored filled circles (●) with appropriate color rather than emoji, as emoji rendering varies by system.

```javascript
// Preferred: Colored bullet
new TextRun({
    text: '●',
    color: 'C00000',  // CRITICAL red
    size: 20
});

// Avoid: Emoji (inconsistent rendering)
new TextRun({
    text: '🔴'
});
```
