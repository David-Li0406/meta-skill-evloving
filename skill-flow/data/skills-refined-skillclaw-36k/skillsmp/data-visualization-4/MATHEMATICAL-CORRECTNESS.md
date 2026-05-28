# Mathematical Correctness for Data Visualizations

**Purpose**: Ensure mathematical overlays (trendlines, regressions, indicators) are geometrically correct, not just visually acceptable.

**Core principle**: Regression domain must match visualization axis domain

---

## Domain Compatibility

### The Problem: Domain Mismatch

**Symptom**: Trendlines appear wavy at weekend gaps, holidays, or irregular data spacing

**Root cause**: Using array indices for regression but timestamps for visualization axis

```javascript
// ❌ BAD: Index-based regression on continuous time axis
function fitLinearTrendline(points) {
    const n = points.length;

    // BUG: Using array indices (0, 1, 2, 3...) for X
    const sumX = points.reduce((sum, p, i) => sum + i, 0);
    const sumXY = points.reduce((sum, p, i) => sum + i * p.y, 0);
    const sumX2 = points.reduce((sum, p, i) => sum + i * i, 0);

    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;

    // Returns Y calculated from indices, but X uses timestamps
    return points.map((p, i) => ({
        x: p.x,                    // Real timestamp (milliseconds)
        y: slope * i + intercept   // BUG: Index-based Y
    }));
}

// Chart configuration
scales: {
    x: {
        type: 'time',  // Continuous calendar time (includes weekends)
    }
}
```

**Why it breaks**:
- Chart.js X-axis: Continuous time (includes weekend gaps)
- Regression X-domain: Array indices (0,1,2,3... uniform spacing)
- **Domain mismatch**: Y assumes 1-day spacing, but X has 3-day gaps (weekends)
- **Result**: Line "bends" at gaps (slope appears to change)

---

### Visual Impact of Domain Mismatch

```
Price Chart (continuous time axis):
Mon  Tue  Wed  [weekend gap]  Mon  Tue
 •    •    •                    •    •
  \    \    \                  /  /    ← Line "bends" at gap
   Index: 0→1→2              →3→4

Spacing in indices: 1, 1, 1, 1 (uniform)
Spacing on X-axis:  1d, 1d, 3d, 1d (irregular - gap!)

Result: Line slope changes at gap (looks wavy)
```

**Explanation**:
- Index 2→3: Increment of 1 (expects 1-day spacing)
- Actual time 2→3: 3 days (weekend gap)
- Line spreads same Y-change over 3x the X-distance
- Slope appears flatter (wavy appearance)

---

### The Solution: Domain Match

**Rule**: Regression X-domain MUST match visualization axis domain

```javascript
// ✅ GOOD: Timestamp-based regression matches time axis
function fitLinearTrendline(points) {
    const n = points.length;

    // Use actual timestamps (p.x) for X domain
    const sumX = points.reduce((sum, p) => sum + p.x, 0);
    const sumXY = points.reduce((sum, p) => sum + p.x * p.y, 0);
    const sumX2 = points.reduce((sum, p) => sum + p.x * p.x, 0);

    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;

    // Y calculated from timestamps - DOMAIN MATCH!
    return points.map((p) => ({
        x: p.x,                      // Real timestamp
        y: slope * p.x + intercept   // Timestamp-based Y
    }));
}

// Result: Lines stay straight across weekend gaps
```

---

## Domain Compatibility Matrix

| Axis Type | Correct Domain | Wrong Domain | Symptom |
|-----------|---------------|--------------|---------|
| **Continuous time** | Timestamps (ms since epoch) | Array indices | Wavy at gaps |
| **Discrete categories** | Category indices | Alphabetical order | Wrong ordering |
| **Log scale** | Log-transformed values | Raw values | Curved line |
| **Polar coordinates** | Angles (radians) | Linear spacing | Spiral artifacts |

---

## Domain Compatibility Rule

```
Regression domain MUST match visualization axis domain

Continuous time axis → Use timestamps in regression
Discrete index axis  → Use indices in regression
Mixed domains        → Convert to common domain first
```

---

## Testing Strategy

### Edge Case: Weekend Gaps

```javascript
// Test data with irregular spacing (weekend gap)
const testData = [
    { x: Date.parse('2024-01-01'), y: 100 },  // Mon
    { x: Date.parse('2024-01-02'), y: 102 },  // Tue
    { x: Date.parse('2024-01-03'), y: 104 },  // Wed
    // Weekend gap (Thu, Fri, Sat, Sun missing)
    { x: Date.parse('2024-01-08'), y: 106 },  // Mon (5 days later!)
    { x: Date.parse('2024-01-09'), y: 108 },  // Tue
];

const trendline = fitLinearTrendline(testData);

// Visual inspection: Line should stay straight across gap
// If wavy → domain mismatch bug
```

---

### Edge Case: Holidays

```javascript
// Variable gaps (holidays)
const testData = [
    { x: Date.parse('2024-12-23'), y: 100 },
    { x: Date.parse('2024-12-24'), y: 102 },
    // Christmas break: 4 days missing
    { x: Date.parse('2024-12-30'), y: 106 },
];
```

---

### Edge Case: Missing Data Points

```javascript
// Null values (missing data)
const testData = [
    { x: Date.parse('2024-01-01'), y: 100 },
    { x: Date.parse('2024-01-02'), y: null },  // Missing!
    { x: Date.parse('2024-01-03'), y: 104 },
];

// Regression should skip null values
const filtered = testData.filter(p => p.y !== null);
const trendline = fitLinearTrendline(filtered);
```

---

### Edge Case: Variable Sampling Rates

```javascript
// Mixed frequency (daily → weekly → monthly)
const testData = [
    { x: Date.parse('2024-01-01'), y: 100 },  // Daily
    { x: Date.parse('2024-01-02'), y: 102 },  // Daily
    { x: Date.parse('2024-01-10'), y: 110 },  // Weekly (8 days later)
    { x: Date.parse('2024-02-01'), y: 120 },  // Monthly (22 days later)
];

// Timestamp-based regression handles this correctly
// Index-based regression would assume uniform spacing
```

---

## Validation Checklist

Before deploying mathematical overlays:

- [ ] **Identify axis domain**: What's the X-axis? (time, categories, continuous)
- [ ] **Match regression domain**: Timestamps for time, indices for discrete
- [ ] **Test with weekend gaps**: Does line stay straight?
- [ ] **Test with holidays**: Handles irregular gaps?
- [ ] **Test with nulls**: Skips missing values gracefully?
- [ ] **Test with variable sampling**: Daily → weekly → monthly?
- [ ] **Verify Chart.js config**: `type: 'time'` for continuous time?

---

## Common Mistakes

### Mistake 1: Assuming Domains Are Equivalent

```javascript
// ❌ WRONG ASSUMPTION
// "Indices and timestamps are basically the same, right?"
const sumX = points.reduce((sum, p, i) => sum + i, 0);  // Indices
return { x: p.x, y: slope * i + intercept };             // Timestamps

// NO! Domain mismatch causes subtle but critical bugs
```

**Fix**: Use same domain for both X and Y calculations

---

### Mistake 2: Not Testing Edge Cases

```javascript
// ❌ TESTING WITH PERFECT DATA ONLY
const testData = [
    { date: '2024-01-01', value: 100 },
    { date: '2024-01-02', value: 102 },
    { date: '2024-01-03', value: 104 },
    { date: '2024-01-04', value: 106 },
];
// All perfectly spaced - hides bugs!
```

**Fix**: Test with irregular spacing (weekends, holidays, gaps)

---

### Mistake 3: Visual Inspection Only

```javascript
// ❌ STOPPING AT "LOOKS GOOD"
console.log('Screenshot looks good! Ship it!');
// Missing: Mathematical verification, edge case testing
```

**Fix**: Progressive validation (visual → code → edge → math)

---

## Linear Regression Formula

**Standard formula**: `y = mx + b`

**Least squares solution**:
```javascript
const n = points.length;

// Sums (use domain-appropriate X values!)
const sumX = points.reduce((sum, p) => sum + p.x, 0);
const sumY = points.reduce((sum, p) => sum + p.y, 0);
const sumXY = points.reduce((sum, p) => sum + p.x * p.y, 0);
const sumX2 = points.reduce((sum, p) => sum + p.x * p.x, 0);

// Slope (m)
const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);

// Intercept (b)
const intercept = (sumY - slope * sumX) / n;

// Apply to each point
return points.map(p => ({
    x: p.x,
    y: slope * p.x + intercept
}));
```

**Critical**: Use `p.x` (domain value), not `i` (array index)

---

## Numerical Stability

### Large Timestamp Values

**Issue**: Timestamps are large numbers (ms since 1970)

```javascript
const timestamp = Date.parse('2024-01-01');  // 1704067200000 (10^12)
```

**Risk**: Numerical precision issues with large sums

**Mitigation**: Normalize to epoch

```javascript
function fitLinearTrendline(points) {
    // Normalize to first point as epoch
    const epoch = points[0].x;
    const normalized = points.map(p => ({ x: p.x - epoch, y: p.y }));

    // Run regression on normalized data
    const trendline = computeRegression(normalized);

    // Denormalize back to original timestamps
    return trendline.map(p => ({ x: p.x + epoch, y: p.y }));
}
```

---

## Benefits

**Mathematical correctness**:
- ✅ Straight lines across irregular spacing
- ✅ Correct slope (domain-appropriate)
- ✅ No visual artifacts (wavy lines, curvature)

**Robustness**:
- ✅ Handles weekend gaps gracefully
- ✅ Works with holidays, missing data
- ✅ Variable sampling rates supported

**Professional quality**:
- ✅ Matches industry tools (TradingView, mplfinance)
- ✅ Mathematically rigorous (not just "looks okay")

---

## References

- **Linear regression**: [Wikipedia](https://en.wikipedia.org/wiki/Linear_regression)
- **Least squares method**: [Wikipedia](https://en.wikipedia.org/wiki/Least_squares)
- **Chart.js time scale**: [Docs](https://www.chartjs.org/docs/latest/axes/cartesian/time.html)

---

**See also**:
- [VALIDATION.md](VALIDATION.md#edge-case-testing) - Testing strategy
- `docs/frontend/UI_PRINCIPLES.md` - Domain compatibility principle
- `.claude/implementations/2026-01-05-proper-pattern-trendlines-all-types.md` - Real-world bug fix
