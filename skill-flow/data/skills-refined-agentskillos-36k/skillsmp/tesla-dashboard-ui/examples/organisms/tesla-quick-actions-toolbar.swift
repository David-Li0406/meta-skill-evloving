// Tesla Dashboard UI - Quick Actions Toolbar
// クイックアクションツールバー
// 9項目 + 2ドライブモード対応

import SwiftUI

// MARK: - Tesla Quick Actions Toolbar

/// Tesla風クイックアクションツールバー
/// 頻繁に使用する機能への素早いアクセス
struct TeslaQuickActionsToolbar: View {
    // MARK: - Properties

    @Binding var vehicleData: VehicleData
    var onAction: ((QuickAction) -> Void)? = nil

    // MARK: - Environment

    @Environment(\.teslaTheme) private var theme
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    // MARK: - State

    @State private var selectedDriveMode: DriveMode

    // MARK: - Initialization

    init(vehicleData: Binding<VehicleData>, onAction: ((QuickAction) -> Void)? = nil) {
        self._vehicleData = vehicleData
        self.onAction = onAction
        self._selectedDriveMode = State(initialValue: vehicleData.wrappedValue.driveMode)
    }

    // MARK: - Body

    var body: some View {
        VStack(spacing: 16) {
            // Drive Mode Selector
            driveModeSelector

            // Quick Actions Grid
            quickActionsGrid
        }
        .padding(16)
        .teslaCard()
    }

    // MARK: - Drive Mode Selector

    private var driveModeSelector: some View {
        HStack(spacing: 12) {
            ForEach(DriveMode.allCases, id: \.self) { mode in
                Button {
                    withAnimation(reduceMotion ? .none : TeslaAnimation.quick) {
                        selectedDriveMode = mode
                        vehicleData.driveMode = mode
                    }
                    onAction?(.driveMode(mode))
                } label: {
                    HStack(spacing: 8) {
                        TeslaIconView(
                            icon: mode.icon,
                            size: 16,
                            color: selectedDriveMode == mode ? .white : TeslaColors.textSecondary
                        )

                        Text(mode.displayName)
                            .font(TeslaTypography.labelMedium)
                            .foregroundStyle(selectedDriveMode == mode ? .white : TeslaColors.textSecondary)
                    }
                    .padding(.horizontal, 16)
                    .padding(.vertical, 10)
                    .background(
                        RoundedRectangle(cornerRadius: 8)
                            .fill(selectedDriveMode == mode ? TeslaColors.accent : TeslaColors.glassBackground)
                    )
                }
                .buttonStyle(TeslaScaleButtonStyle())
            }

            Spacer()
        }
    }

    // MARK: - Quick Actions Grid

    private var quickActionsGrid: some View {
        LazyVGrid(columns: Array(repeating: GridItem(.flexible(), spacing: 12), count: 5), spacing: 12) {
            ForEach(QuickAction.allCases) { action in
                quickActionButton(for: action)
            }
        }
    }

    private func quickActionButton(for action: QuickAction) -> some View {
        TeslaIconButton(
            icon: action.icon,
            label: action.label,
            isSelected: isActionActive(action),
            size: .medium
        ) {
            withAnimation(reduceMotion ? .none : TeslaAnimation.quick) {
                toggleAction(action)
            }
            onAction?(action)
        }
    }

    // MARK: - Action State

    private func isActionActive(_ action: QuickAction) -> Bool {
        switch action {
        case .lock:
            return vehicleData.isLocked
        case .climate:
            return vehicleData.isClimateOn
        case .defrost:
            return vehicleData.isDefrostOn
        case .seatHeater:
            return vehicleData.seatHeaterDriver > 0
        case .charging:
            return vehicleData.chargingState.isCharging
        default:
            return false
        }
    }

    private func toggleAction(_ action: QuickAction) {
        switch action {
        case .lock:
            vehicleData.isLocked.toggle()
        case .climate:
            vehicleData.isClimateOn.toggle()
        case .defrost:
            vehicleData.isDefrostOn.toggle()
        case .seatHeater:
            vehicleData.seatHeaterDriver = vehicleData.seatHeaterDriver > 0 ? 0 : 2
        case .charging:
            if vehicleData.chargingState.isConnected {
                vehicleData.chargingState = vehicleData.chargingState.isCharging ? .stopped : .charging
            }
        default:
            break
        }
    }
}

// MARK: - Quick Action

/// クイックアクション定義
enum QuickAction: String, CaseIterable, Identifiable {
    case lock = "lock"
    case unlock = "unlock"
    case climate = "climate"
    case defrost = "defrost"
    case seatHeater = "seat_heater"
    case frunk = "frunk"
    case trunk = "trunk"
    case lights = "lights"
    case horn = "horn"
    case charging = "charging"
    case camera = "camera"

    // Drive mode (associated value)
    case driveMode

    var id: String { rawValue }

    var label: String {
        switch self {
        case .lock: return "ロック"
        case .unlock: return "アンロック"
        case .climate: return "空調"
        case .defrost: return "デフロスト"
        case .seatHeater: return "シートヒーター"
        case .frunk: return "フランク"
        case .trunk: return "トランク"
        case .lights: return "ライト"
        case .horn: return "ホーン"
        case .charging: return "充電"
        case .camera: return "カメラ"
        case .driveMode: return "ドライブ"
        }
    }

    var icon: TeslaIcon {
        switch self {
        case .lock: return .lock
        case .unlock: return .unlock
        case .climate: return .climate
        case .defrost: return .defrost
        case .seatHeater: return .seatHeater
        case .frunk: return .frunk
        case .trunk: return .trunk
        case .lights: return .light
        case .horn: return .horn
        case .charging: return .charging
        case .camera: return .camera
        case .driveMode: return .car
        }
    }

    static var allCases: [QuickAction] {
        [.lock, .climate, .defrost, .seatHeater, .frunk, .trunk, .lights, .horn, .charging]
    }

    static func driveMode(_ mode: DriveMode) -> QuickAction {
        .driveMode
    }
}

// MARK: - Compact Quick Actions

/// コンパクトクイックアクション（横スクロール）
struct TeslaCompactQuickActions: View {
    @Binding var vehicleData: VehicleData
    var onAction: ((QuickAction) -> Void)? = nil

    var body: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 12) {
                ForEach(QuickAction.allCases.prefix(6)) { action in
                    TeslaIconButton(
                        icon: action.icon,
                        label: action.label,
                        isSelected: isActionActive(action),
                        size: .small
                    ) {
                        onAction?(action)
                    }
                }
            }
            .padding(.horizontal, 16)
        }
    }

    private func isActionActive(_ action: QuickAction) -> Bool {
        switch action {
        case .lock:
            return vehicleData.isLocked
        case .climate:
            return vehicleData.isClimateOn
        case .defrost:
            return vehicleData.isDefrostOn
        case .seatHeater:
            return vehicleData.seatHeaterDriver > 0
        case .charging:
            return vehicleData.chargingState.isCharging
        default:
            return false
        }
    }
}

// MARK: - Preview

#Preview("Tesla Quick Actions Toolbar") {
    struct QuickActionsPreview: View {
        @State private var vehicleData = VehicleData.preview

        var body: some View {
            VStack(spacing: 24) {
                // Full Toolbar
                TeslaQuickActionsToolbar(
                    vehicleData: $vehicleData,
                    onAction: { action in
                        print("Action: \(action.label)")
                    }
                )

                Divider()
                    .background(TeslaColors.glassBorder)

                // Compact Actions
                VStack(alignment: .leading, spacing: 12) {
                    Text("Compact Actions")
                        .font(TeslaTypography.titleSmall)
                        .foregroundStyle(TeslaColors.textPrimary)
                        .padding(.horizontal, 16)

                    TeslaCompactQuickActions(
                        vehicleData: $vehicleData,
                        onAction: { action in
                            print("Compact Action: \(action.label)")
                        }
                    )
                }

                Spacer()
            }
            .padding(.vertical, 24)
            .background(TeslaColors.background)
        }
    }

    return QuickActionsPreview()
}
