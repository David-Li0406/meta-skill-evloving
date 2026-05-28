# Navigation Patterns / ナビゲーションパターン

Tesla Dashboard UIの画面遷移とナビゲーションパターンについて解説します。

## Overview / 概要

タブベース + モーダル + 分割ビューを組み合わせたナビゲーションシステムです。

## Tab Navigation / タブナビゲーション

### TeslaMenuTab

```swift
enum TeslaMenuTab: String, CaseIterable, Identifiable {
    case navigation = "navigation"
    case media = "media"
    case climate = "climate"
    case vehicle = "vehicle"
    case settings = "settings"

    var id: String { rawValue }

    var label: String {
        switch self {
        case .navigation: return "ナビ"
        case .media: return "メディア"
        case .climate: return "空調"
        case .vehicle: return "車両"
        case .settings: return "設定"
        }
    }

    var iconName: String {
        switch self {
        case .navigation: return "location.fill"
        case .media: return "music.note"
        case .climate: return "thermometer.medium"
        case .vehicle: return "car.fill"
        case .settings: return "gearshape.fill"
        }
    }
}
```

### 実装

```swift
struct TeslaMainDashboard: View {
    @State private var selectedTab: TeslaMenuTab = .navigation

    var body: some View {
        VStack(spacing: 0) {
            // Content
            switch selectedTab {
            case .navigation:
                TeslaNavigationScreen(...)
            case .media:
                TeslaMediaScreen(...)
            case .climate:
                TeslaClimateScreen(...)
            case .vehicle:
                TeslaVehicleScreen(...)
            case .settings:
                TeslaSettingsScreen()
            }

            // Tab Bar
            TeslaTouchscreenMenu(selectedTab: $selectedTab)
        }
    }
}
```

## Layout Modes / レイアウトモード

### TeslaLayoutMode

```swift
enum TeslaLayoutMode: String, CaseIterable {
    case fullscreen = "fullscreen"
    case split = "split"
    case compact = "compact"

    var displayName: String {
        switch self {
        case .fullscreen: return "全画面"
        case .split: return "分割"
        case .compact: return "コンパクト"
        }
    }

    var icon: String {
        switch self {
        case .fullscreen: return "arrow.up.left.and.arrow.down.right"
        case .split: return "rectangle.split.2x1"
        case .compact: return "rectangle.compress.vertical"
        }
    }
}
```

### 切り替え実装

```swift
struct TeslaNavigationScreen: View {
    @Binding var layoutMode: TeslaLayoutMode

    var body: some View {
        TeslaNavigationSplitLayout(
            mapContent: { TeslaMapView(...) },
            controlContent: { navigationControls },
            layoutMode: $layoutMode
        )
    }
}
```

## Modal Presentation / モーダル表示

### Sheet

```swift
struct TeslaMainDashboard: View {
    @State private var showMusicExpanded = false

    var body: some View {
        VStack {
            // Content
        }
        .sheet(isPresented: $showMusicExpanded) {
            TeslaExpandedMusicView(...)
                .presentationDetents([.medium, .large])
                .presentationDragIndicator(.visible)
        }
    }
}
```

### Full Screen Cover

```swift
.fullScreenCover(isPresented: $showFullScreenMap) {
    TeslaFullScreenMapView(...)
}
```

### Detents（iOS 16+）

```swift
.sheet(isPresented: $showSearch) {
    NavigationSearchSheet(...)
        .presentationDetents([.medium, .large])
        .presentationBackgroundInteraction(.enabled)
}
```

## Split View Navigation / 分割ビューナビゲーション

### TeslaSplitViewLayout

```swift
struct TeslaSplitViewLayout<Primary: View, Secondary: View>: View {
    let primary: Primary
    let secondary: Secondary
    var splitRatio: CGFloat = 0.6
    var orientation: SplitOrientation = .horizontal

    var body: some View {
        GeometryReader { geometry in
            if orientation == .horizontal {
                HStack(spacing: 0) {
                    primary.frame(width: geometry.size.width * splitRatio)
                    secondary
                }
            } else {
                VStack(spacing: 0) {
                    primary.frame(height: geometry.size.height * splitRatio)
                    secondary
                }
            }
        }
    }
}
```

### 使用例

```swift
TeslaSplitViewLayout(
    splitRatio: 0.65,
    primary: {
        TeslaMapView(...)
    },
    secondary: {
        ScrollView {
            VStack {
                searchBar
                quickDestinations
                navigationInfo
            }
        }
    }
)
```

## Drill-Down Navigation / ドリルダウンナビゲーション

### NavigationStack（iOS 16+）

```swift
struct TeslaSettingsScreen: View {
    @State private var navigationPath = NavigationPath()

    var body: some View {
        NavigationStack(path: $navigationPath) {
            List {
                NavigationLink("表示設定", value: SettingsDestination.display)
                NavigationLink("ナビゲーション", value: SettingsDestination.navigation)
                NavigationLink("通知", value: SettingsDestination.notifications)
            }
            .navigationDestination(for: SettingsDestination.self) { destination in
                switch destination {
                case .display:
                    DisplaySettingsView()
                case .navigation:
                    NavigationSettingsView()
                case .notifications:
                    NotificationSettingsView()
                }
            }
        }
    }
}

enum SettingsDestination: Hashable {
    case display
    case navigation
    case notifications
}
```

## Programmatic Navigation / プログラム的ナビゲーション

### タブ切り替え

```swift
class NavigationCoordinator: ObservableObject {
    @Published var selectedTab: TeslaMenuTab = .navigation

    func navigateToClimate() {
        selectedTab = .climate
    }

    func navigateToCharging() {
        selectedTab = .vehicle
        // さらにセクションを選択
    }
}
```

### ディープリンク

```swift
struct TeslaMainDashboard: View {
    @StateObject private var coordinator = NavigationCoordinator()

    var body: some View {
        VStack { /* content */ }
            .onOpenURL { url in
                handleDeepLink(url)
            }
    }

    func handleDeepLink(_ url: URL) {
        guard let components = URLComponents(url: url, resolvingAgainstBaseURL: true) else { return }

        switch components.host {
        case "navigation":
            coordinator.selectedTab = .navigation
        case "climate":
            coordinator.selectedTab = .climate
        case "charging":
            coordinator.selectedTab = .vehicle
        default:
            break
        }
    }
}
```

## Transition Animations / 遷移アニメーション

### カスタムトランジション

```swift
extension AnyTransition {
    static var teslaSlide: AnyTransition {
        .asymmetric(
            insertion: .move(edge: .trailing).combined(with: .opacity),
            removal: .move(edge: .leading).combined(with: .opacity)
        )
    }

    static var teslaScale: AnyTransition {
        .scale(scale: 0.9).combined(with: .opacity)
    }
}
```

### 使用例

```swift
if showDetail {
    DetailView()
        .transition(.teslaSlide)
}
```

## State Preservation / 状態保存

### SceneStorage

```swift
struct TeslaMainDashboard: View {
    @SceneStorage("selectedTab") private var selectedTab: String = "navigation"
    @SceneStorage("layoutMode") private var layoutMode: String = "split"

    var body: some View {
        // ...
    }
}
```

### AppStorage

```swift
struct TeslaSettingsScreen: View {
    @AppStorage("lastViewedTab") private var lastViewedTab: String = "navigation"

    var body: some View {
        // ...
    }
}
```

## iPad Specific / iPad固有

### サイドバー

```swift
struct TeslaSideMenu: View {
    @Binding var selectedTab: TeslaMenuTab

    var body: some View {
        VStack(spacing: 8) {
            ForEach(TeslaMenuTab.allCases) { tab in
                sideMenuButton(for: tab)
            }
            Spacer()
        }
        .frame(width: 80)
        .background(TeslaColors.surface)
    }
}
```

### マルチウィンドウ

```swift
@main
struct TeslaDashboardApp: App {
    var body: some Scene {
        WindowGroup {
            TeslaMainDashboard()
        }

        WindowGroup(id: "map", for: UUID.self) { $id in
            TeslaFullScreenMapView()
        }
    }
}

// 新しいウィンドウを開く
@Environment(\.openWindow) private var openWindow

Button("地図を別ウィンドウで開く") {
    openWindow(id: "map", value: UUID())
}
```

## Best Practices / ベストプラクティス

### 1. 状態の一元管理

```swift
// ✅ Good: Coordinatorで管理
class NavigationCoordinator: ObservableObject {
    @Published var selectedTab: TeslaMenuTab = .navigation
    @Published var layoutMode: TeslaLayoutMode = .split
}

// ❌ Bad: 各Viewでバラバラに管理
```

### 2. アニメーションの統一

```swift
// ✅ Good: TeslaAnimationを使用
withAnimation(TeslaAnimation.standard) {
    selectedTab = .climate
}
```

### 3. アクセシビリティ対応

```swift
TeslaTouchscreenMenu(selectedTab: $selectedTab)
    .accessibilityLabel("メインメニュー")
    .accessibilityHint("タブを選択して画面を切り替え")
```

## Related Documents / 関連ドキュメント

- [Atomic Design Patterns](./atomic-design-patterns.md)
- [Animation Guidelines](./animation-guidelines.md)
- [Accessibility Guide](./accessibility-guide.md)
