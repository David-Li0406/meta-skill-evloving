// Tesla Dashboard UI - Navigation Screen
// ナビゲーション画面
// 全画面/分割モード切り替え対応

import SwiftUI
import MapKit

// MARK: - Tesla Navigation Screen

/// Tesla風ナビゲーション画面
struct TeslaNavigationScreen: View {
    // MARK: - Properties

    @ObservedObject var navigationManager: TeslaNavigationManager
    let vehicleData: VehicleData
    @Binding var layoutMode: TeslaLayoutMode

    // MARK: - State

    @State private var searchText: String = ""
    @State private var showSearchSheet: Bool = false
    @State private var showFavoritesSheet: Bool = false
    @State private var selectedDestination: TeslaDestination?

    // MARK: - Environment

    @Environment(\.teslaTheme) private var theme

    // MARK: - Body

    var body: some View {
        TeslaNavigationSplitLayout(
            mapContent: {
                TeslaMapView(
                    navigationManager: navigationManager,
                    isFullScreen: layoutMode == .fullscreen,
                    onExpandTap: {
                        withAnimation(TeslaAnimation.standard) {
                            layoutMode = layoutMode == .fullscreen ? .split : .fullscreen
                        }
                    }
                )
            },
            controlContent: {
                navigationControls
            },
            layoutMode: $layoutMode
        )
        .sheet(isPresented: $showSearchSheet) {
            NavigationSearchSheet(
                searchText: $searchText,
                onSelect: { destination in
                    selectedDestination = destination
                    showSearchSheet = false
                    startNavigation(to: destination)
                }
            )
            .presentationDetents([.medium, .large])
        }
        .sheet(isPresented: $showFavoritesSheet) {
            FavoritesSheet(
                onSelect: { destination in
                    selectedDestination = destination
                    showFavoritesSheet = false
                    startNavigation(to: destination)
                }
            )
            .presentationDetents([.medium, .large])
        }
    }

    // MARK: - Navigation Controls

    private var navigationControls: some View {
        VStack(spacing: 16) {
            // Search Bar
            searchBar

            // Quick Destinations
            quickDestinations

            // Current Navigation Info (if navigating)
            if navigationManager.isNavigating {
                currentNavigationInfo
            }

            // Vehicle Status (compact)
            TeslaCompactVehicleStatus(vehicleData: vehicleData)

            Spacer()
        }
    }

    // MARK: - Search Bar

    private var searchBar: some View {
        Button {
            showSearchSheet = true
        } label: {
            HStack(spacing: 12) {
                Image(systemName: "magnifyingglass")
                    .font(.system(size: 16))
                    .foregroundStyle(TeslaColors.textSecondary)

                Text("目的地を検索")
                    .font(TeslaTypography.bodyMedium)
                    .foregroundStyle(TeslaColors.textSecondary)

                Spacer()

                // Voice Search
                Button {
                    // Voice search
                } label: {
                    Image(systemName: "mic.fill")
                        .font(.system(size: 16))
                        .foregroundStyle(TeslaColors.accent)
                }
            }
            .padding(16)
            .background(TeslaColors.glassBackground)
            .clipShape(RoundedRectangle(cornerRadius: 12))
        }
    }

    // MARK: - Quick Destinations

    private var quickDestinations: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text("よく行く場所")
                    .font(TeslaTypography.titleSmall)
                    .foregroundStyle(TeslaColors.textSecondary)

                Spacer()

                Button {
                    showFavoritesSheet = true
                } label: {
                    Text("すべて見る")
                        .font(TeslaTypography.labelMedium)
                        .foregroundStyle(TeslaColors.accent)
                }
            }

            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 12) {
                    // Home
                    quickDestinationButton(
                        icon: "house.fill",
                        label: "自宅",
                        destination: TeslaDestination(
                            name: "自宅",
                            coordinate: CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671)
                        )
                    )

                    // Work
                    quickDestinationButton(
                        icon: "building.2.fill",
                        label: "職場",
                        destination: TeslaDestination(
                            name: "職場",
                            coordinate: CLLocationCoordinate2D(latitude: 35.6895, longitude: 139.6917)
                        )
                    )

                    // Supercharger
                    quickDestinationButton(
                        icon: "bolt.fill",
                        label: "Supercharger",
                        destination: TeslaDestination(
                            name: "Tesla 東京ベイ",
                            coordinate: CLLocationCoordinate2D(latitude: 35.6290, longitude: 139.7763)
                        )
                    )
                }
            }
        }
        .padding(16)
        .background(TeslaColors.glassBackground)
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }

    private func quickDestinationButton(
        icon: String,
        label: String,
        destination: TeslaDestination
    ) -> some View {
        Button {
            startNavigation(to: destination)
        } label: {
            VStack(spacing: 8) {
                Image(systemName: icon)
                    .font(.system(size: 20))
                    .foregroundStyle(TeslaColors.accent)
                    .frame(width: 48, height: 48)
                    .background(TeslaColors.accent.opacity(0.2))
                    .clipShape(Circle())

                Text(label)
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textSecondary)
            }
        }
        .buttonStyle(TeslaScaleButtonStyle())
    }

    // MARK: - Current Navigation Info

    private var currentNavigationInfo: some View {
        VStack(spacing: 12) {
            // Destination
            HStack {
                Image(systemName: "mappin.circle.fill")
                    .font(.system(size: 20))
                    .foregroundStyle(TeslaColors.statusRed)

                VStack(alignment: .leading, spacing: 2) {
                    Text(navigationManager.destination?.name ?? "")
                        .font(TeslaTypography.titleSmall)
                        .foregroundStyle(TeslaColors.textPrimary)

                    Text(navigationManager.destination?.address ?? "")
                        .font(TeslaTypography.labelSmall)
                        .foregroundStyle(TeslaColors.textSecondary)
                        .lineLimit(1)
                }

                Spacer()

                // Cancel Button
                Button {
                    navigationManager.stopNavigation()
                } label: {
                    Image(systemName: "xmark")
                        .font(.system(size: 12, weight: .semibold))
                        .foregroundStyle(TeslaColors.textSecondary)
                        .frame(width: 28, height: 28)
                        .background(TeslaColors.glassBackground)
                        .clipShape(Circle())
                }
            }

            Divider()
                .background(TeslaColors.glassBorder)

            // ETA & Distance
            HStack {
                VStack(alignment: .leading, spacing: 2) {
                    Text("到着予定")
                        .font(TeslaTypography.labelSmall)
                        .foregroundStyle(TeslaColors.textTertiary)

                    Text(navigationManager.formattedETA)
                        .font(TeslaTypography.titleMedium)
                        .foregroundStyle(TeslaColors.textPrimary)
                }

                Spacer()

                VStack(alignment: .trailing, spacing: 2) {
                    Text("残り")
                        .font(TeslaTypography.labelSmall)
                        .foregroundStyle(TeslaColors.textTertiary)

                    Text(navigationManager.formattedRemainingDistance)
                        .font(TeslaTypography.titleMedium)
                        .foregroundStyle(TeslaColors.textPrimary)
                }
            }
        }
        .padding(16)
        .background(TeslaColors.glassBackground)
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }

    // MARK: - Methods

    private func startNavigation(to destination: TeslaDestination) {
        Task {
            let result = await navigationManager.startNavigation(to: destination)
            switch result {
            case .success:
                // Navigation started
                break
            case .failure(let error):
                // Handle error
                print("Navigation error: \(error.localizedDescription)")
            }
        }
    }
}

// MARK: - Navigation Search Sheet

struct NavigationSearchSheet: View {
    @Binding var searchText: String
    var onSelect: (TeslaDestination) -> Void

    @State private var searchResults: [TeslaDestination] = []

    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                // Search Field
                HStack(spacing: 12) {
                    Image(systemName: "magnifyingglass")
                        .foregroundStyle(TeslaColors.textSecondary)

                    TextField("目的地を検索", text: $searchText)
                        .font(TeslaTypography.bodyMedium)
                        .foregroundStyle(TeslaColors.textPrimary)

                    if !searchText.isEmpty {
                        Button {
                            searchText = ""
                        } label: {
                            Image(systemName: "xmark.circle.fill")
                                .foregroundStyle(TeslaColors.textTertiary)
                        }
                    }
                }
                .padding(16)
                .background(TeslaColors.glassBackground)
                .clipShape(RoundedRectangle(cornerRadius: 12))
                .padding(16)

                // Results
                if searchResults.isEmpty {
                    ContentUnavailableView(
                        "場所を検索",
                        systemImage: "magnifyingglass",
                        description: Text("目的地を入力してください")
                    )
                } else {
                    List(searchResults) { result in
                        Button {
                            onSelect(result)
                        } label: {
                            HStack {
                                Image(systemName: "mappin.circle")
                                    .foregroundStyle(TeslaColors.accent)

                                VStack(alignment: .leading) {
                                    Text(result.name)
                                        .font(TeslaTypography.bodyMedium)
                                        .foregroundStyle(TeslaColors.textPrimary)

                                    if let address = result.address {
                                        Text(address)
                                            .font(TeslaTypography.labelSmall)
                                            .foregroundStyle(TeslaColors.textSecondary)
                                    }
                                }
                            }
                        }
                    }
                    .listStyle(.plain)
                }
            }
            .background(TeslaColors.background)
            .navigationTitle("目的地を検索")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}

// MARK: - Favorites Sheet

struct FavoritesSheet: View {
    var onSelect: (TeslaDestination) -> Void

    @State private var favorites: [TeslaFavoriteLocation] = TeslaFavoriteLocation.previewList

    var body: some View {
        NavigationStack {
            List(favorites) { favorite in
                Button {
                    let destination = TeslaDestination(
                        name: favorite.name,
                        coordinate: favorite.coordinate,
                        address: favorite.formattedAddress
                    )
                    onSelect(destination)
                } label: {
                    HStack {
                        Image(systemName: favorite.categoryEnum.icon.systemName)
                            .foregroundStyle(Color(hex: favorite.displayColor) ?? TeslaColors.accent)
                            .frame(width: 32, height: 32)
                            .background(TeslaColors.glassBackground)
                            .clipShape(Circle())

                        VStack(alignment: .leading) {
                            Text(favorite.name)
                                .font(TeslaTypography.bodyMedium)
                                .foregroundStyle(TeslaColors.textPrimary)

                            Text(favorite.shortAddress)
                                .font(TeslaTypography.labelSmall)
                                .foregroundStyle(TeslaColors.textSecondary)
                        }
                    }
                }
            }
            .listStyle(.plain)
            .background(TeslaColors.background)
            .navigationTitle("お気に入り")
            .navigationBarTitleDisplayMode(.inline)
        }
    }
}

// MARK: - Color Extension

extension Color {
    init?(hex: String) {
        var hexSanitized = hex.trimmingCharacters(in: .whitespacesAndNewlines)
        hexSanitized = hexSanitized.replacingOccurrences(of: "#", with: "")

        var rgb: UInt64 = 0

        guard Scanner(string: hexSanitized).scanHexInt64(&rgb) else {
            return nil
        }

        self.init(
            red: Double((rgb & 0xFF0000) >> 16) / 255.0,
            green: Double((rgb & 0x00FF00) >> 8) / 255.0,
            blue: Double(rgb & 0x0000FF) / 255.0
        )
    }
}

// MARK: - Preview

#Preview("Tesla Navigation Screen") {
    struct NavigationScreenPreview: View {
        @StateObject private var navigationManager = TeslaNavigationManager()
        @State private var layoutMode: TeslaLayoutMode = .split

        var body: some View {
            TeslaNavigationScreen(
                navigationManager: navigationManager,
                vehicleData: .preview,
                layoutMode: $layoutMode
            )
        }
    }

    return NavigationScreenPreview()
        .teslaTheme()
}
