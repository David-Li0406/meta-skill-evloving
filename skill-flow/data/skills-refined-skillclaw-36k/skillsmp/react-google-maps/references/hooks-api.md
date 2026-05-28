# Hooks API Reference

## useMap

Access the `google.maps.Map` instance.

```tsx
import { useMap } from '@vis.gl/react-google-maps';

function MapControls() {
  const map = useMap();

  useEffect(() => {
    if (!map) return;
    
    // Access all google.maps.Map methods
    map.panTo({ lat: 40.7128, lng: -74.006 });
    map.setZoom(15);
    map.fitBounds(bounds);
  }, [map]);

  return <button onClick={() => map?.panTo(center)}>Center Map</button>;
}
```

### With Multiple Maps

```tsx
// Give maps explicit IDs
<Map id="main-map" {...props} />
<Map id="mini-map" {...props} />

// Access specific map
const mainMap = useMap('main-map');
const miniMap = useMap('mini-map');
```

### Common Map Methods

```tsx
const map = useMap();

// Viewport control
map.panTo(latLng);
map.setCenter(latLng);
map.setZoom(level);
map.fitBounds(bounds, padding?);
map.panToBounds(bounds);

// Get current state
map.getCenter();
map.getZoom();
map.getBounds();

// Other
map.setMapTypeId('satellite');
map.setOptions({ gestureHandling: 'none' });
```

---

## useMapsLibrary

Dynamically load Google Maps libraries. Returns the library object or `null` while loading.

```tsx
import { useMapsLibrary } from '@vis.gl/react-google-maps';

function GeocodingComponent() {
  const geocodingLib = useMapsLibrary('geocoding');
  const [geocoder, setGeocoder] = useState<google.maps.Geocoder | null>(null);

  useEffect(() => {
    if (!geocodingLib) return;
    setGeocoder(new geocodingLib.Geocoder());
  }, [geocodingLib]);

  // Use geocoder...
}
```

### Available Libraries

| Library | Use Case | Key Classes |
|---------|----------|-------------|
| `'places'` | Places search, autocomplete | `AutocompleteService`, `PlacesService` |
| `'geocoding'` | Address ↔ coordinates | `Geocoder` |
| `'drawing'` | Drawing tools | `DrawingManager` |
| `'geometry'` | Distance, area calculations | `spherical`, `poly`, `encoding` |
| `'visualization'` | Heatmaps | `HeatmapLayer` |
| `'marker'` | Marker utilities | `PinElement` |
| `'routes'` | Directions | `DirectionsService`, `DirectionsRenderer` |
| `'maps3d'` | 3D maps | `Map3DElement` |

### Example: Geocoding

```tsx
function useGeocoder() {
  const geocodingLib = useMapsLibrary('geocoding');
  
  const geocode = useCallback(async (address: string) => {
    if (!geocodingLib) return null;
    
    const geocoder = new geocodingLib.Geocoder();
    const response = await geocoder.geocode({ address });
    
    if (response.results.length > 0) {
      const { lat, lng } = response.results[0].geometry.location;
      return { lat: lat(), lng: lng() };
    }
    return null;
  }, [geocodingLib]);

  return { geocode, isReady: !!geocodingLib };
}
```

### Example: Directions

```tsx
function useDirections() {
  const routesLib = useMapsLibrary('routes');
  const map = useMap();
  const [renderer, setRenderer] = useState<google.maps.DirectionsRenderer | null>(null);

  useEffect(() => {
    if (!routesLib || !map) return;
    
    const directionsRenderer = new routesLib.DirectionsRenderer({ map });
    setRenderer(directionsRenderer);
    
    return () => directionsRenderer.setMap(null);
  }, [routesLib, map]);

  const getRoute = useCallback(async (origin: string, destination: string) => {
    if (!routesLib || !renderer) return;
    
    const service = new routesLib.DirectionsService();
    const result = await service.route({
      origin,
      destination,
      travelMode: google.maps.TravelMode.DRIVING,
    });
    
    renderer.setDirections(result);
  }, [routesLib, renderer]);

  return { getRoute, isReady: !!renderer };
}
```

---

## useAdvancedMarkerRef

Connect an AdvancedMarker to an InfoWindow.

```tsx
import { useAdvancedMarkerRef } from '@vis.gl/react-google-maps';

function MarkerWithInfoWindow({ position }: { position: google.maps.LatLngLiteral }) {
  const [markerRef, marker] = useAdvancedMarkerRef();
  const [infoOpen, setInfoOpen] = useState(false);

  return (
    <>
      <AdvancedMarker
        ref={markerRef}
        position={position}
        onClick={() => setInfoOpen(true)}
      />
      
      {infoOpen && (
        <InfoWindow anchor={marker} onClose={() => setInfoOpen(false)}>
          <div>Info content</div>
        </InfoWindow>
      )}
    </>
  );
}
```

### Return Value

```tsx
const [markerRef, marker] = useAdvancedMarkerRef();
// markerRef: RefCallback to pass to AdvancedMarker's ref prop
// marker: The AdvancedMarkerElement instance (or null)
```

---

## useMarkerRef

Same as `useAdvancedMarkerRef` but for the legacy `Marker` component.

```tsx
const [markerRef, marker] = useMarkerRef();

<Marker ref={markerRef} position={position} />
```

---

## useApiIsLoaded

Check if the Maps JavaScript API has finished loading.

```tsx
import { useApiIsLoaded } from '@vis.gl/react-google-maps';

function MapComponent() {
  const isLoaded = useApiIsLoaded();

  if (!isLoaded) {
    return <div>Loading map...</div>;
  }

  return <Map {...props} />;
}
```

---

## useApiLoadingStatus

Get detailed loading status.

```tsx
import { useApiLoadingStatus, APILoadingStatus } from '@vis.gl/react-google-maps';

function MapComponent() {
  const status = useApiLoadingStatus();

  switch (status) {
    case APILoadingStatus.NOT_LOADED:
      return <div>Not started</div>;
    case APILoadingStatus.LOADING:
      return <div>Loading...</div>;
    case APILoadingStatus.LOADED:
      return <Map {...props} />;
    case APILoadingStatus.FAILED:
      return <div>Failed to load</div>;
  }
}
```

---

## Custom Hook Patterns

### useMapBounds

```tsx
function useMapBounds() {
  const map = useMap();
  const [bounds, setBounds] = useState<google.maps.LatLngBounds | null>(null);

  useEffect(() => {
    if (!map) return;
    
    const listener = map.addListener('bounds_changed', () => {
      setBounds(map.getBounds() ?? null);
    });
    
    return () => listener.remove();
  }, [map]);

  return bounds;
}
```

### useFitBounds

```tsx
function useFitBounds(positions: google.maps.LatLngLiteral[]) {
  const map = useMap();

  useEffect(() => {
    if (!map || positions.length === 0) return;

    const bounds = new google.maps.LatLngBounds();
    positions.forEach((pos) => bounds.extend(pos));
    map.fitBounds(bounds, { padding: 50 });
  }, [map, positions]);
}
```

### useMapClick

```tsx
function useMapClick(callback: (latLng: google.maps.LatLng) => void) {
  const map = useMap();

  useEffect(() => {
    if (!map) return;
    
    const listener = map.addListener('click', (e: google.maps.MapMouseEvent) => {
      if (e.latLng) callback(e.latLng);
    });
    
    return () => listener.remove();
  }, [map, callback]);
}
```
