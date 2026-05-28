// Tesla Dashboard UI - Climate Control
// スライダーベース空調コントロール
// 温度・ファン・シートヒーター・プリコンディショニング対応

import SwiftUI

// MARK: - Tesla Climate Control

/// Tesla風空調コントロールパネル
/// 温度、ファン速度、シートヒーター、デフロスター制御
struct TeslaClimateControl: View {
    // MARK: - Properties

    @Binding var climateData: TeslaClimateData
    var onClimateToggle: ((Bool) -> Void)? = nil
    var onTemperatureChange: ((Double) -> Void)? = nil

    // MARK: - Environment

    @Environment(\.teslaTheme) private var theme
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    // MARK: - Body

    var body: some View {
        VStack(spacing: 24) {
            // Header
            climateHeader

            // Temperature Control
            temperatureSection

            // Fan & Air Flow
            fanSection

            // Seat Heaters
            seatHeaterSection

            // Quick Controls
            quickControlsSection
        }
        .padding(24)
        .teslaCard()
    }

    // MARK: - Header

    private var climateHeader: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text("空調コントロール")
                    .font(TeslaTypography.headlineSmall)
                    .foregroundStyle(TeslaColors.textPrimary)

                HStack(spacing: 8) {
                    // Interior Temp
                    HStack(spacing: 4) {
                        Image(systemName: "thermometer.medium")
                            .font(.system(size: 12))
                        Text("車内 \(String(format: "%.1f", climateData.interiorTemperature))°C")
                            .font(TeslaTypography.labelMedium)
                    }
                    .foregroundStyle(TeslaColors.textSecondary)

                    Text("•")
                        .foregroundStyle(TeslaColors.textTertiary)

                    // Exterior Temp
                    Text("外気 \(String(format: "%.1f", climateData.exteriorTemperature))°C")
                        .font(TeslaTypography.labelMedium)
                        .foregroundStyle(TeslaColors.textSecondary)
                }
            }

            Spacer()

            // Climate Power Toggle
            TeslaToggle(
                isOn: $climateData.isClimateOn,
                label: "",
                icon: .climate
            )
            .onChange(of: climateData.isClimateOn) { _, newValue in
                onClimateToggle?(newValue)
            }
        }
    }

    // MARK: - Temperature Section

    private var temperatureSection: some View {
        VStack(spacing: 16) {
            // Temperature Display
            HStack(alignment: .center, spacing: 32) {
                // Driver Side
                temperatureControl(
                    label: "運転席",
                    temperature: $climateData.driverTemperature,
                    isLinked: climateData.isTemperatureLinked
                )

                // Sync Button
                Button {
                    withAnimation(TeslaAnimation.quick) {
                        climateData.isTemperatureLinked.toggle()
                        if climateData.isTemperatureLinked {
                            climateData.passengerTemperature = climateData.driverTemperature
                        }
                    }
                } label: {
                    Image(systemName: climateData.isTemperatureLinked ? "link" : "link.badge.plus")
                        .font(.system(size: 16))
                        .foregroundStyle(climateData.isTemperatureLinked ? TeslaColors.accent : TeslaColors.textSecondary)
                        .frame(width: 44, height: 44)
                        .background(TeslaColors.glassBackground)
                        .clipShape(Circle())
                }
                .buttonStyle(TeslaScaleButtonStyle())

                // Passenger Side
                temperatureControl(
                    label: "助手席",
                    temperature: Binding(
                        get: { climateData.isTemperatureLinked ? climateData.driverTemperature : climateData.passengerTemperature },
                        set: { climateData.passengerTemperature = $0 }
                    ),
                    isLinked: climateData.isTemperatureLinked,
                    isDisabled: climateData.isTemperatureLinked
                )
            }
        }
        .padding(16)
        .background(TeslaColors.glassBackground)
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }

    private func temperatureControl(
        label: String,
        temperature: Binding<Double>,
        isLinked: Bool,
        isDisabled: Bool = false
    ) -> some View {
        VStack(spacing: 8) {
            Text(label)
                .font(TeslaTypography.labelMedium)
                .foregroundStyle(TeslaColors.textSecondary)

            // Temperature Display
            HStack(alignment: .lastTextBaseline, spacing: 2) {
                Text(String(format: "%.1f", temperature.wrappedValue))
                    .font(TeslaTypography.displaySmall)
                    .foregroundStyle(isDisabled ? TeslaColors.textDisabled : TeslaColors.textPrimary)
                    .monospacedDigit()
                    .contentTransition(.numericText())

                Text("°C")
                    .font(TeslaTypography.titleSmall)
                    .foregroundStyle(TeslaColors.textSecondary)
            }

            // Temperature Buttons
            HStack(spacing: 8) {
                temperatureButton(systemName: "minus", delta: -0.5, temperature: temperature, isDisabled: isDisabled)
                temperatureButton(systemName: "plus", delta: 0.5, temperature: temperature, isDisabled: isDisabled)
            }
        }
        .opacity(isDisabled ? 0.5 : 1.0)
    }

    private func temperatureButton(
        systemName: String,
        delta: Double,
        temperature: Binding<Double>,
        isDisabled: Bool
    ) -> some View {
        Button {
            withAnimation(TeslaAnimation.quick) {
                let newValue = temperature.wrappedValue + delta
                temperature.wrappedValue = max(16, min(28, newValue))
                onTemperatureChange?(temperature.wrappedValue)
            }
        } label: {
            Image(systemName: systemName)
                .font(.system(size: 14, weight: .semibold))
                .foregroundStyle(TeslaColors.textPrimary)
                .frame(width: 36, height: 36)
                .background(TeslaColors.glassBackground)
                .clipShape(Circle())
        }
        .buttonStyle(TeslaScaleButtonStyle())
        .disabled(isDisabled)
    }

    // MARK: - Fan Section

    private var fanSection: some View {
        VStack(spacing: 12) {
            HStack {
                TeslaIconView(icon: .fan, size: 18, color: TeslaColors.textSecondary)
                Text("ファン速度")
                    .font(TeslaTypography.titleSmall)
                    .foregroundStyle(TeslaColors.textSecondary)

                Spacer()

                // Auto Button
                Button {
                    withAnimation(TeslaAnimation.quick) {
                        climateData.isAutoFan.toggle()
                    }
                } label: {
                    Text("自動")
                        .font(TeslaTypography.labelSmall)
                        .foregroundStyle(climateData.isAutoFan ? TeslaColors.accent : TeslaColors.textSecondary)
                        .padding(.horizontal, 12)
                        .padding(.vertical, 6)
                        .background(
                            RoundedRectangle(cornerRadius: 6)
                                .fill(climateData.isAutoFan ? TeslaColors.accent.opacity(0.2) : TeslaColors.glassBackground)
                        )
                }
            }

            TeslaSlider(
                value: $climateData.fanSpeed,
                range: 1...7,
                step: 1,
                showValue: true,
                valueFormatter: { "レベル \(Int($0))" }
            )
            .disabled(climateData.isAutoFan)
            .opacity(climateData.isAutoFan ? 0.5 : 1.0)
        }
        .padding(16)
        .background(TeslaColors.glassBackground)
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }

    // MARK: - Seat Heater Section

    private var seatHeaterSection: some View {
        VStack(spacing: 12) {
            HStack {
                TeslaIconView(icon: .seatHeater, size: 18, color: TeslaColors.textSecondary)
                Text("シートヒーター")
                    .font(TeslaTypography.titleSmall)
                    .foregroundStyle(TeslaColors.textSecondary)

                Spacer()
            }

            HStack(spacing: 24) {
                // Driver Seat
                seatHeaterControl(
                    label: "運転席",
                    level: $climateData.driverSeatHeater
                )

                Divider()
                    .frame(height: 60)
                    .background(TeslaColors.glassBorder)

                // Passenger Seat
                seatHeaterControl(
                    label: "助手席",
                    level: $climateData.passengerSeatHeater
                )
            }
        }
        .padding(16)
        .background(TeslaColors.glassBackground)
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }

    private func seatHeaterControl(label: String, level: Binding<Int>) -> some View {
        VStack(spacing: 8) {
            Text(label)
                .font(TeslaTypography.labelMedium)
                .foregroundStyle(TeslaColors.textSecondary)

            // Heat Level Indicator
            HStack(spacing: 4) {
                ForEach(1...3, id: \.self) { index in
                    Button {
                        withAnimation(TeslaAnimation.quick) {
                            level.wrappedValue = level.wrappedValue == index ? 0 : index
                        }
                    } label: {
                        RoundedRectangle(cornerRadius: 4)
                            .fill(index <= level.wrappedValue ? TeslaColors.statusOrange : TeslaColors.glassBackground)
                            .frame(width: 24, height: 8 + CGFloat(index) * 4)
                    }
                    .buttonStyle(TeslaScaleButtonStyle())
                }
            }

            Text(seatHeaterLabel(level.wrappedValue))
                .font(TeslaTypography.labelSmall)
                .foregroundStyle(TeslaColors.textTertiary)
        }
    }

    private func seatHeaterLabel(_ level: Int) -> String {
        switch level {
        case 0: return "オフ"
        case 1: return "弱"
        case 2: return "中"
        case 3: return "強"
        default: return "オフ"
        }
    }

    // MARK: - Quick Controls Section

    private var quickControlsSection: some View {
        HStack(spacing: 16) {
            // Defrost
            TeslaIconButton(
                icon: .defrost,
                label: "デフロスト",
                isSelected: climateData.isDefrostOn
            ) {
                withAnimation(TeslaAnimation.quick) {
                    climateData.isDefrostOn.toggle()
                }
            }

            // Rear Defrost
            TeslaIconButton(
                icon: .rearDefrost,
                label: "リア",
                isSelected: climateData.isRearDefrostOn
            ) {
                withAnimation(TeslaAnimation.quick) {
                    climateData.isRearDefrostOn.toggle()
                }
            }

            // Recirculation
            TeslaIconButton(
                icon: .fan,
                label: "内気循環",
                isSelected: climateData.isRecirculationOn
            ) {
                withAnimation(TeslaAnimation.quick) {
                    climateData.isRecirculationOn.toggle()
                }
            }

            Spacer()

            // Preconditioning
            VStack(spacing: 4) {
                Button {
                    withAnimation(TeslaAnimation.quick) {
                        climateData.isPreconditioningEnabled.toggle()
                    }
                } label: {
                    HStack(spacing: 6) {
                        Image(systemName: "clock.arrow.circlepath")
                            .font(.system(size: 14))
                        Text("プリコン")
                            .font(TeslaTypography.labelMedium)
                    }
                    .foregroundStyle(climateData.isPreconditioningEnabled ? .white : TeslaColors.textSecondary)
                    .padding(.horizontal, 16)
                    .padding(.vertical, 10)
                    .background(
                        RoundedRectangle(cornerRadius: 8)
                            .fill(climateData.isPreconditioningEnabled ? TeslaColors.accent : TeslaColors.glassBackground)
                    )
                }
                .buttonStyle(TeslaScaleButtonStyle())
            }
        }
    }
}

// MARK: - Tesla Climate Data

/// 空調データ
struct TeslaClimateData {
    // Status
    var isClimateOn: Bool = false
    var interiorTemperature: Double = 22.0
    var exteriorTemperature: Double = 25.0

    // Temperature
    var driverTemperature: Double = 22.0
    var passengerTemperature: Double = 22.0
    var isTemperatureLinked: Bool = true

    // Fan
    var fanSpeed: Double = 3
    var isAutoFan: Bool = true

    // Seat Heaters (0-3)
    var driverSeatHeater: Int = 0
    var passengerSeatHeater: Int = 0

    // Controls
    var isDefrostOn: Bool = false
    var isRearDefrostOn: Bool = false
    var isRecirculationOn: Bool = false
    var isPreconditioningEnabled: Bool = false
}

// MARK: - Preview

extension TeslaClimateData {
    static var preview: TeslaClimateData {
        TeslaClimateData(
            isClimateOn: true,
            interiorTemperature: 24.5,
            exteriorTemperature: 30.0,
            driverTemperature: 22.0,
            passengerTemperature: 22.0,
            fanSpeed: 4,
            driverSeatHeater: 2
        )
    }
}

#Preview("Tesla Climate Control") {
    struct ClimatePreview: View {
        @State private var climateData = TeslaClimateData.preview

        var body: some View {
            ScrollView {
                TeslaClimateControl(
                    climateData: $climateData,
                    onClimateToggle: { isOn in
                        print("Climate: \(isOn)")
                    },
                    onTemperatureChange: { temp in
                        print("Temperature: \(temp)")
                    }
                )
                .padding(24)
            }
            .background(TeslaColors.background)
        }
    }

    return ClimatePreview()
}
