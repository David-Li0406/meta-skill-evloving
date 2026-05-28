# MapLibre GL JS Patterns

Patterns for building interactive maps with MapLibre GL JS in React applications.

## Setup

```bash
npm install maplibre-gl
```

```typescript
import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
```

## Map Initialization

### Single Instance Pattern (React)

Create the map once on mount, never recreate. Use refs for stable instance access:

```typescript
const mapContainer = useRef<HTMLDivElement>(null)
const map = useRef<maplibregl.Map | null>(null)
const [mapLoaded, setMapLoaded] = useState(false)

useEffect(() => {
  if (!mapContainer.current || map.current) return

  map.current = new maplibregl.Map({
    container: mapContainer.current,
    style: 'https://api.maptiler.com/maps/streets/style.json?key=YOUR_KEY',
    center: [-75.1652, 39.9526],
    zoom: 12,
  })

  map.current.addControl(new maplibregl.NavigationControl())

  map.current.on('load', () => {
    setMapLoaded(true)
  })

  return () => {
    map.current?.remove()
    map.current = null
  }
}, []) // Empty deps - initialize once
```

### Centralized Config

Extract constants and initialization to a config file:

```typescript
// mapConfig.ts
export const DEFAULT_CENTER: [number, number] = [-75.1652, 39.9526]
export const DEFAULT_ZOOM = 12
export const ZOOM_THRESHOLD = 13 // For scale-dependent rendering

export function initializeMap(container: HTMLElement) {
  const map = new maplibregl.Map({
    container,
    style: 'https://api.maptiler.com/maps/openstreetmap/style.json?key=YOUR_KEY',
    center: DEFAULT_CENTER,
    zoom: DEFAULT_ZOOM
  })
  map.addControl(new maplibregl.NavigationControl())
  return map
}
```

## Layer Management

### Layer Ordering

Add layers in visual order (bottom to top): base fill, hover, selection, lines, labels.

```typescript
// Add source first
map.addSource('regions', {
  type: 'geojson',
  data: geojsonData
})

// Base fill layer
map.addLayer({
  id: 'regions-fill',
  type: 'fill',
  source: 'regions',
  paint: {
    'fill-color': '#627BC1',
    'fill-opacity': 0.8
  }
})

// Hover layer (filter-based for efficiency)
map.addLayer({
  id: 'regions-hover',
  type: 'line',
  source: 'regions',
  paint: {
    'line-color': '#000000',
    'line-width': 2
  },
  filter: ['==', ['get', 'id'], ''] // Empty = hidden
})

// Selection layer
map.addLayer({
  id: 'regions-selection',
  type: 'fill',
  source: 'regions',
  paint: {
    'fill-color': '#ff474c',
    'fill-opacity': 0.6
  },
  filter: ['==', ['get', 'id'], '']
})

// Labels last (always on top)
map.addLayer({
  id: 'regions-labels',
  type: 'symbol',
  source: 'regions',
  minzoom: 13, // Only show at higher zoom
  layout: {
    'text-field': ['get', 'name'],
    'text-size': 14,
    'text-allow-overlap': true
  },
  paint: {
    'text-color': '#ffffff',
    'text-halo-color': '#000000',
    'text-halo-width': 1
  }
})
```

### Safe Layer Removal

Always check existence before removing:

```typescript
function removeLayerSafely(map: maplibregl.Map, layerId: string, sourceId: string) {
  if (map.getLayer(layerId)) {
    map.removeLayer(layerId)
  }
  if (map.getSource(sourceId)) {
    map.removeSource(sourceId)
  }
}
```

### Style Load Guard

Wait for style to load before manipulating layers:

```typescript
if (!map.isStyleLoaded()) {
  map.once('style.load', () => {
    addLayers(map)
  })
  return
}
addLayers(map)
```

## Source Management

### Dynamic GeoJSON Updates

Use `setData()` to update source data:

```typescript
function updateSourceWithCounts(map: maplibregl.Map, stats: Record<string, number>) {
  const source = map.getSource('regions') as maplibregl.GeoJSONSource
  if (!source) return

  // Get current data and update properties
  const currentData = source._data as GeoJSON.FeatureCollection
  const updatedFeatures = currentData.features.map(feature => ({
    ...feature,
    properties: {
      ...feature.properties,
      count: Number(stats[feature.properties?.id] ?? 0)
    }
  }))

  source.setData({
    type: 'FeatureCollection',
    features: updatedFeatures
  })
}
```

## Event Handling

### Click and Hover with Refs

Store callbacks in refs to avoid stale closures:

```typescript
const onFeatureClickRef = useRef(onFeatureClick)
useEffect(() => {
  onFeatureClickRef.current = onFeatureClick
}, [onFeatureClick])

// In layer setup effect:
const handleClick = (e: maplibregl.MapLayerMouseEvent) => {
  if (!e.features?.length) return
  const feature = e.features[0]
  onFeatureClickRef.current?.(feature.properties?.id, feature)
}

const handleMouseMove = (e: maplibregl.MapLayerMouseEvent) => {
  map.getCanvas().style.cursor = 'pointer'
  if (e.features?.length) {
    const id = e.features[0].properties?.id
    map.setFilter('regions-hover', ['==', ['get', 'id'], id])
  }
}

const handleMouseLeave = () => {
  map.getCanvas().style.cursor = ''
  map.setFilter('regions-hover', ['==', ['get', 'id'], ''])
}

map.on('click', 'regions-fill', handleClick)
map.on('mousemove', 'regions-fill', handleMouseMove)
map.on('mouseleave', 'regions-fill', handleMouseLeave)

// Cleanup
return () => {
  map.off('click', 'regions-fill', handleClick)
  map.off('mousemove', 'regions-fill', handleMouseMove)
  map.off('mouseleave', 'regions-fill', handleMouseLeave)
}
```

### Background Click for Deselection

```typescript
const handleMapBackgroundClick = (e: maplibregl.MapMouseEvent) => {
  const features = map.queryRenderedFeatures(e.point, {
    layers: ['regions-fill']
  })
  if (features.length === 0) {
    onFeatureClickRef.current?.(null, null) // Clear selection
  }
}

map.on('click', handleMapBackgroundClick)
```

## Popup Management

### Shared Popup Pattern

For multi-map scenarios, share a popup ref to ensure only one popup is visible:

```typescript
interface Props {
  sharedPopupRef?: React.MutableRefObject<maplibregl.Popup | null>
}

function MapComponent({ sharedPopupRef }: Props) {
  const localPopupRef = useRef<maplibregl.Popup | null>(null)
  const popupRef = sharedPopupRef || localPopupRef

  const createPopup = useCallback((
    map: maplibregl.Map,
    lngLat: [number, number],
    feature: GeoJSON.Feature
  ) => {
    // CRITICAL: Clear ref before removing old popup
    // This prevents old popup's close handler from clearing selection
    const oldPopup = popupRef.current
    popupRef.current = null
    oldPopup?.remove()

    const popup = new maplibregl.Popup({
      closeButton: true,
      closeOnClick: false, // Handle manually
    })
      .setLngLat(lngLat)
      .setHTML(buildPopupHTML(feature))
      .addTo(map)

    popupRef.current = popup

    popup.on('close', () => {
      if (popupRef.current === popup) {
        onFeatureClickRef.current?.(null, null)
        popupRef.current = null
      }
    })
  }, [])
}
```

### Popup HTML Builder

```typescript
const buildPopupHTML = (feature: GeoJSON.Feature): string => {
  const props = feature.properties
  return `
    <div class="p-2">
      <h3 class="font-semibold">${props?.name || 'Unknown'}</h3>
      <p class="text-sm">Value: ${props?.value?.toFixed(1) ?? 'N/A'}</p>
    </div>
  `
}
```

## Custom Markers

### DOM Element Marker

```typescript
function createPulsingMarker() {
  const el = document.createElement('div')
  el.style.cssText = `
    width: 50px; height: 50px;
    display: flex; align-items: center; justify-content: center;
  `

  const dot = document.createElement('div')
  dot.style.cssText = `
    width: 12px; height: 12px;
    background-color: #3388ff;
    border-radius: 50%;
  `
  el.appendChild(dot)

  // Add animated rings
  for (let i = 0; i < 3; i++) {
    const ring = document.createElement('div')
    ring.style.cssText = `
      position: absolute;
      border: 2px solid #3388ff;
      border-radius: 50%;
      animation: pulse${i + 1} 2s infinite;
    `
    el.appendChild(ring)
  }

  return el
}

const marker = new maplibregl.Marker({
  element: createPulsingMarker(),
  anchor: 'center'
})
  .setLngLat([lng, lat])
  .addTo(map)
```

### SDF Icons for Dynamic Coloring

Generate SDF images for icons that can be dynamically colored:

```bash
npx image-sdf icon.png --spread 10 --downscale 4 --color white > icon.sdf.png
```

```typescript
// Load SDF image
const image = await map.loadImage('/icon.sdf.png')
map.addImage('my-icon', image.data, { sdf: true })

// Use in layer with dynamic color
map.addLayer({
  id: 'markers',
  type: 'symbol',
  source: 'points',
  layout: {
    'icon-image': 'my-icon',
    'icon-size': 0.5,
  },
  paint: {
    'icon-color': ['get', 'color'], // Color from feature property
  }
})
```

## Data-Driven Styling

### Threshold-Based Colors

```typescript
const OTP_THRESHOLDS = { good: 83, fair: 70 }
const OTP_COLORS = { good: '#10b981', fair: '#f59e0b', poor: '#ef4444' }

const colorExpression: maplibregl.ExpressionSpecification = [
  'case',
  ['>=', ['get', 'pct_on_time'], OTP_THRESHOLDS.good], OTP_COLORS.good,
  ['>=', ['get', 'pct_on_time'], OTP_THRESHOLDS.fair], OTP_COLORS.fair,
  OTP_COLORS.poor,
]

map.addLayer({
  id: 'segments',
  type: 'line',
  source: 'data',
  paint: {
    'line-color': colorExpression,
    'line-width': 4,
  }
})
```

### Logarithmic Color Scale

For skewed data distributions:

```typescript
function getLogColorScale(minCount: number, maxCount: number) {
  const colors = ['#e5f5e0', '#c7e9c0', '#a1d99b', '#74c476', '#41ab5d', '#238b45', '#006d2c']
  const stops: [number, string][] = [[0, '#f5f5f5']] // Zero = gray

  if (minCount === maxCount) {
    stops.push([maxCount, colors[colors.length - 1]])
    return stops
  }

  const logMin = Math.log(Math.max(0.1, minCount))
  const logMax = Math.log(maxCount)
  const step = (logMax - logMin) / (colors.length - 1)

  colors.forEach((color, i) => {
    const value = Math.round(Math.exp(logMin + step * i) * 100) / 100
    stops.push([value, color])
  })

  return stops
}

// Apply to layer
map.setPaintProperty('regions-fill', 'fill-color', [
  'case',
  ['==', ['to-number', ['get', 'count']], 0], '#f5f5f5',
  ['interpolate', ['linear'], ['to-number', ['get', 'count']], ...colorStops.flat()]
])
```

### Null/Zero Value Handling

```typescript
const fillColorExpression = [
  'case',
  ['any',
    ['==', ['typeof', ['get', 'count']], 'null'],
    ['==', ['to-number', ['get', 'count']], 0]
  ],
  '#f5f5f5', // Gray for null/zero
  colorExpression
]
```

## Selection and Dimming

### Dim Non-Selected Features

```typescript
useEffect(() => {
  if (!map || !mapLoaded) return

  const opacityProp = isPointLayer ? 'circle-opacity' : 'line-opacity'

  if (selectedFeatureKey) {
    map.setPaintProperty(LAYER_ID, opacityProp, [
      'case',
      ['==', ['get', 'id'], selectedFeatureKey],
      0.8,  // Selected keeps full opacity
      0.2   // Non-selected dimmed
    ])
  } else {
    map.setPaintProperty(LAYER_ID, opacityProp, 0.8)
  }
}, [selectedFeatureKey, mapLoaded])
```

## Performance Patterns

### Debounce Frequent Operations

```typescript
function debounce<T extends (...args: any[]) => void>(fn: T, delay = 300) {
  let timeoutId: ReturnType<typeof setTimeout>
  return function (this: any, ...args: Parameters<T>) {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => fn.apply(this, args), delay)
  }
}

// Usage: debounce fitBounds calls
const debouncedFitBounds = debounce((bounds: maplibregl.LngLatBounds) => {
  map.fitBounds(bounds, { padding: 50 })
}, 300)
```

### Query Features by Coordinates

```typescript
function findFeatureAtCoordinates(map: maplibregl.Map, lngLat: maplibregl.LngLat) {
  const features = map.queryRenderedFeatures(
    map.project([lngLat.lng, lngLat.lat]),
    { layers: ['regions-fill'] }
  )
  return features[0] ?? null
}
```

## Issues & Resolutions

| Issue | Cause | Solution |
|-------|-------|----------|
| **Popup conflicts between dual maps** | Each map creates its own popup | Use a shared `popupRef` passed as prop |
| **SDF image loading errors** | Using `createImageBitmap` instead of map API | Use `map.loadImage()` and access `.data` property |
| **Map fitting jank on resize** | `fitBounds` called too frequently | Debounce fitBounds calls |
| **Stale closure in callbacks** | React callback identity changes | Store callbacks in refs, update ref in separate effect |
| **Race conditions with style** | Manipulating layers before style loads | Guard with `isStyleLoaded()` + listen for `style.load` event |
| **Layer removal errors** | Removing non-existent layers | Always check `getLayer()` before `removeLayer()` |
