# Core Location Reference

Core Locationフレームワークを使用した位置情報取得の詳細ガイド。

## CLLocationManager

位置情報サービスの中心となるクラス。

### 初期化と設定

```swift
@MainActor
@Observable
final class LocationManager: NSObject, CLLocationManagerDelegate {
    var location: CLLocation?
    var heading: CLHeading?
    var authorizationStatus: CLAuthorizationStatus = .notDetermined
    var isUpdating = false

    private let manager = CLLocationManager()

    override init() {
        super.init()
        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyBest
        manager.distanceFilter = 10  // 10メートルごとに更新
        authorizationStatus = manager.authorizationStatus
    }
}
```

### 精度設定

| 定数 | 精度 | バッテリー消費 | 用途 |
|------|------|--------------|------|
| `kCLLocationAccuracyBestForNavigation` | 最高 | 最大 | ナビゲーション |
| `kCLLocationAccuracyBest` | 高 | 大 | 一般的な位置追跡 |
| `kCLLocationAccuracyNearestTenMeters` | 10m | 中 | 周辺検索 |
| `kCLLocationAccuracyHundredMeters` | 100m | 小 | 地域特定 |
| `kCLLocationAccuracyKilometer` | 1km | 最小 | 都市レベル |
| `kCLLocationAccuracyThreeKilometers` | 3km | 最小 | 国/地域レベル |
| `kCLLocationAccuracyReduced` | 可変 | 最小 | プライバシー重視 |

### 距離フィルター

```swift
// 更新間隔（メートル）
manager.distanceFilter = 10  // 10m移動ごとに更新
manager.distanceFilter = kCLDistanceFilterNone  // 全ての更新を受信
```

## 位置情報の取得

### 継続的な更新

```swift
func startUpdating() {
    guard authorizationStatus == .authorizedWhenInUse ||
          authorizationStatus == .authorizedAlways else {
        return
    }

    isUpdating = true
    manager.startUpdatingLocation()
}

func stopUpdating() {
    isUpdating = false
    manager.stopUpdatingLocation()
}

// デリゲートメソッド
nonisolated func locationManager(
    _ manager: CLLocationManager,
    didUpdateLocations locations: [CLLocation]
) {
    Task { @MainActor in
        location = locations.last
    }
}
```

### 一回限りの位置取得

```swift
func requestLocation() {
    manager.requestLocation()
}

// didUpdateLocations または didFailWithError が呼ばれる
```

### async/await パターン

```swift
func getCurrentLocation() async throws -> CLLocation {
    return try await withCheckedThrowingContinuation { continuation in
        locationContinuation = continuation
        manager.requestLocation()
    }
}

nonisolated func locationManager(
    _ manager: CLLocationManager,
    didUpdateLocations locations: [CLLocation]
) {
    Task { @MainActor in
        if let continuation = locationContinuation,
           let location = locations.last {
            continuation.resume(returning: location)
            locationContinuation = nil
        }
        location = locations.last
    }
}

nonisolated func locationManager(
    _ manager: CLLocationManager,
    didFailWithError error: Error
) {
    Task { @MainActor in
        if let continuation = locationContinuation {
            continuation.resume(throwing: error)
            locationContinuation = nil
        }
    }
}
```

## CLLocation

位置情報データを格納するクラス。

### 主要プロパティ

```swift
let location: CLLocation

// 座標
location.coordinate.latitude   // 緯度
location.coordinate.longitude  // 経度

// 高度
location.altitude              // メートル単位
location.ellipsoidalAltitude   // 楕円体高度

// 精度
location.horizontalAccuracy    // 水平精度（メートル）
location.verticalAccuracy      // 垂直精度（メートル）

// 速度と方向
location.speed                 // m/s
location.course                // 0-360度（北基準）

// タイムスタンプ
location.timestamp             // Date
```

### 距離計算

```swift
let distance = location1.distance(from: location2)  // メートル
```

### 位置の有効性チェック

```swift
// 精度が負の場合は無効
if location.horizontalAccuracy >= 0 {
    // 有効な位置情報
}

// 古すぎるデータをフィルタ
let age = Date().timeIntervalSince(location.timestamp)
if age < 60 {  // 60秒以内
    // 新鮮な位置情報
}
```

## Heading（方位）

デバイスの向きを取得。

### Heading更新の開始

```swift
func startUpdatingHeading() {
    guard CLLocationManager.headingAvailable() else { return }
    manager.startUpdatingHeading()
}

func stopUpdatingHeading() {
    manager.stopUpdatingHeading()
}

nonisolated func locationManager(
    _ manager: CLLocationManager,
    didUpdateHeading newHeading: CLHeading
) {
    Task { @MainActor in
        heading = newHeading
    }
}
```

### CLHeading プロパティ

```swift
let heading: CLHeading

// 磁北基準の方位
heading.magneticHeading  // 0-360度

// 真北基準の方位（位置情報が必要）
heading.trueHeading      // 0-360度（位置情報不可時は負の値）

// 精度
heading.headingAccuracy  // 度単位

// 生データ
heading.x  // X軸磁場
heading.y  // Y軸磁場
heading.z  // Z軸磁場
```

## バックグラウンド位置情報

### 設定

```swift
// バックグラウンド更新を許可
manager.allowsBackgroundLocationUpdates = true

// インジケーター表示（ブルーバー）
manager.showsBackgroundLocationIndicator = true

// バックグラウンドでの自動一時停止を無効化
manager.pausesLocationUpdatesAutomatically = false
```

### Info.plist設定

```xml
<key>UIBackgroundModes</key>
<array>
    <string>location</string>
</array>

<key>NSLocationAlwaysAndWhenInUseUsageDescription</key>
<string>バックグラウンドでのナビゲーションのために位置情報を使用します。</string>
```

### バッテリー効率化

```swift
// 重要な位置変更のみ監視（バッテリー効率的）
manager.startMonitoringSignificantLocationChanges()
manager.stopMonitoringSignificantLocationChanges()

// アクティビティタイプを指定（システムが最適化）
manager.activityType = .automotiveNavigation  // 車
manager.activityType = .fitness               // 運動
manager.activityType = .otherNavigation       // その他のナビ
```

## Region Monitoring（ジオフェンス）

特定の地域への出入りを監視。

### 設定

```swift
func startMonitoring(region: CLCircularRegion) {
    guard CLLocationManager.isMonitoringAvailable(for: CLCircularRegion.self) else {
        return
    }

    let region = CLCircularRegion(
        center: CLLocationCoordinate2D(latitude: 35.6762, longitude: 139.6503),
        radius: 100,  // メートル（最大は CLLocationDistance(maximumRegionMonitoringDistance)）
        identifier: "Tokyo"
    )

    region.notifyOnEntry = true
    region.notifyOnExit = true

    manager.startMonitoring(for: region)
}
```

### デリゲートメソッド

```swift
nonisolated func locationManager(
    _ manager: CLLocationManager,
    didEnterRegion region: CLRegion
) {
    Task { @MainActor in
        handleRegionEntry(region)
    }
}

nonisolated func locationManager(
    _ manager: CLLocationManager,
    didExitRegion region: CLRegion
) {
    Task { @MainActor in
        handleRegionExit(region)
    }
}

nonisolated func locationManager(
    _ manager: CLLocationManager,
    monitoringDidFailFor region: CLRegion?,
    withError error: Error
) {
    Task { @MainActor in
        handleMonitoringError(region, error)
    }
}
```

## Visit Monitoring

ユーザーが滞在した場所を検出。

```swift
func startMonitoringVisits() {
    manager.startMonitoringVisits()
}

nonisolated func locationManager(
    _ manager: CLLocationManager,
    didVisit visit: CLVisit
) {
    Task { @MainActor in
        // visit.coordinate - 滞在した場所
        // visit.arrivalDate - 到着時刻
        // visit.departureDate - 出発時刻
        // visit.horizontalAccuracy - 精度
        handleVisit(visit)
    }
}
```

## エラーハンドリング

### CLError コード

| コード | 名前 | 説明 |
|--------|------|------|
| 0 | `locationUnknown` | 位置を特定できない |
| 1 | `denied` | 権限が拒否された |
| 2 | `network` | ネットワークエラー |
| 3 | `headingFailure` | 方位を特定できない |
| 4 | `regionMonitoringDenied` | 地域監視が拒否された |
| 5 | `regionMonitoringFailure` | 地域監視に失敗 |
| 6 | `regionMonitoringSetupDelayed` | 地域監視のセットアップが遅延 |
| 7 | `regionMonitoringResponseDelayed` | 地域監視の応答が遅延 |
| 8 | `geocodeFoundNoResult` | ジオコーディング結果なし |
| 9 | `geocodeFoundPartialResult` | 部分的な結果 |
| 10 | `geocodeCanceled` | ジオコーディングがキャンセル |

### エラー処理パターン

```swift
nonisolated func locationManager(
    _ manager: CLLocationManager,
    didFailWithError error: Error
) {
    Task { @MainActor in
        if let clError = error as? CLError {
            switch clError.code {
            case .denied:
                // 権限が拒否された
                handlePermissionDenied()
            case .locationUnknown:
                // 一時的なエラー、リトライ可能
                retryLocationRequest()
            case .network:
                // ネットワークエラー
                handleNetworkError()
            default:
                handleOtherError(clError)
            }
        }
    }
}
```

## CLLocationCoordinate2D 拡張

便利な拡張を定義。

```swift
extension CLLocationCoordinate2D {
    // 東京駅
    static let tokyoStation = CLLocationCoordinate2D(
        latitude: 35.6812,
        longitude: 139.7671
    )

    // 渋谷駅
    static let shibuyaStation = CLLocationCoordinate2D(
        latitude: 35.6580,
        longitude: 139.7016
    )

    // 有効性チェック
    var isValid: Bool {
        CLLocationCoordinate2DIsValid(self)
    }
}
```

## Sendable対応

iOS 17+ Swift Concurrency対応。

```swift
// CLLocation は Sendable
// CLLocationCoordinate2D は Sendable

// CLLocationManagerDelegate のメソッドは nonisolated
nonisolated func locationManager(
    _ manager: CLLocationManager,
    didUpdateLocations locations: [CLLocation]
) {
    Task { @MainActor in
        // MainActor に移行して UI を更新
        self.location = locations.last
    }
}
```

## パフォーマンス最適化

### バッテリー消費を抑える

```swift
// 必要な精度のみ要求
manager.desiredAccuracy = kCLLocationAccuracyHundredMeters

// 距離フィルターを設定
manager.distanceFilter = 50  // 50m以上移動したら更新

// 不要な時は更新を停止
func onDisappear() {
    manager.stopUpdatingLocation()
}

// アクティビティタイプを指定
manager.activityType = .fitness
```

### メモリ管理

```swift
// 古い位置情報を保持しない
var recentLocations: [CLLocation] = []

func locationManager(
    _ manager: CLLocationManager,
    didUpdateLocations locations: [CLLocation]
) {
    // 最新の数件のみ保持
    recentLocations = Array(locations.suffix(10))
}
```
