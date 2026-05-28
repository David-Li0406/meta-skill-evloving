// Tesla Dashboard UI - Trip History Model
// SwiftData @Model による走行履歴の永続化
// 走行データの記録と分析

import Foundation
import SwiftData
import CoreLocation

// MARK: - Tesla Trip History Model

/// 走行履歴モデル（SwiftData永続化）
@Model
final class TeslaTripHistory {
    // MARK: - Identifiers

    /// 走行ID
    @Attribute(.unique)
    var tripId: String

    /// 走行名（自動生成または手動設定）
    var name: String?

    // MARK: - Trip Data

    /// 出発地緯度
    var startLatitude: Double

    /// 出発地経度
    var startLongitude: Double

    /// 出発地住所
    var startAddress: String?

    /// 到着地緯度
    var endLatitude: Double?

    /// 到着地経度
    var endLongitude: Double?

    /// 到着地住所
    var endAddress: String?

    // MARK: - Time Data

    /// 出発時刻
    var startTime: Date

    /// 到着時刻
    var endTime: Date?

    /// 走行時間（分）
    var durationMinutes: Int?

    // MARK: - Distance & Energy

    /// 走行距離（km）
    var distanceKm: Double

    /// 開始時バッテリー（%）
    var startBatteryLevel: Int

    /// 終了時バッテリー（%）
    var endBatteryLevel: Int?

    /// 消費エネルギー（kWh）
    var energyUsedKWh: Double?

    /// 平均電費（Wh/km）
    var averageEfficiency: Double?

    // MARK: - Driving Data

    /// 平均速度（km/h）
    var averageSpeedKmh: Double?

    /// 最高速度（km/h）
    var maxSpeedKmh: Double?

    /// ドライブモード
    var driveMode: String?

    // MARK: - Climate Data

    /// 外気温（°C）
    var outsideTemperature: Double?

    /// 空調使用有無
    var climateUsed: Bool

    // MARK: - Route Data

    /// ルートポイント（JSON形式）
    var routePointsJson: String?

    // MARK: - Status

    /// 走行完了フラグ
    var isCompleted: Bool

    /// 走行中フラグ
    var isActive: Bool

    // MARK: - Timestamps

    /// 作成日
    var createdAt: Date

    /// 更新日
    var updatedAt: Date

    // MARK: - Relationships

    /// 所属車両
    var vehicle: TeslaVehicle?

    // MARK: - Initialization

    init(
        tripId: String = UUID().uuidString,
        startLatitude: Double,
        startLongitude: Double,
        startAddress: String? = nil,
        startBatteryLevel: Int
    ) {
        self.tripId = tripId
        self.startLatitude = startLatitude
        self.startLongitude = startLongitude
        self.startAddress = startAddress
        self.startTime = Date()
        self.distanceKm = 0
        self.startBatteryLevel = startBatteryLevel
        self.climateUsed = false
        self.isCompleted = false
        self.isActive = true
        self.createdAt = Date()
        self.updatedAt = Date()
    }
}

// MARK: - Computed Properties

extension TeslaTripHistory {
    /// 出発地座標
    var startCoordinate: CLLocationCoordinate2D {
        CLLocationCoordinate2D(latitude: startLatitude, longitude: startLongitude)
    }

    /// 到着地座標
    var endCoordinate: CLLocationCoordinate2D? {
        guard let lat = endLatitude, let lon = endLongitude else { return nil }
        return CLLocationCoordinate2D(latitude: lat, longitude: lon)
    }

    /// 走行時間（フォーマット済み）
    var formattedDuration: String {
        guard let minutes = durationMinutes else { return "--" }

        if minutes < 60 {
            return "\(minutes)分"
        } else {
            let hours = minutes / 60
            let mins = minutes % 60
            return mins > 0 ? "\(hours)時間\(mins)分" : "\(hours)時間"
        }
    }

    /// 走行距離（フォーマット済み）
    var formattedDistance: String {
        if distanceKm < 1 {
            return String(format: "%.0f m", distanceKm * 1000)
        } else {
            return String(format: "%.1f km", distanceKm)
        }
    }

    /// バッテリー消費（%）
    var batteryUsed: Int? {
        guard let endLevel = endBatteryLevel else { return nil }
        return startBatteryLevel - endLevel
    }

    /// バッテリー消費（フォーマット済み）
    var formattedBatteryUsed: String {
        guard let used = batteryUsed else { return "--" }
        return "\(used)%"
    }

    /// 電費（フォーマット済み）
    var formattedEfficiency: String {
        guard let efficiency = averageEfficiency else { return "--" }
        return String(format: "%.0f Wh/km", efficiency)
    }

    /// 平均速度（フォーマット済み）
    var formattedAverageSpeed: String {
        guard let speed = averageSpeedKmh else { return "--" }
        return String(format: "%.0f km/h", speed)
    }

    /// 走行名（自動生成）
    var displayName: String {
        if let name, !name.isEmpty {
            return name
        }

        let formatter = DateFormatter()
        formatter.dateFormat = "M/d HH:mm"

        if let endAddress {
            return "\(formatter.string(from: startTime)) → \(endAddress)"
        } else if let startAddress {
            return "\(formatter.string(from: startTime)) \(startAddress)"
        } else {
            return formatter.string(from: startTime)
        }
    }

    /// 走行日（フォーマット済み）
    var formattedDate: String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy/MM/dd"
        return formatter.string(from: startTime)
    }

    /// 走行時刻（フォーマット済み）
    var formattedTime: String {
        let formatter = DateFormatter()
        formatter.dateFormat = "HH:mm"

        var result = formatter.string(from: startTime)
        if let endTime {
            result += " - \(formatter.string(from: endTime))"
        }
        return result
    }
}

// MARK: - Trip Management

extension TeslaTripHistory {
    /// 走行を終了
    func complete(
        endLatitude: Double,
        endLongitude: Double,
        endAddress: String? = nil,
        endBatteryLevel: Int,
        distanceKm: Double,
        averageSpeedKmh: Double? = nil,
        maxSpeedKmh: Double? = nil
    ) {
        self.endLatitude = endLatitude
        self.endLongitude = endLongitude
        self.endAddress = endAddress
        self.endTime = Date()
        self.endBatteryLevel = endBatteryLevel
        self.distanceKm = distanceKm
        self.averageSpeedKmh = averageSpeedKmh
        self.maxSpeedKmh = maxSpeedKmh
        self.isCompleted = true
        self.isActive = false

        // 走行時間を計算
        if let endTime = self.endTime {
            self.durationMinutes = Int(endTime.timeIntervalSince(startTime) / 60)
        }

        // 電費を計算
        if let usedBattery = batteryUsed, distanceKm > 0 {
            // 仮定: 75kWhバッテリー
            let usedKWh = Double(usedBattery) / 100.0 * 75.0
            self.energyUsedKWh = usedKWh
            self.averageEfficiency = (usedKWh * 1000) / distanceKm
        }

        self.updatedAt = Date()
    }

    /// 走行をキャンセル
    func cancel() {
        self.isCompleted = false
        self.isActive = false
        self.updatedAt = Date()
    }

    /// 走行中のデータを更新
    func updateProgress(
        distanceKm: Double,
        currentBatteryLevel: Int,
        currentSpeedKmh: Double? = nil
    ) {
        self.distanceKm = distanceKm

        // 最高速度を更新
        if let speed = currentSpeedKmh {
            if let maxSpeed = self.maxSpeedKmh {
                self.maxSpeedKmh = max(maxSpeed, speed)
            } else {
                self.maxSpeedKmh = speed
            }
        }

        self.updatedAt = Date()
    }
}

// MARK: - Route Points

extension TeslaTripHistory {
    /// ルートポイントを追加
    func addRoutePoint(_ coordinate: CLLocationCoordinate2D) {
        var points = routePoints
        points.append([coordinate.latitude, coordinate.longitude])

        if let jsonData = try? JSONEncoder().encode(points),
           let jsonString = String(data: jsonData, encoding: .utf8) {
            routePointsJson = jsonString
        }
    }

    /// ルートポイントを取得
    var routePoints: [[Double]] {
        guard let json = routePointsJson,
              let data = json.data(using: .utf8),
              let points = try? JSONDecoder().decode([[Double]].self, from: data) else {
            return []
        }
        return points
    }

    /// ルート座標を取得
    var routeCoordinates: [CLLocationCoordinate2D] {
        routePoints.compactMap { point in
            guard point.count == 2 else { return nil }
            return CLLocationCoordinate2D(latitude: point[0], longitude: point[1])
        }
    }
}

// MARK: - SwiftData Queries

extension TeslaTripHistory {
    /// 全履歴を取得（新しい順）
    static var allTripsFetch: FetchDescriptor<TeslaTripHistory> {
        FetchDescriptor<TeslaTripHistory>(
            predicate: #Predicate { $0.isCompleted },
            sortBy: [SortDescriptor(\.startTime, order: .reverse)]
        )
    }

    /// 最近の履歴を取得
    static func recentTrips(limit: Int = 10) -> FetchDescriptor<TeslaTripHistory> {
        var descriptor = FetchDescriptor<TeslaTripHistory>(
            predicate: #Predicate { $0.isCompleted },
            sortBy: [SortDescriptor(\.startTime, order: .reverse)]
        )
        descriptor.fetchLimit = limit
        return descriptor
    }

    /// アクティブな走行を取得
    static var activeTripFetch: FetchDescriptor<TeslaTripHistory> {
        FetchDescriptor<TeslaTripHistory>(
            predicate: #Predicate { $0.isActive }
        )
    }

    /// 日付範囲で取得
    static func tripsByDateRange(from startDate: Date, to endDate: Date) -> FetchDescriptor<TeslaTripHistory> {
        FetchDescriptor<TeslaTripHistory>(
            predicate: #Predicate { trip in
                trip.isCompleted && trip.startTime >= startDate && trip.startTime <= endDate
            },
            sortBy: [SortDescriptor(\.startTime, order: .reverse)]
        )
    }
}

// MARK: - Preview

#if DEBUG
extension TeslaTripHistory {
    /// プレビュー用のサンプルデータ
    static var preview: TeslaTripHistory {
        let trip = TeslaTripHistory(
            startLatitude: 35.6812,
            startLongitude: 139.7671,
            startAddress: "東京駅",
            startBatteryLevel: 80
        )
        trip.complete(
            endLatitude: 35.6895,
            endLongitude: 139.6917,
            endAddress: "新宿駅",
            endBatteryLevel: 72,
            distanceKm: 12.5,
            averageSpeedKmh: 35.2,
            maxSpeedKmh: 60.0
        )
        trip.driveMode = "Comfort"
        trip.outsideTemperature = 25.0
        trip.climateUsed = true
        return trip
    }

    /// プレビュー用のリスト
    static var previewList: [TeslaTripHistory] {
        [
            {
                let trip = TeslaTripHistory(
                    startLatitude: 35.6812,
                    startLongitude: 139.7671,
                    startAddress: "東京駅",
                    startBatteryLevel: 80
                )
                trip.complete(
                    endLatitude: 35.6895,
                    endLongitude: 139.6917,
                    endAddress: "新宿駅",
                    endBatteryLevel: 72,
                    distanceKm: 12.5,
                    averageSpeedKmh: 35.2
                )
                return trip
            }(),
            {
                let trip = TeslaTripHistory(
                    startLatitude: 35.6895,
                    startLongitude: 139.6917,
                    startAddress: "新宿駅",
                    startBatteryLevel: 72
                )
                trip.complete(
                    endLatitude: 35.4437,
                    endLongitude: 139.6380,
                    endAddress: "横浜駅",
                    endBatteryLevel: 58,
                    distanceKm: 35.2,
                    averageSpeedKmh: 55.8
                )
                return trip
            }(),
            {
                let trip = TeslaTripHistory(
                    startLatitude: 35.4437,
                    startLongitude: 139.6380,
                    startAddress: "横浜駅",
                    startBatteryLevel: 90
                )
                trip.complete(
                    endLatitude: 35.6812,
                    endLongitude: 139.7671,
                    endAddress: "東京駅",
                    endBatteryLevel: 78,
                    distanceKm: 30.1,
                    averageSpeedKmh: 42.3
                )
                return trip
            }()
        ]
    }
}
#endif
