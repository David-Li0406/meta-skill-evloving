// Tesla Dashboard UI - Animation
// KeyframeAnimator/PhaseAnimator によるカスタムアニメーション
// iOS 17+ の高度なアニメーションAPIを活用

import SwiftUI

// MARK: - Tesla Animation

/// Tesla Dashboard UI のアニメーション設定
enum TeslaAnimation {

    // MARK: - Spring Animations

    /// 標準的なスプリングアニメーション
    static let standard = Animation.spring(response: 0.4, dampingFraction: 0.8)

    /// 素早いスプリングアニメーション（ボタン押下など）
    static let quick = Animation.spring(response: 0.25, dampingFraction: 0.7)

    /// ゆっくりとしたスプリングアニメーション（画面遷移など）
    static let slow = Animation.spring(response: 0.6, dampingFraction: 0.85)

    /// バウンス効果のあるスプリングアニメーション
    static let bouncy = Animation.spring(response: 0.5, dampingFraction: 0.6)

    // MARK: - Easing Animations

    /// イーズイン・アウト
    static let easeInOut = Animation.easeInOut(duration: 0.3)

    /// イーズアウト（終わりがゆっくり）
    static let easeOut = Animation.easeOut(duration: 0.3)

    /// イーズイン（始まりがゆっくり）
    static let easeIn = Animation.easeIn(duration: 0.25)

    // MARK: - Custom Curves

    /// Tesla風のカスタムイージングカーブ（素早く始まり、ゆっくり終わる）
    static let teslaEase = Animation.timingCurve(0.2, 0.8, 0.2, 1.0, duration: 0.4)

    /// 画面展開用のカスタムカーブ
    static let expand = Animation.timingCurve(0.0, 0.0, 0.2, 1.0, duration: 0.35)

    /// 画面縮小用のカスタムカーブ
    static let collapse = Animation.timingCurve(0.4, 0.0, 1.0, 1.0, duration: 0.3)

    // MARK: - Durations

    /// 短い継続時間
    static let durationShort: Double = 0.2

    /// 標準の継続時間
    static let durationMedium: Double = 0.35

    /// 長い継続時間
    static let durationLong: Double = 0.5
}

// MARK: - Animation Scheme

/// テーマで使用するアニメーションスキーム
struct TeslaAnimationScheme: Sendable {
    let standard: Animation
    let quick: Animation
    let slow: Animation
    let bouncy: Animation

    /// デフォルトスキーム
    static let `default` = TeslaAnimationScheme(
        standard: TeslaAnimation.standard,
        quick: TeslaAnimation.quick,
        slow: TeslaAnimation.slow,
        bouncy: TeslaAnimation.bouncy
    )

    /// Reduce Motion対応スキーム（アニメーションなし）
    static let reduced = TeslaAnimationScheme(
        standard: .linear(duration: 0),
        quick: .linear(duration: 0),
        slow: .linear(duration: 0),
        bouncy: .linear(duration: 0)
    )
}

// MARK: - Phase Animator States

/// 音楽バー展開のフェーズ
enum TeslaMusicBarPhase: CaseIterable {
    case collapsed
    case expanding
    case expanded

    var height: CGFloat {
        switch self {
        case .collapsed: return 72
        case .expanding: return 150
        case .expanded: return 280
        }
    }

    var opacity: Double {
        switch self {
        case .collapsed: return 0
        case .expanding: return 0.5
        case .expanded: return 1.0
        }
    }
}

/// 車両ステータス表示のフェーズ
enum TeslaVehicleStatusPhase: CaseIterable {
    case hidden
    case appearing
    case visible

    var scale: CGFloat {
        switch self {
        case .hidden: return 0.8
        case .appearing: return 1.05
        case .visible: return 1.0
        }
    }

    var opacity: Double {
        switch self {
        case .hidden: return 0
        case .appearing: return 0.8
        case .visible: return 1.0
        }
    }
}

/// 充電アニメーションのフェーズ
enum TeslaChargingPhase: CaseIterable {
    case idle
    case pulse1
    case pulse2
    case pulse3

    var glowIntensity: Double {
        switch self {
        case .idle: return 0.3
        case .pulse1: return 0.6
        case .pulse2: return 0.9
        case .pulse3: return 0.6
        }
    }
}

// MARK: - Keyframe Values

/// 速度表示アニメーションのキーフレーム値
struct TeslaSpeedKeyframeValues {
    var scale: CGFloat = 1.0
    var opacity: Double = 1.0
    var offsetY: CGFloat = 0
}

/// バッテリー表示アニメーションのキーフレーム値
struct TeslaBatteryKeyframeValues {
    var fillWidth: CGFloat = 0
    var glowOpacity: Double = 0
}

// MARK: - Animation Modifiers

/// Reduce Motion対応のアニメーションViewModifier
struct TeslaReduceMotionModifier: ViewModifier {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    let animation: Animation
    let reducedAnimation: Animation

    func body(content: Content) -> some View {
        content
            .animation(reduceMotion ? reducedAnimation : animation, value: UUID())
    }
}

extension View {
    /// Reduce Motion対応のアニメーションを適用
    /// - Parameters:
    ///   - animation: 通常時のアニメーション
    ///   - reducedAnimation: Reduce Motion時のアニメーション（デフォルト: なし）
    func teslaAnimation(
        _ animation: Animation = TeslaAnimation.standard,
        reduced reducedAnimation: Animation = .linear(duration: 0)
    ) -> some View {
        modifier(TeslaReduceMotionModifier(
            animation: animation,
            reducedAnimation: reducedAnimation
        ))
    }
}

// MARK: - Pulse Animation Modifier

/// パルスアニメーション（充電中表示など）
struct TeslaPulseModifier: ViewModifier {
    @State private var isAnimating = false
    let duration: Double
    let minOpacity: Double
    let maxOpacity: Double

    func body(content: Content) -> some View {
        content
            .opacity(isAnimating ? maxOpacity : minOpacity)
            .onAppear {
                withAnimation(
                    .easeInOut(duration: duration)
                    .repeatForever(autoreverses: true)
                ) {
                    isAnimating = true
                }
            }
    }
}

extension View {
    /// パルスアニメーションを適用
    /// - Parameters:
    ///   - duration: 1サイクルの時間
    ///   - minOpacity: 最小不透明度
    ///   - maxOpacity: 最大不透明度
    func teslaPulse(
        duration: Double = 1.5,
        minOpacity: Double = 0.4,
        maxOpacity: Double = 1.0
    ) -> some View {
        modifier(TeslaPulseModifier(
            duration: duration,
            minOpacity: minOpacity,
            maxOpacity: maxOpacity
        ))
    }
}

// MARK: - Scale on Press Modifier

/// 押下時のスケールアニメーション
struct TeslaScaleOnPressModifier: ViewModifier {
    let isPressed: Bool
    let scale: CGFloat

    func body(content: Content) -> some View {
        content
            .scaleEffect(isPressed ? scale : 1.0)
            .animation(TeslaAnimation.quick, value: isPressed)
    }
}

extension View {
    /// 押下時のスケールアニメーションを適用
    /// - Parameters:
    ///   - isPressed: 押下状態
    ///   - scale: 押下時のスケール（デフォルト: 0.95）
    func teslaScaleOnPress(_ isPressed: Bool, scale: CGFloat = 0.95) -> some View {
        modifier(TeslaScaleOnPressModifier(isPressed: isPressed, scale: scale))
    }
}

// MARK: - Preview

#Preview("Tesla Animations") {
    struct AnimationPreview: View {
        @State private var isExpanded = false
        @State private var isPressed = false
        @State private var showStatus = false

        var body: some View {
            ScrollView {
                VStack(spacing: 32) {
                    // Spring Animations
                    VStack(alignment: .leading, spacing: 16) {
                        Text("Spring Animations")
                            .font(TeslaTypography.headlineSmall)
                            .foregroundStyle(TeslaColors.textPrimary)

                        Button("Toggle Expand") {
                            withAnimation(TeslaAnimation.standard) {
                                isExpanded.toggle()
                            }
                        }
                        .foregroundStyle(TeslaColors.accent)

                        RoundedRectangle(cornerRadius: 16)
                            .fill(TeslaColors.surface)
                            .frame(height: isExpanded ? 200 : 80)
                            .overlay {
                                Text(isExpanded ? "Expanded" : "Collapsed")
                                    .foregroundStyle(TeslaColors.textPrimary)
                            }
                    }

                    Divider()
                        .background(TeslaColors.glassBorder)

                    // Scale on Press
                    VStack(alignment: .leading, spacing: 16) {
                        Text("Scale on Press")
                            .font(TeslaTypography.headlineSmall)
                            .foregroundStyle(TeslaColors.textPrimary)

                        Button {
                            // Action
                        } label: {
                            Text("Hold Me")
                                .font(TeslaTypography.labelLarge)
                                .foregroundStyle(TeslaColors.textPrimary)
                                .padding()
                                .teslaGlassmorphism()
                        }
                        .buttonStyle(TeslaScaleButtonStyle())
                    }

                    Divider()
                        .background(TeslaColors.glassBorder)

                    // Pulse Animation
                    VStack(alignment: .leading, spacing: 16) {
                        Text("Pulse Animation")
                            .font(TeslaTypography.headlineSmall)
                            .foregroundStyle(TeslaColors.textPrimary)

                        HStack(spacing: 16) {
                            Circle()
                                .fill(TeslaColors.statusGreen)
                                .frame(width: 20, height: 20)
                                .teslaPulse()

                            Text("Charging...")
                                .font(TeslaTypography.bodyMedium)
                                .foregroundStyle(TeslaColors.statusGreen)
                        }
                    }

                    Divider()
                        .background(TeslaColors.glassBorder)

                    // Phase Animator
                    VStack(alignment: .leading, spacing: 16) {
                        Text("Phase Animator")
                            .font(TeslaTypography.headlineSmall)
                            .foregroundStyle(TeslaColors.textPrimary)

                        Button("Show Status") {
                            showStatus.toggle()
                        }
                        .foregroundStyle(TeslaColors.accent)

                        if showStatus {
                            PhaseAnimator(TeslaVehicleStatusPhase.allCases) { phase in
                                RoundedRectangle(cornerRadius: 16)
                                    .fill(TeslaColors.surface)
                                    .frame(height: 100)
                                    .scaleEffect(phase.scale)
                                    .opacity(phase.opacity)
                                    .overlay {
                                        Text("Vehicle Status")
                                            .foregroundStyle(TeslaColors.textPrimary)
                                    }
                            } animation: { phase in
                                switch phase {
                                case .hidden: .easeOut(duration: 0.1)
                                case .appearing: .spring(response: 0.3, dampingFraction: 0.6)
                                case .visible: .spring(response: 0.2, dampingFraction: 0.8)
                                }
                            }
                        }
                    }
                }
                .padding(24)
            }
            .background(TeslaColors.background)
        }
    }

    return AnimationPreview()
}

// MARK: - Button Style

/// Tesla風のボタンスタイル（スケールアニメーション付き）
struct TeslaScaleButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
            .animation(TeslaAnimation.quick, value: configuration.isPressed)
    }
}
