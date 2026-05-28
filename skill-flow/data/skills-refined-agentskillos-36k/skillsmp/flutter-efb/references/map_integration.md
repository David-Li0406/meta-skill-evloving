# Map Integration with flutter_map

Implementing moving maps for EFB applications using flutter_map and MBTiles.

## Basic Setup

### Dependencies

```yaml
dependencies:
  flutter_map: ^6.0.0
  latlong2: ^0.9.0
  flutter_map_mbtiles: ^1.0.0
  geolocator: ^10.0.0
  flutter_compass: ^0.7.0
```

### Basic Map Widget

```dart
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

class AviationMap extends StatefulWidget {
  final LatLng initialCenter;
  final double initialZoom;

  const AviationMap({
    super.key,
    this.initialCenter = const LatLng(37.7749, -122.4194),
    this.initialZoom = 10,
  });

  @override
  State<AviationMap> createState() => _AviationMapState();
}

class _AviationMapState extends State<AviationMap> {
  late final MapController _mapController;

  @override
  void initState() {
    super.initState();
    _mapController = MapController();
  }

  @override
  Widget build(BuildContext context) {
    return FlutterMap(
      mapController: _mapController,
      options: MapOptions(
        initialCenter: widget.initialCenter,
        initialZoom: widget.initialZoom,
        minZoom: 4,
        maxZoom: 16,
        interactionOptions: const InteractionOptions(
          flags: InteractiveFlag.all & ~InteractiveFlag.rotate,
        ),
        onPositionChanged: _onPositionChanged,
      ),
      children: [
        // Base map layer
        TileLayer(
          urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
          userAgentPackageName: 'com.magentaline.efb',
        ),

        // Offline tiles layer (when available)
        // MBTilesTileLayer(path: 'assets/tiles/sectional.mbtiles'),

        // Airspace layer
        PolygonLayer(polygons: _airspacePolygons),

        // Airport markers
        MarkerLayer(markers: _airportMarkers),

        // Current position
        CurrentLocationLayer(),

        // Route line
        PolylineLayer(polylines: _routeLines),
      ],
    );
  }
}
```

## Offline Tiles with MBTiles

### Loading MBTiles

```dart
import 'package:flutter_map_mbtiles/flutter_map_mbtiles.dart';

class OfflineTileManager {
  final Map<String, MBTilesProvider> _providers = {};

  Future<MBTilesProvider> loadTileSet(String path) async {
    if (_providers.containsKey(path)) {
      return _providers[path]!;
    }

    final provider = MBTilesProvider.fromPath(path);
    await provider.open();
    _providers[path] = provider;
    return provider;
  }

  Widget buildTileLayer(String path) {
    return FutureBuilder<MBTilesProvider>(
      future: loadTileSet(path),
      builder: (context, snapshot) {
        if (!snapshot.hasData) {
          return const SizedBox.shrink();
        }
        return TileLayer(
          tileProvider: snapshot.data!,
        );
      },
    );
  }

  Future<void> dispose() async {
    for (final provider in _providers.values) {
      await provider.close();
    }
    _providers.clear();
  }
}
```

### Layer Switching

```dart
enum ChartType {
  sectional,
  tac,
  ifrLow,
  ifrHigh,
}

class ChartLayerManager {
  ChartType _currentChart = ChartType.sectional;

  String get currentPath => switch (_currentChart) {
    ChartType.sectional => 'assets/tiles/sectional.mbtiles',
    ChartType.tac => 'assets/tiles/tac.mbtiles',
    ChartType.ifrLow => 'assets/tiles/ifr_low.mbtiles',
    ChartType.ifrHigh => 'assets/tiles/ifr_high.mbtiles',
  };

  void switchTo(ChartType chart) {
    _currentChart = chart;
  }
}
```

## GPS Integration

### Position Tracking

```dart
import 'package:geolocator/geolocator.dart';

class GpsService {
  StreamSubscription<Position>? _subscription;
  final _positionController = StreamController<Position>.broadcast();

  Stream<Position> get positionStream => _positionController.stream;

  Future<void> startTracking() async {
    // Check permissions
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      throw LocationServiceDisabledException();
    }

    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
    }

    // Start listening
    _subscription = Geolocator.getPositionStream(
      locationSettings: const LocationSettings(
        accuracy: LocationAccuracy.high,
        distanceFilter: 10, // meters
      ),
    ).listen((position) {
      _positionController.add(position);
    });
  }

  void stopTracking() {
    _subscription?.cancel();
    _subscription = null;
  }

  void dispose() {
    stopTracking();
    _positionController.close();
  }
}
```

### Aircraft Marker

```dart
class AircraftMarker extends StatelessWidget {
  final LatLng position;
  final double heading;
  final double groundSpeed;

  const AircraftMarker({
    super.key,
    required this.position,
    required this.heading,
    required this.groundSpeed,
  });

  @override
  Widget build(BuildContext context) {
    return Marker(
      point: position,
      width: 40,
      height: 40,
      child: Transform.rotate(
        angle: heading * pi / 180,
        child: const Icon(
          Icons.navigation,
          color: Colors.blue,
          size: 40,
        ),
      ),
    );
  }
}
```

## Airport Markers

```dart
class AirportMarkerLayer extends StatelessWidget {
  final List<Airport> airports;
  final Function(Airport)? onTap;

  const AirportMarkerLayer({
    super.key,
    required this.airports,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return MarkerLayer(
      markers: airports.map((airport) {
        return Marker(
          point: LatLng(airport.latitude, airport.longitude),
          width: 30,
          height: 30,
          child: GestureDetector(
            onTap: () => onTap?.call(airport),
            child: _buildAirportIcon(airport),
          ),
        );
      }).toList(),
    );
  }

  Widget _buildAirportIcon(Airport airport) {
    // Different icons based on airport type
    if (airport.isTowered) {
      return Container(
        decoration: BoxDecoration(
          color: Colors.blue,
          shape: BoxShape.circle,
          border: Border.all(color: Colors.white, width: 2),
        ),
        child: Center(
          child: Text(
            airport.id,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 8,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      );
    } else {
      return Container(
        decoration: BoxDecoration(
          color: Colors.purple,
          shape: BoxShape.circle,
        ),
        child: const Icon(Icons.location_on, color: Colors.white, size: 20),
      );
    }
  }
}
```

## Route Display

```dart
class RouteLayer extends StatelessWidget {
  final List<LatLng> waypoints;
  final LatLng? currentPosition;

  const RouteLayer({
    super.key,
    required this.waypoints,
    this.currentPosition,
  });

  @override
  Widget build(BuildContext context) {
    final List<Polyline> lines = [];

    // Magenta course line (ahead)
    if (currentPosition != null && waypoints.isNotEmpty) {
      final remainingPoints = [currentPosition!, ...waypoints];
      lines.add(Polyline(
        points: remainingPoints,
        color: const Color(0xFFFF00FF), // Magenta!
        strokeWidth: 4,
      ));
    }

    // Gray line (already flown)
    // ... add previous track

    return PolylineLayer(polylines: lines);
  }
}
```

## Airspace Display

```dart
class AirspaceLayer extends StatelessWidget {
  final List<Airspace> airspaces;

  const AirspaceLayer({super.key, required this.airspaces});

  @override
  Widget build(BuildContext context) {
    return PolygonLayer(
      polygons: airspaces.map((airspace) {
        return Polygon(
          points: airspace.boundary,
          color: _getAirspaceColor(airspace.type).withOpacity(0.2),
          borderColor: _getAirspaceColor(airspace.type),
          borderStrokeWidth: 2,
          label: airspace.name,
          labelStyle: const TextStyle(color: Colors.black87, fontSize: 10),
        );
      }).toList(),
    );
  }

  Color _getAirspaceColor(AirspaceType type) => switch (type) {
    AirspaceType.classB => Colors.blue,
    AirspaceType.classC => Colors.purple,
    AirspaceType.classD => Colors.blue[300]!,
    AirspaceType.classE => Colors.grey,
    AirspaceType.moa => Colors.orange,
    AirspaceType.restricted => Colors.red,
    AirspaceType.prohibited => Colors.red[900]!,
    AirspaceType.warning => Colors.yellow,
    AirspaceType.alert => Colors.yellow[700]!,
    _ => Colors.grey,
  };
}
```

## Map Controls

```dart
class MapControls extends StatelessWidget {
  final MapController controller;
  final VoidCallback? onCenterOnPosition;
  final VoidCallback? onToggleNorthUp;
  final bool isNorthUp;

  const MapControls({
    super.key,
    required this.controller,
    this.onCenterOnPosition,
    this.onToggleNorthUp,
    this.isNorthUp = true,
  });

  @override
  Widget build(BuildContext context) {
    return Positioned(
      right: 16,
      bottom: 100,
      child: Column(
        children: [
          FloatingActionButton.small(
            heroTag: 'zoom_in',
            onPressed: () => controller.move(
              controller.camera.center,
              controller.camera.zoom + 1,
            ),
            child: const Icon(Icons.add),
          ),
          const SizedBox(height: 8),
          FloatingActionButton.small(
            heroTag: 'zoom_out',
            onPressed: () => controller.move(
              controller.camera.center,
              controller.camera.zoom - 1,
            ),
            child: const Icon(Icons.remove),
          ),
          const SizedBox(height: 16),
          FloatingActionButton.small(
            heroTag: 'center',
            onPressed: onCenterOnPosition,
            child: const Icon(Icons.my_location),
          ),
          const SizedBox(height: 8),
          FloatingActionButton.small(
            heroTag: 'north',
            backgroundColor: isNorthUp ? Colors.blue : Colors.grey,
            onPressed: onToggleNorthUp,
            child: const Icon(Icons.navigation),
          ),
        ],
      ),
    );
  }
}
```
