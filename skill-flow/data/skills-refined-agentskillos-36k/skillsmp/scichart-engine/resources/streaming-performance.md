# Streaming & Performance Optimization

## Backpressure Management
When dealing with ultra-high-speed data (e.g., 100kHz sensors), the `BackpressureManager` ensures the UI remains responsive by dropping or sampling points if the buffer overflows.

### Strategies:
- `drop-oldest`: Keeps only the most recent data (default).
- `drop-newest`: Ignores incoming data if the buffer is full.
- `sample`: Keeps every Nth point (adaptive downsampling).
- `pause`: Pauses processing until the buffer drains.

```typescript
import { createBackpressureManager } from 'scichart-engine';

const bp = createBackpressureManager(50000, 'drop-oldest');

// Push high-speed data
websocket.onmessage = (data) => bp.push('sensor-1', data.points);

// Consume in render loop (60 FPS)
setInterval(() => {
  const points = bp.consume('sensor-1', 1000);
  chart.appendData('series-1', points);
}, 16);
```

## Circular Buffers
Use `CircularBuffer` for high-performance memory management without frequent GC sweeps.

```typescript
import { CircularBuffer } from 'scichart-engine';

const buffer = new CircularBuffer(1000); // Fixed size
buffer.pushOverwrite(newPoint); // Efficient O(1) push or overwrite
```

## Offscreen Rendering
The `PluginOffscreen` allows the entire chart rendering to happen in a Web Worker, preventing the main thread from locking up during complex visual updates.

```typescript
import { PluginOffscreen } from 'scichart-engine/plugins/offscreen';

chart.use(PluginOffscreen({
  workerUrl: '/workers/chart-worker.js'
}));
```

## Virtualization
For datasets exceeding 10M points, `PluginVirtualization` uses a dynamic Level-of-Detail (LoD) system to only load and render data visible in the current viewport.
