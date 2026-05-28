# MKDirections Reference

MKDirectionsを使用した経路検索とナビゲーションの詳細ガイド。

## MKDirections.Request

経路検索リクエストを構成。

### 基本的な設定

```swift
let request = MKDirections.Request()

// 出発地
request.source = MKMapItem(placemark: MKPlacemark(coordinate: sourceCoordinate))

// 目的地
request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destinationCoordinate))

// 交通手段
request.transportType = .automobile
```

### 現在地を出発地に設定

```swift
request.source = MKMapItem.forCurrentLocation()
request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destinationCoordinate))
```

### 交通手段

```swift
// 車
request.transportType = .automobile

// 徒歩
request.transportType = .walking

// 公共交通機関
request.transportType = .transit

// 複数の交通手段（ビット演算）
request.transportType = [.automobile, .walking]
```

### その他のオプション

```swift
// 複数の代替ルートを取得
request.requestsAlternateRoutes = true

// 出発時刻（公共交通機関で使用）
request.departureDate = Date()

// 到着時刻（公共交通機関で使用）
request.arrivalDate = Date().addingTimeInterval(3600)

// 有料道路を避ける（iOS 17+）
request.tollPreference = .avoid

// 高速道路を避ける（iOS 17+）
request.highwayPreference = .avoid
```

## MKDirections

経路計算を実行。

### 基本的な使用

```swift
func calculateRoute(
    from source: CLLocationCoordinate2D,
    to destination: CLLocationCoordinate2D
) async throws -> MKRoute {
    let request = MKDirections.Request()
    request.source = MKMapItem(placemark: MKPlacemark(coordinate: source))
    request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destination))
    request.transportType = .automobile

    let directions = MKDirections(request: request)
    let response = try await directions.calculate()

    guard let route = response.routes.first else {
        throw DirectionsError.noRouteFound
    }

    return route
}
```

### 代替ルートの取得

```swift
func calculateAlternateRoutes(
    from source: CLLocationCoordinate2D,
    to destination: CLLocationCoordinate2D
) async throws -> [MKRoute] {
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

### ETA（到着予想時間）のみ取得

```swift
func calculateETA(
    from source: CLLocationCoordinate2D,
    to destination: CLLocationCoordinate2D
) async throws -> TimeInterval {
    let request = MKDirections.Request()
    request.source = MKMapItem(placemark: MKPlacemark(coordinate: source))
    request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destination))
    request.transportType = .automobile

    let directions = MKDirections(request: request)
    let response = try await directions.calculateETA()

    return response.expectedTravelTime
}
```

## MKRoute

経路情報を格納。

### 主要プロパティ

```swift
let route: MKRoute

// 基本情報
route.name                    // ルート名
route.distance                // 距離（メートル）
route.expectedTravelTime      // 予想所要時間（秒）

// 経路形状
route.polyline               // MKPolyline（地図描画用）

// ターンバイターン案内
route.steps                  // [MKRoute.Step]

// 交通手段
route.transportType          // MKDirectionsTransportType

// 推奨事項
route.advisoryNotices        // [String] 注意事項
route.hasHighways            // 高速道路を含む
route.hasTolls               // 有料道路を含む
```

### MKRoute.Step

各案内ステップの情報。

```swift
for step in route.steps {
    // 案内テキスト
    print(step.instructions)         // "首都高速湾岸線に入る"

    // 距離
    print(step.distance)             // メートル

    // このステップのポリライン
    let polyline = step.polyline

    // 交通手段
    print(step.transportType)

    // 通知（公共交通機関）
    print(step.notice ?? "")
}
```

## 地図への経路表示

### SwiftUI Map での表示

```swift
struct RouteMapView: View {
    @State private var route: MKRoute?
    @State private var position: MapCameraPosition = .automatic

    let source: CLLocationCoordinate2D
    let destination: CLLocationCoordinate2D

    var body: some View {
        Map(position: $position) {
            // 出発地マーカー
            Marker("出発", systemImage: "figure.walk", coordinate: source)
                .tint(.green)

            // 目的地マーカー
            Marker("到着", systemImage: "flag.fill", coordinate: destination)
                .tint(.red)

            // 経路ライン
            if let route {
                MapPolyline(route.polyline)
                    .stroke(.blue, lineWidth: 5)
            }
        }
        .task {
            await calculateRoute()
        }
    }

    private func calculateRoute() async {
        let request = MKDirections.Request()
        request.source = MKMapItem(placemark: MKPlacemark(coordinate: source))
        request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destination))
        request.transportType = .automobile

        let directions = MKDirections(request: request)

        do {
            let response = try await directions.calculate()
            route = response.routes.first

            // ルートに合わせてカメラを調整
            if let route {
                position = .rect(route.polyline.boundingMapRect)
            }
        } catch {
            print("Route calculation failed: \(error)")
        }
    }
}
```

### 複数ルートの表示

```swift
struct MultiRouteMapView: View {
    @State private var routes: [MKRoute] = []
    @State private var selectedRoute: MKRoute?

    var body: some View {
        Map {
            ForEach(routes, id: \.name) { route in
                MapPolyline(route.polyline)
                    .stroke(
                        selectedRoute?.name == route.name ? .blue : .gray,
                        lineWidth: selectedRoute?.name == route.name ? 5 : 3
                    )
            }
        }
    }
}
```

## ターンバイターンナビゲーション

### 案内ステップの表示

```swift
struct RouteStepsView: View {
    let route: MKRoute

    var body: some View {
        List(route.steps, id: \.instructions) { step in
            HStack {
                Image(systemName: stepIcon(for: step))
                    .frame(width: 30)

                VStack(alignment: .leading) {
                    Text(step.instructions)
                        .font(.body)

                    Text(formatDistance(step.distance))
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }
            }
        }
    }

    private func stepIcon(for step: MKRoute.Step) -> String {
        // 案内テキストからアイコンを推定
        let instructions = step.instructions.lowercased()
        if instructions.contains("左") || instructions.contains("left") {
            return "arrow.turn.up.left"
        } else if instructions.contains("右") || instructions.contains("right") {
            return "arrow.turn.up.right"
        } else if instructions.contains("直進") || instructions.contains("straight") {
            return "arrow.up"
        } else if instructions.contains("到着") || instructions.contains("destination") {
            return "flag.fill"
        }
        return "arrow.forward"
    }

    private func formatDistance(_ meters: CLLocationDistance) -> String {
        if meters >= 1000 {
            return String(format: "%.1f km", meters / 1000)
        } else {
            return String(format: "%.0f m", meters)
        }
    }
}
```

### ルートサマリー

```swift
struct RouteSummaryView: View {
    let route: MKRoute

    var body: some View {
        VStack(spacing: 8) {
            HStack {
                Label(formatDistance(route.distance), systemImage: "car.fill")
                Spacer()
                Label(formatTime(route.expectedTravelTime), systemImage: "clock")
            }

            if route.hasTolls {
                Label("有料道路を含む", systemImage: "yensign.circle")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }

            if route.hasHighways {
                Label("高速道路を含む", systemImage: "road.lanes")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
        }
        .padding()
        .background(.regularMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }

    private func formatDistance(_ meters: CLLocationDistance) -> String {
        if meters >= 1000 {
            return String(format: "%.1f km", meters / 1000)
        } else {
            return String(format: "%.0f m", meters)
        }
    }

    private func formatTime(_ seconds: TimeInterval) -> String {
        let hours = Int(seconds) / 3600
        let minutes = (Int(seconds) % 3600) / 60

        if hours > 0 {
            return "\(hours)時間\(minutes)分"
        } else {
            return "\(minutes)分"
        }
    }
}
```

## 公共交通機関

### Transit経路の取得

```swift
func calculateTransitRoute(
    from source: CLLocationCoordinate2D,
    to destination: CLLocationCoordinate2D,
    departureDate: Date = Date()
) async throws -> MKRoute {
    let request = MKDirections.Request()
    request.source = MKMapItem(placemark: MKPlacemark(coordinate: source))
    request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destination))
    request.transportType = .transit
    request.departureDate = departureDate

    let directions = MKDirections(request: request)
    let response = try await directions.calculate()

    guard let route = response.routes.first else {
        throw DirectionsError.noRouteFound
    }

    return route
}
```

**注意:** 公共交通機関の経路検索は、Apple Mapsが公共交通機関データを持っている地域でのみ機能します。日本の多くの都市では利用可能です。

## エラーハンドリング

### MKError

| コード | 名前 | 説明 |
|--------|------|------|
| 1 | `unknown` | 不明なエラー |
| 2 | `serverFailure` | サーバーエラー |
| 3 | `loadingThrottled` | リクエスト制限 |
| 4 | `placemarkNotFound` | 場所が見つからない |
| 5 | `directionsNotFound` | 経路が見つからない |
| 6 | `decodingFailed` | デコード失敗 |

### エラー処理パターン

```swift
func calculateRouteSafely(
    from source: CLLocationCoordinate2D,
    to destination: CLLocationCoordinate2D
) async -> Result<MKRoute, DirectionsError> {
    let request = MKDirections.Request()
    request.source = MKMapItem(placemark: MKPlacemark(coordinate: source))
    request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destination))
    request.transportType = .automobile

    let directions = MKDirections(request: request)

    do {
        let response = try await directions.calculate()

        guard let route = response.routes.first else {
            return .failure(.noRouteFound)
        }

        return .success(route)
    } catch let error as MKError {
        switch error.code {
        case .directionsNotFound:
            return .failure(.noRouteFound)
        case .serverFailure:
            return .failure(.serverError)
        case .loadingThrottled:
            return .failure(.rateLimited)
        default:
            return .failure(.unknown(error))
        }
    } catch {
        return .failure(.unknown(error))
    }
}

enum DirectionsError: Error {
    case noRouteFound
    case serverError
    case rateLimited
    case unknown(Error)
}
```

## キャンセル

```swift
class DirectionsService {
    private var currentDirections: MKDirections?

    func calculateRoute(
        from source: CLLocationCoordinate2D,
        to destination: CLLocationCoordinate2D
    ) async throws -> MKRoute {
        // 進行中のリクエストをキャンセル
        currentDirections?.cancel()

        let request = MKDirections.Request()
        request.source = MKMapItem(placemark: MKPlacemark(coordinate: source))
        request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destination))
        request.transportType = .automobile

        let directions = MKDirections(request: request)
        currentDirections = directions

        let response = try await directions.calculate()

        guard let route = response.routes.first else {
            throw DirectionsError.noRouteFound
        }

        return route
    }

    func cancel() {
        currentDirections?.cancel()
        currentDirections = nil
    }
}
```

## ベストプラクティス

### キャッシュ

```swift
actor RouteCache {
    private var cache: [String: MKRoute] = [:]

    func route(from source: CLLocationCoordinate2D, to destination: CLLocationCoordinate2D) async throws -> MKRoute {
        let key = "\(source.latitude),\(source.longitude)-\(destination.latitude),\(destination.longitude)"

        if let cached = cache[key] {
            return cached
        }

        let route = try await calculateRoute(from: source, to: destination)
        cache[key] = route

        return route
    }

    private func calculateRoute(from source: CLLocationCoordinate2D, to destination: CLLocationCoordinate2D) async throws -> MKRoute {
        // 実際の経路計算
        let request = MKDirections.Request()
        request.source = MKMapItem(placemark: MKPlacemark(coordinate: source))
        request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destination))
        request.transportType = .automobile

        let directions = MKDirections(request: request)
        let response = try await directions.calculate()

        guard let route = response.routes.first else {
            throw DirectionsError.noRouteFound
        }

        return route
    }
}
```

### 経路の更新

```swift
// ユーザーが経路から外れた場合の再計算
func recalculateIfNeeded(currentLocation: CLLocation, route: MKRoute) async -> MKRoute? {
    // 経路からの距離を計算
    let routePoints = route.polyline.points()
    let pointCount = route.polyline.pointCount

    var minDistance: CLLocationDistance = .infinity

    for i in 0..<pointCount {
        let point = routePoints[i]
        let coordinate = point.coordinate
        let location = CLLocation(latitude: coordinate.latitude, longitude: coordinate.longitude)
        let distance = currentLocation.distance(from: location)
        minDistance = min(minDistance, distance)
    }

    // 100m以上離れたら再計算
    if minDistance > 100 {
        // 再計算ロジック
        return nil  // 新しいルートを返す
    }

    return nil
}
```
