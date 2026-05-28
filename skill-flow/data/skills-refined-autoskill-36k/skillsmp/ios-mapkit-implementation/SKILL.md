---
name: iOS MapKit Implementation
description: This skill should be used when the user asks to "add map view", "show user location", "implement MapKit", "add markers to map", "calculate route", "use MKDirections", "search nearby places", "use MKLocalSearch", "implement geocoding", "use CLGeocoder", "add Look Around", "customize map style", "add map annotations", "track user location", "configure location permissions", "地図を表示したい", "MapKitを実装", "マーカーを追加", "経路検索を実装", "ナビゲーション機能", "現在地を取得", "周辺検索", "ジオコーディング", "住所から座標を取得", "座標から住所", "Look Aroundを追加", "地図をカスタマイズ", "位置情報の権限設定", or needs guidance on MapKit for SwiftUI, Core Location integration, MKDirections, MKLocalSearch, CLGeocoder, Look Around preview, map annotations, custom overlays, or location privacy settings for iOS 17+ SwiftUI applications.
version: 0.1.0
---

# iOS MapKit Implementation

iOS 17+向けSwiftUIアプリケーションにおけるMapKit実装ガイド。地図表示、位置情報、経路検索、周辺検索機能の実装をサポートする。

## Quick Start Checklist

MapKit機能を実装する際の必須手順：

1. **Info.plist設定**
   - `NSLocationWhenInUseUsageDescription` - 使用中の位置情報アクセス理由
   - `NSLocationAlwaysAndWhenInUseUsageDescription` - 常時位置情報（必要な場合）

2. **フレームワークインポート**
   ```swift
   import MapKit
   import CoreLocation
   ```

3. **位置情報権限リクエスト**
   - `CLLocationManager.authorizationStatus`で状態確認
   - `requestWhenInUseAuthorization()`で権限リクエスト

4. **地図表示**
   - SwiftUI Map viewで表示
   - MapCameraPositionで位置・ズーム制御

## Core Components

### Map (SwiftUI iOS 17+)

iOS 17で刷新されたMap APIを使用。

```swift
@State private var position: MapCameraPosition = .automatic

var body: some View {
    Map(position: $position) {
        Marker("Tokyo", coordinate: .tokyo)
        UserAnnotation()
    }
    .mapStyle(.standard(elevation: .realistic))
    .mapControls {
        MapUserLocationButton()
        MapCompass()
        MapScaleView()
    }
}
```

**主要プロパティ:**
- `position` - カメラ位置（`.automatic`, `.userLocation()`, `.region()`, `.camera()`）
- `mapStyle` - 地図スタイル（`.standard`, `.imagery`, `.hybrid`）
- `interactionModes` - 操作モード（`.all`, `.pan`, `.zoom`, `.rotate`, `.pitch`）

### MapCameraPosition

カメラ位置を制御する構造体。

```swift
// ユーザー位置を追従
let position: MapCameraPosition = .userLocation(fallback: .automatic)

// 特定の地域を表示
let position: MapCameraPosition = .region(MKCoordinateRegion(
    center: CLLocationCoordinate2D(latitude: 35.6762, longitude: 139.6503),
    span: MKCoordinateSpan(latitudeDelta: 0.1, longitudeDelta: 0.1)
))

// カメラアングル指定
let position: MapCameraPosition = .camera(MapCamera(
    centerCoordinate: CLLocationCoordinate2D(latitude: 35.6762, longitude: 139.6503),
    distance: 1000,
    heading: 45,
    pitch: 60
))
```

### MapStyle

地図の外観を設定。

```swift
// 標準スタイル
.mapStyle(.standard)

// 3D建物付き標準スタイル
.mapStyle(.standard(elevation: .realistic))

// 衛星写真
.mapStyle(.imagery)

// 衛星写真 + 道路名
.mapStyle(.hybrid)

// POIフィルタリング
.mapStyle(.standard(pointsOfInterest: .including([.restaurant, .cafe])))
```

## Markers and Annotations

### Marker

システム提供のマーカー。

```swift
Map {
    // 基本マーカー
    Marker("Tokyo Station", coordinate: .tokyoStation)

    // システムイメージ付き
    Marker("Restaurant", systemImage: "fork.knife", coordinate: location)
        .tint(.orange)

    // モノグラム
    Marker("A", monogram: Text("A"), coordinate: location)
}
```

### Annotation

カスタムビューをマーカーとして表示。

```swift
Map {
    Annotation("Custom", coordinate: location) {
        VStack {
            Image(systemName: "star.fill")
                .foregroundStyle(.yellow)
            Text("Spot")
                .font(.caption)
        }
        .padding(4)
        .background(.white)
        .clipShape(RoundedRectangle(cornerRadius: 8))
    }
}
```

### UserAnnotation

ユーザーの現在地を表示。

```swift
Map {
    UserAnnotation()
}
.mapControls {
    MapUserLocationButton()
}
```

## Core Location Integration

### CLLocationManager Setup

位置情報マネージャーの設定。

```swift
@MainActor
@Observable
final class LocationManager: NSObject, CLLocationManagerDelegate {
    var location: CLLocation?
    var authorizationStatus: CLAuthorizationStatus = .notDetermined

    private let manager = CLLocationManager()

    override init() {
        super.init()
        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyBest
    }

    func requestAuthorization() {
        manager.requestWhenInUseAuthorization()
    }

    func startUpdating() {
        manager.startUpdatingLocation()
    }

    nonisolated func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        Task { @MainActor in
            location = locations.last
        }
    }

    nonisolated func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        Task { @MainActor in
            authorizationStatus = manager.authorizationStatus
        }
    }
}
```

### Authorization States

| State | 説明 | 対応 |
|-------|------|------|
| `.authorizedWhenInUse` | 使用中のみ許可 | 位置情報取得可能 |
| `.authorizedAlways` | 常時許可 | バックグラウンドでも取得可能 |
| `.denied` | 拒否された | 設定アプリへ誘導 |
| `.restricted` | 制限されている | 機能無効化 |
| `.notDetermined` | 未決定 | 権限リクエスト実行 |

## Route & Navigation

### MKDirections

経路検索を実行。

```swift
func calculateRoute(from source: CLLocationCoordinate2D, to destination: CLLocationCoordinate2D) async throws -> MKRoute {
    let request = MKDirections.Request()
    request.source = MKMapItem(placemark: MKPlacemark(coordinate: source))
    request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destination))
    request.transportType = .automobile

    let directions = MKDirections(request: request)
    let response = try await directions.calculate()

    guard let route = response.routes.first else {
        throw MapError.noRouteFound
    }

    return route
}
```

### Route Display

経路をMapに表示。

```swift
@State private var route: MKRoute?

var body: some View {
    Map {
        if let route {
            MapPolyline(route.polyline)
                .stroke(.blue, lineWidth: 5)
        }
    }
}
```

### Turn-by-Turn Steps

ターンバイターン案内情報を取得。

```swift
for step in route.steps {
    print("距離: \(step.distance)m")
    print("案内: \(step.instructions)")
}
```

## Local Search

### MKLocalSearch

周辺検索を実行。

```swift
func searchNearby(query: String, region: MKCoordinateRegion) async throws -> [MKMapItem] {
    let request = MKLocalSearch.Request()
    request.naturalLanguageQuery = query
    request.region = region

    let search = MKLocalSearch(request: request)
    let response = try await search.start()

    return response.mapItems
}
```

### MKLocalSearchCompleter

検索サジェストを提供。

```swift
@Observable
final class SearchCompleter: NSObject, MKLocalSearchCompleterDelegate {
    var results: [MKLocalSearchCompletion] = []
    private let completer = MKLocalSearchCompleter()

    override init() {
        super.init()
        completer.delegate = self
        completer.resultTypes = [.address, .pointOfInterest]
    }

    func search(query: String) {
        completer.queryFragment = query
    }

    nonisolated func completerDidUpdateResults(_ completer: MKLocalSearchCompleter) {
        Task { @MainActor in
            results = completer.results
        }
    }
}
```

## Look Around (iOS 17+)

### Scene Request

Look Aroundシーンを取得。

```swift
func getLookAroundScene(for coordinate: CLLocationCoordinate2D) async -> MKLookAroundScene? {
    let request = MKLookAroundSceneRequest(coordinate: coordinate)
    return try? await request.scene
}
```

### LookAroundPreview

プレビューを埋め込み表示。

```swift
@State private var lookAroundScene: MKLookAroundScene?

var body: some View {
    VStack {
        if let scene = lookAroundScene {
            LookAroundPreview(scene: scene)
                .frame(height: 200)
        } else {
            ContentUnavailableView("Look Around利用不可", systemImage: "eye.slash")
        }
    }
    .task {
        lookAroundScene = await getLookAroundScene(for: coordinate)
    }
}
```

## Geocoding

### Forward Geocoding（住所 → 座標）

```swift
func geocode(address: String) async throws -> CLLocationCoordinate2D {
    let geocoder = CLGeocoder()
    let placemarks = try await geocoder.geocodeAddressString(address)

    guard let location = placemarks.first?.location else {
        throw MapError.geocodingFailed
    }

    return location.coordinate
}
```

### Reverse Geocoding（座標 → 住所）

```swift
func reverseGeocode(coordinate: CLLocationCoordinate2D) async throws -> String {
    let geocoder = CLGeocoder()
    let location = CLLocation(latitude: coordinate.latitude, longitude: coordinate.longitude)
    let placemarks = try await geocoder.reverseGeocodeLocation(location)

    guard let placemark = placemarks.first else {
        throw MapError.geocodingFailed
    }

    return [placemark.locality, placemark.thoroughfare, placemark.subThoroughfare]
        .compactMap { $0 }
        .joined(separator: " ")
}
```

## Custom Overlays

### MapCircle

円形オーバーレイ。

```swift
Map {
    MapCircle(center: coordinate, radius: 500)
        .foregroundStyle(.blue.opacity(0.3))
        .stroke(.blue, lineWidth: 2)
}
```

### MapPolygon

多角形オーバーレイ。

```swift
Map {
    MapPolygon(coordinates: polygonCoordinates)
        .foregroundStyle(.green.opacity(0.3))
        .stroke(.green, lineWidth: 2)
}
```

## Error Handling

MapKit/CoreLocationで発生しうる主要エラー：

| エラー | 原因 | 対処 |
|--------|------|------|
| `CLError.denied` | 位置情報が拒否された | 設定アプリへ誘導 |
| `CLError.locationUnknown` | 位置を特定できない | リトライまたはフォールバック |
| `MKError.serverFailure` | サーバーエラー | リトライ |
| `MKError.directionsNotFound` | 経路が見つからない | 代替手段を提案 |

詳細なトラブルシューティングは `references/troubleshooting.md` を参照。

## Quick Reference

| Component | Purpose | Key API |
|-----------|---------|---------|
| `Map` | 地図表示 | `Map(position:) { }` |
| `MapCameraPosition` | カメラ制御 | `.automatic`, `.region()`, `.camera()` |
| `Marker` | マーカー表示 | `Marker(_:coordinate:)` |
| `Annotation` | カスタムマーカー | `Annotation(_:coordinate:) { }` |
| `CLLocationManager` | 位置情報管理 | `startUpdatingLocation()` |
| `MKDirections` | 経路検索 | `calculate()` |
| `MKLocalSearch` | 周辺検索 | `start()` |
| `CLGeocoder` | ジオコーディング | `geocodeAddressString(_:)` |
| `LookAroundPreview` | Look Around表示 | `LookAroundPreview(scene:)` |

## Additional Resources

### Reference Files

詳細な情報は以下を参照：

- **`references/mapkit-swiftui.md`** - MapKit for SwiftUI API詳細リファレンス
- **`references/core-location.md`** - Core Location統合の詳細
- **`references/geocoding.md`** - ジオコーディングの詳細設定
- **`references/directions.md`** - 経路検索APIリファレンス
- **`references/local-search.md`** - ローカル検索の詳細
- **`references/look-around.md`** - Look Around機能の詳細
- **`references/custom-overlays.md`** - カスタムオーバーレイの実装
- **`references/permission-patterns.md`** - 権限リクエストパターンとInfo.plist設定
- **`references/troubleshooting.md`** - エラーコード一覧とデバッグ手法

### Example Files

実装サンプルは `examples/` ディレクトリを参照：

- **`examples/basic-map-view.swift`** - 基本的な地図表示
- **`examples/map-viewmodel.swift`** - 完全な地図用ViewModel実装
- **`examples/marker-annotation-view.swift`** - マーカー/アノテーション実装
- **`examples/directions-view.swift`** - 経路検索・ナビゲーション画面
- **`examples/local-search-view.swift`** - ローカル検索UI
- **`examples/look-around-view.swift`** - Look Around統合
- **`examples/location-manager.swift`** - 位置情報マネージャー実装
- **`examples/info-plist-config.xml`** - Info.plist設定テンプレート
