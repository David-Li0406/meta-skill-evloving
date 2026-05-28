# AppKit Integration

AppKitアプリでMKMapViewを使用する方法。

## NSViewRepresentable

SwiftUIからAppKitのMKMapViewを使用する場合。

### 基本実装

```swift
import SwiftUI
import MapKit

struct AppKitMapView: NSViewRepresentable {
    @Binding var region: MKCoordinateRegion

    func makeNSView(context: Context) -> MKMapView {
        let mapView = MKMapView()
        mapView.delegate = context.coordinator
        return mapView
    }

    func updateNSView(_ mapView: MKMapView, context: Context) {
        mapView.setRegion(region, animated: true)
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
    }
}
```

## MKMapView 設定

### 表示設定

```swift
// 基本表示
mapView.showsUserLocation = true
mapView.showsCompass = true
mapView.showsZoomControls = true  // macOS
mapView.showsScale = true

// 地図タイプ
mapView.mapType = .standard      // 標準
mapView.mapType = .satellite     // 衛星
mapView.mapType = .hybrid        // ハイブリッド
mapView.mapType = .mutedStandard // 控えめ
```

### 操作設定

```swift
mapView.isZoomEnabled = true
mapView.isScrollEnabled = true
mapView.isRotateEnabled = true
mapView.isPitchEnabled = true
```

### カメラ設定

```swift
// 地域設定
mapView.setRegion(region, animated: true)

// カメラ設定
let camera = MKMapCamera(
    lookingAtCenter: coordinate,
    fromDistance: 1000,
    pitch: 45,
    heading: 0
)
mapView.setCamera(camera, animated: true)

// 中心座標
mapView.setCenter(coordinate, animated: true)
```

## MKMapViewDelegate

### 地域変更

```swift
// 変更開始
func mapView(_ mapView: MKMapView, regionWillChangeAnimated animated: Bool) {
    // ユーザー操作開始
}

// 変更完了
func mapView(_ mapView: MKMapView, regionDidChangeAnimated animated: Bool) {
    // 新しい地域: mapView.region
}
```

### アノテーション

```swift
// カスタムアノテーションビュー
func mapView(_ mapView: MKMapView, viewFor annotation: MKAnnotation) -> MKAnnotationView? {
    // ユーザー位置はデフォルト
    guard !(annotation is MKUserLocation) else { return nil }

    let identifier = "CustomAnnotation"
    var view = mapView.dequeueReusableAnnotationView(withIdentifier: identifier) as? MKMarkerAnnotationView

    if view == nil {
        view = MKMarkerAnnotationView(annotation: annotation, reuseIdentifier: identifier)
        view?.canShowCallout = true

        // コールアウトアクセサリ
        view?.rightCalloutAccessoryView = NSButton(title: "詳細", target: nil, action: nil)
    } else {
        view?.annotation = annotation
    }

    return view
}

// コールアウトタップ
func mapView(_ mapView: MKMapView, annotationView view: MKAnnotationView, calloutAccessoryControlTapped control: NSView) {
    guard let annotation = view.annotation else { return }
    // 処理
}
```

### オーバーレイ

```swift
func mapView(_ mapView: MKMapView, rendererFor overlay: MKOverlay) -> MKOverlayRenderer {
    if let polyline = overlay as? MKPolyline {
        let renderer = MKPolylineRenderer(polyline: polyline)
        renderer.strokeColor = .systemBlue
        renderer.lineWidth = 4
        return renderer
    }

    if let circle = overlay as? MKCircle {
        let renderer = MKCircleRenderer(circle: circle)
        renderer.fillColor = NSColor.systemBlue.withAlphaComponent(0.2)
        renderer.strokeColor = .systemBlue
        renderer.lineWidth = 2
        return renderer
    }

    if let polygon = overlay as? MKPolygon {
        let renderer = MKPolygonRenderer(polygon: polygon)
        renderer.fillColor = NSColor.systemGreen.withAlphaComponent(0.2)
        renderer.strokeColor = .systemGreen
        renderer.lineWidth = 2
        return renderer
    }

    return MKOverlayRenderer(overlay: overlay)
}
```

## アノテーション管理

### 追加・削除

```swift
// 追加
mapView.addAnnotation(annotation)
mapView.addAnnotations([annotation1, annotation2])

// 削除
mapView.removeAnnotation(annotation)
mapView.removeAnnotations(mapView.annotations)

// 特定のアノテーション以外を削除
let toRemove = mapView.annotations.filter { !($0 is MKUserLocation) }
mapView.removeAnnotations(toRemove)
```

### カスタムアノテーションクラス

```swift
class CustomAnnotation: NSObject, MKAnnotation {
    let coordinate: CLLocationCoordinate2D
    let title: String?
    let subtitle: String?

    init(coordinate: CLLocationCoordinate2D, title: String?, subtitle: String? = nil) {
        self.coordinate = coordinate
        self.title = title
        self.subtitle = subtitle
        super.init()
    }
}
```

## オーバーレイ管理

### 追加・削除

```swift
// 追加
mapView.addOverlay(overlay)
mapView.addOverlays([overlay1, overlay2])

// 削除
mapView.removeOverlay(overlay)
mapView.removeOverlays(mapView.overlays)

// 特定レベルに追加
mapView.addOverlay(overlay, level: .aboveRoads)
mapView.addOverlay(overlay, level: .aboveLabels)
```

### オーバーレイ作成

```swift
// 円
let circle = MKCircle(center: coordinate, radius: 500)

// ポリライン
let polyline = MKPolyline(coordinates: &coordinates, count: coordinates.count)

// ポリゴン
let polygon = MKPolygon(coordinates: &coordinates, count: coordinates.count)
```

## MKAnnotationView カスタマイズ

### MKMarkerAnnotationView

```swift
let view = MKMarkerAnnotationView(annotation: annotation, reuseIdentifier: identifier)
view.markerTintColor = .systemBlue
view.glyphText = "A"
view.glyphImage = NSImage(systemSymbolName: "star.fill", accessibilityDescription: nil)
view.canShowCallout = true
view.animatesWhenAdded = true
view.displayPriority = .required
```

### カスタムビュー

```swift
let view = MKAnnotationView(annotation: annotation, reuseIdentifier: identifier)
view.image = NSImage(named: "customMarker")
view.centerOffset = CGPoint(x: 0, y: -view.image!.size.height / 2)
view.canShowCallout = true
```

## macOS固有の機能

### ズームコントロール

```swift
mapView.showsZoomControls = true  // macOSのみ
```

### キーボード操作

- 矢印キー: パン
- +/-: ズーム
- Command + 矢印: 回転

### マウス・トラックパッド

- スクロール: ズーム
- ピンチ: ズーム
- 2本指回転: 回転
- 右クリックドラッグ: 回転

## NSWindowとの連携

```swift
// ウィンドウサイズに合わせてリサイズ
mapView.autoresizingMask = [.width, .height]

// フルスクリーン対応
mapView.allowsFullScreen = true
```
