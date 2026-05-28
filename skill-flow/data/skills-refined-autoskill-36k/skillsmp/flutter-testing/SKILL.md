---
name: flutter-testing
description: Flutter testing patterns for aviation EFB applications. Use when writing unit tests, widget tests, integration tests, or golden tests. Includes mocking strategies for location/sensors, test fixtures for aviation data, and patterns for testing BLoC state management, offline scenarios, and safety-critical navigation calculations.
---

# Flutter Testing

## Overview

Comprehensive testing patterns for MagentaLine EFB, ensuring reliability for safety-critical aviation software.

## Test Types

| Type | Location | Purpose | Speed |
|------|----------|---------|-------|
| Unit | `test/` | Pure Dart logic, calculations | Fast |
| Widget | `test/` | UI components in isolation | Fast |
| Integration | `integration_test/` | Full app flows | Slow |
| Golden | `test/` | Visual regression | Medium |

## Quick Start

### Run All Tests
```bash
flutter test
flutter test --coverage
```

### Run Specific Test
```bash
flutter test test/domain/navigation_test.dart
```

### Integration Tests
```bash
flutter test integration_test/app_test.dart
```

## Unit Testing Aviation Calculations

**Critical**: All navigation math must have 100% test coverage.

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:magentaline/domain/navigation/haversine.dart';

void main() {
  group('Haversine Distance', () {
    test('KLAX to KSFO is ~300nm', () {
      final distance = haversineNm(
        lat1: 33.9425, lon1: -118.4081,  // KLAX
        lat2: 37.6213, lon2: -122.3790,  // KSFO
      );
      expect(distance, closeTo(300, 5));
    });

    test('same point returns zero', () {
      expect(haversineNm(lat1: 0, lon1: 0, lat2: 0, lon2: 0), equals(0));
    });

    test('antipodal points return half circumference', () {
      final distance = haversineNm(lat1: 0, lon1: 0, lat2: 0, lon2: 180);
      expect(distance, closeTo(10800, 10)); // ~180° of great circle
    });
  });
}
```

## Widget Testing

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:magentaline/presentation/widgets/altitude_tape.dart';

void main() {
  testWidgets('AltitudeTape displays current altitude', (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: AltitudeTape(altitude: 5500, verticalSpeed: 500),
      ),
    );

    expect(find.text('5500'), findsOneWidget);
    expect(find.byIcon(Icons.arrow_upward), findsOneWidget);
  });

  testWidgets('AltitudeTape shows descent indicator', (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: AltitudeTape(altitude: 3000, verticalSpeed: -800),
      ),
    );

    expect(find.byIcon(Icons.arrow_downward), findsOneWidget);
  });
}
```

## BLoC Testing

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockAirportRepository extends Mock implements AirportRepository {}

void main() {
  late MockAirportRepository mockRepository;

  setUp(() {
    mockRepository = MockAirportRepository();
  });

  group('AirportSearchBloc', () {
    blocTest<AirportSearchBloc, AirportSearchState>(
      'emits [loading, loaded] when search succeeds',
      build: () {
        when(() => mockRepository.search('KLAX'))
            .thenAnswer((_) async => [testAirport]);
        return AirportSearchBloc(repository: mockRepository);
      },
      act: (bloc) => bloc.add(const SearchAirports('KLAX')),
      expect: () => [
        const AirportSearchLoading(),
        AirportSearchLoaded([testAirport]),
      ],
    );

    blocTest<AirportSearchBloc, AirportSearchState>(
      'emits [loading, error] when search fails',
      build: () {
        when(() => mockRepository.search(any()))
            .thenThrow(Exception('Network error'));
        return AirportSearchBloc(repository: mockRepository);
      },
      act: (bloc) => bloc.add(const SearchAirports('KLAX')),
      expect: () => [
        const AirportSearchLoading(),
        isA<AirportSearchError>(),
      ],
    );
  });
}
```

## Mocking Sensors & Location

See `references/mocking_sensors.md` for comprehensive mocking patterns.

```dart
// Mock GPS position stream
class MockLocationService extends Mock implements LocationService {}

void main() {
  late MockLocationService mockLocation;

  setUp(() {
    mockLocation = MockLocationService();
    when(() => mockLocation.positionStream).thenAnswer(
      (_) => Stream.fromIterable([
        Position(latitude: 33.9425, longitude: -118.4081, altitude: 1000),
        Position(latitude: 33.9500, longitude: -118.4000, altitude: 1500),
      ]),
    );
  });
}
```

## Golden Tests

```dart
import 'package:golden_toolkit/golden_toolkit.dart';

void main() {
  testGoldens('FlightInstruments renders correctly', (tester) async {
    await loadAppFonts();

    final builder = DeviceBuilder()
      ..overrideDevicesForAllScenarios(devices: [Device.phone, Device.tablet])
      ..addScenario(
        name: 'day_mode',
        widget: const FlightInstruments(theme: EfbTheme.day),
      )
      ..addScenario(
        name: 'night_mode',
        widget: const FlightInstruments(theme: EfbTheme.night),
      );

    await tester.pumpDeviceBuilder(builder);
    await screenMatchesGolden(tester, 'flight_instruments');
  });
}
```

## Test Fixtures

Use `references/test_fixtures.md` for aviation test data patterns.

```dart
// test/fixtures/airports.dart
final testKLAX = Airport(
  id: 'KLAX',
  name: 'Los Angeles International',
  latitude: 33.9425,
  longitude: -118.4081,
  elevation: 128,
  runways: [testRunway25L, testRunway25R],
);
```

## Integration Testing

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:magentaline/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('complete flight planning flow', (tester) async {
    app.main();
    await tester.pumpAndSettle();

    // Search for departure airport
    await tester.tap(find.byKey(const Key('departure_field')));
    await tester.enterText(find.byKey(const Key('departure_field')), 'KLAX');
    await tester.pumpAndSettle();
    await tester.tap(find.text('Los Angeles International'));
    await tester.pumpAndSettle();

    // Search for destination
    await tester.tap(find.byKey(const Key('destination_field')));
    await tester.enterText(find.byKey(const Key('destination_field')), 'KSFO');
    await tester.pumpAndSettle();
    await tester.tap(find.text('San Francisco International'));
    await tester.pumpAndSettle();

    // Verify route calculated
    expect(find.textContaining('300 nm'), findsOneWidget);
  });
}
```

## Coverage Requirements

For aviation safety-critical code:

| Component | Minimum Coverage |
|-----------|-----------------|
| Navigation math | 100% |
| Flight planning | 95% |
| Data parsing | 90% |
| UI widgets | 80% |
| Overall | 85% |

```bash
# Generate coverage report
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html
```

## References

| Document | Description |
|----------|-------------|
| `references/mocking_sensors.md` | GPS, compass, barometer mocking |
| `references/test_fixtures.md` | Aviation data fixtures |
| `references/bloc_testing.md` | BLoC test patterns |
| `references/golden_testing.md` | Visual regression setup |
