# Professional Selection & Anomalies

## Region of Interest (ROI) Selection
The `PluginROI` provides advanced interactive selection tools (Lasso, Polygon, Rectangle) for scientific data analysis.

```typescript
import { PluginROI } from 'scichart-engine/plugins/roi';

await chart.use(PluginROI({
  defaultTool: 'lasso', // 'rectangle', 'polygon', 'lasso', 'circle'
  mask: true            // Automatically identify points within the region
}));

chart.on('roi:selected', (event) => {
  console.log('Points inside region:', event.masks);
  // event.masks is a map of seriesId -> array of point indices
});
```

## Anomaly Detection
The `PluginAnomalyDetection` uses statistical and ML algorithms to find outliers in real-time or batch mode.

### Available Algorithms:
- `zscore`: Standard deviation based (fast, assumes normal distribution).
- `mad`: Median Absolute Deviation (robust to existing outliers).
- `iqr`: Interquartile Range (distribution-free, classic box plot method).
- `isolation-forest`: ML-based random partitioning (best for complex patterns).

```typescript
import { PluginAnomalyDetection } from 'scichart-engine/plugins/anomaly-detection';

chart.use(PluginAnomalyDetection({
  method: 'mad',
  sensitivity: 3.5,
  realtime: true,
  highlight: true // Draw red markers on anomalies
}));

chart.on('anomaly:detected', (result) => {
  console.log(`Found ${result.anomalies.length} outliers in ${result.seriesId}`);
});
```

## Data Transformation Pipeline
The `PluginDataTransform` allows chaining mathematical operations on data series without modifying the original source.

```typescript
import { PluginDataTransform } from 'scichart-engine/plugins/data-transform';

chart.use(PluginDataTransform());

// Chain: Normalize -> Moving Average -> Derivative
chart.processing.transform('sensor-1', [
  { type: 'normalize', parameters: { range: [0, 1] } },
  { type: 'moving-average', parameters: { window: 10 } },
  { type: 'derivative', parameters: { order: 1 } }
]);
```
