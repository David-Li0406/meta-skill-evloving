# BLoC State Management Patterns

Best practices for using BLoC pattern in EFB applications.

## Event-Driven Architecture

```
┌────────────┐    Event    ┌──────────────┐    State    ┌────────────┐
│   Widget   │ ─────────▶  │     BLoC     │ ─────────▶  │   Widget   │
│            │ ◀───────────│              │             │  (rebuild) │
└────────────┘    State    └──────────────┘             └────────────┘
```

## Basic BLoC Structure

### Events

```dart
// airport_event.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'airport_event.freezed.dart';

@freezed
class AirportEvent with _$AirportEvent {
  // Load airports near a location
  const factory AirportEvent.loadNearby({
    required double latitude,
    required double longitude,
    @Default(50.0) double radiusNm,
  }) = LoadNearbyAirports;

  // Search airports by query
  const factory AirportEvent.search({
    required String query,
  }) = SearchAirports;

  // Select an airport for details
  const factory AirportEvent.select({
    required String airportId,
  }) = SelectAirport;

  // Clear selection
  const factory AirportEvent.clearSelection() = ClearSelection;

  // Refresh data
  const factory AirportEvent.refresh() = RefreshAirports;
}
```

### States

```dart
// airport_state.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'airport_state.freezed.dart';

@freezed
class AirportState with _$AirportState {
  const factory AirportState({
    @Default([]) List<Airport> airports,
    @Default([]) List<Airport> searchResults,
    Airport? selectedAirport,
    @Default(false) bool isLoading,
    @Default(false) bool isSearching,
    String? error,
    double? lastLatitude,
    double? lastLongitude,
  }) = _AirportState;

  const AirportState._();

  bool get hasSelection => selectedAirport != null;
  bool get hasError => error != null;
  bool get hasAirports => airports.isNotEmpty;
}
```

### BLoC Implementation

```dart
// airport_bloc.dart
import 'package:flutter_bloc/flutter_bloc.dart';

class AirportBloc extends Bloc<AirportEvent, AirportState> {
  final GetNearbyAirports getNearbyAirports;
  final SearchAirports searchAirportsUseCase;
  final GetAirportDetails getAirportDetails;

  AirportBloc({
    required this.getNearbyAirports,
    required this.searchAirportsUseCase,
    required this.getAirportDetails,
  }) : super(const AirportState()) {
    on<LoadNearbyAirports>(_onLoadNearby);
    on<SearchAirports>(_onSearch);
    on<SelectAirport>(_onSelect);
    on<ClearSelection>(_onClearSelection);
    on<RefreshAirports>(_onRefresh);
  }

  Future<void> _onLoadNearby(
    LoadNearbyAirports event,
    Emitter<AirportState> emit,
  ) async {
    emit(state.copyWith(
      isLoading: true,
      error: null,
      lastLatitude: event.latitude,
      lastLongitude: event.longitude,
    ));

    final result = await getNearbyAirports(NearbyParams(
      latitude: event.latitude,
      longitude: event.longitude,
      radiusNm: event.radiusNm,
    ));

    result.fold(
      (failure) => emit(state.copyWith(
        isLoading: false,
        error: failure.message,
      )),
      (airports) => emit(state.copyWith(
        isLoading: false,
        airports: airports,
      )),
    );
  }

  Future<void> _onSearch(
    SearchAirports event,
    Emitter<AirportState> emit,
  ) async {
    if (event.query.isEmpty) {
      emit(state.copyWith(searchResults: [], isSearching: false));
      return;
    }

    emit(state.copyWith(isSearching: true));

    final result = await searchAirportsUseCase(event.query);

    result.fold(
      (failure) => emit(state.copyWith(
        isSearching: false,
        error: failure.message,
      )),
      (airports) => emit(state.copyWith(
        isSearching: false,
        searchResults: airports,
      )),
    );
  }

  Future<void> _onSelect(
    SelectAirport event,
    Emitter<AirportState> emit,
  ) async {
    emit(state.copyWith(isLoading: true));

    final result = await getAirportDetails(event.airportId);

    result.fold(
      (failure) => emit(state.copyWith(
        isLoading: false,
        error: failure.message,
      )),
      (airport) => emit(state.copyWith(
        isLoading: false,
        selectedAirport: airport,
      )),
    );
  }

  void _onClearSelection(
    ClearSelection event,
    Emitter<AirportState> emit,
  ) {
    emit(state.copyWith(selectedAirport: null));
  }

  Future<void> _onRefresh(
    RefreshAirports event,
    Emitter<AirportState> emit,
  ) async {
    if (state.lastLatitude != null && state.lastLongitude != null) {
      add(LoadNearbyAirports(
        latitude: state.lastLatitude!,
        longitude: state.lastLongitude!,
      ));
    }
  }
}
```

## Using BLoCs in Widgets

### Provider Setup

```dart
// main.dart or feature widget
BlocProvider(
  create: (context) => AirportBloc(
    getNearbyAirports: sl(),
    searchAirportsUseCase: sl(),
    getAirportDetails: sl(),
  ),
  child: const AirportPage(),
)
```

### Consuming State

```dart
class AirportPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocBuilder<AirportBloc, AirportState>(
      builder: (context, state) {
        if (state.isLoading) {
          return const LoadingIndicator();
        }

        if (state.hasError) {
          return ErrorWidget(
            message: state.error!,
            onRetry: () => context.read<AirportBloc>().add(RefreshAirports()),
          );
        }

        return AirportList(
          airports: state.airports,
          onSelect: (airport) {
            context.read<AirportBloc>().add(SelectAirport(airport.id));
          },
        );
      },
    );
  }
}
```

### Selective Rebuilds

```dart
// Only rebuild when specific parts of state change
BlocSelector<AirportBloc, AirportState, List<Airport>>(
  selector: (state) => state.airports,
  builder: (context, airports) {
    return AirportList(airports: airports);
  },
)

// Listen without rebuilding
BlocListener<AirportBloc, AirportState>(
  listenWhen: (previous, current) =>
    previous.selectedAirport != current.selectedAirport,
  listener: (context, state) {
    if (state.selectedAirport != null) {
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => AirportDetailPage(airport: state.selectedAirport!),
        ),
      );
    }
  },
  child: ...,
)
```

## Multi-BLoC Communication

### Using BlocListener for Cross-BLoC Events

```dart
class MapPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MultiBlocListener(
      listeners: [
        // When GPS position changes, load nearby airports
        BlocListener<GpsBloc, GpsState>(
          listenWhen: (previous, current) =>
            previous.position != current.position,
          listener: (context, state) {
            if (state.position != null) {
              context.read<AirportBloc>().add(LoadNearbyAirports(
                latitude: state.position!.latitude,
                longitude: state.position!.longitude,
              ));
            }
          },
        ),

        // When weather loads, update map overlays
        BlocListener<WeatherBloc, WeatherState>(
          listener: (context, state) {
            if (state.hasRadar) {
              context.read<MapBloc>().add(UpdateRadarOverlay(state.radar));
            }
          },
        ),
      ],
      child: const MapView(),
    );
  }
}
```

## Cubit for Simpler State

For simple state without complex events:

```dart
class ThemeCubit extends Cubit<ThemeMode> {
  ThemeCubit() : super(ThemeMode.system);

  void setDayMode() => emit(ThemeMode.light);
  void setNightMode() => emit(ThemeMode.dark);
  void setAutoMode() => emit(ThemeMode.system);

  void toggleMode() {
    switch (state) {
      case ThemeMode.light:
        emit(ThemeMode.dark);
        break;
      case ThemeMode.dark:
        emit(ThemeMode.light);
        break;
      case ThemeMode.system:
        emit(ThemeMode.light);
        break;
    }
  }
}
```

## Testing BLoCs

```dart
void main() {
  group('AirportBloc', () {
    late AirportBloc bloc;
    late MockGetNearbyAirports mockGetNearbyAirports;

    setUp(() {
      mockGetNearbyAirports = MockGetNearbyAirports();
      bloc = AirportBloc(getNearbyAirports: mockGetNearbyAirports);
    });

    tearDown(() => bloc.close());

    blocTest<AirportBloc, AirportState>(
      'emits [loading, loaded] when LoadNearbyAirports succeeds',
      build: () {
        when(() => mockGetNearbyAirports(any()))
          .thenAnswer((_) async => Right(testAirports));
        return bloc;
      },
      act: (bloc) => bloc.add(LoadNearbyAirports(
        latitude: 37.7749,
        longitude: -122.4194,
      )),
      expect: () => [
        AirportState(isLoading: true),
        AirportState(airports: testAirports),
      ],
    );
  });
}
```
