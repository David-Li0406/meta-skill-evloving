# Components API Reference

## APIProvider

Loads the Google Maps JavaScript API. Must wrap all map components.

```tsx
<APIProvider
  apiKey="YOUR_API_KEY"
  libraries={['places', 'geocoding']} // Optional: preload libraries
  version="weekly"                     // Optional: API version
  region="PR"                          // Optional: region bias
>
  {children}
</APIProvider>
```

**Props:**
- `apiKey` (required): Google Maps API key
- `libraries`: Array of libraries to preload (`'places'`, `'geocoding'`, `'drawing'`, `'geometry'`, `'visualization'`)
- `version`: API version (`'weekly'`, `'quarterly'`, `'beta'`)
- `region`: Region code for localized behavior
- `language`: Language code

---

## Map

The map container component.

```tsx
<Map
  style={{ width: '100%', height: '400px' }}
  defaultCenter={{ lat: 40.7128, lng: -74.006 }}
  defaultZoom={12}
  mapId="YOUR_MAP_ID"
  gestureHandling="greedy"
  disableDefaultUI={false}
  onClick={(e) => console.log(e.detail.latLng)}
  onCameraChanged={(e) => console.log(e.detail)}
>
  {/* Markers, InfoWindows, etc. */}
</Map>
```

### Controlled vs Uncontrolled

**Uncontrolled (default):** Use `defaultCenter`, `defaultZoom` - map manages its own state after init.

**Controlled:** Use `center`, `zoom` - React controls the viewport, map always syncs to props.

```tsx
// Uncontrolled - user can freely pan/zoom
<Map defaultCenter={center} defaultZoom={10} />

// Controlled - viewport locked to React state
const [camera, setCamera] = useState({ center, zoom: 10 });
<Map
  center={camera.center}
  zoom={camera.zoom}
  onCameraChanged={(e) => setCamera(e.detail)}
/>
```

### Key Props

| Prop | Type | Description |
|------|------|-------------|
| `mapId` | string | Required for AdvancedMarker, enables cloud styling |
| `defaultCenter` / `center` | LatLngLiteral | Initial/controlled center |
| `defaultZoom` / `zoom` | number | Initial/controlled zoom (0-22) |
| `gestureHandling` | `'cooperative'` \| `'greedy'` \| `'none'` \| `'auto'` | How map handles gestures |
| `disableDefaultUI` | boolean | Hide all default controls |
| `mapTypeId` | `'roadmap'` \| `'satellite'` \| `'hybrid'` \| `'terrain'` | Map type |
| `clickableIcons` | boolean | Whether POI icons are clickable |
| `style` / `className` | CSSProperties / string | Container styling |

### Events

| Event | Type | Description |
|-------|------|-------------|
| `onClick` | `(e: MapMouseEvent) => void` | Map clicked |
| `onDblClick` | `(e: MapMouseEvent) => void` | Map double-clicked |
| `onContextMenu` | `(e: MapMouseEvent) => void` | Right-click |
| `onCameraChanged` | `(e: CameraChangedEvent) => void` | Camera changed |
| `onBoundsChanged` | `() => void` | Bounds changed |
| `onIdle` | `() => void` | Map idle after pan/zoom |

---

## AdvancedMarker

Modern marker component. **Requires `mapId` on the Map component.**

```tsx
<AdvancedMarker
  position={{ lat: 40.7128, lng: -74.006 }}
  title="New York"
  draggable
  onClick={(e) => console.log('clicked')}
  onDrag={(e) => console.log(e.latLng)}
  onDragEnd={(e) => console.log('final position:', e.latLng)}
>
  {/* Optional: custom content instead of default pin */}
  <Pin background="#FF0000" />
</AdvancedMarker>
```

### Custom HTML Marker

```tsx
<AdvancedMarker position={position}>
  <div className="custom-marker">
    <img src="/marker-icon.png" alt="marker" />
    <span>Label</span>
  </div>
</AdvancedMarker>
```

### Props

| Prop | Type | Description |
|------|------|-------------|
| `position` | LatLngLiteral \| LatLngAltitudeLiteral | Marker position |
| `title` | string | Accessibility title |
| `draggable` | boolean | Enable dragging |
| `clickable` | boolean | Enable click events |
| `zIndex` | number | Stacking order |
| `collisionBehavior` | CollisionBehavior | Collision handling |
| `className` / `style` | string / CSSProperties | Content element styling |

### Events

| Event | Type | Description |
|-------|------|-------------|
| `onClick` | `(e: AdvancedMarkerClickEvent) => void` | Marker clicked |
| `onDragStart` | `(e: MapMouseEvent) => void` | Drag started |
| `onDrag` | `(e: MapMouseEvent) => void` | **During drag** (for real-time updates) |
| `onDragEnd` | `(e: MapMouseEvent) => void` | Drag ended |
| `onMouseEnter` | `(e: MouseEvent) => void` | Mouse entered |
| `onMouseLeave` | `(e: MouseEvent) => void` | Mouse left |

### Anchor Point

Control which part of the marker aligns with the position:

```tsx
import { AdvancedMarkerAnchorPoint } from '@vis.gl/react-google-maps';

<AdvancedMarker
  position={position}
  anchorPoint={AdvancedMarkerAnchorPoint.CENTER} // or TOP_LEFT, BOTTOM_CENTER, etc.
>
  <CustomContent />
</AdvancedMarker>
```

---

## Pin

Customizable pin for AdvancedMarker.

```tsx
<AdvancedMarker position={position}>
  <Pin
    background="#0f9d58"
    borderColor="#006425"
    glyphColor="#60d98f"
    glyph="A"           // Text or element
    scale={1.2}         // Size multiplier
  />
</AdvancedMarker>
```

### Props

| Prop | Type | Description |
|------|------|-------------|
| `background` | string | Pin background color |
| `borderColor` | string | Pin border color |
| `glyphColor` | string | Glyph (icon/text) color |
| `glyph` | string \| Element | Content inside pin |
| `scale` | number | Size multiplier |

---

## InfoWindow

Popup window attached to a marker or position.

```tsx
const [markerRef, marker] = useAdvancedMarkerRef();
const [open, setOpen] = useState(false);

<AdvancedMarker ref={markerRef} position={position} onClick={() => setOpen(true)} />

{open && (
  <InfoWindow
    anchor={marker}
    onClose={() => setOpen(false)}
    headerContent={<h3>Title</h3>}
  >
    <p>Window content</p>
  </InfoWindow>
)}
```

### Props

| Prop | Type | Description |
|------|------|-------------|
| `anchor` | AdvancedMarkerElement \| Marker | Anchor to marker |
| `position` | LatLngLiteral | Position if no anchor |
| `onClose` | `() => void` | Close callback (required for sync) |
| `onCloseClick` | `() => void` | Close button clicked |
| `headerContent` | ReactNode | Header content |
| `headerDisabled` | boolean | Hide header |
| `minWidth` / `maxWidth` | number | Width constraints |
| `disableAutoPan` | boolean | Don't pan map to show window |
| `pixelOffset` | [number, number] | Offset from anchor |

**Important:** Always provide `onClose` to keep React state in sync when the map closes the InfoWindow.

---

## MapControl

Add custom UI elements to the map.

```tsx
import { ControlPosition } from '@vis.gl/react-google-maps';

<Map {...props}>
  <MapControl position={ControlPosition.TOP_LEFT}>
    <button className="map-button">My Control</button>
  </MapControl>
  
  <MapControl position={ControlPosition.BOTTOM_CENTER}>
    <div className="legend">Legend content</div>
  </MapControl>
</Map>
```

### ControlPosition Values

```
TOP_LEFT      TOP_CENTER      TOP_RIGHT
LEFT_TOP                      RIGHT_TOP
LEFT_CENTER                   RIGHT_CENTER
LEFT_BOTTOM                   RIGHT_BOTTOM
BOTTOM_LEFT   BOTTOM_CENTER   BOTTOM_RIGHT
```

---

## Marker (Deprecated)

Legacy marker. Use AdvancedMarker for new projects.

```tsx
import { useMarkerRef } from '@vis.gl/react-google-maps';

const [markerRef, marker] = useMarkerRef();

<Marker
  ref={markerRef}
  position={position}
  icon="/custom-icon.png"
  label="A"
/>
```
