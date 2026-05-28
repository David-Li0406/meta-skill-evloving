# Mocking Sensors & Platform Services

## GPS/Location Mocking

### Mock Location Service

```dart
import 'package:mocktail/mocktail.dart';
import 'package:geolocator/geolocator.dart';

class MockGeolocator extends Mock implements GeolocatorPlatform {}

class FakePosition extends Fake implements Position {}

void main() {
  late MockGeolocator mockGeolocator;

  setUpAll(() {
    registerFallbackValue(FakePosition());
    registerFallbackValue(const LocationSettings());
  });

  setUp(() {
    mockGeolocator = MockGeolocator();
    GeolocatorPlatform.instance = mockGeolocator;
  });

  test('tracks position updates', () async {
    final positions = [
      Position(
        latitude: 33.9425,
        longitude: -118.4081,
        altitude: 1000,
        accuracy: 5,
        heading: 270,
        speed: 125, // knots converted to m/s
        speedAccuracy: 1,
        timestamp: DateTime.now(),
        altitudeAccuracy: 10,
        headingAccuracy: 2,
      ),
      Position(
        latitude: 33.9500,
        longitude: -118.4100,
        altitude: 1500,
        accuracy: 5,
        heading: 275,
        speed: 130,
        speedAccuracy: 1,
        timestamp: DateTime.now().add(const Duration(seconds: 5)),
        altitudeAccuracy: 10,
        headingAccuracy: 2,
      ),
    ];

    when(() => mockGeolocator.getPositionStream(
      locationSettings: any(named: 'locationSettings'),
    )).thenAnswer((_) => Stream.fromIterable(positions));

    // Test your location-dependent code
  });
}
```

### Simulating Flight Path

```dart
/// Generate a stream of positions simulating a flight path
Stream<Position> simulateFlightPath({
  required Position start,
  required Position end,
  required Duration duration,
  required int updateIntervalMs,
}) async* {
  final steps = duration.inMilliseconds ~/ updateIntervalMs;
  final latStep = (end.latitude - start.latitude) / steps;
  final lonStep = (end.longitude - start.longitude) / steps;
  final altStep = (end.altitude - start.altitude) / steps;

  for (int i = 0; i <= steps; i++) {
    yield Position(
      latitude: start.latitude + (latStep * i),
      longitude: start.longitude + (lonStep * i),
      altitude: start.altitude + (altStep * i),
      accuracy: 5,
      heading: _calculateBearing(
        start.latitude + (latStep * i),
        start.longitude + (lonStep * i),
        end.latitude,
        end.longitude,
      ),
      speed: 75.0, // ~145 knots in m/s
      speedAccuracy: 1,
      timestamp: DateTime.now().add(Duration(milliseconds: updateIntervalMs * i)),
      altitudeAccuracy: 10,
      headingAccuracy: 2,
    );
    await Future.delayed(Duration(milliseconds: updateIntervalMs));
  }
}
```

## Compass/Heading Mocking

```dart
class MockCompassService extends Mock implements CompassService {}

void main() {
  late MockCompassService mockCompass;

  setUp(() {
    mockCompass = MockCompassService();
  });

  test('heading indicator follows compass', () async {
    when(() => mockCompass.headingStream).thenAnswer(
      (_) => Stream.periodic(
        const Duration(milliseconds: 100),
        (i) => CompassHeading(
          heading: (270.0 + i) % 360, // Slowly rotating
          accuracy: 5.0,
        ),
      ),
    );

    // Test heading-dependent widgets
  });
}
```

## Barometer/Pressure Altitude

```dart
class MockBarometerService extends Mock implements BarometerService {}

void main() {
  late MockBarometerService mockBarometer;

  setUp(() {
    mockBarometer = MockBarometerService();
  });

  test('pressure altitude calculation', () {
    // Standard pressure at sea level: 1013.25 hPa
    // Pressure decreases ~1 hPa per 30 feet
    when(() => mockBarometer.currentPressure)
        .thenReturn(983.25); // ~1000 ft pressure altitude

    when(() => mockBarometer.pressureStream).thenAnswer(
      (_) => Stream.fromIterable([
        983.25, // 1000 ft
        980.25, // 1100 ft
        977.25, // 1200 ft
      ]),
    );
  });
}
```

## ADS-B/Traffic Mocking

```dart
class MockStratuxService extends Mock implements StratuxService {}

Traffic createMockTraffic({
  required String callsign,
  required double lat,
  required double lon,
  required int altitude,
  required int heading,
  required int groundSpeed,
}) {
  return Traffic(
    icaoAddress: 0xABCDEF,
    callsign: callsign,
    latitude: lat,
    longitude: lon,
    altitude: altitude,
    altitudeType: AltitudeType.baro,
    heading: heading,
    groundSpeed: groundSpeed,
    verticalSpeed: 0,
    squawk: 1200,
    timestamp: DateTime.now(),
  );
}

void main() {
  late MockStratuxService mockStratux;

  setUp(() {
    mockStratux = MockStratuxService();
  });

  test('traffic display shows nearby aircraft', () async {
    final traffic = [
      createMockTraffic(
        callsign: 'N12345',
        lat: 33.95,
        lon: -118.40,
        altitude: 5500,
        heading: 180,
        groundSpeed: 120,
      ),
      createMockTraffic(
        callsign: 'UAL123',
        lat: 33.90,
        lon: -118.35,
        altitude: 10000,
        heading: 270,
        groundSpeed: 350,
      ),
    ];

    when(() => mockStratux.trafficStream)
        .thenAnswer((_) => Stream.fromIterable([traffic]));

    // Test traffic display
  });
}
```

## Network Connectivity

```dart
class MockConnectivity extends Mock implements Connectivity {}

void main() {
  late MockConnectivity mockConnectivity;

  setUp(() {
    mockConnectivity = MockConnectivity();
  });

  group('offline mode', () {
    setUp(() {
      when(() => mockConnectivity.checkConnectivity())
          .thenAnswer((_) async => ConnectivityResult.none);
      when(() => mockConnectivity.onConnectivityChanged)
          .thenAnswer((_) => Stream.value(ConnectivityResult.none));
    });

    test('uses cached data when offline', () async {
      // Test offline behavior
    });
  });

  group('online mode', () {
    setUp(() {
      when(() => mockConnectivity.checkConnectivity())
          .thenAnswer((_) async => ConnectivityResult.wifi);
    });

    test('fetches fresh data when online', () async {
      // Test online behavior
    });
  });
}
```

## Platform Channel Mocking

```dart
void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUpAll(() {
    // Mock platform channel for native features
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(
      const MethodChannel('com.magentaline/sensors'),
      (call) async {
        switch (call.method) {
          case 'getAHRS':
            return {
              'pitch': 5.0,
              'roll': -3.0,
              'heading': 270.0,
            };
          case 'getGForce':
            return {'x': 0.0, 'y': 0.0, 'z': 1.0};
          default:
            return null;
        }
      },
    );
  });
}
```
