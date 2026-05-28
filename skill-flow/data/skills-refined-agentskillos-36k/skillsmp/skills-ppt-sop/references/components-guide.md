# Components Guide

Complete guide for using HTML presentation components.

## Component Overview

All components are designed to:
- Work with 12-column grid system
- Use design system CSS variables
- Be copy-paste ready
- Maintain visual consistency

## 1. Data Table (`data-table.html`)

### Purpose
Display tabular data with totals and proper formatting.

### Key Features
- Full-width table (12 columns)
- Right-aligned numbers
- Total row with double border
- Alternating row colors (optional)
- Header with gray background

### Structure

```html
<div class="col-12">
  <div class="card">
    <h3>表格标题</h3>
    <table>
      <thead>
        <tr>
          <th>项目</th>
          <th class="num">数量</th>
          <th class="num">金额</th>
          <th class="num">占比</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>项目一</td>
          <td class="num">1,234</td>
          <td class="num">¥56.7万</td>
          <td class="num">32.5%</td>
        </tr>
        <tr class="total">
          <td>合计</td>
          <td class="num">7,035</td>
          <td class="num">¥170.1万</td>
          <td class="num">100%</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
```

### Customization Points

**Columns:**
- Add/remove `<th>` and `<td>` elements
- Use `.num` class for numeric columns
- Keep header and body columns aligned

**Data Formatting:**
- Numbers: Use thousands separators (1,234)
- Currency: Add currency symbol (¥, $)
- Percentages: Use % symbol
- Decimals: Consistent precision (1 or 2 decimal places)

**Styling:**
- `h3`: Table title (24px, bold)
- `th`: Header cells (gray background, bottom border)
- `td`: Data cells (bottom border)
- `tr.total`: Total row (double top border, bold)

### When to Use
- Financial data (revenue, expenses)
- Metrics comparisons
- Any tabular data with totals
- Lists with numeric values

### Common Mistakes

**Alignment Errors**
- ❌ Numbers left-aligned
- ✅ Always use `.num` class for numeric columns

**Missing Totals**
- ❌ No total row
- ✅ Always include `tr.total` for numeric data

**Inconsistent Formatting**
- ❌ Mixed decimal places (1.23, 4.5, 6)
- ✅ Consistent precision (1.23, 4.50, 6.00)

**Too Many Columns**
- ❌ More than 6 columns
- ✅ Split into multiple tables or slides

### Advanced Customization

**Alternating Row Colors:**
```css
tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}
```

**Highlighting Specific Rows:**
```css
tbody tr.highlight {
  background-color: var(--accent);
  color: white;
}
```

## 2. Bar Chart (`bar-chart.html`)

### Purpose
Display categorical data comparison with vertical bars.

### Key Features
- 2D flat design
- SVG-based rendering
- Color-coded bars using design system
- Axis labels
- Scalable vector graphics

### Structure

```html
<div class="col-6">
  <div class="card">
    <h3>柱状图标题</h3>
    <div class="chart-container">
      <svg width="100%" height="300" viewBox="0 0 400 300">
        <!-- Axis -->
        <line x1="40" y1="260" x2="380" y2="260" stroke="#74788d" stroke-width="2"/>
        <line x1="40" y1="40" x2="40" y2="260" stroke="#74788d" stroke-width="2"/>
        
        <!-- Bars -->
        <rect x="60" y="100" width="50" height="160" fill="var(--aux3)" rx="2"/>
        <rect x="130" y="80" width="50" height="180" fill="var(--aux2)" rx="2"/>
        <rect x="200" y="120" width="50" height="140" fill="var(--aux4)" rx="2"/>
        <rect x="270" y="60" width="50" height="200" fill="var(--aux1)" rx="2"/>
        
        <!-- Labels -->
        <text x="85" y="280" text-anchor="middle" fill="#333" font-size="14">Q1</text>
        <text x="155" y="280" text-anchor="middle" fill="#333" font-size="14">Q2</text>
        <text x="225" y="280" text-anchor="middle" fill="#333" font-size="14">Q3</text>
        <text x="295" y="280" text-anchor="middle" fill="#333" font-size="14">Q4</text>
      </svg>
    </div>
  </div>
</div>
```

### Customization Points

**Bar Properties:**
- `x`: Horizontal position (start at 60, increment by 70)
- `y`: Top position (calculate: 260 - height)
- `width`: Bar width (50px recommended)
- `height`: Bar height (scale data to fit)
- `fill`: Color (use `var(--aux1)` to `var(--aux4)`)
- `rx`: Corner radius (2px for slight rounding)

**Data Scaling:**
- Max height: 220px (from y=40 to y=260)
- Calculate: `height = (value / max_value) * 220`
- Calculate: `y = 260 - height`

**Labels:**
- X-axis labels: Below bars (y=280)
- Y-axis labels: Optional, add to left of axis
- Font size: 14px for labels

### When to Use
- Quarterly comparisons (Q1-Q4)
- Category comparisons (Product A, B, C, D)
- Time series data (months, years)
- Any 4-6 categorical data points

### Common Mistakes

**Too Many Bars**
- ❌ More than 6 bars
- ✅ Split into multiple charts or use table

**Inconsistent Scaling**
- ❌ Bars don't reflect actual data ratios
- ✅ Calculate heights proportionally

**Missing Labels**
- ❌ No axis labels
- ✅ Always label x-axis categories

**Poor Color Choice**
- ❌ Random colors
- ✅ Use design system colors (`var(--aux1-4)`)

### Advanced Customization

**Adding Value Labels on Bars:**
```html
<text x="85" y="95" text-anchor="middle" fill="#333" font-size="12">120</text>
```

**Adding Y-Axis Grid Lines:**
```html
<line x1="40" y1="180" x2="380" y2="180" stroke="#ddd" stroke-width="1"/>
<line x1="40" y1="100" x2="380" y2="100" stroke="#ddd" stroke-width="1"/>
```

**Horizontal Bar Chart:**
Swap x/y coordinates for horizontal bars.

## 3. Radar Chart (`radar-chart.html`)

### Purpose
Display multi-dimensional metrics in spider/radar format.

### Key Features
- Polygon shape
- Multiple data series
- Axis lines from center
- Filled areas with transparency

### Structure

```html
<div class="col-6">
  <div class="card">
    <h3>雷达图标题</h3>
    <div class="chart-container">
      <svg width="100%" height="300" viewBox="0 0 400 300">
        <!-- Background grid -->
        <polygon points="200,60 340,130 340,230 200,300 60,230 60,130" 
                 fill="none" stroke="#ddd" stroke-width="1"/>
        
        <!-- Axis lines -->
        <line x1="200" y1="180" x2="200" y2="60" stroke="#ddd" stroke-width="1"/>
        <line x1="200" y1="180" x2="340" y2="130" stroke="#ddd" stroke-width="1"/>
        <line x1="200" y1="180" x2="340" y2="230" stroke="#ddd" stroke-width="1"/>
        <line x1="200" y1="180" x2="200" y2="300" stroke="#ddd" stroke-width="1"/>
        <line x1="200" y1="180" x2="60" y2="230" stroke="#ddd" stroke-width="1"/>
        <line x1="200" y1="180" x2="60" y2="130" stroke="#ddd" stroke-width="1"/>
        
        <!-- Data polygon -->
        <polygon points="200,80 300,140 280,220 200,260 120,210 110,140" 
                 fill="var(--aux1)" fill-opacity="0.3" stroke="var(--aux1)" stroke-width="2"/>
        
        <!-- Labels -->
        <text x="200" y="50" text-anchor="middle" fill="#333" font-size="12">指标1</text>
        <text x="350" y="125" text-anchor="middle" fill="#333" font-size="12">指标2</text>
        <text x="350" y="240" text-anchor="middle" fill="#333" font-size="12">指标3</text>
        <text x="200" y="315" text-anchor="middle" fill="#333" font-size="12">指标4</text>
        <text x="50" y="240" text-anchor="middle" fill="#333" font-size="12">指标5</text>
        <text x="50" y="125" text-anchor="middle" fill="#333" font-size="12">指标6</text>
      </svg>
    </div>
  </div>
</div>
```

### Customization Points

**Data Points:**
- Center: (200, 180)
- Radius: 120px
- Calculate points using trigonometry:
  - `x = 200 + radius * cos(angle)`
  - `y = 180 + radius * sin(angle)`

**Labels:**
- Position labels outside the polygon
- Use 12px font size
- Center-align text

**Styling:**
- `fill-opacity`: Transparency (0.3 recommended)
- `stroke-width`: Line thickness (2px)
- `fill`: Color (use design system colors)

### When to Use
- Skill assessments (6 dimensions)
- Product comparisons (multiple metrics)
- Performance evaluations
- Multi-dimensional data (5-7 axes)

### Common Mistakes

**Too Many Axes**
- ❌ More than 7 axes
- ✅ Limit to 5-7 metrics

**Poor Label Placement**
- ❌ Labels overlapping chart
- ✅ Position labels outside polygon

**Inconsistent Scaling**
- ❌ Axes not evenly spaced
- ✅ Use equal angles between axes

**Missing Context**
- ❌ No legend or explanation
- ✅ Add caption or legend

### Advanced Customization

**Multiple Data Series:**
```html
<!-- Series 1 -->
<polygon points="..." fill="var(--aux1)" fill-opacity="0.3" stroke="var(--aux1)"/>
<!-- Series 2 -->
<polygon points="..." fill="var(--aux2)" fill-opacity="0.3" stroke="var(--aux2)"/>
```

**Concentric Grid Lines:**
```html
<polygon points="..." fill="none" stroke="#ddd" stroke-width="1"/>
<polygon points="..." fill="none" stroke="#ddd" stroke-width="1"/>
```

## 4. Icons (`icons.html`)

### Purpose
Add visual indicators and icons to slides.

### Key Features
- SVG-based icons
- Linear style (outline)
- Scalable
- Color-customizable

### Structure

```html
<div class="col-4">
  <div class="card">
    <h3>图标标题</h3>
    <div class="icon-container">
      <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2">
        <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
      </svg>
      <p>图标说明文字</p>
    </div>
  </div>
</div>
```

### Customization Points

**Icon Properties:**
- `width/height`: Size (60px recommended)
- `stroke`: Color (use design system colors)
- `stroke-width`: Line thickness (2px standard)
- `viewBox`: Always "0 0 24 24"

**Common Icon Paths:**
- Checkmark: `<path d="M20 6L9 17l-5-5"/>`
- Arrow: `<path d="M5 12h14M12 5l7 7-7 7"/>`
- Warning: `<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0zM12 9v4M12 17h.01"/>`
- Info: `<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>`

### When to Use
- Feature highlights
- Key points
- Visual indicators
- Status indicators

### Common Mistakes

**Inconsistent Sizing**
- ❌ Different icon sizes on same slide
- ✅ Use consistent width/height

**Poor Color Choice**
- ❌ Random colors
- ✅ Use design system colors

**Overuse**
- ❌ Too many icons (more than 4-6 per slide)
- ✅ Use sparingly for emphasis

### Advanced Customization

**Colored Icons:**
```html
<svg fill="var(--accent)" stroke="none">
  <!-- Solid icon -->
</svg>
```

**Animated Icons:**
```css
.icon-container svg {
  transition: transform 0.3s;
}
.icon-container:hover svg {
  transform: scale(1.1);
}
```

## Component Integration Workflow

1. **Choose component**
   - Table: Tabular data with totals
   - Bar chart: 4-6 categorical comparisons
   - Radar chart: 5-7 dimensional metrics
   - Icons: Visual indicators

2. **Copy component HTML**
   - Read from `components/` directory
   - Copy entire component block

3. **Insert into slide**
   - Use appropriate `.col-*` class
   - Wrap in `.card` if needed

4. **Customize content**
   - Replace placeholder data
   - Adjust styling as needed
   - Ensure consistency

5. **Test rendering**
   - Verify layout
   - Check data accuracy
   - Ensure accessibility

## Common Component Issues

### Table Issues

**Symptom**: Numbers misaligned
**Cause**: Missing `.num` class
**Solution**: Add `.num` class to numeric columns

**Symptom**: Table overflows card
**Cause**: Too many columns or wide content
**Solution**: Reduce columns or split into multiple tables

### Chart Issues

**Symptom**: Chart distorted
**Cause**: Incorrect viewBox or dimensions
**Solution**: Use correct viewBox (0 0 400 300)

**Symptom**: Labels cut off
**Cause**: Labels positioned outside SVG
**Solution**: Adjust label positions or increase SVG size

### Icon Issues

**Symptom**: Icons not visible
**Cause**: Stroke color matches background
**Solution**: Use contrasting color from design system

**Symptom**: Icons pixelated
**Cause**: Using raster images instead of SVG
**Solution**: Always use SVG format

## Best Practices

1. **Use components as-is**: Don't modify core structure
2. **Maintain consistency**: Use design system colors
3. **Keep it simple**: Don't over-customize
4. **Test thoroughly**: Verify rendering in browser
5. **Consider accessibility**: Add alt text where appropriate

## Component Combinations

**Table + Chart:**
```html
<div class="col-6">
  <!-- Table component -->
</div>
<div class="col-6">
  <!-- Bar chart component -->
</div>
```

**Icons + Text:**
```html
<div class="col-4">
  <div class="card">
    <!-- Icon component -->
    <p>Description</p>
  </div>
</div>
```

**Multiple Charts:**
```html
<div class="col-6">
  <!-- Bar chart component -->
</div>
<div class="col-6">
  <!-- Radar chart component -->
</div>
```
