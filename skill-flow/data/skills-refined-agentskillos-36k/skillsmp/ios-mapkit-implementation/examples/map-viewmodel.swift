// MARK: - Map ViewModel Example
// iOS 17+ SwiftUI MapKit MVVM パターン

import SwiftUI
import MapKit
import CoreLocation

// MARK: - Data Models

/// 地図上に表示する場所
struct Place: Identifiable, Equatable, Hashable {
    let id = UUID()
    let name: String
    let coordinate: CLLocationCoordinate2D
    let category: PlaceCategory

    static func == (lhs: Place, rhs: Place) -> Bool {
        lhs.id == rhs.id
    }

    func hash(into hasher: inout Hasher) {
        hasher.combine(id)
    }
}

enum PlaceCategory: String, CaseIterable {
    case restaurant = "レストラン"
    case cafe = "カフェ"
    case shop = "ショップ"
    case landmark = "ランドマーク"

    var systemImage: String {
        switch self {
        case .restaurant: return "fork.knife"
        case .cafe: return "cup.and.saucer"
        case .shop: return "bag"
        case .landmark: return "building.2"
        }
    }

    var color: Color {
        switch self {
        case .restaurant: return .orange
        case .cafe: return .brown
        case .shop: return .purple
        case .landmark: return .blue
        }
    }
}

// MARK: - Map ViewModel

/// 地図機能を管理するViewModel
@MainActor
@Observable
final class MapViewModel {
    // MARK: - Published Properties

    /// カメラ位置
    var cameraPosition: MapCameraPosition = .automatic

    /// 表示する場所のリスト
    var places: [Place] = []

    /// 選択中の場所
    var selectedPlace: Place?

    /// 計算された経路
    var route: MKRoute?

    /// 検索結果
    var searchResults: [MKMapItem] = []

    /// ローディング状態
    var isLoading = false

    /// エラーメッセージ
    var errorMessage: String?

    /// 現在の表示領域
    var visibleRegion: MKCoordinateRegion?

    // MARK: - Private Properties

    private let locationManager: LocationManager
    private var searchTask: Task<Void, Never>?

    // MARK: - Initialization

    init(locationManager: LocationManager = LocationManager()) {
        self.locationManager = locationManager
    }

    // MARK: - Public Methods

    /// 現在地に移動
    func moveToUserLocation() {
        cameraPosition = .userLocation(fallback: .automatic)
    }

    /// 特定の座標に移動
    func moveTo(coordinate: CLLocationCoordinate2D, animated: Bool = true) {
        let region = MKCoordinateRegion(
            center: coordinate,
            span: MKCoordinateSpan(latitudeDelta: 0.01, longitudeDelta: 0.01)
        )

        if animated {
            withAnimation(.easeInOut(duration: 0.5)) {
                cameraPosition = .region(region)
            }
        } else {
            cameraPosition = .region(region)
        }
    }

    /// 場所を選択
    func selectPlace(_ place: Place) {
        selectedPlace = place
        moveTo(coordinate: place.coordinate)
    }

    /// 周辺検索
    func searchNearby(query: String) async {
        searchTask?.cancel()

        guard !query.isEmpty else {
            searchResults = []
            return
        }

        searchTask = Task {
            isLoading = true
            defer { isLoading = false }

            do {
                try await Task.sleep(for: .milliseconds(300)) // デバウンス

                guard !Task.isCancelled else { return }

                let request = MKLocalSearch.Request()
                request.naturalLanguageQuery = query

                if let region = visibleRegion {
                    request.region = region
                }

                let search = MKLocalSearch(request: request)
                let response = try await search.start()

                guard !Task.isCancelled else { return }

                searchResults = response.mapItems
                errorMessage = nil
            } catch {
                if !Task.isCancelled {
                    errorMessage = "検索に失敗しました: \(error.localizedDescription)"
                    searchResults = []
                }
            }
        }
    }

    /// 経路を計算
    func calculateRoute(to destination: CLLocationCoordinate2D) async {
        guard let userLocation = locationManager.location else {
            errorMessage = "現在地を取得できません"
            return
        }

        isLoading = true
        defer { isLoading = false }

        do {
            let request = MKDirections.Request()
            request.source = MKMapItem.forCurrentLocation()
            request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destination))
            request.transportType = .automobile

            let directions = MKDirections(request: request)
            let response = try await directions.calculate()

            if let firstRoute = response.routes.first {
                route = firstRoute

                // 経路全体が見えるようにカメラを調整
                let rect = firstRoute.polyline.boundingMapRect
                cameraPosition = .rect(rect)
            }

            errorMessage = nil
        } catch {
            errorMessage = "経路の計算に失敗しました: \(error.localizedDescription)"
            route = nil
        }
    }

    /// 経路をクリア
    func clearRoute() {
        route = nil
    }

    /// 検索結果から場所を追加
    func addPlaceFromSearchResult(_ mapItem: MKMapItem, category: PlaceCategory) {
        let place = Place(
            name: mapItem.name ?? "Unknown",
            coordinate: mapItem.placemark.coordinate,
            category: category
        )
        places.append(place)
    }

    /// 表示領域を更新
    func updateVisibleRegion(_ region: MKCoordinateRegion) {
        visibleRegion = region
    }

    /// サンプルデータを読み込み
    func loadSamplePlaces() {
        places = [
            Place(name: "東京駅", coordinate: CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671), category: .landmark),
            Place(name: "渋谷駅", coordinate: CLLocationCoordinate2D(latitude: 35.6580, longitude: 139.7016), category: .landmark),
            Place(name: "新宿駅", coordinate: CLLocationCoordinate2D(latitude: 35.6896, longitude: 139.7006), category: .landmark),
            Place(name: "カフェA", coordinate: CLLocationCoordinate2D(latitude: 35.6800, longitude: 139.7650), category: .cafe),
            Place(name: "レストランB", coordinate: CLLocationCoordinate2D(latitude: 35.6590, longitude: 139.7030), category: .restaurant)
        ]
    }
}

// MARK: - Location Manager

/// 位置情報を管理
@MainActor
@Observable
final class LocationManager: NSObject, CLLocationManagerDelegate {
    var location: CLLocation?
    var authorizationStatus: CLAuthorizationStatus = .notDetermined

    private let manager = CLLocationManager()

    override init() {
        super.init()
        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyBest
        authorizationStatus = manager.authorizationStatus
    }

    func requestAuthorization() {
        manager.requestWhenInUseAuthorization()
    }

    func startUpdating() {
        manager.startUpdatingLocation()
    }

    func stopUpdating() {
        manager.stopUpdatingLocation()
    }

    // MARK: - CLLocationManagerDelegate

    nonisolated func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        Task { @MainActor in
            location = locations.last
        }
    }

    nonisolated func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        Task { @MainActor in
            authorizationStatus = manager.authorizationStatus

            if authorizationStatus == .authorizedWhenInUse || authorizationStatus == .authorizedAlways {
                self.manager.startUpdatingLocation()
            }
        }
    }

    nonisolated func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        print("Location error: \(error.localizedDescription)")
    }
}

// MARK: - Map View with ViewModel

/// ViewModelを使用した地図ビュー
struct MapWithViewModelView: View {
    @State private var viewModel = MapViewModel()
    @State private var searchText = ""

    var body: some View {
        ZStack {
            // 地図
            Map(position: $viewModel.cameraPosition, selection: $viewModel.selectedPlace) {
                // ユーザー位置
                UserAnnotation()

                // 場所マーカー
                ForEach(viewModel.places) { place in
                    Marker(place.name, systemImage: place.category.systemImage, coordinate: place.coordinate)
                        .tint(place.category.color)
                        .tag(place)
                }

                // 検索結果
                ForEach(viewModel.searchResults, id: \.self) { item in
                    Marker(item.name ?? "", coordinate: item.placemark.coordinate)
                        .tint(.red)
                }

                // 経路
                if let route = viewModel.route {
                    MapPolyline(route.polyline)
                        .stroke(.blue, lineWidth: 5)
                }
            }
            .mapControls {
                MapUserLocationButton()
                MapCompass()
                MapScaleView()
            }
            .onMapCameraChange { context in
                viewModel.updateVisibleRegion(context.region)
            }

            // オーバーレイUI
            VStack {
                // 検索バー
                HStack {
                    Image(systemName: "magnifyingglass")
                        .foregroundStyle(.secondary)

                    TextField("場所を検索", text: $searchText)
                        .textFieldStyle(.plain)
                        .onChange(of: searchText) { _, newValue in
                            Task {
                                await viewModel.searchNearby(query: newValue)
                            }
                        }

                    if viewModel.isLoading {
                        ProgressView()
                            .scaleEffect(0.8)
                    }
                }
                .padding()
                .background(.regularMaterial)
                .clipShape(RoundedRectangle(cornerRadius: 12))
                .padding()

                Spacer()

                // 選択中の場所情報
                if let place = viewModel.selectedPlace {
                    PlaceDetailCard(place: place) {
                        Task {
                            await viewModel.calculateRoute(to: place.coordinate)
                        }
                    }
                    .padding()
                }

                // 経路情報
                if let route = viewModel.route {
                    RouteInfoCard(route: route) {
                        viewModel.clearRoute()
                    }
                    .padding()
                }
            }
        }
        .onAppear {
            viewModel.loadSamplePlaces()
        }
    }
}

// MARK: - Supporting Views

/// 場所の詳細カード
struct PlaceDetailCard: View {
    let place: Place
    let onRouteRequest: () -> Void

    var body: some View {
        HStack {
            VStack(alignment: .leading) {
                Text(place.name)
                    .font(.headline)
                Text(place.category.rawValue)
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }

            Spacer()

            Button("経路", action: onRouteRequest)
                .buttonStyle(.borderedProminent)
        }
        .padding()
        .background(.regularMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}

/// 経路情報カード
struct RouteInfoCard: View {
    let route: MKRoute
    let onClear: () -> Void

    var body: some View {
        HStack {
            VStack(alignment: .leading) {
                Text("経路")
                    .font(.headline)
                HStack {
                    Label(formatDistance(route.distance), systemImage: "car.fill")
                    Label(formatTime(route.expectedTravelTime), systemImage: "clock")
                }
                .font(.caption)
                .foregroundStyle(.secondary)
            }

            Spacer()

            Button("クリア", action: onClear)
                .buttonStyle(.bordered)
        }
        .padding()
        .background(.regularMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }

    private func formatDistance(_ meters: CLLocationDistance) -> String {
        if meters >= 1000 {
            return String(format: "%.1f km", meters / 1000)
        }
        return String(format: "%.0f m", meters)
    }

    private func formatTime(_ seconds: TimeInterval) -> String {
        let minutes = Int(seconds) / 60
        if minutes >= 60 {
            let hours = minutes / 60
            let mins = minutes % 60
            return "\(hours)時間\(mins)分"
        }
        return "\(minutes)分"
    }
}

// MARK: - Preview

#Preview {
    MapWithViewModelView()
}
