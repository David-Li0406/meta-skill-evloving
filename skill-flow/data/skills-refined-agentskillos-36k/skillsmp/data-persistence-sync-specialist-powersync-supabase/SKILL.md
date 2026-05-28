---
name: Data Persistence & Sync Specialist (PowerSync + Supabase)
description: Arquitecto de bases de datos distribuidas. Especialista en esquemas SQL robustos, políticas de seguridad (RLS) y lógica "Local-First" utilizando PowerSync. Garantiza que los datos estén disponibles siempre, haya o no internet.
---

## Responsabilidad Única
Sincronización de datos, persistencia local y estrategias de conflict resolution. NO incluye arquitectura general, UI, ni lógica de negocio.

---

## Arquitectura Local-First

### Principio Fundamental
- **Datos locales primero**: Todas las operaciones se realizan contra base de datos local
- **Sincronización en background**: Sync con Supabase cuando hay conexión
- **Offline-first**: App funciona completamente sin internet
- **Eventual consistency**: Los datos convergen eventualmente

### Stack Técnico
- **PowerSync**: Motor de sincronización local-first
- **Supabase**: Backend PostgreSQL con real-time
- **SQLite**: Base de datos local (via PowerSync)

---

## Supabase Integration

### Setup y Configuración
```dart
final supabase = SupabaseClient(
  'YOUR_SUPABASE_URL',
  'YOUR_SUPABASE_ANON_KEY',
  authOptions: AuthClientOptions(
    authFlowType: AuthFlowType.pkce,
  ),
);
```

### Autenticación
```dart
// Sign in
await supabase.auth.signInWithPassword(
  email: email,
  password: password,
);

// Get current session
final session = supabase.auth.currentSession;

// Listen to auth changes
supabase.auth.onAuthStateChange.listen((data) {
  final session = data.session;
  // Handle auth state
});
```

---

## PowerSync Configuration

### Schema Definition
Definir esquema local que refleja tablas de Supabase:

```dart
const schema = Schema([
  Table('packages', [
    Column.text('id'),
    Column.text('tracking_number'),
    Column.text('customer_name'),
    Column.text('customer_phone'),
    Column.text('address'),
    Column.real('latitude'),
    Column.real('longitude'),
    Column.text('status'),
    Column.integer('delivery_attempts'),
    Column.text('route_id'),
    Column.text('photo_url'),
    Column.text('recipient_name'),
    Column.text('notes'),
    Column.integer('created_at'),
    Column.integer('updated_at'),
  ]),
  Table('routes', [
    Column.text('id'),
    Column.text('driver_id'),
    Column.text('status'),
    Column.integer('date'),
    Column.integer('created_at'),
    Column.integer('updated_at'),
  ]),
  Table('cached_addresses', [
    Column.text('id'),
    Column.text('query'),
    Column.real('latitude'),
    Column.real('longitude'),
    Column.text('full_address'),
    Column.integer('timestamp'),
  ]),
]);
```

### PowerSync Initialization
```dart
final powerSync = PowerSyncDatabase.withFactory(
  path: 'powersync.db',
  schema: schema,
  factory: PowerSyncSQLiteFactory(),
);

await powerSync.initialize();
```

### Connector Setup
```dart
class SupabasePowerSyncConnector extends PowerSyncBackendConnector {
  final SupabaseClient supabase;
  
  @override
  Future<PowerSyncCredentials?> fetchCredentials() async {
    final session = supabase.auth.currentSession;
    if (session == null) return null;
    
    return PowerSyncCredentials(
      endpoint: 'YOUR_POWERSYNC_ENDPOINT',
      token: session.accessToken,
    );
  }
  
  @override
  Future<void> uploadData(PowerSyncDatabase database) async {
    final transaction = await database.getNextCrudTransaction();
    if (transaction == null) return;
    
    try {
      for (final op in transaction.crud) {
        await _processCrudOperation(op);
      }
      await transaction.complete();
    } catch (e) {
      // Handle error, retry later
    }
  }
}
```

---

## CRUD Operations (Local-First)

### Create
```dart
Future<void> createPackage(Package package) async {
  // Escribir a base de datos local
  await powerSync.execute(
    '''
    INSERT INTO packages (id, tracking_number, customer_name, ...)
    VALUES (?, ?, ?, ...)
    ''',
    [package.id, package.trackingNumber, package.customerName, ...],
  );
  
  // PowerSync sincronizará automáticamente cuando haya conexión
}
```

### Read
```dart
Future<List<Package>> getPackages() async {
  final results = await powerSync.getAll(
    'SELECT * FROM packages WHERE route_id = ? ORDER BY created_at DESC',
    [routeId],
  );
  
  return results.map((row) => PackageModel.fromMap(row).toEntity()).toList();
}
```

### Update
```dart
Future<void> updatePackageStatus(String packageId, String status) async {
  await powerSync.execute(
    '''
    UPDATE packages 
    SET status = ?, updated_at = ?
    WHERE id = ?
    ''',
    [status, DateTime.now().millisecondsSinceEpoch, packageId],
  );
}
```

### Delete
```dart
Future<void> deletePackage(String packageId) async {
  await powerSync.execute(
    'DELETE FROM packages WHERE id = ?',
    [packageId],
  );
}
```

---

## Idempotency Patterns

### Upsert para Prevenir Duplicados
En Supabase, usar `upsert` en lugar de `insert`:

```dart
Future<void> syncPackageToSupabase(Package package) async {
  await supabase.from('packages').upsert({
    'id': package.id,
    'tracking_number': package.trackingNumber,
    'customer_name': package.customerName,
    // ... otros campos
  }, onConflict: 'id'); // Usar ID como constraint
}
```

### Retry con Exponential Backoff
```dart
Future<T> retryWithBackoff<T>(
  Future<T> Function() operation, {
  int maxAttempts = 3,
  Duration initialDelay = const Duration(seconds: 1),
}) async {
  int attempt = 0;
  while (true) {
    try {
      return await operation();
    } catch (e) {
      attempt++;
      if (attempt >= maxAttempts) rethrow;
      
      final delay = initialDelay * pow(2, attempt - 1);
      await Future.delayed(delay);
    }
  }
}
```

---

## Conflict Resolution

### Estrategia: Last Write Wins
Por defecto, la última modificación gana:

```dart
// PowerSync maneja esto automáticamente con timestamps
// Asegurar que todas las tablas tengan updated_at
```

### Detección de Conflictos
```dart
Future<void> handleConflict(CrudEntry entry) async {
  // Obtener versión local
  final local = await powerSync.get(
    'SELECT * FROM packages WHERE id = ?',
    [entry.id],
  );
  
  // Obtener versión remota
  final remote = await supabase
    .from('packages')
    .select()
    .eq('id', entry.id)
    .single();
  
  // Comparar timestamps
  if (local['updated_at'] > remote['updated_at']) {
    // Local más reciente, forzar upload
    await _forceUpload(entry);
  } else {
    // Remoto más reciente, aceptar cambio
    await _acceptRemote(remote);
  }
}
```

### Conflictos Críticos
Para datos críticos (entregas confirmadas), notificar al usuario:

```dart
if (local['status'] == 'delivered' && remote['status'] != 'delivered') {
  // Conflicto crítico: entrega confirmada localmente pero no en servidor
  await _notifyConflictToUser(local, remote);
}
```

---

## Real-time Subscriptions

### Escuchar Cambios en Tiempo Real
```dart
final subscription = supabase
  .from('packages')
  .stream(primaryKey: ['id'])
  .eq('route_id', routeId)
  .listen((data) {
    // Actualizar UI cuando hay cambios remotos
    _updateLocalCache(data);
  });

// Cancelar en dispose
subscription.cancel();
```

### Optimización de Subscriptions
- Solo suscribirse a datos relevantes (ej: ruta activa)
- Cancelar subscriptions cuando no se necesiten
- Usar filtros para reducir tráfico de red

---

## Data Caching Strategies

### Cache de Geocoding
```dart
class CachedAddressRepository {
  final PowerSyncDatabase db;
  
  Future<Address?> findAddress(String query) async {
    final result = await db.get(
      '''
      SELECT * FROM cached_addresses 
      WHERE query = ? AND timestamp > ?
      LIMIT 1
      ''',
      [query, _thirtyDaysAgo()],
    );
    
    if (result == null) return null;
    return Address.fromMap(result);
  }
  
  Future<void> saveAddress(Address address) async {
    await db.execute(
      '''
      INSERT OR REPLACE INTO cached_addresses 
      (id, query, latitude, longitude, full_address, timestamp)
      VALUES (?, ?, ?, ?, ?, ?)
      ''',
      [
        address.id,
        address.query,
        address.latitude,
        address.longitude,
        address.fullAddress,
        DateTime.now().millisecondsSinceEpoch,
      ],
    );
  }
  
  int _thirtyDaysAgo() {
    return DateTime.now()
      .subtract(Duration(days: 30))
      .millisecondsSinceEpoch;
  }
}
```

### Cache Invalidation
- **Time-based**: Invalidar después de 30 días
- **Manual**: Permitir al usuario limpiar caché
- **Size-based**: Limitar tamaño de caché (ej: 1000 direcciones)

---

## Error Handling

### PostgrestException
```dart
try {
  await supabase.from('packages').insert(data);
} on PostgrestException catch (e) {
  if (e.code == '23505') {
    // Duplicate key error
    return Left(DuplicatePackageFailure());
  } else if (e.code == '23503') {
    // Foreign key violation
    return Left(InvalidRouteFailure());
  } else {
    return Left(DatabaseFailure(e.message));
  }
}
```

### Network Errors
```dart
try {
  await supabase.from('packages').select();
} on SocketException {
  // No internet, usar datos locales
  return await _getLocalPackages();
} on TimeoutException {
  // Timeout, reintentar
  return await retryWithBackoff(() => _fetchPackages());
}
```

---

## Sync Status Monitoring

### Detectar Estado de Sync
```dart
class SyncStatusProvider extends Notifier<SyncStatus> {
  StreamSubscription? _subscription;
  
  @override
  SyncStatus build() {
    _subscription = powerSync.statusStream.listen((status) {
      state = SyncStatus(
        isConnected: status.connected,
        isSyncing: status.uploading || status.downloading,
        lastSyncTime: status.lastSyncedAt,
      );
    });
    
    return SyncStatus.initial();
  }
  
  @override
  void dispose() {
    _subscription?.cancel();
    super.dispose();
  }
}
```

### Mostrar Indicador de Sync en UI
```dart
Consumer(
  builder: (context, ref, child) {
    final syncStatus = ref.watch(syncStatusProvider);
    
    if (!syncStatus.isConnected) {
      return OfflineIndicator();
    }
    
    if (syncStatus.isSyncing) {
      return SyncingIndicator();
    }
    
    return SyncedIndicator();
  },
)
```

---

## Row Level Security (RLS) en Supabase

### Políticas de Seguridad
```sql
-- Solo el repartidor puede ver sus propias rutas
CREATE POLICY "Drivers can view own routes"
ON routes FOR SELECT
USING (auth.uid() = driver_id);

-- Solo el repartidor puede actualizar paquetes de sus rutas
CREATE POLICY "Drivers can update own packages"
ON packages FOR UPDATE
USING (
  route_id IN (
    SELECT id FROM routes WHERE driver_id = auth.uid()
  )
);

-- Solo el repartidor puede insertar paquetes en sus rutas
CREATE POLICY "Drivers can insert packages to own routes"
ON packages FOR INSERT
WITH CHECK (
  route_id IN (
    SELECT id FROM routes WHERE driver_id = auth.uid()
  )
);
```

---

## Database Migrations

### Versionado de Schema
```dart
const schema_v1 = Schema([...]);
const schema_v2 = Schema([...]); // Con nuevas columnas

Future<void> migrateDatabase(int oldVersion, int newVersion) async {
  if (oldVersion < 2) {
    await powerSync.execute(
      'ALTER TABLE packages ADD COLUMN priority INTEGER DEFAULT 0'
    );
  }
}
```

---

## Optimización de Queries

### Índices
```sql
-- Crear índices para queries frecuentes
CREATE INDEX idx_packages_route_id ON packages(route_id);
CREATE INDEX idx_packages_status ON packages(status);
CREATE INDEX idx_cached_addresses_query ON cached_addresses(query);
```

### Queries Eficientes
```dart
// ✅ Usar índices
final packages = await powerSync.getAll(
  'SELECT * FROM packages WHERE route_id = ? AND status = ?',
  [routeId, 'pending'],
);

// ❌ Evitar SELECT *
// ✅ Seleccionar solo campos necesarios
final packages = await powerSync.getAll(
  'SELECT id, tracking_number, status FROM packages WHERE route_id = ?',
  [routeId],
);
```

---

## Checklist de Implementación

Antes de considerar sync completo:

- [ ] PowerSync schema definido y sincronizado con Supabase
- [ ] Connector implementado con fetchCredentials y uploadData
- [ ] CRUD operations usando base de datos local
- [ ] Upsert implementado para idempotencia
- [ ] Retry con exponential backoff
- [ ] Conflict resolution strategy definida
- [ ] Real-time subscriptions configuradas
- [ ] Cache de geocoding implementado
- [ ] Error handling para PostgrestException
- [ ] Sync status monitoring activo
- [ ] RLS policies configuradas en Supabase
- [ ] Índices creados para queries frecuentes
- [ ] Offline indicator en UI