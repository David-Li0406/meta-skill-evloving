# Offline-First Architecture

Building EFB applications that work reliably without network connectivity.

## Core Principles

1. **All data available offline** - Aviation data must work without internet
2. **Local-first** - Read from local database, sync when connected
3. **Graceful degradation** - App remains functional if sync fails
4. **Background sync** - Update data without blocking UI

## Data Storage Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
├─────────────────────────────────────────────────────────────┤
│   Repository (decides: local cache vs remote fetch)         │
├────────────────────────┬────────────────────────────────────┤
│    Local Data Source   │       Remote Data Source           │
│       (SQLite)         │          (REST API)                │
├────────────────────────┼────────────────────────────────────┤
│   • Aviation database  │    • Weather API                   │
│   • Chart tiles        │    • TFR updates                   │
│   • User preferences   │    • NOTAM service                 │
│   • Flight plans       │    • Sync service                  │
│   • Track logs         │                                    │
└────────────────────────┴────────────────────────────────────┘
```

## SQLite Setup

### Database Initialization

```dart
import 'package:sqlite3_flutter_libs/sqlite3_flutter_libs.dart';
import 'package:sqlite3/sqlite3.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as p;

class DatabaseService {
  Database? _db;

  Future<Database> get database async {
    if (_db != null) return _db!;
    _db = await _initDatabase();
    return _db!;
  }

  Future<Database> _initDatabase() async {
    // Get platform-specific database path
    final dir = await getApplicationDocumentsDirectory();
    final path = p.join(dir.path, 'aviation.db');

    // Open database
    final db = sqlite3.open(path);

    // Enable foreign keys
    db.execute('PRAGMA foreign_keys = ON');

    // Run migrations
    await _runMigrations(db);

    return db;
  }

  Future<void> _runMigrations(Database db) async {
    final version = db.select('PRAGMA user_version').first['user_version'] as int;

    if (version < 1) {
      // Initial schema
      db.execute('''
        CREATE TABLE airports (
          id TEXT PRIMARY KEY,
          name TEXT NOT NULL,
          icao_id TEXT,
          latitude REAL NOT NULL,
          longitude REAL NOT NULL,
          elevation_ft REAL,
          created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
      ''');

      db.execute('CREATE INDEX idx_airports_coords ON airports(latitude, longitude)');

      db.execute('PRAGMA user_version = 1');
    }

    // Add more migrations as needed
    if (version < 2) {
      // Migration 2...
    }
  }

  void close() {
    _db?.dispose();
    _db = null;
  }
}
```

### Repository with Offline Support

```dart
class AirportRepositoryImpl implements AirportRepository {
  final AirportLocalDataSource localDataSource;
  final AirportRemoteDataSource remoteDataSource;
  final NetworkInfo networkInfo;

  AirportRepositoryImpl({
    required this.localDataSource,
    required this.remoteDataSource,
    required this.networkInfo,
  });

  @override
  Future<Either<Failure, List<Airport>>> getNearbyAirports(
    double lat, double lon, double radiusNm,
  ) async {
    // Always use local data for aviation info
    try {
      final airports = await localDataSource.getNearbyAirports(lat, lon, radiusNm);
      return Right(airports);
    } on CacheException catch (e) {
      return Left(CacheFailure(e.message));
    }
  }

  @override
  Future<Either<Failure, Airport>> getAirportDetails(String id) async {
    try {
      // First try local
      final local = await localDataSource.getAirport(id);
      return Right(local);
    } on CacheException {
      // If not found locally and online, try remote
      if (await networkInfo.isConnected) {
        try {
          final remote = await remoteDataSource.getAirport(id);
          await localDataSource.cacheAirport(remote);
          return Right(remote);
        } on ServerException catch (e) {
          return Left(ServerFailure(e.message));
        }
      }
      return Left(CacheFailure('Airport not found'));
    }
  }
}
```

## Weather Data Caching

Weather data needs a time-based cache strategy:

```dart
class WeatherCache {
  final Database db;
  final Duration maxAge;

  WeatherCache({
    required this.db,
    this.maxAge = const Duration(hours: 1),
  });

  Future<Metar?> getMetar(String stationId) async {
    final result = db.select('''
      SELECT * FROM metar_cache
      WHERE station_id = ?
      AND datetime(fetched_at) > datetime('now', '-1 hour')
      ORDER BY fetched_at DESC
      LIMIT 1
    ''', [stationId]);

    if (result.isEmpty) return null;

    return Metar.fromMap(result.first);
  }

  Future<void> cacheMetar(Metar metar) async {
    db.execute('''
      INSERT OR REPLACE INTO metar_cache (
        station_id, raw_text, observed_at, fetched_at, data_json
      ) VALUES (?, ?, ?, datetime('now'), ?)
    ''', [
      metar.stationId,
      metar.rawText,
      metar.observedAt.toIso8601String(),
      jsonEncode(metar.toJson()),
    ]);
  }

  Future<void> pruneOldData() async {
    db.execute('''
      DELETE FROM metar_cache
      WHERE datetime(fetched_at) < datetime('now', '-24 hours')
    ''');
  }
}
```

## MBTiles for Offline Charts

```dart
class OfflineChartManager {
  final String chartsDirectory;

  OfflineChartManager({required this.chartsDirectory});

  Future<List<ChartPackage>> getAvailableCharts() async {
    final dir = Directory(chartsDirectory);
    if (!await dir.exists()) return [];

    final packages = <ChartPackage>[];

    await for (final file in dir.list()) {
      if (file.path.endsWith('.mbtiles')) {
        final package = await _loadChartMetadata(file.path);
        if (package != null) {
          packages.add(package);
        }
      }
    }

    return packages;
  }

  Future<ChartPackage?> _loadChartMetadata(String path) async {
    try {
      final db = sqlite3.open(path);
      final metadata = db.select('SELECT name, value FROM metadata');

      final map = <String, String>{};
      for (final row in metadata) {
        map[row['name'] as String] = row['value'] as String;
      }

      db.dispose();

      return ChartPackage(
        path: path,
        name: map['name'] ?? 'Unknown',
        description: map['description'] ?? '',
        bounds: _parseBounds(map['bounds']),
        minZoom: int.tryParse(map['minzoom'] ?? '') ?? 0,
        maxZoom: int.tryParse(map['maxzoom'] ?? '') ?? 18,
        format: map['format'] ?? 'png',
      );
    } catch (e) {
      return null;
    }
  }

  Future<void> downloadChart(String url, String name) async {
    // Download in background with progress
    final response = await http.Client().send(
      http.Request('GET', Uri.parse(url)),
    );

    final total = response.contentLength ?? 0;
    var received = 0;

    final file = File('$chartsDirectory/$name.mbtiles');
    final sink = file.openWrite();

    await for (final chunk in response.stream) {
      sink.add(chunk);
      received += chunk.length;

      // Report progress
      final progress = total > 0 ? received / total : 0.0;
      _progressController.add(DownloadProgress(name, progress));
    }

    await sink.close();
  }
}
```

## Sync Manager

```dart
class SyncManager {
  final DatabaseService database;
  final ApiClient api;
  final NetworkInfo networkInfo;

  final _syncStatusController = StreamController<SyncStatus>.broadcast();
  Stream<SyncStatus> get syncStatus => _syncStatusController.stream;

  Future<void> syncAll() async {
    if (!await networkInfo.isConnected) {
      _syncStatusController.add(SyncStatus.offline);
      return;
    }

    _syncStatusController.add(SyncStatus.syncing);

    try {
      // Sync in order of priority
      await _syncAviationData();
      await _syncWeather();
      await _syncTfrs();
      await _syncNotams();

      _syncStatusController.add(SyncStatus.complete);
    } catch (e) {
      _syncStatusController.add(SyncStatus.error);
    }
  }

  Future<void> _syncAviationData() async {
    // Check if new AIRAC cycle available
    final currentCycle = await database.getCurrentCycle();
    final latestCycle = await api.getLatestCycle();

    if (latestCycle != currentCycle) {
      // Download new data package
      await _downloadDataPackage(latestCycle);
    }
  }

  Future<void> _syncWeather() async {
    // Get list of favorited airports
    final favorites = await database.getFavoriteAirports();

    // Fetch weather for each
    for (final airport in favorites) {
      try {
        final metar = await api.getMetar(airport.id);
        await database.cacheMetar(metar);

        final taf = await api.getTaf(airport.id);
        await database.cacheTaf(taf);
      } catch (e) {
        // Continue with other airports
      }
    }
  }
}
```

## Background Sync

```dart
// Using workmanager for background tasks
void callbackDispatcher() {
  Workmanager().executeTask((task, inputData) async {
    switch (task) {
      case 'syncWeather':
        await _backgroundSyncWeather();
        return true;
      case 'syncTfrs':
        await _backgroundSyncTfrs();
        return true;
      default:
        return false;
    }
  });
}

Future<void> setupBackgroundSync() async {
  await Workmanager().initialize(callbackDispatcher);

  // Sync weather every 30 minutes
  await Workmanager().registerPeriodicTask(
    'weatherSync',
    'syncWeather',
    frequency: const Duration(minutes: 30),
    constraints: Constraints(networkType: NetworkType.connected),
  );

  // Sync TFRs every hour
  await Workmanager().registerPeriodicTask(
    'tfrSync',
    'syncTfrs',
    frequency: const Duration(hours: 1),
    constraints: Constraints(networkType: NetworkType.connected),
  );
}
```

## Data Freshness Indicator

```dart
class DataFreshnessWidget extends StatelessWidget {
  final DateTime? lastSync;
  final String dataType;

  const DataFreshnessWidget({
    super.key,
    required this.lastSync,
    required this.dataType,
  });

  @override
  Widget build(BuildContext context) {
    if (lastSync == null) {
      return const Chip(
        label: Text('No data'),
        backgroundColor: Colors.red,
      );
    }

    final age = DateTime.now().difference(lastSync!);

    Color color;
    String text;

    if (age.inMinutes < 30) {
      color = Colors.green;
      text = 'Current';
    } else if (age.inHours < 2) {
      color = Colors.orange;
      text = '${age.inMinutes}m ago';
    } else {
      color = Colors.red;
      text = '${age.inHours}h ago';
    }

    return Chip(
      label: Text('$dataType: $text'),
      backgroundColor: color.withOpacity(0.2),
      side: BorderSide(color: color),
    );
  }
}
```
