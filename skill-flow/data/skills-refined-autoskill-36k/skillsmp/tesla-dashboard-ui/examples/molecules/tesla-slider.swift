// Tesla Dashboard UI - Slider
// アクセシビリティ完全対応のカスタムスライダー
// VoiceOver, Dynamic Type, Reduce Motion対応

import SwiftUI

// MARK: - Tesla Slider

/// Tesla風カスタムスライダー
/// ガラスモーフィズムデザインとアクセシビリティ対応
struct TeslaSlider: View {
    // MARK: - Properties

    @Binding var value: Double
    var range: ClosedRange<Double> = 0...1
    var step: Double? = nil
    var icon: TeslaIcon? = nil
    var label: String? = nil
    var showValue: Bool = true
    var valueFormatter: ((Double) -> String)? = nil

    // MARK: - Environment

    @Environment(\.teslaTheme) private var theme
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @Environment(\.isEnabled) private var isEnabled

    // MARK: - State

    @State private var isDragging = false

    // MARK: - Body

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            // Label Row
            if label != nil || showValue {
                labelRow
            }

            // Slider
            sliderView
        }
        .accessibilityElement(children: .combine)
        .accessibilityLabel(accessibilityLabel)
        .accessibilityValue(Text(formattedValue))
        .accessibilityAdjustableAction { direction in
            adjustValue(direction: direction)
        }
    }

    // MARK: - Label Row

    private var labelRow: some View {
        HStack {
            if let icon {
                TeslaIconView(
                    icon: icon,
                    size: 18,
                    color: isEnabled ? TeslaColors.textSecondary : TeslaColors.textDisabled
                )
            }

            if let label {
                Text(label)
                    .font(TeslaTypography.labelMedium)
                    .foregroundStyle(isEnabled ? TeslaColors.textSecondary : TeslaColors.textDisabled)
            }

            Spacer()

            if showValue {
                Text(formattedValue)
                    .font(TeslaTypography.labelMedium)
                    .foregroundStyle(isEnabled ? TeslaColors.textPrimary : TeslaColors.textDisabled)
                    .monospacedDigit()
            }
        }
    }

    // MARK: - Slider View

    private var sliderView: some View {
        GeometryReader { geometry in
            ZStack(alignment: .leading) {
                // Track Background
                RoundedRectangle(cornerRadius: 4)
                    .fill(TeslaColors.glassBackground)
                    .frame(height: 8)

                // Fill
                RoundedRectangle(cornerRadius: 4)
                    .fill(isEnabled ? TeslaColors.accent : TeslaColors.textDisabled)
                    .frame(width: fillWidth(for: geometry.size.width), height: 8)

                // Thumb
                Circle()
                    .fill(Color.white)
                    .frame(width: thumbSize, height: thumbSize)
                    .shadow(color: .black.opacity(0.3), radius: 4, y: 2)
                    .offset(x: thumbOffset(for: geometry.size.width))
                    .scaleEffect(isDragging ? 1.1 : 1.0)
                    .animation(
                        reduceMotion ? .none : TeslaAnimation.quick,
                        value: isDragging
                    )
                    .gesture(
                        DragGesture(minimumDistance: 0)
                            .onChanged { gesture in
                                isDragging = true
                                updateValue(from: gesture, width: geometry.size.width)
                            }
                            .onEnded { _ in
                                isDragging = false
                            }
                    )
            }
            .frame(height: 24)
        }
        .frame(height: 24)
        .allowsHitTesting(isEnabled)
    }

    // MARK: - Computed Properties

    private var normalizedValue: Double {
        (value - range.lowerBound) / (range.upperBound - range.lowerBound)
    }

    private var thumbSize: CGFloat { 24 }

    private var formattedValue: String {
        if let formatter = valueFormatter {
            return formatter(value)
        }
        return "\(Int(value * 100))%"
    }

    private var accessibilityLabel: String {
        if let label {
            return label
        }
        return "スライダー"
    }

    // MARK: - Methods

    private func fillWidth(for totalWidth: CGFloat) -> CGFloat {
        totalWidth * normalizedValue
    }

    private func thumbOffset(for totalWidth: CGFloat) -> CGFloat {
        (totalWidth - thumbSize) * normalizedValue
    }

    private func updateValue(from gesture: DragGesture.Value, width: CGFloat) {
        let newNormalized = max(0, min(1, gesture.location.x / width))
        var newValue = range.lowerBound + (range.upperBound - range.lowerBound) * newNormalized

        // Step snapping
        if let step {
            newValue = (newValue / step).rounded() * step
        }

        value = max(range.lowerBound, min(range.upperBound, newValue))
    }

    private func adjustValue(direction: AccessibilityAdjustmentDirection) {
        let stepAmount = step ?? ((range.upperBound - range.lowerBound) / 10)

        switch direction {
        case .increment:
            value = min(value + stepAmount, range.upperBound)
        case .decrement:
            value = max(value - stepAmount, range.lowerBound)
        @unknown default:
            break
        }
    }
}

// MARK: - Convenience Initializers

extension TeslaSlider {
    /// パーセント表示用スライダー
    /// - Parameters:
    ///   - value: 0.0〜1.0 の値
    ///   - label: ラベル
    ///   - icon: アイコン
    init(
        percent value: Binding<Double>,
        label: String? = nil,
        icon: TeslaIcon? = nil
    ) {
        self._value = value
        self.range = 0...1
        self.label = label
        self.icon = icon
        self.valueFormatter = { "\(Int($0 * 100))%" }
    }

    /// 温度用スライダー（16〜28度）
    /// - Parameters:
    ///   - temperature: 温度値
    ///   - label: ラベル
    init(
        temperature: Binding<Double>,
        label: String = "温度"
    ) {
        self._value = temperature
        self.range = 16...28
        self.step = 0.5
        self.label = label
        self.icon = .climate
        self.valueFormatter = { String(format: "%.1f°", $0) }
    }

    /// 音量用スライダー
    /// - Parameters:
    ///   - volume: 0.0〜1.0 の音量値
    ///   - label: ラベル
    init(
        volume: Binding<Double>,
        label: String = "音量"
    ) {
        self._value = volume
        self.range = 0...1
        self.label = label
        self.icon = .volume
        self.valueFormatter = { "\(Int($0 * 100))%" }
    }
}

// MARK: - Preview

#Preview("Tesla Slider") {
    struct SliderPreview: View {
        @State private var percentValue: Double = 0.5
        @State private var temperatureValue: Double = 22.0
        @State private var volumeValue: Double = 0.7
        @State private var customValue: Double = 50

        var body: some View {
            ScrollView {
                VStack(spacing: 32) {
                    // Basic Slider
                    VStack(alignment: .leading, spacing: 16) {
                        Text("Basic Slider")
                            .font(TeslaTypography.headlineSmall)
                            .foregroundStyle(TeslaColors.textPrimary)

                        TeslaSlider(
                            value: $percentValue,
                            label: "明るさ",
                            icon: .light
                        )
                    }

                    Divider()
                        .background(TeslaColors.glassBorder)

                    // Temperature Slider
                    VStack(alignment: .leading, spacing: 16) {
                        Text("Temperature")
                            .font(TeslaTypography.headlineSmall)
                            .foregroundStyle(TeslaColors.textPrimary)

                        TeslaSlider(temperature: $temperatureValue)
                    }

                    Divider()
                        .background(TeslaColors.glassBorder)

                    // Volume Slider
                    VStack(alignment: .leading, spacing: 16) {
                        Text("Volume")
                            .font(TeslaTypography.headlineSmall)
                            .foregroundStyle(TeslaColors.textPrimary)

                        TeslaSlider(volume: $volumeValue)
                    }

                    Divider()
                        .background(TeslaColors.glassBorder)

                    // Custom Range Slider
                    VStack(alignment: .leading, spacing: 16) {
                        Text("Custom Range (0-100)")
                            .font(TeslaTypography.headlineSmall)
                            .foregroundStyle(TeslaColors.textPrimary)

                        TeslaSlider(
                            value: $customValue,
                            range: 0...100,
                            step: 5,
                            icon: .fan,
                            label: "ファン速度",
                            valueFormatter: { "\(Int($0))" }
                        )
                    }

                    Divider()
                        .background(TeslaColors.glassBorder)

                    // Disabled Slider
                    VStack(alignment: .leading, spacing: 16) {
                        Text("Disabled")
                            .font(TeslaTypography.headlineSmall)
                            .foregroundStyle(TeslaColors.textPrimary)

                        TeslaSlider(
                            value: .constant(0.5),
                            label: "無効",
                            icon: .settings
                        )
                        .disabled(true)
                    }
                }
                .padding(24)
            }
            .background(TeslaColors.background)
        }
    }

    return SliderPreview()
}
