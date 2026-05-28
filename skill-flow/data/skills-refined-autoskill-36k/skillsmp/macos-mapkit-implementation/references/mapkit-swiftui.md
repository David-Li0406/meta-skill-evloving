# MapKit for SwiftUI (macOS 14+)

macOS 14以降で利用可能なSwiftUI Map APIの詳細リファレンス。

## Map View

### 基本構文

```swift
Map(position: $position) {
    // MapContent
}
```

### パラメータ

| パラメータ | 型 | 説明 |
|-----------|---|------|
| `position` | `Binding<MapCameraPosition>` | カメラ位置 |
| `bounds` | `MapCameraBounds?` | カメラ移動範囲制限 |
| `interactionModes` | `MapInteractionModes` | 許可する操作 |
| `selection` | `Binding<T?>` | 選択されたアイテム |
| `content` | `() -> MapContent` | マーカー等のコンテンツ |

### MapCameraPosition

```swift
// 自動調整
.automatic

// ユーザー位置追従
.userLocation(fallback: .automatic)

// 地域指定
.region(MKCoordinateRegion(...))

// カメラ指定
.camera(MapCamera(...))

// アイテムにフォーカス
.item(MKMapItem)

// 矩形領域
.rect(MKMapRect)
```

### MapInteractionModes

```swift
// すべての操作を許可
.all

// 個別指定
[.pan, .zoom, .rotate, .pitch]

// 特定の操作を無効化
MapInteractionModes.all.subtracting(.rotate)
```

### mapStyle モディファイア

```swift
.mapStyle(.standard)
.mapStyle(.standard(elevation: .realistic))
.mapStyle(.standard(pointsOfInterest: .including([.restaurant])))
.mapStyle(.imagery)
.mapStyle(.hybrid)
```

### mapControls モディファイア

```swift
.mapControls {
    MapUserLocationButton()  // ユーザー位置ボタン
    MapCompass()             // コンパス
    MapScaleView()           // スケール表示
    MapZoomStepper()         // ズームステッパー（macOS）
    MapPitchToggle()         // 傾きトグル
}
```

### onMapCameraChange

```swift
.onMapCameraChange { context in
    let region = context.region
    let rect = context.rect
    let camera = context.camera
}

// 変更終了時のみ
.onMapCameraChange(frequency: .onEnd) { context in
    // ...
}
```

## MapCamera

### 初期化

```swift
MapCamera(
    centerCoordinate: CLLocationCoordinate2D,
    distance: CLLocationDistance,  // メートル
    heading: CLLocationDirection,  // 度（0-360）
    pitch: Double                  // 度（0-90）
)
```

### プロパティ

| プロパティ | 型 | 説明 |
|-----------|---|------|
| `centerCoordinate` | `CLLocationCoordinate2D` | 中心座標 |
| `distance` | `CLLocationDistance` | 地表からの距離（メートル） |
| `heading` | `CLLocationDirection` | 方角（北=0） |
| `pitch` | `Double` | 傾き角度 |

## MapCameraBounds

カメラの移動範囲を制限。

```swift
Map(
    position: $position,
    bounds: MapCameraBounds(
        centerCoordinateBounds: MKCoordinateRegion(...),
        minimumDistance: 100,
        maximumDistance: 10000
    )
)
```

## MapStyle

### standard

```swift
.standard                              // デフォルト
.standard(elevation: .realistic)       // 3D建物
.standard(elevation: .flat)            // フラット
.standard(emphasis: .muted)            // 控えめ
.standard(pointsOfInterest: .all)      // 全POI表示
.standard(pointsOfInterest: .excluding([.restaurant]))
.standard(showsTraffic: true)          // 交通情報表示
```

### imagery

```swift
.imagery                               // 衛星写真
.imagery(elevation: .realistic)        // 3D地形
```

### hybrid

```swift
.hybrid                                // 衛星写真+ラベル
.hybrid(elevation: .realistic)
.hybrid(showsTraffic: true)
```

## MapContent

### Marker

```swift
Marker("タイトル", coordinate: coordinate)
Marker("タイトル", systemImage: "star", coordinate: coordinate)
Marker("タイトル", monogram: Text("A"), coordinate: coordinate)
    .tint(.red)
    .tag(item)  // 選択用
```

### Annotation

```swift
Annotation("タイトル", coordinate: coordinate, anchor: .bottom) {
    // カスタムView
}
```

### UserAnnotation

```swift
UserAnnotation()
UserAnnotation(anchor: .center)
```

### MapCircle

```swift
MapCircle(center: coordinate, radius: 500)
    .foregroundStyle(.blue.opacity(0.3))
    .stroke(.blue, lineWidth: 2)
```

### MapPolygon

```swift
MapPolygon(coordinates: [coord1, coord2, coord3])
    .foregroundStyle(.green.opacity(0.3))
    .stroke(.green, lineWidth: 2)
```

### MapPolyline

```swift
MapPolyline(coordinates: [coord1, coord2, coord3])
    .stroke(.blue, lineWidth: 3)

// MKRouteから
MapPolyline(route.polyline)
    .stroke(.blue, lineWidth: 5)
```

## 選択機能

```swift
@State private var selectedItem: MKMapItem?

Map(position: $position, selection: $selectedItem) {
    ForEach(items, id: \.self) { item in
        Marker(item.name ?? "", coordinate: item.placemark.coordinate)
            .tag(item)
    }
}
```

## MapReader

タップ位置から座標を取得。

```swift
MapReader { proxy in
    Map(position: $position) {
        // content
    }
    .onTapGesture { location in
        if let coordinate = proxy.convert(location, from: .local) {
            // coordinate を使用
        }
    }
}
```

## macOS固有の注意点

1. **MapZoomStepper** - macOSで利用可能なズームコントロール
2. **MapPitchToggle** - 2D/3D切り替えトグル
3. **キーボード操作** - 矢印キーでパン、+/-でズーム
4. **トラックパッド** - ピンチでズーム、2本指で回転
5. **マウス** - スクロールでズーム、右ドラッグで回転
