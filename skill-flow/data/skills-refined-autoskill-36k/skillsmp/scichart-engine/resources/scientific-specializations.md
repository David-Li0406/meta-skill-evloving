# Scientific Specializations

## Cyclic Voltammetry (Electrochemistry)
The engine is optimized for electrochemical techniques where X-axis stability is critical.

### Stable X-Axis Pattern
When streaming data where the X-range is fixed (like potential sweeps), use `autoScaleYOnly` or a stable X-axis configuration to prevent visual jitter.

```typescript
// During real-time acquisition
chart.updateSeries('cv', {
  x: [newPotential],
  y: [newCurrent],
  append: true,
  streaming: true // Hints the engine to keep X-axis stable
});
```

### Direction Indicators
The `DirectionIndicatorPlugin` tracks the movement of recent data points and renders a smooth arrow showing the trend.

```typescript
import { DirectionIndicatorPlugin } from 'scichart-engine/plugins';

chart.use(DirectionIndicatorPlugin({
  seriesId: 'live-data',
  color: '#FF9800',
  size: 25
}));
```

## Broken Axes (Data Gaps)
The `PluginBrokenAxis` allows "skipping" regions with no data, effectively bringing distant clusters together.

```typescript
import { PluginBrokenAxis } from 'scichart-engine/plugins/broken-axis';

chart.use(PluginBrokenAxis({
  axes: {
    default: {
      breaks: [
        { start: 100, end: 500, symbol: 'diagonal' }
      ]
    }
  }
}));
```

## SI & Scientific Formatting
Scientific data often requires specific formatting (e.g., `1.5 MHz` or `1.23e-6`). The engine's localization system handles this natively.

```typescript
import { createLocaleFormatter } from 'scichart-engine';

const formatter = createLocaleFormatter('en-US');
formatter.formatWithPrefix(1500000, 'Hz'); // "1.5 MHz"
formatter.formatScientific(0.00000123);    // "1.23e-6"
```
