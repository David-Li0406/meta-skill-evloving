# Animation Guidelines / アニメーションガイドライン

Tesla Dashboard UIのアニメーションシステムと実装パターンについて解説します。

## Overview / 概要

iOS 17+ の `KeyframeAnimator` / `PhaseAnimator` を活用したモダンなアニメーションシステムです。

## Animation Presets / アニメーションプリセット

### TeslaAnimation

```swift
enum TeslaAnimation {
    /// 標準アニメーション（0.35秒）
    static let standard = Animation.spring(response: 0.35, dampingFraction: 0.8)

    /// クイックアニメーション（0.25秒）
    static let quick = Animation.spring(response: 0.25, dampingFraction: 0.85)

    /// スローアニメーション（0.5秒）
    static let slow = Animation.spring(response: 0.5, dampingFraction: 0.75)

    /// バウンシーアニメーション
    static let bouncy = Animation.spring(response: 0.4, dampingFraction: 0.6)
}
```

### 使用例

```swift
withAnimation(TeslaAnimation.quick) {
    isSelected.toggle()
}
```

## Custom Timing Curves / カスタムイージングカーブ

```swift
extension Animation {
    /// Tesla風イージング
    static let teslaEase = Animation.timingCurve(0.25, 0.1, 0.25, 1.0, duration: 0.3)

    /// 展開アニメーション
    static let teslaExpand = Animation.timingCurve(0.0, 0.0, 0.2, 1.0, duration: 0.4)

    /// 折りたたみアニメーション
    static let teslaCollapse = Animation.timingCurve(0.4, 0.0, 1.0, 1.0, duration: 0.3)
}
```

## Phase Animator / フェーズアニメーター

### 基本パターン

```swift
enum TeslaMusicBarPhase: CaseIterable {
    case idle
    case playing
    case paused

    var scale: Double {
        switch self {
        case .idle: return 1.0
        case .playing: return 1.02
        case .paused: return 0.98
        }
    }

    var opacity: Double {
        switch self {
        case .idle: return 1.0
        case .playing: return 1.0
        case .paused: return 0.8
        }
    }
}
```

### 使用例

```swift
struct TeslaMusicBarAnimated: View {
    let isPlaying: Bool

    var body: some View {
        PhaseAnimator(TeslaMusicBarPhase.allCases, trigger: isPlaying) { phase in
            HStack {
                // Content
            }
            .scaleEffect(phase.scale)
            .opacity(phase.opacity)
        } animation: { phase in
            switch phase {
            case .idle: return .spring(response: 0.3)
            case .playing: return .spring(response: 0.4, dampingFraction: 0.7)
            case .paused: return .easeOut(duration: 0.2)
            }
        }
    }
}
```

## Keyframe Animator / キーフレームアニメーター

### 車両ステータスアニメーション

```swift
struct TeslaVehicleStatusAnimated: View {
    @State private var animationTrigger = false

    var body: some View {
        KeyframeAnimator(
            initialValue: AnimationValues(),
            trigger: animationTrigger
        ) { values in
            VStack {
                speedDisplay
                    .scaleEffect(values.scale)
                    .opacity(values.opacity)
            }
        } keyframes: { _ in
            KeyframeTrack(\.scale) {
                CubicKeyframe(1.05, duration: 0.15)
                CubicKeyframe(1.0, duration: 0.25)
            }
            KeyframeTrack(\.opacity) {
                LinearKeyframe(0.7, duration: 0.1)
                LinearKeyframe(1.0, duration: 0.2)
            }
        }
    }

    struct AnimationValues {
        var scale: Double = 1.0
        var opacity: Double = 1.0
    }
}
```

### 充電アニメーション

```swift
struct TeslaChargingAnimation: View {
    @State private var isAnimating = false

    var body: some View {
        KeyframeAnimator(
            initialValue: ChargingAnimationValues(),
            repeating: true
        ) { values in
            Image(systemName: "bolt.fill")
                .foregroundStyle(TeslaColors.statusGreen)
                .scaleEffect(values.scale)
                .opacity(values.opacity)
                .offset(y: values.offsetY)
        } keyframes: { _ in
            KeyframeTrack(\.scale) {
                CubicKeyframe(1.2, duration: 0.5)
                CubicKeyframe(1.0, duration: 0.5)
            }
            KeyframeTrack(\.opacity) {
                LinearKeyframe(1.0, duration: 0.3)
                LinearKeyframe(0.6, duration: 0.4)
                LinearKeyframe(1.0, duration: 0.3)
            }
            KeyframeTrack(\.offsetY) {
                SpringKeyframe(-5, duration: 0.5)
                SpringKeyframe(0, duration: 0.5)
            }
        }
    }

    struct ChargingAnimationValues {
        var scale: Double = 1.0
        var opacity: Double = 1.0
        var offsetY: Double = 0
    }
}
```

## View Modifiers / ビューモディファイア

### TeslaPulseModifier

```swift
struct TeslaPulseModifier: ViewModifier {
    @State private var isPulsing = false

    func body(content: Content) -> some View {
        content
            .scaleEffect(isPulsing ? 1.05 : 1.0)
            .opacity(isPulsing ? 0.8 : 1.0)
            .onAppear {
                withAnimation(
                    .easeInOut(duration: 1.0)
                    .repeatForever(autoreverses: true)
                ) {
                    isPulsing = true
                }
            }
    }
}

extension View {
    func teslaPulse() -> some View {
        modifier(TeslaPulseModifier())
    }
}
```

### 使用例

```swift
Image(systemName: "bolt.fill")
    .teslaPulse()  // 充電中のパルスアニメーション
```

## Button Styles / ボタンスタイル

### TeslaScaleButtonStyle

```swift
struct TeslaScaleButtonStyle: ButtonStyle {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.92 : 1.0)
            .animation(
                reduceMotion ? .none : TeslaAnimation.quick,
                value: configuration.isPressed
            )
    }
}
```

### 使用例

```swift
Button("Action") { }
    .buttonStyle(TeslaScaleButtonStyle())
```

## Content Transition / コンテンツトランジション

### 数値アニメーション

```swift
Text("\(Int(speed))")
    .contentTransition(.numericText())

// カウントアップ/ダウン
Text("\(batteryLevel)%")
    .contentTransition(.numericText(countsDown: false))
```

### シンボルアニメーション

```swift
Image(systemName: isPlaying ? "pause.fill" : "play.fill")
    .contentTransition(.symbolEffect(.replace))
```

## Accessibility / アクセシビリティ

### Reduce Motion対応

```swift
struct TeslaAnimatedView: View {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        Button("Action") {
            withAnimation(reduceMotion ? .none : TeslaAnimation.quick) {
                // action
            }
        }
    }
}
```

### 条件付きアニメーション

```swift
.animation(
    reduceMotion ? .none : TeslaAnimation.standard,
    value: someValue
)
```

## Performance Tips / パフォーマンスヒント

### 1. drawingGroup() を使用

```swift
VStack {
    // 複雑なアニメーション
}
.drawingGroup()  // GPU レンダリング
```

### 2. アニメーション範囲を限定

```swift
// ✅ Good: 必要な部分のみアニメーション
VStack {
    staticContent

    animatedContent
        .animation(TeslaAnimation.quick, value: isAnimating)
}

// ❌ Bad: 全体をアニメーション
VStack {
    staticContent
    animatedContent
}
.animation(TeslaAnimation.quick, value: isAnimating)
```

### 3. transaction を使用

```swift
var transaction = Transaction(animation: TeslaAnimation.quick)
transaction.disablesAnimations = reduceMotion

withTransaction(transaction) {
    isExpanded.toggle()
}
```

## Common Patterns / 共通パターン

### トグルアニメーション

```swift
withAnimation(TeslaAnimation.quick) {
    isSelected.toggle()
}
```

### 展開/折りたたみ

```swift
withAnimation(TeslaAnimation.standard) {
    isExpanded.toggle()
}

// View
DisclosureGroup(isExpanded: $isExpanded) {
    // content
}
```

### スライドイン

```swift
.transition(.asymmetric(
    insertion: .move(edge: .trailing).combined(with: .opacity),
    removal: .move(edge: .leading).combined(with: .opacity)
))
```

### フェード

```swift
.transition(.opacity.animation(TeslaAnimation.slow))
```

## Related Documents / 関連ドキュメント

- [Theme Configuration](./theme-configuration.md)
- [Accessibility Guide](./accessibility-guide.md)
- [Design System](./design-system.md)
