# Layout & Positioning Guide

This module provides detailed control over chart component positioning, spacing, and behavior.

## Overview

The layout system allows fine-grained customization of:
- **Legend** - positioning, hover behavior, and styling
- **Toolbar** - position presets and custom placement
- **Margins & Padding** - chart boundaries and plot area spacing
- **Axis Layout** - spacing between axis elements
- **Chart Title** - title configuration and positioning

> **Note**: Crosshair/cursor configuration is done via `enableCursor()`, not the layout options.

## Quick Start

```typescript
import { createChart } from 'scichart-engine';

const chart = createChart({
  container: document.getElementById('chart'),
  layout: {
    legend: {
      highlightOnHover: false,  // Don't change color (default)
      bringToFrontOnHover: true, // Bring series to front (default)
      position: 'top-right',
    },
    margins: { top: 30, right: 40, bottom: 60, left: 80 },
  },
});

// Configure cursor separately
chart.enableCursor({
  crosshair: true,
  valueDisplayMode: 'corner',     // 'disabled' | 'floating' | 'corner'
  cornerPosition: 'top-right',
  lineStyle: 'dashed',
});
```

## Legend Configuration

### LegendOptions

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `visible` | `boolean` | `true` | Show/hide the legend |
| `position` | `LegendPositionPreset \| {x, y}` | `'top-right'` | Position preset or custom coordinates |
| `width` | `number` | `120` | Width in pixels |
| `highlightOnHover` | `boolean` | **`false`** | Change series color on legend hover |
| `bringToFrontOnHover` | `boolean` | **`true`** | Bring series to foreground on hover |
| `draggable` | `boolean` | `true` | Allow dragging the legend |
| `resizable` | `boolean` | `true` | Allow resizing the legend |

### Position Presets

```typescript
type LegendPositionPreset = 
  | 'top-left' 
  | 'top-right' 
  | 'bottom-left' 
  | 'bottom-right'
  | 'top-center'
  | 'bottom-center';
```

### Hover Behavior

By default, hovering over a series in the legend will:
- ✅ Bring the series to the foreground (z-index)
- ❌ **NOT** change the series color

To enable color highlighting:

```typescript
layout: {
  legend: {
    highlightOnHover: true, // Enable color change on hover
  },
}
```

## Cursor & Crosshair

Cursor configuration is done via `chart.enableCursor()`, not the layout options:

```typescript
chart.enableCursor({
  enabled: true,
  crosshair: true,                 // Show crosshair lines
  snap: true,                      // Snap to data points
  valueDisplayMode: 'corner',      // 'disabled' | 'floating' | 'corner'
  cornerPosition: 'top-right',     // For 'corner' mode
  lineStyle: 'dashed',             // 'solid' | 'dashed' | 'dotted'
  formatter: (x, y) => `X: ${x.toFixed(2)}, Y: ${y.toFixed(4)}`,
});
```

### Value Display Modes

| Mode | Description |
|------|-------------|
| `'floating'` | Tooltip follows cursor (default) |
| `'corner'` | Fixed position in corner of plot area |
| `'disabled'` | No values shown, crosshair lines only |

### Corner Positions

```typescript
type CornerPosition = 
  | 'top-left' 
  | 'top-right' 
  | 'bottom-left' 
  | 'bottom-right';
```

## Margins & Padding

### ChartMargins

Control space between container edges and chart area:

```typescript
layout: {
  margins: {
    top: 30,    // Space above chart
    right: 40,  // Space to the right
    bottom: 60, // Space below (for x-axis labels)
    left: 80,   // Space to the left (for y-axis labels)
  },
}
```

### PlotAreaPadding

Control space inside the plot area:

```typescript
layout: {
  plotPadding: {
    top: 10,
    right: 10,
    bottom: 10,
    left: 10,
  },
}
```

## Axis Layout

Control spacing between axis elements:

```typescript
layout: {
  xAxisLayout: {
    titleGap: 12,   // Distance between axis line and title
    labelGap: 6,    // Distance between tick labels and axis
    tickGap: 2,     // Distance between tick marks and axis
    axisPadding: 0, // Padding between axis area and plot
  },
  yAxisLayout: {
    titleGap: 10,
    labelGap: 4,
    tickGap: 2,
    axisPadding: 0,
  },
}
```

## Chart Title

```typescript
layout: {
  title: {
    text: 'My Chart Title',
    visible: true,
    fontSize: 18,
    fontWeight: 600,
    color: '#ffffff',
    position: 'top',      // 'top' | 'bottom'
    align: 'center',      // 'left' | 'center' | 'right'
    padding: { top: 12, bottom: 12 },
  },
}
```

## Toolbar Positioning

```typescript
// Using preset
layout: {
  toolbarPosition: 'top-right',
}

// Using custom position
layout: {
  toolbarPosition: {
    horizontal: 'center',
    vertical: 'top',
    offset: { x: 0, y: 10 },
  },
}
```

## Complete Example

```typescript
import { createChart } from 'scichart-engine';

const chart = createChart({
  container: document.getElementById('chart'),
  theme: 'midnight',
  xAxis: { label: 'Time (s)' },
  yAxis: { label: 'Value' },
  layout: {
    // Chart title
    title: {
      text: 'Scientific Data Analysis',
      visible: true,
      fontSize: 18,
      position: 'top',
      align: 'center',
    },
    
    // Legend configuration
    legend: {
      visible: true,
      position: 'top-right',
      highlightOnHover: false, // No color change
      bringToFrontOnHover: true, // Bring to front
      draggable: true,
    },
    
    // Toolbar position
    toolbarPosition: 'top-center',
    
    // Margins
    margins: {
      top: 40,
      right: 30,
      bottom: 60,
      left: 80,
    },
    
    // Axis layout
    xAxisLayout: { titleGap: 12, labelGap: 6 },
    yAxisLayout: { titleGap: 10, labelGap: 4 },
  },
});

// Enable cursor with corner display
chart.enableCursor({
  enabled: true,
  crosshair: true,
  valueDisplayMode: 'corner',
  cornerPosition: 'top-left',
  lineStyle: 'dashed',
});
```

## Migration from Previous API

### Legend Hover Behavior

**Before (v1.x):** Legend hover always changed series color.

**After (v1.10.4):** Legend hover does NOT change color by default, only brings to front.

To restore previous behavior:
```typescript
layout: {
  legend: {
    highlightOnHover: true,
  },
}
```

### Cursor Value Display

**Before:** Used a CrosshairPlugin or layout.crosshair options.

**After (v1.10.4):** Use native `enableCursor()` method.

```typescript
// Enable cursor with corner value display
chart.enableCursor({
  crosshair: true,
  valueDisplayMode: 'corner',
  cornerPosition: 'top-right',
});
```
