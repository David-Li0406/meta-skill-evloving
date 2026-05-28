# SciChart Engine API Summary

## Creation & Lifecycle
- `createChart(options)`: Initialize a chart.
- `chart.destroy()`: Cleanup WebGL context and listeners.
- `chart.resize()`: Manually trigger a resize.

## Data & Series
- `chart.addSeries(options)`: Add a new series.
  - Types: `line`, `scatter`, `step`, `band`, `area`, `bar`, `heatmap`, `boxplot`, `waterfall`, `ternary`.
- `chart.updateSeries(id, data)`: Update data for an existing series.
- `chart.appendData(id, x, y)`: Efficiently append real-time data.
- `chart.removeSeries(id)`: Remove a series.

## Cursor & Crosshair
- `chart.enableCursor(options)`: Enable cursor with crosshair and tooltips.
- `chart.disableCursor()`: Hide the cursor.

### Cursor Options
```typescript
chart.enableCursor({
  enabled: true,
  crosshair: true,                    // Show crosshair lines
  snap: true,                         // Snap to data points
  valueDisplayMode: 'corner',         // 'disabled' | 'floating' | 'corner'
  cornerPosition: 'top-right',        // 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right'
  lineStyle: 'dashed',                // 'solid' | 'dashed' | 'dotted'
  formatter: (x, y, seriesId) => `X: ${x.toFixed(2)}\nY: ${y.toFixed(4)}`,
});
```

**Value Display Modes:**
- `'floating'` (default): Tooltip follows cursor
- `'corner'`: Fixed position in corner of plot area
- `'disabled'`: No coordinate values shown (crosshair lines only)

## Interaction Modes
- `chart.setMode(mode)`: Change interaction mode (`pan`, `boxZoom`, `select`, `delta`, `peak`).

## Annotations
- `chart.addAnnotation(options)`: Types include `text`, `horizontal-line`, `vertical-line`, `rectangle`, `band`, `arrow`.
- `chart.updateAnnotation(id, options)`: Dynamic update.
- `chart.removeAnnotation(id)`: Cleanup.

## Events
Subscribe using `chart.on(event, callback)`:
- `render`: `{ fps, frameTime }`
- `zoom`: `{ x, y }` (axis ranges)
- `pan`: `{ deltaX, deltaY }`
- `click`: `{ x, y, seriesId? }`
- `measure`: Fired by tools like `delta` or `peak` with results.

## Advanced View Control
- `chart.resetZoom()`: Return to original scale.
- `chart.getViewBounds()`: Get current visible data range.
- `chart.updateXAxis(options)`: Change X-axis labels, scale type, etc.
- `chart.updateYAxis(options)`: Change Y-axis properties.

## Multi-Axis
- `chart.addYAxis(options)`: Add secondary Y-axis (e.g., `yAxis2`).
- Mapping a series: `chart.addSeries({ ..., yAxisId: 'yAxis2' })`.

## Themes
- `chart.setTheme(themeNameOrConfig)`: Predefined: `midnight`, `electrochemistry`, `dark`, `light`.
- `createTheme(config)`: Create a brand-new design system.

## Layout Configuration
Configure via `createChart({ layout: {...} })`:

- **Legend Options**:
  - `legend.highlightOnHover`: Change color on hover (default: `false`)
  - `legend.bringToFrontOnHover`: Bring series to front (default: `true`)
  - `legend.position`: Position preset or `{x, y}` coordinates

- **Margins & Spacing**:
  - `margins`: `{ top, right, bottom, left }` - Container to chart spacing
  - `plotPadding`: `{ top, right, bottom, left }` - Plot area internal padding
  - `xAxisLayout.titleGap`, `yAxisLayout.titleGap`: Axis to title spacing

- **Other**:
  - `title`: Chart title configuration
  - `toolbarPosition`: Toolbar placement preset or custom
