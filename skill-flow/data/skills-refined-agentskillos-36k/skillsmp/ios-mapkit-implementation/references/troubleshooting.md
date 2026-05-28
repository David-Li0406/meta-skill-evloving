# Troubleshooting Reference

MapKitとCore Locationで発生する問題のトラブルシューティングガイド。

## 位置情報エラー

### CLError

| コード | 名前 | 説明 | 対処法 |
|--------|------|------|--------|
| 0 | `locationUnknown` | 位置を特定できない | リトライ、GPS受信状況を確認 |
| 1 | `denied` | 権限が拒否された | 設定アプリへ誘導 |
| 2 | `network` | ネットワークエラー | ネットワーク接続を確認 |
| 3 | `headingFailure` | 方位を特定できない | 磁気干渉をチェック |
| 4 | `regionMonitoringDenied` | 地域監視が拒否された | 権限を確認 |
| 5 | `regionMonitoringFailure` | 地域監視に失敗 | 地域設定を確認 |
| 8 | `geocodeFoundNoResult` | ジオコーディング結果なし | クエリを修正 |
| 10 | `geocodeCanceled` | ジオコーディングがキャンセル | 意図的でなければリトライ |

### 位置情報が取得できない

**症状:** `locationManager:didFailWithError:` が呼ばれる

**確認事項:**
1. Info.plistに権限キーが設定されているか
2. 権限がauthorizedになっているか
3. 位置情報サービスがデバイスで有効か
4. シミュレータの場合、位置がシミュレートされているか

```swift
// デバッグコード
func debugLocationStatus() {
    let manager = CLLocationManager()

    print("Location Services Enabled: \(CLLocationManager.locationServicesEnabled())")
    print("Authorization Status: \(manager.authorizationStatus.rawValue)")
    print("Accuracy Authorization: \(manager.accuracyAuthorization.rawValue)")

    if !CLLocationManager.locationServicesEnabled() {
        print("⚠️ Location Services are disabled on this device")
    }

    switch manager.authorizationStatus {
    case .notDetermined:
        print("⚠️ Authorization not requested yet")
    case .denied:
        print("❌ Authorization denied by user")
    case .restricted:
        print("❌ Authorization restricted")
    case .authorizedWhenInUse, .authorizedAlways:
        print("✅ Authorization granted")
    @unknown default:
        break
    }
}
```

### 精度が低い

**症状:** `horizontalAccuracy` が大きい値を返す

**対処法:**
```swift
// 高精度モードを設定
manager.desiredAccuracy = kCLLocationAccuracyBest

// 精度が十分な位置情報のみ使用
func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
    guard let location = locations.last else { return }

    // 精度が100m以下の場合のみ使用
    if location.horizontalAccuracy <= 100 && location.horizontalAccuracy >= 0 {
        self.location = location
    }
}
```

## MapKitエラー

### MKError

| コード | 名前 | 説明 | 対処法 |
|--------|------|------|--------|
| 1 | `unknown` | 不明なエラー | リトライ |
| 2 | `serverFailure` | サーバーエラー | しばらく待ってリトライ |
| 3 | `loadingThrottled` | リクエスト制限 | リクエスト頻度を下げる |
| 4 | `placemarkNotFound` | 場所が見つからない | クエリを修正 |
| 5 | `directionsNotFound` | 経路が見つからない | 出発地/目的地を確認 |
| 6 | `decodingFailed` | デコード失敗 | データ形式を確認 |

### 経路が見つからない

**症状:** `MKError.directionsNotFound`

**確認事項:**
1. 出発地と目的地が有効な座標か
2. 同じ地点でないか
3. 交通手段で到達可能な場所か（海上、離島など）

```swift
func calculateRouteWithFallback(
    from source: CLLocationCoordinate2D,
    to destination: CLLocationCoordinate2D
) async -> MKRoute? {
    // 車で試行
    if let route = try? await calculateRoute(from: source, to: destination, type: .automobile) {
        return route
    }

    // 徒歩で試行
    if let route = try? await calculateRoute(from: source, to: destination, type: .walking) {
        return route
    }

    return nil
}
```

### 検索結果が空

**症状:** `MKLocalSearch` が結果を返さない

**対処法:**
```swift
// 検索範囲を広げる
func searchWithExpandingRegion(query: String, center: CLLocationCoordinate2D) async -> [MKMapItem] {
    let radii: [CLLocationDistance] = [1000, 5000, 10000, 50000]

    for radius in radii {
        let region = MKCoordinateRegion(
            center: center,
            latitudinalMeters: radius,
            longitudinalMeters: radius
        )

        let request = MKLocalSearch.Request()
        request.naturalLanguageQuery = query
        request.region = region

        let search = MKLocalSearch(request: request)

        if let response = try? await search.start(), !response.mapItems.isEmpty {
            return response.mapItems
        }
    }

    return []
}
```

## シミュレータの問題

### 位置情報をシミュレート

**Xcode Menu:** Debug > Simulate Location

または、スキームで設定:
1. Edit Scheme > Run > Options
2. "Default Location" を設定

### GPXファイルを使用

```xml
<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1">
    <wpt lat="35.6812" lon="139.7671">
        <name>Tokyo Station</name>
    </wpt>
</gpx>
```

XcodeにGPXファイルをドラッグ&ドロップして使用。

### シミュレータの制限

- Look Aroundは限定的なサポート
- コンパスは動作しない
- バックグラウンド位置情報の動作が異なる

## パフォーマンス問題

### 大量のマーカーで遅い

**症状:** 数百〜数千のマーカーで地図がカクつく

**対処法:**
```swift
// クラスタリングを実装
struct ClusteredMapView: View {
    let items: [MapItem]
    @State private var clusters: [Cluster] = []
    @State private var region: MKCoordinateRegion?

    var body: some View {
        Map()
            .onMapCameraChange { context in
                region = context.region
                updateClusters()
            }
    }

    private func updateClusters() {
        guard let region else { return }

        // ズームレベルに応じてクラスタリング
        let gridSize = region.span.latitudeDelta / 10

        var grid: [String: [MapItem]] = [:]

        for item in items {
            let key = "\(Int(item.coordinate.latitude / gridSize))-\(Int(item.coordinate.longitude / gridSize))"
            grid[key, default: []].append(item)
        }

        clusters = grid.map { _, items in
            Cluster(items: items)
        }
    }
}
```

### メモリ使用量が多い

**確認事項:**
1. 不要なオーバーレイを削除しているか
2. 画像リソースを適切にキャッシュしているか
3. 位置情報の履歴を無制限に保存していないか

```swift
// メモリ効率の良い位置情報管理
class LocationHistory {
    private var locations: [CLLocation] = []
    private let maxCount = 100

    func add(_ location: CLLocation) {
        locations.append(location)

        // 古いデータを削除
        if locations.count > maxCount {
            locations.removeFirst(locations.count - maxCount)
        }
    }
}
```

### バッテリー消費が激しい

**対処法:**
```swift
// 必要最小限の精度
manager.desiredAccuracy = kCLLocationAccuracyHundredMeters

// 距離フィルターを設定
manager.distanceFilter = 50  // 50m移動ごとに更新

// 不要な時は更新を停止
func onDisappear() {
    manager.stopUpdatingLocation()
}

// 重要な位置変更のみ監視
manager.startMonitoringSignificantLocationChanges()
```

## 権限関連

### 権限が「未決定」のまま

**症状:** `authorizationStatus` が `.notDetermined` のまま変わらない

**確認事項:**
1. `requestWhenInUseAuthorization()` を呼んでいるか
2. Info.plistに説明文が設定されているか
3. デリゲートが正しく設定されているか

```swift
// デバッグ用ログ
func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
    print("Authorization changed to: \(manager.authorizationStatus.rawValue)")
}
```

### 権限ダイアログが表示されない

**確認事項:**
1. 以前に権限を拒否していないか（設定でリセット）
2. シミュレータをリセット（Simulator > Reset Content and Settings）
3. Info.plistのキーが正しいか

```xml
<!-- 正しいキー名 -->
<key>NSLocationWhenInUseUsageDescription</key>
<string>説明文</string>

<!-- 間違い: キー名のタイポ -->
<key>NSLocationWhenInUseUsageDecription</key>  <!-- typo! -->
```

## ジオコーディング

### レート制限エラー

**症状:** 連続リクエストで失敗

**対処法:**
```swift
actor RateLimitedGeocoder {
    private let geocoder = CLGeocoder()
    private var lastRequestTime: Date?
    private let minimumInterval: TimeInterval = 1.0

    func geocode(address: String) async throws -> CLLocationCoordinate2D {
        // レート制限
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

### 日本語住所で結果が得られない

**対処法:**
```swift
// ロケールを明示的に指定
func geocodeJapaneseAddress(_ address: String) async throws -> CLLocationCoordinate2D {
    let geocoder = CLGeocoder()
    let placemarks = try await geocoder.geocodeAddressString(
        address,
        in: nil,
        preferredLocale: Locale(identifier: "ja_JP")
    )

    guard let location = placemarks.first?.location else {
        throw GeocodingError.noResult
    }

    return location.coordinate
}
```

## デバッグツール

### 位置情報のログ

```swift
extension CLLocation {
    var debugDescription: String {
        """
        Location:
          Coordinate: \(coordinate.latitude), \(coordinate.longitude)
          Accuracy: \(horizontalAccuracy)m
          Altitude: \(altitude)m (accuracy: \(verticalAccuracy)m)
          Speed: \(speed)m/s
          Course: \(course)°
          Timestamp: \(timestamp)
        """
    }
}
```

### MapKit操作のログ

```swift
Map()
    .onMapCameraChange { context in
        print("Camera changed:")
        print("  Region: \(context.region)")
        print("  Camera: \(context.camera)")
    }
```

### ネットワークモニタリング

```swift
import Network

class NetworkMonitor: ObservableObject {
    private let monitor = NWPathMonitor()
    @Published var isConnected = true

    init() {
        monitor.pathUpdateHandler = { [weak self] path in
            DispatchQueue.main.async {
                self?.isConnected = path.status == .satisfied
            }
        }
        monitor.start(queue: DispatchQueue.global())
    }

    deinit {
        monitor.cancel()
    }
}
```

## よくある問題と解決策

### 地図が表示されない

1. ネットワーク接続を確認
2. Apple Mapsサービスのステータスを確認
3. デバイスの日時設定を確認

### マーカーが表示されない

1. 座標が有効か確認（`CLLocationCoordinate2DIsValid`）
2. 座標が地図の表示範囲内か確認
3. Markerの初期化が正しいか確認

### カメラが動かない

1. `position` がバインディングになっているか確認
2. `interactionModes` が制限されていないか確認
3. `bounds` が設定されていないか確認

### Look Aroundが表示されない

1. その場所でLook Aroundが利用可能か確認
2. シミュレータでは限定的なサポート
3. ネットワーク接続を確認
