// Tesla Dashboard UI - Vehicle Screen
// 車両情報画面
// 完全な車両ステータス、コントロール、統計

import SwiftUI

// MARK: - Tesla Vehicle Screen

/// Tesla風車両情報画面
struct TeslaVehicleScreen: View {
    // MARK: - Properties

    let vehicleData: VehicleData
    let vehicleProvider: VehicleDataProvider

    // MARK: - State

    @State private var selectedSection: VehicleSection = .status
    @State private var isLoading: Bool = false
    @State private var error: TeslaError?

    // MARK: - Environment

    @Environment(\.teslaTheme) private var theme
    @Environment(\.horizontalSizeClass) private var horizontalSizeClass

    // MARK: - Body

    var body: some View {
        VStack(spacing: 0) {
            // Section Selector
            sectionSelector

            // Content
            ScrollView {
                switch selectedSection {
                case .status:
                    statusSection
                case .controls:
                    controlsSection
                case .charging:
                    chargingSection
                case .stats:
                    statsSection
                }
            }
        }
        .background(TeslaColors.background)
        .alert("エラー", isPresented: .constant(error != nil)) {
            Button("OK") { error = nil }
        } message: {
            Text(error?.localizedDescription ?? "")
        }
    }

    // MARK: - Section Selector

    private var sectionSelector: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 8) {
                ForEach(VehicleSection.allCases) { section in
                    Button {
                        withAnimation(TeslaAnimation.quick) {
                            selectedSection = section
                        }
                    } label: {
                        HStack(spacing: 8) {
                            Image(systemName: section.iconName)
                                .font(.system(size: 14))

                            Text(section.displayName)
                                .font(TeslaTypography.labelMedium)
                        }
                        .foregroundStyle(selectedSection == section ? .white : TeslaColors.textSecondary)
                        .padding(.horizontal, 16)
                        .padding(.vertical, 10)
                        .background(
                            RoundedRectangle(cornerRadius: 8)
                                .fill(selectedSection == section ? TeslaColors.accent : TeslaColors.glassBackground)
                        )
                    }
                    .buttonStyle(TeslaScaleButtonStyle())
                }
            }
            .padding(16)
        }
        .background(TeslaColors.surface)
    }

    // MARK: - Status Section

    private var statusSection: some View {
        VStack(spacing: 24) {
            // Full Vehicle Status
            TeslaVehicleStatus(
                vehicleData: vehicleData,
                showDetailedBattery: true,
                onDoorTap: { doorId in
                    handleDoorTap(doorId)
                }
            )

            // Vehicle Info Card
            TeslaCardLayout(title: "車両情報") {
                VStack(spacing: 16) {
                    infoRow(label: "モデル", value: vehicleData.model)
                    infoRow(label: "ソフトウェア", value: "2024.12.1")
                    infoRow(label: "VIN", value: "5YJ3E1EA1LF000001")
                    infoRow(label: "最終更新", value: formattedLastUpdate)
                }
            }

            // Location Card
            TeslaCardLayout(title: "現在地") {
                HStack {
                    Image(systemName: "location.fill")
                        .font(.system(size: 20))
                        .foregroundStyle(TeslaColors.accent)

                    VStack(alignment: .leading, spacing: 4) {
                        Text("東京都千代田区丸の内1-1-1")
                            .font(TeslaTypography.bodyMedium)
                            .foregroundStyle(TeslaColors.textPrimary)

                        Text("最終更新: \(formattedLastUpdate)")
                            .font(TeslaTypography.labelSmall)
                            .foregroundStyle(TeslaColors.textTertiary)
                    }

                    Spacer()

                    Button {
                        // Open in Maps
                    } label: {
                        Image(systemName: "map")
                            .font(.system(size: 16))
                            .foregroundStyle(TeslaColors.accent)
                            .frame(width: 36, height: 36)
                            .background(TeslaColors.glassBackground)
                            .clipShape(Circle())
                    }
                }
            }
        }
        .padding(24)
    }

    private func infoRow(label: String, value: String) -> some View {
        HStack {
            Text(label)
                .font(TeslaTypography.labelMedium)
                .foregroundStyle(TeslaColors.textSecondary)

            Spacer()

            Text(value)
                .font(TeslaTypography.bodyMedium)
                .foregroundStyle(TeslaColors.textPrimary)
        }
    }

    // MARK: - Controls Section

    private var controlsSection: some View {
        VStack(spacing: 24) {
            // Security Controls
            TeslaCardLayout(title: "セキュリティ") {
                VStack(spacing: 16) {
                    controlButton(
                        icon: vehicleData.isLocked ? "lock.fill" : "lock.open.fill",
                        label: vehicleData.isLocked ? "ロック中" : "アンロック中",
                        isActive: vehicleData.isLocked,
                        action: {
                            await toggleLock()
                        }
                    )

                    Divider().background(TeslaColors.glassBorder)

                    HStack(spacing: 16) {
                        quickControlButton(icon: "light.beacon.max.fill", label: "ライト点滅") {
                            await flashLights()
                        }

                        quickControlButton(icon: "speaker.wave.2.fill", label: "ホーン") {
                            await honkHorn()
                        }
                    }
                }
            }

            // Trunk Controls
            TeslaCardLayout(title: "トランク") {
                HStack(spacing: 24) {
                    trunkButton(
                        label: "フランク",
                        isOpen: vehicleData.doors.frunk,
                        action: { await openTrunk(.front) }
                    )

                    Divider()
                        .frame(height: 60)
                        .background(TeslaColors.glassBorder)

                    trunkButton(
                        label: "トランク",
                        isOpen: vehicleData.doors.trunk,
                        action: { await openTrunk(.rear) }
                    )
                }
            }

            // Remote Start
            TeslaCardLayout(title: "リモートスタート") {
                HStack {
                    VStack(alignment: .leading, spacing: 4) {
                        Text("リモートスタート")
                            .font(TeslaTypography.bodyMedium)
                            .foregroundStyle(TeslaColors.textPrimary)

                        Text("2分間エンジンを始動します")
                            .font(TeslaTypography.labelSmall)
                            .foregroundStyle(TeslaColors.textSecondary)
                    }

                    Spacer()

                    Button {
                        // Remote start
                    } label: {
                        Text("開始")
                            .font(TeslaTypography.labelMedium)
                            .foregroundStyle(.white)
                            .padding(.horizontal, 24)
                            .padding(.vertical, 12)
                            .background(TeslaColors.accent)
                            .clipShape(RoundedRectangle(cornerRadius: 8))
                    }
                    .buttonStyle(TeslaScaleButtonStyle())
                }
            }
        }
        .padding(24)
    }

    private func controlButton(icon: String, label: String, isActive: Bool, action: @escaping () async -> Void) -> some View {
        Button {
            Task {
                isLoading = true
                await action()
                isLoading = false
            }
        } label: {
            HStack {
                Image(systemName: icon)
                    .font(.system(size: 24))
                    .foregroundStyle(isActive ? TeslaColors.statusGreen : TeslaColors.textSecondary)
                    .frame(width: 48, height: 48)
                    .background(TeslaColors.glassBackground)
                    .clipShape(Circle())

                Text(label)
                    .font(TeslaTypography.titleMedium)
                    .foregroundStyle(TeslaColors.textPrimary)

                Spacer()

                if isLoading {
                    ProgressView()
                        .tint(TeslaColors.accent)
                } else {
                    Image(systemName: "chevron.right")
                        .font(.system(size: 14))
                        .foregroundStyle(TeslaColors.textTertiary)
                }
            }
        }
        .disabled(isLoading)
    }

    private func quickControlButton(icon: String, label: String, action: @escaping () async -> Void) -> some View {
        Button {
            Task { await action() }
        } label: {
            VStack(spacing: 8) {
                Image(systemName: icon)
                    .font(.system(size: 20))
                    .foregroundStyle(TeslaColors.textSecondary)
                    .frame(width: 56, height: 56)
                    .background(TeslaColors.glassBackground)
                    .clipShape(Circle())

                Text(label)
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textSecondary)
            }
        }
        .buttonStyle(TeslaScaleButtonStyle())
    }

    private func trunkButton(label: String, isOpen: Bool, action: @escaping () async -> Void) -> some View {
        Button {
            Task { await action() }
        } label: {
            VStack(spacing: 12) {
                Image(systemName: "car.rear.fill")
                    .font(.system(size: 32))
                    .foregroundStyle(isOpen ? TeslaColors.statusOrange : TeslaColors.textSecondary)

                Text(label)
                    .font(TeslaTypography.labelMedium)
                    .foregroundStyle(TeslaColors.textPrimary)

                Text(isOpen ? "開いています" : "閉じています")
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(isOpen ? TeslaColors.statusOrange : TeslaColors.statusGreen)
            }
            .frame(maxWidth: .infinity)
        }
        .buttonStyle(TeslaScaleButtonStyle())
    }

    // MARK: - Charging Section

    private var chargingSection: some View {
        VStack(spacing: 24) {
            // Charging Status
            TeslaCardLayout(title: "充電状態") {
                VStack(spacing: 16) {
                    // Battery
                    TeslaBatteryBar(
                        level: vehicleData.batteryLevel,
                        chargeLimit: vehicleData.chargeLimit,
                        isCharging: vehicleData.chargingState.isCharging
                    )

                    HStack {
                        VStack(alignment: .leading, spacing: 4) {
                            Text("\(vehicleData.batteryLevel)%")
                                .font(TeslaTypography.displaySmall)
                                .foregroundStyle(TeslaColors.textPrimary)

                            Text("充電上限: \(vehicleData.chargeLimit)%")
                                .font(TeslaTypography.labelSmall)
                                .foregroundStyle(TeslaColors.textSecondary)
                        }

                        Spacer()

                        VStack(alignment: .trailing, spacing: 4) {
                            Text("\(Int(vehicleData.estimatedRange)) km")
                                .font(TeslaTypography.titleLarge)
                                .foregroundStyle(TeslaColors.textPrimary)

                            Text("航続距離")
                                .font(TeslaTypography.labelSmall)
                                .foregroundStyle(TeslaColors.textSecondary)
                        }
                    }
                }
            }

            // Charging Controls
            TeslaCardLayout(title: "充電設定") {
                VStack(spacing: 16) {
                    // Charge Limit Slider
                    VStack(alignment: .leading, spacing: 8) {
                        Text("充電上限")
                            .font(TeslaTypography.labelMedium)
                            .foregroundStyle(TeslaColors.textSecondary)

                        TeslaSlider(
                            value: .constant(Double(vehicleData.chargeLimit) / 100),
                            range: 0.5...1.0,
                            valueFormatter: { "\(Int($0 * 100))%" }
                        )
                    }

                    Divider().background(TeslaColors.glassBorder)

                    // Start/Stop Charging
                    if vehicleData.chargingState.isConnected {
                        Button {
                            Task {
                                _ = await vehicleProvider.setCharging(!vehicleData.chargingState.isCharging)
                            }
                        } label: {
                            HStack {
                                Image(systemName: vehicleData.chargingState.isCharging ? "pause.fill" : "play.fill")
                                Text(vehicleData.chargingState.isCharging ? "充電を停止" : "充電を開始")
                            }
                            .font(TeslaTypography.labelMedium)
                            .foregroundStyle(.white)
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 14)
                            .background(vehicleData.chargingState.isCharging ? TeslaColors.statusOrange : TeslaColors.statusGreen)
                            .clipShape(RoundedRectangle(cornerRadius: 8))
                        }
                        .buttonStyle(TeslaScaleButtonStyle())
                    }
                }
            }

            // Nearby Chargers
            TeslaCardLayout(title: "近くの充電スポット") {
                VStack(spacing: 12) {
                    chargerRow(name: "Tesla 東京ベイ", distance: "2.3 km", available: 4, total: 8)
                    chargerRow(name: "Tesla 新宿", distance: "5.1 km", available: 2, total: 6)
                    chargerRow(name: "Tesla 渋谷", distance: "6.8 km", available: 6, total: 8)
                }
            }
        }
        .padding(24)
    }

    private func chargerRow(name: String, distance: String, available: Int, total: Int) -> some View {
        HStack {
            Image(systemName: "bolt.fill")
                .font(.system(size: 16))
                .foregroundStyle(TeslaColors.statusGreen)
                .frame(width: 36, height: 36)
                .background(TeslaColors.glassBackground)
                .clipShape(Circle())

            VStack(alignment: .leading, spacing: 2) {
                Text(name)
                    .font(TeslaTypography.bodyMedium)
                    .foregroundStyle(TeslaColors.textPrimary)

                Text(distance)
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textSecondary)
            }

            Spacer()

            Text("\(available)/\(total) 空き")
                .font(TeslaTypography.labelMedium)
                .foregroundStyle(available > 0 ? TeslaColors.statusGreen : TeslaColors.statusRed)
        }
        .padding(12)
        .background(TeslaColors.glassBackground)
        .clipShape(RoundedRectangle(cornerRadius: 8))
    }

    // MARK: - Stats Section

    private var statsSection: some View {
        VStack(spacing: 24) {
            // Energy Stats
            TeslaCardLayout(title: "エネルギー統計") {
                let stats = TeslaEnergyStats.preview

                VStack(spacing: 16) {
                    HStack {
                        statItem(value: stats.formattedDistance, label: "走行距離")
                        Divider().frame(height: 40).background(TeslaColors.glassBorder)
                        statItem(value: stats.formattedEfficiency, label: "平均電費")
                        Divider().frame(height: 40).background(TeslaColors.glassBorder)
                        statItem(value: stats.formattedEnergyConsumed, label: "消費電力")
                    }
                }
            }

            // Trip History
            TeslaCardLayout(title: "最近の走行") {
                VStack(spacing: 12) {
                    ForEach(TeslaTripHistory.previewList) { trip in
                        tripRow(trip: trip)
                    }
                }
            }
        }
        .padding(24)
    }

    private func statItem(value: String, label: String) -> some View {
        VStack(spacing: 4) {
            Text(value)
                .font(TeslaTypography.titleMedium)
                .foregroundStyle(TeslaColors.textPrimary)

            Text(label)
                .font(TeslaTypography.labelSmall)
                .foregroundStyle(TeslaColors.textTertiary)
        }
        .frame(maxWidth: .infinity)
    }

    private func tripRow(trip: TeslaTripHistory) -> some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(trip.displayName)
                    .font(TeslaTypography.bodyMedium)
                    .foregroundStyle(TeslaColors.textPrimary)
                    .lineLimit(1)

                Text(trip.formattedDate)
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textTertiary)
            }

            Spacer()

            VStack(alignment: .trailing, spacing: 4) {
                Text(trip.formattedDistance)
                    .font(TeslaTypography.labelMedium)
                    .foregroundStyle(TeslaColors.textPrimary)

                Text(trip.formattedBatteryUsed)
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textSecondary)
            }
        }
        .padding(12)
        .background(TeslaColors.glassBackground)
        .clipShape(RoundedRectangle(cornerRadius: 8))
    }

    // MARK: - Computed Properties

    private var formattedLastUpdate: String {
        let formatter = DateFormatter()
        formatter.dateFormat = "HH:mm"
        return formatter.string(from: vehicleData.lastUpdated)
    }

    // MARK: - Actions

    private func handleDoorTap(_ doorId: String) {
        // Handle door tap
    }

    private func toggleLock() async {
        let result = await vehicleProvider.setDoorLock(!vehicleData.isLocked)
        if case .failure(let err) = result {
            error = err
        }
    }

    private func flashLights() async {
        let result = await vehicleProvider.flashLights()
        if case .failure(let err) = result {
            error = err
        }
    }

    private func honkHorn() async {
        let result = await vehicleProvider.honkHorn()
        if case .failure(let err) = result {
            error = err
        }
    }

    private func openTrunk(_ trunk: TrunkType) async {
        let result = await vehicleProvider.openTrunk(trunk)
        if case .failure(let err) = result {
            error = err
        }
    }
}

// MARK: - Vehicle Section

/// 車両画面セクション
enum VehicleSection: String, CaseIterable, Identifiable {
    case status = "status"
    case controls = "controls"
    case charging = "charging"
    case stats = "stats"

    var id: String { rawValue }

    var displayName: String {
        switch self {
        case .status: return "ステータス"
        case .controls: return "コントロール"
        case .charging: return "充電"
        case .stats: return "統計"
        }
    }

    var iconName: String {
        switch self {
        case .status: return "car.fill"
        case .controls: return "slider.horizontal.3"
        case .charging: return "bolt.fill"
        case .stats: return "chart.bar.fill"
        }
    }
}

// MARK: - Preview

#Preview("Tesla Vehicle Screen") {
    TeslaVehicleScreen(
        vehicleData: .preview,
        vehicleProvider: MockVehicleDataProvider()
    )
    .teslaTheme()
}
