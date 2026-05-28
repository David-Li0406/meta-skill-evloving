# Look Around (macOS)

macOSでのLook Around機能の詳細ガイド。

## 概要

Look Aroundは、Appleのストリートレベル画像サービスで、地図上の特定の場所を360度見渡すことができます。

**macOS制限事項:**
- macOS 15時点で、フルスクリーンナビゲーションボタンが表示されない問題が報告されている
- 埋め込みプレビューは正常に動作する

## MKLookAroundSceneRequest

シーンの存在確認と取得。

### 基本実装

```swift
func getLookAroundScene(for coordinate: CLLocationCoordinate2D) async -> MKLookAroundScene? {
    let request = MKLookAroundSceneRequest(coordinate: coordinate)

    do {
        return try await request.scene
    } catch {
        return nil
    }
}
```

### キャンセル

```swift
let request = MKLookAroundSceneRequest(coordinate: coordinate)

// キャンセル
request.cancel()

// キャンセル状態確認
if request.isCancelled {
    // キャンセルされた
}
```

## LookAroundPreview (SwiftUI)

### 基本使用

```swift
@State private var lookAroundScene: MKLookAroundScene?

var body: some View {
    VStack {
        if let scene = lookAroundScene {
            LookAroundPreview(initialScene: scene)
                .frame(height: 300)
        } else {
            ContentUnavailableView(
                "Look Around利用不可",
                systemImage: "eye.slash",
                description: Text("この場所ではLook Aroundが利用できません")
            )
        }
    }
    .task {
        lookAroundScene = await getLookAroundScene(for: coordinate)
    }
}
```

### バインディング使用

```swift
@State private var scene: MKLookAroundScene?

LookAroundPreview(initialScene: scene, allowsNavigation: true, showsRoadLabels: true)
```

### パラメータ

| パラメータ | 型 | 説明 |
|-----------|---|------|
| `initialScene` | `MKLookAroundScene?` | 初期シーン |
| `allowsNavigation` | `Bool` | ナビゲーション許可 |
| `showsRoadLabels` | `Bool` | 道路ラベル表示 |
| `pointOfInterestFilter` | `MKPointOfInterestFilter?` | POIフィルター |
| `badgePosition` | `MKLookAroundBadgePosition` | バッジ位置 |

## MKLookAroundViewController (AppKit)

AppKitでの使用。

### NSViewControllerRepresentable

```swift
struct LookAroundViewControllerRepresentable: NSViewControllerRepresentable {
    let scene: MKLookAroundScene

    func makeNSViewController(context: Context) -> MKLookAroundViewController {
        let controller = MKLookAroundViewController(scene: scene)
        controller.delegate = context.coordinator
        return controller
    }

    func updateNSViewController(_ controller: MKLookAroundViewController, context: Context) {
        controller.scene = scene
    }

    func makeCoordinator() -> Coordinator {
        Coordinator()
    }

    class Coordinator: NSObject, MKLookAroundViewControllerDelegate {
        func lookAroundViewControllerWillUpdateScene(_ viewController: MKLookAroundViewController) {
            // シーン更新開始
        }

        func lookAroundViewControllerDidUpdateScene(_ viewController: MKLookAroundViewController) {
            // シーン更新完了
        }

        func lookAroundViewController(_ viewController: MKLookAroundViewController, didFailLoadingSceneWithError error: Error) {
            // シーン読み込み失敗
        }
    }
}
```

## 地図との連携

### 選択位置のLook Around

```swift
struct MapWithLookAroundView: View {
    @State private var position: MapCameraPosition = .automatic
    @State private var selectedItem: MKMapItem?
    @State private var lookAroundScene: MKLookAroundScene?

    var body: some View {
        VStack(spacing: 0) {
            // 地図
            Map(position: $position, selection: $selectedItem) {
                ForEach(landmarks, id: \.self) { landmark in
                    Marker(landmark.name ?? "", coordinate: landmark.placemark.coordinate)
                }
            }
            .onChange(of: selectedItem) { _, newItem in
                if let item = newItem {
                    Task {
                        await loadScene(for: item.placemark.coordinate)
                    }
                }
            }

            // Look Around
            if let scene = lookAroundScene {
                LookAroundPreview(initialScene: scene)
                    .frame(height: 200)
            }
        }
    }

    private func loadScene(for coordinate: CLLocationCoordinate2D) async {
        lookAroundScene = nil
        let request = MKLookAroundSceneRequest(coordinate: coordinate)
        lookAroundScene = try? await request.scene
    }
}
```

## フォールバック実装

Look Aroundが利用できない場合の代替表示。

### 3D衛星画像

```swift
@State private var lookAroundScene: MKLookAroundScene?

var body: some View {
    VStack {
        if let scene = lookAroundScene {
            LookAroundPreview(initialScene: scene)
                .frame(height: 300)
        } else {
            // フォールバック: 3D衛星画像
            Map(position: .constant(.camera(MapCamera(
                centerCoordinate: coordinate,
                distance: 200,
                heading: 0,
                pitch: 60
            )))) {
                Marker("", coordinate: coordinate)
            }
            .mapStyle(.imagery(elevation: .realistic))
            .frame(height: 300)
            .overlay(alignment: .topLeading) {
                Text("Look Around利用不可")
                    .font(.caption)
                    .padding(4)
                    .background(.regularMaterial)
                    .clipShape(RoundedRectangle(cornerRadius: 4))
                    .padding(8)
            }
        }
    }
}
```

### 静止画像

```swift
// Apple Maps Static APIは公開されていないため、
// 通常の地図スナップショットを使用

func createMapSnapshot(coordinate: CLLocationCoordinate2D) async -> NSImage? {
    let options = MKMapSnapshotter.Options()
    options.region = MKCoordinateRegion(
        center: coordinate,
        span: MKCoordinateSpan(latitudeDelta: 0.005, longitudeDelta: 0.005)
    )
    options.mapType = .satellite
    options.size = NSSize(width: 400, height: 300)

    let snapshotter = MKMapSnapshotter(options: options)

    do {
        let snapshot = try await snapshotter.start()
        return snapshot.image
    } catch {
        return nil
    }
}
```

## macOS固有の制限事項

### 1. フルスクリーンナビゲーション

macOS 15時点で、LookAroundPreviewのフルスクリーンボタンが表示されない、または動作しない場合があります。

**回避策:**
- 埋め込みプレビューのみ使用
- シートやポップオーバーで大きく表示

### 2. インタラクション

- パン（ドラッグ）で視点移動
- ピンチでズーム
- マウスホイールでズーム

### 3. カバレッジ

Look Aroundは限られた地域でのみ利用可能です。日本国内でも一部エリアのみ対応。

## カバレッジ確認

```swift
func checkLookAroundAvailability(for coordinate: CLLocationCoordinate2D) async -> Bool {
    let request = MKLookAroundSceneRequest(coordinate: coordinate)

    do {
        let scene = try await request.scene
        return scene != nil
    } catch {
        return false
    }
}
```

## エラーハンドリング

```swift
func getLookAroundScene(for coordinate: CLLocationCoordinate2D) async throws -> MKLookAroundScene {
    let request = MKLookAroundSceneRequest(coordinate: coordinate)

    do {
        guard let scene = try await request.scene else {
            throw LookAroundError.notAvailable
        }
        return scene
    } catch let error as MKError {
        switch error.code {
        case .serverFailure:
            throw LookAroundError.serverError
        case .loadingThrottled:
            throw LookAroundError.rateLimited
        default:
            throw LookAroundError.unknown(error)
        }
    }
}

enum LookAroundError: Error {
    case notAvailable
    case serverError
    case rateLimited
    case unknown(Error)
}
```

## 使用上の注意

1. **カバレッジ** - 全ての場所で利用可能ではない
2. **ネットワーク** - オンライン接続が必要
3. **macOS制限** - フルスクリーン機能に制限あり
4. **フォールバック** - 利用不可時の代替UIを用意
5. **パフォーマンス** - 3D表示は重い場合がある
