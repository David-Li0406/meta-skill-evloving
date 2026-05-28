# ジオコーディング

CLGeocoderを使用した住所⇔座標変換。

## CLGeocoder

### 基本

```swift
let geocoder = CLGeocoder()
```

**注意:** 同一インスタンスで同時に複数のリクエストは不可。新しいリクエストは前のリクエストをキャンセルします。

## Forward Geocoding（住所 → 座標）

### 基本実装

```swift
func geocode(address: String) async throws -> CLLocationCoordinate2D {
    let geocoder = CLGeocoder()
    let placemarks = try await geocoder.geocodeAddressString(address)

    guard let location = placemarks.first?.location else {
        throw GeocodingError.noResults
    }

    return location.coordinate
}
```

### 地域を指定

```swift
func geocode(address: String, in region: CLCircularRegion) async throws -> CLLocationCoordinate2D {
    let geocoder = CLGeocoder()
    let placemarks = try await geocoder.geocodeAddressString(address, in: region)

    guard let location = placemarks.first?.location else {
        throw GeocodingError.noResults
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
        throw GeocodingError.noResults
    }

    return location.coordinate
}
```

## Reverse Geocoding（座標 → 住所）

### 基本実装

```swift
func reverseGeocode(coordinate: CLLocationCoordinate2D) async throws -> String {
    let geocoder = CLGeocoder()
    let location = CLLocation(latitude: coordinate.latitude, longitude: coordinate.longitude)
    let placemarks = try await geocoder.reverseGeocodeLocation(location)

    guard let placemark = placemarks.first else {
        throw GeocodingError.noResults
    }

    return formatAddress(placemark)
}

private func formatAddress(_ placemark: CLPlacemark) -> String {
    var components: [String] = []

    if let country = placemark.country {
        components.append(country)
    }
    if let administrativeArea = placemark.administrativeArea {
        components.append(administrativeArea)
    }
    if let locality = placemark.locality {
        components.append(locality)
    }
    if let subLocality = placemark.subLocality {
        components.append(subLocality)
    }
    if let thoroughfare = placemark.thoroughfare {
        components.append(thoroughfare)
    }
    if let subThoroughfare = placemark.subThoroughfare {
        components.append(subThoroughfare)
    }

    return components.joined(separator: " ")
}
```

### ロケールを指定

```swift
func reverseGeocode(coordinate: CLLocationCoordinate2D, locale: Locale) async throws -> CLPlacemark {
    let geocoder = CLGeocoder()
    let location = CLLocation(latitude: coordinate.latitude, longitude: coordinate.longitude)
    let placemarks = try await geocoder.reverseGeocodeLocation(location, preferredLocale: locale)

    guard let placemark = placemarks.first else {
        throw GeocodingError.noResults
    }

    return placemark
}
```

## CLPlacemark プロパティ

| プロパティ | 説明 | 例 |
|-----------|------|---|
| `name` | 場所の名前 | "東京タワー" |
| `thoroughfare` | 通り名 | "芝公園" |
| `subThoroughfare` | 番地 | "4-2-8" |
| `locality` | 市区町村 | "港区" |
| `subLocality` | 地区 | "芝公園" |
| `administrativeArea` | 都道府県 | "東京都" |
| `subAdministrativeArea` | 郡 | - |
| `postalCode` | 郵便番号 | "105-0011" |
| `country` | 国 | "日本" |
| `isoCountryCode` | 国コード | "JP" |
| `timeZone` | タイムゾーン | "Asia/Tokyo" |
| `location` | CLLocation | - |
| `areasOfInterest` | 関連する場所 | ["東京タワー"] |

## 日本語住所の処理

### フォーマット例

```swift
func formatJapaneseAddress(_ placemark: CLPlacemark) -> String {
    var components: [String] = []

    // 日本式の住所表記（大→小）
    if let postalCode = placemark.postalCode {
        components.append("〒\(postalCode)")
    }
    if let administrativeArea = placemark.administrativeArea {
        components.append(administrativeArea)
    }
    if let locality = placemark.locality {
        components.append(locality)
    }
    if let subLocality = placemark.subLocality {
        components.append(subLocality)
    }
    if let thoroughfare = placemark.thoroughfare {
        components.append(thoroughfare)
    }
    if let subThoroughfare = placemark.subThoroughfare {
        components.append(subThoroughfare)
    }

    return components.joined()
}
```

## レート制限対策

CLGeocoderにはAppleによるレート制限があります。

### ベストプラクティス

```swift
actor GeocodingService {
    private let geocoder = CLGeocoder()
    private var lastRequestTime: Date?
    private let minimumInterval: TimeInterval = 0.5  // 500ms

    func geocode(address: String) async throws -> CLLocationCoordinate2D {
        // レート制限対策
        if let lastTime = lastRequestTime {
            let elapsed = Date().timeIntervalSince(lastTime)
            if elapsed < minimumInterval {
                try await Task.sleep(nanoseconds: UInt64((minimumInterval - elapsed) * 1_000_000_000))
            }
        }

        lastRequestTime = Date()

        let placemarks = try await geocoder.geocodeAddressString(address)

        guard let location = placemarks.first?.location else {
            throw GeocodingError.noResults
        }

        return location.coordinate
    }
}
```

### キャッシュ実装

```swift
actor GeocodingCache {
    private var cache: [String: CLLocationCoordinate2D] = [:]
    private let geocoder = CLGeocoder()

    func geocode(address: String) async throws -> CLLocationCoordinate2D {
        // キャッシュ確認
        if let cached = cache[address] {
            return cached
        }

        let placemarks = try await geocoder.geocodeAddressString(address)

        guard let location = placemarks.first?.location else {
            throw GeocodingError.noResults
        }

        let coordinate = location.coordinate
        cache[address] = coordinate

        return coordinate
    }
}
```

## エラーハンドリング

### CLError コード

| コード | 説明 | 対処 |
|-------|------|------|
| `.geocodeCanceled` | キャンセルされた | - |
| `.geocodeFoundNoResult` | 結果なし | 入力を確認 |
| `.geocodeFoundPartialResult` | 部分的な結果 | 結果を確認 |
| `.network` | ネットワークエラー | リトライ |

### エラーハンドリング例

```swift
func geocode(address: String) async throws -> CLLocationCoordinate2D {
    do {
        let geocoder = CLGeocoder()
        let placemarks = try await geocoder.geocodeAddressString(address)

        guard let location = placemarks.first?.location else {
            throw GeocodingError.noResults
        }

        return location.coordinate
    } catch let error as CLError {
        switch error.code {
        case .geocodeCanceled:
            throw GeocodingError.cancelled
        case .geocodeFoundNoResult:
            throw GeocodingError.noResults
        case .network:
            throw GeocodingError.networkError
        default:
            throw GeocodingError.unknown(error)
        }
    }
}

enum GeocodingError: Error {
    case noResults
    case cancelled
    case networkError
    case unknown(Error)
}
```

## 使用上の注意

1. **レート制限** - 短時間に多数のリクエストを送らない
2. **キャッシュ** - 同じ住所の繰り返しリクエストはキャッシュ
3. **ネットワーク** - オフライン時は失敗する
4. **精度** - 結果は常に100%正確ではない
5. **言語** - ロケール設定で結果の言語が変わる
