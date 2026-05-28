# Core Location (macOS)

macOS向けCore Location統合の詳細ガイド。

## CLLocationManager

### 基本設定

```swift
let manager = CLLocationManager()
manager.delegate = self
manager.desiredAccuracy = kCLLocationAccuracyBest
manager.distanceFilter = 10  // 10メートルごとに更新
```

### 精度定数

| 定数 | 精度 | 用途 |
|-----|-----|------|
| `kCLLocationAccuracyBestForNavigation` | 最高精度 | ナビゲーション |
| `kCLLocationAccuracyBest` | 高精度 | 一般的な用途 |
| `kCLLocationAccuracyNearestTenMeters` | 10m | 周辺検索 |
| `kCLLocationAccuracyHundredMeters` | 100m | 都市レベル |
| `kCLLocationAccuracyKilometer` | 1km | 地域レベル |
| `kCLLocationAccuracyThreeKilometers` | 3km | 大まかな位置 |

## macOS CLAuthorizationStatus

| ステータス | 値 | macOSでの意味 |
|-----------|---|--------------|
| `.notDetermined` | 0 | 未決定 |
| `.restricted` | 1 | 制限（ペアレンタルコントロール等） |
| `.denied` | 2 | 拒否 |
| `.authorized` | 3 | 許可（macOS主要） |
| `.authorizedAlways` | 3 | 常時許可（.authorizedと同値） |

**重要:** macOSでは`.authorizedWhenInUse`は利用不可。

## 権限リクエスト

```swift
// 権限リクエスト
manager.requestWhenInUseAuthorization()

// 状態確認
let status = manager.authorizationStatus

// デリゲートで変更を監視
func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
    switch manager.authorizationStatus {
    case .authorized, .authorizedAlways:
        // 許可された
        manager.startUpdatingLocation()
    case .denied:
        // 拒否された
        openLocationSettings()
    case .restricted:
        // 制限されている
        break
    case .notDetermined:
        // 未決定
        break
    @unknown default:
        break
    }
}
```

## 位置情報取得

### 継続的な更新

```swift
// 開始
manager.startUpdatingLocation()

// 停止
manager.stopUpdatingLocation()

// デリゲート
func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
    guard let location = locations.last else { return }
    // location を使用
}
```

### 一回だけ取得

```swift
manager.requestLocation()
```

### async/await パターン

```swift
func getCurrentLocation() async throws -> CLLocation {
    return try await withCheckedThrowingContinuation { continuation in
        locationContinuation = continuation
        manager.requestLocation()
    }
}

// デリゲートで完了
func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
    if let location = locations.last, let continuation = locationContinuation {
        continuation.resume(returning: location)
        locationContinuation = nil
    }
}

func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
    if let continuation = locationContinuation {
        continuation.resume(throwing: error)
        locationContinuation = nil
    }
}
```

## CLLocation プロパティ

| プロパティ | 型 | 説明 |
|-----------|---|------|
| `coordinate` | `CLLocationCoordinate2D` | 緯度経度 |
| `altitude` | `CLLocationDistance` | 高度（メートル） |
| `horizontalAccuracy` | `CLLocationAccuracy` | 水平精度（メートル） |
| `verticalAccuracy` | `CLLocationAccuracy` | 垂直精度（メートル） |
| `speed` | `CLLocationSpeed` | 速度（m/s） |
| `course` | `CLLocationDirection` | 進行方向（度） |
| `timestamp` | `Date` | タイムスタンプ |
| `floor` | `CLFloor?` | フロア情報 |

## Significant Location Changes

大きな位置変化時のみ通知（バッテリー節約）。

```swift
// 開始
manager.startMonitoringSignificantLocationChanges()

// 停止
manager.stopMonitoringSignificantLocationChanges()
```

**注意:** macOSでは通常のデスクトップアプリでは使用頻度が低い。

## Heading（方位）

```swift
// 利用可能か確認
if CLLocationManager.headingAvailable() {
    manager.startUpdatingHeading()
}

// デリゲート
func locationManager(_ manager: CLLocationManager, didUpdateHeading newHeading: CLHeading) {
    let magneticHeading = newHeading.magneticHeading  // 磁北
    let trueHeading = newHeading.trueHeading          // 真北
}
```

**注意:** macOSでは一部のMacでのみ利用可能。

## Region Monitoring（ジオフェンス）

```swift
// 利用可能か確認
if CLLocationManager.isMonitoringAvailable(for: CLCircularRegion.self) {
    let region = CLCircularRegion(
        center: coordinate,
        radius: 100,
        identifier: "myRegion"
    )
    region.notifyOnEntry = true
    region.notifyOnExit = true

    manager.startMonitoring(for: region)
}

// デリゲート
func locationManager(_ manager: CLLocationManager, didEnterRegion region: CLRegion) {
    // 領域に入った
}

func locationManager(_ manager: CLLocationManager, didExitRegion region: CLRegion) {
    // 領域から出た
}
```

## エラーハンドリング

```swift
func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
    if let clError = error as? CLError {
        switch clError.code {
        case .denied:
            // 権限が拒否された
            break
        case .locationUnknown:
            // 位置を特定できない（リトライ可能）
            break
        case .network:
            // ネットワークエラー
            break
        case .headingFailure:
            // 方位取得失敗
            break
        case .regionMonitoringDenied:
            // リージョンモニタリング拒否
            break
        case .regionMonitoringFailure:
            // リージョンモニタリング失敗
            break
        default:
            break
        }
    }
}
```

## システム環境設定への誘導

```swift
func openLocationSettings() {
    if let url = URL(string: "x-apple.systempreferences:com.apple.preference.security?Privacy_LocationServices") {
        NSWorkspace.shared.open(url)
    }
}
```

## macOS固有の制限事項

1. **バックグラウンド位置情報** - 通常のデスクトップアプリでは不要
2. **`.authorizedWhenInUse`** - macOSでは利用不可
3. **Heading** - 一部のMacでのみ利用可能
4. **App Sandbox** - エンタイトルメント必須
5. **ネットワーク** - 位置情報に`network.client`エンタイトルメント必要
