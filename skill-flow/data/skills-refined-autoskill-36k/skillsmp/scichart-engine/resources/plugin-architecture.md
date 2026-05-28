# Plugin Architecture & Lifecycle

SciChart Engine is built on a modular plugin system. Every advanced feature (Tooltips, Analysis, ROI) is a plugin.

## Plugin Interface
A plugin is an object or a factory that implements the `ChartPlugin` interface.

### Lifecycle Hooks:
- `onInit(ctx, config)`: Called once when the plugin is attached. Setup listeners and UI.
- `onDataUpdate(ctx, event)`: Called when any series data changes.
- `onViewChange(ctx, event)`: Called during zoom or pan.
- `onBeforeRender(ctx, event)`: Pre-render logic. Return `false` to skip the frame.
- `onRenderWebGL(ctx, event)`: Custom WebGL drawing logic.
- `onRenderOverlay(ctx, event)`: Custom Canvas 2D drawing (ideal for UI/labels).
- `onDestroy(ctx)`: Cleanup logic.

## Plugin Context (`ctx`)
The context provides safe access to chart internals:
- `ctx.chart`: The main Chart API.
- `ctx.render`: Access to `gl` (WebGL) and `ctx2d` (Overlay).
- `ctx.coords`: Converters between pixels and data values (`dataToPixel`, `pixelToData`).
- `ctx.data`: Access to all series and annotations.
- `ctx.ui`: Helper to manage HTML elements above the chart.

## Custom Plugin Example
```typescript
import { createConfigurablePlugin } from 'scichart-engine/plugins';

const ThresholdPlugin = createConfigurablePlugin<{ value: number }>(
  { name: 'threshold-warning' },
  (config) => ({
    onRenderOverlay(ctx) {
      const { ctx2d, plotArea } = ctx.render;
      const y = ctx.coords.yDataToPixel(config.value);

      if (y >= plotArea.y && y <= plotArea.y + plotArea.height) {
        ctx2d.strokeStyle = 'red';
        ctx2d.beginPath();
        ctx2d.moveTo(plotArea.x, y);
        ctx2d.lineTo(plotArea.x + plotArea.width, y);
        ctx2d.stroke();
      }
    }
  })
);

chart.use(ThresholdPlugin({ value: 85 }));
```
