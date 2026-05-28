---
name: macOS MapKit Implementation
description: This skill should be used when the user asks to "add map view to macOS app", "show user location on macOS", "implement MapKit for macOS", "add markers to map in macOS app", "calculate route in macOS app", "use MKDirections on macOS", "search nearby places on macOS", "use MKLocalSearch on macOS", "implement geocoding on macOS", "use CLGeocoder on macOS", "add Look Around on macOS", "customize map style on macOS", "configure location permissions for macOS", "set up App Sandbox for location", "use MKMapView with AppKit", "macOSアプリに地図を追加", "macOSで位置情報を表示", "macOSでMapKitを実装", "macOSでマーカーを追加", "macOSで経路検索", "macOSで周辺検索", "macOSでジオコーディング", "macOSでLook Around", "macOSで地図をカスタマイズ", "macOSの位置情報権限設定", "App Sandboxで位置情報", "AppKitでMKMapView", or needs guidance on MapKit for macOS 14+ SwiftUI/AppKit applications, App Sandbox configuration, location entitlements, or macOS-specific location permission handling.
version: 0.1.0
---

# macOS MapKit Implementation

macOS 14+ (Sonoma) 向けSwiftUI/AppKitアプリケーションにおけるMapKit実装ガイド。地図表示、位置情報、経路検索、周辺検索機能の実装をサポートする。

## Quick Start Checklist

MapKit機能を実装する際の必須手順：

1. **Info.plist設定**
   - `NSLocationUsageDescription` - 位置情報アクセス理由

2. **エンタイトルメント設定** (App Sandbox)
   - `com.apple.security.personal-information.location` - 位置情報アクセス
   - `com.apple.security.network.client` - ネットワークアクセス（位置情報サービスに必要）

3. **フレームワークインポート**
   ```swift
   import MapKit
   import CoreLocation
   ```

4. **位置情報権限リクエスト**
   - `CLLocationManager.authorizationStatus`で状態確認
   - `requestWhenInUseAuthorization()`で権限リクエスト

5. **地図表示**
   - SwiftUI Map viewで表示
   - MapCameraPositionで位置・ズーム制御

## Core Components

### Map (SwiftUI macOS 14+)

macOS 14で刷新されたMap APIを使用。

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
        MapZoomStepper() // macOS向け
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

## Core Location Integration (macOS)

### CLLocationManager Setup

macOS用位置情報マネージャーの設定。

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

            // macOSでは.authorizedが主に使用される
            switch authorizationStatus {
            case .authorized, .authorizedAlways:
                startUpdating()
            case .denied, .restricted:
                // システム環境設定へ誘導
                openLocationSettings()
            case .notDetermined:
                break
            @unknown default:
                break
            }
        }
    }

    private func openLocationSettings() {
        if let url = URL(string: "x-apple.systempreferences:com.apple.preference.security?Privacy_LocationServices") {
            NSWorkspace.shared.open(url)
        }
    }
}
```

### Authorization States (macOS)

| State | 説明 | 対応 |
|-------|------|------|
| `.authorized` | 許可（macOS主要） | 位置情報取得可能 |
| `.authorizedAlways` | 常時許可 | 位置情報取得可能 |
| `.denied` | 拒否された | システム環境設定へ誘導 |
| `.restricted` | 制限されている | 機能無効化 |
| `.notDetermined` | 未決定 | 権限リクエスト実行 |

**注意:** macOSでは`.authorizedWhenInUse`はiOSほど一般的ではなく、`.authorized`または`.authorizedAlways`が返されることが多い。

## AppKit Integration

### MKMapView with NSViewRepresentable

AppKitアプリでMKMapViewを使用する場合。

```swift
import SwiftUI
import MapKit

struct AppKitMapView: NSViewRepresentable {
    @Binding var region: MKCoordinateRegion
    var annotations: [MKAnnotation]

    func makeNSView(context: Context) -> MKMapView {
        let mapView = MKMapView()
        mapView.delegate = context.coordinator
        mapView.showsUserLocation = true
        mapView.showsCompass = true
        mapView.showsZoomControls = true
        return mapView
    }

    func updateNSView(_ mapView: MKMapView, context: Context) {
        mapView.setRegion(region, animated: true)

        // アノテーション更新
        mapView.removeAnnotations(mapView.annotations)
        mapView.addAnnotations(annotations)
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, MKMapViewDelegate {
        var parent: AppKitMapView

        init(_ parent: AppKitMapView) {
            self.parent = parent
        }

        func mapView(_ mapView: MKMapView, regionDidChangeAnimated animated: Bool) {
            parent.region = mapView.region
        }

        func mapView(_ mapView: MKMapView, viewFor annotation: MKAnnotation) -> MKAnnotationView? {
            guard !(annotation is MKUserLocation) else { return nil }

            let identifier = "CustomAnnotation"
            var view = mapView.dequeueReusableAnnotationView(withIdentifier: identifier) as? MKMarkerAnnotationView

            if view == nil {
                view = MKMarkerAnnotationView(annotation: annotation, reuseIdentifier: identifier)
                view?.canShowCallout = true
            } else {
                view?.annotation = annotation
            }

            return view
        }
    }
}
```

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

## Look Around (macOS 14+)

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
                .frame(height: 300)
        } else {
            ContentUnavailableView("Look Around利用不可", systemImage: "eye.slash")
        }
    }
    .task {
        lookAroundScene = await getLookAroundScene(for: coordinate)
    }
}
```

**macOS制限事項:**
- macOS 15時点で、フルスクリーンナビゲーションボタンが表示されない問題が報告されている
- 埋め込みプレビューは正常に動作する
- フォールバックとして衛星画像（`.imagery`スタイル）を使用することを推奨

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

## App Sandbox Configuration

macOSアプリはApp Sandboxを使用する場合、位置情報にアクセスするためにエンタイトルメントが必要。

### 必須エンタイトルメント

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.app-sandbox</key>
    <true/>
    <key>com.apple.security.personal-information.location</key>
    <true/>
    <key>com.apple.security.network.client</key>
    <true/>
</dict>
</plist>
```

**重要:** `com.apple.security.network.client`（送信接続）は位置情報サービスにも必要。これがないと位置情報が取得できない場合がある。

### Xcodeでの設定

1. プロジェクト設定 > Signing & Capabilities
2. App Sandboxを有効化
3. Location にチェック
4. Outgoing Connections (Client) にチェック

## Error Handling

MapKit/CoreLocationで発生しうる主要エラー：

| エラー | 原因 | 対処 |
|--------|------|------|
| `CLError.denied` | 位置情報が拒否された | システム環境設定へ誘導 |
| `CLError.locationUnknown` | 位置を特定できない | リトライまたはフォールバック |
| `MKError.serverFailure` | サーバーエラー | リトライ |
| `MKError.directionsNotFound` | 経路が見つからない | 代替手段を提案 |
| エンタイトルメント不足 | Sandbox設定漏れ | エンタイトルメント確認 |

詳細なトラブルシューティングは `references/troubleshooting-macos.md` を参照。

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
| `MKMapView` | AppKit地図 | `NSViewRepresentable` |

## Additional Resources

### Reference Files

詳細な情報は以下を参照：

- **`references/mapkit-swiftui.md`** - MapKit for SwiftUI API詳細リファレンス
- **`references/core-location-macos.md`** - macOS Core Location統合の詳細
- **`references/appkit-integration.md`** - AppKit MKMapView統合
- **`references/sandbox-entitlements.md`** - App Sandbox設定詳細
- **`references/permission-patterns-macos.md`** - macOS権限リクエストパターン
- **`references/geocoding.md`** - ジオコーディングの詳細設定
- **`references/directions.md`** - 経路検索APIリファレンス
- **`references/local-search.md`** - ローカル検索の詳細
- **`references/look-around-macos.md`** - Look Around機能（macOS制限事項）
- **`references/custom-overlays.md`** - カスタムオーバーレイの実装
- **`references/window-integration.md`** - ウィンドウ管理統合
- **`references/troubleshooting-macos.md`** - macOS特有のトラブルシューティング

### Example Files

実装サンプルは `examples/` ディレクトリを参照：

- **`examples/basic-map-view.swift`** - 基本的な地図表示
- **`examples/appkit-mapview.swift`** - AppKit MKMapView統合
- **`examples/location-manager-macos.swift`** - macOS用位置情報マネージャー
- **`examples/marker-annotation-view.swift`** - マーカー/アノテーション実装
- **`examples/directions-view.swift`** - 経路検索・ナビゲーション画面
- **`examples/local-search-view.swift`** - ローカル検索UI
- **`examples/look-around-view.swift`** - Look Around統合
- **`examples/info-plist-config.xml`** - Info.plist設定テンプレート
- **`examples/entitlements-config.xml`** - エンタイトルメント設定テンプレート
