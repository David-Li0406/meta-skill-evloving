---
name: tesla-dashboard-ui
description: |
  This skill should be used when the user asks to "create Tesla-style dashboard",
  "implement car dashboard UI", "add vehicle status display", "create dark modern UI",
  "implement touchscreen interface", "build automotive dashboard", "add navigation map UI",
  "create media player controls", "implement climate control UI", "add EV battery display",
  "create glassmorphism UI", "implement SwiftData persistence", "add remote command support",
  "Tesla風ダッシュボードを作成", "車載ダッシュボードUI", "ダークモダンUI",
  "タッチスクリーンインターフェース", "車両ステータス表示", "ナビゲーションマップUI",
  "メディアプレーヤーコントロール", "空調コントロールUI", "EVバッテリー表示",
  "ガラスモーフィズムUI", "SwiftData永続化", "リモートコマンド対応",
  or needs guidance on Tesla-inspired dashboard interfaces with atomic design principles,
  dark theme, custom controls, MapKit navigation, AVFoundation media playback,
  SwiftData persistence, and automotive UI patterns for iPad applications targeting iOS 17+.
version: 1.0.0
---

# Tesla Dashboard UI

iOS 17+ iPad向けSwiftUIアプリケーションにおける、Tesla風ダッシュボードUIコンポーネントライブラリの実装ガイド。

## Overview

**Target Platform**: iPad専用 / iOS 17+ / Swift 5.9+

**Design Principles**:
- アトミックデザイン原則（Atoms → Molecules → Organisms → Templates → Pages）
- Teslaデザイン言語（ダークテーマ、ガラスモーフィズム、クリーンなタイポグラフィ）
- 高コントラスト・高視認性（車載ダッシュボード向け）
- 完全アクセシビリティ対応（VoiceOver, Dynamic Type, Reduce Motion）

**Core Features**:
- カスタムテーマシステム（@Observable + Environment）
- SF Symbols + カスタムSVGアイコン
- SwiftData永続化（設定・お気に入り・走行履歴・エネルギー統計）
- MapKit完全統合（ルート検索・LookAround・音声案内）
- AVFoundation音楽再生（MPRemoteCommandCenter対応）
- KeyframeAnimator/PhaseAnimatorによる高度なアニメーション

## Quick Start Checklist

Tesla Dashboard UIを実装する際の必須手順：

1. **テーマプロバイダー設定**
   ```swift
   @main
   struct MyApp: App {
       @State private var theme = TeslaTheme()

       var body: some Scene {
           WindowGroup {
               TeslaMainDashboard()
                   .environment(\.teslaTheme, theme)
                   .preferredColorScheme(.dark)
           }
           .modelContainer(for: [
               TeslaSettings.self,
               TeslaFavoriteLocation.self,
               TeslaTripHistory.self,
               TeslaEnergyStats.self
           ])
       }
   }
   ```

2. **Info.plist設定**
   - `NSLocationWhenInUseUsageDescription` - 位置情報アクセス理由
   - `NSLocationAlwaysAndWhenInUseUsageDescription` - 常時位置情報（必要な場合）
   - `UIBackgroundModes` - `audio` (音楽再生用)

3. **フレームワークインポート**
   ```swift
   import SwiftUI
   import SwiftData
   import MapKit
   import CoreLocation
   import AVFoundation
   import MediaPlayer
   ```

## Component Hierarchy

### Atoms（原子）- 最小UI単位
- **TeslaColors** - ダークテーマカラーパレット（blur 30, opacity 0.16）
- **TeslaTypography** - Tesla風タイポグラフィ（Display 57pt〜）
- **TeslaIcons** - SF Symbols + カスタムアイコン
- **TeslaAnimation** - KeyframeAnimator/PhaseAnimatorカーブ

### Molecules（分子）- 機能的UI部品
- **TeslaIconButton** - ガラスモーフィズムアイコンボタン
- **TeslaSlider** - アクセシビリティ対応カスタムスライダー
- **TeslaToggle** - トグルスイッチ
- **TeslaBrightnessControl** - 明るさ調整コントロール

### Organisms（生物）- 複合コンポーネント
- **TeslaNavigationBar** - ナビゲーションバー
- **TeslaVehicleStatus** - 完全車両データビュー（速度/バッテリー/航続距離）
- **TeslaQuickActionsToolbar** - 9項目クイックアクション + ドライブモード
- **TeslaMusicBar** - AVFoundation + MPRemoteCommandCenter統合
- **TeslaClimateControl** - スライダーベース空調（プリコンディショニング対応）
- **TeslaTouchscreenMenu** - 5タブメニュー
- **TeslaMapView** - MapKit + AVSpeechSynthesizer音声案内

### Models（モデル）- データ層
- **TeslaError** - Result<T, TeslaError>用エラー定義
- **VehicleDataProvider** - 車両データprotocol
- **TeslaVehicleData** - @Model 車両データ
- **TeslaSettings** - @Model 設定データ
- **TeslaFavoriteLocation** - @Model お気に入り地点
- **TeslaTripHistory** - @Model 走行履歴
- **TeslaEnergyStats** - @Model エネルギー統計

### Templates（テンプレート）- レイアウト構造
- **TeslaDashboardLayout** - iPad向けダッシュボードレイアウト
- **TeslaSplitViewLayout** - 分割ビューレイアウト
- **TeslaThemeProvider** - @Observableテーマプロバイダー

### Pages（ページ）- 完成画面
- **TeslaMainDashboard** - メインダッシュボード
- **TeslaNavigationScreen** - モード切り替えナビゲーション
- **TeslaMediaScreen** - メディア再生画面
- **TeslaClimateScreen** - 空調設定画面
- **TeslaVehicleScreen** - 車両情報画面

## Color Palette

| 用途 | 変数名 | HEX | 説明 |
|------|--------|-----|------|
| Background | `background` | #141416 | メイン背景色 |
| Surface | `surface` | #1E1E22 | カード・パネル背景 |
| Surface Elevated | `surfaceElevated` | #28282C | 浮き上がった要素 |
| Accent | `accent` | #3399FF | Tesla Blue（主要アクション） |
| Status Green | `statusGreen` | #4DD966 | 正常・充電完了 |
| Status Orange | `statusOrange` | #FF9933 | 注意・後進 |
| Status Red | `statusRed` | #F24D4D | エラー・緊急 |
| Text Primary | `textPrimary` | #FFFFFF | メインテキスト |
| Text Secondary | `textSecondary` | #B3B3B3 | サブテキスト |
| Glass Background | `glassBackground` | #FFFFFF14 | ガラスモーフィズム背景 |

## Typography Scale

| スタイル | サイズ | ウェイト | 用途 |
|----------|--------|----------|------|
| Display Large | 57pt | Regular | 速度表示 |
| Display Medium | 45pt | Regular | バッテリー残量 |
| Display Small | 36pt | Regular | 航続距離 |
| Headline Large | 32pt | Semibold | セクション見出し |
| Headline Medium | 28pt | Semibold | カードタイトル |
| Title Large | 22pt | Medium | サブセクション |
| Title Medium | 18pt | Medium | リスト項目 |
| Body Large | 16pt | Regular | 本文 |
| Body Medium | 14pt | Regular | 説明文 |
| Label Large | 14pt | Medium | ボタンラベル |
| Label Small | 10pt | Medium | 補助テキスト |

## Glassmorphism Effect

強いガラスモーフィズム効果を使用：

```swift
.background(.ultraThinMaterial)
.background(TeslaColors.glassBackground)
.blur(radius: 30)
```

または Material を使用：

```swift
.background(.ultraThinMaterial)
```

## Error Handling

Result型ベースのエラーハンドリング：

```swift
enum TeslaError: Error, LocalizedError {
    case locationPermissionDenied
    case routeNotFound
    case audioSessionFailed
    case dataNotFound

    var errorDescription: String? {
        switch self {
        case .locationPermissionDenied: return "位置情報の権限が必要です"
        case .routeNotFound: return "ルートが見つかりませんでした"
        case .audioSessionFailed: return "オーディオセッションの開始に失敗しました"
        case .dataNotFound: return "データが見つかりませんでした"
        }
    }
}

typealias TeslaResult<T> = Result<T, TeslaError>
```

## Preview Data Pattern

extension + static var preview パターン：

```swift
extension TeslaVehicleData {
    static var preview: TeslaVehicleData {
        TeslaVehicleData(
            speed: 65,
            batteryLevel: 85,
            range: 340,
            isCharging: false,
            driveMode: .comfort
        )
    }
}

#Preview {
    TeslaVehicleStatus(data: .preview)
        .environment(\.teslaTheme, TeslaTheme())
}
```

## Additional Resources

### Reference Files
- **`references/design-system.md`** - デザインシステム完全ガイド（日英）
- **`references/atomic-design-patterns.md`** - アトミックデザインパターン詳細
- **`references/theme-configuration.md`** - テーマプロバイダー実装詳細
- **`references/swiftdata-models.md`** - SwiftDataモデル設計ガイド
- **`references/animation-guidelines.md`** - Keyframe/Phaseアニメーション
- **`references/accessibility-guide.md`** - 完全アクセシビリティガイド
- **`references/mapkit-integration.md`** - MapKit + 音声案内統合
- **`references/avfoundation-integration.md`** - AVFoundation + RemoteCommand
- **`references/error-handling.md`** - Result<T, TeslaError>パターン
- **`references/troubleshooting.md`** - トラブルシューティング

### Example Files
実装サンプルは `examples/` ディレクトリを参照：

**Atoms:**
- `examples/atoms/tesla-colors.swift` - カラーパレット定義
- `examples/atoms/tesla-typography.swift` - タイポグラフィスケール
- `examples/atoms/tesla-icons.swift` - アイコン定義
- `examples/atoms/tesla-animation.swift` - アニメーションカーブ

**Molecules:**
- `examples/molecules/tesla-icon-button.swift` - アイコンボタン
- `examples/molecules/tesla-slider.swift` - スライダー
- `examples/molecules/tesla-toggle.swift` - トグル
- `examples/molecules/tesla-brightness-control.swift` - 明るさ調整

**Models:**
- `examples/models/tesla-error.swift` - エラー定義
- `examples/models/vehicle-data-provider.swift` - データプロバイダー
- `examples/models/tesla-vehicle-data.swift` - 車両データ
- `examples/models/tesla-settings.swift` - 設定
- `examples/models/tesla-favorite-location.swift` - お気に入り
- `examples/models/tesla-trip-history.swift` - 走行履歴
- `examples/models/tesla-energy-stats.swift` - エネルギー統計

**Organisms:**
- `examples/organisms/tesla-navigation-bar.swift` - ナビゲーションバー
- `examples/organisms/tesla-vehicle-status.swift` - 車両ステータス
- `examples/organisms/tesla-quick-actions-toolbar.swift` - クイックアクション
- `examples/organisms/tesla-music-bar.swift` - 音楽バー
- `examples/organisms/tesla-climate-control.swift` - 空調コントロール
- `examples/organisms/tesla-touchscreen-menu.swift` - タッチスクリーンメニュー
- `examples/organisms/tesla-map-view.swift` - マップビュー

**Templates:**
- `examples/templates/tesla-dashboard-layout.swift` - ダッシュボードレイアウト
- `examples/templates/tesla-split-view-layout.swift` - 分割ビュー
- `examples/templates/tesla-theme-provider.swift` - テーマプロバイダー

**Pages:**
- `examples/pages/tesla-main-dashboard.swift` - メインダッシュボード
- `examples/pages/tesla-navigation-screen.swift` - ナビゲーション画面
- `examples/pages/tesla-media-screen.swift` - メディア画面
- `examples/pages/tesla-climate-screen.swift` - 空調画面
- `examples/pages/tesla-vehicle-screen.swift` - 車両情報画面
