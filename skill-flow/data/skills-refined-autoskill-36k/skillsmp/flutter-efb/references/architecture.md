# Clean Architecture for EFB

Flutter EFB application architecture following Clean Architecture principles.

## Layer Overview

```
┌────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Screens    │  │    BLoCs     │  │   Widgets    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
├────────────────────────────────────────────────────────────┤
│                      DOMAIN LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Entities   │  │  Use Cases   │  │ Repositories │      │
│  │              │  │              │  │ (Interfaces) │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
├────────────────────────────────────────────────────────────┤
│                       DATA LAYER                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │    Models    │  │ Data Sources │  │  Repository  │      │
│  │              │  │              │  │   Impl       │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
lib/
├── core/
│   ├── constants/
│   │   ├── app_constants.dart
│   │   └── aviation_constants.dart
│   ├── error/
│   │   ├── exceptions.dart
│   │   └── failures.dart
│   ├── usecases/
│   │   └── usecase.dart
│   ├── utils/
│   │   ├── navigation_math.dart
│   │   └── coordinate_utils.dart
│   └── di/
│       └── injection.dart
│
├── features/
│   ├── airports/
│   │   ├── data/
│   │   │   ├── datasources/
│   │   │   │   └── airport_local_datasource.dart
│   │   │   ├── models/
│   │   │   │   └── airport_model.dart
│   │   │   └── repositories/
│   │   │       └── airport_repository_impl.dart
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   └── airport.dart
│   │   │   ├── repositories/
│   │   │   │   └── airport_repository.dart
│   │   │   └── usecases/
│   │   │       ├── get_airport.dart
│   │   │       └── search_airports.dart
│   │   └── presentation/
│   │       ├── bloc/
│   │       │   ├── airport_bloc.dart
│   │       │   ├── airport_event.dart
│   │       │   └── airport_state.dart
│   │       ├── pages/
│   │       │   └── airport_detail_page.dart
│   │       └── widgets/
│   │           └── airport_card.dart
│   │
│   ├── map/
│   ├── weather/
│   ├── flight_plan/
│   └── adsb/
│
└── main.dart
```

## Entity Example

Domain entities are the core business objects.

```dart
// lib/features/airports/domain/entities/airport.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'airport.freezed.dart';

@freezed
class Airport with _$Airport {
  const factory Airport({
    required String id,
    required String name,
    required String icaoId,
    required double latitude,
    required double longitude,
    required double elevationFt,
    String? city,
    String? state,
    double? magneticVariation,
    List<Runway>? runways,
    List<Frequency>? frequencies,
  }) = _Airport;
}

@freezed
class Runway with _$Runway {
  const factory Runway({
    required String id,
    required int lengthFt,
    required int widthFt,
    required String surface,
    required int baseHeading,
    required int recipHeading,
  }) = _Runway;
}

@freezed
class Frequency with _$Frequency {
  const factory Frequency({
    required String type,
    required double frequencyMhz,
    String? name,
  }) = _Frequency;
}
```

## Repository Pattern

### Domain Interface

```dart
// lib/features/airports/domain/repositories/airport_repository.dart
import 'package:dartz/dartz.dart';

abstract class AirportRepository {
  Future<Either<Failure, Airport>> getAirport(String id);
  Future<Either<Failure, List<Airport>>> searchAirports(String query);
  Future<Either<Failure, List<Airport>>> getNearbyAirports(
    double lat, double lon, double radiusNm,
  );
  Future<Either<Failure, List<Airport>>> getAirportsWithMinRunway(
    double lat, double lon, double radiusNm, int minLengthFt,
  );
}
```

### Data Implementation

```dart
// lib/features/airports/data/repositories/airport_repository_impl.dart
class AirportRepositoryImpl implements AirportRepository {
  final AirportLocalDataSource localDataSource;

  AirportRepositoryImpl({required this.localDataSource});

  @override
  Future<Either<Failure, Airport>> getAirport(String id) async {
    try {
      final model = await localDataSource.getAirport(id);
      return Right(model.toEntity());
    } on CacheException {
      return Left(CacheFailure());
    }
  }

  @override
  Future<Either<Failure, List<Airport>>> getNearbyAirports(
    double lat, double lon, double radiusNm,
  ) async {
    try {
      final models = await localDataSource.getNearbyAirports(lat, lon, radiusNm);
      return Right(models.map((m) => m.toEntity()).toList());
    } on CacheException {
      return Left(CacheFailure());
    }
  }
}
```

## Use Cases

```dart
// lib/features/airports/domain/usecases/get_nearby_airports.dart
class GetNearbyAirports implements UseCase<List<Airport>, NearbyParams> {
  final AirportRepository repository;

  GetNearbyAirports(this.repository);

  @override
  Future<Either<Failure, List<Airport>>> call(NearbyParams params) {
    return repository.getNearbyAirports(
      params.latitude,
      params.longitude,
      params.radiusNm,
    );
  }
}

class NearbyParams {
  final double latitude;
  final double longitude;
  final double radiusNm;

  NearbyParams({
    required this.latitude,
    required this.longitude,
    this.radiusNm = 50,
  });
}
```

## BLoC Pattern

```dart
// lib/features/airports/presentation/bloc/airport_bloc.dart
class AirportBloc extends Bloc<AirportEvent, AirportState> {
  final GetNearbyAirports getNearbyAirports;
  final GetAirport getAirport;

  AirportBloc({
    required this.getNearbyAirports,
    required this.getAirport,
  }) : super(AirportInitial()) {
    on<LoadNearbyAirports>(_onLoadNearbyAirports);
    on<SelectAirport>(_onSelectAirport);
  }

  Future<void> _onLoadNearbyAirports(
    LoadNearbyAirports event,
    Emitter<AirportState> emit,
  ) async {
    emit(AirportLoading());

    final result = await getNearbyAirports(NearbyParams(
      latitude: event.latitude,
      longitude: event.longitude,
      radiusNm: event.radiusNm,
    ));

    result.fold(
      (failure) => emit(AirportError(failure.message)),
      (airports) => emit(AirportsLoaded(airports)),
    );
  }
}
```

## Dependency Injection

Using `get_it` for dependency injection:

```dart
// lib/core/di/injection.dart
final sl = GetIt.instance;

Future<void> init() async {
  // BLoCs
  sl.registerFactory(
    () => AirportBloc(
      getNearbyAirports: sl(),
      getAirport: sl(),
    ),
  );

  // Use cases
  sl.registerLazySingleton(() => GetNearbyAirports(sl()));
  sl.registerLazySingleton(() => GetAirport(sl()));

  // Repositories
  sl.registerLazySingleton<AirportRepository>(
    () => AirportRepositoryImpl(localDataSource: sl()),
  );

  // Data sources
  sl.registerLazySingleton<AirportLocalDataSource>(
    () => AirportLocalDataSourceImpl(database: sl()),
  );

  // External
  final database = await openDatabase('aviation.db');
  sl.registerLazySingleton(() => database);
}
```

## Error Handling

```dart
// lib/core/error/failures.dart
abstract class Failure {
  final String message;
  const Failure(this.message);
}

class CacheFailure extends Failure {
  const CacheFailure([String message = 'Cache error']) : super(message);
}

class NetworkFailure extends Failure {
  const NetworkFailure([String message = 'Network error']) : super(message);
}

class DatabaseFailure extends Failure {
  const DatabaseFailure([String message = 'Database error']) : super(message);
}

// lib/core/error/exceptions.dart
class CacheException implements Exception {}
class NetworkException implements Exception {}
class DatabaseException implements Exception {}
```
