// Tesla Dashboard UI - Dashboard Layout
// iPad向けダッシュボードレイアウト
// 全画面/分割ビュー切り替え対応

import SwiftUI

// MARK: - Tesla Dashboard Layout

/// Tesla風ダッシュボードレイアウト
/// iPad向けの適応型レイアウト
struct TeslaDashboardLayout<Content: View, Sidebar: View>: View {
    // MARK: - Properties

    let content: Content
    let sidebar: Sidebar?
    var showSidebar: Bool = true
    var sidebarWidth: CGFloat = 320

    // MARK: - Environment

    @Environment(\.teslaTheme) private var theme
    @Environment(\.horizontalSizeClass) private var horizontalSizeClass

    // MARK: - Initialization

    init(
        @ViewBuilder content: () -> Content,
        @ViewBuilder sidebar: () -> Sidebar
    ) {
        self.content = content()
        self.sidebar = sidebar()
    }

    init(
        showSidebar: Bool = true,
        sidebarWidth: CGFloat = 320,
        @ViewBuilder content: () -> Content
    ) where Sidebar == EmptyView {
        self.content = content()
        self.sidebar = nil
        self.showSidebar = showSidebar
        self.sidebarWidth = sidebarWidth
    }

    // MARK: - Body

    var body: some View {
        GeometryReader { geometry in
            HStack(spacing: 0) {
                // Sidebar (if present and visible)
                if let sidebar, showSidebar, horizontalSizeClass == .regular {
                    sidebar
                        .frame(width: sidebarWidth)
                        .background(TeslaColors.surface)
                }

                // Main Content
                content
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            }
            .background(TeslaColors.background)
        }
    }
}

// MARK: - Tesla Full Screen Layout

/// 全画面レイアウト
struct TeslaFullScreenLayout<Content: View>: View {
    let content: Content
    var showNavigationBar: Bool = true
    var navigationBar: AnyView?

    init(
        showNavigationBar: Bool = true,
        @ViewBuilder content: () -> Content
    ) {
        self.content = content()
        self.showNavigationBar = showNavigationBar
    }

    var body: some View {
        VStack(spacing: 0) {
            // Navigation Bar
            if showNavigationBar, let navigationBar {
                navigationBar
            }

            // Content
            content
                .frame(maxWidth: .infinity, maxHeight: .infinity)
        }
        .background(TeslaColors.background)
        .ignoresSafeArea(edges: .bottom)
    }

    func navigationBar<NavBar: View>(@ViewBuilder _ bar: () -> NavBar) -> TeslaFullScreenLayout {
        var layout = self
        layout.navigationBar = AnyView(bar())
        return layout
    }
}

// MARK: - Tesla Card Layout

/// カード形式のレイアウト
struct TeslaCardLayout<Content: View>: View {
    let title: String?
    let subtitle: String?
    let content: Content

    init(
        title: String? = nil,
        subtitle: String? = nil,
        @ViewBuilder content: () -> Content
    ) {
        self.title = title
        self.subtitle = subtitle
        self.content = content()
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            // Header
            if title != nil || subtitle != nil {
                VStack(alignment: .leading, spacing: 4) {
                    if let title {
                        Text(title)
                            .font(TeslaTypography.headlineSmall)
                            .foregroundStyle(TeslaColors.textPrimary)
                    }

                    if let subtitle {
                        Text(subtitle)
                            .font(TeslaTypography.bodyMedium)
                            .foregroundStyle(TeslaColors.textSecondary)
                    }
                }
            }

            // Content
            content
        }
        .padding(24)
        .teslaCard()
    }
}

// MARK: - Tesla Grid Layout

/// グリッドレイアウト
struct TeslaGridLayout<Item: Identifiable, Content: View>: View {
    let items: [Item]
    let columns: Int
    let spacing: CGFloat
    let content: (Item) -> Content

    init(
        items: [Item],
        columns: Int = 2,
        spacing: CGFloat = 16,
        @ViewBuilder content: @escaping (Item) -> Content
    ) {
        self.items = items
        self.columns = columns
        self.spacing = spacing
        self.content = content
    }

    var body: some View {
        LazyVGrid(
            columns: Array(repeating: GridItem(.flexible(), spacing: spacing), count: columns),
            spacing: spacing
        ) {
            ForEach(items) { item in
                content(item)
            }
        }
    }
}

// MARK: - Tesla Adaptive Stack

/// 適応型スタック（画面サイズに応じて水平/垂直を切り替え）
struct TeslaAdaptiveStack<Content: View>: View {
    @Environment(\.horizontalSizeClass) private var horizontalSizeClass

    let content: Content
    var horizontalAlignment: HorizontalAlignment = .center
    var verticalAlignment: VerticalAlignment = .center
    var spacing: CGFloat = 16

    init(
        horizontalAlignment: HorizontalAlignment = .center,
        verticalAlignment: VerticalAlignment = .center,
        spacing: CGFloat = 16,
        @ViewBuilder content: () -> Content
    ) {
        self.horizontalAlignment = horizontalAlignment
        self.verticalAlignment = verticalAlignment
        self.spacing = spacing
        self.content = content()
    }

    var body: some View {
        if horizontalSizeClass == .regular {
            HStack(alignment: verticalAlignment, spacing: spacing) {
                content
            }
        } else {
            VStack(alignment: horizontalAlignment, spacing: spacing) {
                content
            }
        }
    }
}

// MARK: - Layout Mode

/// レイアウトモード
enum TeslaLayoutMode: String, CaseIterable {
    case fullscreen = "fullscreen"
    case split = "split"
    case compact = "compact"

    var displayName: String {
        switch self {
        case .fullscreen: return "全画面"
        case .split: return "分割"
        case .compact: return "コンパクト"
        }
    }

    var icon: String {
        switch self {
        case .fullscreen: return "arrow.up.left.and.arrow.down.right"
        case .split: return "rectangle.split.2x1"
        case .compact: return "rectangle.compress.vertical"
        }
    }
}

// MARK: - Layout Mode Picker

/// レイアウトモード切り替えボタン
struct TeslaLayoutModePicker: View {
    @Binding var mode: TeslaLayoutMode

    var body: some View {
        HStack(spacing: 8) {
            ForEach(TeslaLayoutMode.allCases, id: \.self) { layoutMode in
                Button {
                    withAnimation(TeslaAnimation.quick) {
                        mode = layoutMode
                    }
                } label: {
                    Image(systemName: layoutMode.icon)
                        .font(.system(size: 14))
                        .foregroundStyle(mode == layoutMode ? TeslaColors.accent : TeslaColors.textSecondary)
                        .frame(width: 32, height: 32)
                        .background(
                            mode == layoutMode ? TeslaColors.accent.opacity(0.2) : TeslaColors.glassBackground
                        )
                        .clipShape(RoundedRectangle(cornerRadius: 6))
                }
                .buttonStyle(TeslaScaleButtonStyle())
            }
        }
        .padding(4)
        .background(TeslaColors.glassBackground)
        .clipShape(RoundedRectangle(cornerRadius: 10))
    }
}

// MARK: - Preview

#Preview("Tesla Dashboard Layout") {
    TeslaDashboardLayout(
        content: {
            VStack {
                Text("Main Content")
                    .font(TeslaTypography.displaySmall)
                    .foregroundStyle(TeslaColors.textPrimary)
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .background(TeslaColors.background)
        },
        sidebar: {
            VStack(alignment: .leading, spacing: 16) {
                Text("Sidebar")
                    .font(TeslaTypography.headlineMedium)
                    .foregroundStyle(TeslaColors.textPrimary)

                Spacer()
            }
            .padding(24)
        }
    )
}

#Preview("Tesla Card Layout") {
    ScrollView {
        VStack(spacing: 16) {
            TeslaCardLayout(title: "車両ステータス", subtitle: "オンライン") {
                Text("Content here")
                    .foregroundStyle(TeslaColors.textSecondary)
            }

            TeslaCardLayout(title: "空調") {
                Text("Climate content")
                    .foregroundStyle(TeslaColors.textSecondary)
            }
        }
        .padding(24)
    }
    .background(TeslaColors.background)
}
