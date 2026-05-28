// Tesla Dashboard UI - Vehicle Status
// 完全な車両ステータス表示
// 速度、バッテリー、航続距離、ドア状態

import SwiftUI

// MARK: - Tesla Vehicle Status

/// Tesla風車両ステータスビュー
/// ダッシュボードのメイン車両情報表示
struct TeslaVehicleStatus: View {
    // MARK: - Properties

    let vehicleData: VehicleData
    var showDetailedBattery: Bool = true
    var onDoorTap: ((String) -> Void)? = nil

    // MARK: - Environment

    @Environment(\.teslaTheme) private var theme
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    // MARK: - Body

    var body: some View {
        VStack(spacing: 24) {
            // Speed & Range Section
            speedAndRangeSection

            // Battery Section
            if showDetailedBattery {
                batterySection
            }

            // Door Status Section
            doorStatusSection
        }
        .padding(24)
        .teslaCard()
    }

    // MARK: - Speed & Range Section

    private var speedAndRangeSection: some View {
        HStack(spacing: 32) {
            // Speed
            VStack(spacing: 4) {
                HStack(alignment: .lastTextBaseline, spacing: 4) {
                    Text("\(Int(vehicleData.speed))")
                        .font(TeslaTypography.displayLarge)
                        .foregroundStyle(TeslaColors.textPrimary)
                        .monospacedDigit()
                        .contentTransition(.numericText())

                    Text("km/h")
                        .font(TeslaTypography.titleSmall)
                        .foregroundStyle(TeslaColors.textSecondary)
                }

                Text("速度")
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textTertiary)
            }

            Divider()
                .frame(height: 60)
                .background(TeslaColors.glassBorder)

            // Range
            VStack(spacing: 4) {
                HStack(alignment: .lastTextBaseline, spacing: 4) {
                    Text("\(Int(vehicleData.estimatedRange))")
                        .font(TeslaTypography.displayMedium)
                        .foregroundStyle(TeslaColors.textPrimary)
                        .monospacedDigit()
                        .contentTransition(.numericText())

                    Text("km")
                        .font(TeslaTypography.titleSmall)
                        .foregroundStyle(TeslaColors.textSecondary)
                }

                Text("航続距離")
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textTertiary)
            }

            Divider()
                .frame(height: 60)
                .background(TeslaColors.glassBorder)

            // Odometer
            VStack(spacing: 4) {
                Text(formattedOdometer)
                    .font(TeslaTypography.titleLarge)
                    .foregroundStyle(TeslaColors.textPrimary)
                    .monospacedDigit()

                Text("走行距離")
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textTertiary)
            }
        }
    }

    // MARK: - Battery Section

    private var batterySection: some View {
        VStack(spacing: 12) {
            // Battery Header
            HStack {
                TeslaIconView(icon: .battery, size: 18, color: TeslaColors.textSecondary)

                Text("バッテリー")
                    .font(TeslaTypography.titleSmall)
                    .foregroundStyle(TeslaColors.textSecondary)

                Spacer()

                // Charging Status
                if vehicleData.chargingState.isCharging {
                    HStack(spacing: 4) {
                        Image(systemName: "bolt.fill")
                            .font(.system(size: 12))
                            .foregroundStyle(TeslaColors.statusGreen)

                        Text("充電中")
                            .font(TeslaTypography.labelMedium)
                            .foregroundStyle(TeslaColors.statusGreen)

                        if let minutes = vehicleData.minutesToFullCharge {
                            Text("• \(minutes)分")
                                .font(TeslaTypography.labelMedium)
                                .foregroundStyle(TeslaColors.textSecondary)
                        }
                    }
                    .teslaPulse()
                }
            }

            // Battery Bar
            TeslaBatteryBar(
                level: vehicleData.batteryLevel,
                chargeLimit: vehicleData.chargeLimit,
                isCharging: vehicleData.chargingState.isCharging
            )

            // Battery Details
            HStack {
                // Battery Level
                Text("\(vehicleData.batteryLevel)%")
                    .font(TeslaTypography.titleMedium)
                    .foregroundStyle(batteryColor)

                Spacer()

                // Charge Rate (if charging)
                if vehicleData.chargingState.isCharging && vehicleData.chargeRate > 0 {
                    Text("\(String(format: "%.1f", vehicleData.chargeRate)) kW")
                        .font(TeslaTypography.labelMedium)
                        .foregroundStyle(TeslaColors.statusGreen)
                }

                // Charge Limit
                Text("上限: \(vehicleData.chargeLimit)%")
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textTertiary)
            }
        }
        .padding(16)
        .background(TeslaColors.glassBackground)
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }

    // MARK: - Door Status Section

    private var doorStatusSection: some View {
        VStack(spacing: 12) {
            // Header
            HStack {
                TeslaIconView(icon: .car, size: 18, color: TeslaColors.textSecondary)

                Text("ドア状態")
                    .font(TeslaTypography.titleSmall)
                    .foregroundStyle(TeslaColors.textSecondary)

                Spacer()

                // Lock Status
                HStack(spacing: 4) {
                    Image(systemName: vehicleData.isLocked ? "lock.fill" : "lock.open.fill")
                        .font(.system(size: 12))
                        .foregroundStyle(vehicleData.isLocked ? TeslaColors.statusGreen : TeslaColors.statusOrange)

                    Text(vehicleData.isLocked ? "ロック" : "アンロック")
                        .font(TeslaTypography.labelMedium)
                        .foregroundStyle(vehicleData.isLocked ? TeslaColors.statusGreen : TeslaColors.statusOrange)
                }
            }

            // Door Diagram
            TeslaDoorDiagram(
                doors: vehicleData.doors,
                onDoorTap: onDoorTap
            )
        }
        .padding(16)
        .background(TeslaColors.glassBackground)
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }

    // MARK: - Computed Properties

    private var formattedOdometer: String {
        let formatter = NumberFormatter()
        formatter.numberStyle = .decimal
        formatter.maximumFractionDigits = 0
        return "\(formatter.string(from: NSNumber(value: vehicleData.odometer)) ?? "0") km"
    }

    private var batteryColor: Color {
        switch vehicleData.batteryLevel {
        case 0..<20: return TeslaColors.statusRed
        case 20..<50: return TeslaColors.statusOrange
        default: return TeslaColors.statusGreen
        }
    }
}

// MARK: - Tesla Battery Bar

/// バッテリーバー表示
struct TeslaBatteryBar: View {
    let level: Int
    var chargeLimit: Int = 100
    var isCharging: Bool = false

    var body: some View {
        GeometryReader { geometry in
            ZStack(alignment: .leading) {
                // Background
                RoundedRectangle(cornerRadius: 4)
                    .fill(TeslaColors.glassBackground)

                // Battery Fill
                RoundedRectangle(cornerRadius: 4)
                    .fill(batteryGradient)
                    .frame(width: geometry.size.width * CGFloat(level) / 100)

                // Charge Limit Marker
                if chargeLimit < 100 {
                    Rectangle()
                        .fill(TeslaColors.textSecondary)
                        .frame(width: 2)
                        .offset(x: geometry.size.width * CGFloat(chargeLimit) / 100 - 1)
                }
            }
        }
        .frame(height: 16)
        .accessibilityLabel("バッテリー \(level)パーセント")
    }

    private var batteryGradient: LinearGradient {
        let color: Color = {
            if isCharging {
                return TeslaColors.statusGreen
            }
            switch level {
            case 0..<20: return TeslaColors.statusRed
            case 20..<50: return TeslaColors.statusOrange
            default: return TeslaColors.statusGreen
            }
        }()

        return LinearGradient(
            colors: [color.opacity(0.8), color],
            startPoint: .leading,
            endPoint: .trailing
        )
    }
}

// MARK: - Tesla Door Diagram

/// ドア状態ダイアグラム
struct TeslaDoorDiagram: View {
    let doors: DoorStatus
    var onDoorTap: ((String) -> Void)? = nil

    var body: some View {
        HStack(spacing: 24) {
            // Front View
            VStack(spacing: 8) {
                Text("前方")
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textTertiary)

                HStack(spacing: 16) {
                    doorIndicator(isOpen: doors.driverFront, label: "運転席", id: "driver_front")
                    doorIndicator(isOpen: doors.passengerFront, label: "助手席", id: "passenger_front")
                }
            }

            Divider()
                .frame(height: 60)
                .background(TeslaColors.glassBorder)

            // Rear View
            VStack(spacing: 8) {
                Text("後方")
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textTertiary)

                HStack(spacing: 16) {
                    doorIndicator(isOpen: doors.driverRear, label: "左後部", id: "driver_rear")
                    doorIndicator(isOpen: doors.passengerRear, label: "右後部", id: "passenger_rear")
                }
            }

            Divider()
                .frame(height: 60)
                .background(TeslaColors.glassBorder)

            // Trunk View
            VStack(spacing: 8) {
                Text("トランク")
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textTertiary)

                HStack(spacing: 16) {
                    doorIndicator(isOpen: doors.frunk, label: "フランク", id: "frunk")
                    doorIndicator(isOpen: doors.trunk, label: "トランク", id: "trunk")
                }
            }
        }
    }

    private func doorIndicator(isOpen: Bool, label: String, id: String) -> some View {
        Button {
            onDoorTap?(id)
        } label: {
            VStack(spacing: 4) {
                RoundedRectangle(cornerRadius: 4)
                    .fill(isOpen ? TeslaColors.statusOrange : TeslaColors.statusGreen)
                    .frame(width: 24, height: 32)
                    .overlay(
                        RoundedRectangle(cornerRadius: 4)
                            .stroke(isOpen ? TeslaColors.statusOrange : TeslaColors.statusGreen.opacity(0.5), lineWidth: 1)
                    )

                Text(label)
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textTertiary)
            }
        }
        .buttonStyle(TeslaScaleButtonStyle())
        .accessibilityLabel("\(label) \(isOpen ? "開いています" : "閉じています")")
    }
}

// MARK: - Compact Vehicle Status

/// コンパクト車両ステータス（ナビモード用）
struct TeslaCompactVehicleStatus: View {
    let vehicleData: VehicleData

    var body: some View {
        HStack(spacing: 16) {
            // Speed
            HStack(alignment: .lastTextBaseline, spacing: 2) {
                Text("\(Int(vehicleData.speed))")
                    .font(TeslaTypography.displaySmall)
                    .foregroundStyle(TeslaColors.textPrimary)
                    .monospacedDigit()

                Text("km/h")
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textSecondary)
            }

            Divider()
                .frame(height: 30)
                .background(TeslaColors.glassBorder)

            // Range
            HStack(spacing: 4) {
                TeslaIconView(icon: .battery, size: 14, color: TeslaColors.textSecondary)

                Text("\(Int(vehicleData.estimatedRange)) km")
                    .font(TeslaTypography.labelMedium)
                    .foregroundStyle(TeslaColors.textSecondary)
            }
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 8)
        .background(TeslaColors.glassBackground)
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}

// MARK: - Preview

#Preview("Tesla Vehicle Status") {
    ScrollView {
        VStack(spacing: 24) {
            // Full Status
            TeslaVehicleStatus(vehicleData: .preview)

            // Charging Status
            TeslaVehicleStatus(vehicleData: .chargingPreview)

            // Driving Status
            TeslaVehicleStatus(vehicleData: .drivingPreview)

            // Compact Status
            TeslaCompactVehicleStatus(vehicleData: .preview)
        }
        .padding(24)
    }
    .background(TeslaColors.background)
}
