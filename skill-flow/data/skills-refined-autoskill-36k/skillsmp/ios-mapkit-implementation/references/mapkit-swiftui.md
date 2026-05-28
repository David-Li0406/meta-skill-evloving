# MapKit for SwiftUI API Reference

iOS 17+で刷新されたMapKit for SwiftUIの詳細リファレンス。

## Map View

### 基本的な初期化

```swift
// 基本的なMap
Map()

// カメラ位置をバインディング
@State private var position: MapCameraPosition = .automatic
Map(position: $position)

// 初期位置を指定（バインディングなし）
Map(initialPosition: .region(region))

// 選択状態をバインディング
@State private var selection: MapFeature?
Map(selection: $selection)
```

### Map Content Builder

```swift
Map {
    // Marker
    Marker("Tokyo", coordinate: .tokyo)

    // Annotation
    Annotation("Custom", coordinate: location) {
        CustomView()
    }

    // User Location
    UserAnnotation()

    // Overlays
    MapCircle(center: center, radius: 500)
    MapPolyline(coordinates: path)
    MapPolygon(coordinates: polygon)
}
```

## MapCameraPosition

カメラの位置と向きを制御する列挙型。

### 種類

```swift
// 自動（コンテンツに合わせて調整）
.automatic

// ユーザー位置を追従
.userLocation(fallback: .automatic)
.userLocation(followsHeading: true, fallback: .automatic)

// 特定の地域を表示
.region(MKCoordinateRegion)

// カメラアングル指定
.camera(MapCamera)

// 特定のアイテムを表示
.item(MKMapItem)

// 複数の座標を含む領域
.rect(MKMapRect)
```

### MapCamera

```swift
let camera = MapCamera(
    centerCoordinate: CLLocationCoordinate2D(latitude: 35.6762, longitude: 139.6503),
    distance: 1000,        // メートル単位の距離
    heading: 45,           // 北からの角度（0-360）
    pitch: 60              // 傾き角度（0-90）
)

let position: MapCameraPosition = .camera(camera)
```

### MKCoordinateRegion

```swift
let region = MKCoordinateRegion(
    center: CLLocationCoordinate2D(latitude: 35.6762, longitude: 139.6503),
    span: MKCoordinateSpan(latitudeDelta: 0.1, longitudeDelta: 0.1)
)

// または距離指定
let region = MKCoordinateRegion(
    center: coordinate,
    latitudinalMeters: 1000,
    longitudinalMeters: 1000
)
```

## MapStyle

地図の外観スタイルを設定。

### 標準スタイル

```swift
// 基本
.mapStyle(.standard)

// 3D建物表示
.mapStyle(.standard(elevation: .realistic))

// 高架・平面
.mapStyle(.standard(elevation: .flat))

// 建物強調
.mapStyle(.standard(emphasis: .automatic))
.mapStyle(.standard(emphasis: .muted))

// POIフィルタリング
.mapStyle(.standard(pointsOfInterest: .all))
.mapStyle(.standard(pointsOfInterest: .excludingAll))
.mapStyle(.standard(pointsOfInterest: .including([.restaurant, .cafe, .hotel])))
.mapStyle(.standard(pointsOfInterest: .excluding([.parking])))

// 交通情報表示
.mapStyle(.standard(showsTraffic: true))
```

### 衛星写真スタイル

```swift
// 衛星写真のみ
.mapStyle(.imagery)

// 3D地形
.mapStyle(.imagery(elevation: .realistic))

// 衛星写真 + ラベル
.mapStyle(.hybrid)

// 衛星写真 + ラベル + 3D
.mapStyle(.hybrid(elevation: .realistic))

// POIフィルタリング
.mapStyle(.hybrid(pointsOfInterest: .including([.airport])))
```

### POI Categories

```swift
// 主要なカテゴリ
MKPointOfInterestCategory.airport
MKPointOfInterestCategory.cafe
MKPointOfInterestCategory.hospital
MKPointOfInterestCategory.hotel
MKPointOfInterestCategory.museum
MKPointOfInterestCategory.park
MKPointOfInterestCategory.parking
MKPointOfInterestCategory.publicTransport
MKPointOfInterestCategory.restaurant
MKPointOfInterestCategory.store
// ... 他多数
```

## Marker

システム提供のマーカー表示。

### 基本的な使用

```swift
// テキストラベル
Marker("Tokyo", coordinate: coordinate)

// システムイメージ
Marker("Restaurant", systemImage: "fork.knife", coordinate: coordinate)

// モノグラム（1文字）
Marker("A", monogram: Text("A"), coordinate: coordinate)

// イメージ
Marker("Photo", image: "custom-image", coordinate: coordinate)
```

### カスタマイズ

```swift
Marker("Cafe", systemImage: "cup.and.saucer.fill", coordinate: coordinate)
    .tint(.brown)           // マーカーの色

Marker("Selected", coordinate: coordinate)
    .tag(item)              // 選択用のタグ
```

## Annotation

カスタムビューをマーカーとして表示。

### 基本的な使用

```swift
Annotation("Label", coordinate: coordinate) {
    // カスタムビュー
    Image(systemName: "star.fill")
        .foregroundStyle(.yellow)
        .padding(8)
        .background(.white)
        .clipShape(Circle())
}
```

### アンカー位置

```swift
Annotation("Label", coordinate: coordinate, anchor: .bottom) {
    // .bottom: ビューの下端が座標位置
    // .center: ビューの中心が座標位置
    // .top: ビューの上端が座標位置
    CustomView()
}
```

### 選択可能なAnnotation

```swift
@State private var selection: PlaceItem?

Map(selection: $selection) {
    ForEach(places) { place in
        Annotation(place.name, coordinate: place.coordinate) {
            PlaceView(place: place, isSelected: selection == place)
        }
        .tag(place)
    }
}
```

## UserAnnotation

ユーザーの現在位置を表示。

```swift
Map {
    // デフォルトスタイル
    UserAnnotation()

    // 可視性制御
    UserAnnotation(anchor: .center)
}
```

## Map Controls

地図上のコントロールUI。

### 使用方法

```swift
Map()
    .mapControls {
        // ユーザー位置ボタン
        MapUserLocationButton()

        // コンパス（回転時のみ表示）
        MapCompass()

        // スケールバー（ズーム時に表示）
        MapScaleView()

        // ピッチ切り替え
        MapPitchToggle()
    }
```

### MapUserLocationButton

```swift
MapUserLocationButton()
    // タップするとユーザー位置にアニメーション移動
```

### MapCompass

```swift
MapCompass()
    // 地図が北向きでない時に表示
    // タップで北向きに戻る
```

### 可視性制御

```swift
Map()
    .mapControlVisibility(.hidden)     // 全て非表示
    .mapControlVisibility(.visible)    // 全て表示
    .mapControlVisibility(.automatic)  // 自動（デフォルト）
```

## Map Interaction

### インタラクションモード

```swift
Map(interactionModes: .all)          // 全ての操作を許可
Map(interactionModes: [.pan, .zoom]) // パンとズームのみ
Map(interactionModes: .pan)          // パンのみ
Map(interactionModes: [])            // 操作を禁止
```

### 利用可能なモード

```swift
MapInteractionModes.all      // 全て
MapInteractionModes.pan      // パン（移動）
MapInteractionModes.zoom     // ズーム
MapInteractionModes.rotate   // 回転
MapInteractionModes.pitch    // 傾き
```

## Overlays

### MapCircle

```swift
MapCircle(center: coordinate, radius: 500)  // メートル単位
    .foregroundStyle(.blue.opacity(0.3))
    .stroke(.blue, lineWidth: 2)
```

### MapPolyline

```swift
// 座標配列から
MapPolyline(coordinates: [coord1, coord2, coord3])
    .stroke(.red, lineWidth: 3)

// MKPolylineから（経路表示など）
MapPolyline(route.polyline)
    .stroke(.blue, lineWidth: 5)
```

### MapPolygon

```swift
MapPolygon(coordinates: [coord1, coord2, coord3, coord4])
    .foregroundStyle(.green.opacity(0.3))
    .stroke(.green, lineWidth: 2)
```

## Map Selection

### Feature Selection

```swift
@State private var selectedFeature: MapFeature?

Map(selection: $selectedFeature) {
    // コンテンツ
}
.onMapFeatureSelection { feature in
    // 選択されたPOI等の処理
}
```

### Marker/Annotation Selection

```swift
@State private var selectedItem: PlaceItem?

Map(selection: $selectedItem) {
    ForEach(places) { place in
        Marker(place.name, coordinate: place.coordinate)
            .tag(place)
    }
}
.onChange(of: selectedItem) { _, newValue in
    if let place = newValue {
        // 選択されたアイテムの処理
    }
}
```

## Camera Animation

### プログラムによるカメラ移動

```swift
@State private var position: MapCameraPosition = .automatic

// 即座に移動
position = .region(newRegion)

// アニメーション付きで移動
withAnimation(.easeInOut(duration: 0.5)) {
    position = .camera(newCamera)
}
```

### MapCameraUpdateContext

```swift
Map()
    .onMapCameraChange { context in
        // context.region - 現在の表示領域
        // context.camera - 現在のカメラ設定
    }
    .onMapCameraChange(frequency: .continuous) { context in
        // 連続的に呼ばれる（パフォーマンス注意）
    }
```

## Map Bounds

### 表示範囲の制限

```swift
Map(bounds: MapCameraBounds(
    centerCoordinateBounds: MKCoordinateRegion(
        center: CLLocationCoordinate2D(latitude: 35.6762, longitude: 139.6503),
        span: MKCoordinateSpan(latitudeDelta: 1.0, longitudeDelta: 1.0)
    ),
    minimumDistance: 100,    // 最小ズーム距離
    maximumDistance: 10000   // 最大ズーム距離
))
```

## Best Practices

### パフォーマンス

```swift
// 大量のマーカーは ForEach で
Map {
    ForEach(places) { place in
        Marker(place.name, coordinate: place.coordinate)
    }
}

// 不要なリビルドを避ける
// MapCameraPosition の変更頻度を最小限に
```

### アクセシビリティ

```swift
Marker("Tokyo Station", systemImage: "tram.fill", coordinate: coordinate)
    .accessibilityLabel("東京駅")
    .accessibilityHint("タップして詳細を表示")
```

### メモリ管理

```swift
// 大量の Annotation のカスタムビューは軽量に
Annotation(place.name, coordinate: place.coordinate) {
    // 重いビューは避ける
    Circle()
        .fill(.blue)
        .frame(width: 20, height: 20)
}
```
