# Accessibility Guide / アクセシビリティガイド

Tesla Dashboard UIのアクセシビリティ対応について解説します。

## Overview / 概要

VoiceOver、Dynamic Type、Reduce Motion に完全対応したアクセシビリティシステムです。

## VoiceOver Support / VoiceOver対応

### 基本的なラベル設定

```swift
struct TeslaIconButton: View {
    let icon: TeslaIcon
    let label: String
    let isSelected: Bool

    var body: some View {
        Button { /* action */ } label: {
            VStack {
                Image(systemName: icon.systemName)
                Text(label)
            }
        }
        .accessibilityLabel(label)
        .accessibilityHint(isSelected ? "選択済み" : "ダブルタップで選択")
        .accessibilityAddTraits(isSelected ? .isSelected : [])
    }
}
```

### 複合コンポーネント

```swift
struct TeslaVehicleStatus: View {
    let vehicleData: VehicleData

    var body: some View {
        VStack {
            speedDisplay
            batteryDisplay
            rangeDisplay
        }
        .accessibilityElement(children: .combine)
        .accessibilityLabel(accessibilityDescription)
    }

    private var accessibilityDescription: String {
        "車両ステータス。速度 \(Int(vehicleData.speed))キロメートル毎時。バッテリー \(vehicleData.batteryLevel)パーセント。航続距離 \(Int(vehicleData.estimatedRange))キロメートル。"
    }
}
```

### アジャスタブルアクション（スライダー）

```swift
struct TeslaSlider: View {
    @Binding var value: Double
    let range: ClosedRange<Double>
    let label: String

    var body: some View {
        sliderView
            .accessibilityElement(children: .combine)
            .accessibilityLabel(label)
            .accessibilityValue(formattedValue)
            .accessibilityAdjustableAction { direction in
                adjustValue(direction: direction)
            }
    }

    private func adjustValue(direction: AccessibilityAdjustmentDirection) {
        let step = (range.upperBound - range.lowerBound) / 10
        switch direction {
        case .increment:
            value = min(value + step, range.upperBound)
        case .decrement:
            value = max(value - step, range.lowerBound)
        @unknown default:
            break
        }
    }
}
```

### カスタムアクション

```swift
struct TeslaQuickActionsToolbar: View {
    var body: some View {
        HStack {
            // actions
        }
        .accessibilityElement(children: .contain)
        .accessibilityCustomContent("状態", "空調オン、ロック済み")
    }
}
```

## Dynamic Type / Dynamic Type対応

### スケーラブルフォント

```swift
enum TeslaTypography {
    static let displayLarge = Font.system(size: 57, weight: .bold)
        .leading(.tight)

    static let titleMedium = Font.system(size: 16, weight: .medium)

    // Dynamic Type対応バージョン
    static func scaledDisplayLarge(for sizeCategory: ContentSizeCategory) -> Font {
        let baseSize: CGFloat = 57
        let scaleFactor = scaleFactor(for: sizeCategory)
        return Font.system(size: baseSize * scaleFactor, weight: .bold)
    }
}
```

### @ScaledMetric

```swift
struct TeslaIconButton: View {
    @ScaledMetric(relativeTo: .body) private var iconSize: CGFloat = 24
    @ScaledMetric(relativeTo: .caption) private var labelSpacing: CGFloat = 8

    var body: some View {
        VStack(spacing: labelSpacing) {
            Image(systemName: icon.systemName)
                .font(.system(size: iconSize))
            Text(label)
        }
    }
}
```

### minimumScaleFactor

```swift
Text(vehicleData.name)
    .font(TeslaTypography.titleMedium)
    .minimumScaleFactor(0.7)  // 最小70%まで縮小
    .lineLimit(1)
```

## Reduce Motion / Reduce Motion対応

### 基本パターン

```swift
struct TeslaAnimatedView: View {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        Button("Action") {
            withAnimation(reduceMotion ? .none : TeslaAnimation.quick) {
                isExpanded.toggle()
            }
        }
    }
}
```

### アニメーション切り替え

```swift
struct TeslaToggle: View {
    @Binding var isOn: Bool
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        toggleSwitch
            .animation(
                reduceMotion ? .none : TeslaAnimation.quick,
                value: isOn
            )
    }
}
```

### パルスアニメーションの制御

```swift
struct TeslaPulseModifier: ViewModifier {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var isPulsing = false

    func body(content: Content) -> some View {
        if reduceMotion {
            // アニメーションなし
            content
        } else {
            content
                .scaleEffect(isPulsing ? 1.05 : 1.0)
                .onAppear {
                    withAnimation(.easeInOut(duration: 1.0).repeatForever()) {
                        isPulsing = true
                    }
                }
        }
    }
}
```

## Color Contrast / カラーコントラスト

### WCAG 2.1 AA準拠

```swift
// テキストコントラスト比 4.5:1 以上
TeslaColors.textPrimary    // #FFFFFF on #141416 = 15.3:1 ✅
TeslaColors.textSecondary  // #B3B3B3 on #141416 = 8.5:1 ✅
TeslaColors.textTertiary   // #666666 on #141416 = 3.9:1 ⚠️ (大きいテキストのみ)

// ステータス色
TeslaColors.statusGreen   // #4DD966 十分なコントラスト
TeslaColors.statusOrange  // #FF9933 十分なコントラスト
TeslaColors.statusRed     // #F24D4D 十分なコントラスト
```

### アイコン + ラベルの併用

```swift
// アイコンだけでなくラベルも表示
HStack {
    Image(systemName: "lock.fill")
    Text("ロック中")
}

// 色だけでなくアイコンも変更
Image(systemName: vehicle.isLocked ? "lock.fill" : "lock.open.fill")
    .foregroundStyle(vehicle.isLocked ? TeslaColors.statusGreen : TeslaColors.statusOrange)
```

## Touch Targets / タッチターゲット

### 最小サイズ 44x44pt

```swift
struct TeslaIconButton: View {
    var body: some View {
        Button { } label: {
            Image(systemName: icon.systemName)
                .font(.system(size: 20))
        }
        .frame(minWidth: 44, minHeight: 44)  // 最小タッチサイズ
    }
}
```

### contentShape

```swift
HStack {
    icon
    label
}
.contentShape(Rectangle())  // タップ領域を拡大
.onTapGesture { }
```

## Focus Management / フォーカス管理

### @FocusState

```swift
struct TeslaSearchView: View {
    @FocusState private var isSearchFocused: Bool
    @State private var searchText = ""

    var body: some View {
        TextField("検索", text: $searchText)
            .focused($isSearchFocused)

        Button("検索") {
            // search action
        }
        .onSubmit {
            isSearchFocused = false
        }
    }
}
```

### フォーカス順序

```swift
VStack {
    temperatureSlider
        .accessibilitySortPriority(3)

    fanSpeedSlider
        .accessibilitySortPriority(2)

    confirmButton
        .accessibilitySortPriority(1)
}
```

## Semantic Content / セマンティックコンテンツ

### accessibilityElement

```swift
// 子要素を結合
.accessibilityElement(children: .combine)

// 子要素を含む
.accessibilityElement(children: .contain)

// 子要素を無視
.accessibilityElement(children: .ignore)
```

### accessibilityHidden

```swift
// 装飾的な要素を隠す
Image("decorative-background")
    .accessibilityHidden(true)
```

### accessibilityInputLabels

```swift
Button("OK") { }
    .accessibilityInputLabels(["OK", "確認", "決定", "はい"])
```

## Haptic Feedback / ハプティックフィードバック

```swift
struct TeslaToggle: View {
    @Binding var isOn: Bool

    var body: some View {
        Toggle("", isOn: $isOn)
            .onChange(of: isOn) { _, _ in
                let generator = UIImpactFeedbackGenerator(style: .medium)
                generator.impactOccurred()
            }
    }
}
```

## Testing Checklist / テストチェックリスト

### VoiceOver
- [ ] すべてのインタラクティブ要素にラベルがある
- [ ] 状態変化が読み上げられる
- [ ] 適切な順序でフォーカスが移動する

### Dynamic Type
- [ ] Extra Extra Large でレイアウトが崩れない
- [ ] テキストが切れずに表示される
- [ ] スクロール可能な領域が適切に動作する

### Reduce Motion
- [ ] アニメーションが無効になる
- [ ] 機能は維持される
- [ ] フラッシュや点滅がない

### Color Contrast
- [ ] テキストのコントラスト比が4.5:1以上
- [ ] 重要な情報が色だけでなく形状やテキストでも区別できる

## Related Documents / 関連ドキュメント

- [Animation Guidelines](./animation-guidelines.md)
- [Theme Configuration](./theme-configuration.md)
- [Design System](./design-system.md)
