# カスタムオーバーレイ

MapKitのオーバーレイ機能の詳細リファレンス。

## SwiftUI オーバーレイ

### MapCircle

円形オーバーレイ。

```swift
Map(position: $position) {
    MapCircle(center: coordinate, radius: 500)
        .foregroundStyle(.blue.opacity(0.3))
        .stroke(.blue, lineWidth: 2)
}
```

### MapPolygon

多角形オーバーレイ。

```swift
let polygonCoordinates = [
    CLLocationCoordinate2D(latitude: 35.69, longitude: 139.76),
    CLLocationCoordinate2D(latitude: 35.69, longitude: 139.78),
    CLLocationCoordinate2D(latitude: 35.67, longitude: 139.78),
    CLLocationCoordinate2D(latitude: 35.67, longitude: 139.76)
]

Map(position: $position) {
    MapPolygon(coordinates: polygonCoordinates)
        .foregroundStyle(.green.opacity(0.3))
        .stroke(.green, lineWidth: 2)
}
```

### MapPolyline

線オーバーレイ。

```swift
let routeCoordinates = [
    CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671),
    CLLocationCoordinate2D(latitude: 35.6580, longitude: 139.7016)
]

Map(position: $position) {
    MapPolyline(coordinates: routeCoordinates)
        .stroke(.blue, lineWidth: 4)
}

// MKRouteから
MapPolyline(route.polyline)
    .stroke(.blue, lineWidth: 5)
```

### スタイル設定

```swift
MapPolyline(coordinates: coordinates)
    .stroke(.blue, lineWidth: 4)

// グラデーション
MapPolyline(coordinates: coordinates)
    .stroke(
        LinearGradient(
            colors: [.blue, .green],
            startPoint: .leading,
            endPoint: .trailing
        ),
        lineWidth: 4
    )

// 破線
MapPolyline(coordinates: coordinates)
    .stroke(.blue, style: StrokeStyle(lineWidth: 4, dash: [10, 5]))
```

## AppKit オーバーレイ

### MKCircle

```swift
let circle = MKCircle(center: coordinate, radius: 500)
mapView.addOverlay(circle)
```

### MKPolygon

```swift
var coordinates = [
    CLLocationCoordinate2D(latitude: 35.69, longitude: 139.76),
    CLLocationCoordinate2D(latitude: 35.69, longitude: 139.78),
    CLLocationCoordinate2D(latitude: 35.67, longitude: 139.78),
    CLLocationCoordinate2D(latitude: 35.67, longitude: 139.76)
]

let polygon = MKPolygon(coordinates: &coordinates, count: coordinates.count)
mapView.addOverlay(polygon)
```

### MKPolyline

```swift
var coordinates = [
    CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671),
    CLLocationCoordinate2D(latitude: 35.6580, longitude: 139.7016)
]

let polyline = MKPolyline(coordinates: &coordinates, count: coordinates.count)
mapView.addOverlay(polyline)
```

### 穴あきポリゴン

```swift
// 外側のポリゴン
var outerCoordinates = [...]
let outerPolygon = MKPolygon(coordinates: &outerCoordinates, count: outerCoordinates.count)

// 穴（内側）
var holeCoordinates = [...]
let hole = MKPolygon(coordinates: &holeCoordinates, count: holeCoordinates.count)

// 穴あきポリゴンを作成
let polygonWithHole = MKPolygon(
    coordinates: &outerCoordinates,
    count: outerCoordinates.count,
    interiorPolygons: [hole]
)
mapView.addOverlay(polygonWithHole)
```

## MKMapViewDelegate

### レンダラー設定

```swift
func mapView(_ mapView: MKMapView, rendererFor overlay: MKOverlay) -> MKOverlayRenderer {
    if let circle = overlay as? MKCircle {
        let renderer = MKCircleRenderer(circle: circle)
        renderer.fillColor = NSColor.blue.withAlphaComponent(0.2)
        renderer.strokeColor = .blue
        renderer.lineWidth = 2
        return renderer
    }

    if let polygon = overlay as? MKPolygon {
        let renderer = MKPolygonRenderer(polygon: polygon)
        renderer.fillColor = NSColor.green.withAlphaComponent(0.2)
        renderer.strokeColor = .green
        renderer.lineWidth = 2
        return renderer
    }

    if let polyline = overlay as? MKPolyline {
        let renderer = MKPolylineRenderer(polyline: polyline)
        renderer.strokeColor = .blue
        renderer.lineWidth = 4
        return renderer
    }

    return MKOverlayRenderer(overlay: overlay)
}
```

### 線スタイル

```swift
let renderer = MKPolylineRenderer(polyline: polyline)
renderer.strokeColor = .blue
renderer.lineWidth = 4
renderer.lineCap = .round          // 線端: 丸
renderer.lineJoin = .round         // 接合: 丸
renderer.lineDashPattern = [10, 5] // 破線パターン
renderer.alpha = 0.8               // 透明度
```

## オーバーレイ管理

### 追加

```swift
// 単一追加
mapView.addOverlay(overlay)

// 複数追加
mapView.addOverlays([overlay1, overlay2])

// レベル指定
mapView.addOverlay(overlay, level: .aboveRoads)   // 道路の上
mapView.addOverlay(overlay, level: .aboveLabels)  // ラベルの上
```

### 削除

```swift
// 単一削除
mapView.removeOverlay(overlay)

// 複数削除
mapView.removeOverlays(overlays)

// 全削除
mapView.removeOverlays(mapView.overlays)
```

### 順序変更

```swift
// 最前面に
mapView.insertOverlay(overlay, at: mapView.overlays.count)

// 最背面に
mapView.insertOverlay(overlay, at: 0)

// 特定のオーバーレイの上に
mapView.insertOverlay(overlay, above: existingOverlay)

// 特定のオーバーレイの下に
mapView.insertOverlay(overlay, below: existingOverlay)

// 入れ替え
mapView.exchangeOverlay(overlay1, with: overlay2)
```

## カスタムオーバーレイ

### MKOverlayクラス

```swift
class CustomOverlay: NSObject, MKOverlay {
    let coordinate: CLLocationCoordinate2D
    let boundingMapRect: MKMapRect

    init(coordinate: CLLocationCoordinate2D, radius: CLLocationDistance) {
        self.coordinate = coordinate

        let region = MKCoordinateRegion(
            center: coordinate,
            latitudinalMeters: radius * 2,
            longitudinalMeters: radius * 2
        )
        self.boundingMapRect = MKMapRect(region)

        super.init()
    }
}
```

### カスタムレンダラー

```swift
class CustomOverlayRenderer: MKOverlayRenderer {
    override func draw(_ mapRect: MKMapRect, zoomScale: MKZoomScale, in context: CGContext) {
        guard let overlay = overlay as? CustomOverlay else { return }

        let rect = self.rect(for: overlay.boundingMapRect)

        context.setFillColor(NSColor.blue.withAlphaComponent(0.3).cgColor)
        context.setStrokeColor(NSColor.blue.cgColor)
        context.setLineWidth(2 / zoomScale)

        context.addEllipse(in: rect)
        context.drawPath(using: .fillStroke)
    }
}
```

## パフォーマンス最適化

### boundingMapRect

```swift
// 効率的なboundingMapRect計算
class EfficientOverlay: NSObject, MKOverlay {
    let coordinate: CLLocationCoordinate2D
    private(set) var boundingMapRect: MKMapRect

    init(coordinates: [CLLocationCoordinate2D]) {
        guard let first = coordinates.first else {
            self.coordinate = CLLocationCoordinate2D()
            self.boundingMapRect = MKMapRect.null
            super.init()
            return
        }

        var rect = MKMapRect(origin: MKMapPoint(first), size: MKMapSize(width: 0, height: 0))

        for coord in coordinates {
            let point = MKMapPoint(coord)
            let pointRect = MKMapRect(origin: point, size: MKMapSize(width: 0, height: 0))
            rect = rect.union(pointRect)
        }

        self.coordinate = first
        self.boundingMapRect = rect

        super.init()
    }
}
```

### レンダリング最適化

```swift
class OptimizedRenderer: MKOverlayRenderer {
    override func draw(_ mapRect: MKMapRect, zoomScale: MKZoomScale, in context: CGContext) {
        // 表示範囲外は描画しない
        guard mapRect.intersects(overlay.boundingMapRect) else { return }

        // ズームレベルに応じた詳細度調整
        let lineWidth = 4 / zoomScale

        // 描画処理
    }
}
```

## 使用例

### 範囲表示

```swift
// 検索範囲を表示
MapCircle(center: searchCenter, radius: searchRadius)
    .foregroundStyle(.blue.opacity(0.1))
    .stroke(.blue, lineWidth: 1)
```

### エリアハイライト

```swift
// 特定エリアをハイライト
MapPolygon(coordinates: areaCoordinates)
    .foregroundStyle(.yellow.opacity(0.3))
    .stroke(.orange, lineWidth: 2)
```

### 経路表示

```swift
// 移動経路を表示
MapPolyline(coordinates: trackingHistory.map { $0.coordinate })
    .stroke(.blue, lineWidth: 3)
```
