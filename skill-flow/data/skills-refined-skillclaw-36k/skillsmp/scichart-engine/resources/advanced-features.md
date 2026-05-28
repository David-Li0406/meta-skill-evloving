# Advanced SciChart Engine Features

## Multi-Axis Support
The engine allows multiple X and Y axes, which is essential for comparing datasets with different scales.

```typescript
// Add secondary Y axis
chart.addYAxis({
  id: 'temperature-axis',
  label: 'Temp (°C)',
  auto: true
});

// Map a series to the secondary axis
chart.addSeries({
  id: 'temp-data',
  yAxisId: 'temperature-axis',
  data: { x, y }
});
```

## Chart Synchronization (`scichart-sync`)
Synchronize zooming and panning across multiple chart instances.

```typescript
import { PluginSync } from 'scichart-engine/plugins/sync';

const syncGroup = 'experiment-1';
chart1.use(PluginSync({ group: syncGroup }));
chart2.use(PluginSync({ group: syncGroup }));
```

## Professional Annotations
Add context to your scientific data with drawing primitives.

- `text`: Scientific labels or notes.
- `horizontal-line` / `vertical-line`: Thresholds or markers.
- `rectangle` / `band`: Highlight specific regions (e.g., ROI).
- `arrow`: Point out anomalies or specific peaks.

```typescript
chart.addAnnotation({
  type: 'rectangle',
  x: [10, 20],
  y: [0, 5],
  style: { fill: 'rgba(255, 0, 0, 0.1)', stroke: 'red' }
});
```

## Virtualization & Massive Data
For datasets exceeding 10M points, use `PluginVirtualization`. It dynamically manages memory and Level-of-Detail (LoD) to maintain 60 FPS.

```typescript
import { PluginVirtualization } from 'scichart-engine/plugins/virtualization';

chart.use(PluginVirtualization({
  cacheSize: '2GB',
  preloadDistance: 0.5 // Preload 50% more data outside view
}));
```

## Video Recording
Record high-resolution videos of your animated charts or real-time experiments.

```typescript
import { PluginVideoRecorder } from 'scichart-engine/plugins/video-recorder';

chart.use(PluginVideoRecorder());
chart.videoRecorder.start({ fps: 60, quality: 1.0 });
// ... after some time
const blob = await chart.videoRecorder.stop();
```
