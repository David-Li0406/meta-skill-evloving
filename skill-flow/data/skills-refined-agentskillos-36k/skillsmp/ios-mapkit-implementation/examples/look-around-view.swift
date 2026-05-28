// MARK: - Look Around View Example
// iOS 17+ SwiftUI MapKit Look Around機能

import SwiftUI
import MapKit

// MARK: - 基本的なLook Around

/// 座標を指定してLook Aroundを表示
struct BasicLookAroundView: View {
    let coordinate = CLLocationCoordinate2D(latitude: 35.6586, longitude: 139.7454) // 東京タワー
    @State private var scene: MKLookAroundScene?
    @State private var isLoading = true

    var body: some View {
        VStack {
            if isLoading {
                ProgressView("Look Aroundを読み込み中...")
            } else if let scene {
                LookAroundPreview(scene: scene)
                    .frame(height: 300)
                    .clipShape(RoundedRectangle(cornerRadius: 12))
            } else {
                ContentUnavailableView(
                    "Look Around利用不可",
                    systemImage: "eye.slash",
                    description: Text("この場所ではLook Aroundを利用できません")
                )
            }

            Spacer()
        }
        .padding()
        .task {
            await loadScene()
        }
    }

    private func loadScene() async {
        isLoading = true
        defer { isLoading = false }

        let request = MKLookAroundSceneRequest(coordinate: coordinate)
        scene = try? await request.scene
    }
}

// MARK: - 地図とLook Aroundの連携

/// 地図上の場所を選択してLook Aroundを表示
struct MapWithLookAroundView: View {
    @State private var position: MapCameraPosition = .automatic
    @State private var selectedPlace: LookAroundPlace?
    @State private var lookAroundScene: MKLookAroundScene?
    @State private var showLookAround = false

    let places: [LookAroundPlace] = [
        LookAroundPlace(name: "東京タワー", coordinate: CLLocationCoordinate2D(latitude: 35.6586, longitude: 139.7454)),
        LookAroundPlace(name: "渋谷スクランブル交差点", coordinate: CLLocationCoordinate2D(latitude: 35.6595, longitude: 139.7004)),
        LookAroundPlace(name: "浅草寺", coordinate: CLLocationCoordinate2D(latitude: 35.7148, longitude: 139.7967))
    ]

    var body: some View {
        VStack(spacing: 0) {
            // 地図
            Map(position: $position, selection: $selectedPlace) {
                ForEach(places) { place in
                    Marker(place.name, coordinate: place.coordinate)
                        .tag(place)
                }
            }
            .onChange(of: selectedPlace) { _, newPlace in
                if let place = newPlace {
                    Task {
                        await loadLookAround(for: place.coordinate)
                    }
                }
            }

            // Look Aroundプレビュー
            if showLookAround, let scene = lookAroundScene {
                VStack(spacing: 0) {
                    HStack {
                        Text(selectedPlace?.name ?? "")
                            .font(.headline)
                        Spacer()
                        Button {
                            showLookAround = false
                        } label: {
                            Image(systemName: "xmark.circle.fill")
                                .font(.title2)
                        }
                    }
                    .padding()
                    .background(.regularMaterial)

                    LookAroundPreview(scene: scene)
                        .frame(height: 200)
                }
                .transition(.move(edge: .bottom))
            }
        }
        .animation(.easeInOut, value: showLookAround)
    }

    private func loadLookAround(for coordinate: CLLocationCoordinate2D) async {
        let request = MKLookAroundSceneRequest(coordinate: coordinate)

        if let scene = try? await request.scene {
            lookAroundScene = scene
            showLookAround = true
        } else {
            showLookAround = false
        }
    }
}

struct LookAroundPlace: Identifiable, Equatable, Hashable {
    let id = UUID()
    let name: String
    let coordinate: CLLocationCoordinate2D

    static func == (lhs: LookAroundPlace, rhs: LookAroundPlace) -> Bool {
        lhs.id == rhs.id
    }

    func hash(into hasher: inout Hasher) {
        hasher.combine(id)
    }
}

// MARK: - Look Aroundの可用性チェック

/// Look Aroundが利用可能かどうかを表示
struct LookAroundAvailabilityView: View {
    @State private var places: [PlaceWithAvailability] = []

    let coordinates: [(String, CLLocationCoordinate2D)] = [
        ("東京タワー", CLLocationCoordinate2D(latitude: 35.6586, longitude: 139.7454)),
        ("富士山頂", CLLocationCoordinate2D(latitude: 35.3606, longitude: 138.7274)),
        ("渋谷駅", CLLocationCoordinate2D(latitude: 35.6580, longitude: 139.7016)),
        ("皇居", CLLocationCoordinate2D(latitude: 35.6852, longitude: 139.7528))
    ]

    var body: some View {
        List(places) { place in
            HStack {
                VStack(alignment: .leading) {
                    Text(place.name)
                        .font(.headline)
                    Text("\(place.coordinate.latitude, specifier: "%.4f"), \(place.coordinate.longitude, specifier: "%.4f")")
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }

                Spacer()

                if place.isChecking {
                    ProgressView()
                } else {
                    Image(systemName: place.isAvailable ? "checkmark.circle.fill" : "xmark.circle.fill")
                        .foregroundStyle(place.isAvailable ? .green : .red)
                }
            }
        }
        .navigationTitle("Look Around 可用性")
        .task {
            await checkAvailability()
        }
    }

    private func checkAvailability() async {
        // 初期データを設定
        places = coordinates.map {
            PlaceWithAvailability(name: $0.0, coordinate: $0.1)
        }

        // 並行してチェック
        await withTaskGroup(of: (Int, Bool).self) { group in
            for (index, place) in places.enumerated() {
                group.addTask {
                    let request = MKLookAroundSceneRequest(coordinate: place.coordinate)
                    let available = (try? await request.scene) != nil
                    return (index, available)
                }
            }

            for await (index, available) in group {
                places[index].isAvailable = available
                places[index].isChecking = false
            }
        }
    }
}

struct PlaceWithAvailability: Identifiable {
    let id = UUID()
    let name: String
    let coordinate: CLLocationCoordinate2D
    var isAvailable = false
    var isChecking = true
}

// MARK: - フルスクリーンLook Around

/// フルスクリーンでLook Aroundを表示
struct FullScreenLookAroundView: View {
    let coordinate: CLLocationCoordinate2D
    @State private var scene: MKLookAroundScene?
    @State private var showFullScreen = false
    @State private var isLoading = true

    var body: some View {
        VStack(spacing: 20) {
            if isLoading {
                ProgressView()
            } else if let scene {
                // プレビュー
                LookAroundPreview(scene: scene)
                    .frame(height: 200)
                    .clipShape(RoundedRectangle(cornerRadius: 12))

                // フルスクリーンボタン
                Button {
                    showFullScreen = true
                } label: {
                    Label("フルスクリーンで表示", systemImage: "arrow.up.left.and.arrow.down.right")
                }
                .buttonStyle(.borderedProminent)
            } else {
                ContentUnavailableView(
                    "利用不可",
                    systemImage: "eye.slash",
                    description: Text("Look Aroundはこの場所で利用できません")
                )
            }
        }
        .padding()
        .fullScreenCover(isPresented: $showFullScreen) {
            if let scene {
                LookAroundFullScreenWrapper(scene: scene) {
                    showFullScreen = false
                }
            }
        }
        .task {
            await loadScene()
        }
    }

    private func loadScene() async {
        isLoading = true
        defer { isLoading = false }

        let request = MKLookAroundSceneRequest(coordinate: coordinate)
        scene = try? await request.scene
    }
}

struct LookAroundFullScreenWrapper: UIViewControllerRepresentable {
    let scene: MKLookAroundScene
    let onDismiss: () -> Void

    func makeUIViewController(context: Context) -> MKLookAroundViewController {
        let controller = MKLookAroundViewController(scene: scene)
        controller.delegate = context.coordinator
        return controller
    }

    func updateUIViewController(_ uiViewController: MKLookAroundViewController, context: Context) {
        uiViewController.scene = scene
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(onDismiss: onDismiss)
    }

    class Coordinator: NSObject, MKLookAroundViewControllerDelegate {
        let onDismiss: () -> Void

        init(onDismiss: @escaping () -> Void) {
            self.onDismiss = onDismiss
        }

        func lookAroundViewControllerDidDismissFullScreen(_ viewController: MKLookAroundViewController) {
            onDismiss()
        }
    }
}

// MARK: - 場所詳細カード with Look Around

/// 場所の詳細にLook Aroundを統合
struct PlaceDetailWithLookAroundView: View {
    let place: DetailPlace
    @State private var lookAroundScene: MKLookAroundScene?
    @State private var position: MapCameraPosition

    init(place: DetailPlace) {
        self.place = place
        self._position = State(initialValue: .region(MKCoordinateRegion(
            center: place.coordinate,
            span: MKCoordinateSpan(latitudeDelta: 0.005, longitudeDelta: 0.005)
        )))
    }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                // 場所情報
                VStack(alignment: .leading, spacing: 8) {
                    Text(place.name)
                        .font(.title)
                        .fontWeight(.bold)

                    Text(place.address)
                        .font(.subheadline)
                        .foregroundStyle(.secondary)

                    if let description = place.description {
                        Text(description)
                            .font(.body)
                    }
                }
                .padding(.horizontal)

                // Look Aroundプレビュー
                VStack(alignment: .leading, spacing: 8) {
                    Text("Look Around")
                        .font(.headline)
                        .padding(.horizontal)

                    if let scene = lookAroundScene {
                        LookAroundPreview(scene: scene)
                            .frame(height: 200)
                    } else {
                        HStack {
                            Spacer()
                            VStack {
                                Image(systemName: "binoculars")
                                    .font(.largeTitle)
                                    .foregroundStyle(.secondary)
                                Text("Look Around利用不可")
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                            }
                            Spacer()
                        }
                        .frame(height: 200)
                        .background(Color.gray.opacity(0.1))
                    }
                }

                // 地図
                VStack(alignment: .leading, spacing: 8) {
                    Text("地図")
                        .font(.headline)
                        .padding(.horizontal)

                    Map(position: $position) {
                        Marker(place.name, coordinate: place.coordinate)
                    }
                    .frame(height: 200)
                    .clipShape(RoundedRectangle(cornerRadius: 12))
                    .padding(.horizontal)
                }

                // アクションボタン
                HStack(spacing: 16) {
                    Button {
                        openInMaps()
                    } label: {
                        Label("経路", systemImage: "arrow.triangle.turn.up.right.diamond")
                            .frame(maxWidth: .infinity)
                    }
                    .buttonStyle(.borderedProminent)

                    Button {
                        shareLocation()
                    } label: {
                        Label("共有", systemImage: "square.and.arrow.up")
                            .frame(maxWidth: .infinity)
                    }
                    .buttonStyle(.bordered)
                }
                .padding(.horizontal)
            }
            .padding(.vertical)
        }
        .task {
            await loadLookAround()
        }
    }

    private func loadLookAround() async {
        let request = MKLookAroundSceneRequest(coordinate: place.coordinate)
        lookAroundScene = try? await request.scene
    }

    private func openInMaps() {
        let mapItem = MKMapItem(placemark: MKPlacemark(coordinate: place.coordinate))
        mapItem.name = place.name
        mapItem.openInMaps(launchOptions: [
            MKLaunchOptionsDirectionsModeKey: MKLaunchOptionsDirectionsModeDriving
        ])
    }

    private func shareLocation() {
        // 共有機能の実装
    }
}

struct DetailPlace {
    let name: String
    let address: String
    let description: String?
    let coordinate: CLLocationCoordinate2D
}

// MARK: - Preview

#Preview("Basic Look Around") {
    BasicLookAroundView()
}

#Preview("Map with Look Around") {
    MapWithLookAroundView()
}

#Preview("Availability Check") {
    NavigationStack {
        LookAroundAvailabilityView()
    }
}

#Preview("Full Screen") {
    FullScreenLookAroundView(
        coordinate: CLLocationCoordinate2D(latitude: 35.6586, longitude: 139.7454)
    )
}

#Preview("Place Detail") {
    PlaceDetailWithLookAroundView(
        place: DetailPlace(
            name: "東京タワー",
            address: "東京都港区芝公園4丁目2-8",
            description: "東京のシンボルとして知られる電波塔。高さ333メートル。",
            coordinate: CLLocationCoordinate2D(latitude: 35.6586, longitude: 139.7454)
        )
    )
}
