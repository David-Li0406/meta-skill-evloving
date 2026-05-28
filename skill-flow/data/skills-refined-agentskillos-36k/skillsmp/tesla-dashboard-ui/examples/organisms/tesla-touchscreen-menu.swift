// Tesla Dashboard UI - Touchscreen Menu
// 5タブメニュー
// ナビ/音楽/空調/車両/設定

import SwiftUI

// MARK: - Tesla Touchscreen Menu

/// Tesla風タッチスクリーンメニュー
/// 画面下部のタブバー
struct TeslaTouchscreenMenu: View {
    // MARK: - Properties

    @Binding var selectedTab: TeslaMenuTab
    var onTabChange: ((TeslaMenuTab) -> Void)? = nil

    // MARK: - Environment

    @Environment(\.teslaTheme) private var theme
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    // MARK: - Body

    var body: some View {
        HStack(spacing: 0) {
            ForEach(TeslaMenuTab.allCases) { tab in
                menuButton(for: tab)
            }
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 8)
        .background(
            TeslaColors.surface
                .opacity(0.95)
                .blur(radius: 0.5)
        )
        .overlay(
            Rectangle()
                .fill(TeslaColors.glassBorder)
                .frame(height: 1),
            alignment: .top
        )
    }

    // MARK: - Menu Button

    private func menuButton(for tab: TeslaMenuTab) -> some View {
        Button {
            withAnimation(reduceMotion ? .none : TeslaAnimation.quick) {
                selectedTab = tab
            }
            onTabChange?(tab)
        } label: {
            VStack(spacing: 6) {
                // Icon
                ZStack {
                    if selectedTab == tab {
                        Circle()
                            .fill(TeslaColors.accent.opacity(0.2))
                            .frame(width: 44, height: 44)
                    }

                    Image(systemName: tab.iconName)
                        .font(.system(size: 20, weight: selectedTab == tab ? .semibold : .regular))
                        .foregroundStyle(selectedTab == tab ? TeslaColors.accent : TeslaColors.textSecondary)
                }
                .frame(width: 44, height: 44)

                // Label
                Text(tab.label)
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(selectedTab == tab ? TeslaColors.accent : TeslaColors.textSecondary)
            }
            .frame(maxWidth: .infinity)
        }
        .buttonStyle(TeslaMenuButtonStyle())
        .accessibilityLabel(tab.label)
        .accessibilityAddTraits(selectedTab == tab ? .isSelected : [])
    }
}

// MARK: - Tesla Menu Tab

/// メニュータブ定義
enum TeslaMenuTab: String, CaseIterable, Identifiable {
    case navigation = "navigation"
    case media = "media"
    case climate = "climate"
    case vehicle = "vehicle"
    case settings = "settings"

    var id: String { rawValue }

    var label: String {
        switch self {
        case .navigation: return "ナビ"
        case .media: return "メディア"
        case .climate: return "空調"
        case .vehicle: return "車両"
        case .settings: return "設定"
        }
    }

    var iconName: String {
        switch self {
        case .navigation: return "location.fill"
        case .media: return "music.note"
        case .climate: return "thermometer.medium"
        case .vehicle: return "car.fill"
        case .settings: return "gearshape.fill"
        }
    }

    var icon: TeslaIcon {
        switch self {
        case .navigation: return .navigation
        case .media: return .music
        case .climate: return .climate
        case .vehicle: return .car
        case .settings: return .settings
        }
    }
}

// MARK: - Tesla Menu Button Style

/// メニューボタン用スタイル
struct TeslaMenuButtonStyle: ButtonStyle {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
            .animation(
                reduceMotion ? .none : .easeInOut(duration: 0.1),
                value: configuration.isPressed
            )
    }
}

// MARK: - Compact Menu

/// コンパクトメニュー（ナビ全画面モード用）
struct TeslaCompactMenu: View {
    @Binding var selectedTab: TeslaMenuTab
    var visibleTabs: [TeslaMenuTab] = [.navigation, .media, .climate]

    var body: some View {
        HStack(spacing: 8) {
            ForEach(visibleTabs) { tab in
                compactButton(for: tab)
            }
        }
        .padding(8)
        .background(TeslaColors.glassBackground)
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }

    private func compactButton(for tab: TeslaMenuTab) -> some View {
        Button {
            withAnimation(TeslaAnimation.quick) {
                selectedTab = tab
            }
        } label: {
            Image(systemName: tab.iconName)
                .font(.system(size: 16, weight: selectedTab == tab ? .semibold : .regular))
                .foregroundStyle(selectedTab == tab ? TeslaColors.accent : TeslaColors.textSecondary)
                .frame(width: 36, height: 36)
                .background(
                    selectedTab == tab ? TeslaColors.accent.opacity(0.2) : Color.clear
                )
                .clipShape(Circle())
        }
        .buttonStyle(TeslaScaleButtonStyle())
    }
}

// MARK: - Side Menu

/// サイドメニュー（縦型レイアウト用）
struct TeslaSideMenu: View {
    @Binding var selectedTab: TeslaMenuTab
    var onTabChange: ((TeslaMenuTab) -> Void)? = nil

    var body: some View {
        VStack(spacing: 8) {
            ForEach(TeslaMenuTab.allCases) { tab in
                sideMenuButton(for: tab)
            }

            Spacer()
        }
        .padding(12)
        .frame(width: 80)
        .background(TeslaColors.surface)
    }

    private func sideMenuButton(for tab: TeslaMenuTab) -> some View {
        Button {
            withAnimation(TeslaAnimation.quick) {
                selectedTab = tab
            }
            onTabChange?(tab)
        } label: {
            VStack(spacing: 6) {
                ZStack {
                    if selectedTab == tab {
                        RoundedRectangle(cornerRadius: 8)
                            .fill(TeslaColors.accent.opacity(0.2))
                            .frame(width: 48, height: 48)
                    }

                    Image(systemName: tab.iconName)
                        .font(.system(size: 20, weight: selectedTab == tab ? .semibold : .regular))
                        .foregroundStyle(selectedTab == tab ? TeslaColors.accent : TeslaColors.textSecondary)
                }
                .frame(width: 48, height: 48)

                Text(tab.label)
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(selectedTab == tab ? TeslaColors.accent : TeslaColors.textSecondary)
            }
        }
        .buttonStyle(TeslaScaleButtonStyle())
    }
}

// MARK: - Preview

#Preview("Tesla Touchscreen Menu") {
    struct MenuPreview: View {
        @State private var selectedTab: TeslaMenuTab = .navigation

        var body: some View {
            VStack(spacing: 0) {
                // Content Area
                ZStack {
                    TeslaColors.background

                    VStack(spacing: 16) {
                        Text(selectedTab.label)
                            .font(TeslaTypography.displaySmall)
                            .foregroundStyle(TeslaColors.textPrimary)

                        Image(systemName: selectedTab.iconName)
                            .font(.system(size: 64))
                            .foregroundStyle(TeslaColors.accent)
                    }
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)

                // Menu
                TeslaTouchscreenMenu(
                    selectedTab: $selectedTab,
                    onTabChange: { tab in
                        print("Selected: \(tab.label)")
                    }
                )
            }
            .ignoresSafeArea(edges: .bottom)
        }
    }

    return MenuPreview()
}

#Preview("Compact & Side Menu") {
    HStack(spacing: 24) {
        // Side Menu
        TeslaSideMenu(selectedTab: .constant(.navigation))

        VStack {
            Spacer()

            // Compact Menu
            TeslaCompactMenu(selectedTab: .constant(.media))

            Spacer()
        }
        .frame(maxWidth: .infinity)
    }
    .background(TeslaColors.background)
}
