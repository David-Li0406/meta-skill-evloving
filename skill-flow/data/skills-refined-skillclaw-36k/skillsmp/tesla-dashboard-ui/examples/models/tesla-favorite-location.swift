// Tesla Dashboard UI - Favorite Location Model
// SwiftData @Model によるお気に入り地点の永続化
// ナビゲーション用のブックマーク機能

import Foundation
import SwiftData
import CoreLocation

// MARK: - Tesla Favorite Location Model

/// お気に入り地点モデル（SwiftData永続化）
@Model
final class TeslaFavoriteLocation {
    // MARK: - Identifiers

    /// 地点ID
    @Attribute(.unique)
    var locationId: String

    /// 表示名
    var name: String

    // MARK: - Location Data

    /// 緯度
    var latitude: Double

    /// 経度
    var longitude: Double

    /// 住所
    var address: String?

    /// 郵便番号
    var postalCode: String?

    /// 都道府県
    var prefecture: String?

    /// 市区町村
    var city: String?

    // MARK: - Categorization

    /// カテゴリ
    var category: String

    /// カスタムアイコン名
    var iconName: String?

    /// 色（HEX）
    var colorHex: String?

    // MARK: - Metadata

    /// メモ
    var notes: String?

    /// 訪問回数
    var visitCount: Int

    /// 最終訪問日
    var lastVisitedAt: Date?

    /// お気に入り順序
    var sortOrder: Int

    /// 非表示フラグ
    var isHidden: Bool

    // MARK: - Charging Info (if applicable)

    /// 充電スポットかどうか
    var isChargingStation: Bool

    /// 充電器タイプ
    var chargerType: String?

    /// 充電出力（kW）
    var chargerPower: Double?

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
        locationId: String = UUID().uuidString,
        name: String,
        latitude: Double,
        longitude: Double,
        address: String? = nil,
        category: LocationCategory = .other,
        notes: String? = nil
    ) {
        self.locationId = locationId
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.category = category.rawValue
        self.notes = notes
        self.visitCount = 0
        self.sortOrder = 0
        self.isHidden = false
        self.isChargingStation = false
        self.createdAt = Date()
        self.updatedAt = Date()
    }
}

// MARK: - Location Category

/// 地点カテゴリ
enum LocationCategory: String, Codable, CaseIterable {
    case home = "home"
    case work = "work"
    case charging = "charging"
    case shopping = "shopping"
    case restaurant = "restaurant"
    case parking = "parking"
    case other = "other"

    var displayName: String {
        switch self {
        case .home: return "自宅"
        case .work: return "職場"
        case .charging: return "充電スポット"
        case .shopping: return "買い物"
        case .restaurant: return "飲食店"
        case .parking: return "駐車場"
        case .other: return "その他"
        }
    }

    var icon: TeslaIcon {
        switch self {
        case .home: return .home
        case .work: return .location
        case .charging: return .charging
        case .shopping: return .location
        case .restaurant: return .location
        case .parking: return .location
        case .other: return .location
        }
    }

    var defaultColor: String {
        switch self {
        case .home: return "#3399FF"
        case .work: return "#9966FF"
        case .charging: return "#4DD966"
        case .shopping: return "#FF9933"
        case .restaurant: return "#F24D4D"
        case .parking: return "#66B3FF"
        case .other: return "#B3B3B3"
        }
    }
}

// MARK: - Computed Properties

extension TeslaFavoriteLocation {
    /// CLLocationCoordinate2D
    var coordinate: CLLocationCoordinate2D {
        CLLocationCoordinate2D(latitude: latitude, longitude: longitude)
    }

    /// カテゴリenum
    var categoryEnum: LocationCategory {
        LocationCategory(rawValue: category) ?? .other
    }

    /// アイコン
    var icon: TeslaIcon {
        if let iconName, let customIcon = TeslaIcon(rawValue: iconName) {
            return customIcon
        }
        return categoryEnum.icon
    }

    /// 表示色
    var displayColor: String {
        colorHex ?? categoryEnum.defaultColor
    }

    /// フォーマットされた住所
    var formattedAddress: String {
        var components: [String] = []

        if let postalCode {
            components.append("〒\(postalCode)")
        }
        if let prefecture {
            components.append(prefecture)
        }
        if let city {
            components.append(city)
        }
        if let address {
            components.append(address)
        }

        return components.isEmpty ? "住所不明" : components.joined(separator: " ")
    }

    /// 短い住所
    var shortAddress: String {
        if let city {
            return city
        }
        if let prefecture {
            return prefecture
        }
        return address ?? "住所不明"
    }
}

// MARK: - Update Methods

extension TeslaFavoriteLocation {
    /// 訪問を記録
    func recordVisit() {
        visitCount += 1
        lastVisitedAt = Date()
        updatedAt = Date()
    }

    /// 位置情報を更新
    func updateLocation(latitude: Double, longitude: Double, address: String? = nil) {
        self.latitude = latitude
        self.longitude = longitude
        if let address {
            self.address = address
        }
        self.updatedAt = Date()
    }

    /// カテゴリを変更
    func updateCategory(_ newCategory: LocationCategory) {
        self.category = newCategory.rawValue
        self.updatedAt = Date()
    }

    /// 充電スポット情報を設定
    func setChargingInfo(chargerType: String, power: Double) {
        self.isChargingStation = true
        self.chargerType = chargerType
        self.chargerPower = power
        self.category = LocationCategory.charging.rawValue
        self.updatedAt = Date()
    }
}

// MARK: - SwiftData Queries

extension TeslaFavoriteLocation {
    /// 全お気に入りを取得（ソート順）
    static var allFavoritesFetch: FetchDescriptor<TeslaFavoriteLocation> {
        var descriptor = FetchDescriptor<TeslaFavoriteLocation>(
            predicate: #Predicate { !$0.isHidden },
            sortBy: [
                SortDescriptor(\.sortOrder),
                SortDescriptor(\.name)
            ]
        )
        return descriptor
    }

    /// カテゴリで絞り込み
    static func favoritesByCategory(_ category: LocationCategory) -> FetchDescriptor<TeslaFavoriteLocation> {
        let categoryRawValue = category.rawValue
        return FetchDescriptor<TeslaFavoriteLocation>(
            predicate: #Predicate { $0.category == categoryRawValue && !$0.isHidden },
            sortBy: [SortDescriptor(\.sortOrder), SortDescriptor(\.name)]
        )
    }

    /// 充電スポットのみ取得
    static var chargingStationsFetch: FetchDescriptor<TeslaFavoriteLocation> {
        FetchDescriptor<TeslaFavoriteLocation>(
            predicate: #Predicate { $0.isChargingStation && !$0.isHidden },
            sortBy: [SortDescriptor(\.name)]
        )
    }

    /// 最近訪問した地点
    static func recentlyVisited(limit: Int = 10) -> FetchDescriptor<TeslaFavoriteLocation> {
        var descriptor = FetchDescriptor<TeslaFavoriteLocation>(
            predicate: #Predicate { $0.lastVisitedAt != nil && !$0.isHidden },
            sortBy: [SortDescriptor(\.lastVisitedAt, order: .reverse)]
        )
        descriptor.fetchLimit = limit
        return descriptor
    }

    /// よく訪問する地点
    static func frequentlyVisited(limit: Int = 10) -> FetchDescriptor<TeslaFavoriteLocation> {
        var descriptor = FetchDescriptor<TeslaFavoriteLocation>(
            predicate: #Predicate { $0.visitCount > 0 && !$0.isHidden },
            sortBy: [SortDescriptor(\.visitCount, order: .reverse)]
        )
        descriptor.fetchLimit = limit
        return descriptor
    }
}

// MARK: - Preview

#if DEBUG
extension TeslaFavoriteLocation {
    /// プレビュー用のサンプルデータ
    static var preview: TeslaFavoriteLocation {
        let location = TeslaFavoriteLocation(
            name: "自宅",
            latitude: 35.6812,
            longitude: 139.7671,
            address: "東京都千代田区丸の内1-1-1",
            category: .home
        )
        location.prefecture = "東京都"
        location.city = "千代田区"
        location.postalCode = "100-0001"
        location.visitCount = 42
        location.lastVisitedAt = Date()
        return location
    }

    /// プレビュー用のリスト
    static var previewList: [TeslaFavoriteLocation] {
        [
            {
                let loc = TeslaFavoriteLocation(
                    name: "自宅",
                    latitude: 35.6812,
                    longitude: 139.7671,
                    category: .home
                )
                loc.city = "千代田区"
                loc.sortOrder = 0
                return loc
            }(),
            {
                let loc = TeslaFavoriteLocation(
                    name: "会社",
                    latitude: 35.6895,
                    longitude: 139.6917,
                    category: .work
                )
                loc.city = "新宿区"
                loc.sortOrder = 1
                return loc
            }(),
            {
                let loc = TeslaFavoriteLocation(
                    name: "Tesla 東京ベイ",
                    latitude: 35.6290,
                    longitude: 139.7763,
                    category: .charging
                )
                loc.city = "港区"
                loc.isChargingStation = true
                loc.chargerType = "Supercharger"
                loc.chargerPower = 250.0
                loc.sortOrder = 2
                return loc
            }()
        ]
    }
}
#endif
