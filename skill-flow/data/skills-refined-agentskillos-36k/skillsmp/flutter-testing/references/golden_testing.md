# Golden Testing for Flutter

## Setup

```yaml
# pubspec.yaml
dev_dependencies:
  golden_toolkit: ^0.15.0
```

```dart
// test/flutter_test_config.dart
import 'dart:async';
import 'package:golden_toolkit/golden_toolkit.dart';

Future<void> testExecutable(FutureOr<void> Function() testMain) async {
  await loadAppFonts();
  return testMain();
}
```

## Basic Golden Test

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:golden_toolkit/golden_toolkit.dart';

void main() {
  testGoldens('AltitudeTape renders correctly', (tester) async {
    final widget = MaterialApp(
      home: Scaffold(
        body: AltitudeTape(
          altitude: 5500,
          verticalSpeed: 500,
        ),
      ),
    );

    await tester.pumpWidget(widget);
    await screenMatchesGolden(tester, 'altitude_tape_climbing');
  });
}
```

## Multi-Device Testing

```dart
testGoldens('FlightInstruments across devices', (tester) async {
  final builder = DeviceBuilder()
    ..overrideDevicesForAllScenarios(devices: [
      Device.phone,
      Device.iphone11,
      Device.tabletPortrait,
      Device.tabletLandscape,
      const Device(
        name: 'ipad_mini',
        size: Size(768, 1024),
        devicePixelRatio: 2.0,
      ),
    ])
    ..addScenario(
      name: 'default',
      widget: const FlightInstruments(),
    );

  await tester.pumpDeviceBuilder(builder);
  await screenMatchesGolden(tester, 'flight_instruments_devices');
});
```

## Day/Night Theme Testing

```dart
testGoldens('MapDisplay day and night themes', (tester) async {
  final builder = DeviceBuilder()
    ..overrideDevicesForAllScenarios(devices: [Device.phone])
    ..addScenario(
      name: 'day_mode',
      widget: Theme(
        data: EfbTheme.day,
        child: const MapDisplay(),
      ),
    )
    ..addScenario(
      name: 'night_mode',
      widget: Theme(
        data: EfbTheme.night,
        child: const MapDisplay(),
      ),
    )
    ..addScenario(
      name: 'night_mode_red',
      widget: Theme(
        data: EfbTheme.nightRed,
        child: const MapDisplay(),
      ),
    );

  await tester.pumpDeviceBuilder(builder);
  await screenMatchesGolden(tester, 'map_display_themes');
});
```

## Widget State Scenarios

```dart
testGoldens('WeatherDisplay states', (tester) async {
  final builder = DeviceBuilder()
    ..overrideDevicesForAllScenarios(devices: [Device.phone])
    ..addScenario(
      name: 'vfr',
      widget: WeatherDisplay(metar: testMetarVFR),
    )
    ..addScenario(
      name: 'mvfr',
      widget: WeatherDisplay(metar: testMetarMVFR),
    )
    ..addScenario(
      name: 'ifr',
      widget: WeatherDisplay(metar: testMetarIFR),
    )
    ..addScenario(
      name: 'lifr',
      widget: WeatherDisplay(metar: testMetarLIFR),
    )
    ..addScenario(
      name: 'loading',
      widget: const WeatherDisplay(metar: null, isLoading: true),
    )
    ..addScenario(
      name: 'error',
      widget: const WeatherDisplay(metar: null, error: 'Network error'),
    );

  await tester.pumpDeviceBuilder(builder);
  await screenMatchesGolden(tester, 'weather_display_states');
});
```

## Custom Device for Aviation Displays

```dart
// Common aviation display sizes
const efbTablet = Device(
  name: 'efb_tablet',
  size: Size(1024, 768), // iPad landscape
  devicePixelRatio: 2.0,
);

const efbTabletPortrait = Device(
  name: 'efb_tablet_portrait',
  size: Size(768, 1024),
  devicePixelRatio: 2.0,
);

const efbMountedDisplay = Device(
  name: 'panel_mounted',
  size: Size(1280, 800), // 7" panel mount
  devicePixelRatio: 1.5,
);
```

## Updating Golden Files

```bash
# Update all golden files
flutter test --update-goldens

# Update specific test file
flutter test test/widgets/altitude_tape_test.dart --update-goldens

# CI check (fails if goldens don't match)
flutter test
```

## Organizing Golden Files

```
test/
├── goldens/
│   ├── ci/                    # Reference images for CI
│   │   ├── altitude_tape_climbing.png
│   │   ├── flight_instruments_devices.png
│   │   └── map_display_themes.png
│   └── failures/              # Failed comparison images
├── widgets/
│   ├── altitude_tape_test.dart
│   └── flight_instruments_test.dart
└── flutter_test_config.dart
```

## Font Loading

```dart
// flutter_test_config.dart
Future<void> testExecutable(FutureOr<void> Function() testMain) async {
  return GoldenToolkit.runWithConfiguration(
    () async {
      await loadAppFonts();
      return testMain();
    },
    config: GoldenToolkitConfiguration(
      enableRealShadows: true,
      // Skip on CI if fonts cause issues
      skipGoldenAssertion: () => !Platform.environment.containsKey('CI'),
    ),
  );
}
```

## Custom Comparison Tolerance

```dart
testGoldens('map with dynamic content', (tester) async {
  // Allow small pixel differences for anti-aliasing
  await tester.pumpWidget(const MapView());

  await screenMatchesGolden(
    tester,
    'map_view',
    customPump: (tester) async {
      await tester.pumpAndSettle();
    },
  );
},
// Configure in golden_toolkit.yaml or programmatically
);
```

## Integration with CI

```yaml
# .github/workflows/test.yml
- name: Run golden tests
  run: flutter test --tags=golden

- name: Upload golden failures
  if: failure()
  uses: actions/upload-artifact@v3
  with:
    name: golden-failures
    path: test/goldens/failures/
```

## Tagging Golden Tests

```dart
@Tags(['golden'])
void main() {
  testGoldens('widget appearance', (tester) async {
    // ...
  });
}
```

```bash
# Run only golden tests
flutter test --tags golden

# Exclude golden tests
flutter test --exclude-tags golden
```

## Accessibility Golden Tests

```dart
testGoldens('accessible color contrast', (tester) async {
  final builder = DeviceBuilder()
    ..addScenario(
      name: 'normal_vision',
      widget: const FlightDisplay(),
    )
    ..addScenario(
      name: 'high_contrast',
      widget: MediaQuery(
        data: const MediaQueryData(highContrast: true),
        child: const FlightDisplay(),
      ),
    );

  await tester.pumpDeviceBuilder(builder);
  await screenMatchesGolden(tester, 'flight_display_accessibility');
});
```
