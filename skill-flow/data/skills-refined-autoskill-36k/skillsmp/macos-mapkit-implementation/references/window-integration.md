# ウィンドウ管理統合

macOSのウィンドウ管理とMapKitの統合ガイド。

## SwiftUI Window管理

### 基本的なウィンドウ

```swift
@main
struct MapApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

struct ContentView: View {
    var body: some View {
        Map(position: .constant(.automatic))
    }
}
```

### ウィンドウサイズ制限

```swift
WindowGroup {
    MapView()
}
.defaultSize(width: 800, height: 600)
.windowResizability(.contentMinSize)
```

### 複数ウィンドウ

```swift
@main
struct MapApp: App {
    var body: some Scene {
        // メインウィンドウ
        WindowGroup {
            MainMapView()
        }

        // セカンダリウィンドウ
        Window("場所の詳細", id: "place-detail") {
            PlaceDetailView()
        }
    }
}
```

## NavigationSplitView

macOS向け3カラムレイアウト。

```swift
struct MapSplitView: View {
    @State private var selectedPlace: Place?
    @State private var selectedDetail: PlaceDetail?

    var body: some View {
        NavigationSplitView {
            // サイドバー: 場所リスト
            PlaceListView(selection: $selectedPlace)
        } content: {
            // コンテンツ: 地図
            if let place = selectedPlace {
                MapContentView(place: place, selection: $selectedDetail)
            } else {
                ContentUnavailableView("場所を選択", systemImage: "map")
            }
        } detail: {
            // 詳細: 選択した詳細情報
            if let detail = selectedDetail {
                PlaceDetailView(detail: detail)
            } else {
                ContentUnavailableView("詳細を選択", systemImage: "info.circle")
            }
        }
    }
}
```

## ツールバー統合

### 基本ツールバー

```swift
struct MapToolbarView: View {
    @State private var position: MapCameraPosition = .automatic
    @State private var mapStyle: MapStyle = .standard

    var body: some View {
        Map(position: $position)
            .mapStyle(mapStyle)
            .toolbar {
                ToolbarItemGroup(placement: .primaryAction) {
                    Button {
                        // 現在地に移動
                        position = .userLocation(fallback: .automatic)
                    } label: {
                        Image(systemName: "location")
                    }

                    Picker("スタイル", selection: $mapStyle) {
                        Text("標準").tag(MapStyle.standard)
                        Text("衛星").tag(MapStyle.imagery)
                        Text("ハイブリッド").tag(MapStyle.hybrid)
                    }
                    .pickerStyle(.segmented)
                }

                ToolbarItem(placement: .secondaryAction) {
                    Button {
                        // 検索
                    } label: {
                        Image(systemName: "magnifyingglass")
                    }
                }
            }
    }
}
```

### カスタムツールバー

```swift
.toolbar {
    ToolbarItem(placement: .navigation) {
        Button(action: goBack) {
            Image(systemName: "chevron.left")
        }
    }

    ToolbarItem(placement: .principal) {
        Text("地図")
            .font(.headline)
    }

    ToolbarItemGroup(placement: .primaryAction) {
        // アクションボタン
    }
}
```

## フルスクリーン対応

```swift
struct FullScreenMapView: View {
    @State private var position: MapCameraPosition = .automatic
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        Map(position: $position)
            .ignoresSafeArea()
            .overlay(alignment: .topTrailing) {
                Button {
                    dismiss()
                } label: {
                    Image(systemName: "xmark.circle.fill")
                        .font(.title)
                }
                .padding()
            }
    }
}
```

### プログラマティックフルスクリーン

```swift
// NSWindowを使用
if let window = NSApplication.shared.keyWindow {
    window.toggleFullScreen(nil)
}
```

## シート・ポップオーバー

### シート

```swift
struct MapWithSheetView: View {
    @State private var position: MapCameraPosition = .automatic
    @State private var showingDetail = false
    @State private var selectedItem: MKMapItem?

    var body: some View {
        Map(position: $position, selection: $selectedItem)
            .onChange(of: selectedItem) { _, newItem in
                showingDetail = newItem != nil
            }
            .sheet(isPresented: $showingDetail) {
                if let item = selectedItem {
                    PlaceDetailSheet(item: item)
                        .frame(minWidth: 400, minHeight: 300)
                }
            }
    }
}
```

### ポップオーバー

```swift
struct MapWithPopoverView: View {
    @State private var showingPopover = false
    @State private var popoverAnchor: CGPoint = .zero

    var body: some View {
        Map(position: $position)
            .popover(isPresented: $showingPopover, arrowEdge: .bottom) {
                PlacePopover()
                    .frame(width: 300, height: 200)
            }
    }
}
```

## Inspector（サイドパネル）

```swift
struct MapWithInspectorView: View {
    @State private var position: MapCameraPosition = .automatic
    @State private var showingInspector = true
    @State private var selectedItem: MKMapItem?

    var body: some View {
        Map(position: $position, selection: $selectedItem)
            .inspector(isPresented: $showingInspector) {
                if let item = selectedItem {
                    PlaceInspector(item: item)
                } else {
                    Text("場所を選択してください")
                        .foregroundStyle(.secondary)
                }
            }
            .toolbar {
                ToolbarItem {
                    Button {
                        showingInspector.toggle()
                    } label: {
                        Image(systemName: "sidebar.right")
                    }
                }
            }
    }
}
```

## メニューコマンド

```swift
@main
struct MapApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .commands {
            CommandGroup(replacing: .newItem) {
                Button("新しい地図ウィンドウ") {
                    // 新しいウィンドウを開く
                }
                .keyboardShortcut("n", modifiers: .command)
            }

            CommandMenu("地図") {
                Button("現在地に移動") {
                    // 現在地に移動
                }
                .keyboardShortcut("l", modifiers: .command)

                Divider()

                Button("標準") {
                    // 標準スタイル
                }
                Button("衛星") {
                    // 衛星スタイル
                }
                Button("ハイブリッド") {
                    // ハイブリッドスタイル
                }
            }
        }
    }
}
```

## 設定ウィンドウ

```swift
@main
struct MapApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }

        Settings {
            MapSettingsView()
        }
    }
}

struct MapSettingsView: View {
    @AppStorage("defaultMapStyle") private var defaultMapStyle = "standard"
    @AppStorage("showTraffic") private var showTraffic = false

    var body: some View {
        Form {
            Picker("デフォルトスタイル", selection: $defaultMapStyle) {
                Text("標準").tag("standard")
                Text("衛星").tag("imagery")
                Text("ハイブリッド").tag("hybrid")
            }

            Toggle("交通情報を表示", isOn: $showTraffic)
        }
        .formStyle(.grouped)
        .frame(width: 400)
        .padding()
    }
}
```

## AppKit NSWindow連携

### NSWindowControllerとの統合

```swift
class MapWindowController: NSWindowController {
    convenience init() {
        let window = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: 800, height: 600),
            styleMask: [.titled, .closable, .resizable, .miniaturizable],
            backing: .buffered,
            defer: false
        )

        window.title = "地図"
        window.contentView = NSHostingView(rootView: MapContentView())

        self.init(window: window)
    }
}
```

### ウィンドウ状態の監視

```swift
NotificationCenter.default.addObserver(
    forName: NSWindow.didBecomeKeyNotification,
    object: nil,
    queue: .main
) { notification in
    // ウィンドウがアクティブになった
}

NotificationCenter.default.addObserver(
    forName: NSWindow.didResizeNotification,
    object: nil,
    queue: .main
) { notification in
    // ウィンドウがリサイズされた
}
```

## ドラッグ＆ドロップ

```swift
struct MapWithDropView: View {
    @State private var position: MapCameraPosition = .automatic
    @State private var droppedItems: [DroppedLocation] = []

    var body: some View {
        Map(position: $position) {
            ForEach(droppedItems) { item in
                Marker(item.name, coordinate: item.coordinate)
            }
        }
        .dropDestination(for: String.self) { items, location in
            // ドロップされた住所をジオコーディング
            for address in items {
                Task {
                    if let coordinate = await geocode(address: address) {
                        droppedItems.append(DroppedLocation(
                            name: address,
                            coordinate: coordinate
                        ))
                    }
                }
            }
            return true
        }
    }
}
```
