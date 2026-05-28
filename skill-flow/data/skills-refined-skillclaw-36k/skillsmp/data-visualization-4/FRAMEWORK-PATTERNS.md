# Framework Patterns for Data Visualizations

**Purpose**: Use charting framework's built-in features instead of custom implementations for robustness and maintainability.

**Core principle**: Framework-native over custom solutions

---

## Framework-Native Over Custom Solutions

### The Problem: Custom Implementation Fragility

Custom solutions are fragile, unmaintained, and harder to debug:

```javascript
// ❌ BAD: Custom polygon fill (doesn't work in Chart.js)
function createShadedRegion(upperLine, lowerLine) {
    // Concatenate upper + reversed lower to form polygon
    const polygon = [
        ...upperLine,                    // Left to right (top)
        ...lowerLine.slice().reverse()   // Right to left (bottom)
    ];

    return {
        type: 'line',
        data: polygon,
        fill: true,
        backgroundColor: 'rgba(38, 166, 154, 0.25)'
    };
}

// Chart.js doesn't render this correctly
// Result: No fill, or incorrect fill, or rendering artifacts
```

**Why it fails**:
- Chart.js expects separate datasets, not concatenated arrays
- Framework doesn't know polygon is closed shape
- Custom approach bypasses framework's fill logic
- No documentation, no community support

---

### The Solution: Dataset-to-Dataset Fill

**Chart.js native feature**: Fill area between two datasets

```javascript
// ✅ GOOD: Using Chart.js dataset-to-dataset fill
const datasets = [];

// 1. Draw lower boundary first
const lowerIndex = datasets.length;
datasets.push({
    label: 'Support Line',
    data: lowerLine,
    borderColor: '#26A69A',
    borderWidth: 3,
    fill: false,
    order: 2,
    pointRadius: 0
});

// 2. Draw upper boundary with fill TO lower dataset
datasets.push({
    label: 'Resistance Line',
    data: upperLine,
    borderColor: '#26A69A',
    borderWidth: 3,
    backgroundColor: 'rgba(38, 166, 154, 0.25)',  // 25% opacity
    fill: lowerIndex,  // Fill to support dataset (Chart.js native!)
    order: 2,
    pointRadius: 0
});

// Result: Shaded area between support and resistance
```

**Why it works**:
- Uses Chart.js's built-in fill feature
- Documented in official Chart.js docs
- Tested by framework maintainers
- Handles edge cases (nulls, gaps) automatically

---

## Research Pattern: Check Docs Before Implementing

**Before writing custom code, research framework capabilities:**

### Step 1: Identify the Need

"I need to fill the area between two trendlines"

### Step 2: Search Framework Documentation

**Query**: "Chart.js fill area between lines"

**Resources**:
- Official docs: https://www.chartjs.org/docs/latest/charts/line.html#filling-modes
- GitHub issues: Search for similar use cases
- Stack Overflow: Real-world examples

### Step 3: Evaluate Native Feature

**Questions**:
- Does framework have built-in feature?
- Does it handle my use case?
- Is it well-documented?
- Are there community examples?

### Step 4: Choose Implementation Path

**If native feature exists**: Use it (prefer framework-native)
**If native feature insufficient**: Extend it (composition over custom)
**If no native feature**: Implement custom (last resort)

---

## Chart.js Fill Modes

### Fill Mode: `false` (No Fill)
```javascript
datasets.push({
    data: points,
    fill: false  // Just a line, no fill
});
```

**Use when**: Simple trendlines without shaded regions

---

### Fill Mode: `true` or `'origin'` (Fill to Zero)
```javascript
datasets.push({
    data: points,
    fill: true,  // or fill: 'origin'
    backgroundColor: 'rgba(38, 166, 154, 0.25)'
});
```

**Use when**: Area chart (fill from line to zero axis)

**Example**: Volume chart, cumulative metrics

---

### Fill Mode: `'+1'` or `'-1'` (Fill to Adjacent Dataset)
```javascript
datasets.push({ data: line1, fill: false });   // Dataset 0
datasets.push({ data: line2, fill: '-1' });    // Fill to previous dataset
```

**Use when**: Filling between consecutive datasets

**Example**: Confidence bands around main line

---

### Fill Mode: `<number>` (Fill to Specific Dataset Index)
```javascript
const lowerIndex = datasets.length;
datasets.push({ data: lowerLine, fill: false });  // Dataset at lowerIndex
datasets.push({ data: upperLine, fill: lowerIndex });  // Fill to lowerIndex
```

**Use when**: Filling between non-adjacent datasets (most flexible)

**Example**: Channel patterns (support/resistance with gap in between)

---

## Polygon vs Dataset-to-Dataset Fill

### Comparison Table

| Aspect | Custom Polygon | Dataset-to-Dataset Fill |
|--------|----------------|-------------------------|
| **Implementation** | Concatenate arrays | Reference dataset index |
| **Framework support** | None (custom) | Native Chart.js feature |
| **Documentation** | None | Official docs |
| **Edge cases** | Manual handling | Automatic |
| **Maintenance** | Your responsibility | Framework handles |
| **Community support** | None | Stack Overflow, GitHub |
| **Rendering** | May not work | Guaranteed to work |

---

## When Custom Solutions Are Acceptable

**Valid reasons for custom implementation**:

1. **Framework limitation**: Native feature doesn't exist and can't be composed
2. **Performance critical**: Native feature too slow for your use case
3. **Unique requirement**: Highly specialized visualization (not general pattern)
4. **Framework constraint**: Using framework that doesn't support feature

**Requirements for custom solutions**:
- Document why custom (link to framework limitation)
- Add tests for edge cases (nulls, gaps, irregular spacing)
- Consider contributing to framework (if widely useful)
- Plan for maintenance (who owns it?)

---

## D3.js Patterns (Alternative Framework)

### D3.js Area Generator

**Native feature**: `d3.area()` for shaded regions

```javascript
// D3.js native area generator
const area = d3.area()
    .x(d => xScale(d.x))
    .y0(d => yScale(d.lower))  // Lower boundary
    .y1(d => yScale(d.upper)); // Upper boundary

// Render
svg.append('path')
    .datum(data)
    .attr('fill', 'rgba(38, 166, 154, 0.25)')
    .attr('d', area);
```

**When to use D3.js**:
- Need fine-grained control over SVG
- Complex custom visualizations
- Interactive transitions/animations
- Large datasets (Canvas rendering)

**When to use Chart.js**:
- Standard chart types (line, bar, candlestick)
- Quick implementation
- Responsive design built-in
- Simpler API

---

## Recharts Patterns (React Framework)

### Recharts Area Component

**Native feature**: `<Area>` component for shaded regions

```javascript
import { AreaChart, Area, XAxis, YAxis } from 'recharts';

<AreaChart data={data}>
  <XAxis dataKey="x" type="number" domain={['dataMin', 'dataMax']} />
  <YAxis />
  <Area
    type="monotone"
    dataKey="value"
    fill="rgba(38, 166, 154, 0.25)"
    stroke="#26A69A"
    strokeWidth={3}
  />
</AreaChart>
```

**When to use Recharts**:
- React application
- Declarative chart configuration
- TypeScript support
- Built-in responsiveness

---

## Framework Selection Guide

### Chart.js
**Strengths**: Simple API, canvas rendering (fast), candlestick plugin available
**Weaknesses**: Less flexible than D3, limited custom shapes
**Best for**: Standard charts with mathematical overlays

### D3.js
**Strengths**: Maximum flexibility, SVG control, rich ecosystem
**Weaknesses**: Steep learning curve, verbose API
**Best for**: Highly custom visualizations, complex interactions

### Recharts
**Strengths**: React integration, declarative API, TypeScript
**Weaknesses**: Smaller community than Chart.js/D3, less flexible
**Best for**: React apps with standard chart types

### Plotly.js
**Strengths**: 3D charts, scientific plots, interactive
**Weaknesses**: Large bundle size, limited customization
**Best for**: Scientific/statistical visualizations

---

## Anti-Patterns

### ❌ Implementing Custom Before Researching

```javascript
// BAD: Writing custom polygon fill without checking docs
function customFillBetweenLines(upper, lower) {
    // 100 lines of custom code...
}
// Later discover Chart.js has built-in feature!
```

**Fix**: Research framework docs FIRST, implement custom LAST

---

### ❌ Mixing Framework Patterns Inconsistently

```javascript
// BAD: Using native feature for one pattern, custom for another
datasets.push({ fill: lowerIndex });  // Native (pattern 1)
datasets.push({ data: customPolygon });  // Custom (pattern 2)
// Result: Inconsistent behavior, harder maintenance
```

**Fix**: Use framework-native consistently across all patterns

---

### ❌ Not Testing Framework Limits

```javascript
// BAD: Assuming framework handles edge case without testing
datasets.push({ fill: lowerIndex });
// Untested: What if lower dataset has nulls? Gaps? Different length?
```

**Fix**: Test edge cases even with native features (nulls, gaps, variable length)

---

## Benefits

**Robustness**:
- ✅ Framework handles edge cases automatically
- ✅ Tested by thousands of users
- ✅ Bug fixes from maintainers

**Maintainability**:
- ✅ Documented in official docs
- ✅ Community support (Stack Overflow, GitHub)
- ✅ Framework upgrades bring improvements

**Development speed**:
- ✅ Less code to write (configuration > implementation)
- ✅ Faster debugging (known issues documented)
- ✅ Easier onboarding (standard patterns)

---

## References

**Chart.js**:
- Fill modes: https://www.chartjs.org/docs/latest/charts/line.html#filling-modes
- Area charts: https://www.chartjs.org/docs/latest/charts/area.html

**D3.js**:
- Area generator: https://d3js.org/d3-shape/area
- Official examples: https://observablehq.com/@d3/area-chart

**Recharts**:
- Area component: https://recharts.org/en-US/api/Area
- Documentation: https://recharts.org/en-US/

---

**See also**:
- [VISUAL-HIERARCHY.md](VISUAL-HIERARCHY.md#shaded-regions) - How to use fills for visual hierarchy
- [VALIDATION.md](VALIDATION.md#code-review-layer) - How to verify framework usage correctness
- `docs/frontend/UI_PRINCIPLES.md` - Framework-native principle
