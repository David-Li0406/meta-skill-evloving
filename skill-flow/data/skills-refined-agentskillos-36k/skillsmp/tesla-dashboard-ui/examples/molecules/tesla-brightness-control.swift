// Tesla Dashboard UI - Brightness Control
// 明るさ調整コントロール
// スライダー + アイコン付きの専用コンポーネント

import SwiftUI

// MARK: - Tesla Brightness Control

/// Tesla風明るさ調整コントロール
/// 太陽/月アイコンと連動したスライダー
struct TeslaBrightnessControl: View {
    // MARK: - Properties

    @Binding var brightness: Double
    var label: String = "画面の明るさ"
    var showAutoButton: Bool = true
    var onAutoTap: (() -> Void)? = nil

    // MARK: - Environment

    @Environment(\.teslaTheme) private var theme
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    // MARK: - State

    @State private var isAutoEnabled = false

    // MARK: - Body

    var body: some View {
        VStack(spacing: 16) {
            // Header
            HStack {
                Text(label)
                    .font(TeslaTypography.titleMedium)
                    .foregroundStyle(TeslaColors.textPrimary)

                Spacer()

                if showAutoButton {
                    autoButton
                }
            }

            // Brightness Slider
            HStack(spacing: 16) {
                // Min Icon (Moon)
                Image(systemName: "sun.min.fill")
                    .font(.system(size: 16))
                    .foregroundStyle(iconColor(for: 0.3))

                // Slider
                brightnessSlider

                // Max Icon (Sun)
                Image(systemName: "sun.max.fill")
                    .font(.system(size: 20))
                    .foregroundStyle(iconColor(for: 1.0))
            }

            // Value Display
            Text("\(Int(brightness * 100))%")
                .font(TeslaTypography.labelMedium)
                .foregroundStyle(TeslaColors.textSecondary)
                .monospacedDigit()
        }
        .padding(16)
        .teslaGlassmorphism()
        .accessibilityElement(children: .combine)
        .accessibilityLabel(label)
        .accessibilityValue("\(Int(brightness * 100))パーセント")
        .accessibilityAdjustableAction { direction in
            adjustBrightness(direction: direction)
        }
    }

    // MARK: - Auto Button

    private var autoButton: some View {
        Button {
            withAnimation(TeslaAnimation.quick) {
                isAutoEnabled.toggle()
            }
            onAutoTap?()
        } label: {
            HStack(spacing: 4) {
                Image(systemName: "wand.and.stars")
                    .font(.system(size: 12))

                Text("自動")
                    .font(TeslaTypography.labelSmall)
            }
            .foregroundStyle(isAutoEnabled ? TeslaColors.accent : TeslaColors.textSecondary)
            .padding(.horizontal, 12)
            .padding(.vertical, 6)
            .background(
                RoundedRectangle(cornerRadius: 8)
                    .fill(isAutoEnabled ? TeslaColors.accent.opacity(0.2) : TeslaColors.glassBackground)
            )
        }
        .buttonStyle(TeslaScaleButtonStyle())
    }

    // MARK: - Brightness Slider

    private var brightnessSlider: some View {
        GeometryReader { geometry in
            ZStack(alignment: .leading) {
                // Track Background
                RoundedRectangle(cornerRadius: 6)
                    .fill(TeslaColors.glassBackground)
                    .frame(height: 12)

                // Gradient Fill
                RoundedRectangle(cornerRadius: 6)
                    .fill(
                        LinearGradient(
                            colors: [
                                TeslaColors.textTertiary,
                                TeslaColors.accent
                            ],
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
                    .frame(width: geometry.size.width * brightness, height: 12)

                // Thumb
                Circle()
                    .fill(Color.white)
                    .frame(width: 28, height: 28)
                    .shadow(color: .black.opacity(0.2), radius: 4, y: 2)
                    .offset(x: thumbOffset(for: geometry.size.width))
                    .gesture(
                        DragGesture(minimumDistance: 0)
                            .onChanged { gesture in
                                updateBrightness(from: gesture, width: geometry.size.width)
                            }
                    )
            }
            .frame(height: 28)
        }
        .frame(height: 28)
    }

    // MARK: - Computed Properties

    private func iconColor(for targetBrightness: Double) -> Color {
        brightness >= targetBrightness ? TeslaColors.accent : TeslaColors.textTertiary
    }

    private func thumbOffset(for width: CGFloat) -> CGFloat {
        let thumbWidth: CGFloat = 28
        return (width - thumbWidth) * brightness
    }

    // MARK: - Methods

    private func updateBrightness(from gesture: DragGesture.Value, width: CGFloat) {
        let newValue = gesture.location.x / width
        brightness = max(0, min(1, newValue))
    }

    private func adjustBrightness(direction: AccessibilityAdjustmentDirection) {
        let step: Double = 0.1
        switch direction {
        case .increment:
            brightness = min(brightness + step, 1.0)
        case .decrement:
            brightness = max(brightness - step, 0.0)
        @unknown default:
            break
        }
    }
}

// MARK: - Compact Brightness Control

/// コンパクトな明るさ調整コントロール（アイコンのみ）
struct TeslaCompactBrightnessControl: View {
    @Binding var brightness: Double

    var body: some View {
        HStack(spacing: 12) {
            // Decrease Button
            Button {
                withAnimation(TeslaAnimation.quick) {
                    brightness = max(0, brightness - 0.1)
                }
            } label: {
                Image(systemName: "sun.min.fill")
                    .font(.system(size: 18))
                    .foregroundStyle(TeslaColors.textSecondary)
                    .frame(width: 44, height: 44)
                    .background(TeslaColors.glassBackground)
                    .clipShape(Circle())
            }
            .buttonStyle(TeslaScaleButtonStyle())

            // Value
            Text("\(Int(brightness * 100))%")
                .font(TeslaTypography.titleMedium)
                .foregroundStyle(TeslaColors.textPrimary)
                .monospacedDigit()
                .frame(minWidth: 50)

            // Increase Button
            Button {
                withAnimation(TeslaAnimation.quick) {
                    brightness = min(1, brightness + 0.1)
                }
            } label: {
                Image(systemName: "sun.max.fill")
                    .font(.system(size: 18))
                    .foregroundStyle(TeslaColors.textSecondary)
                    .frame(width: 44, height: 44)
                    .background(TeslaColors.glassBackground)
                    .clipShape(Circle())
            }
            .buttonStyle(TeslaScaleButtonStyle())
        }
    }
}

// MARK: - Preview

#Preview("Tesla Brightness Control") {
    struct BrightnessPreview: View {
        @State private var brightness1: Double = 0.7
        @State private var brightness2: Double = 0.5

        var body: some View {
            VStack(spacing: 32) {
                // Full Brightness Control
                VStack(alignment: .leading, spacing: 16) {
                    Text("Full Control")
                        .font(TeslaTypography.headlineSmall)
                        .foregroundStyle(TeslaColors.textPrimary)

                    TeslaBrightnessControl(
                        brightness: $brightness1,
                        label: "画面の明るさ"
                    ) {
                        print("Auto tapped")
                    }
                }

                Divider()
                    .background(TeslaColors.glassBorder)

                // Without Auto Button
                VStack(alignment: .leading, spacing: 16) {
                    Text("Without Auto")
                        .font(TeslaTypography.headlineSmall)
                        .foregroundStyle(TeslaColors.textPrimary)

                    TeslaBrightnessControl(
                        brightness: $brightness2,
                        label: "ディスプレイ",
                        showAutoButton: false
                    )
                }

                Divider()
                    .background(TeslaColors.glassBorder)

                // Compact Control
                VStack(alignment: .leading, spacing: 16) {
                    Text("Compact")
                        .font(TeslaTypography.headlineSmall)
                        .foregroundStyle(TeslaColors.textPrimary)

                    TeslaCompactBrightnessControl(brightness: $brightness1)
                        .padding(16)
                        .teslaCard()
                }

                Spacer()
            }
            .padding(24)
            .background(TeslaColors.background)
        }
    }

    return BrightnessPreview()
}
