// Tesla Dashboard UI - Navigation Bar
// トップナビゲーションバー
// 時刻、接続状態、バッテリー表示

import SwiftUI

// MARK: - Tesla Navigation Bar

/// Tesla風ナビゲーションバー
/// ダッシュボード上部に表示される情報バー
struct TeslaNavigationBar: View {
    // MARK: - Properties

    let vehicleData: VehicleData
    var onSettingsTap: (() -> Void)? = nil

    // MARK: - Environment

    @Environment(\.teslaTheme) private var theme

    // MARK: - State

    @State private var currentTime = Date()

    // Timer for clock update
    private let timer = Timer.publish(every: 1, on: .main, in: .common).autoconnect()

    // MARK: - Body

    var body: some View {
        HStack(spacing: 16) {
            // Left: Time & Temperature
            leftSection

            Spacer()

            // Center: Vehicle Name & Status
            centerSection

            Spacer()

            // Right: Connection & Battery
            rightSection
        }
        .padding(.horizontal, 24)
        .padding(.vertical, 12)
        .background(TeslaColors.surface.opacity(0.8))
        .onReceive(timer) { _ in
            currentTime = Date()
        }
    }

    // MARK: - Left Section

    private var leftSection: some View {
        HStack(spacing: 16) {
            // Time
            Text(formattedTime)
                .font(TeslaTypography.titleLarge)
                .foregroundStyle(TeslaColors.textPrimary)
                .monospacedDigit()

            // Outside Temperature
            HStack(spacing: 4) {
                Image(systemName: "thermometer.medium")
                    .font(.system(size: 14))
                Text(formattedTemperature)
                    .font(TeslaTypography.bodyMedium)
            }
            .foregroundStyle(TeslaColors.textSecondary)
        }
    }

    // MARK: - Center Section

    private var centerSection: some View {
        VStack(spacing: 2) {
            // Vehicle Name
            Text(vehicleData.name)
                .font(TeslaTypography.titleMedium)
                .foregroundStyle(TeslaColors.textPrimary)

            // Status
            HStack(spacing: 6) {
                // Online Status
                Circle()
                    .fill(vehicleData.isOnline ? TeslaColors.statusGreen : TeslaColors.textTertiary)
                    .frame(width: 6, height: 6)

                Text(vehicleData.isOnline ? "オンライン" : "オフライン")
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textSecondary)

                // Drive Mode
                if vehicleData.speed > 0 {
                    Text("•")
                        .foregroundStyle(TeslaColors.textTertiary)

                    Text(vehicleData.driveMode.displayName)
                        .font(TeslaTypography.labelSmall)
                        .foregroundStyle(TeslaColors.accent)
                }
            }
        }
    }

    // MARK: - Right Section

    private var rightSection: some View {
        HStack(spacing: 16) {
            // Connection Icons
            connectionIcons

            // Battery
            batteryIndicator

            // Settings Button
            if let onSettingsTap {
                Button(action: onSettingsTap) {
                    Image(systemName: "gearshape.fill")
                        .font(.system(size: 18))
                        .foregroundStyle(TeslaColors.textSecondary)
                        .frame(width: 36, height: 36)
                }
                .buttonStyle(TeslaScaleButtonStyle())
            }
        }
    }

    // MARK: - Connection Icons

    private var connectionIcons: some View {
        HStack(spacing: 8) {
            // Bluetooth
            Image(systemName: "antenna.radiowaves.left.and.right")
                .font(.system(size: 14))
                .foregroundStyle(TeslaColors.textSecondary)

            // Cellular
            Image(systemName: "cellularbars")
                .font(.system(size: 14))
                .foregroundStyle(TeslaColors.textSecondary)

            // WiFi
            Image(systemName: "wifi")
                .font(.system(size: 14))
                .foregroundStyle(TeslaColors.textSecondary)
        }
    }

    // MARK: - Battery Indicator

    private var batteryIndicator: some View {
        HStack(spacing: 6) {
            // Battery Icon
            BatteryIconView(
                level: vehicleData.batteryLevel,
                isCharging: vehicleData.chargingState.isCharging
            )

            // Battery Percentage
            Text("\(vehicleData.batteryLevel)%")
                .font(TeslaTypography.titleSmall)
                .foregroundStyle(batteryColor)
                .monospacedDigit()
        }
    }

    // MARK: - Computed Properties

    private var formattedTime: String {
        let formatter = DateFormatter()
        formatter.dateFormat = "HH:mm"
        return formatter.string(from: currentTime)
    }

    private var formattedTemperature: String {
        String(format: "%.0f°C", vehicleData.exteriorTemperature)
    }

    private var batteryColor: Color {
        switch vehicleData.batteryLevel {
        case 0..<20: return TeslaColors.statusRed
        case 20..<50: return TeslaColors.statusOrange
        default: return TeslaColors.textPrimary
        }
    }
}

// MARK: - Battery Icon View

/// バッテリーアイコン
struct BatteryIconView: View {
    let level: Int
    var isCharging: Bool = false

    var body: some View {
        ZStack {
            // Battery Outline
            RoundedRectangle(cornerRadius: 3)
                .stroke(TeslaColors.textSecondary, lineWidth: 1.5)
                .frame(width: 28, height: 14)

            // Battery Cap
            Rectangle()
                .fill(TeslaColors.textSecondary)
                .frame(width: 2, height: 6)
                .offset(x: 15)

            // Battery Fill
            GeometryReader { geometry in
                RoundedRectangle(cornerRadius: 1.5)
                    .fill(batteryFillColor)
                    .frame(width: max(0, (geometry.size.width - 4) * CGFloat(level) / 100))
                    .padding(2)
            }
            .frame(width: 28, height: 14)

            // Charging Icon
            if isCharging {
                Image(systemName: "bolt.fill")
                    .font(.system(size: 8))
                    .foregroundStyle(TeslaColors.statusGreen)
            }
        }
    }

    private var batteryFillColor: Color {
        if isCharging {
            return TeslaColors.statusGreen
        }
        switch level {
        case 0..<20: return TeslaColors.statusRed
        case 20..<50: return TeslaColors.statusOrange
        default: return TeslaColors.statusGreen
        }
    }
}

// MARK: - Compact Navigation Bar

/// コンパクトナビゲーションバー（ナビ全画面モード用）
struct TeslaCompactNavigationBar: View {
    let vehicleData: VehicleData
    var onBackTap: (() -> Void)? = nil

    @State private var currentTime = Date()
    private let timer = Timer.publish(every: 1, on: .main, in: .common).autoconnect()

    var body: some View {
        HStack(spacing: 12) {
            // Back Button
            if let onBackTap {
                Button(action: onBackTap) {
                    Image(systemName: "chevron.left")
                        .font(.system(size: 16, weight: .semibold))
                        .foregroundStyle(TeslaColors.textPrimary)
                        .frame(width: 36, height: 36)
                        .background(TeslaColors.glassBackground)
                        .clipShape(Circle())
                }
                .buttonStyle(TeslaScaleButtonStyle())
            }

            Spacer()

            // Time
            Text(formattedTime)
                .font(TeslaTypography.titleSmall)
                .foregroundStyle(TeslaColors.textPrimary)
                .monospacedDigit()

            // Battery
            HStack(spacing: 4) {
                BatteryIconView(
                    level: vehicleData.batteryLevel,
                    isCharging: vehicleData.chargingState.isCharging
                )
                Text("\(vehicleData.batteryLevel)%")
                    .font(TeslaTypography.labelMedium)
                    .foregroundStyle(TeslaColors.textSecondary)
                    .monospacedDigit()
            }
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 8)
        .onReceive(timer) { _ in
            currentTime = Date()
        }
    }

    private var formattedTime: String {
        let formatter = DateFormatter()
        formatter.dateFormat = "HH:mm"
        return formatter.string(from: currentTime)
    }
}

// MARK: - Preview

#Preview("Tesla Navigation Bar") {
    VStack(spacing: 24) {
        // Standard Navigation Bar
        TeslaNavigationBar(
            vehicleData: .preview,
            onSettingsTap: { print("Settings tapped") }
        )

        Divider()
            .background(TeslaColors.glassBorder)

        // Compact Navigation Bar
        TeslaCompactNavigationBar(
            vehicleData: .preview,
            onBackTap: { print("Back tapped") }
        )
        .background(TeslaColors.surface.opacity(0.8))

        Divider()
            .background(TeslaColors.glassBorder)

        // Charging State
        TeslaNavigationBar(
            vehicleData: .chargingPreview
        )

        Spacer()
    }
    .background(TeslaColors.background)
}
