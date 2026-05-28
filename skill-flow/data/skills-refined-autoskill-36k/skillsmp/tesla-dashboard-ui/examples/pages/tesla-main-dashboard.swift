// Tesla Dashboard UI - Main Dashboard
// メインダッシュボード画面
// 車両ステータス、クイックアクション、ナビ、音楽の統合表示

import SwiftUI
import SwiftData

// MARK: - Tesla Main Dashboard

/// Tesla風メインダッシュボード
/// アプリのメイン画面
struct TeslaMainDashboard: View {
    // MARK: - Properties

    @StateObject private var vehicleProvider = MockVehicleDataProvider()
    @StateObject private var musicPlayer = TeslaMusicPlayer()
    @StateObject private var navigationManager = TeslaNavigationManager()

    // MARK: - State

    @State private var selectedTab: TeslaMenuTab = .navigation
    @State private var vehicleData: VehicleData = .preview
    @State private var showMusicExpanded = false
    @State private var layoutMode: TeslaLayoutMode = .split

    // MARK: - Environment

    @Environment(\.teslaTheme) private var theme
    @Environment(\.modelContext) private var modelContext

    // MARK: - Body

    var body: some View {
        VStack(spacing: 0) {
            // Navigation Bar
            TeslaNavigationBar(
                vehicleData: vehicleData,
                onSettingsTap: {
                    selectedTab = .settings
                }
            )

            // Main Content
            mainContent

            // Music Bar
            if selectedTab != .media {
                TeslaMusicBar(player: musicPlayer) {
                    withAnimation(TeslaAnimation.standard) {
                        showMusicExpanded = true
                    }
                }
                .padding(.horizontal, 16)
                .padding(.bottom, 8)
            }

            // Tab Menu
            TeslaTouchscreenMenu(
                selectedTab: $selectedTab,
                onTabChange: { tab in
                    handleTabChange(tab)
                }
            )
        }
        .background(TeslaColors.background)
        .sheet(isPresented: $showMusicExpanded) {
            TeslaExpandedMusicView(player: musicPlayer, isExpanded: $showMusicExpanded)
                .presentationDetents([.large])
                .presentationDragIndicator(.visible)
        }
        .onAppear {
            setupDemoData()
        }
        .onReceive(vehicleProvider.vehicleDataPublisher) { data in
            vehicleData = data
        }
    }

    // MARK: - Main Content

    @ViewBuilder
    private var mainContent: some View {
        switch selectedTab {
        case .navigation:
            TeslaNavigationScreen(
                navigationManager: navigationManager,
                vehicleData: vehicleData,
                layoutMode: $layoutMode
            )
        case .media:
            TeslaMediaScreen(player: musicPlayer)
        case .climate:
            TeslaClimateScreen(vehicleData: $vehicleData)
        case .vehicle:
            TeslaVehicleScreen(
                vehicleData: vehicleData,
                vehicleProvider: vehicleProvider
            )
        case .settings:
            TeslaSettingsScreen()
        }
    }

    // MARK: - Methods

    private func setupDemoData() {
        // Setup demo music track
        musicPlayer.currentTrack = TeslaTrack(
            title: "Bohemian Rhapsody",
            artist: "Queen",
            album: "A Night at the Opera"
        )
        musicPlayer.isPlaying = true
        musicPlayer.progress = 0.35
    }

    private func handleTabChange(_ tab: TeslaMenuTab) {
        // Handle tab-specific actions
    }
}

// MARK: - Tesla Settings Screen (Placeholder)

struct TeslaSettingsScreen: View {
    @State private var settings = TeslaSettings()

    var body: some View {
        ScrollView {
            VStack(spacing: 24) {
                // Display Settings
                TeslaCardLayout(title: "表示設定") {
                    VStack(spacing: 16) {
                        TeslaBrightnessControl(
                            brightness: $settings.screenBrightness
                        )

                        TeslaToggle("自動明るさ調整", isOn: $settings.autoBrightness)
                    }
                }

                // Unit Settings
                TeslaCardLayout(title: "単位設定") {
                    VStack(spacing: 16) {
                        TeslaToggle("摂氏表示 (°C)", isOn: $settings.useCelsius)
                        TeslaToggle("キロメートル表示", isOn: $settings.useKilometers)
                        TeslaToggle("24時間表示", isOn: $settings.use24HourFormat)
                    }
                }

                // Navigation Settings
                TeslaCardLayout(title: "ナビゲーション設定") {
                    VStack(spacing: 16) {
                        TeslaToggle("音声案内", isOn: $settings.voiceGuidanceEnabled)

                        TeslaSlider(
                            volume: $settings.voiceGuidanceVolume,
                            label: "音声音量"
                        )
                        .disabled(!settings.voiceGuidanceEnabled)

                        TeslaToggle("交通情報を表示", isOn: $settings.showTrafficInfo)
                        TeslaToggle("充電スポットを表示", isOn: $settings.showChargingStations)
                    }
                }

                // Notification Settings
                TeslaCardLayout(title: "通知設定") {
                    VStack(spacing: 16) {
                        TeslaToggle("充電完了通知", isOn: $settings.chargeCompleteNotification)
                        TeslaToggle("バッテリー低下通知", isOn: $settings.lowBatteryNotification)
                        TeslaToggle("セキュリティ通知", isOn: $settings.securityNotification)
                    }
                }
            }
            .padding(24)
        }
        .background(TeslaColors.background)
    }
}

// MARK: - Preview

#Preview("Tesla Main Dashboard") {
    TeslaMainDashboard()
        .teslaTheme()
}

// MARK: - App Entry Point Example

/// アプリのエントリーポイント例
/// 実際のプロジェクトで使用
/*
@main
struct TeslaDashboardApp: App {
    var sharedModelContainer: ModelContainer = {
        let schema = Schema([
            TeslaVehicle.self,
            TeslaSettings.self,
            TeslaFavoriteLocation.self,
            TeslaTripHistory.self,
            TeslaEnergyStats.self
        ])
        let modelConfiguration = ModelConfiguration(
            schema: schema,
            isStoredInMemoryOnly: false
        )

        do {
            return try ModelContainer(for: schema, configurations: [modelConfiguration])
        } catch {
            fatalError("Could not create ModelContainer: \(error)")
        }
    }()

    var body: some Scene {
        WindowGroup {
            TeslaMainDashboard()
                .teslaTheme()
        }
        .modelContainer(sharedModelContainer)
    }
}
*/
