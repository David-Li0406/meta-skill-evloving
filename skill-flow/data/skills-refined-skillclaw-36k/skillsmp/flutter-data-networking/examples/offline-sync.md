# Offline-First Data Synchronization

Complete implementation of offline-first architecture with data synchronization and conflict resolution.

## Overview

This example demonstrates a production-ready offline-first implementation that:

- Works fully offline with local database
- Syncs data automatically when online
- Queues write operations while offline
- Resolves conflicts intelligently
- Uses repository pattern for data abstraction
- Provides real-time connectivity status

## Architecture

```
┌─────────────┐
│ Application │
└──────┬──────┘
       │
┌──────▼──────────┐
│   Repository    │  (Single source of truth)
└──────┬──────────┘
       │
   ┌───┴────┐
   │        │
┌──▼──┐  ┌─▼────┐
│Local│  │Remote│
│ DB  │  │ API  │
└─────┘  └──────┘
```

## Dependencies

```yaml
dependencies:
  # Database
  drift: ^2.14.0
  sqlite3_flutter_libs: ^0.5.0
  path_provider: ^2.1.1
  path: ^1.8.3

  # Networking
  dio: ^5.4.0

  # Connectivity
  connectivity_plus: ^5.0.0

  # State management
  riverpod: ^2.4.9
  flutter_riverpod: ^2.4.9

  # Background sync
  workmanager: ^0.5.1

dev_dependencies:
  drift_dev: ^2.14.0
  build_runner: ^2.4.7
```

## Database Schema

Define local database with Drift:

```dart
// lib/database/database.dart
import 'package:drift/drift.dart';
import 'package:drift/native.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as p;
import 'dart:io';

part 'database.g.dart';

// Users table
class Users extends Table {
  TextColumn get id => text()();
  TextColumn get name => text()();
  TextColumn get email => text()();
  TextColumn get bio => text().nullable()();
  DateTimeColumn get createdAt => dateTime()();
  DateTimeColumn get updatedAt => dateTime()();
  BoolColumn get isDirty => boolean().withDefault(const Constant(false))();
  DateTimeColumn get lastSyncedAt => dateTime().nullable()();

  @override
  Set<Column> get primaryKey => {id};
}

// Pending operations queue
class PendingOperations extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get type => text()(); // 'create', 'update', 'delete'
  TextColumn get entityType => text()(); // 'user', 'post', etc.
  TextColumn get entityId => text()();
  TextColumn get data => text()(); // JSON data
  DateTimeColumn get createdAt => dateTime()();
  IntColumn get retryCount => integer().withDefault(const Constant(0))();
}

@DriftDatabase(tables: [Users, PendingOperations])
class AppDatabase extends _$AppDatabase {
  AppDatabase() : super(_openConnection());

  @override
  int get schemaVersion => 1;

  static LazyDatabase _openConnection() {
    return LazyDatabase(() async {
      final dbFolder = await getApplicationDocumentsDirectory();
      final file = File(p.join(dbFolder.path, 'app.db'));
      return NativeDatabase(file);
    });
  }
}
```

## Connectivity Service

Monitor network connectivity:

```dart
// lib/services/connectivity_service.dart
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:riverpod/riverpod.dart';

class ConnectivityService {
  final Connectivity _connectivity = Connectivity();

  Stream<bool> get isConnected => _connectivity.onConnectivityChanged.map(
        (result) => result != ConnectivityResult.none,
      );

  Future<bool> checkConnectivity() async {
    final result = await _connectivity.checkConnectivity();
    return result != ConnectivityResult.none;
  }
}

final connectivityServiceProvider = Provider((ref) => ConnectivityService());

final connectivityStreamProvider = StreamProvider<bool>((ref) {
  final service = ref.watch(connectivityServiceProvider);
  return service.isConnected;
});
```

## Sync Manager

Manage synchronization operations:

```dart
// lib/services/sync_manager.dart
import 'package:dio/dio.dart';

enum SyncStatus {
  idle,
  syncing,
  success,
  error,
}

class SyncManager {
  final AppDatabase _db;
  final Dio _dio;
  final ConnectivityService _connectivity;

  SyncManager(this._db, this._dio, this._connectivity);

  Future<void> syncAll() async {
    // Check connectivity
    final isOnline = await _connectivity.checkConnectivity();
    if (!isOnline) {
      print('Cannot sync: No internet connection');
      return;
    }

    try {
      // 1. Push pending local changes
      await _pushPendingOperations();

      // 2. Pull remote changes
      await _pullRemoteChanges();

      print('Sync completed successfully');
    } catch (e) {
      print('Sync error: $e');
      rethrow;
    }
  }

  Future<void> _pushPendingOperations() async {
    final operations = await _db.select(_db.pendingOperations).get();

    for (final operation in operations) {
      try {
        await _executePendingOperation(operation);

        // Remove from queue on success
        await (_db.delete(_db.pendingOperations)
              ..where((t) => t.id.equals(operation.id)))
            .go();

        print('Pushed operation: ${operation.type} ${operation.entityType}');
      } catch (e) {
        // Increment retry count
        await (_db.update(_db.pendingOperations)
              ..where((t) => t.id.equals(operation.id)))
            .write(
          PendingOperationsCompanion(
            retryCount: Value(operation.retryCount + 1),
          ),
        );

        // Remove after 5 failed attempts
        if (operation.retryCount >= 5) {
          await (_db.delete(_db.pendingOperations)
                ..where((t) => t.id.equals(operation.id)))
              .go();
          print('Discarded operation after 5 retries');
        }
      }
    }
  }

  Future<void> _executePendingOperation(PendingOperation operation) async {
    final data = jsonDecode(operation.data);

    switch (operation.type) {
      case 'create':
        await _dio.post(
          '/${operation.entityType}s',
          data: data,
        );
        break;

      case 'update':
        await _dio.patch(
          '/${operation.entityType}s/${operation.entityId}',
          data: data,
        );
        break;

      case 'delete':
        await _dio.delete(
          '/${operation.entityType}s/${operation.entityId}',
        );
        break;
    }
  }

  Future<void> _pullRemoteChanges() async {
    // Get last sync timestamp
    final lastSync = await _getLastSyncTimestamp();

    // Fetch changes since last sync
    final response = await _dio.get(
      '/users',
      queryParameters: {
        if (lastSync != null) 'updated_after': lastSync.toIso8601String(),
      },
    );

    final users = (response.data as List)
        .map((json) => User.fromJson(json))
        .toList();

    // Update local database
    for (final user in users) {
      await _db.into(_db.users).insertOnConflictUpdate(
            UsersCompanion(
              id: Value(user.id),
              name: Value(user.name),
              email: Value(user.email),
              bio: Value(user.bio),
              createdAt: Value(user.createdAt),
              updatedAt: Value(user.updatedAt),
              isDirty: const Value(false),
              lastSyncedAt: Value(DateTime.now()),
            ),
          );
    }

    print('Pulled ${users.length} users from server');
  }

  Future<DateTime?> _getLastSyncTimestamp() async {
    final result = await (_db.select(_db.users)
          ..orderBy([(t) => OrderingTerm.desc(t.lastSyncedAt)])
          ..limit(1))
        .getSingleOrNull();

    return result?.lastSyncedAt;
  }
}

final syncManagerProvider = Provider((ref) {
  final db = ref.watch(databaseProvider);
  final dio = ref.watch(dioProvider);
  final connectivity = ref.watch(connectivityServiceProvider);

  return SyncManager(db, dio, connectivity);
});
```

## Repository with Offline Support

Implement repository that works offline:

```dart
// lib/repositories/offline_user_repository.dart
import 'package:rxdart/rxdart.dart';

class OfflineUserRepository {
  final AppDatabase _db;
  final Dio _dio;
  final ConnectivityService _connectivity;
  final SyncManager _syncManager;

  OfflineUserRepository(
    this._db,
    this._dio,
    this._connectivity,
    this._syncManager,
  );

  // Get single user (cache-first)
  Future<User?> getUser(String id) async {
    // Try local database first
    final localUser = await (_db.select(_db.users)
          ..where((t) => t.id.equals(id)))
        .getSingleOrNull();

    if (localUser != null) {
      // Return cached data immediately
      final user = _mapToUser(localUser);

      // Fetch fresh data in background if online
      _fetchUserInBackground(id);

      return user;
    }

    // Not in cache, fetch from server
    return await _fetchUser(id);
  }

  // Watch user (stream of updates)
  Stream<User?> watchUser(String id) {
    return (_db.select(_db.users)..where((t) => t.id.equals(id)))
        .watchSingleOrNull()
        .map((data) => data != null ? _mapToUser(data) : null);
  }

  // Get all users (cache-first)
  Stream<List<User>> watchUsers() {
    return _db.select(_db.users).watch().map(
          (list) => list.map(_mapToUser).toList(),
        );
  }

  // Create user
  Future<User> createUser({
    required String name,
    required String email,
  }) async {
    final id = Uuid().v4();
    final now = DateTime.now();

    final user = User(
      id: id,
      name: name,
      email: email,
      createdAt: now,
      updatedAt: now,
    );

    // Save to local database immediately
    await _db.into(_db.users).insert(
          UsersCompanion(
            id: Value(id),
            name: Value(name),
            email: Value(email),
            createdAt: Value(now),
            updatedAt: Value(now),
            isDirty: const Value(true),
          ),
        );

    // Queue operation for sync
    await _queueOperation(
      type: 'create',
      entityType: 'user',
      entityId: id,
      data: {'name': name, 'email': email},
    );

    // Trigger sync if online
    _syncManager.syncAll().catchError((e) {
      print('Background sync failed: $e');
    });

    return user;
  }

  // Update user
  Future<User> updateUser(
    String id, {
    String? name,
    String? bio,
  }) async {
    final now = DateTime.now();

    // Update local database
    await (_db.update(_db.users)..where((t) => t.id.equals(id))).write(
      UsersCompanion(
        name: name != null ? Value(name) : const Value.absent(),
        bio: bio != null ? Value(bio) : const Value.absent(),
        updatedAt: Value(now),
        isDirty: const Value(true),
      ),
    );

    // Queue operation
    await _queueOperation(
      type: 'update',
      entityType: 'user',
      entityId: id,
      data: {
        if (name != null) 'name': name,
        if (bio != null) 'bio': bio,
      },
    );

    // Trigger sync
    _syncManager.syncAll().catchError((e) {});

    // Return updated user
    final updatedUser = await getUser(id);
    return updatedUser!;
  }

  // Delete user
  Future<void> deleteUser(String id) async {
    // Mark as deleted locally (soft delete)
    await (_db.delete(_db.users)..where((t) => t.id.equals(id))).go();

    // Queue operation
    await _queueOperation(
      type: 'delete',
      entityType: 'user',
      entityId: id,
      data: {},
    );

    // Trigger sync
    _syncManager.syncAll().catchError((e) {});
  }

  // Private methods

  Future<User?> _fetchUser(String id) async {
    final isOnline = await _connectivity.checkConnectivity();

    if (!isOnline) {
      return null;
    }

    try {
      final response = await _dio.get('/users/$id');
      final user = User.fromJson(response.data);

      // Cache in local database
      await _db.into(_db.users).insertOnConflictUpdate(
            UsersCompanion(
              id: Value(user.id),
              name: Value(user.name),
              email: Value(user.email),
              bio: Value(user.bio),
              createdAt: Value(user.createdAt),
              updatedAt: Value(user.updatedAt),
              isDirty: const Value(false),
              lastSyncedAt: Value(DateTime.now()),
            ),
          );

      return user;
    } catch (e) {
      print('Error fetching user: $e');
      return null;
    }
  }

  void _fetchUserInBackground(String id) {
    _fetchUser(id).catchError((e) {
      print('Background fetch failed: $e');
    });
  }

  Future<void> _queueOperation({
    required String type,
    required String entityType,
    required String entityId,
    required Map<String, dynamic> data,
  }) async {
    await _db.into(_db.pendingOperations).insert(
          PendingOperationsCompanion(
            type: Value(type),
            entityType: Value(entityType),
            entityId: Value(entityId),
            data: Value(jsonEncode(data)),
            createdAt: Value(DateTime.now()),
            retryCount: const Value(0),
          ),
        );
  }

  User _mapToUser(UserData data) {
    return User(
      id: data.id,
      name: data.name,
      email: data.email,
      bio: data.bio,
      createdAt: data.createdAt,
      updatedAt: data.updatedAt,
    );
  }
}

final offlineUserRepositoryProvider = Provider((ref) {
  final db = ref.watch(databaseProvider);
  final dio = ref.watch(dioProvider);
  final connectivity = ref.watch(connectivityServiceProvider);
  final syncManager = ref.watch(syncManagerProvider);

  return OfflineUserRepository(db, dio, connectivity, syncManager);
});
```

## Background Sync with WorkManager

Schedule periodic background sync:

```dart
// lib/services/background_sync.dart
import 'package:workmanager/workmanager.dart';

@pragma('vm:entry-point')
void callbackDispatcher() {
  Workmanager().executeTask((task, inputData) async {
    try {
      // Initialize dependencies
      final db = AppDatabase();
      final dio = Dio(BaseOptions(baseUrl: 'https://api.example.com'));
      final connectivity = ConnectivityService();
      final syncManager = SyncManager(db, dio, connectivity);

      // Perform sync
      await syncManager.syncAll();

      return true;
    } catch (e) {
      print('Background sync failed: $e');
      return false;
    }
  });
}

class BackgroundSyncService {
  static Future<void> initialize() async {
    await Workmanager().initialize(
      callbackDispatcher,
      isInDebugMode: kDebugMode,
    );

    // Register periodic sync task (runs every 15 minutes)
    await Workmanager().registerPeriodicTask(
      'sync-task',
      'syncData',
      frequency: const Duration(minutes: 15),
      constraints: Constraints(
        networkType: NetworkType.connected,
      ),
    );
  }

  static Future<void> cancelAll() async {
    await Workmanager().cancelAll();
  }
}

// Initialize in main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await BackgroundSyncService.initialize();
  runApp(MyApp());
}
```

## UI with Offline Indicator

Show connectivity status to users:

```dart
// lib/screens/user_list_screen.dart
class UserListScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isOnline = ref.watch(connectivityStreamProvider);
    final usersStream = ref.watch(offlineUserRepositoryProvider).watchUsers();

    return Scaffold(
      appBar: AppBar(
        title: Text('Users'),
        actions: [
          // Connectivity indicator
          isOnline.when(
            data: (online) => Icon(
              online ? Icons.cloud_done : Icons.cloud_off,
              color: online ? Colors.green : Colors.grey,
            ),
            loading: () => SizedBox.shrink(),
            error: (_, __) => Icon(Icons.error, color: Colors.red),
          ),
          // Sync button
          IconButton(
            icon: Icon(Icons.sync),
            onPressed: () async {
              final syncManager = ref.read(syncManagerProvider);
              try {
                await syncManager.syncAll();
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Sync completed')),
                );
              } catch (e) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Sync failed: $e')),
                );
              }
            },
          ),
        ],
      ),
      body: Column(
        children: [
          // Offline banner
          isOnline.when(
            data: (online) => !online
                ? Container(
                    color: Colors.orange,
                    padding: EdgeInsets.all(8),
                    child: Row(
                      children: [
                        Icon(Icons.cloud_off, color: Colors.white),
                        SizedBox(width: 8),
                        Text(
                          'Offline - Changes will sync when connected',
                          style: TextStyle(color: Colors.white),
                        ),
                      ],
                    ),
                  )
                : SizedBox.shrink(),
            loading: () => SizedBox.shrink(),
            error: (_, __) => SizedBox.shrink(),
          ),
          // User list
          Expanded(
            child: StreamBuilder<List<User>>(
              stream: usersStream,
              builder: (context, snapshot) {
                if (!snapshot.hasData) {
                  return Center(child: CircularProgressIndicator());
                }

                final users = snapshot.data!;

                if (users.isEmpty) {
                  return Center(child: Text('No users yet'));
                }

                return ListView.builder(
                  itemCount: users.length,
                  itemBuilder: (context, index) {
                    final user = users[index];
                    return ListTile(
                      title: Text(user.name),
                      subtitle: Text(user.email),
                      trailing: IconButton(
                        icon: Icon(Icons.delete),
                        onPressed: () async {
                          final repo = ref.read(offlineUserRepositoryProvider);
                          await repo.deleteUser(user.id);
                        },
                      ),
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        child: Icon(Icons.add),
        onPressed: () {
          // Show create user dialog
          _showCreateUserDialog(context, ref);
        },
      ),
    );
  }

  void _showCreateUserDialog(BuildContext context, WidgetRef ref) {
    // Implementation details...
  }
}
```

## Conflict Resolution

Handle conflicts when local and remote data diverge:

```dart
enum ConflictStrategy {
  lastWriteWins,
  serverWins,
  clientWins,
  merge,
}

class ConflictResolver {
  Future<User> resolveConflict(
    User localUser,
    User remoteUser,
    ConflictStrategy strategy,
  ) async {
    switch (strategy) {
      case ConflictStrategy.lastWriteWins:
        return localUser.updatedAt.isAfter(remoteUser.updatedAt)
            ? localUser
            : remoteUser;

      case ConflictStrategy.serverWins:
        return remoteUser;

      case ConflictStrategy.clientWins:
        return localUser;

      case ConflictStrategy.merge:
        // Custom merge logic
        return User(
          id: localUser.id,
          name: localUser.name, // Keep local name
          email: remoteUser.email, // Use server email
          bio: localUser.bio ?? remoteUser.bio,
          createdAt: remoteUser.createdAt,
          updatedAt: DateTime.now(),
        );
    }
  }
}
```

## Testing

Test offline functionality:

```dart
import 'package:test/test.dart';

void main() {
  group('OfflineUserRepository', () {
    test('creates user offline and syncs when online', () async {
      final repository = OfflineUserRepository(/* ... */);

      // Create user while offline
      final user = await repository.createUser(
        name: 'John Doe',
        email: 'john@example.com',
      );

      expect(user.name, 'John Doe');

      // Verify queued operation
      final operations = await db.select(db.pendingOperations).get();
      expect(operations.length, 1);
      expect(operations.first.type, 'create');

      // Simulate going online
      await syncManager.syncAll();

      // Verify operation cleared
      final remainingOps = await db.select(db.pendingOperations).get();
      expect(remainingOps, isEmpty);
    });
  });
}
```

## Best Practices

1. **Cache-First**: Always return cached data immediately, then fetch updates
2. **Optimistic Updates**: Update UI instantly, sync in background
3. **Operation Queue**: Queue all write operations for reliable syncing
4. **Conflict Resolution**: Choose appropriate strategy for your domain
5. **Background Sync**: Use WorkManager for periodic background syncing
6. **Error Handling**: Gracefully handle sync failures with retries
7. **UI Feedback**: Show connectivity status and sync progress
8. **Testing**: Test offline scenarios thoroughly

## Conclusion

This offline-first implementation provides a robust foundation for Flutter apps that work reliably regardless of connectivity. Users can continue working offline with all changes automatically synced when connectivity is restored.
