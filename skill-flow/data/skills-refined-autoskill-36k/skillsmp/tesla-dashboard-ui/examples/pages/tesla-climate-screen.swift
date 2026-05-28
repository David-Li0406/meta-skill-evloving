// Tesla Dashboard UI - Climate Screen
// 空調画面
// 詳細な空調コントロールと可視化

import SwiftUI

// MARK: - Tesla Climate Screen

/// Tesla風空調画面
struct TeslaClimateScreen: View {
    // MARK: - Properties

    @Binding var vehicleData: VehicleData

    // MARK: - State

    @State private var climateData = TeslaClimateData.preview
    @State private var selectedZone: ClimateZone = .all
    @State private var showSchedule: Bool = false

    // MARK: - Environment

    @Environment(\.teslaTheme) private var theme
    @Environment(\.horizontalSizeClass) private var horizontalSizeClass

    // MARK: - Body

    var body: some View {
        ScrollView {
            if horizontalSizeClass == .regular {
                // iPad: Grid layout
                LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 24) {
                    // Climate Control
                    TeslaClimateControl(
                        climateData: $climateData,
                        onClimateToggle: { isOn in
                            vehicleData.isClimateOn = isOn
                        },
                        onTemperatureChange: { temp in
                            vehicleData.targetTemperature = temp
                        }
                    )
                    .gridCellColumns(2)

                    // Cabin Visualization
                    cabinVisualization

                    // Zone Selector
                    zoneSelector

                    // Air Flow Controls
                    airFlowControls

                    // Schedule
                    scheduleSection
                }
                .padding(24)
            } else {
                // iPhone: Stack layout
                VStack(spacing: 24) {
                    TeslaClimateControl(
                        climateData: $climateData,
                        onClimateToggle: { isOn in
                            vehicleData.isClimateOn = isOn
                        }
                    )

                    cabinVisualization
                    zoneSelector
                    airFlowControls
                    scheduleSection
                }
                .padding(24)
            }
        }
        .background(TeslaColors.background)
        .onChange(of: climateData.isClimateOn) { _, newValue in
            vehicleData.isClimateOn = newValue
        }
    }

    // MARK: - Cabin Visualization

    private var cabinVisualization: some View {
        TeslaCardLayout(title: "車内温度分布") {
            GeometryReader { geometry in
                ZStack {
                    // Car outline
                    RoundedRectangle(cornerRadius: 20)
                        .stroke(TeslaColors.glassBorder, lineWidth: 2)

                    // Temperature zones
                    HStack(spacing: 0) {
                        // Driver side
                        VStack(spacing: 0) {
                            temperatureZone(
                                temp: climateData.driverTemperature,
                                label: "運転席",
                                isSelected: selectedZone == .driverFront || selectedZone == .all
                            )
                            temperatureZone(
                                temp: climateData.driverTemperature - 1,
                                label: "左後部",
                                isSelected: selectedZone == .driverRear || selectedZone == .all
                            )
                        }

                        Divider()
                            .background(TeslaColors.glassBorder)

                        // Passenger side
                        VStack(spacing: 0) {
                            temperatureZone(
                                temp: climateData.passengerTemperature,
                                label: "助手席",
                                isSelected: selectedZone == .passengerFront || selectedZone == .all
                            )
                            temperatureZone(
                                temp: climateData.passengerTemperature - 1,
                                label: "右後部",
                                isSelected: selectedZone == .passengerRear || selectedZone == .all
                            )
                        }
                    }
                }
            }
            .frame(height: 200)
        }
    }

    private func temperatureZone(temp: Double, label: String, isSelected: Bool) -> some View {
        VStack(spacing: 4) {
            Text(String(format: "%.1f°", temp))
                .font(TeslaTypography.titleMedium)
                .foregroundStyle(isSelected ? TeslaColors.accent : TeslaColors.textSecondary)

            Text(label)
                .font(TeslaTypography.labelSmall)
                .foregroundStyle(TeslaColors.textTertiary)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(temperatureColor(for: temp).opacity(isSelected ? 0.3 : 0.1))
    }

    private func temperatureColor(for temp: Double) -> Color {
        if temp < 20 {
            return TeslaColors.accent
        } else if temp > 24 {
            return TeslaColors.statusOrange
        } else {
            return TeslaColors.statusGreen
        }
    }

    // MARK: - Zone Selector

    private var zoneSelector: some View {
        TeslaCardLayout(title: "ゾーン選択") {
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 12) {
                    ForEach(ClimateZone.allCases) { zone in
                        Button {
                            withAnimation(TeslaAnimation.quick) {
                                selectedZone = zone
                            }
                        } label: {
                            VStack(spacing: 8) {
                                Image(systemName: zone.iconName)
                                    .font(.system(size: 20))
                                    .foregroundStyle(selectedZone == zone ? .white : TeslaColors.textSecondary)
                                    .frame(width: 48, height: 48)
                                    .background(
                                        selectedZone == zone ? TeslaColors.accent : TeslaColors.glassBackground
                                    )
                                    .clipShape(Circle())

                                Text(zone.displayName)
                                    .font(TeslaTypography.labelSmall)
                                    .foregroundStyle(selectedZone == zone ? TeslaColors.accent : TeslaColors.textSecondary)
                            }
                        }
                        .buttonStyle(TeslaScaleButtonStyle())
                    }
                }
            }
        }
    }

    // MARK: - Air Flow Controls

    private var airFlowControls: some View {
        TeslaCardLayout(title: "エアフロー") {
            VStack(spacing: 16) {
                // Air Direction
                HStack {
                    Text("吹き出し口")
                        .font(TeslaTypography.labelMedium)
                        .foregroundStyle(TeslaColors.textSecondary)

                    Spacer()
                }

                HStack(spacing: 12) {
                    airFlowButton(icon: "person.fill", label: "顔", isSelected: true)
                    airFlowButton(icon: "figure.stand", label: "体", isSelected: true)
                    airFlowButton(icon: "shoe.fill", label: "足元", isSelected: false)
                }

                Divider()
                    .background(TeslaColors.glassBorder)

                // Air Intake
                HStack(spacing: 16) {
                    TeslaToggle("内気循環", icon: .fan, isOn: $climateData.isRecirculationOn)
                }
            }
        }
    }

    private func airFlowButton(icon: String, label: String, isSelected: Bool) -> some View {
        Button {
            // Toggle air flow
        } label: {
            VStack(spacing: 8) {
                Image(systemName: icon)
                    .font(.system(size: 16))
                    .foregroundStyle(isSelected ? .white : TeslaColors.textSecondary)
                    .frame(width: 44, height: 44)
                    .background(
                        isSelected ? TeslaColors.accent : TeslaColors.glassBackground
                    )
                    .clipShape(Circle())

                Text(label)
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(isSelected ? TeslaColors.accent : TeslaColors.textSecondary)
            }
        }
        .buttonStyle(TeslaScaleButtonStyle())
    }

    // MARK: - Schedule Section

    private var scheduleSection: some View {
        TeslaCardLayout(title: "スケジュール") {
            VStack(spacing: 16) {
                // Preconditioning
                HStack {
                    VStack(alignment: .leading, spacing: 4) {
                        Text("出発前プリコンディショニング")
                            .font(TeslaTypography.bodyMedium)
                            .foregroundStyle(TeslaColors.textPrimary)

                        Text("設定時刻に合わせて車内を快適にします")
                            .font(TeslaTypography.labelSmall)
                            .foregroundStyle(TeslaColors.textSecondary)
                    }

                    Spacer()

                    Toggle("", isOn: $climateData.isPreconditioningEnabled)
                        .toggleStyle(.tesla)
                }

                if climateData.isPreconditioningEnabled {
                    Divider()
                        .background(TeslaColors.glassBorder)

                    // Schedule Settings
                    Button {
                        showSchedule = true
                    } label: {
                        HStack {
                            Image(systemName: "clock")
                                .font(.system(size: 16))
                                .foregroundStyle(TeslaColors.accent)

                            VStack(alignment: .leading, spacing: 2) {
                                Text("平日")
                                    .font(TeslaTypography.labelMedium)
                                    .foregroundStyle(TeslaColors.textPrimary)

                                Text("7:30 出発")
                                    .font(TeslaTypography.bodyMedium)
                                    .foregroundStyle(TeslaColors.textSecondary)
                            }

                            Spacer()

                            Image(systemName: "chevron.right")
                                .font(.system(size: 14))
                                .foregroundStyle(TeslaColors.textTertiary)
                        }
                        .padding(12)
                        .background(TeslaColors.glassBackground)
                        .clipShape(RoundedRectangle(cornerRadius: 8))
                    }
                }
            }
        }
    }
}

// MARK: - Climate Zone

/// 空調ゾーン
enum ClimateZone: String, CaseIterable, Identifiable {
    case all = "all"
    case driverFront = "driver_front"
    case passengerFront = "passenger_front"
    case driverRear = "driver_rear"
    case passengerRear = "passenger_rear"

    var id: String { rawValue }

    var displayName: String {
        switch self {
        case .all: return "全体"
        case .driverFront: return "運転席"
        case .passengerFront: return "助手席"
        case .driverRear: return "左後部"
        case .passengerRear: return "右後部"
        }
    }

    var iconName: String {
        switch self {
        case .all: return "car.fill"
        case .driverFront: return "person.fill"
        case .passengerFront: return "person.fill"
        case .driverRear: return "person.2.fill"
        case .passengerRear: return "person.2.fill"
        }
    }
}

// MARK: - Preview

#Preview("Tesla Climate Screen") {
    struct ClimateScreenPreview: View {
        @State private var vehicleData = VehicleData.preview

        var body: some View {
            TeslaClimateScreen(vehicleData: $vehicleData)
        }
    }

    return ClimateScreenPreview()
        .teslaTheme()
}
