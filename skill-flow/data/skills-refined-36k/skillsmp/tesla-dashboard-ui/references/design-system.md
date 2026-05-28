# Tesla Dashboard UI Design System

Tesla Dashboard UIのデザインシステム完全ガイド。

## Overview / 概要

Tesla Dashboard UIは、Tesla Model 3のダッシュボードにインスパイアされたiOS向けUIコンポーネントライブラリです。アトミックデザイン原則に基づき、ダークテーマ、ガラスモーフィズム、高視認性を特徴としています。

This is a comprehensive UI component library for iOS, inspired by Tesla Model 3's dashboard. Built on atomic design principles, featuring dark theme, glassmorphism, and high visibility for automotive applications.

---

## Design Principles / デザイン原則

### 1. Dark Theme First / ダークテーマファースト

車載環境での使用を想定し、目の疲れを軽減するダークテーマを採用。

- 背景色は純粋な黒ではなく、わずかに青みがかったダークグレー (#141416)
- 高コントラストなテキストと要素
- グレアを防ぐマットな色調

### 2. High Visibility / 高視認性

運転中の一瞬の視認を想定した大きな文字とアイコン。

- Display フォントは 57pt から開始
- アイコンは 24pt 以上
- 重要な情報は画面の上部または中央に配置

### 3. Touch-Friendly / タッチフレンドリー

大きなタッチターゲットと明確なフィードバック。

- 最小タッチターゲット: 44pt × 44pt
- ボタンのスケールアニメーション
- 押下状態の視覚的フィードバック

### 4. Glassmorphism / ガラスモーフィズム

奥行きと階層を表現するガラス効果。

- Blur radius: 30
- Background opacity: 0.16
- Border: 1px white at 12% opacity

---

## Color Palette / カラーパレット

### Background Colors / 背景色

| Name | Variable | HEX | RGB | Usage |
|------|----------|-----|-----|-------|
| Background | `background` | #141416 | 20, 20, 22 | メイン背景 |
| Surface | `surface` | #1E1E22 | 30, 30, 34 | カード・パネル |
| Surface Elevated | `surfaceElevated` | #28282C | 40, 40, 44 | 浮き上がった要素 |

### Accent Colors / アクセント色

| Name | Variable | HEX | RGB | Usage |
|------|----------|-----|-----|-------|
| Tesla Blue | `accent` | #3399FF | 51, 153, 255 | 主要アクション |
| Status Green | `statusGreen` | #4DD966 | 77, 217, 102 | 正常・充電完了 |
| Status Orange | `statusOrange` | #FF9933 | 255, 153, 51 | 警告・後進 |
| Status Red | `statusRed` | #F24D4D | 242, 77, 77 | エラー・緊急 |

### Text Colors / テキスト色

| Name | Variable | HEX | Opacity | Usage |
|------|----------|-----|---------|-------|
| Primary | `textPrimary` | #FFFFFF | 100% | メインテキスト |
| Secondary | `textSecondary` | #B3B3B3 | 70% | サブテキスト |
| Tertiary | `textTertiary` | #808080 | 50% | 補助テキスト |
| Disabled | `textDisabled` | #4D4D4D | 30% | 無効テキスト |

### Glassmorphism Colors / ガラスモーフィズム色

| Name | Variable | Value | Usage |
|------|----------|-------|-------|
| Glass Background | `glassBackground` | #FFFFFF at 8% | 標準ガラス背景 |
| Glass Background Elevated | `glassBackgroundElevated` | #FFFFFF at 16% | 強調ガラス背景 |
| Glass Border | `glassBorder` | #FFFFFF at 12% | ガラス境界線 |

---

## Typography / タイポグラフィ

### Type Scale / タイプスケール

```
Display Large   : 57pt / Regular  → 速度表示
Display Medium  : 45pt / Regular  → バッテリー残量
Display Small   : 36pt / Regular  → 航続距離
Headline Large  : 32pt / Semibold → セクション見出し
Headline Medium : 28pt / Semibold → カードタイトル
Headline Small  : 24pt / Semibold → サブセクション見出し
Title Large     : 22pt / Medium   → リスト見出し
Title Medium    : 18pt / Medium   → リスト項目
Title Small     : 14pt / Medium   → 小見出し
Body Large      : 16pt / Regular  → 本文
Body Medium     : 14pt / Regular  → 説明文
Body Small      : 12pt / Regular  → 注釈
Label Large     : 14pt / Medium   → ボタンラベル
Label Medium    : 12pt / Medium   → タブラベル
Label Small     : 10pt / Medium   → 補助ラベル
```

### Font Family / フォントファミリー

- **Primary**: SF Pro (System Default)
- **Monospaced**: SF Mono (数値表示用)

### Dynamic Type Support / Dynamic Type対応

- 最大サイズ制限: xxxLarge
- アクセシビリティサイズへの対応
- `.dynamicTypeSize(...maxSize)` で制限

---

## Spacing / 間隔

### Base Unit / 基本単位

4pt グリッドシステムを採用。

### Spacing Scale / 間隔スケール

| Token | Value | Usage |
|-------|-------|-------|
| `xxs` | 4pt | アイコンとテキストの間 |
| `xs` | 8pt | 関連要素間 |
| `sm` | 12pt | コンポーネント内部 |
| `md` | 16pt | カード内パディング |
| `lg` | 24pt | セクション間 |
| `xl` | 32pt | 大きなセクション間 |
| `xxl` | 48pt | ページ間 |

---

## Component Specifications / コンポーネント仕様

### Buttons / ボタン

**Icon Button (TeslaIconButton)**
- Size: 56pt × 56pt (touch target)
- Icon size: 24pt
- Corner radius: 28pt (circle)
- Background: `glassBackground`
- Selected state: `accent` background

**Primary Button**
- Height: 56pt
- Corner radius: 12pt
- Background: `accent`
- Text: `textPrimary`, Label Large

### Cards / カード

**Standard Card**
- Padding: 16pt
- Corner radius: 16pt
- Background: `surface`

**Glass Card**
- Padding: 16pt
- Corner radius: 16pt
- Background: `.ultraThinMaterial` + `glassBackground`
- Border: 1pt `glassBorder`

### Sliders / スライダー

**Standard Slider**
- Track height: 8pt
- Thumb size: 24pt × 24pt
- Track background: `glassBackground`
- Fill: `accent`
- Thumb: White with shadow

### Navigation Bar / ナビゲーションバー

- Height: 64pt
- Background: `background`
- Title: Headline Large
- Safe area: Top inset respected

---

## Animation / アニメーション

### Spring Animations / スプリングアニメーション

| Type | Response | Damping | Usage |
|------|----------|---------|-------|
| Standard | 0.4s | 0.8 | 一般的な遷移 |
| Quick | 0.25s | 0.7 | ボタン押下 |
| Slow | 0.6s | 0.85 | 画面遷移 |
| Bouncy | 0.5s | 0.6 | 強調表示 |

### Custom Curves / カスタムカーブ

**Tesla Ease**
```swift
Animation.timingCurve(0.2, 0.8, 0.2, 1.0, duration: 0.4)
```
素早く始まり、ゆっくり終わる自然な動き。

### Phase Animator / フェーズアニメーター

複雑な状態遷移に使用:
- 音楽バーの展開
- 車両ステータスの表示
- 充電アニメーション

### Reduce Motion / モーション軽減

`@Environment(\.accessibilityReduceMotion)` で確認し、必要に応じてアニメーションを無効化。

---

## Accessibility / アクセシビリティ

### VoiceOver Support / VoiceOver対応

すべてのインタラクティブ要素に:
- `accessibilityLabel` - 要素の説明
- `accessibilityHint` - 操作の結果
- `accessibilityValue` - 現在の値

### Dynamic Type / Dynamic Type

- すべてのテキストがスケール可能
- 最大サイズを適切に制限
- レイアウトが崩れないよう配慮

### Color Contrast / カラーコントラスト

- テキスト: 最低 4.5:1
- 大きなテキスト: 最低 3:1
- インタラクティブ要素: 最低 3:1

### Reduce Motion / モーション軽減

- アニメーションを無効化またはシンプル化
- 重要な情報は静的に表示

---

## Implementation Guidelines / 実装ガイドライン

### File Naming / ファイル命名

```
tesla-[category]-[name].swift
例: tesla-icon-button.swift
```

### Component Naming / コンポーネント命名

```
Tesla[Name]
例: TeslaIconButton, TeslaSlider
```

### Preview Pattern / プレビューパターン

```swift
#Preview("Component Name") {
    TeslaThemeProvider {
        ComponentName()
    }
}
```

### Static Preview Data / 静的プレビューデータ

```swift
extension ModelName {
    static var preview: ModelName {
        ModelName(...)
    }
}
```

---

## Platform Support / プラットフォームサポート

| Platform | Version | Notes |
|----------|---------|-------|
| iOS | 17.0+ | Primary target |
| iPadOS | 17.0+ | Optimized for landscape |
| macOS | - | Not supported |
| watchOS | - | Not supported |
| tvOS | - | Not supported |

---

## Dependencies / 依存関係

### Required Frameworks / 必須フレームワーク

- SwiftUI
- SwiftData
- Observation

### Optional Frameworks / オプションフレームワーク

- MapKit (ナビゲーション機能)
- CoreLocation (位置情報)
- AVFoundation (音楽再生)
- MediaPlayer (Now Playing)
- AVSpeechSynthesizer (音声案内)

---

## Version History / バージョン履歴

### 1.0.0 (2024-XX-XX)

- Initial release
- Complete atomic design component set
- SwiftData integration
- MapKit + AVFoundation integration
- Full accessibility support
