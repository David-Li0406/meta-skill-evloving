# Atomic Design Patterns / アトミックデザインパターン

Tesla Dashboard UIのコンポーネント構造とアトミックデザイン原則について解説します。

## Overview / 概要

このスキルはアトミックデザインの原則に基づいて構築されています。

```
Atoms → Molecules → Organisms → Templates → Pages
```

## Hierarchy / 階層構造

### 1. Atoms（原子）

最小単位のUIコンポーネント。他のコンポーネントに依存しません。

| ファイル | 説明 |
|---------|------|
| `tesla-colors.swift` | カラーパレット定義 |
| `tesla-typography.swift` | タイポグラフィ定義 |
| `tesla-icons.swift` | アイコン定義 |
| `tesla-animation.swift` | アニメーション定義 |

**特徴:**
- 単一責任
- 再利用可能
- 状態を持たない（または最小限）

```swift
// Atom の例: TeslaColors
enum TeslaColors {
    static let accent = Color(hex: "#3399FF")
    static let background = Color(hex: "#141416")
}
```

### 2. Molecules（分子）

Atomsを組み合わせた小さなUIコンポーネント。

| ファイル | 説明 |
|---------|------|
| `tesla-icon-button.swift` | アイコン + ラベル |
| `tesla-slider.swift` | トラック + サム + 値表示 |
| `tesla-toggle.swift` | スイッチ + ラベル |
| `tesla-brightness-control.swift` | スライダー + アイコン |

**特徴:**
- 2〜3個のAtomsで構成
- 単一の明確な機能
- 基本的なインタラクション

```swift
// Molecule の例: TeslaIconButton
struct TeslaIconButton: View {
    let icon: TeslaIcon        // Atom
    let label: String          // Atom (Text)
    // ...Colors, Typography   // Atoms
}
```

### 3. Organisms（有機体）

Moleculesを組み合わせた複雑なUIコンポーネント。

| ファイル | 説明 |
|---------|------|
| `tesla-navigation-bar.swift` | 時刻 + ステータス + バッテリー |
| `tesla-vehicle-status.swift` | 速度 + 航続距離 + バッテリーバー + ドア状態 |
| `tesla-quick-actions-toolbar.swift` | 複数のアイコンボタン + ドライブモード |
| `tesla-music-bar.swift` | アートワーク + トラック情報 + コントロール |
| `tesla-climate-control.swift` | 温度 + ファン + シートヒーター |
| `tesla-touchscreen-menu.swift` | タブボタン群 |
| `tesla-map-view.swift` | 地図 + マーカー + ルート + 指示 |

**特徴:**
- 機能的に完結
- 複数のMoleculesで構成
- データバインディング

```swift
// Organism の例: TeslaVehicleStatus
struct TeslaVehicleStatus: View {
    let vehicleData: VehicleData  // モデル

    var body: some View {
        VStack {
            speedAndRangeSection  // Molecules
            batterySection        // Molecules
            doorStatusSection     // Molecules
        }
    }
}
```

### 4. Templates（テンプレート）

ページのレイアウト構造を定義。

| ファイル | 説明 |
|---------|------|
| `tesla-dashboard-layout.swift` | サイドバー + メインコンテンツ |
| `tesla-split-view-layout.swift` | 2ペイン分割レイアウト |
| `tesla-theme-provider.swift` | テーマコンテキスト提供 |

**特徴:**
- コンテンツに依存しない
- レイアウトの骨組みのみ
- 汎用的

```swift
// Template の例: TeslaDashboardLayout
struct TeslaDashboardLayout<Content: View, Sidebar: View>: View {
    let content: Content    // ジェネリック
    let sidebar: Sidebar?   // ジェネリック
    var sidebarWidth: CGFloat = 320
    // レイアウト構造のみ定義
}
```

### 5. Pages（ページ）

実際のデータを流し込んだ完成画面。

| ファイル | 説明 |
|---------|------|
| `tesla-main-dashboard.swift` | メインダッシュボード |
| `tesla-navigation-screen.swift` | ナビゲーション画面 |
| `tesla-media-screen.swift` | メディア画面 |
| `tesla-climate-screen.swift` | 空調画面 |
| `tesla-vehicle-screen.swift` | 車両情報画面 |

**特徴:**
- 完全な機能を持つ画面
- データソースと接続
- ユーザーフローを実装

```swift
// Page の例: TeslaMainDashboard
struct TeslaMainDashboard: View {
    @StateObject private var vehicleProvider = MockVehicleDataProvider()
    @StateObject private var musicPlayer = TeslaMusicPlayer()
    @State private var selectedTab: TeslaMenuTab = .navigation

    var body: some View {
        VStack {
            TeslaNavigationBar(...)     // Organism
            mainContent                  // Template + Organisms
            TeslaMusicBar(...)          // Organism
            TeslaTouchscreenMenu(...)   // Organism
        }
    }
}
```

## Design Principles / 設計原則

### 1. 単一責任原則

各コンポーネントは1つの責任のみを持ちます。

```swift
// ✅ Good
struct TeslaBatteryBar: View { /* バッテリー表示のみ */ }
struct TeslaDoorDiagram: View { /* ドア状態表示のみ */ }

// ❌ Bad
struct TeslaVehicleInfoAndControls: View { /* 複数の責任 */ }
```

### 2. 疎結合

コンポーネント間の依存を最小限に。

```swift
// ✅ Good: プロトコルで抽象化
protocol VehicleDataProvider { ... }

struct TeslaVehicleStatus: View {
    let vehicleData: VehicleData  // データのみ依存
}

// ❌ Bad: 具体的なクラスに依存
struct TeslaVehicleStatus: View {
    @ObservedObject var provider: TeslaAPIClient  // 実装に依存
}
```

### 3. 合成優先

継承より合成を優先します。

```swift
// ✅ Good: 合成
struct TeslaQuickActionsToolbar: View {
    var body: some View {
        VStack {
            driveModeSelector  // 別のView
            quickActionsGrid   // 別のView
        }
    }
}

// ❌ Bad: 継承（SwiftUIでは不可能）
class TeslaQuickActionsToolbar: TeslaToolbar { }
```

## File Organization / ファイル構成

```
examples/
├── atoms/          # 最小単位
├── molecules/      # 小さなコンポーネント
├── organisms/      # 複雑なコンポーネント
├── templates/      # レイアウト
├── pages/          # 完成画面
└── models/         # データモデル
```

## Best Practices / ベストプラクティス

### 1. 命名規則

```swift
// Prefix: Tesla
TeslaColors, TeslaIconButton, TeslaVehicleStatus

// 機能を明確に
TeslaBrightnessControl  // ✅ 何をするか明確
TeslaControl            // ❌ 曖昧
```

### 2. プレビュー

各コンポーネントに`#Preview`を提供：

```swift
#Preview("Tesla Icon Button") {
    TeslaIconButton(...)
}
```

### 3. ドキュメントコメント

```swift
/// Tesla風アイコンボタン
/// ガラスモーフィズム効果と押下時のスケールアニメーション付き
struct TeslaIconButton: View {
    /// 表示するアイコン
    let icon: TeslaIcon
    /// ラベルテキスト
    let label: String
    // ...
}
```

## Related Documents / 関連ドキュメント

- [Design System](./design-system.md)
- [Theme Configuration](./theme-configuration.md)
- [Animation Guidelines](./animation-guidelines.md)
