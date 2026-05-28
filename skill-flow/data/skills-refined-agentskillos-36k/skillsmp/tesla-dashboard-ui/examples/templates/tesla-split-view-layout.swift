// Tesla Dashboard UI - Split View Layout
// 分割ビューレイアウト
// ナビ+コントロール等の2ペイン表示

import SwiftUI

// MARK: - Tesla Split View Layout

/// Tesla風分割ビューレイアウト
/// 左右または上下の2ペイン表示
struct TeslaSplitViewLayout<Primary: View, Secondary: View>: View {
    // MARK: - Properties

    let primary: Primary
    let secondary: Secondary
    var splitRatio: CGFloat = 0.6
    var orientation: SplitOrientation = .horizontal
    var showDivider: Bool = true

    // MARK: - Environment

    @Environment(\.teslaTheme) private var theme
    @Environment(\.horizontalSizeClass) private var horizontalSizeClass

    // MARK: - State

    @State private var currentRatio: CGFloat

    // MARK: - Initialization

    init(
        splitRatio: CGFloat = 0.6,
        orientation: SplitOrientation = .horizontal,
        showDivider: Bool = true,
        @ViewBuilder primary: () -> Primary,
        @ViewBuilder secondary: () -> Secondary
    ) {
        self.primary = primary()
        self.secondary = secondary()
        self.splitRatio = splitRatio
        self.orientation = orientation
        self.showDivider = showDivider
        self._currentRatio = State(initialValue: splitRatio)
    }

    // MARK: - Body

    var body: some View {
        GeometryReader { geometry in
            if orientation == .horizontal {
                horizontalLayout(geometry: geometry)
            } else {
                verticalLayout(geometry: geometry)
            }
        }
        .background(TeslaColors.background)
    }

    // MARK: - Horizontal Layout

    private func horizontalLayout(geometry: GeometryProxy) -> some View {
        HStack(spacing: 0) {
            // Primary View
            primary
                .frame(width: geometry.size.width * currentRatio)

            // Divider
            if showDivider {
                splitDivider(isHorizontal: true)
                    .gesture(
                        DragGesture()
                            .onChanged { value in
                                let newRatio = (geometry.size.width * currentRatio + value.translation.width) / geometry.size.width
                                currentRatio = max(0.3, min(0.8, newRatio))
                            }
                    )
            }

            // Secondary View
            secondary
                .frame(maxWidth: .infinity)
        }
    }

    // MARK: - Vertical Layout

    private func verticalLayout(geometry: GeometryProxy) -> some View {
        VStack(spacing: 0) {
            // Primary View
            primary
                .frame(height: geometry.size.height * currentRatio)

            // Divider
            if showDivider {
                splitDivider(isHorizontal: false)
                    .gesture(
                        DragGesture()
                            .onChanged { value in
                                let newRatio = (geometry.size.height * currentRatio + value.translation.height) / geometry.size.height
                                currentRatio = max(0.3, min(0.8, newRatio))
                            }
                    )
            }

            // Secondary View
            secondary
                .frame(maxHeight: .infinity)
        }
    }

    // MARK: - Divider

    private func splitDivider(isHorizontal: Bool) -> some View {
        ZStack {
            Rectangle()
                .fill(TeslaColors.glassBorder)
                .frame(
                    width: isHorizontal ? 1 : nil,
                    height: isHorizontal ? nil : 1
                )

            // Drag Handle
            RoundedRectangle(cornerRadius: 2)
                .fill(TeslaColors.textTertiary)
                .frame(
                    width: isHorizontal ? 4 : 32,
                    height: isHorizontal ? 32 : 4
                )
        }
        .frame(
            width: isHorizontal ? 12 : nil,
            height: isHorizontal ? nil : 12
        )
        .contentShape(Rectangle())
    }
}

// MARK: - Split Orientation

/// 分割方向
enum SplitOrientation {
    case horizontal
    case vertical
}

// MARK: - Tesla Navigation Split Layout

/// ナビゲーション用分割レイアウト
/// 地図が主、コントロールが副
struct TeslaNavigationSplitLayout<MapContent: View, ControlContent: View>: View {
    // MARK: - Properties

    let mapContent: MapContent
    let controlContent: ControlContent
    @Binding var layoutMode: TeslaLayoutMode

    // MARK: - Body

    var body: some View {
        switch layoutMode {
        case .fullscreen:
            fullscreenLayout
        case .split:
            splitLayout
        case .compact:
            compactLayout
        }
    }

    // MARK: - Fullscreen Layout

    private var fullscreenLayout: some View {
        ZStack {
            mapContent
                .ignoresSafeArea()

            // Floating Controls
            VStack {
                Spacer()

                HStack {
                    Spacer()

                    // Layout Toggle
                    layoutToggleButton
                        .padding(16)
                }
            }
        }
    }

    // MARK: - Split Layout

    private var splitLayout: some View {
        TeslaSplitViewLayout(
            splitRatio: 0.65,
            orientation: .horizontal,
            primary: {
                mapContent
            },
            secondary: {
                ScrollView {
                    controlContent
                        .padding(16)
                }
                .background(TeslaColors.surface)
            }
        )
        .overlay(alignment: .topTrailing) {
            layoutToggleButton
                .padding(16)
        }
    }

    // MARK: - Compact Layout

    private var compactLayout: some View {
        VStack(spacing: 0) {
            // Map (smaller)
            mapContent
                .frame(height: 200)
                .clipShape(RoundedRectangle(cornerRadius: 16))
                .padding(16)

            // Controls (scrollable)
            ScrollView {
                controlContent
                    .padding(.horizontal, 16)
            }
        }
        .background(TeslaColors.background)
        .overlay(alignment: .topTrailing) {
            layoutToggleButton
                .padding(16)
        }
    }

    // MARK: - Layout Toggle Button

    private var layoutToggleButton: some View {
        Button {
            withAnimation(TeslaAnimation.standard) {
                switch layoutMode {
                case .fullscreen: layoutMode = .split
                case .split: layoutMode = .compact
                case .compact: layoutMode = .fullscreen
                }
            }
        } label: {
            Image(systemName: layoutMode.icon)
                .font(.system(size: 14, weight: .semibold))
                .foregroundStyle(TeslaColors.textPrimary)
                .frame(width: 36, height: 36)
                .background(TeslaColors.glassBackground)
                .clipShape(Circle())
        }
        .buttonStyle(TeslaScaleButtonStyle())
    }
}

// MARK: - Tesla Media Split Layout

/// メディア用分割レイアウト
/// アートワークとコントロール
struct TeslaMediaSplitLayout<ArtworkContent: View, ControlContent: View>: View {
    let artworkContent: ArtworkContent
    let controlContent: ControlContent
    var isExpanded: Bool = true

    @Environment(\.horizontalSizeClass) private var horizontalSizeClass

    var body: some View {
        if horizontalSizeClass == .regular && isExpanded {
            // iPad: 横並び
            HStack(spacing: 32) {
                artworkContent
                    .frame(maxWidth: 400)

                controlContent
                    .frame(maxWidth: .infinity)
            }
            .padding(32)
        } else {
            // iPhone/Compact: 縦並び
            VStack(spacing: 24) {
                artworkContent
                    .frame(maxWidth: 300)

                controlContent
            }
            .padding(24)
        }
    }
}

// MARK: - Preview

#Preview("Tesla Split View Layout") {
    TeslaSplitViewLayout(
        splitRatio: 0.6,
        orientation: .horizontal,
        primary: {
            ZStack {
                TeslaColors.surface

                Text("Map View")
                    .font(TeslaTypography.displaySmall)
                    .foregroundStyle(TeslaColors.textPrimary)
            }
        },
        secondary: {
            ScrollView {
                VStack(spacing: 16) {
                    ForEach(0..<5) { i in
                        RoundedRectangle(cornerRadius: 12)
                            .fill(TeslaColors.glassBackground)
                            .frame(height: 100)
                            .overlay(
                                Text("Card \(i + 1)")
                                    .foregroundStyle(TeslaColors.textSecondary)
                            )
                    }
                }
                .padding(16)
            }
            .background(TeslaColors.surface)
        }
    )
}

#Preview("Tesla Navigation Split Layout") {
    struct NavigationSplitPreview: View {
        @State private var layoutMode: TeslaLayoutMode = .split

        var body: some View {
            TeslaNavigationSplitLayout(
                mapContent: {
                    ZStack {
                        Color.gray.opacity(0.3)
                        Text("Map")
                            .font(TeslaTypography.displaySmall)
                            .foregroundStyle(TeslaColors.textPrimary)
                    }
                },
                controlContent: {
                    VStack(spacing: 16) {
                        ForEach(0..<3) { i in
                            RoundedRectangle(cornerRadius: 12)
                                .fill(TeslaColors.glassBackground)
                                .frame(height: 80)
                                .overlay(
                                    Text("Control \(i + 1)")
                                        .foregroundStyle(TeslaColors.textSecondary)
                                )
                        }
                    }
                },
                layoutMode: $layoutMode
            )
        }
    }

    return NavigationSplitPreview()
}
