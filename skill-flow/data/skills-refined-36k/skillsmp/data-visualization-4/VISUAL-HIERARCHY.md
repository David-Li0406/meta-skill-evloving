# Visual Hierarchy for Data Visualizations

**Purpose**: Make chart overlays (patterns, trendlines, indicators) visually prominent without obscuring underlying data.

**Core principle**: Shaded regions + bold trendlines + explicit layer ordering = visual hierarchy

---

## Visual Prominence Through Layering

### The Problem

Simple thin lines blend into busy charts:

```javascript
// ❌ LOW VISIBILITY
datasets.push({
    type: 'line',
    data: trendlinePoints,
    borderColor: '#FF6B6B',
    borderWidth: 2,  // Too thin (2px)
    // No fill, no layering
});
```

**Result**: Pattern hard to see against candlesticks (low contrast, no depth)

---

### The Solution

**Three-layer approach**:

```javascript
// ✅ HIGH VISIBILITY

// Layer 3: Fill area (rendered behind trendlines)
datasets.push({
    label: 'Pattern Area',
    data: polygonPoints,
    backgroundColor: 'rgba(38, 166, 154, 0.25)',  // 25% opacity
    fill: true,
    borderColor: 'transparent',  // No outline on fill itself
    order: 3,  // Behind trendlines
    pointRadius: 0
});

// Layer 2: Trendline (rendered in front of fill)
datasets.push({
    label: 'Trendline',
    data: trendlinePoints,
    borderColor: '#26A69A',  // Solid color
    borderWidth: 3,  // Bold (3px, not 2px)
    fill: false,
    order: 2,  // In front of fill
    pointRadius: 0
});

// Layer 1: Data (highest priority - always visible)
datasets.push({
    type: 'candlestick',
    data: ohlcData,
    order: 1  // Front-most layer
});
```

---

## Layer Ordering Strategy

### Chart.js Layer System

Chart.js renders datasets in `order` (lower number = front):

```
Layer 1 (order: 1) - Data layer (candlesticks, line chart)
  ↑ Always visible, highest priority

Layer 2 (order: 2) - Overlay layer (trendlines, pattern boundaries)
  ↑ Clear boundaries, in front of fills

Layer 3 (order: 3) - Context layer (shaded fills, highlighted regions)
  ↑ Provides emphasis without obscuring

Layer 4 (order: 4) - Background layer (support/resistance lines, grid)
  ↑ Contextual information, lowest priority
```

### Implementation

```javascript
const datasets = [];

// Add in any order - Chart.js sorts by `order` property
datasets.push({ label: 'Fill', order: 3 });       // Renders 3rd
datasets.push({ label: 'Data', order: 1 });       // Renders 1st
datasets.push({ label: 'Trendline', order: 2 });  // Renders 2nd
datasets.push({ label: 'Grid', order: 4 });       // Renders 4th
```

**Effect**: Predictable z-index (data always visible, fills never obscure)

---

## Opacity Guidelines

### Web vs Print

**Screen displays** (backlit):
- Fill opacity: 25-30% (higher than print)
- Visibility threshold: 20% minimum
- Recommended: 25% for patterns, 30% for confidence bands

**Print/paper** (reflective):
- Fill opacity: 10-15% (lower than screen)
- Based on mplfinance defaults
- Screen requires higher opacity for same visual weight

### Testing Strategy

```javascript
// Test on actual medium (not code-only)
const opacity = isWeb ? 0.25 : 0.12;

// Screenshot on screen, review visibility
// Print to PDF, check if too bold/subtle
```

---

## Color Palette

### Semantic Colors (Financial Domain)

**Bullish patterns** (green):
```javascript
borderColor: '#26A69A'                  // Teal green (solid)
fillColor: 'rgba(38, 166, 154, 0.25)'   // 25% opacity
```

**Bearish patterns** (red):
```javascript
borderColor: '#EF5350'                  // Red (solid)
fillColor: 'rgba(239, 83, 80, 0.25)'    // 25% opacity
```

**Neutral patterns** (purple):
```javascript
borderColor: '#9C27B0'                  // Purple (solid)
fillColor: 'rgba(156, 39, 176, 0.25)'   // 25% opacity
```

**Rationale**:
- Green/red: Financial convention (bullish/bearish)
- Purple: Distinct from support/resistance, clearly neutral
- Consistent across all pattern types

---

## Line Styling

### Width Guidelines

**Data layer** (candlesticks, main chart):
- Candlestick body: Default
- Wicks: 1px

**Overlay layer** (trendlines):
- Pattern trendlines: **3px** (bold, prominent)
- Moving averages: 2-2.5px (visible but less prominent)
- Support/resistance: 2px (contextual)

**Context layer** (fills):
- Border: `transparent` (fill has no outline)
- Fill only (shaded area provides prominence)

### Style Variations

**Solid lines** (default):
```javascript
borderDash: []  // Solid (no dashing)
```

**Dashed lines** (special cases):
```javascript
borderDash: [10, 5]  // 10px dash, 5px gap
// Use for: necklines (H&S), projected trendlines
```

**Why dashing**:
- Distinguishes projected/hypothetical from actual
- Neckline (H&S) visually different from trendline

---

## Shaded Regions

### Polygon Creation

**Technique**: Combine upper boundary + reversed lower boundary

```javascript
// Upper line (left to right)
const upperLine = [
    { x: t1, y: y1 },
    { x: t2, y: y2 },
    { x: t3, y: y3 }
];

// Lower line (left to right)
const lowerLine = [
    { x: t1, y: y0 },
    { x: t2, y: y1 },
    { x: t3, y: y2 }
];

// Create closed polygon
const polygonData = [
    ...upperLine,                    // Left to right (top)
    ...lowerLine.slice().reverse()   // Right to left (bottom)
];
// Result: Closed polygon (continuous boundary)
```

### Chart.js Implementation

**Option 1: Polygon array** (doesn't work well in Chart.js)
```javascript
// ❌ BAD: Concatenating arrays
datasets.push({
    data: [...upper, ...lower.reverse()],
    fill: true
});
// Chart.js doesn't render this correctly
```

**Option 2: Dataset-to-dataset fill** (Chart.js native)
```javascript
// ✅ GOOD: Using Chart.js fill feature
const lowerIndex = datasets.length;
datasets.push({
    label: 'Lower Boundary',
    data: lowerLine,
    fill: false,
    order: 2
});

datasets.push({
    label: 'Upper Boundary',
    data: upperLine,
    fill: lowerIndex,  // Fill TO lower dataset
    backgroundColor: 'rgba(38, 166, 154, 0.25)',
    order: 2
});
```

**See**: [FRAMEWORK-PATTERNS.md](FRAMEWORK-PATTERNS.md#dataset-to-dataset-fill) for details

---

## Pattern-Specific Styling

### Wedge Patterns

**Visual**: Converging triangle with shaded area

```javascript
const color = pattern === 'wedge_rising' ? '#26A69A' : '#EF5350';
const fillColor = pattern === 'wedge_rising'
    ? 'rgba(38, 166, 154, 0.25)'
    : 'rgba(239, 83, 80, 0.25)';

// Fill area (order: 3)
// Resistance line (order: 2, width: 3px)
// Support line (order: 2, width: 3px)
```

---

### Flag/Pennant Patterns

**Visual**: Rectangular or triangular consolidation area

```javascript
// Shaded rectangle
backgroundColor: 'rgba(38, 166, 154, 0.25)',  // 25% opacity
borderWidth: 2.5,  // Slightly thinner than wedge
borderDash: [],    // Solid (not dashed)
```

---

### Triangle Patterns

**Visual**: Converging triangle with type-specific colors

```javascript
const fillColor = type === 'ascending' ? 'rgba(38, 166, 154, 0.25)' :  // Green
                  type === 'descending' ? 'rgba(239, 83, 80, 0.25)' :  // Red
                  'rgba(156, 39, 176, 0.25)';  // Purple (symmetrical)

borderWidth: 3,  // Bold
opacity: 0.25    // Standard web opacity
```

---

### Head & Shoulders Patterns

**Visual**: Band around neckline (subtle emphasis)

```javascript
// Neckline
borderWidth: 3,
borderDash: [10, 5],  // Dashed (distinguishes from trendline)

// Shaded band (± 5% of pattern height)
backgroundColor: 'rgba(38, 166, 154, 0.08)',  // Lower opacity (8%)
// Subtle because neckline is already prominent
```

---

### Double Top/Bottom Patterns

**Visual**: Horizontal zone at extreme price

```javascript
// Horizontal line at peak/trough
borderWidth: 3,
borderDash: [],  // Solid

// Shaded band (± 3% of pattern height)
backgroundColor: 'rgba(239, 83, 80, 0.10)',  // 10% opacity
// Moderate opacity for horizontal zone
```

---

## Benefits

**Visual prominence**:
- ✅ Patterns 3-5x more visible
- ✅ Immediate recognition (shaded areas draw attention)
- ✅ Matches industry standards (TradingView, mplfinance)

**Clarity**:
- ✅ Data always visible (layering prevents obscuring)
- ✅ Clear boundaries (bold trendlines + fills)
- ✅ Visual hierarchy (importance conveyed through layers)

**Professional appearance**:
- ✅ Looks polished (not amateur)
- ✅ User expectations met (familiar from pro tools)

---

## Anti-Patterns

### ❌ All Elements Same Layer
```javascript
datasets.push({ order: 1 });  // Fill
datasets.push({ order: 1 });  // Line
datasets.push({ order: 1 });  // Data
// Result: Random rendering order, unpredictable visibility
```

**Fix**: Explicit layer ordering (1=data, 2=lines, 3=fills)

---

### ❌ Opacity Too Low (Web)
```javascript
backgroundColor: 'rgba(38, 166, 154, 0.10)',  // 10% (too subtle for screen)
// Result: Fill barely visible
```

**Fix**: 25-30% for web displays (test on actual screen, not code)

---

### ❌ Thin Trendlines
```javascript
borderWidth: 1,  // Too thin (1px)
// Result: Lines blend into chart, hard to see
```

**Fix**: 3px for prominence (2.5px minimum)

---

## References

- **Industry examples**: TradingView (shaded patterns), mplfinance (fill_between)
- **Chart.js docs**: [Dataset fill modes](https://www.chartjs.org/docs/latest/charts/line.html#filling-modes)
- **Related**: [FRAMEWORK-PATTERNS.md](FRAMEWORK-PATTERNS.md) for Chart.js-specific patterns

---

**See also**:
- `docs/frontend/UI_PRINCIPLES.md` - Comprehensive UI principles
- `.claude/implementations/2026-01-05-shaded-pattern-visualization.md` - Implementation case study
