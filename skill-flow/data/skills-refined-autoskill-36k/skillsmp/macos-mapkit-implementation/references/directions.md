# 経路検索 (MKDirections)

MKDirectionsを使用した経路検索APIリファレンス。

## MKDirections.Request

### 基本設定

```swift
let request = MKDirections.Request()
request.source = MKMapItem(placemark: MKPlacemark(coordinate: sourceCoordinate))
request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destinationCoordinate))
request.transportType = .automobile
```

### プロパティ

| プロパティ | 型 | 説明 |
|-----------|---|------|
| `source` | `MKMapItem?` | 出発地 |
| `destination` | `MKMapItem?` | 目的地 |
| `transportType` | `MKDirectionsTransportType` | 交通手段 |
| `requestsAlternateRoutes` | `Bool` | 代替ルートを要求 |
| `departureDate` | `Date?` | 出発日時 |
| `arrivalDate` | `Date?` | 到着日時 |

### MKDirectionsTransportType

| タイプ | 説明 |
|-------|------|
| `.automobile` | 自動車 |
| `.walking` | 徒歩 |
| `.transit` | 公共交通機関 |
| `.any` | すべて |

## 経路検索

### async/await

```swift
func calculateRoute(from source: CLLocationCoordinate2D, to destination: CLLocationCoordinate2D) async throws -> MKRoute {
    let request = MKDirections.Request()
    request.source = MKMapItem(placemark: MKPlacemark(coordinate: source))
    request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destination))
    request.transportType = .automobile
    request.requestsAlternateRoutes = true

    let directions = MKDirections(request: request)
    let response = try await directions.calculate()

    guard let route = response.routes.first else {
        throw DirectionsError.noRouteFound
    }

    return route
}
```

### 複数ルート取得

```swift
func calculateRoutes(from source: CLLocationCoordinate2D, to destination: CLLocationCoordinate2D) async throws -> [MKRoute] {
    let request = MKDirections.Request()
    request.source = MKMapItem(placemark: MKPlacemark(coordinate: source))
    request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destination))
    request.transportType = .automobile
    request.requestsAlternateRoutes = true

    let directions = MKDirections(request: request)
    let response = try await directions.calculate()

    return response.routes
}
```

## MKRoute

### プロパティ

| プロパティ | 型 | 説明 |
|-----------|---|------|
| `name` | `String` | ルート名 |
| `distance` | `CLLocationDistance` | 総距離（メートル） |
| `expectedTravelTime` | `TimeInterval` | 予想所要時間（秒） |
| `transportType` | `MKDirectionsTransportType` | 交通手段 |
| `polyline` | `MKPolyline` | 経路のポリライン |
| `steps` | `[MKRoute.Step]` | ターンバイターン案内 |
| `advisoryNotices` | `[String]` | 注意事項 |

### 距離フォーマット

```swift
func formatDistance(_ meters: CLLocationDistance) -> String {
    if meters >= 1000 {
        return String(format: "%.1f km", meters / 1000)
    } else {
        return String(format: "%.0f m", meters)
    }
}
```

### 所要時間フォーマット

```swift
func formatDuration(_ seconds: TimeInterval) -> String {
    let hours = Int(seconds) / 3600
    let minutes = (Int(seconds) % 3600) / 60

    if hours > 0 {
        return "\(hours)時間\(minutes)分"
    } else {
        return "\(minutes)分"
    }
}
```

## MKRoute.Step

ターンバイターン案内情報。

### プロパティ

| プロパティ | 型 | 説明 |
|-----------|---|------|
| `instructions` | `String` | 案内テキスト |
| `notice` | `String?` | 注意事項 |
| `distance` | `CLLocationDistance` | ステップの距離 |
| `transportType` | `MKDirectionsTransportType` | 交通手段 |
| `polyline` | `MKPolyline` | ステップのポリライン |

### ステップ表示例

```swift
ForEach(Array(route.steps.enumerated()), id: \.offset) { index, step in
    if !step.instructions.isEmpty {
        HStack(alignment: .top) {
            Text("\(index + 1)")
                .font(.caption)
                .foregroundStyle(.secondary)
                .frame(width: 24)

            VStack(alignment: .leading) {
                Text(step.instructions)
                Text(formatDistance(step.distance))
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
        }
    }
}
```

## 経路表示 (SwiftUI)

### MapPolyline

```swift
@State private var route: MKRoute?

var body: some View {
    Map(position: $position) {
        if let route {
            MapPolyline(route.polyline)
                .stroke(.blue, lineWidth: 5)
        }

        // 出発地・目的地マーカー
        Marker("出発地", coordinate: sourceCoordinate)
            .tint(.green)
        Marker("目的地", coordinate: destinationCoordinate)
            .tint(.red)
    }
}
```

### 経路全体を表示

```swift
if let route {
    let rect = route.polyline.boundingMapRect
    position = .rect(rect)
}
```

### 複数ルート表示

```swift
@State private var routes: [MKRoute] = []
@State private var selectedRouteIndex = 0

var body: some View {
    Map(position: $position) {
        ForEach(Array(routes.enumerated()), id: \.offset) { index, route in
            MapPolyline(route.polyline)
                .stroke(
                    index == selectedRouteIndex ? .blue : .gray.opacity(0.5),
                    lineWidth: index == selectedRouteIndex ? 5 : 3
                )
        }
    }
}
```

## 経路表示 (AppKit)

### MKMapView

```swift
// オーバーレイ追加
mapView.addOverlay(route.polyline, level: .aboveRoads)

// レンダラー
func mapView(_ mapView: MKMapView, rendererFor overlay: MKOverlay) -> MKOverlayRenderer {
    if let polyline = overlay as? MKPolyline {
        let renderer = MKPolylineRenderer(polyline: polyline)
        renderer.strokeColor = .systemBlue
        renderer.lineWidth = 5
        return renderer
    }
    return MKOverlayRenderer(overlay: overlay)
}

// 経路全体を表示
mapView.setVisibleMapRect(
    route.polyline.boundingMapRect,
    edgePadding: NSEdgeInsets(top: 50, left: 50, bottom: 50, right: 50),
    animated: true
)
```

## 到着予想時刻 (ETA)

### 計算

```swift
func calculateETA(from source: CLLocationCoordinate2D, to destination: CLLocationCoordinate2D) async throws -> TimeInterval {
    let request = MKDirections.Request()
    request.source = MKMapItem(placemark: MKPlacemark(coordinate: source))
    request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destination))
    request.transportType = .automobile

    let directions = MKDirections(request: request)
    let response = try await directions.calculateETA()

    return response.expectedTravelTime
}
```

### MKDirections.ETAResponse

| プロパティ | 型 | 説明 |
|-----------|---|------|
| `source` | `MKMapItem` | 出発地 |
| `destination` | `MKMapItem` | 目的地 |
| `expectedTravelTime` | `TimeInterval` | 予想所要時間 |
| `distance` | `CLLocationDistance` | 距離 |
| `expectedArrivalDate` | `Date` | 予想到着日時 |
| `expectedDepartureDate` | `Date` | 予想出発日時 |
| `transportType` | `MKDirectionsTransportType` | 交通手段 |

## エラーハンドリング

### MKError

| コード | 説明 | 対処 |
|-------|------|------|
| `.unknown` | 不明なエラー | リトライ |
| `.serverFailure` | サーバーエラー | リトライ |
| `.loadingThrottled` | レート制限 | 待機してリトライ |
| `.placemarkNotFound` | 場所が見つからない | 入力を確認 |
| `.directionsNotFound` | 経路が見つからない | 別の交通手段を試す |

### エラーハンドリング例

```swift
func calculateRoute(...) async throws -> MKRoute {
    do {
        let directions = MKDirections(request: request)
        let response = try await directions.calculate()

        guard let route = response.routes.first else {
            throw DirectionsError.noRouteFound
        }

        return route
    } catch let error as MKError {
        switch error.code {
        case .directionsNotFound:
            throw DirectionsError.noRouteAvailable
        case .serverFailure:
            throw DirectionsError.serverError
        case .loadingThrottled:
            throw DirectionsError.rateLimited
        default:
            throw DirectionsError.unknown(error)
        }
    }
}

enum DirectionsError: Error {
    case noRouteFound
    case noRouteAvailable
    case serverError
    case rateLimited
    case unknown(Error)
}
```

## 使用上の注意

1. **レート制限** - 短時間に多数のリクエストを送らない
2. **交通状況** - 予想時間は交通状況により変動
3. **地域制限** - 一部の地域では利用不可
4. **公共交通機関** - `.transit`は地域によって利用可否が異なる
5. **キャンセル** - `directions.cancel()`でキャンセル可能
