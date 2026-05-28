# Look Around Reference

Look Around機能（Apple版ストリートビュー）の詳細ガイド。iOS 17+対応。

## 概要

Look Aroundは、Apple Mapsの360度パノラマビュー機能。特定の場所の街路レベルの画像を表示できる。

**対応地域:**
- 主要都市の一部（米国、ヨーロッパ、日本の一部都市など）
- 全ての場所で利用可能ではないため、可用性チェックが必要

## MKLookAroundSceneRequest

Look Aroundシーンを取得するリクエスト。

### 基本的な使用

```swift
func getLookAroundScene(for coordinate: CLLocationCoordinate2D) async -> MKLookAroundScene? {
    let request = MKLookAroundSceneRequest(coordinate: coordinate)

    do {
        return try await request.scene
    } catch {
        // シーンが利用できない場所
        return nil
    }
}
```

### MKMapItemから取得

```swift
func getLookAroundScene(for mapItem: MKMapItem) async -> MKLookAroundScene? {
    let request = MKLookAroundSceneRequest(mapItem: mapItem)

    do {
        return try await request.scene
    } catch {
        return nil
    }
}
```

## MKLookAroundScene

Look Aroundシーンデータ。

```swift
let scene: MKLookAroundScene

// シーンのプロパティは主に内部使用
// LookAroundPreviewやMKLookAroundViewControllerに渡して使用
```

## LookAroundPreview (SwiftUI)

SwiftUIでLook Aroundプレビューを埋め込み表示。

### 基本的な使用

```swift
struct LookAroundView: View {
    let coordinate: CLLocationCoordinate2D
    @State private var scene: MKLookAroundScene?
    @State private var isLoading = true

    var body: some View {
        Group {
            if isLoading {
                ProgressView()
            } else if let scene {
                LookAroundPreview(scene: scene)
            } else {
                ContentUnavailableView(
                    "Look Around利用不可",
                    systemImage: "eye.slash",
                    description: Text("この場所ではLook Aroundを利用できません")
                )
            }
        }
        .task {
            await loadScene()
        }
    }

    private func loadScene() async {
        isLoading = true
        defer { isLoading = false }

        let request = MKLookAroundSceneRequest(coordinate: coordinate)
        scene = try? await request.scene
    }
}
```

### プレビューのカスタマイズ

```swift
LookAroundPreview(scene: scene)
    .frame(height: 200)
    .clipShape(RoundedRectangle(cornerRadius: 12))
```

### 初期方向の設定

```swift
LookAroundPreview(
    initialScene: scene,
    allowsNavigation: true,     // ナビゲーション許可
    badgePosition: .bottomTrailing  // バッジ位置
)
```

## LookAroundPreview Options

### allowsNavigation

```swift
// ユーザーが別の場所に移動できるか
LookAroundPreview(scene: scene, allowsNavigation: true)  // 移動可能
LookAroundPreview(scene: scene, allowsNavigation: false) // 固定
```

### badgePosition

```swift
// Apple Mapsバッジの位置
LookAroundPreview(scene: scene, badgePosition: .topLeading)
LookAroundPreview(scene: scene, badgePosition: .topTrailing)
LookAroundPreview(scene: scene, badgePosition: .bottomLeading)
LookAroundPreview(scene: scene, badgePosition: .bottomTrailing)
```

## MKLookAroundViewController (UIKit)

フルスクリーンのLook Around表示。

### SwiftUIからの使用

```swift
struct LookAroundFullScreenView: UIViewControllerRepresentable {
    let scene: MKLookAroundScene

    func makeUIViewController(context: Context) -> MKLookAroundViewController {
        let controller = MKLookAroundViewController(scene: scene)
        controller.delegate = context.coordinator
        return controller
    }

    func updateUIViewController(_ uiViewController: MKLookAroundViewController, context: Context) {
        uiViewController.scene = scene
    }

    func makeCoordinator() -> Coordinator {
        Coordinator()
    }

    class Coordinator: NSObject, MKLookAroundViewControllerDelegate {
        func lookAroundViewControllerWillUpdateScene(_ viewController: MKLookAroundViewController) {
            // シーン更新前
        }

        func lookAroundViewControllerDidUpdateScene(_ viewController: MKLookAroundViewController) {
            // シーン更新後
        }

        func lookAroundViewControllerWillDismissFullScreen(_ viewController: MKLookAroundViewController) {
            // フルスクリーン終了前
        }

        func lookAroundViewControllerDidDismissFullScreen(_ viewController: MKLookAroundViewController) {
            // フルスクリーン終了後
        }
    }
}
```

### MKLookAroundViewControllerDelegate

```swift
protocol MKLookAroundViewControllerDelegate {
    // シーン更新
    func lookAroundViewControllerWillUpdateScene(_ viewController: MKLookAroundViewController)
    func lookAroundViewControllerDidUpdateScene(_ viewController: MKLookAroundViewController)

    // フルスクリーン
    func lookAroundViewControllerWillDismissFullScreen(_ viewController: MKLookAroundViewController)
    func lookAroundViewControllerDidDismissFullScreen(_ viewController: MKLookAroundViewController)
}
```

## 実装パターン

### 地図とLook Aroundの連携

```swift
struct MapWithLookAround: View {
    @State private var position: MapCameraPosition = .automatic
    @State private var selectedCoordinate: CLLocationCoordinate2D?
    @State private var lookAroundScene: MKLookAroundScene?
    @State private var showLookAround = false

    let places: [Place]

    var body: some View {
        VStack(spacing: 0) {
            // 地図
            Map(position: $position) {
                ForEach(places) { place in
                    Marker(place.name, coordinate: place.coordinate)
                }
            }
            .onTapGesture { location in
                // タップ位置を座標に変換（実装は簡略化）
            }

            // Look Aroundプレビュー
            if showLookAround, let scene = lookAroundScene {
                LookAroundPreview(scene: scene)
                    .frame(height: 200)
                    .overlay(alignment: .topTrailing) {
                        Button {
                            showLookAround = false
                        } label: {
                            Image(systemName: "xmark.circle.fill")
                                .font(.title2)
                                .foregroundStyle(.white)
                                .padding(8)
                        }
                    }
            }
        }
    }

    private func loadLookAround(for coordinate: CLLocationCoordinate2D) async {
        let request = MKLookAroundSceneRequest(coordinate: coordinate)

        do {
            lookAroundScene = try await request.scene
            showLookAround = true
        } catch {
            showLookAround = false
        }
    }
}
```

### マーカー選択時にLook Around表示

```swift
struct PlaceDetailView: View {
    let place: Place
    @State private var lookAroundScene: MKLookAroundScene?

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                // 場所情報
                Text(place.name)
                    .font(.title)

                Text(place.address)
                    .foregroundStyle(.secondary)

                // Look Aroundプレビュー
                if let scene = lookAroundScene {
                    VStack(alignment: .leading) {
                        Text("Look Around")
                            .font(.headline)

                        LookAroundPreview(scene: scene)
                            .frame(height: 200)
                            .clipShape(RoundedRectangle(cornerRadius: 12))
                    }
                }

                // 地図
                Map {
                    Marker(place.name, coordinate: place.coordinate)
                }
                .frame(height: 200)
                .clipShape(RoundedRectangle(cornerRadius: 12))
            }
            .padding()
        }
        .task {
            await loadLookAroundScene()
        }
    }

    private func loadLookAroundScene() async {
        let request = MKLookAroundSceneRequest(coordinate: place.coordinate)
        lookAroundScene = try? await request.scene
    }
}
```

### 可用性の事前チェック

```swift
@MainActor
@Observable
final class LookAroundManager {
    var isAvailable = false
    var scene: MKLookAroundScene?
    var isLoading = false
    var error: Error?

    func checkAvailability(for coordinate: CLLocationCoordinate2D) async {
        isLoading = true
        defer { isLoading = false }

        let request = MKLookAroundSceneRequest(coordinate: coordinate)

        do {
            scene = try await request.scene
            isAvailable = true
            error = nil
        } catch let lookAroundError {
            scene = nil
            isAvailable = false
            error = lookAroundError
        }
    }
}
```

## エラーハンドリング

### 主なエラーケース

```swift
func handleLookAroundError(_ error: Error) -> String {
    if let mkError = error as? MKError {
        switch mkError.code {
        case .unknown:
            return "不明なエラーが発生しました"
        case .serverFailure:
            return "サーバーに接続できません"
        case .loadingThrottled:
            return "リクエスト制限に達しました"
        default:
            return "Look Aroundを読み込めません"
        }
    }

    return "この場所ではLook Aroundを利用できません"
}
```

### フォールバックUI

```swift
struct LookAroundWithFallback: View {
    let coordinate: CLLocationCoordinate2D
    @State private var scene: MKLookAroundScene?
    @State private var loadState: LoadState = .loading

    enum LoadState {
        case loading
        case available
        case unavailable
    }

    var body: some View {
        Group {
            switch loadState {
            case .loading:
                ProgressView("Look Aroundを読み込み中...")

            case .available:
                if let scene {
                    LookAroundPreview(scene: scene)
                }

            case .unavailable:
                // フォールバック: 衛星写真を表示
                Map(initialPosition: .camera(MapCamera(
                    centerCoordinate: coordinate,
                    distance: 200,
                    heading: 0,
                    pitch: 60
                )))
                .mapStyle(.imagery(elevation: .realistic))
                .overlay(alignment: .bottom) {
                    Text("Look Aroundは利用できません")
                        .font(.caption)
                        .padding(8)
                        .background(.regularMaterial)
                        .clipShape(Capsule())
                        .padding()
                }
            }
        }
        .task {
            await loadScene()
        }
    }

    private func loadScene() async {
        loadState = .loading

        let request = MKLookAroundSceneRequest(coordinate: coordinate)

        do {
            scene = try await request.scene
            loadState = .available
        } catch {
            loadState = .unavailable
        }
    }
}
```

## キャッシュ

```swift
actor LookAroundCache {
    private var cache: [String: MKLookAroundScene] = [:]
    private var unavailableLocations: Set<String> = []

    func scene(for coordinate: CLLocationCoordinate2D) async -> MKLookAroundScene? {
        let key = "\(coordinate.latitude),\(coordinate.longitude)"

        // 利用不可な場所はスキップ
        if unavailableLocations.contains(key) {
            return nil
        }

        // キャッシュから取得
        if let cached = cache[key] {
            return cached
        }

        // 新規取得
        let request = MKLookAroundSceneRequest(coordinate: coordinate)

        do {
            let scene = try await request.scene
            cache[key] = scene
            return scene
        } catch {
            unavailableLocations.insert(key)
            return nil
        }
    }

    func clearCache() {
        cache.removeAll()
        unavailableLocations.removeAll()
    }
}
```

## ベストプラクティス

### 遅延読み込み

```swift
// ユーザーが詳細を見る時にのみ読み込む
struct PlaceRow: View {
    let place: Place
    @State private var showDetail = false

    var body: some View {
        Button {
            showDetail = true
        } label: {
            Text(place.name)
        }
        .sheet(isPresented: $showDetail) {
            PlaceDetailView(place: place)  // ここでLook Aroundを読み込む
        }
    }
}
```

### バッチチェック

```swift
func checkLookAroundAvailability(for places: [Place]) async -> [Place: Bool] {
    var results: [Place: Bool] = [:]

    await withTaskGroup(of: (Place, Bool).self) { group in
        for place in places {
            group.addTask {
                let request = MKLookAroundSceneRequest(coordinate: place.coordinate)
                let available = (try? await request.scene) != nil
                return (place, available)
            }
        }

        for await (place, available) in group {
            results[place] = available
        }
    }

    return results
}
```

### ユーザーへのフィードバック

```swift
struct LookAroundButton: View {
    let coordinate: CLLocationCoordinate2D
    @State private var isAvailable: Bool?
    @State private var showLookAround = false
    @State private var scene: MKLookAroundScene?

    var body: some View {
        Button {
            if let scene {
                showLookAround = true
            }
        } label: {
            HStack {
                Image(systemName: "binoculars")
                Text("Look Around")
            }
        }
        .disabled(isAvailable != true)
        .opacity(isAvailable == true ? 1 : 0.5)
        .task {
            let request = MKLookAroundSceneRequest(coordinate: coordinate)
            scene = try? await request.scene
            isAvailable = scene != nil
        }
        .sheet(isPresented: $showLookAround) {
            if let scene {
                LookAroundPreview(scene: scene)
            }
        }
    }
}
```
