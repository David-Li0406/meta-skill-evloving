# Custom Overlays Reference

MapKitでのカスタムオーバーレイ（図形描画）の詳細ガイド。

## 基本的なオーバーレイ

### MapCircle

円形のオーバーレイを描画。

```swift
Map {
    // 基本的な円
    MapCircle(center: coordinate, radius: 500)  // 半径はメートル単位

    // スタイル付き
    MapCircle(center: coordinate, radius: 1000)
        .foregroundStyle(.blue.opacity(0.3))
        .stroke(.blue, lineWidth: 2)
}
```

### 複数の円

```swift
struct RadiusMapView: View {
    let center: CLLocationCoordinate2D

    var body: some View {
        Map {
            // 同心円を描画
            MapCircle(center: center, radius: 500)
                .foregroundStyle(.green.opacity(0.2))
                .stroke(.green, lineWidth: 1)

            MapCircle(center: center, radius: 1000)
                .foregroundStyle(.yellow.opacity(0.2))
                .stroke(.yellow, lineWidth: 1)

            MapCircle(center: center, radius: 1500)
                .foregroundStyle(.red.opacity(0.2))
                .stroke(.red, lineWidth: 1)

            Marker("Center", coordinate: center)
        }
    }
}
```

## MapPolygon

多角形のオーバーレイを描画。

### 基本的な使用

```swift
Map {
    MapPolygon(coordinates: [
        CLLocationCoordinate2D(latitude: 35.68, longitude: 139.76),
        CLLocationCoordinate2D(latitude: 35.69, longitude: 139.77),
        CLLocationCoordinate2D(latitude: 35.68, longitude: 139.78),
        CLLocationCoordinate2D(latitude: 35.67, longitude: 139.77)
    ])
    .foregroundStyle(.green.opacity(0.3))
    .stroke(.green, lineWidth: 2)
}
```

### エリアのハイライト

```swift
struct AreaHighlightView: View {
    let areas: [Area]

    struct Area: Identifiable {
        let id = UUID()
        let name: String
        let coordinates: [CLLocationCoordinate2D]
        let color: Color
    }

    var body: some View {
        Map {
            ForEach(areas) { area in
                MapPolygon(coordinates: area.coordinates)
                    .foregroundStyle(area.color.opacity(0.3))
                    .stroke(area.color, lineWidth: 2)

                // エリア中心にラベル
                if let center = area.coordinates.center {
                    Annotation(area.name, coordinate: center) {
                        Text(area.name)
                            .font(.caption)
                            .padding(4)
                            .background(.white.opacity(0.8))
                            .clipShape(RoundedRectangle(cornerRadius: 4))
                    }
                }
            }
        }
    }
}

extension Array where Element == CLLocationCoordinate2D {
    var center: CLLocationCoordinate2D? {
        guard !isEmpty else { return nil }

        let latSum = reduce(0) { $0 + $1.latitude }
        let lonSum = reduce(0) { $0 + $1.longitude }

        return CLLocationCoordinate2D(
            latitude: latSum / Double(count),
            longitude: lonSum / Double(count)
        )
    }
}
```

## MapPolyline

線のオーバーレイを描画。

### 基本的な使用

```swift
Map {
    MapPolyline(coordinates: [
        CLLocationCoordinate2D(latitude: 35.68, longitude: 139.76),
        CLLocationCoordinate2D(latitude: 35.69, longitude: 139.77),
        CLLocationCoordinate2D(latitude: 35.68, longitude: 139.78)
    ])
    .stroke(.blue, lineWidth: 3)
}
```

### 経路表示

```swift
struct RouteOverlayView: View {
    let route: MKRoute

    var body: some View {
        Map {
            // MKPolylineからMapPolylineを作成
            MapPolyline(route.polyline)
                .stroke(.blue, lineWidth: 5)
        }
    }
}
```

### グラデーション線

```swift
Map {
    MapPolyline(coordinates: pathCoordinates)
        .stroke(
            LinearGradient(
                colors: [.green, .yellow, .red],
                startPoint: .leading,
                endPoint: .trailing
            ),
            lineWidth: 4
        )
}
```

### 破線

```swift
Map {
    MapPolyline(coordinates: pathCoordinates)
        .stroke(.blue, style: StrokeStyle(lineWidth: 3, dash: [10, 5]))
}
```

## 複合オーバーレイ

### ジオフェンス表示

```swift
struct GeofenceMapView: View {
    let geofences: [Geofence]

    struct Geofence: Identifiable {
        let id = UUID()
        let name: String
        let center: CLLocationCoordinate2D
        let radius: CLLocationDistance
        let isActive: Bool
    }

    var body: some View {
        Map {
            ForEach(geofences) { geofence in
                // ジオフェンスエリア
                MapCircle(center: geofence.center, radius: geofence.radius)
                    .foregroundStyle(
                        geofence.isActive
                            ? Color.green.opacity(0.2)
                            : Color.gray.opacity(0.2)
                    )
                    .stroke(
                        geofence.isActive ? .green : .gray,
                        lineWidth: 2
                    )

                // 中心マーカー
                Marker(geofence.name, systemImage: "mappin.circle", coordinate: geofence.center)
                    .tint(geofence.isActive ? .green : .gray)
            }
        }
    }
}
```

### ルートとウェイポイント

```swift
struct WaypointRouteView: View {
    let waypoints: [CLLocationCoordinate2D]

    var body: some View {
        Map {
            // ルート線
            MapPolyline(coordinates: waypoints)
                .stroke(.blue, lineWidth: 4)

            // ウェイポイントマーカー
            ForEach(Array(waypoints.enumerated()), id: \.offset) { index, coordinate in
                Annotation("\(index + 1)", coordinate: coordinate) {
                    Circle()
                        .fill(.white)
                        .frame(width: 24, height: 24)
                        .overlay {
                            Text("\(index + 1)")
                                .font(.caption.bold())
                        }
                        .shadow(radius: 2)
                }
            }
        }
    }
}
```

## ヒートマップ風表示

### 密度表示

```swift
struct DensityMapView: View {
    let points: [CLLocationCoordinate2D]

    var body: some View {
        Map {
            ForEach(Array(points.enumerated()), id: \.offset) { _, point in
                MapCircle(center: point, radius: 50)
                    .foregroundStyle(.red.opacity(0.1))
            }
        }
    }
}
```

### クラスター表示

```swift
struct ClusterMapView: View {
    let clusters: [Cluster]

    struct Cluster: Identifiable {
        let id = UUID()
        let center: CLLocationCoordinate2D
        let count: Int
    }

    var body: some View {
        Map {
            ForEach(clusters) { cluster in
                // サイズをカウントに基づいて決定
                let radius = Double(min(cluster.count * 10, 200))

                MapCircle(center: cluster.center, radius: radius)
                    .foregroundStyle(clusterColor(for: cluster.count).opacity(0.5))
                    .stroke(clusterColor(for: cluster.count), lineWidth: 2)

                Annotation("", coordinate: cluster.center) {
                    Text("\(cluster.count)")
                        .font(.caption.bold())
                        .foregroundStyle(.white)
                        .padding(6)
                        .background(clusterColor(for: cluster.count))
                        .clipShape(Circle())
                }
            }
        }
    }

    private func clusterColor(for count: Int) -> Color {
        switch count {
        case 0..<10: return .green
        case 10..<50: return .yellow
        case 50..<100: return .orange
        default: return .red
        }
    }
}
```

## インタラクティブオーバーレイ

### タップ可能なエリア

```swift
struct TappableAreaMapView: View {
    let areas: [NamedArea]
    @State private var selectedArea: NamedArea?

    struct NamedArea: Identifiable, Equatable {
        let id = UUID()
        let name: String
        let coordinates: [CLLocationCoordinate2D]
    }

    var body: some View {
        Map(selection: $selectedArea) {
            ForEach(areas) { area in
                MapPolygon(coordinates: area.coordinates)
                    .foregroundStyle(
                        selectedArea == area
                            ? Color.blue.opacity(0.5)
                            : Color.blue.opacity(0.2)
                    )
                    .stroke(
                        selectedArea == area ? .blue : .gray,
                        lineWidth: selectedArea == area ? 3 : 1
                    )
                    .tag(area)
            }
        }
        .onChange(of: selectedArea) { _, newValue in
            if let area = newValue {
                print("Selected: \(area.name)")
            }
        }
    }
}
```

## UIKitオーバーレイ（高度なカスタマイズ）

SwiftUI Mapでは直接サポートされない高度なオーバーレイ（タイルオーバーレイ、カスタムレンダラーなど）はUIKitのMKMapViewを使用。

### MKMapViewのSwiftUIラッパー

```swift
struct CustomOverlayMapView: UIViewRepresentable {
    let overlays: [MKOverlay]

    func makeUIView(context: Context) -> MKMapView {
        let mapView = MKMapView()
        mapView.delegate = context.coordinator
        return mapView
    }

    func updateUIView(_ mapView: MKMapView, context: Context) {
        mapView.removeOverlays(mapView.overlays)
        mapView.addOverlays(overlays)
    }

    func makeCoordinator() -> Coordinator {
        Coordinator()
    }

    class Coordinator: NSObject, MKMapViewDelegate {
        func mapView(_ mapView: MKMapView, rendererFor overlay: MKOverlay) -> MKOverlayRenderer {
            if let polygon = overlay as? MKPolygon {
                let renderer = MKPolygonRenderer(polygon: polygon)
                renderer.fillColor = UIColor.blue.withAlphaComponent(0.3)
                renderer.strokeColor = .blue
                renderer.lineWidth = 2
                return renderer
            }

            if let polyline = overlay as? MKPolyline {
                let renderer = MKPolylineRenderer(polyline: polyline)
                renderer.strokeColor = .red
                renderer.lineWidth = 3
                return renderer
            }

            if let circle = overlay as? MKCircle {
                let renderer = MKCircleRenderer(circle: circle)
                renderer.fillColor = UIColor.green.withAlphaComponent(0.3)
                renderer.strokeColor = .green
                renderer.lineWidth = 2
                return renderer
            }

            return MKOverlayRenderer(overlay: overlay)
        }
    }
}
```

### タイルオーバーレイ

```swift
class CustomTileOverlay: MKTileOverlay {
    override func url(forTilePath path: MKTileOverlayPath) -> URL {
        // カスタムタイルサーバーのURL
        let urlString = "https://tiles.example.com/\(path.z)/\(path.x)/\(path.y).png"
        return URL(string: urlString)!
    }
}

struct TileOverlayMapView: UIViewRepresentable {
    func makeUIView(context: Context) -> MKMapView {
        let mapView = MKMapView()

        let overlay = CustomTileOverlay(urlTemplate: nil)
        overlay.canReplaceMapContent = false  // true: ベースマップを置き換え
        mapView.addOverlay(overlay, level: .aboveLabels)

        return mapView
    }

    func updateUIView(_ mapView: MKMapView, context: Context) {}
}
```

## パフォーマンス最適化

### 大量のオーバーレイ

```swift
struct OptimizedOverlayMapView: View {
    let allCircles: [CircleData]
    @State private var visibleCircles: [CircleData] = []
    @State private var region: MKCoordinateRegion?

    var body: some View {
        Map()
            .onMapCameraChange { context in
                region = context.region
                updateVisibleCircles()
            }
            .overlay {
                // 可視エリア内のオーバーレイのみ表示
                Map {
                    ForEach(visibleCircles, id: \.id) { circle in
                        MapCircle(center: circle.coordinate, radius: circle.radius)
                            .foregroundStyle(.blue.opacity(0.3))
                    }
                }
            }
    }

    private func updateVisibleCircles() {
        guard let region else { return }

        // 可視範囲内のオーバーレイのみフィルタ
        visibleCircles = allCircles.filter { circle in
            isCoordinateVisible(circle.coordinate, in: region)
        }
    }

    private func isCoordinateVisible(_ coordinate: CLLocationCoordinate2D, in region: MKCoordinateRegion) -> Bool {
        let latDelta = region.span.latitudeDelta / 2
        let lonDelta = region.span.longitudeDelta / 2

        return coordinate.latitude >= region.center.latitude - latDelta &&
               coordinate.latitude <= region.center.latitude + latDelta &&
               coordinate.longitude >= region.center.longitude - lonDelta &&
               coordinate.longitude <= region.center.longitude + lonDelta
    }
}

struct CircleData: Identifiable {
    let id = UUID()
    let coordinate: CLLocationCoordinate2D
    let radius: CLLocationDistance
}
```

### 簡略化

```swift
// ズームレベルに応じてポリラインを簡略化
func simplifyPolyline(coordinates: [CLLocationCoordinate2D], tolerance: Double) -> [CLLocationCoordinate2D] {
    guard coordinates.count > 2 else { return coordinates }

    // Douglas-Peucker アルゴリズムの簡易実装
    // 実際の実装では専用ライブラリを使用することを推奨

    // 仮の簡略化（N個おきに取得）
    let step = max(1, coordinates.count / 100)
    return stride(from: 0, to: coordinates.count, by: step).map { coordinates[$0] }
}
```

## ベストプラクティス

### オーバーレイの構成

```swift
// 良い例: データ構造を分離
struct MapData {
    var circles: [CircleOverlay]
    var polygons: [PolygonOverlay]
    var polylines: [PolylineOverlay]
}

struct CircleOverlay: Identifiable {
    let id: UUID
    let center: CLLocationCoordinate2D
    let radius: CLLocationDistance
    let fillColor: Color
    let strokeColor: Color
}

// 地図ビュー
struct StructuredOverlayMapView: View {
    let mapData: MapData

    var body: some View {
        Map {
            ForEach(mapData.circles) { circle in
                MapCircle(center: circle.center, radius: circle.radius)
                    .foregroundStyle(circle.fillColor.opacity(0.3))
                    .stroke(circle.strokeColor, lineWidth: 2)
            }

            ForEach(mapData.polygons) { polygon in
                MapPolygon(coordinates: polygon.coordinates)
                    .foregroundStyle(polygon.fillColor.opacity(0.3))
                    .stroke(polygon.strokeColor, lineWidth: 2)
            }

            ForEach(mapData.polylines) { polyline in
                MapPolyline(coordinates: polyline.coordinates)
                    .stroke(polyline.color, lineWidth: polyline.lineWidth)
            }
        }
    }
}
```

### アクセシビリティ

```swift
Map {
    MapCircle(center: coordinate, radius: 500)
        .foregroundStyle(.blue.opacity(0.3))
        .stroke(.blue, lineWidth: 2)
        .accessibilityLabel("検索範囲")
        .accessibilityHint("半径500メートルのエリア")
}
```
