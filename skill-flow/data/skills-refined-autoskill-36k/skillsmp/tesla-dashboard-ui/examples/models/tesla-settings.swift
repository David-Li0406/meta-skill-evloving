// Tesla Dashboard UI - Settings Model
// SwiftData @Model による設定の永続化
// アプリ全体の設定を管理

import Foundation
import SwiftData

// MARK: - Tesla Settings Model

/// アプリ設定モデル（SwiftData永続化）
@Model
final class TeslaSettings {
    // MARK: - Identifiers

    /// 設定ID（シングルトン用）
    @Attribute(.unique)
    var settingsId: String

    // MARK: - Display Settings

    /// 画面の明るさ（0.0〜1.0）
    var screenBrightness: Double

    /// 自動明るさ調整
    var autoBrightness: Bool

    /// 温度単位（true: Celsius, false: Fahrenheit）
    var useCelsius: Bool

    /// 距離単位（true: km, false: miles）
    var useKilometers: Bool

    /// 時間形式（true: 24h, false: 12h）
    var use24HourFormat: Bool

    // MARK: - Navigation Settings

    /// 音声案内有効
    var voiceGuidanceEnabled: Bool

    /// 音声案内音量（0.0〜1.0）
    var voiceGuidanceVolume: Double

    /// 交通情報表示
    var showTrafficInfo: Bool

    /// 充電スポット表示
    var showChargingStations: Bool

    /// 地図タイプ（standard, satellite, hybrid）
    var mapType: String

    // MARK: - Climate Settings

    /// 自動空調有効
    var autoClimateEnabled: Bool

    /// プリコンディショニング有効
    var preconditioningEnabled: Bool

    /// 出発時刻自動設定
    var scheduledDepartureEnabled: Bool

    /// 出発時刻
    var scheduledDepartureTime: Date?

    // MARK: - Charging Settings

    /// スケジュール充電有効
    var scheduledChargingEnabled: Bool

    /// 充電開始時刻
    var scheduledChargingTime: Date?

    /// オフピーク充電のみ
    var offPeakChargingOnly: Bool

    // MARK: - Notification Settings

    /// 充電完了通知
    var chargeCompleteNotification: Bool

    /// バッテリー低下通知
    var lowBatteryNotification: Bool

    /// バッテリー低下閾値（%）
    var lowBatteryThreshold: Int

    /// セキュリティ通知
    var securityNotification: Bool

    // MARK: - Audio Settings

    /// メディア音量（0.0〜1.0）
    var mediaVolume: Double

    /// 起動音有効
    var startupSoundEnabled: Bool

    /// 操作音有効
    var hapticFeedbackEnabled: Bool

    // MARK: - Privacy Settings

    /// 位置情報履歴保存
    var saveLocationHistory: Bool

    /// 走行データ収集
    var collectDrivingData: Bool

    // MARK: - Timestamps

    /// 作成日
    var createdAt: Date

    /// 更新日
    var updatedAt: Date

    // MARK: - Initialization

    init(settingsId: String = "default") {
        self.settingsId = settingsId

        // Display
        self.screenBrightness = 0.7
        self.autoBrightness = true
        self.useCelsius = true
        self.useKilometers = true
        self.use24HourFormat = true

        // Navigation
        self.voiceGuidanceEnabled = true
        self.voiceGuidanceVolume = 0.8
        self.showTrafficInfo = true
        self.showChargingStations = true
        self.mapType = "standard"

        // Climate
        self.autoClimateEnabled = true
        self.preconditioningEnabled = false
        self.scheduledDepartureEnabled = false
        self.scheduledDepartureTime = nil

        // Charging
        self.scheduledChargingEnabled = false
        self.scheduledChargingTime = nil
        self.offPeakChargingOnly = false

        // Notifications
        self.chargeCompleteNotification = true
        self.lowBatteryNotification = true
        self.lowBatteryThreshold = 20
        self.securityNotification = true

        // Audio
        self.mediaVolume = 0.5
        self.startupSoundEnabled = true
        self.hapticFeedbackEnabled = true

        // Privacy
        self.saveLocationHistory = true
        self.collectDrivingData = true

        // Timestamps
        self.createdAt = Date()
        self.updatedAt = Date()
    }
}

// MARK: - Computed Properties

extension TeslaSettings {
    /// 地図タイプのenum
    var mapTypeEnum: MapDisplayType {
        MapDisplayType(rawValue: mapType) ?? .standard
    }

    /// 温度フォーマッター
    func formatTemperature(_ celsius: Double) -> String {
        if useCelsius {
            return String(format: "%.1f°C", celsius)
        } else {
            let fahrenheit = celsius * 9 / 5 + 32
            return String(format: "%.1f°F", fahrenheit)
        }
    }

    /// 距離フォーマッター
    func formatDistance(_ kilometers: Double) -> String {
        if useKilometers {
            return String(format: "%.1f km", kilometers)
        } else {
            let miles = kilometers * 0.621371
            return String(format: "%.1f mi", miles)
        }
    }

    /// 時刻フォーマッター
    var timeFormatter: DateFormatter {
        let formatter = DateFormatter()
        formatter.dateFormat = use24HourFormat ? "HH:mm" : "h:mm a"
        return formatter
    }
}

// MARK: - Map Display Type

/// 地図表示タイプ
enum MapDisplayType: String, Codable, CaseIterable {
    case standard = "standard"
    case satellite = "satellite"
    case hybrid = "hybrid"

    var displayName: String {
        switch self {
        case .standard: return "標準"
        case .satellite: return "衛星写真"
        case .hybrid: return "ハイブリッド"
        }
    }
}

// MARK: - Update Methods

extension TeslaSettings {
    /// 表示設定を更新
    func updateDisplaySettings(
        brightness: Double? = nil,
        autoBrightness: Bool? = nil,
        useCelsius: Bool? = nil,
        useKilometers: Bool? = nil,
        use24HourFormat: Bool? = nil
    ) {
        if let brightness {
            self.screenBrightness = max(0, min(1, brightness))
        }
        if let autoBrightness {
            self.autoBrightness = autoBrightness
        }
        if let useCelsius {
            self.useCelsius = useCelsius
        }
        if let useKilometers {
            self.useKilometers = useKilometers
        }
        if let use24HourFormat {
            self.use24HourFormat = use24HourFormat
        }
        self.updatedAt = Date()
    }

    /// ナビゲーション設定を更新
    func updateNavigationSettings(
        voiceGuidanceEnabled: Bool? = nil,
        voiceGuidanceVolume: Double? = nil,
        showTrafficInfo: Bool? = nil,
        showChargingStations: Bool? = nil,
        mapType: MapDisplayType? = nil
    ) {
        if let voiceGuidanceEnabled {
            self.voiceGuidanceEnabled = voiceGuidanceEnabled
        }
        if let voiceGuidanceVolume {
            self.voiceGuidanceVolume = max(0, min(1, voiceGuidanceVolume))
        }
        if let showTrafficInfo {
            self.showTrafficInfo = showTrafficInfo
        }
        if let showChargingStations {
            self.showChargingStations = showChargingStations
        }
        if let mapType {
            self.mapType = mapType.rawValue
        }
        self.updatedAt = Date()
    }

    /// デフォルト設定にリセット
    func resetToDefaults() {
        let defaultSettings = TeslaSettings()

        // Copy all values except ID and timestamps
        self.screenBrightness = defaultSettings.screenBrightness
        self.autoBrightness = defaultSettings.autoBrightness
        self.useCelsius = defaultSettings.useCelsius
        self.useKilometers = defaultSettings.useKilometers
        self.use24HourFormat = defaultSettings.use24HourFormat

        self.voiceGuidanceEnabled = defaultSettings.voiceGuidanceEnabled
        self.voiceGuidanceVolume = defaultSettings.voiceGuidanceVolume
        self.showTrafficInfo = defaultSettings.showTrafficInfo
        self.showChargingStations = defaultSettings.showChargingStations
        self.mapType = defaultSettings.mapType

        self.autoClimateEnabled = defaultSettings.autoClimateEnabled
        self.preconditioningEnabled = defaultSettings.preconditioningEnabled
        self.scheduledDepartureEnabled = defaultSettings.scheduledDepartureEnabled
        self.scheduledDepartureTime = defaultSettings.scheduledDepartureTime

        self.scheduledChargingEnabled = defaultSettings.scheduledChargingEnabled
        self.scheduledChargingTime = defaultSettings.scheduledChargingTime
        self.offPeakChargingOnly = defaultSettings.offPeakChargingOnly

        self.chargeCompleteNotification = defaultSettings.chargeCompleteNotification
        self.lowBatteryNotification = defaultSettings.lowBatteryNotification
        self.lowBatteryThreshold = defaultSettings.lowBatteryThreshold
        self.securityNotification = defaultSettings.securityNotification

        self.mediaVolume = defaultSettings.mediaVolume
        self.startupSoundEnabled = defaultSettings.startupSoundEnabled
        self.hapticFeedbackEnabled = defaultSettings.hapticFeedbackEnabled

        self.saveLocationHistory = defaultSettings.saveLocationHistory
        self.collectDrivingData = defaultSettings.collectDrivingData

        self.updatedAt = Date()
    }
}

// MARK: - SwiftData Queries

extension TeslaSettings {
    /// デフォルト設定を取得
    static var defaultSettingsFetch: FetchDescriptor<TeslaSettings> {
        FetchDescriptor<TeslaSettings>(
            predicate: #Predicate { $0.settingsId == "default" }
        )
    }
}

// MARK: - Preview

#if DEBUG
extension TeslaSettings {
    /// プレビュー用のサンプルデータ
    static var preview: TeslaSettings {
        let settings = TeslaSettings()
        settings.screenBrightness = 0.7
        settings.voiceGuidanceEnabled = true
        settings.showTrafficInfo = true
        return settings
    }
}
#endif
