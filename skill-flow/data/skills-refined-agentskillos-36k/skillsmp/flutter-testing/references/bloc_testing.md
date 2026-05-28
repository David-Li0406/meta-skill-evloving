# BLoC Testing Patterns

## Dependencies

```yaml
dev_dependencies:
  bloc_test: ^9.1.0
  mocktail: ^1.0.0
```

## Basic BLoC Test Structure

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockRepository extends Mock implements SomeRepository {}
class FakeParam extends Fake implements SomeParam {}

void main() {
  late MockRepository mockRepository;

  setUpAll(() {
    registerFallbackValue(FakeParam());
  });

  setUp(() {
    mockRepository = MockRepository();
  });

  group('MyBloc', () {
    test('initial state is correct', () {
      expect(MyBloc().state, equals(MyInitial()));
    });

    blocTest<MyBloc, MyState>(
      'description of what it tests',
      build: () => MyBloc(repository: mockRepository),
      act: (bloc) => bloc.add(SomeEvent()),
      expect: () => [ExpectedState()],
    );
  });
}
```

## Testing State Transitions

```dart
blocTest<FlightPlanBloc, FlightPlanState>(
  'emits [loading, loaded] when flight plan loads successfully',
  setUp: () {
    when(() => mockRepository.loadFlightPlan('FPL123'))
        .thenAnswer((_) async => testFlightPlan);
  },
  build: () => FlightPlanBloc(repository: mockRepository),
  act: (bloc) => bloc.add(const LoadFlightPlan('FPL123')),
  expect: () => [
    const FlightPlanLoading(),
    FlightPlanLoaded(testFlightPlan),
  ],
);

blocTest<FlightPlanBloc, FlightPlanState>(
  'emits [loading, error] when loading fails',
  setUp: () {
    when(() => mockRepository.loadFlightPlan(any()))
        .thenThrow(Exception('Network error'));
  },
  build: () => FlightPlanBloc(repository: mockRepository),
  act: (bloc) => bloc.add(const LoadFlightPlan('FPL123')),
  expect: () => [
    const FlightPlanLoading(),
    isA<FlightPlanError>()
        .having((e) => e.message, 'message', contains('Network')),
  ],
);
```

## Testing with Seeds

```dart
blocTest<NavigationBloc, NavigationState>(
  'updates heading from existing navigation state',
  seed: () => NavigationActive(
    position: testPosition,
    heading: 270,
    groundSpeed: 120,
  ),
  build: () => NavigationBloc(),
  act: (bloc) => bloc.add(const HeadingUpdated(280)),
  expect: () => [
    NavigationActive(
      position: testPosition,
      heading: 280,
      groundSpeed: 120,
    ),
  ],
);
```

## Testing Debounced Events

```dart
blocTest<AirportSearchBloc, AirportSearchState>(
  'debounces search queries',
  build: () {
    when(() => mockRepository.search(any()))
        .thenAnswer((_) async => [testKLAX]);
    return AirportSearchBloc(repository: mockRepository);
  },
  act: (bloc) async {
    bloc.add(const SearchQueryChanged('K'));
    bloc.add(const SearchQueryChanged('KL'));
    bloc.add(const SearchQueryChanged('KLA'));
    bloc.add(const SearchQueryChanged('KLAX'));
    await Future.delayed(const Duration(milliseconds: 500));
  },
  expect: () => [
    const AirportSearchLoading(),
    AirportSearchLoaded([testKLAX]),
  ],
  verify: (_) {
    // Only one search call due to debouncing
    verify(() => mockRepository.search('KLAX')).called(1);
    verifyNever(() => mockRepository.search('K'));
    verifyNever(() => mockRepository.search('KL'));
    verifyNever(() => mockRepository.search('KLA'));
  },
);
```

## Testing Stream Subscriptions

```dart
blocTest<TrafficBloc, TrafficState>(
  'subscribes to traffic updates',
  setUp: () {
    when(() => mockStratux.trafficStream).thenAnswer(
      (_) => Stream.fromIterable([
        [traffic1],
        [traffic1, traffic2],
        [traffic1, traffic2, traffic3],
      ]),
    );
  },
  build: () => TrafficBloc(stratuxService: mockStratux),
  act: (bloc) => bloc.add(const StartTrafficMonitoring()),
  expect: () => [
    const TrafficLoading(),
    TrafficUpdated([traffic1]),
    TrafficUpdated([traffic1, traffic2]),
    TrafficUpdated([traffic1, traffic2, traffic3]),
  ],
);
```

## Testing Error Recovery

```dart
blocTest<WeatherBloc, WeatherState>(
  'recovers from error and retries successfully',
  build: () {
    var callCount = 0;
    when(() => mockWeatherService.getMetar('KLAX')).thenAnswer((_) async {
      callCount++;
      if (callCount == 1) throw Exception('Temporary failure');
      return testMetarKLAX;
    });
    return WeatherBloc(weatherService: mockWeatherService);
  },
  act: (bloc) async {
    bloc.add(const FetchWeather('KLAX'));
    await Future.delayed(const Duration(milliseconds: 100));
    bloc.add(const RetryFetchWeather('KLAX'));
  },
  expect: () => [
    const WeatherLoading(),
    isA<WeatherError>(),
    const WeatherLoading(),
    WeatherLoaded(testMetarKLAX),
  ],
);
```

## Testing Concurrent Events

```dart
blocTest<MapBloc, MapState>(
  'handles concurrent pan and zoom events',
  build: () => MapBloc(),
  act: (bloc) {
    bloc.add(const PanMap(dx: 10, dy: 20));
    bloc.add(const ZoomMap(zoomLevel: 12));
    bloc.add(const PanMap(dx: 5, dy: 10));
  },
  expect: () => [
    // States depend on bloc transformer
    // concurrent: all states emitted
    // sequential: processed in order
    // droppable: some may be dropped
  ],
);
```

## Testing BLoC-to-BLoC Communication

```dart
void main() {
  late FlightPlanBloc flightPlanBloc;
  late NavigationBloc navigationBloc;

  setUp(() {
    flightPlanBloc = FlightPlanBloc(repository: mockRepository);
    navigationBloc = NavigationBloc(flightPlanBloc: flightPlanBloc);
  });

  tearDown(() {
    flightPlanBloc.close();
    navigationBloc.close();
  });

  blocTest<NavigationBloc, NavigationState>(
    'updates route when flight plan changes',
    build: () => navigationBloc,
    act: (bloc) {
      flightPlanBloc.add(LoadFlightPlan('FPL123'));
    },
    expect: () => [
      NavigationState(route: testFlightPlan.route),
    ],
  );
}
```

## Verifying Repository Calls

```dart
blocTest<FlightPlanBloc, FlightPlanState>(
  'saves flight plan with correct data',
  setUp: () {
    when(() => mockRepository.save(any())).thenAnswer((_) async {});
  },
  build: () => FlightPlanBloc(repository: mockRepository),
  act: (bloc) => bloc.add(SaveFlightPlan(testFlightPlan)),
  verify: (_) {
    verify(() => mockRepository.save(testFlightPlan)).called(1);
  },
);
```

## Custom Matchers

```dart
Matcher isFlightPlanLoadedWith({
  required String departure,
  required String destination,
}) {
  return isA<FlightPlanLoaded>()
      .having((s) => s.plan.departure.id, 'departure', equals(departure))
      .having((s) => s.plan.destination.id, 'destination', equals(destination));
}

// Usage
expect: () => [
  const FlightPlanLoading(),
  isFlightPlanLoadedWith(departure: 'KLAX', destination: 'KSFO'),
],
```
