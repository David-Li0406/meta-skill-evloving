# Geocoding Reference

CLGeocoderを使用した住所と座標の相互変換ガイド。

## CLGeocoder

ジオコーディング（住所→座標）とリバースジオコーディング（座標→住所）を実行。

### 基本的な使用

```swift
let geocoder = CLGeocoder()
```

**重要な注意点:**
- ネットワーク接続が必要
- レート制限あり（短時間に多数のリクエストは失敗する可能性）
- 一度に1つのジオコーディングリクエストのみ
- 結果はキャッシュすることを推奨

## Forward Geocoding（住所 → 座標）

### 基本的な使用

```swift
func geocode(address: String) async throws -> CLLocationCoordinate2D {
    let geocoder = CLGeocoder()
    let placemarks = try await geocoder.geocodeAddressString(address)

    guard let location = placemarks.first?.location else {
        throw GeocodingError.noResult
    }

    return location.coordinate
}
```

### 地域を限定してジオコーディング

```swift
func geocode(address: String, in region: CLCircularRegion) async throws -> CLLocationCoordinate2D {
    let geocoder = CLGeocoder()
    let placemarks = try await geocoder.geocodeAddressString(
        address,
        in: region
    )

    guard let location = placemarks.first?.location else {
        throw GeocodingError.noResult
    }

    return location.coordinate
}
```

### ロケールを指定

```swift
func geocode(address: String, locale: Locale) async throws -> CLLocationCoordinate2D {
    let geocoder = CLGeocoder()
    let placemarks = try await geocoder.geocodeAddressString(
        address,
        in: nil,
        preferredLocale: locale
    )

    guard let location = placemarks.first?.location else {
        throw GeocodingError.noResult
    }

    return location.coordinate
}

// 日本語ロケールで検索
let coordinate = try await geocode(address: "東京駅", locale: Locale(identifier: "ja_JP"))
```

## Reverse Geocoding（座標 → 住所）

### 基本的な使用

```swift
func reverseGeocode(coordinate: CLLocationCoordinate2D) async throws -> String {
    let geocoder = CLGeocoder()
    let location = CLLocation(
        latitude: coordinate.latitude,
        longitude: coordinate.longitude
    )
    let placemarks = try await geocoder.reverseGeocodeLocation(location)

    guard let placemark = placemarks.first else {
        throw GeocodingError.noResult
    }

    return formatAddress(placemark)
}

private func formatAddress(_ placemark: CLPlacemark) -> String {
    // 日本の住所形式
    return [
        placemark.postalCode,
        placemark.administrativeArea,  // 都道府県
        placemark.locality,            // 市区町村
        placemark.thoroughfare,        // 町名
        placemark.subThoroughfare      // 番地
    ]
    .compactMap { $0 }
    .joined(separator: " ")
}
```

### ロケールを指定

```swift
func reverseGeocode(
    coordinate: CLLocationCoordinate2D,
    locale: Locale
) async throws -> CLPlacemark {
    let geocoder = CLGeocoder()
    let location = CLLocation(
        latitude: coordinate.latitude,
        longitude: coordinate.longitude
    )
    let placemarks = try await geocoder.reverseGeocodeLocation(
        location,
        preferredLocale: locale
    )

    guard let placemark = placemarks.first else {
        throw GeocodingError.noResult
    }

    return placemark
}
```

## CLPlacemark

ジオコーディング結果を格納するクラス。

### 主要プロパティ

```swift
let placemark: CLPlacemark

// 位置情報
placemark.location           // CLLocation
placemark.region             // CLRegion?
placemark.timeZone           // TimeZone?

// 住所コンポーネント
placemark.name               // 場所の名前
placemark.thoroughfare       // 通り名（日本: 町名）
placemark.subThoroughfare    // 番地
placemark.locality           // 市区町村
placemark.subLocality        // 地区
placemark.administrativeArea // 都道府県
placemark.subAdministrativeArea // 郡
placemark.postalCode         // 郵便番号
placemark.country            // 国名
placemark.isoCountryCode     // 国コード（JP, US等）

// 海域・水域
placemark.ocean              // 海洋名
placemark.inlandWater        // 内陸水域名

// POI情報
placemark.areasOfInterest    // [String]? 近くのランドマーク
```

### 住所フォーマット

```swift
// 日本語住所形式
func formatJapaneseAddress(_ placemark: CLPlacemark) -> String {
    return [
        placemark.postalCode.map { "〒\($0)" },
        placemark.administrativeArea,
        placemark.locality,
        placemark.subLocality,
        placemark.thoroughfare,
        placemark.subThoroughfare
    ]
    .compactMap { $0 }
    .joined()
}

// 例: 〒100-0001東京都千代田区千代田1-1
```

```swift
// 英語（欧米）住所形式
func formatWesternAddress(_ placemark: CLPlacemark) -> String {
    return [
        [placemark.subThoroughfare, placemark.thoroughfare]
            .compactMap { $0 }
            .joined(separator: " "),
        placemark.locality,
        [placemark.administrativeArea, placemark.postalCode]
            .compactMap { $0 }
            .joined(separator: " "),
        placemark.country
    ]
    .compactMap { $0?.isEmpty == false ? $0 : nil }
    .joined(separator: ", ")
}

// 例: 1600 Amphitheatre Parkway, Mountain View, CA 94043, United States
```

## 複数結果の処理

```swift
func geocodeWithMultipleResults(address: String) async throws -> [CLPlacemark] {
    let geocoder = CLGeocoder()
    return try await geocoder.geocodeAddressString(address)
}

// 使用例
let placemarks = try await geocodeWithMultipleResults(address: "渋谷")
for placemark in placemarks {
    if let location = placemark.location {
        print("\(placemark.name ?? "Unknown"): \(location.coordinate)")
    }
}
```

## エラーハンドリング

### CLError.Code

| コード | 名前 | 説明 |
|--------|------|------|
| 8 | `geocodeFoundNoResult` | 結果が見つからない |
| 9 | `geocodeFoundPartialResult` | 部分的な結果のみ |
| 10 | `geocodeCanceled` | キャンセルされた |
| 2 | `network` | ネットワークエラー |

### エラー処理パターン

```swift
func geocodeSafely(address: String) async -> Result<CLLocationCoordinate2D, GeocodingError> {
    let geocoder = CLGeocoder()

    do {
        let placemarks = try await geocoder.geocodeAddressString(address)

        guard let location = placemarks.first?.location else {
            return .failure(.noResult)
        }

        return .success(location.coordinate)
    } catch let error as CLError {
        switch error.code {
        case .geocodeFoundNoResult:
            return .failure(.noResult)
        case .geocodeFoundPartialResult:
            return .failure(.partialResult)
        case .geocodeCanceled:
            return .failure(.canceled)
        case .network:
            return .failure(.networkError)
        default:
            return .failure(.unknown(error))
        }
    } catch {
        return .failure(.unknown(error))
    }
}

enum GeocodingError: Error {
    case noResult
    case partialResult
    case canceled
    case networkError
    case unknown(Error)
}
```

## キャンセル

```swift
class GeocodingService {
    private var geocoder = CLGeocoder()

    func geocode(address: String) async throws -> CLLocationCoordinate2D {
        // 進行中のリクエストをキャンセル
        geocoder.cancelGeocode()

        let placemarks = try await geocoder.geocodeAddressString(address)

        guard let location = placemarks.first?.location else {
            throw GeocodingError.noResult
        }

        return location.coordinate
    }

    func cancel() {
        geocoder.cancelGeocode()
    }
}
```

## キャッシュ実装

レート制限対策とパフォーマンス向上のためのキャッシュ。

```swift
actor GeocodingCache {
    private var forwardCache: [String: CLLocationCoordinate2D] = [:]
    private var reverseCache: [String: CLPlacemark] = [:]

    private let geocoder = CLGeocoder()

    func geocode(address: String) async throws -> CLLocationCoordinate2D {
        // キャッシュを確認
        if let cached = forwardCache[address] {
            return cached
        }

        // ジオコーディング実行
        let placemarks = try await geocoder.geocodeAddressString(address)

        guard let location = placemarks.first?.location else {
            throw GeocodingError.noResult
        }

        // キャッシュに保存
        forwardCache[address] = location.coordinate

        return location.coordinate
    }

    func reverseGeocode(coordinate: CLLocationCoordinate2D) async throws -> CLPlacemark {
        let key = "\(coordinate.latitude),\(coordinate.longitude)"

        // キャッシュを確認
        if let cached = reverseCache[key] {
            return cached
        }

        // リバースジオコーディング実行
        let location = CLLocation(
            latitude: coordinate.latitude,
            longitude: coordinate.longitude
        )
        let placemarks = try await geocoder.reverseGeocodeLocation(location)

        guard let placemark = placemarks.first else {
            throw GeocodingError.noResult
        }

        // キャッシュに保存
        reverseCache[key] = placemark

        return placemark
    }

    func clearCache() {
        forwardCache.removeAll()
        reverseCache.removeAll()
    }
}
```

## ベストプラクティス

### レート制限対策

```swift
actor ThrottledGeocoder {
    private let geocoder = CLGeocoder()
    private var lastRequestTime: Date?
    private let minimumInterval: TimeInterval = 1.0  // 1秒間隔

    func geocode(address: String) async throws -> CLLocationCoordinate2D {
        // 前回のリクエストからの経過時間を確認
        if let lastTime = lastRequestTime {
            let elapsed = Date().timeIntervalSince(lastTime)
            if elapsed < minimumInterval {
                try await Task.sleep(for: .seconds(minimumInterval - elapsed))
            }
        }

        lastRequestTime = Date()

        let placemarks = try await geocoder.geocodeAddressString(address)

        guard let location = placemarks.first?.location else {
            throw GeocodingError.noResult
        }

        return location.coordinate
    }
}
```

### バッチ処理

```swift
func geocodeBatch(addresses: [String]) async -> [String: CLLocationCoordinate2D] {
    var results: [String: CLLocationCoordinate2D] = [:]
    let geocoder = CLGeocoder()

    for address in addresses {
        do {
            let placemarks = try await geocoder.geocodeAddressString(address)
            if let location = placemarks.first?.location {
                results[address] = location.coordinate
            }
            // レート制限対策
            try await Task.sleep(for: .seconds(0.5))
        } catch {
            continue
        }
    }

    return results
}
```

### オフラインフォールバック

```swift
func geocodeWithFallback(address: String) async -> CLLocationCoordinate2D? {
    // オンラインジオコーディングを試行
    do {
        return try await geocode(address: address)
    } catch {
        // オフラインの場合、ローカルキャッシュから検索
        return localCache[address]
    }
}
```
