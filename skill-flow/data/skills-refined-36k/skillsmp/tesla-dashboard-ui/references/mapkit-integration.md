# MapKit Integration / MapKit統合

Tesla Dashboard UIのMapKit統合と音声案内について解説します。

## Overview / 概要

MapKit + AVSpeechSynthesizer を使用した完全なナビゲーションシステムです。

## Map View / マップビュー

### 基本構造

```swift
import SwiftUI
import MapKit

struct TeslaMapView: View {
    @ObservedObject var navigationManager: TeslaNavigationManager
    @State private var cameraPosition: MapCameraPosition = .automatic

    var body: some View {
        Map(position: $cameraPosition) {
            // User Location
            if let location = navigationManager.currentLocation {
                Annotation("現在地", coordinate: location) {
                    UserLocationMarker()
                }
            }

            // Destination
            if let destination = navigationManager.destination {
                Annotation(destination.name, coordinate: destination.coordinate) {
                    DestinationMarker()
                }
            }

            // Route
            if let route = navigationManager.currentRoute {
                MapPolyline(route.polyline)
                    .stroke(TeslaColors.accent, lineWidth: 6)
            }
        }
        .mapStyle(.standard(elevation: .realistic))
    }
}
```

### マップスタイル

```swift
// 標準マップ
.mapStyle(.standard)

// 衛星写真
.mapStyle(.imagery)

// ハイブリッド
.mapStyle(.hybrid)

// リアルな標高
.mapStyle(.standard(elevation: .realistic))

// POI表示
.mapStyle(.standard(pointsOfInterest: .including([.parking, .gasStation])))
```

### カメラコントロール

```swift
// 自動
cameraPosition = .automatic

// 特定位置
cameraPosition = .region(MKCoordinateRegion(
    center: coordinate,
    span: MKCoordinateSpan(latitudeDelta: 0.01, longitudeDelta: 0.01)
))

// 3Dカメラ
cameraPosition = .camera(MapCamera(
    centerCoordinate: coordinate,
    distance: 1000,
    heading: heading,
    pitch: 45
))
```

## Location Manager / 位置情報管理

### 権限リクエスト

```swift
class TeslaNavigationManager: NSObject, ObservableObject, CLLocationManagerDelegate {
    private let locationManager = CLLocationManager()

    func requestLocationPermission() {
        locationManager.delegate = self
        locationManager.requestWhenInUseAuthorization()
    }

    func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        switch manager.authorizationStatus {
        case .authorizedWhenInUse, .authorizedAlways:
            manager.startUpdatingLocation()
        case .denied, .restricted:
            // Handle denial
            break
        case .notDetermined:
            manager.requestWhenInUseAuthorization()
        @unknown default:
            break
        }
    }
}
```

### Info.plist 設定

```xml
<key>NSLocationWhenInUseUsageDescription</key>
<string>ナビゲーションと現在地表示に位置情報を使用します</string>

<key>NSLocationAlwaysAndWhenInUseUsageDescription</key>
<string>バックグラウンドナビゲーションに位置情報を使用します</string>
```

### 位置情報更新

```swift
func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
    guard let location = locations.last else { return }

    Task { @MainActor in
        self.currentLocation = location.coordinate

        if self.isNavigating {
            self.checkStepProgress(location: location)
        }
    }
}

func locationManager(_ manager: CLLocationManager, didUpdateHeading newHeading: CLHeading) {
    Task { @MainActor in
        self.currentHeading = newHeading.trueHeading
    }
}
```

## Route Calculation / ルート計算

### MKDirections

```swift
func calculateRoute(to destination: CLLocationCoordinate2D) async -> TeslaResult<MKRoute> {
    let request = MKDirections.Request()
    request.source = MKMapItem.forCurrentLocation()
    request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destination))
    request.transportType = .automobile
    request.requestsAlternateRoutes = true

    let directions = MKDirections(request: request)

    do {
        let response = try await directions.calculate()
        guard let route = response.routes.first else {
            return .failure(.routeCalculationFailed(reason: "ルートが見つかりません"))
        }
        return .success(route)
    } catch {
        return .failure(.routeCalculationFailed(reason: error.localizedDescription))
    }
}
```

### ルート情報

```swift
let route: MKRoute

// 距離
let distance = route.distance  // メートル

// 所要時間
let duration = route.expectedTravelTime  // 秒

// ステップ
let steps = route.steps
for step in steps {
    print("指示: \(step.instructions)")
    print("距離: \(step.distance)m")
    print("座標: \(step.polyline.coordinate)")
}

// ポリライン
let polyline = route.polyline
```

## Voice Guidance / 音声案内

### AVSpeechSynthesizer

```swift
import AVFoundation

class TeslaNavigationManager {
    private let speechSynthesizer = AVSpeechSynthesizer()

    func speak(_ text: String) {
        guard !speechSynthesizer.isSpeaking else { return }

        let utterance = AVSpeechUtterance(string: text)
        utterance.voice = AVSpeechSynthesisVoice(language: "ja-JP")
        utterance.rate = 0.5  // 0.0 ~ 1.0
        utterance.pitchMultiplier = 1.0  // 0.5 ~ 2.0
        utterance.volume = 1.0  // 0.0 ~ 1.0

        speechSynthesizer.speak(utterance)
    }

    func stopSpeaking() {
        speechSynthesizer.stopSpeaking(at: .immediate)
    }
}
```

### 案内タイミング

```swift
func checkStepProgress(location: CLLocation) {
    guard currentStepIndex < routeSteps.count else { return }

    let step = routeSteps[currentStepIndex]
    let stepEndLocation = CLLocation(
        latitude: step.polyline.coordinate.latitude,
        longitude: step.polyline.coordinate.longitude
    )

    let distanceToStepEnd = location.distance(from: stepEndLocation)

    // 事前案内（300m手前）
    if distanceToStepEnd < 300 && !hasPreAnnounced {
        speak("300メートル先、\(step.instructions)")
        hasPreAnnounced = true
    }

    // 直前案内（50m手前）
    if distanceToStepEnd < 50 {
        speak("まもなく、\(step.instructions)")
        currentStepIndex += 1
        hasPreAnnounced = false
    }
}
```

### マニューバータイプ

```swift
enum ManeuverType {
    case straight
    case slightLeft
    case slightRight
    case left
    case right
    case sharpLeft
    case sharpRight
    case uTurn
    case merge
    case arrive
    case depart

    var iconName: String {
        switch self {
        case .straight: return "arrow.up"
        case .left: return "arrow.turn.up.left"
        case .right: return "arrow.turn.up.right"
        // ...
        }
    }

    static func from(_ instruction: String) -> ManeuverType {
        let lowercased = instruction.lowercased()
        if lowercased.contains("左折") || lowercased.contains("left") {
            return .left
        }
        if lowercased.contains("右折") || lowercased.contains("right") {
            return .right
        }
        // ...
        return .straight
    }
}
```

## Geocoding / ジオコーディング

### 住所 → 座標

```swift
func geocode(address: String) async -> TeslaResult<CLLocationCoordinate2D> {
    let geocoder = CLGeocoder()

    do {
        let placemarks = try await geocoder.geocodeAddressString(address)
        guard let location = placemarks.first?.location else {
            return .failure(.geocodingFailed(address: address))
        }
        return .success(location.coordinate)
    } catch {
        return .failure(.geocodingFailed(address: address))
    }
}
```

### 座標 → 住所

```swift
func reverseGeocode(coordinate: CLLocationCoordinate2D) async -> String? {
    let geocoder = CLGeocoder()
    let location = CLLocation(latitude: coordinate.latitude, longitude: coordinate.longitude)

    do {
        let placemarks = try await geocoder.reverseGeocodeLocation(location)
        guard let placemark = placemarks.first else { return nil }

        var components: [String] = []
        if let postalCode = placemark.postalCode {
            components.append("〒\(postalCode)")
        }
        if let prefecture = placemark.administrativeArea {
            components.append(prefecture)
        }
        if let city = placemark.locality {
            components.append(city)
        }
        if let street = placemark.thoroughfare {
            components.append(street)
        }

        return components.joined(separator: " ")
    } catch {
        return nil
    }
}
```

## Search / 検索

### MKLocalSearch

```swift
func searchPlaces(query: String, region: MKCoordinateRegion) async -> [MKMapItem] {
    let request = MKLocalSearch.Request()
    request.naturalLanguageQuery = query
    request.region = region

    let search = MKLocalSearch(request: request)

    do {
        let response = try await search.start()
        return response.mapItems
    } catch {
        return []
    }
}
```

### 検索結果の表示

```swift
struct SearchResultRow: View {
    let mapItem: MKMapItem

    var body: some View {
        HStack {
            Image(systemName: "mappin.circle")

            VStack(alignment: .leading) {
                Text(mapItem.name ?? "")
                    .font(TeslaTypography.bodyMedium)

                if let address = mapItem.placemark.title {
                    Text(address)
                        .font(TeslaTypography.labelSmall)
                        .foregroundStyle(TeslaColors.textSecondary)
                }
            }
        }
    }
}
```

## Charging Stations / 充電スポット

### 充電スポット検索

```swift
func searchChargingStations(near coordinate: CLLocationCoordinate2D) async -> [TeslaChargingStation] {
    let request = MKLocalSearch.Request()
    request.naturalLanguageQuery = "Tesla Supercharger"
    request.region = MKCoordinateRegion(
        center: coordinate,
        latitudinalMeters: 50000,
        longitudinalMeters: 50000
    )

    let search = MKLocalSearch(request: request)

    do {
        let response = try await search.start()
        return response.mapItems.compactMap { item in
            guard let location = item.placemark.location else { return nil }
            return TeslaChargingStation(
                id: UUID().uuidString,
                name: item.name ?? "Supercharger",
                coordinate: location.coordinate,
                chargerType: "Supercharger",
                power: 250,
                available: 4,
                total: 8
            )
        }
    } catch {
        return []
    }
}
```

## Map Annotations / マップアノテーション

### カスタムマーカー

```swift
struct UserLocationMarker: View {
    var body: some View {
        ZStack {
            Circle()
                .fill(TeslaColors.accent.opacity(0.3))
                .frame(width: 40, height: 40)

            Circle()
                .fill(TeslaColors.accent)
                .frame(width: 16, height: 16)
        }
    }
}

struct DestinationMarker: View {
    var body: some View {
        VStack(spacing: 0) {
            Image(systemName: "mappin.circle.fill")
                .font(.system(size: 32))
                .foregroundStyle(TeslaColors.statusRed)

            // Shadow
            Ellipse()
                .fill(.black.opacity(0.2))
                .frame(width: 12, height: 6)
                .offset(y: -2)
        }
    }
}
```

## Related Documents / 関連ドキュメント

- [Navigation Patterns](./navigation-patterns.md)
- [Error Handling](./error-handling.md)
- [AVFoundation Integration](./avfoundation-integration.md)
