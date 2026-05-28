# SciChart Engine Series Types

The engine supports various series types, each optimized for specific scientific and analytical data.

## 1D & 2D Series

### Line & Scatter
- `line`: Standard connected line.
- `scatter`: Individual data points with customizable symbols.
- `both`: Line with data point markers.

```typescript
chart.addSeries({
  id: 's1',
  type: 'line', // or 'scatter', 'both'
  data: { x, y },
  style: { color: '#00f2ff', width: 2, pointSize: 5, symbol: 'circle' }
});
```

### Specialized Scientific Charts
- `boxplot`: Statistical distribution (low, Q1, median, Q3, high).
- `errorbars`: Visualization of uncertainty (yError, xError).
- `ternary`: Compositional data of 3 components (a + b + c = 1).
- `waterfall`: Cumulative effect of sequentially introduced values.

### Area & Band
- `area`: Filled area from Y to 0.
- `band`: Filled area between two Y lines (Y1 and Y2).

```typescript
chart.addSeries({
  id: 'range',
  type: 'band',
  data: { x, y, y2 },
  style: { fill: 'rgba(0, 242, 255, 0.2)', stroke: '#00f2ff' }
});
```

### Financial & Discrete
- `candlestick`: OHLC data for financial analysis.
- `bar`: Discrete vertical or horizontal bars.
- `step`: Discrete value changes.
- `step+scatter`: Step line with markers at data points.

### Heatmaps
- `heatmap`: 2D intensity maps.

```typescript
chart.addHeatmap({
  id: 'thermal',
  data: {
    x: [0, 10], // Range
    y: [0, 10], // Range
    values: new Float32Array([...]) // Flattened 2D array
  },
  colorMap: {
    minimum: 0, maximum: 100,
    gradient: [{ offset: 0, color: 'blue' }, { offset: 1, color: 'red' }]
  }
});
```

### Indicators (KPIs)
- `gauge`: Radial or linear dials for single value metrics.
- `sankey`: Flow diagrams showing transitions between states.

## Data Structures
Always use **Typed Arrays** for maximum performance.

| Property | Description | Types |
|----------|-------------|-------|
| `x` | X-coordinates | `Float32Array`, `Float64Array` |
| `y` | Y-coordinates | `Float32Array`, `Float64Array` |
| `y2` | Secondary Y (for `band`) | `Float32Array`, `Float64Array` |
| `open`, `high`, `low`, `close` | OHLC (for `candlestick`) | `Float32Array`, `Float64Array` |
| `median` | Median (for `boxplot`) | `Float32Array`, `Float64Array` |
| `yError`, `yErrorPlus`, `yErrorMinus` | Error values | `Float32Array`, `Float64Array` |
| `a`, `b`, `c` | Ternary components | `Float32Array`, `Float64Array` |

## Scatter Symbols
Supported shapes: `circle`, `square`, `diamond`, `triangle`, `triangleDown`, `cross`, `x`, `star`.
