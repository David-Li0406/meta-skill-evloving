# SciChart Engine Plugins Guide

Plugins are imported from `scichart-engine/plugins/[name]`.

## Analysis (`scichart-analysis`)
Provides mathematical operations on data.
- `detectPeaks(seriesId, options)`
- `detectCycles(seriesId, options)`
- `movingAverage(seriesId, windowSize)`
- `fft(seriesId)`
- `singleFrequencyFilter(seriesId, frequency)`

## Tools (`scichart-tools`)
Interactive measurement and interrogation tools.
- `delta`: Measure distance and slope.
- `peak`: Integrate area under a curve.
- `tooltip`: Enhanced tooltips for data points.

### Native Cursor (Recommended)

For crosshair functionality, use the **native cursor API** instead of plugins:

```typescript
// Enable cursor with crosshair
chart.enableCursor({
  enabled: true,
  crosshair: true,
  snap: true,
  valueDisplayMode: 'corner',        // 'disabled' | 'floating' | 'corner'
  cornerPosition: 'top-right',       // Position for 'corner' mode
  lineStyle: 'dashed',               // 'solid' | 'dashed' | 'dotted'
});

// Disable cursor
chart.disableCursor();
```

**Value Display Modes:**
- `'floating'` (default): Tooltip follows the cursor
- `'corner'`: Values displayed in a fixed corner box
- `'disabled'`: Crosshair lines only, no coordinate values

## ML Integration (`scichart-ml-integration`)
Integrates with Machine Learning models for prediction and anomaly detection.
- `chart.ml.predict(seriesId, model)`
- `chart.ml.detectAnomalies(seriesId, algorithm)`

## LaTeX (`scichart-latex`)
Native LaTeX rendering for mathematical expressions. When active, it automatically handles LaTeX strings in:
- **Chart Titles**: `layout: { title: { text: '\\Delta E = mc^2' } }`
- **Axis Labels**: `xAxis: { label: 'Time (\\mu s)' }`
- **Annotations**: Using `latex: true` option.

```typescript
chart.latex.render('\\int_0^\\infty e^{-x^2} dx', ctx, x, y);
```

## Regression (`scichart-regression`)
Advanced curve fitting.
- `chart.regression.fit(seriesId, 'polynomial', { degree: 3 })`

## Data Export (`scichart-data-export`)
Enhanced export capabilities (MATLAB, Python, Excel, Binary).
- `chart.dataExport.toMATLAB()`
- `chart.dataExport.toExcel()`
- `chart.dataExport.toNativeBinary()`

## High Performance (`scichart-virtualization`, `scichart-gpu`)
Handle massive datasets (>10M points) and complex computations.
- `PluginVirtualization`: Dynamic level-of-detail for huge files.
- `PluginGpu`: Offload heavy calculations or use WebGPU for rendering.
- `PluginOffscreen`: Run rendering in a Web Worker to keep main thread responsive.

## UI & Aesthetics
- `PluginContextMenu`: Glassmorphism context menus for chart actions.
- `PluginLoading`: Customized loading indicators and progress bars.
- `PluginThemeEditor`: Interactively tweak chart styles at runtime.

## Accessibility & Localization
- `PluginI18n`: Support for multi-language labels and date formatting.
- `PluginKeyboard`: Mapping chart actions (zoom, pan) to keyboard shortcuts.

## Real-time & Synchronization
- `PluginStreaming`: Efficiently handle WebSocket data feeds.
- `PluginSync`: Synchronize zoom/pan across multiple chart instances.
