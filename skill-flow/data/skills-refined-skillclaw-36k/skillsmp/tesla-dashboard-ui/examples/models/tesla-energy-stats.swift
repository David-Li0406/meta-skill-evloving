// Tesla Dashboard UI - Energy Stats Model
// SwiftData @Model によるエネルギー統計の永続化
// 充電・消費データの記録と分析

import Foundation
import SwiftData

// MARK: - Tesla Energy Stats Model

/// エネルギー統計モデル（SwiftData永続化）
@Model
final class TeslaEnergyStats {
    // MARK: - Identifiers

    /// 統計ID
    @Attribute(.unique)
    var statsId: String

    /// 統計期間タイプ
    var periodType: String

    /// 統計日付
    var date: Date

    // MARK: - Energy Data

    /// 消費エネルギー（kWh）
    var energyConsumedKWh: Double

    /// 充電エネルギー（kWh）
    var energyChargedKWh: Double

    /// 回生エネルギー（kWh）
    var energyRegeneratedKWh: Double

    // MARK: - Driving Data

    /// 走行距離（km）
    var distanceKm: Double

    /// 走行時間（分）
    var drivingMinutes: Int

    /// 走行回数
    var tripCount: Int

    // MARK: - Efficiency Data

    /// 平均電費（Wh/km）
    var averageEfficiency: Double?

    /// 最高電費（Wh/km）
    var bestEfficiency: Double?

    /// 最低電費（Wh/km）
    var worstEfficiency: Double?

    // MARK: - Charging Data

    /// 充電回数
    var chargeCount: Int

    /// スーパーチャージャー使用回数
    var superchargerCount: Int

    /// 自宅充電回数
    var homeChargeCount: Int

    /// 充電時間（分）
    var chargingMinutes: Int

    // MARK: - Climate Data

    /// 空調消費エネルギー（kWh）
    var climateEnergyKWh: Double?

    /// 平均外気温（°C）
    var averageOutsideTemp: Double?

    // MARK: - Cost Data

    /// 充電コスト（円）
    var chargingCost: Double?

    /// 電気代単価（円/kWh）
    var electricityRate: Double?

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
        statsId: String = UUID().uuidString,
        periodType: StatsPeriodType = .daily,
        date: Date = Date()
    ) {
        self.statsId = statsId
        self.periodType = periodType.rawValue
        self.date = date
        self.energyConsumedKWh = 0
        self.energyChargedKWh = 0
        self.energyRegeneratedKWh = 0
        self.distanceKm = 0
        self.drivingMinutes = 0
        self.tripCount = 0
        self.chargeCount = 0
        self.superchargerCount = 0
        self.homeChargeCount = 0
        self.chargingMinutes = 0
        self.createdAt = Date()
        self.updatedAt = Date()
    }
}

// MARK: - Stats Period Type

/// 統計期間タイプ
enum StatsPeriodType: String, Codable, CaseIterable {
    case daily = "daily"
    case weekly = "weekly"
    case monthly = "monthly"
    case yearly = "yearly"
    case allTime = "all_time"

    var displayName: String {
        switch self {
        case .daily: return "日次"
        case .weekly: return "週次"
        case .monthly: return "月次"
        case .yearly: return "年次"
        case .allTime: return "全期間"
        }
    }
}

// MARK: - Computed Properties

extension TeslaEnergyStats {
    /// 期間タイプenum
    var periodTypeEnum: StatsPeriodType {
        StatsPeriodType(rawValue: periodType) ?? .daily
    }

    /// ネット消費エネルギー（回生を差し引いた値）
    var netEnergyConsumed: Double {
        energyConsumedKWh - energyRegeneratedKWh
    }

    /// 電費（フォーマット済み）
    var formattedEfficiency: String {
        guard let efficiency = averageEfficiency else {
            // 計算して表示
            if distanceKm > 0 {
                let calculated = (energyConsumedKWh * 1000) / distanceKm
                return String(format: "%.0f Wh/km", calculated)
            }
            return "--"
        }
        return String(format: "%.0f Wh/km", efficiency)
    }

    /// 走行距離（フォーマット済み）
    var formattedDistance: String {
        String(format: "%.1f km", distanceKm)
    }

    /// 消費エネルギー（フォーマット済み）
    var formattedEnergyConsumed: String {
        String(format: "%.1f kWh", energyConsumedKWh)
    }

    /// 充電エネルギー（フォーマット済み）
    var formattedEnergyCharged: String {
        String(format: "%.1f kWh", energyChargedKWh)
    }

    /// 走行時間（フォーマット済み）
    var formattedDrivingTime: String {
        if drivingMinutes < 60 {
            return "\(drivingMinutes)分"
        } else {
            let hours = drivingMinutes / 60
            let mins = drivingMinutes % 60
            return mins > 0 ? "\(hours)時間\(mins)分" : "\(hours)時間"
        }
    }

    /// 充電コスト（フォーマット済み）
    var formattedChargingCost: String {
        guard let cost = chargingCost else { return "--" }
        return String(format: "¥%.0f", cost)
    }

    /// 回生率（%）
    var regenerationRate: Double {
        guard energyConsumedKWh > 0 else { return 0 }
        return (energyRegeneratedKWh / energyConsumedKWh) * 100
    }

    /// 回生率（フォーマット済み）
    var formattedRegenerationRate: String {
        String(format: "%.1f%%", regenerationRate)
    }

    /// 日付（フォーマット済み）
    var formattedDate: String {
        let formatter = DateFormatter()

        switch periodTypeEnum {
        case .daily:
            formatter.dateFormat = "yyyy/MM/dd"
        case .weekly:
            formatter.dateFormat = "yyyy/MM/dd 週"
        case .monthly:
            formatter.dateFormat = "yyyy/MM"
        case .yearly:
            formatter.dateFormat = "yyyy年"
        case .allTime:
            return "全期間"
        }

        return formatter.string(from: date)
    }
}

// MARK: - Update Methods

extension TeslaEnergyStats {
    /// 走行データを追加
    func addTrip(
        distanceKm: Double,
        energyUsedKWh: Double,
        durationMinutes: Int,
        regeneratedKWh: Double = 0
    ) {
        self.distanceKm += distanceKm
        self.energyConsumedKWh += energyUsedKWh
        self.drivingMinutes += durationMinutes
        self.energyRegeneratedKWh += regeneratedKWh
        self.tripCount += 1

        // 電費を再計算
        if self.distanceKm > 0 {
            self.averageEfficiency = (self.energyConsumedKWh * 1000) / self.distanceKm
        }

        self.updatedAt = Date()
    }

    /// 充電データを追加
    func addCharge(
        energyKWh: Double,
        durationMinutes: Int,
        isSupercharger: Bool = false,
        isHomeCharge: Bool = false,
        cost: Double? = nil
    ) {
        self.energyChargedKWh += energyKWh
        self.chargingMinutes += durationMinutes
        self.chargeCount += 1

        if isSupercharger {
            self.superchargerCount += 1
        }
        if isHomeCharge {
            self.homeChargeCount += 1
        }

        if let cost {
            self.chargingCost = (self.chargingCost ?? 0) + cost
        }

        self.updatedAt = Date()
    }

    /// 空調データを設定
    func setClimateData(energyKWh: Double, averageOutsideTemp: Double?) {
        self.climateEnergyKWh = energyKWh
        self.averageOutsideTemp = averageOutsideTemp
        self.updatedAt = Date()
    }

    /// 電気代を計算
    func calculateChargingCost(rate: Double) {
        self.electricityRate = rate
        self.chargingCost = energyChargedKWh * rate
        self.updatedAt = Date()
    }
}

// MARK: - SwiftData Queries

extension TeslaEnergyStats {
    /// 今日の統計を取得
    static var todayStatsFetch: FetchDescriptor<TeslaEnergyStats> {
        let calendar = Calendar.current
        let startOfDay = calendar.startOfDay(for: Date())
        let periodTypeRaw = StatsPeriodType.daily.rawValue

        return FetchDescriptor<TeslaEnergyStats>(
            predicate: #Predicate { stats in
                stats.periodType == periodTypeRaw && stats.date >= startOfDay
            }
        )
    }

    /// 期間タイプで取得
    static func statsByPeriod(_ periodType: StatsPeriodType, limit: Int = 30) -> FetchDescriptor<TeslaEnergyStats> {
        let periodTypeRaw = periodType.rawValue
        var descriptor = FetchDescriptor<TeslaEnergyStats>(
            predicate: #Predicate { $0.periodType == periodTypeRaw },
            sortBy: [SortDescriptor(\.date, order: .reverse)]
        )
        descriptor.fetchLimit = limit
        return descriptor
    }

    /// 日付範囲で取得
    static func statsByDateRange(
        from startDate: Date,
        to endDate: Date,
        periodType: StatsPeriodType = .daily
    ) -> FetchDescriptor<TeslaEnergyStats> {
        let periodTypeRaw = periodType.rawValue
        return FetchDescriptor<TeslaEnergyStats>(
            predicate: #Predicate { stats in
                stats.periodType == periodTypeRaw &&
                stats.date >= startDate &&
                stats.date <= endDate
            },
            sortBy: [SortDescriptor(\.date)]
        )
    }
}

// MARK: - Preview

#if DEBUG
extension TeslaEnergyStats {
    /// プレビュー用のサンプルデータ
    static var preview: TeslaEnergyStats {
        let stats = TeslaEnergyStats(periodType: .daily)
        stats.distanceKm = 85.5
        stats.energyConsumedKWh = 15.2
        stats.energyChargedKWh = 20.0
        stats.energyRegeneratedKWh = 2.1
        stats.drivingMinutes = 120
        stats.tripCount = 3
        stats.chargeCount = 1
        stats.homeChargeCount = 1
        stats.chargingMinutes = 180
        stats.averageEfficiency = 178
        stats.chargingCost = 600
        stats.electricityRate = 30
        stats.averageOutsideTemp = 22.5
        return stats
    }

    /// プレビュー用の週次データ
    static var weeklyPreview: [TeslaEnergyStats] {
        let calendar = Calendar.current
        var stats: [TeslaEnergyStats] = []

        for i in 0..<7 {
            guard let date = calendar.date(byAdding: .day, value: -i, to: Date()) else { continue }

            let stat = TeslaEnergyStats(periodType: .daily, date: date)
            stat.distanceKm = Double.random(in: 20...100)
            stat.energyConsumedKWh = stat.distanceKm * 0.18
            stat.energyChargedKWh = Double.random(in: 0...30)
            stat.drivingMinutes = Int(stat.distanceKm * 1.5)
            stat.tripCount = Int.random(in: 1...5)
            stat.averageEfficiency = Double.random(in: 150...200)

            stats.append(stat)
        }

        return stats
    }

    /// プレビュー用の月次サマリー
    static var monthlyPreview: TeslaEnergyStats {
        let stats = TeslaEnergyStats(periodType: .monthly)
        stats.distanceKm = 2150.5
        stats.energyConsumedKWh = 380.2
        stats.energyChargedKWh = 420.0
        stats.energyRegeneratedKWh = 52.1
        stats.drivingMinutes = 3600
        stats.tripCount = 62
        stats.chargeCount = 15
        stats.superchargerCount = 3
        stats.homeChargeCount = 12
        stats.chargingMinutes = 2700
        stats.averageEfficiency = 177
        stats.chargingCost = 12600
        stats.electricityRate = 30
        return stats
    }
}
#endif
