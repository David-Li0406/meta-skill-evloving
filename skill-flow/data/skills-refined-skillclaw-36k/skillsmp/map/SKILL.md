---
name: map
description: Especialista en integración de Mapbox y geolocalización. Maneja visualización de mapas, tracking de ubicación, rutas visuales y optimización de geocoding.
---

## Responsabilidad Única
Todo lo relacionado con Mapbox, geolocalización y visualización de mapas. NO incluye lógica de negocio de rutas ni optimizaciones generales.

---

## Mapbox Setup & Configuration

### SDK
- **Mapbox Maps SDK**: Para visualización de mapas
- **Mapbox Search API**: Para geocoding y búsqueda de direcciones
- **Versión**: Usar última versión estable

### Estilo de Mapa
- **Dark Style**: Usar `mapbox://styles/mapbox/dark-v11` para coherencia con Neon-Dark theme
- **Custom Style**: Opcionalmente crear estilo custom con colores neon
- **Zoom levels**: Min 10 (ciudad), Max 18 (calle)

### Configuración Inicial
```dart
MapboxMap(
  styleString: 'mapbox://styles/mapbox/dark-v11',
  cameraOptions: CameraOptions(
    center: Point(coordinates: Position(-74.3636, 4.3369)), // Fusagasugá
    zoom: 13.0,
  ),
  onMapCreated: _onMapCreated,
)
```

---

## Offline Maps (Tile Caching)

### Bounding Box Fusagasugá
Definir área de descarga para tiles offline:
```dart
final fusagasugaBounds = CoordinateBounds(
  southwest: Point(coordinates: Position(-74.4136, 4.2869)),
  northeast: Point(coordinates: Position(-74.3136, 4.3869)),
);
```

### Estrategia de Descarga
- **Cuándo**: Al detectar WiFi o al iniciar ruta por primera vez
- **Zoom levels**: 12-16 (balance entre detalle y tamaño)
- **Tipo**: Vectorial (más ligero y escalable que raster)
- **Tamaño estimado**: ~50-100 MB para Fusagasugá

### Implementación
```dart
final offlineManager = await OfflineManager.getInstance();

await offlineManager.downloadRegion(
  OfflineRegionDefinition(
    styleURL: 'mapbox://styles/mapbox/dark-v11',
    bounds: fusagasugaBounds,
    minZoom: 12.0,
    maxZoom: 16.0,
  ),
  metadata: {'region': 'fusagasuga'},
);
```

### Reglas de Negocio - Offline
- No descargar en datos móviles (solo WiFi)
- Actualizar tiles cada 30 días
- Permitir descarga manual desde configuración
- Mostrar progreso de descarga al usuario

---

## Location Tracking

### Configuración de Precisión
```dart
LocationSettings(
  accuracy: LocationAccuracy.high,
  distanceFilter: 10, // Actualizar cada 10 metros
  timeLimit: Duration(seconds: 5),
)
```

### Location Marker (User Icon)
- **Tipo**: `PointAnnotation` para mejor performance
- **Icono**: Custom icon con flecha direccional
- **Rotación**: Basada en heading del compass
- **Smoothing**: Aplicar LERP para rotación suave

```dart
// Actualizar solo si movimiento significativo
void updateLocationMarker(Position position, double heading) {
  final distance = _calculateDistance(_lastPosition, position);
  final headingDiff = (heading - _lastHeading).abs();
  
  if (distance < 1.0 && headingDiff < 4.0) {
    return; // No actualizar si cambio es mínimo
  }
  
  // Smooth rotation con LERP
  final smoothHeading = _lerp(_lastHeading, heading, 0.3);
  
  _locationAnnotation?.geometry = Point(coordinates: position);
  _locationAnnotation?.iconRotate = smoothHeading;
}

double _lerp(double start, double end, double t) {
  return start + (end - start) * t;
}
```

### Optimizaciones de Location
- Threshold de 1 metro para actualizar posición
- Threshold de 4 grados para actualizar rotación
- Pausar tracking cuando app está en background
- Reanudar tracking al volver a tab de mapa

---

## Polylines y Rutas Visuales

### Gradient Polyline (Progreso de Ruta)
Visualizar ruta con gradiente que cambia según progreso:

```dart
LineLayer(
  id: 'route-layer',
  sourceId: 'route-source',
  lineColor: [
    'interpolate',
    ['linear'],
    ['line-progress'],
    0, '#00FFFF', // Neon Cyan (inicio)
    1, '#39FF14', // Neon Green (fin)
  ],
  lineWidth: 5.0,
  lineGradient: true,
)
```

### Progress Tracking
- Limpiar segmentos ya recorridos para liberar memoria
- Actualizar gradiente en tiempo real
- Mostrar puntos de entrega como markers

### Implementación
```dart
void updateRouteProgress(double progress) {
  // progress: 0.0 - 1.0
  final completedSegments = _routeCoordinates.take(
    (_routeCoordinates.length * progress).round()
  ).toList();
  
  _mapController.updateSource(
    'route-source',
    GeoJsonSource(
      data: LineString(coordinates: completedSegments).toJson(),
    ),
  );
}
```

---

## Markers y Annotations

### Package Markers (Pins Numerados)
Mostrar paquetes en el mapa con números:

```dart
PointAnnotation(
  id: 'package-${package.id}',
  geometry: Point(coordinates: package.coordinates),
  iconImage: 'custom-pin', // Custom image con número
  iconSize: 1.0,
  iconAnchor: IconAnchor.BOTTOM,
)
```

### Custom Pin con Número
Generar imagen de pin con número dinámicamente:
```dart
Future<Uint8List> generateNumberedPin(int number, Color neonColor) async {
  final recorder = ui.PictureRecorder();
  final canvas = Canvas(recorder);
  
  // Dibujar pin con número
  // ... código de drawing
  
  final picture = recorder.endRecording();
  final image = await picture.toImage(60, 80);
  final bytes = await image.toByteData(format: ui.ImageByteFormat.png);
  return bytes!.buffer.asUint8List();
}
```

### Reglas de Markers
- Mostrar solo paquetes de ruta activa
- Color según estado (pending: orange, delivered: green, failed: red)
- Tap en marker abre detalles del paquete
- Cluster markers si hay >20 paquetes cercanos

---

## Geocoding y Búsqueda de Direcciones

### Capa de Caché Local
Antes de consultar API, buscar en caché local:

```dart
Future<Address?> searchAddress(String query) async {
  // 1. Normalizar query
  final normalizedQuery = query.trim().toLowerCase();
  
  // 2. Buscar en caché local
  final cached = await _cacheRepository.findAddress(normalizedQuery);
  if (cached != null && _isCacheValid(cached.timestamp)) {
    return cached;
  }
  
  // 3. Consultar API de Mapbox
  final result = await _mapboxSearchAPI.search(
    query: normalizedQuery,
    proximity: Position(-74.3636, 4.3369), // Fusagasugá
    bbox: fusagasugaBounds,
    limit: 5,
  );
  
  // 4. Guardar en caché
  if (result != null) {
    await _cacheRepository.saveAddress(result);
  }
  
  return result;
}

bool _isCacheValid(DateTime timestamp) {
  return DateTime.now().difference(timestamp).inDays < 30;
}
```

### Optimización de Búsquedas

#### Smart Debouncing
```dart
Timer? _debounceTimer;

void onSearchTextChanged(String text) {
  _debounceTimer?.cancel();
  
  // No buscar si cambio no es significativo
  if (text.trim() == _lastQuery.trim()) return;
  
  _debounceTimer = Timer(Duration(milliseconds: 500), () {
    _performSearch(text);
  });
}
```

#### Bounding Box Estricto
Limitar búsquedas a Fusagasugá y Cundinamarca:
```dart
final searchBounds = CoordinateBounds(
  southwest: Position(-74.5, 4.0),
  northeast: Position(-74.0, 4.5),
);
```

#### Limitación de Resultados
Pedir solo 5 resultados más relevantes para ahorrar ancho de banda:
```dart
final results = await searchAPI.search(
  query: query,
  limit: 5,
  types: ['address', 'place'],
);
```

---

## Lazy Geocoding

### Estrategia
No geocodificar todos los paquetes al cargar lista, solo cuando sea necesario:

```dart
class PackageListItem extends StatefulWidget {
  final Package package;
  
  @override
  Widget build(BuildContext context) {
    return VisibilityDetector(
      key: Key('package-${package.id}'),
      onVisibilityChanged: (info) {
        if (info.visibleFraction > 0.5) {
          // Item visible, geocodificar si no tiene coordenadas
          _geocodeIfNeeded();
        }
      },
      child: PackageCard(package: package),
    );
  }
}
```

### Reglas de Lazy Geocoding
- Geocodificar solo cuando paquete entra en viewport
- Geocodificar cuando usuario abre mapa de paquete específico
- Cachear resultados para no repetir consultas
- Priorizar paquetes de ruta activa

---

## Coordinate Compression

### Precisión Óptima
Almacenar coordenadas con 6 decimales (precisión de ~10cm):
```dart
double compressCoordinate(double coordinate) {
  return double.parse(coordinate.toStringAsFixed(6));
}

Position compressPosition(Position position) {
  return Position(
    compressCoordinate(position.lng),
    compressCoordinate(position.lat),
  );
}
```

### Beneficios
- Reduce tamaño de base de datos local
- Suficiente precisión para logística
- Mejora performance de sync

---

## Gestión de Errores

### Fallback Offline
Si API falla o no hay internet:
```dart
Future<List<Address>> searchWithFallback(String query) async {
  try {
    // Intentar API
    return await _mapboxSearchAPI.search(query);
  } catch (e) {
    // Fallback a búsqueda local parcial
    return await _cacheRepository.searchPartialMatch(query);
  }
}
```

### Manejo de Errores de Mapbox
- **Network error**: Usar caché local
- **Invalid coordinates**: Mostrar error al usuario
- **Rate limit**: Implementar exponential backoff
- **Invalid API key**: Notificar error crítico

---

## Optimización de Performance (Específica a Mapas)

### Prevenir Rebuilds de MapWidget
```dart
class MapScreen extends StatefulWidget {
  @override
  Widget build(BuildContext context) {
    return RepaintBoundary(
      child: MapboxMap(
        // ... configuración
      ),
    );
  }
}
```

### Gestión de Streams
```dart
StreamSubscription? _locationSubscription;
StreamSubscription? _compassSubscription;

@override
void dispose() {
  _locationSubscription?.cancel();
  _compassSubscription?.cancel();
  _mapController?.dispose();
  super.dispose();
}
```

### Actualización Eficiente de Markers
- Usar `updateAnnotation` en lugar de recrear
- Batch updates cuando sea posible
- Remover markers fuera de viewport

---

## Integración con Business Logic

### Separación de Responsabilidades
- **Map Skill**: Cómo mostrar el mapa, markers, rutas
- **Business Logic**: Qué paquetes mostrar, cuándo actualizar estado

### Ejemplo de Integración
```dart
// Map Provider (Presentation Layer)
class MapProvider extends Notifier<MapState> {
  void showPackagesOnMap(List<Package> packages) {
    final annotations = packages.map((p) => 
      _createPackageMarker(p)
    ).toList();
    
    _mapController.addAnnotations(annotations);
  }
  
  PointAnnotation _createPackageMarker(Package package) {
    // Lógica de visualización
  }
}
```

---

## Checklist de Implementación

Antes de considerar feature de mapa completa:

- [ ] Offline maps configurado para Fusagasugá
- [ ] Location tracking con threshold de 1m/4°
- [ ] LERP smoothing implementado para rotación
- [ ] Polyline gradient para progreso de ruta
- [ ] Markers numerados para paquetes
- [ ] Caché local de geocoding (30 días)
- [ ] Smart debouncing en búsquedas (500ms)
- [ ] Bounding box estricto aplicado
- [ ] Lazy geocoding implementado
- [ ] Coordinate compression (6 decimales)
- [ ] Fallback offline funcional
- [ ] RepaintBoundary en MapWidget
- [ ] Streams cancelados en dispose