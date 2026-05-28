// Tesla Dashboard UI - Vehicle Data Model
// SwiftData @Model による永続化
// 車両の基本情報を保存

import Foundation
import SwiftData

// MARK: - Tesla Vehicle Model

/// 車両データモデル（SwiftData永続化）
@Model
final class TeslaVehicle {
    // MARK: - Identifiers

    /// 車両ID（APIから取得）
    @Attribute(.unique)
    var vehicleId: String

    /// 表示名
    var displayName: String

    // MARK: - Vehicle Info

    /// モデル名（Model S, Model 3, Model X, Model Y）
    var modelName: String

    /// VIN番号
    var vin: String?

    /// 車両の色
    var exteriorColor: String?

    /// ホイールタイプ
    var wheelType: String?

    // MARK: - Status Cache

    /// 最後に確認したバッテリーレベル
    var lastKnownBatteryLevel: Int

    /// 最後に確認した走行距離
    var lastKnownOdometer: Double

    /// 最後に確認した航続距離
    var lastKnownRange: Double

    /// オンライン状態
    var isOnline: Bool

    // MARK: - Preferences

    /// デフォルトの温度設定
    var preferredTemperature: Double

    /// デフォルトの充電上限
    var preferredChargeLimit: Int

    /// デフォルトのドライブモード
    var preferredDriveMode: String

    // MARK: - Timestamps

    /// 登録日
    var createdAt: Date

    /// 最終更新日
    var updatedAt: Date

    /// 最終同期日
    var lastSyncedAt: Date?

    // MARK: - Relationships

    /// お気に入り地点
    @Relationship(deleteRule: .cascade, inverse: \TeslaFavoriteLocation.vehicle)
    var favoriteLocations: [TeslaFavoriteLocation]?

    /// 走行履歴
    @Relationship(deleteRule: .cascade, inverse: \TeslaTripHistory.vehicle)
    var tripHistories: [TeslaTripHistory]?

    /// エネルギー統計
    @Relationship(deleteRule: .cascade, inverse: \TeslaEnergyStats.vehicle)
    var energyStats: [TeslaEnergyStats]?

    // MARK: - Initialization

    init(
        vehicleId: String,
        displayName: String,
        modelName: String,
        vin: String? = nil,
        exteriorColor: String? = nil,
        wheelType: String? = nil,
        lastKnownBatteryLevel: Int = 0,
        lastKnownOdometer: Double = 0,
        lastKnownRange: Double = 0,
        isOnline: Bool = false,
        preferredTemperature: Double = 22.0,
        preferredChargeLimit: Int = 80,
        preferredDriveMode: String = "Comfort"
    ) {
        self.vehicleId = vehicleId
        self.displayName = displayName
        self.modelName = modelName
        self.vin = vin
        self.exteriorColor = exteriorColor
        self.wheelType = wheelType
        self.lastKnownBatteryLevel = lastKnownBatteryLevel
        self.lastKnownOdometer = lastKnownOdometer
        self.lastKnownRange = lastKnownRange
        self.isOnline = isOnline
        self.preferredTemperature = preferredTemperature
        self.preferredChargeLimit = preferredChargeLimit
        self.preferredDriveMode = preferredDriveMode
        self.createdAt = Date()
        self.updatedAt = Date()
    }
}

// MARK: - Computed Properties

extension TeslaVehicle {
    /// モデルのアイコン
    var modelIcon: TeslaIcon {
        switch modelName.lowercased() {
        case "model s": return .car
        case "model 3": return .car
        case "model x": return .car
        case "model y": return .car
        default: return .car
        }
    }

    /// バッテリー状態のアイコン
    var batteryIcon: TeslaIcon {
        switch lastKnownBatteryLevel {
        case 0..<20: return .batteryLow
        case 20..<50: return .batteryMedium
        case 50..<80: return .batteryHigh
        default: return .batteryFull
        }
    }

    /// バッテリー状態の色
    var batteryColor: String {
        switch lastKnownBatteryLevel {
        case 0..<20: return "statusRed"
        case 20..<50: return "statusOrange"
        default: return "statusGreen"
        }
    }

    /// フォーマットされた走行距離
    var formattedOdometer: String {
        let formatter = NumberFormatter()
        formatter.numberStyle = .decimal
        formatter.maximumFractionDigits = 0
        return "\(formatter.string(from: NSNumber(value: lastKnownOdometer)) ?? "0") km"
    }

    /// フォーマットされた航続距離
    var formattedRange: String {
        "\(Int(lastKnownRange)) km"
    }

    /// ドライブモード
    var driveMode: DriveMode {
        DriveMode(rawValue: preferredDriveMode) ?? .comfort
    }
}

// MARK: - Update Methods

extension TeslaVehicle {
    /// VehicleDataからキャッシュを更新
    func updateFromVehicleData(_ data: VehicleData) {
        lastKnownBatteryLevel = data.batteryLevel
        lastKnownOdometer = data.odometer
        lastKnownRange = data.estimatedRange
        isOnline = data.isOnline
        lastSyncedAt = Date()
        updatedAt = Date()
    }

    /// 設定を更新
    func updatePreferences(
        temperature: Double? = nil,
        chargeLimit: Int? = nil,
        driveMode: DriveMode? = nil
    ) {
        if let temperature {
            preferredTemperature = temperature
        }
        if let chargeLimit {
            preferredChargeLimit = chargeLimit
        }
        if let driveMode {
            preferredDriveMode = driveMode.rawValue
        }
        updatedAt = Date()
    }
}

// MARK: - SwiftData Queries

extension TeslaVehicle {
    /// 全車両取得のFetchDescriptor
    static var allVehiclesFetch: FetchDescriptor<TeslaVehicle> {
        FetchDescriptor<TeslaVehicle>(
            sortBy: [SortDescriptor(\.displayName)]
        )
    }

    /// オンライン車両のみ取得
    static var onlineVehiclesFetch: FetchDescriptor<TeslaVehicle> {
        var descriptor = FetchDescriptor<TeslaVehicle>(
            predicate: #Predicate { $0.isOnline },
            sortBy: [SortDescriptor(\.displayName)]
        )
        descriptor.fetchLimit = 10
        return descriptor
    }

    /// 特定のモデルで絞り込み
    static func vehiclesByModel(_ modelName: String) -> FetchDescriptor<TeslaVehicle> {
        FetchDescriptor<TeslaVehicle>(
            predicate: #Predicate { $0.modelName == modelName },
            sortBy: [SortDescriptor(\.displayName)]
        )
    }
}

// MARK: - Preview

#if DEBUG
extension TeslaVehicle {
    /// プレビュー用のサンプルデータ
    static var preview: TeslaVehicle {
        TeslaVehicle(
            vehicleId: "vehicle_001",
            displayName: "My Model S",
            modelName: "Model S",
            vin: "5YJ3E1EA1LF000001",
            exteriorColor: "Pearl White",
            wheelType: "19\" Tempest",
            lastKnownBatteryLevel: 80,
            lastKnownOdometer: 12345,
            lastKnownRange: 350,
            isOnline: true,
            preferredTemperature: 22.0,
            preferredChargeLimit: 80,
            preferredDriveMode: "Comfort"
        )
    }

    /// プレビュー用の複数車両
    static var previewList: [TeslaVehicle] {
        [
            TeslaVehicle(
                vehicleId: "vehicle_001",
                displayName: "My Model S",
                modelName: "Model S",
                lastKnownBatteryLevel: 80,
                lastKnownOdometer: 12345,
                lastKnownRange: 350,
                isOnline: true
            ),
            TeslaVehicle(
                vehicleId: "vehicle_002",
                displayName: "Family Model X",
                modelName: "Model X",
                lastKnownBatteryLevel: 65,
                lastKnownOdometer: 45678,
                lastKnownRange: 280,
                isOnline: false
            )
        ]
    }
}
#endif
