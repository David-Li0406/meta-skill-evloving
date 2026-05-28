# SwiftData Models / SwiftDataモデル設計

Tesla Dashboard UIのSwiftDataモデル設計と永続化パターンについて解説します。

## Overview / 概要

SwiftData（iOS 17+）を使用した状態永続化システムです。

## Model Container Setup / モデルコンテナ設定

### App Entry Point

```swift
@main
struct TeslaDashboardApp: App {
    var sharedModelContainer: ModelContainer = {
        let schema = Schema([
            TeslaVehicle.self,
            TeslaSettings.self,
            TeslaFavoriteLocation.self,
            TeslaTripHistory.self,
            TeslaEnergyStats.self
        ])
        let modelConfiguration = ModelConfiguration(
            schema: schema,
            isStoredInMemoryOnly: false
        )

        do {
            return try ModelContainer(for: schema, configurations: [modelConfiguration])
        } catch {
            fatalError("Could not create ModelContainer: \(error)")
        }
    }()

    var body: some Scene {
        WindowGroup {
            TeslaMainDashboard()
        }
        .modelContainer(sharedModelContainer)
    }
}
```

## Models / モデル定義

### TeslaVehicle（車両）

```swift
@Model
final class TeslaVehicle {
    @Attribute(.unique)
    var vehicleId: String
    var displayName: String
    var modelName: String
    var vin: String?

    // Status Cache
    var lastKnownBatteryLevel: Int
    var lastKnownOdometer: Double
    var lastKnownRange: Double
    var isOnline: Bool

    // Preferences
    var preferredTemperature: Double
    var preferredChargeLimit: Int
    var preferredDriveMode: String

    // Timestamps
    var createdAt: Date
    var updatedAt: Date
    var lastSyncedAt: Date?

    // Relationships
    @Relationship(deleteRule: .cascade, inverse: \TeslaFavoriteLocation.vehicle)
    var favoriteLocations: [TeslaFavoriteLocation]?

    @Relationship(deleteRule: .cascade, inverse: \TeslaTripHistory.vehicle)
    var tripHistories: [TeslaTripHistory]?

    @Relationship(deleteRule: .cascade, inverse: \TeslaEnergyStats.vehicle)
    var energyStats: [TeslaEnergyStats]?
}
```

### TeslaSettings（設定）

```swift
@Model
final class TeslaSettings {
    @Attribute(.unique)
    var settingsId: String

    // Display
    var screenBrightness: Double
    var autoBrightness: Bool
    var useCelsius: Bool
    var useKilometers: Bool
    var use24HourFormat: Bool

    // Navigation
    var voiceGuidanceEnabled: Bool
    var voiceGuidanceVolume: Double
    var showTrafficInfo: Bool
    var showChargingStations: Bool
    var mapType: String

    // Climate
    var autoClimateEnabled: Bool
    var preconditioningEnabled: Bool
    var scheduledDepartureEnabled: Bool
    var scheduledDepartureTime: Date?

    // Notifications
    var chargeCompleteNotification: Bool
    var lowBatteryNotification: Bool
    var lowBatteryThreshold: Int
    var securityNotification: Bool

    // Audio
    var mediaVolume: Double
    var startupSoundEnabled: Bool
    var hapticFeedbackEnabled: Bool
}
```

### TeslaFavoriteLocation（お気に入り地点）

```swift
@Model
final class TeslaFavoriteLocation {
    @Attribute(.unique)
    var locationId: String
    var name: String

    // Location
    var latitude: Double
    var longitude: Double
    var address: String?
    var postalCode: String?
    var prefecture: String?
    var city: String?

    // Category
    var category: String  // "home", "work", "charging", etc.
    var iconName: String?
    var colorHex: String?

    // Metadata
    var notes: String?
    var visitCount: Int
    var lastVisitedAt: Date?
    var sortOrder: Int
    var isHidden: Bool

    // Charging Info
    var isChargingStation: Bool
    var chargerType: String?
    var chargerPower: Double?

    // Relationship
    var vehicle: TeslaVehicle?
}
```

### TeslaTripHistory（走行履歴）

```swift
@Model
final class TeslaTripHistory {
    @Attribute(.unique)
    var tripId: String
    var name: String?

    // Start/End
    var startLatitude: Double
    var startLongitude: Double
    var startAddress: String?
    var endLatitude: Double?
    var endLongitude: Double?
    var endAddress: String?

    // Time
    var startTime: Date
    var endTime: Date?
    var durationMinutes: Int?

    // Distance & Energy
    var distanceKm: Double
    var startBatteryLevel: Int
    var endBatteryLevel: Int?
    var energyUsedKWh: Double?
    var averageEfficiency: Double?

    // Driving Data
    var averageSpeedKmh: Double?
    var maxSpeedKmh: Double?
    var driveMode: String?

    // Status
    var isCompleted: Bool
    var isActive: Bool

    // Relationship
    var vehicle: TeslaVehicle?
}
```

### TeslaEnergyStats（エネルギー統計）

```swift
@Model
final class TeslaEnergyStats {
    @Attribute(.unique)
    var statsId: String
    var periodType: String  // "daily", "weekly", "monthly", "yearly"
    var date: Date

    // Energy
    var energyConsumedKWh: Double
    var energyChargedKWh: Double
    var energyRegeneratedKWh: Double

    // Driving
    var distanceKm: Double
    var drivingMinutes: Int
    var tripCount: Int

    // Efficiency
    var averageEfficiency: Double?
    var bestEfficiency: Double?
    var worstEfficiency: Double?

    // Charging
    var chargeCount: Int
    var superchargerCount: Int
    var homeChargeCount: Int
    var chargingMinutes: Int

    // Cost
    var chargingCost: Double?
    var electricityRate: Double?

    // Relationship
    var vehicle: TeslaVehicle?
}
```

## Queries / クエリ

### FetchDescriptor パターン

```swift
extension TeslaVehicle {
    static var allVehiclesFetch: FetchDescriptor<TeslaVehicle> {
        FetchDescriptor<TeslaVehicle>(
            sortBy: [SortDescriptor(\.displayName)]
        )
    }

    static var onlineVehiclesFetch: FetchDescriptor<TeslaVehicle> {
        var descriptor = FetchDescriptor<TeslaVehicle>(
            predicate: #Predicate { $0.isOnline },
            sortBy: [SortDescriptor(\.displayName)]
        )
        descriptor.fetchLimit = 10
        return descriptor
    }
}
```

### View での使用

```swift
struct VehicleListView: View {
    @Query(TeslaVehicle.allVehiclesFetch) private var vehicles: [TeslaVehicle]

    var body: some View {
        List(vehicles) { vehicle in
            VehicleRow(vehicle: vehicle)
        }
    }
}
```

### 動的クエリ

```swift
struct TripHistoryView: View {
    @Query private var trips: [TeslaTripHistory]

    init(vehicleId: String) {
        let descriptor = FetchDescriptor<TeslaTripHistory>(
            predicate: #Predicate { $0.vehicle?.vehicleId == vehicleId },
            sortBy: [SortDescriptor(\.startTime, order: .reverse)]
        )
        _trips = Query(descriptor)
    }
}
```

## CRUD Operations / CRUD操作

### Create（作成）

```swift
func createVehicle(id: String, name: String, model: String) {
    let vehicle = TeslaVehicle(
        vehicleId: id,
        displayName: name,
        modelName: model
    )
    modelContext.insert(vehicle)
}
```

### Read（読み取り）

```swift
func fetchVehicle(by id: String) -> TeslaVehicle? {
    let descriptor = FetchDescriptor<TeslaVehicle>(
        predicate: #Predicate { $0.vehicleId == id }
    )
    return try? modelContext.fetch(descriptor).first
}
```

### Update（更新）

```swift
func updateVehicle(_ vehicle: TeslaVehicle, newName: String) {
    vehicle.displayName = newName
    vehicle.updatedAt = Date()
    // modelContext は自動保存
}
```

### Delete（削除）

```swift
func deleteVehicle(_ vehicle: TeslaVehicle) {
    modelContext.delete(vehicle)
}
```

## Relationships / リレーション

### カスケード削除

```swift
@Relationship(deleteRule: .cascade, inverse: \TeslaFavoriteLocation.vehicle)
var favoriteLocations: [TeslaFavoriteLocation]?
```

車両を削除すると、関連するお気に入り地点も自動削除されます。

### 逆参照

```swift
// TeslaFavoriteLocation 側
var vehicle: TeslaVehicle?

// TeslaVehicle 側
@Relationship(deleteRule: .cascade, inverse: \TeslaFavoriteLocation.vehicle)
var favoriteLocations: [TeslaFavoriteLocation]?
```

## Preview Data / プレビューデータ

```swift
#if DEBUG
extension TeslaVehicle {
    static var preview: TeslaVehicle {
        TeslaVehicle(
            vehicleId: "vehicle_001",
            displayName: "My Model S",
            modelName: "Model S",
            lastKnownBatteryLevel: 80,
            lastKnownOdometer: 12345,
            lastKnownRange: 350,
            isOnline: true
        )
    }
}
#endif
```

## Migration / マイグレーション

```swift
enum TeslaSchemaV1: VersionedSchema {
    static var versionIdentifier = Schema.Version(1, 0, 0)
    static var models: [any PersistentModel.Type] {
        [TeslaVehicle.self, TeslaSettings.self]
    }
}

enum TeslaSchemaV2: VersionedSchema {
    static var versionIdentifier = Schema.Version(2, 0, 0)
    static var models: [any PersistentModel.Type] {
        [TeslaVehicle.self, TeslaSettings.self, TeslaFavoriteLocation.self]
    }
}

enum TeslaMigrationPlan: SchemaMigrationPlan {
    static var schemas: [any VersionedSchema.Type] {
        [TeslaSchemaV1.self, TeslaSchemaV2.self]
    }

    static var stages: [MigrationStage] {
        [migrateV1toV2]
    }

    static let migrateV1toV2 = MigrationStage.lightweight(
        fromVersion: TeslaSchemaV1.self,
        toVersion: TeslaSchemaV2.self
    )
}
```

## Best Practices / ベストプラクティス

### 1. @Attribute(.unique) を使用

```swift
@Attribute(.unique)
var vehicleId: String  // 一意のID
```

### 2. タイムスタンプを含める

```swift
var createdAt: Date
var updatedAt: Date
```

### 3. Computedプロパティは保存しない

```swift
// ✅ Computed（保存されない）
var formattedDistance: String {
    String(format: "%.1f km", distanceKm)
}

// ❌ 保存（不要なデータ）
var formattedDistance: String  // @Model プロパティ
```

### 4. オプショナルを適切に使用

```swift
var vin: String?           // オプショナル（車両に依存）
var lastSyncedAt: Date?    // オプショナル（未同期時はnil）
```

## Related Documents / 関連ドキュメント

- [Error Handling](./error-handling.md)
- [Vehicle Data Provider](../examples/models/vehicle-data-provider.swift)
