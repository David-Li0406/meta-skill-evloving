# SciChart 3D Engine

The engine includes a specialized high-performance 3D renderer for volumetric data, surfaces, and point clouds.

## Initialization
3D charts are initialized via the `createChart3D` function (requires `scichart-engine/plugins/3d`).

```typescript
import { createChart3D } from 'scichart-engine/plugins/3d';

const chart3d = createChart3D({
  container,
  xAxis: { label: 'X' },
  yAxis: { label: 'Y' },
  zAxis: { label: 'Z' }
});
```

## 3D Series Types
- `surface`: Wireframe or solid surface maps (height maps).
- `point-cloud`: Massive 3D scatter plots.
- `mesh`: Custom 3D geometries.
- `volumetric`: 3D voxel rendering (e.g., MRI/CT scans).

## Styling 3D Surfaces
Surfaces can be styled with colormaps (heatmaps) or solid materials.

```typescript
chart3d.addSeries({
  type: 'surface',
  data: {
    xValues,
    zValues,
    yValues: new Float32Array(width * height) // Height values
  },
  style: {
    drawWireframe: true,
    colorMap: 'jet' // Predefined color maps
  }
});
```

## Interaction in 3D
- **Orbit**: Left Click + Drag.
- **Pan**: Right Click + Drag.
- **Zoom**: Scroll Wheel.
- **Auto-Rotation**: `chart3d.startRotation(speed)`.

## Performance Note
3D rendering uses specialized **Point-Sprite** and **Instancing** techniques to handle millions of 3D points at 60 FPS.
