---
name: skills-ppt-sop
description: "Generate professional HTML presentations with strict design standards. Use when creating: (1) Complete multi-slide presentations with navigation, (2) Individual slide pages (cover, TOC, content, summary, end), (3) Data visualizations (tables, charts). Output is single-file HTML with zero external dependencies."
---

# HTML Presentation Generator

Generate professional HTML presentations following Within7 company standards with strict design constraints.

## Decision Tree

Choose output format based on requirements:

| Requirement | Output Format | When to Use |
|-------------|---------------|-------------|
| Complete presentation with navigation | Single HTML file | Default choice, most presentations |
| Individual standalone slides | Multiple HTML files | User explicitly requests separate files |
| Quick prototype | Single HTML file | When testing layout/design |

## Workflow

### Step 1: Analyze Requirements

Identify slide types needed:
- **Cover page**: Title, subtitle, optional background
- **TOC page**: Table of contents with numbered sections
- **Content pages**: Data tables, charts, text content
- **Summary page**: Key metrics and takeaways
- **End page**: Thank you/contact information

### Step 2: Load Templates

**MANDATORY - READ ENTIRE FILE**: Before proceeding, you MUST read [`templates-guide.md`](references/templates-guide.md) completely.

For each slide type, load corresponding template:
- Cover: `templates/cover.html`
- TOC: `templates/toc.html`
- Content: `templates/base-template.html`
- Summary: `templates/summary.html`
- End: `templates/end.html`

### Step 3: Integrate Components

**MANDATORY - READ ENTIRE FILE**: For data visualization, read [`components-guide.md`](references/components-guide.md) completely.

Copy component HTML from `components/` directory:
- Tables: `data-table.html`
- Bar charts: `bar-chart.html`
- Radar charts: `radar-chart.html`
- Icons: `icons.html`

### Step 4: Assemble Presentation

For single-file output:
1. Start with `navigation-template.html` as base
2. Replace slide sections with content from templates
3. Update slide count and navigation logic
4. Verify all CSS variables are defined

For multi-file output:
1. Create separate HTML file for each slide
2. Use individual templates directly
3. Name files: `slide-01.html`, `slide-02.html`, etc.

## Design System Constraints

### Core Rules
- Canvas size: 960×540px (16:9 at 72dpi)
- Safe margins: 40px on all sides
- Responsive: ONLY use `transform:scale(...)`, NO reflow
- Single file HTML, zero external dependencies

### CSS Variables
```css
--bg-main: #FFFFFF
--bg-header: #000000
--accent: #F85d42
--gray: #74788d
--aux1: #556EE6
--aux2: #34c38f
--aux3: #50a5f1
--aux4: #f1b44c
--gray-light: #F5F5F5
--page-bg: #e0e0e0
```

### Layout System
- 12-column grid (60px columns, 20px gaps)
- Card: 8px border-radius, 20px padding
- Header: 60px height, black background

## NEVER Do These

### Common Mistakes

**Breaking Layout**
- Never change canvas size (960×540px is mandatory)
- Never use responsive reflow (use `transform:scale` only)
- Never remove safe margins (40px minimum)

**Design Violations**
- Never use external CSS/JS files
- Never use system fonts other than specified
- Never modify CSS variable values
- Never add custom animations

**Content Errors**
- Never exceed 5-6 bullet points per slide
- Never use font sizes smaller than 16px
- Never place text within 20px of edges
- Never use more than 3 accent colors per slide

### Anti-Patterns

**Generic AI-Generated Designs**
- Purple gradients on white backgrounds
- All corners rounded to 8px
- Cookie-cutter card layouts
- Generic, personality-free styles

**Poor Data Visualization**
- Charts without axis labels
- Tables without total rows
- Numbers left-aligned (always right-align)
- Inconsistent decimal formatting

## Quick Reference

### File Structure
```
skills-ppt-sop/
├── SKILL.md
├── references/
│   ├── templates-guide.md
│   └── components-guide.md
├── templates/
│   ├── navigation-template.html
│   ├── cover.html
│   ├── toc.html
│   ├── base-template.html
│   ├── summary.html
│   └── end.html
└── components/
    ├── data-table.html
    ├── bar-chart.html
    ├── radar-chart.html
    └── icons.html
```

### Template Selection Guide

| Slide Type | Template | Key Features |
|------------|----------|--------------|
| Cover | `cover.html` | Gradient background, centered title |
| TOC | `toc.html` | Numbered list, 60px row height |
| Content | `base-template.html` | 12-column grid, card system |
| Summary | `summary.html` | 3-column metric cards |
| End | `end.html` | Centered thank you message |

### Component Usage

| Component | File | Best For |
|-----------|------|----------|
| Data Table | `data-table.html` | Financial data, metrics |
| Bar Chart | `bar-chart.html` | Q1-Q4 comparisons |
| Radar Chart | `radar-chart.html` | Multi-dimensional metrics |
| Icons | `icons.html` | Visual indicators |

## Output Verification

Before delivering, verify:
- [ ] All CSS variables are defined
- [ ] Canvas size is 960×540px
- [ ] No external dependencies
- [ ] Navigation works (for single-file output)
- [ ] All numbers are right-aligned in tables
- [ ] Font sizes meet minimum requirements
- [ ] Safe margins maintained
