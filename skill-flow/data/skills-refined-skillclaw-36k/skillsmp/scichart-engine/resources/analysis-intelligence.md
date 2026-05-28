# Analysis Intelligence & Prediction

## Technical Pattern Recognition
The `PluginPatternRecognition` identifies geometric and technical patterns in time-series and financial data.

### Supported Patterns:
- **Reversal**: `head-shoulders`, `double-top`, `double-bottom`.
- **Continuation**: `flag`, `pennant`, `rectangle`.
- **Consolidation**: `ascending-triangle`, `descending-triangle`.
- **Exhaustion**: `rising-wedge`, `falling-wedge`.

```typescript
import { PluginPatternRecognition } from 'scichart-engine/plugins/pattern-recognition';

chart.use(PluginPatternRecognition({
  defaultParameters: { minConfidence: 0.8 },
  enableRealtime: true
}));

chart.on('pattern:detected', ({ match }) => {
  console.log(`Detected ${match.pattern.name} (Confidence: ${match.confidence})`);
});
```

## Time-Series Forecasting
The `PluginForecasting` adds predictive capabilities using statistical models.

### Methods:
- `sma`: Simple Moving Average (Baseline).
- `linear`: Projection based on Least Squares.
- `holt`: Double Exponential Smoothing (Trend).
- `holtWinters`: Triple Exponential Smoothing (Trend + Seasonality).

```typescript
import { PluginForecasting } from 'scichart-engine/plugins/forecasting';

chart.use(PluginForecasting());

const result = await chart.forecasting.forecastSeries('sensor-1', {
  method: 'holtWinters',
  horizon: 50, // Predict next 50 points
  params: { period: 24 } // 24-point seasonal cycle
});

chart.forecasting.visualize(result);
```

## Interactive Drag & Drop Editing
The `PluginDragEdit` allows users to manually adjust data points on the chart.

```typescript
import { PluginDragEdit } from 'scichart-engine/plugins/drag-edit';

chart.use(PluginDragEdit({
  constraint: 'y', // Only allow vertical dragging
  snapToGrid: true,
  onDragEnd: (e) => console.log('Point moved:', e.index, e.y)
}));
```
