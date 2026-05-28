# Validation for Data Visualizations

**Purpose**: Verify chart correctness through progressive evidence layers, not just visual appearance.

**Core principle**: Progressive evidence for UI validation

---

## Progressive Evidence for UI Validation

### The Problem: Visual Inspection Only

Visual appearance doesn't prove mathematical correctness:

```javascript
// ❌ VISUAL-ONLY VALIDATION
function validateChart() {
    // Take screenshot
    console.log('Screenshot looks good!');

    // Ship it!
    return true;
}

// Missing:
// - Code review (using framework correctly?)
// - Edge case testing (weekend gaps?)
// - Mathematical verification (domain match?)
```

**Why insufficient**:
- Visual inspection misses subtle bugs (wavy lines at gaps)
- Doesn't test edge cases (holidays, nulls, irregular spacing)
- Doesn't verify mathematical correctness (domain compatibility)
- Screenshot only shows one data sample (not comprehensive)

---

### The Solution: Four-Layer Validation

**Validate through multiple evidence layers**:

```
Layer 4 (Strongest): Mathematical Verification
  ↓ Domain compatibility? Formula correct? Numerical stability?

Layer 3: Edge Case Testing
  ↓ Weekend gaps? Holidays? Nulls? Variable sampling?

Layer 2: Code Review
  ↓ Using framework correctly? Native features? Best practices?

Layer 1 (Weakest): Visual Inspection
  ↓ Does it look right? Screenshot acceptable?
```

---

## Layer 1: Visual Inspection

### Purpose
Verify visual appearance matches design intent.

### Methods
1. **Screenshot comparison**: Take screenshot, compare to reference design
2. **Manual inspection**: Load chart in browser, zoom in/out, check colors
3. **Design review**: Show to designer/user for feedback

### What to Check
- ✅ Pattern visible (not blending into background)
- ✅ Colors correct (green=bullish, red=bearish)
- ✅ Opacity appropriate (25-30% for web)
- ✅ Lines bold enough (3px visible on screen)
- ✅ Layering correct (data in front, fills behind)

### Example Validation
```javascript
// 1. Render chart
const chart = renderChart(data);

// 2. Take screenshot
await page.screenshot({ path: 'chart.png' });

// 3. Visual check
// - Pattern shaded region visible? ✅
// - Trendline bold and clear? ✅
// - Data not obscured? ✅
```

### Limitations
- **Only tests visual layer**: Doesn't verify mathematical correctness
- **Subjective**: "Looks good" depends on viewer
- **Single sample**: Screenshot shows one data configuration

**Verdict**: Necessary but insufficient (weakest evidence)

---

## Layer 2: Code Review

### Purpose
Verify code follows framework patterns and best practices.

### Methods
1. **Framework usage check**: Using native features vs custom code?
2. **Pattern compliance**: Following established patterns (dataset-to-dataset fill)?
3. **Configuration review**: Chart.js options correct (`type: 'time'` for time axis)?

### What to Check
- ✅ Using framework-native features (not custom implementations)
- ✅ Layer ordering explicit (`order: 1,2,3`)
- ✅ Axis type matches data domain (`type: 'time'` for timestamps)
- ✅ Fill mode correct (`fill: lowerIndex` for dataset-to-dataset)
- ✅ No magic numbers (opacity, line width documented)

### Example Validation
```javascript
// ❌ BAD: Custom polygon fill
const polygon = [...upper, ...lower.reverse()];
datasets.push({ data: polygon, fill: true });

// ✅ GOOD: Dataset-to-dataset fill
const lowerIndex = datasets.length;
datasets.push({ data: lowerLine, fill: false });
datasets.push({ data: upperLine, fill: lowerIndex });
```

### Checklist
- [ ] Framework-native features used (not custom code)
- [ ] Layer ordering explicit (order property set)
- [ ] Axis type matches domain (time, linear, category)
- [ ] Fill mode appropriate (false, true, index, origin)
- [ ] Colors semantic (green=bullish, red=bearish)
- [ ] Opacity within guidelines (25-30% web, 10-15% print)
- [ ] Line width prominent (3px for trendlines)

### Limitations
- **Doesn't test execution**: Code looks correct but might fail at runtime
- **Doesn't verify edge cases**: Code might work for perfect data but crash on gaps

**Verdict**: Stronger than visual (tests implementation), but still incomplete

---

## Layer 3: Edge Case Testing

### Purpose
Verify chart handles irregular data correctly (gaps, holidays, nulls).

### Why Edge Cases Matter
**Regular spacing hides bugs**:
```javascript
// Perfect data (daily, no gaps)
const perfectData = [
    { x: Date.parse('2024-01-01'), y: 100 },
    { x: Date.parse('2024-01-02'), y: 102 },
    { x: Date.parse('2024-01-03'), y: 104 },
    { x: Date.parse('2024-01-04'), y: 106 },
];
// Hides domain mismatch bug! (index spacing = time spacing)
```

**Irregular spacing reveals bugs**:
```javascript
// Real data (weekend gap)
const realData = [
    { x: Date.parse('2024-01-01'), y: 100 },  // Mon
    { x: Date.parse('2024-01-02'), y: 102 },  // Tue
    { x: Date.parse('2024-01-03'), y: 104 },  // Wed
    // Weekend gap (Thu-Sun missing)
    { x: Date.parse('2024-01-08'), y: 106 },  // Mon (5 days later!)
];
// Reveals domain mismatch! (wavy lines at gap)
```

---

### Edge Case Categories

#### 1. Weekend Gaps
**Pattern**: Stock markets closed on weekends

```javascript
const weekendGapData = [
    { x: Date.parse('2024-01-05'), y: 100 },  // Fri
    // Weekend gap
    { x: Date.parse('2024-01-08'), y: 102 },  // Mon (3 days later)
];

// Validation: Trendline should stay straight across gap
// If wavy → domain mismatch bug
```

---

#### 2. Holiday Gaps
**Pattern**: Irregular gaps (1-5 days depending on holiday)

```javascript
const holidayGapData = [
    { x: Date.parse('2024-12-23'), y: 100 },  // Mon
    { x: Date.parse('2024-12-24'), y: 102 },  // Tue
    // Christmas break (4 days)
    { x: Date.parse('2024-12-30'), y: 106 },  // Mon
];

// Validation: Pattern rendering correct despite variable gap
```

---

#### 3. Null Values
**Pattern**: Missing data points (API failure, data gap)

```javascript
const nullData = [
    { x: Date.parse('2024-01-01'), y: 100 },
    { x: Date.parse('2024-01-02'), y: null },  // Missing!
    { x: Date.parse('2024-01-03'), y: 104 },
];

// Validation: Chart doesn't crash, skips null gracefully
const filtered = data.filter(p => p.y !== null);
```

---

#### 4. Variable Sampling Rates
**Pattern**: Data frequency changes (daily → weekly → monthly)

```javascript
const variableSamplingData = [
    { x: Date.parse('2024-01-01'), y: 100 },  // Daily
    { x: Date.parse('2024-01-02'), y: 102 },  // Daily
    { x: Date.parse('2024-01-10'), y: 110 },  // Weekly (8 days)
    { x: Date.parse('2024-02-01'), y: 120 },  // Monthly (22 days)
];

// Validation: Regression handles variable spacing correctly
```

---

### Edge Case Testing Strategy

```javascript
describe('Chart Pattern Visualization', () => {
    it('should handle weekend gaps', () => {
        const data = createWeekendGapData();
        const trendline = fitLinearTrendline(data);

        // Visual check: Line straight?
        expect(trendline).toBeStraight();
    });

    it('should handle holiday gaps', () => {
        const data = createHolidayGapData();
        const pattern = detectPattern(data);

        // Rendering check: No crash?
        expect(() => renderPattern(pattern)).not.toThrow();
    });

    it('should handle null values', () => {
        const data = createDataWithNulls();
        const trendline = fitLinearTrendline(data);

        // Filter check: Nulls skipped?
        expect(trendline.length).toBeLessThan(data.length);
    });

    it('should handle variable sampling rates', () => {
        const data = createVariableSamplingData();
        const trendline = fitLinearTrendline(data);

        // Slope check: Correct despite irregular spacing?
        const expectedSlope = calculateExpectedSlope(data);
        expect(trendline.slope).toBeCloseTo(expectedSlope);
    });
});
```

---

### Visual Inspection Pattern

**Technique**: Zoom in on gap area to check for artifacts

```javascript
// 1. Render chart with edge case data
const chart = renderChart(weekendGapData);

// 2. Take screenshot focused on gap
await page.screenshot({
    path: 'weekend-gap-detail.png',
    clip: { x: 400, y: 200, width: 300, height: 200 }
});

// 3. Visual check
// - Line straight across gap? ✅
// - No kinks or curves? ✅
// - Slope consistent? ✅
```

---

### Limitations
- **Tests specific edge cases**: Can't test all possible irregular patterns
- **Doesn't verify algorithm**: Tests behavior, not mathematical correctness

**Verdict**: Strong evidence (catches real-world bugs), but not exhaustive

---

## Layer 4: Mathematical Verification

### Purpose
Verify mathematical correctness of algorithms (domain compatibility, formula accuracy).

### Methods
1. **Domain analysis**: Regression domain matches visualization axis domain?
2. **Formula verification**: Linear regression formula implemented correctly?
3. **Numerical stability**: Handles large timestamp values without precision loss?

### What to Check
- ✅ Domain compatibility (timestamps for time axis, not indices)
- ✅ Formula correctness (least squares: `slope = (n*sumXY - sumX*sumY) / (n*sumX2 - sumX*sumX)`)
- ✅ Numerical stability (normalize timestamps to avoid overflow)
- ✅ Edge case handling (n < 2 returns null, not crash)

---

### Domain Compatibility Verification

**Question**: Does regression domain match axis domain?

**Check**:
```javascript
// 1. Identify axis type
scales: {
    x: { type: 'time' }  // Continuous time domain
}

// 2. Verify regression uses same domain
function fitLinearTrendline(points) {
    // ✅ GOOD: Uses timestamps (p.x)
    const sumX = points.reduce((sum, p) => sum + p.x, 0);

    // ❌ BAD: Uses indices (i)
    const sumX = points.reduce((sum, p, i) => sum + i, 0);
}
```

**Domain compatibility matrix**:

| Axis Type | Correct Domain | Wrong Domain | Bug Symptom |
|-----------|----------------|--------------|-------------|
| `type: 'time'` | Timestamps (ms since epoch) | Array indices | Wavy at gaps |
| `type: 'linear'` | Numeric values | Array indices | Incorrect slope |
| `type: 'category'` | Category indices | Alphabetical | Wrong ordering |
| `type: 'logarithmic'` | Log-transformed values | Raw values | Curved line |

---

### Formula Correctness Verification

**Standard linear regression** (least squares):

```javascript
// Given: points = [{ x, y }, ...]
const n = points.length;

// Sums (use domain-appropriate X values!)
const sumX = points.reduce((sum, p) => sum + p.x, 0);
const sumY = points.reduce((sum, p) => sum + p.y, 0);
const sumXY = points.reduce((sum, p) => sum + p.x * p.y, 0);
const sumX2 = points.reduce((sum, p) => sum + p.x * p.x, 0);

// Slope (m) - CHECK THIS FORMULA
const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);

// Intercept (b) - CHECK THIS FORMULA
const intercept = (sumY - slope * sumX) / n;

// Apply: y = mx + b
return points.map(p => ({
    x: p.x,
    y: slope * p.x + intercept
}));
```

**Verification method**: Compare to reference implementation (NumPy, Excel)

```python
# Reference implementation (NumPy)
import numpy as np

x = np.array([timestamps])
y = np.array([values])

# NumPy linear regression
slope, intercept = np.polyfit(x, y, 1)

# Compare to JavaScript implementation
assert abs(js_slope - slope) < 1e-6
assert abs(js_intercept - intercept) < 1e-6
```

---

### Numerical Stability Verification

**Problem**: Timestamps are large numbers (ms since 1970)

```javascript
const timestamp = Date.parse('2024-01-01');  // 1704067200000 (10^12)
```

**Risk**: Numerical precision issues with large sums

```javascript
// ❌ UNSTABLE: Large timestamp values
const sumX = points.reduce((sum, p) => sum + p.x, 0);  // 10^15 magnitude!

// Potential precision loss in calculations
const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
```

**Mitigation**: Normalize to epoch (first point as origin)

```javascript
// ✅ STABLE: Normalize to first point
function fitLinearTrendline(points) {
    // Normalize to first point as epoch
    const epoch = points[0].x;
    const normalized = points.map(p => ({
        x: p.x - epoch,  // Now small values (0, 86400000, ...)
        y: p.y
    }));

    // Run regression on normalized data
    const { slope, intercept } = computeRegression(normalized);

    // Denormalize back to original timestamps
    return points.map(p => ({
        x: p.x,
        y: slope * (p.x - epoch) + intercept
    }));
}
```

---

### Limitations
- **Theoretical verification**: Tests formula, not all implementations
- **Doesn't test integration**: Algorithm correct but chart rendering might fail

**Verdict**: Strongest evidence (mathematical rigor), but needs other layers for completeness

---

## Progressive Validation Strategy

**Apply layers in order** (stop when bug found):

```
1. Visual Inspection
   ├─ Pass? → Continue to Layer 2
   └─ Fail? → Fix visual issues, restart

2. Code Review
   ├─ Pass? → Continue to Layer 3
   └─ Fail? → Fix code patterns, restart at Layer 1

3. Edge Case Testing
   ├─ Pass? → Continue to Layer 4
   └─ Fail? → Fix edge case handling, restart at Layer 1

4. Mathematical Verification
   ├─ Pass? → Ship it! ✅
   └─ Fail? → Fix algorithm, restart at Layer 1
```

**Rationale**:
- Early layers faster (visual check takes seconds)
- Later layers more rigorous (mathematical proof takes minutes)
- Bug fixes might affect earlier layers (restart validation)

---

## Validation Matrix

**Evidence strength by layer**:

| Layer | Evidence Type | Speed | Rigor | Catches |
|-------|---------------|-------|-------|---------|
| 1. Visual | Screenshot | Fast (seconds) | Low | Color, opacity, visibility issues |
| 2. Code | Review | Medium (minutes) | Medium | Framework misuse, anti-patterns |
| 3. Edge | Testing | Medium (minutes) | High | Domain bugs, crashes, gaps |
| 4. Math | Proof | Slow (hours) | Highest | Formula errors, numerical instability |

**When to stop**:
- **Prototype**: Layer 1 (visual) sufficient
- **Development**: Layer 2 (code) minimum
- **Production**: Layer 3 (edge) required
- **Critical systems**: Layer 4 (math) required

---

## Complete Validation Workflow

```javascript
// Layer 1: Visual Inspection
async function validateVisual(chart) {
    const screenshot = await page.screenshot();

    // Manual review
    console.log('Visual check:');
    console.log('- Pattern visible? ✅');
    console.log('- Colors correct? ✅');
    console.log('- Lines prominent? ✅');
}

// Layer 2: Code Review
function validateCode(implementation) {
    const checks = {
        usesNativeFeatures: checkFrameworkUsage(implementation),
        hasLayerOrdering: checkLayerOrdering(implementation),
        correctAxisType: checkAxisConfig(implementation),
        followsPatterns: checkPatternCompliance(implementation)
    };

    return Object.values(checks).every(Boolean);
}

// Layer 3: Edge Case Testing
describe('Edge Cases', () => {
    it('handles weekend gaps', () => {
        const data = createWeekendGapData();
        const result = fitLinearTrendline(data);
        expect(result).toBeStraight();
    });

    it('handles null values', () => {
        const data = createDataWithNulls();
        expect(() => fitLinearTrendline(data)).not.toThrow();
    });
});

// Layer 4: Mathematical Verification
function validateMathematical(implementation, reference) {
    const testData = generateTestData();

    const jsResult = implementation(testData);
    const referenceResult = reference(testData);  // NumPy

    // Compare slopes (within tolerance)
    expect(jsResult.slope).toBeCloseTo(referenceResult.slope, 6);
    expect(jsResult.intercept).toBeCloseTo(referenceResult.intercept, 6);
}
```

---

## Anti-Patterns

### ❌ Stopping at Visual Layer

```javascript
// BAD: Only visual validation
console.log('Screenshot looks good! Ship it!');
// Missing: Code review, edge cases, math verification
```

**Fix**: Apply all 4 layers for production code

---

### ❌ Testing with Perfect Data Only

```javascript
// BAD: Only testing regular spacing
const testData = [
    { x: Date.parse('2024-01-01'), y: 100 },
    { x: Date.parse('2024-01-02'), y: 102 },
    { x: Date.parse('2024-01-03'), y: 104 },
];
// Hides domain mismatch bugs!
```

**Fix**: Test with weekend gaps, holidays, nulls, variable sampling

---

### ❌ Skipping Mathematical Verification

```javascript
// BAD: Assuming code is correct without proof
function fitLinearTrendline(points) {
    // Some regression code...
    // Never verified against reference implementation!
}
```

**Fix**: Compare to reference (NumPy, Excel, Wolfram Alpha)

---

## Benefits

**Comprehensive coverage**:
- ✅ Visual issues caught (Layer 1)
- ✅ Code patterns verified (Layer 2)
- ✅ Edge cases tested (Layer 3)
- ✅ Math correctness proven (Layer 4)

**Progressive refinement**:
- ✅ Fast feedback (visual check in seconds)
- ✅ Deeper verification (rigorous layers as needed)
- ✅ Confidence building (each layer adds evidence)

**Bug prevention**:
- ✅ Catches bugs early (before deployment)
- ✅ Prevents regressions (tests codified)
- ✅ Documents intent (validation = specification)

---

## Real-World Application

**Case study**: Candlestick chart pattern trendlines

**Layer 1 (Visual)**: User feedback "I don't like the look"
- **Issue**: Simple thin lines, low visibility
- **Fix**: Shaded regions + bold lines
- **Result**: ✅ Patterns 3-5x more visible

**Layer 2 (Code)**: Code review
- **Issue**: Custom polygon fill (didn't work)
- **Fix**: Dataset-to-dataset fill (Chart.js native)
- **Result**: ✅ Rendering works correctly

**Layer 3 (Edge)**: Weekend gap testing
- **Issue**: Trendlines wavy at weekend gaps
- **Fix**: Changed to timestamp-based regression
- **Result**: ✅ Straight lines across gaps

**Layer 4 (Math)**: Domain analysis
- **Issue**: Index-based regression on time axis (domain mismatch)
- **Fix**: Timestamp-based regression (domain match)
- **Result**: ✅ Mathematical correctness verified

**Outcome**: All 4 layers passed → Deployed with confidence

---

## References

**Testing methodologies**:
- Property-based testing: https://fast-check.dev/
- Visual regression testing: https://percy.io/

**Reference implementations**:
- NumPy linear regression: https://numpy.org/doc/stable/reference/generated/numpy.polyfit.html
- Excel LINEST function: https://support.microsoft.com/en-us/office/linest-function-84d7d0d9-6e50-4101-977a-fa7abf772b6d

---

**See also**:
- [MATHEMATICAL-CORRECTNESS.md](MATHEMATICAL-CORRECTNESS.md#validation-checklist) - Domain compatibility checklist
- [FRAMEWORK-PATTERNS.md](FRAMEWORK-PATTERNS.md#testing-strategy) - Framework feature testing
- `docs/frontend/UI_PRINCIPLES.md` - Progressive evidence principle
- `.claude/evolution/2026-01-05-data-visualization-principles.md` - Real-world case study
