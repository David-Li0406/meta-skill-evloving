# Geometry Components (Circle, Polygon, Polyline)

**Important:** These components are NOT exported by `@vis.gl/react-google-maps`. Copy the implementations below into your project.

## Circle Component

```tsx
// components/circle.tsx
import { forwardRef, useContext, useEffect, useImperativeHandle, useRef } from 'react';
import { GoogleMapsContext } from '@vis.gl/react-google-maps';
import type { Ref } from 'react';

type CircleEventProps = {
  onClick?: (e: google.maps.MapMouseEvent) => void;
  onDrag?: (e: google.maps.MapMouseEvent) => void;
  onDragStart?: (e: google.maps.MapMouseEvent) => void;
  onDragEnd?: (e: google.maps.MapMouseEvent) => void;
  onMouseOver?: (e: google.maps.MapMouseEvent) => void;
  onMouseOut?: (e: google.maps.MapMouseEvent) => void;
  onRadiusChanged?: (radius: number) => void;
  onCenterChanged?: (center: google.maps.LatLng) => void;
};

export type CircleProps = google.maps.CircleOptions & CircleEventProps;
export type CircleRef = Ref<google.maps.Circle | null>;

function useCircle(props: CircleProps) {
  const {
    onClick,
    onDrag,
    onDragStart,
    onDragEnd,
    onMouseOver,
    onMouseOut,
    onRadiusChanged,
    onCenterChanged,
    center,
    radius,
    ...circleOptions
  } = props;

  const circleRef = useRef<google.maps.Circle | null>(null);
  const map = useContext(GoogleMapsContext)?.map;

  // Create circle instance
  useEffect(() => {
    if (!map) return;

    const circle = new google.maps.Circle();
    circle.setMap(map);
    circleRef.current = circle;

    return () => {
      circle.setMap(null);
      circleRef.current = null;
    };
  }, [map]);

  // Update options
  useEffect(() => {
    if (!circleRef.current) return;
    circleRef.current.setOptions(circleOptions);
  }, [circleOptions]);

  // Update center
  useEffect(() => {
    if (!circleRef.current || !center) return;
    circleRef.current.setCenter(center);
  }, [center]);

  // Update radius
  useEffect(() => {
    if (!circleRef.current || radius === undefined) return;
    circleRef.current.setRadius(radius);
  }, [radius]);

  // Event listeners
  useEffect(() => {
    if (!circleRef.current) return;
    const circle = circleRef.current;
    const listeners: google.maps.MapsEventListener[] = [];

    if (onClick) listeners.push(circle.addListener('click', onClick));
    if (onDrag) listeners.push(circle.addListener('drag', onDrag));
    if (onDragStart) listeners.push(circle.addListener('dragstart', onDragStart));
    if (onDragEnd) listeners.push(circle.addListener('dragend', onDragEnd));
    if (onMouseOver) listeners.push(circle.addListener('mouseover', onMouseOver));
    if (onMouseOut) listeners.push(circle.addListener('mouseout', onMouseOut));
    if (onRadiusChanged) {
      listeners.push(circle.addListener('radius_changed', () => {
        onRadiusChanged(circle.getRadius() ?? 0);
      }));
    }
    if (onCenterChanged) {
      listeners.push(circle.addListener('center_changed', () => {
        const c = circle.getCenter();
        if (c) onCenterChanged(c);
      }));
    }

    return () => listeners.forEach((l) => l.remove());
  }, [onClick, onDrag, onDragStart, onDragEnd, onMouseOver, onMouseOut, onRadiusChanged, onCenterChanged]);

  return circleRef;
}

export const Circle = forwardRef<google.maps.Circle | null, CircleProps>((props, ref) => {
  const circleRef = useCircle(props);
  useImperativeHandle(ref, () => circleRef.current, []);
  return null;
});

Circle.displayName = 'Circle';
```

### Circle Usage

```tsx
import { Circle } from '@/components/circle';

<Circle
  center={{ lat: 40.7128, lng: -74.006 }}
  radius={1000} // meters
  strokeColor="#FF0000"
  strokeOpacity={0.8}
  strokeWeight={2}
  fillColor="#FF0000"
  fillOpacity={0.35}
  draggable={false}
  editable={false}
  onClick={(e) => console.log('Clicked', e.latLng)}
/>
```

---

## Polygon Component

```tsx
// components/polygon.tsx
import { forwardRef, useContext, useEffect, useImperativeHandle, useRef } from 'react';
import { GoogleMapsContext, useMapsLibrary } from '@vis.gl/react-google-maps';
import type { Ref } from 'react';

type PolygonEventProps = {
  onClick?: (e: google.maps.MapMouseEvent) => void;
  onDrag?: (e: google.maps.MapMouseEvent) => void;
  onDragStart?: (e: google.maps.MapMouseEvent) => void;
  onDragEnd?: (e: google.maps.MapMouseEvent) => void;
  onMouseOver?: (e: google.maps.MapMouseEvent) => void;
  onMouseOut?: (e: google.maps.MapMouseEvent) => void;
};

type PolygonCustomProps = {
  encodedPaths?: string[]; // Encoded polyline paths
};

export type PolygonProps = google.maps.PolygonOptions & PolygonEventProps & PolygonCustomProps;
export type PolygonRef = Ref<google.maps.Polygon | null>;

function usePolygon(props: PolygonProps) {
  const {
    onClick,
    onDrag,
    onDragStart,
    onDragEnd,
    onMouseOver,
    onMouseOut,
    encodedPaths,
    paths,
    ...polygonOptions
  } = props;

  const polygonRef = useRef<google.maps.Polygon | null>(null);
  const map = useContext(GoogleMapsContext)?.map;
  const geometryLib = useMapsLibrary('geometry');

  // Create polygon instance
  useEffect(() => {
    if (!map) return;

    const polygon = new google.maps.Polygon();
    polygon.setMap(map);
    polygonRef.current = polygon;

    return () => {
      polygon.setMap(null);
      polygonRef.current = null;
    };
  }, [map]);

  // Update options
  useEffect(() => {
    if (!polygonRef.current) return;
    polygonRef.current.setOptions(polygonOptions);
  }, [polygonOptions]);

  // Update paths
  useEffect(() => {
    if (!polygonRef.current) return;
    
    if (encodedPaths && geometryLib) {
      const decodedPaths = encodedPaths.map((p) => 
        geometryLib.encoding.decodePath(p)
      );
      polygonRef.current.setPaths(decodedPaths);
    } else if (paths) {
      polygonRef.current.setPaths(paths);
    }
  }, [paths, encodedPaths, geometryLib]);

  // Event listeners
  useEffect(() => {
    if (!polygonRef.current) return;
    const polygon = polygonRef.current;
    const listeners: google.maps.MapsEventListener[] = [];

    if (onClick) listeners.push(polygon.addListener('click', onClick));
    if (onDrag) listeners.push(polygon.addListener('drag', onDrag));
    if (onDragStart) listeners.push(polygon.addListener('dragstart', onDragStart));
    if (onDragEnd) listeners.push(polygon.addListener('dragend', onDragEnd));
    if (onMouseOver) listeners.push(polygon.addListener('mouseover', onMouseOver));
    if (onMouseOut) listeners.push(polygon.addListener('mouseout', onMouseOut));

    return () => listeners.forEach((l) => l.remove());
  }, [onClick, onDrag, onDragStart, onDragEnd, onMouseOver, onMouseOut]);

  return polygonRef;
}

export const Polygon = forwardRef<google.maps.Polygon | null, PolygonProps>((props, ref) => {
  const polygonRef = usePolygon(props);
  useImperativeHandle(ref, () => polygonRef.current, []);
  return null;
});

Polygon.displayName = 'Polygon';
```

### Polygon Usage

```tsx
import { Polygon } from '@/components/polygon';

const trianglePaths = [
  { lat: 25.774, lng: -80.19 },
  { lat: 18.466, lng: -66.118 },
  { lat: 32.321, lng: -64.757 },
];

<Polygon
  paths={trianglePaths}
  strokeColor="#FF0000"
  strokeOpacity={0.8}
  strokeWeight={2}
  fillColor="#FF0000"
  fillOpacity={0.35}
  editable={true}
  draggable={true}
  onDrag={(e) => console.log('Dragging polygon')}
/>
```

---

## Polyline Component

```tsx
// components/polyline.tsx
import { forwardRef, useContext, useEffect, useImperativeHandle, useRef } from 'react';
import { GoogleMapsContext, useMapsLibrary } from '@vis.gl/react-google-maps';
import type { Ref } from 'react';

type PolylineEventProps = {
  onClick?: (e: google.maps.MapMouseEvent) => void;
  onDrag?: (e: google.maps.MapMouseEvent) => void;
  onDragStart?: (e: google.maps.MapMouseEvent) => void;
  onDragEnd?: (e: google.maps.MapMouseEvent) => void;
  onMouseOver?: (e: google.maps.MapMouseEvent) => void;
  onMouseOut?: (e: google.maps.MapMouseEvent) => void;
};

type PolylineCustomProps = {
  encodedPath?: string; // Encoded polyline path
};

export type PolylineProps = google.maps.PolylineOptions & PolylineEventProps & PolylineCustomProps;
export type PolylineRef = Ref<google.maps.Polyline | null>;

function usePolyline(props: PolylineProps) {
  const {
    onClick,
    onDrag,
    onDragStart,
    onDragEnd,
    onMouseOver,
    onMouseOut,
    encodedPath,
    path,
    ...polylineOptions
  } = props;

  const polylineRef = useRef<google.maps.Polyline | null>(null);
  const map = useContext(GoogleMapsContext)?.map;
  const geometryLib = useMapsLibrary('geometry');

  // Create polyline instance
  useEffect(() => {
    if (!map) return;

    const polyline = new google.maps.Polyline();
    polyline.setMap(map);
    polylineRef.current = polyline;

    return () => {
      polyline.setMap(null);
      polylineRef.current = null;
    };
  }, [map]);

  // Update options
  useEffect(() => {
    if (!polylineRef.current) return;
    polylineRef.current.setOptions(polylineOptions);
  }, [polylineOptions]);

  // Update path
  useEffect(() => {
    if (!polylineRef.current) return;
    
    if (encodedPath && geometryLib) {
      const decodedPath = geometryLib.encoding.decodePath(encodedPath);
      polylineRef.current.setPath(decodedPath);
    } else if (path) {
      polylineRef.current.setPath(path);
    }
  }, [path, encodedPath, geometryLib]);

  // Event listeners
  useEffect(() => {
    if (!polylineRef.current) return;
    const polyline = polylineRef.current;
    const listeners: google.maps.MapsEventListener[] = [];

    if (onClick) listeners.push(polyline.addListener('click', onClick));
    if (onDrag) listeners.push(polyline.addListener('drag', onDrag));
    if (onDragStart) listeners.push(polyline.addListener('dragstart', onDragStart));
    if (onDragEnd) listeners.push(polyline.addListener('dragend', onDragEnd));
    if (onMouseOver) listeners.push(polyline.addListener('mouseover', onMouseOver));
    if (onMouseOut) listeners.push(polyline.addListener('mouseout', onMouseOut));

    return () => listeners.forEach((l) => l.remove());
  }, [onClick, onDrag, onDragStart, onDragEnd, onMouseOver, onMouseOut]);

  return polylineRef;
}

export const Polyline = forwardRef<google.maps.Polyline | null, PolylineProps>((props, ref) => {
  const polylineRef = usePolyline(props);
  useImperativeHandle(ref, () => polylineRef.current, []);
  return null;
});

Polyline.displayName = 'Polyline';
```

### Polyline Usage

```tsx
import { Polyline } from '@/components/polyline';

const routePath = [
  { lat: 37.772, lng: -122.214 },
  { lat: 21.291, lng: -157.821 },
  { lat: -18.142, lng: 178.431 },
  { lat: -27.467, lng: 153.027 },
];

<Polyline
  path={routePath}
  strokeColor="#0000FF"
  strokeOpacity={1.0}
  strokeWeight={3}
  geodesic={true}
  editable={true}
/>
```

---

## Real-Time Sync: Marker + Circle

Key pattern for making shapes follow a draggable marker during drag (not just on drop):

```tsx
function DraggableMarkerWithCircle() {
  const [position, setPosition] = useState({ lat: 40.7128, lng: -74.006 });

  return (
    <Map defaultCenter={position} defaultZoom={14} mapId="YOUR_MAP_ID">
      <AdvancedMarker
        position={position}
        draggable
        onDrag={(e) => {
          // Update position DURING drag - this is the key!
          if (e.latLng) {
            setPosition({
              lat: e.latLng.lat(),
              lng: e.latLng.lng(),
            });
          }
        }}
      />
      
      {/* Circle follows marker in real-time */}
      <Circle
        center={position}
        radius={500}
        strokeColor="#4285F4"
        fillColor="#4285F4"
        fillOpacity={0.2}
      />
    </Map>
  );
}
```

### With Multiple Shapes

```tsx
function MarkerWithMultipleShapes() {
  const [center, setCenter] = useState({ lat: 40.7128, lng: -74.006 });

  // Calculate polygon points based on center
  const polygonPaths = useMemo(() => {
    const offset = 0.01;
    return [
      { lat: center.lat + offset, lng: center.lng },
      { lat: center.lat, lng: center.lng + offset },
      { lat: center.lat - offset, lng: center.lng },
      { lat: center.lat, lng: center.lng - offset },
    ];
  }, [center]);

  return (
    <>
      <AdvancedMarker
        position={center}
        draggable
        onDrag={(e) => {
          if (e.latLng) {
            setCenter({ lat: e.latLng.lat(), lng: e.latLng.lng() });
          }
        }}
      />
      
      <Circle center={center} radius={500} fillColor="#FF0000" fillOpacity={0.2} />
      <Polygon paths={polygonPaths} fillColor="#00FF00" fillOpacity={0.2} />
    </>
  );
}
```

---

## Common Options Reference

### Shared Shape Options

| Option | Type | Description |
|--------|------|-------------|
| `strokeColor` | string | Stroke color (CSS color) |
| `strokeOpacity` | number | Stroke opacity (0-1) |
| `strokeWeight` | number | Stroke width in pixels |
| `fillColor` | string | Fill color (CSS color) |
| `fillOpacity` | number | Fill opacity (0-1) |
| `draggable` | boolean | Can be dragged |
| `editable` | boolean | Can be edited (resize/reshape) |
| `visible` | boolean | Is visible |
| `zIndex` | number | Stacking order |
| `clickable` | boolean | Responds to click events |

### Circle-Specific

| Option | Type | Description |
|--------|------|-------------|
| `center` | LatLngLiteral | Circle center |
| `radius` | number | Radius in meters |

### Polygon/Polyline-Specific

| Option | Type | Description |
|--------|------|-------------|
| `paths` / `path` | LatLngLiteral[] | Array of coordinates |
| `geodesic` | boolean | Geodesic segments (follow Earth curve) |
