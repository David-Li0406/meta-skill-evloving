// Tesla Dashboard UI - Map View
// MapKit統合ナビゲーション
// ルート検索 + LookAround + 音声案内(AVSpeechSynthesizer)

import SwiftUI
import MapKit
import CoreLocation
import AVFoundation

// MARK: - Tesla Map View

/// Tesla風マップビュー
/// MapKit統合とナビゲーション機能
struct TeslaMapView: View {
    // MARK: - Properties

    @ObservedObject var navigationManager: TeslaNavigationManager
    var isFullScreen: Bool = false
    var onExpandTap: (() -> Void)? = nil

    // MARK: - Environment

    @Environment(\.teslaTheme) private var theme

    // MARK: - State

    @State private var cameraPosition: MapCameraPosition = .automatic

    // MARK: - Body

    var body: some View {
        ZStack {
            // Map
            mapContent

            // Overlay Controls
            VStack {
                if !isFullScreen {
                    // Expand Button
                    HStack {
                        Spacer()
                        expandButton
                    }
                    .padding(16)
                }

                Spacer()

                // Navigation Info (if navigating)
                if navigationManager.isNavigating {
                    navigationInfoBar
                }
            }

            // Search Overlay (when not navigating)
            if !navigationManager.isNavigating && !isFullScreen {
                VStack {
                    searchBar
                        .padding(16)
                    Spacer()
                }
            }
        }
        .clipShape(RoundedRectangle(cornerRadius: isFullScreen ? 0 : 16))
        .onChange(of: navigationManager.currentLocation) { _, newLocation in
            if let location = newLocation {
                updateCamera(to: location)
            }
        }
    }

    // MARK: - Map Content

    private var mapContent: some View {
        Map(position: $cameraPosition) {
            // User Location
            if let location = navigationManager.currentLocation {
                Annotation("現在地", coordinate: location) {
                    ZStack {
                        Circle()
                            .fill(TeslaColors.accent.opacity(0.3))
                            .frame(width: 40, height: 40)

                        Circle()
                            .fill(TeslaColors.accent)
                            .frame(width: 16, height: 16)

                        // Heading Indicator
                        if let heading = navigationManager.currentHeading {
                            Triangle()
                                .fill(TeslaColors.accent)
                                .frame(width: 8, height: 12)
                                .rotationEffect(.degrees(heading))
                                .offset(y: -20)
                        }
                    }
                }
            }

            // Destination
            if let destination = navigationManager.destination {
                Annotation(destination.name, coordinate: destination.coordinate) {
                    VStack(spacing: 4) {
                        Image(systemName: "mappin.circle.fill")
                            .font(.system(size: 32))
                            .foregroundStyle(TeslaColors.statusRed)

                        Text(destination.name)
                            .font(TeslaTypography.labelSmall)
                            .foregroundStyle(TeslaColors.textPrimary)
                            .padding(.horizontal, 8)
                            .padding(.vertical, 4)
                            .background(TeslaColors.surface)
                            .clipShape(RoundedRectangle(cornerRadius: 4))
                    }
                }
            }

            // Route
            if let route = navigationManager.currentRoute {
                MapPolyline(route.polyline)
                    .stroke(TeslaColors.accent, lineWidth: 6)
            }

            // Charging Stations
            ForEach(navigationManager.nearbyChargingStations) { station in
                Annotation(station.name, coordinate: station.coordinate) {
                    Image(systemName: "bolt.circle.fill")
                        .font(.system(size: 24))
                        .foregroundStyle(TeslaColors.statusGreen)
                }
            }
        }
        .mapStyle(.standard(elevation: .realistic, pointsOfInterest: .including([.parking, .gasStation])))
        .mapControls {
            MapCompass()
            MapScaleView()
        }
    }

    // MARK: - Expand Button

    private var expandButton: some View {
        Button {
            onExpandTap?()
        } label: {
            Image(systemName: "arrow.up.left.and.arrow.down.right")
                .font(.system(size: 14, weight: .semibold))
                .foregroundStyle(TeslaColors.textPrimary)
                .frame(width: 36, height: 36)
                .background(TeslaColors.glassBackground)
                .clipShape(Circle())
        }
        .buttonStyle(TeslaScaleButtonStyle())
    }

    // MARK: - Search Bar

    private var searchBar: some View {
        Button {
            // Open search
        } label: {
            HStack(spacing: 12) {
                Image(systemName: "magnifyingglass")
                    .font(.system(size: 16))
                    .foregroundStyle(TeslaColors.textSecondary)

                Text("目的地を検索")
                    .font(TeslaTypography.bodyMedium)
                    .foregroundStyle(TeslaColors.textSecondary)

                Spacer()
            }
            .padding(16)
            .background(TeslaColors.surface.opacity(0.95))
            .clipShape(RoundedRectangle(cornerRadius: 12))
        }
    }

    // MARK: - Navigation Info Bar

    private var navigationInfoBar: some View {
        VStack(spacing: 0) {
            // Current Instruction
            if let instruction = navigationManager.currentInstruction {
                HStack(spacing: 16) {
                    // Maneuver Icon
                    Image(systemName: instruction.maneuverIcon)
                        .font(.system(size: 32))
                        .foregroundStyle(TeslaColors.accent)
                        .frame(width: 56, height: 56)
                        .background(TeslaColors.glassBackground)
                        .clipShape(Circle())

                    VStack(alignment: .leading, spacing: 4) {
                        // Distance
                        Text(instruction.formattedDistance)
                            .font(TeslaTypography.displaySmall)
                            .foregroundStyle(TeslaColors.textPrimary)

                        // Instruction
                        Text(instruction.text)
                            .font(TeslaTypography.bodyMedium)
                            .foregroundStyle(TeslaColors.textSecondary)
                            .lineLimit(2)
                    }

                    Spacer()
                }
                .padding(16)
            }

            Divider()
                .background(TeslaColors.glassBorder)

            // ETA & Distance Summary
            HStack {
                // ETA
                VStack(alignment: .leading, spacing: 2) {
                    Text("到着予定")
                        .font(TeslaTypography.labelSmall)
                        .foregroundStyle(TeslaColors.textTertiary)

                    Text(navigationManager.formattedETA)
                        .font(TeslaTypography.titleMedium)
                        .foregroundStyle(TeslaColors.textPrimary)
                }

                Spacer()

                // Remaining Distance
                VStack(alignment: .center, spacing: 2) {
                    Text("残り距離")
                        .font(TeslaTypography.labelSmall)
                        .foregroundStyle(TeslaColors.textTertiary)

                    Text(navigationManager.formattedRemainingDistance)
                        .font(TeslaTypography.titleMedium)
                        .foregroundStyle(TeslaColors.textPrimary)
                }

                Spacer()

                // End Navigation Button
                Button {
                    navigationManager.stopNavigation()
                } label: {
                    Text("終了")
                        .font(TeslaTypography.labelMedium)
                        .foregroundStyle(TeslaColors.statusRed)
                        .padding(.horizontal, 16)
                        .padding(.vertical, 8)
                        .background(TeslaColors.statusRed.opacity(0.2))
                        .clipShape(RoundedRectangle(cornerRadius: 8))
                }
            }
            .padding(16)
        }
        .background(TeslaColors.surface.opacity(0.95))
        .clipShape(RoundedRectangle(cornerRadius: 16))
        .padding(16)
    }

    // MARK: - Camera

    private func updateCamera(to coordinate: CLLocationCoordinate2D) {
        withAnimation {
            cameraPosition = .camera(MapCamera(
                centerCoordinate: coordinate,
                distance: 1000,
                heading: navigationManager.currentHeading ?? 0,
                pitch: 45
            ))
        }
    }
}

// MARK: - Triangle Shape

struct Triangle: Shape {
    func path(in rect: CGRect) -> Path {
        var path = Path()
        path.move(to: CGPoint(x: rect.midX, y: rect.minY))
        path.addLine(to: CGPoint(x: rect.maxX, y: rect.maxY))
        path.addLine(to: CGPoint(x: rect.minX, y: rect.maxY))
        path.closeSubpath()
        return path
    }
}

// MARK: - Tesla Navigation Manager

/// ナビゲーション管理クラス
@MainActor
final class TeslaNavigationManager: NSObject, ObservableObject {
    // MARK: - Published Properties

    @Published var currentLocation: CLLocationCoordinate2D?
    @Published var currentHeading: Double?
    @Published var destination: TeslaDestination?
    @Published var currentRoute: MKRoute?
    @Published var currentInstruction: TeslaNavigationInstruction?
    @Published var isNavigating: Bool = false
    @Published var nearbyChargingStations: [TeslaChargingStation] = []

    // Remaining
    @Published var remainingDistance: CLLocationDistance = 0
    @Published var remainingTime: TimeInterval = 0
    @Published var eta: Date?

    // MARK: - Private Properties

    private let locationManager = CLLocationManager()
    private let speechSynthesizer = AVSpeechSynthesizer()
    private var routeSteps: [MKRoute.Step] = []
    private var currentStepIndex: Int = 0

    // MARK: - Computed Properties

    var formattedETA: String {
        guard let eta else { return "--:--" }
        let formatter = DateFormatter()
        formatter.dateFormat = "HH:mm"
        return formatter.string(from: eta)
    }

    var formattedRemainingDistance: String {
        if remainingDistance < 1000 {
            return String(format: "%.0f m", remainingDistance)
        } else {
            return String(format: "%.1f km", remainingDistance / 1000)
        }
    }

    // MARK: - Initialization

    override init() {
        super.init()
        setupLocationManager()
    }

    private func setupLocationManager() {
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBestForNavigation
        locationManager.requestWhenInUseAuthorization()
    }

    // MARK: - Navigation Methods

    func startNavigation(to destination: TeslaDestination) async -> TeslaResult<MKRoute> {
        self.destination = destination

        // Calculate route
        let request = MKDirections.Request()
        request.source = MKMapItem.forCurrentLocation()
        request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destination.coordinate))
        request.transportType = .automobile

        let directions = MKDirections(request: request)

        do {
            let response = try await directions.calculate()
            guard let route = response.routes.first else {
                return .failure(.routeCalculationFailed(reason: "ルートが見つかりません"))
            }

            self.currentRoute = route
            self.routeSteps = route.steps
            self.currentStepIndex = 0
            self.remainingDistance = route.distance
            self.remainingTime = route.expectedTravelTime
            self.eta = Date().addingTimeInterval(route.expectedTravelTime)
            self.isNavigating = true

            // Start location updates
            locationManager.startUpdatingLocation()
            locationManager.startUpdatingHeading()

            // Announce first instruction
            updateCurrentInstruction()

            return .success(route)
        } catch {
            return .failure(.routeCalculationFailed(reason: error.localizedDescription))
        }
    }

    func stopNavigation() {
        isNavigating = false
        destination = nil
        currentRoute = nil
        currentInstruction = nil
        routeSteps = []
        currentStepIndex = 0

        locationManager.stopUpdatingLocation()
        locationManager.stopUpdatingHeading()
        speechSynthesizer.stopSpeaking(at: .immediate)
    }

    // MARK: - Voice Guidance

    func speak(_ text: String) {
        guard !speechSynthesizer.isSpeaking else { return }

        let utterance = AVSpeechUtterance(string: text)
        utterance.voice = AVSpeechSynthesisVoice(language: "ja-JP")
        utterance.rate = 0.5
        utterance.pitchMultiplier = 1.0
        utterance.volume = 1.0

        speechSynthesizer.speak(utterance)
    }

    // MARK: - Private Methods

    private func updateCurrentInstruction() {
        guard currentStepIndex < routeSteps.count else {
            // Arrived
            currentInstruction = TeslaNavigationInstruction(
                text: "目的地に到着しました",
                distance: 0,
                maneuverType: .arrive
            )
            speak("目的地に到着しました")
            return
        }

        let step = routeSteps[currentStepIndex]
        let instruction = TeslaNavigationInstruction(
            text: step.instructions,
            distance: step.distance,
            maneuverType: ManeuverType.from(step.instructions)
        )

        currentInstruction = instruction

        // Voice guidance
        if step.distance > 0 {
            speak("\(instruction.formattedDistance)先、\(step.instructions)")
        }
    }

    private func checkStepProgress(location: CLLocation) {
        guard currentStepIndex < routeSteps.count else { return }

        let step = routeSteps[currentStepIndex]
        let stepEndLocation = CLLocation(
            latitude: step.polyline.coordinate.latitude,
            longitude: step.polyline.coordinate.longitude
        )

        let distanceToStepEnd = location.distance(from: stepEndLocation)

        // Move to next step if close enough
        if distanceToStepEnd < 50 {
            currentStepIndex += 1
            updateCurrentInstruction()
        }

        // Update remaining distance
        remainingDistance = routeSteps.dropFirst(currentStepIndex).reduce(0) { $0 + $1.distance }
    }
}

// MARK: - CLLocationManagerDelegate

extension TeslaNavigationManager: CLLocationManagerDelegate {
    nonisolated func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard let location = locations.last else { return }

        Task { @MainActor in
            self.currentLocation = location.coordinate

            if self.isNavigating {
                self.checkStepProgress(location: location)
            }
        }
    }

    nonisolated func locationManager(_ manager: CLLocationManager, didUpdateHeading newHeading: CLHeading) {
        Task { @MainActor in
            self.currentHeading = newHeading.trueHeading
        }
    }

    nonisolated func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        Task { @MainActor in
            if manager.authorizationStatus == .authorizedWhenInUse ||
               manager.authorizationStatus == .authorizedAlways {
                manager.startUpdatingLocation()
            }
        }
    }
}

// MARK: - Supporting Types

/// 目的地
struct TeslaDestination: Identifiable {
    let id: String
    let name: String
    let coordinate: CLLocationCoordinate2D
    let address: String?

    init(id: String = UUID().uuidString, name: String, coordinate: CLLocationCoordinate2D, address: String? = nil) {
        self.id = id
        self.name = name
        self.coordinate = coordinate
        self.address = address
    }
}

/// 充電スポット
struct TeslaChargingStation: Identifiable {
    let id: String
    let name: String
    let coordinate: CLLocationCoordinate2D
    let chargerType: String
    let power: Double
    let available: Int
    let total: Int
}

/// ナビゲーション指示
struct TeslaNavigationInstruction {
    let text: String
    let distance: CLLocationDistance
    let maneuverType: ManeuverType

    var formattedDistance: String {
        if distance < 1000 {
            return String(format: "%.0f m", distance)
        } else {
            return String(format: "%.1f km", distance / 1000)
        }
    }

    var maneuverIcon: String {
        maneuverType.iconName
    }
}

/// マニューバータイプ
enum ManeuverType {
    case straight
    case slightLeft
    case slightRight
    case left
    case right
    case sharpLeft
    case sharpRight
    case uTurn
    case merge
    case arrive
    case depart

    var iconName: String {
        switch self {
        case .straight: return "arrow.up"
        case .slightLeft: return "arrow.up.left"
        case .slightRight: return "arrow.up.right"
        case .left: return "arrow.turn.up.left"
        case .right: return "arrow.turn.up.right"
        case .sharpLeft: return "arrow.turn.left.up"
        case .sharpRight: return "arrow.turn.right.up"
        case .uTurn: return "arrow.uturn.left"
        case .merge: return "arrow.merge"
        case .arrive: return "mappin.circle.fill"
        case .depart: return "location.fill"
        }
    }

    static func from(_ instruction: String) -> ManeuverType {
        let lowercased = instruction.lowercased()

        if lowercased.contains("左折") || lowercased.contains("left") {
            if lowercased.contains("斜め") || lowercased.contains("slight") {
                return .slightLeft
            }
            return .left
        }
        if lowercased.contains("右折") || lowercased.contains("right") {
            if lowercased.contains("斜め") || lowercased.contains("slight") {
                return .slightRight
            }
            return .right
        }
        if lowercased.contains("uターン") || lowercased.contains("u-turn") {
            return .uTurn
        }
        if lowercased.contains("合流") || lowercased.contains("merge") {
            return .merge
        }
        if lowercased.contains("到着") || lowercased.contains("arrive") {
            return .arrive
        }

        return .straight
    }
}

// MARK: - Preview

#Preview("Tesla Map View") {
    struct MapPreview: View {
        @StateObject private var navigationManager = TeslaNavigationManager()

        var body: some View {
            TeslaMapView(
                navigationManager: navigationManager,
                isFullScreen: false,
                onExpandTap: {
                    print("Expand tapped")
                }
            )
            .frame(height: 400)
            .padding(24)
            .background(TeslaColors.background)
        }
    }

    return MapPreview()
}
