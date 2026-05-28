// MARK: - Directions View Example
// iOS 17+ SwiftUI MapKit 経路検索とナビゲーション

import SwiftUI
import MapKit

// MARK: - 基本的な経路表示

/// 2地点間の経路を表示
struct BasicDirectionsView: View {
    @State private var route: MKRoute?
    @State private var position: MapCameraPosition = .automatic
    @State private var isLoading = false

    let source = CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671)       // 東京駅
    let destination = CLLocationCoordinate2D(latitude: 35.6586, longitude: 139.7454)  // 東京タワー

    var body: some View {
        ZStack {
            Map(position: $position) {
                // 出発地マーカー
                Marker("出発", systemImage: "figure.walk", coordinate: source)
                    .tint(.green)

                // 目的地マーカー
                Marker("到着", systemImage: "flag.fill", coordinate: destination)
                    .tint(.red)

                // 経路ライン
                if let route {
                    MapPolyline(route.polyline)
                        .stroke(.blue, lineWidth: 5)
                }
            }

            if isLoading {
                ProgressView()
                    .scaleEffect(1.5)
                    .padding()
                    .background(.regularMaterial)
                    .clipShape(RoundedRectangle(cornerRadius: 8))
            }
        }
        .task {
            await calculateRoute()
        }
    }

    private func calculateRoute() async {
        isLoading = true
        defer { isLoading = false }

        let request = MKDirections.Request()
        request.source = MKMapItem(placemark: MKPlacemark(coordinate: source))
        request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destination))
        request.transportType = .automobile

        let directions = MKDirections(request: request)

        do {
            let response = try await directions.calculate()
            route = response.routes.first

            // 経路全体が見えるようにカメラを調整
            if let route {
                let rect = route.polyline.boundingMapRect
                let padding = UIEdgeInsets(top: 50, left: 50, bottom: 50, right: 50)
                position = .rect(rect.insetBy(dx: -padding.left, dy: -padding.top))
            }
        } catch {
            print("経路計算エラー: \(error)")
        }
    }
}

// MARK: - 交通手段切り替え

/// 複数の交通手段で経路を比較
struct TransportTypeDirectionsView: View {
    @State private var selectedTransport: TransportType = .automobile
    @State private var route: MKRoute?
    @State private var position: MapCameraPosition = .automatic
    @State private var isLoading = false

    enum TransportType: String, CaseIterable {
        case automobile = "車"
        case walking = "徒歩"
        case transit = "公共交通"

        var mkType: MKDirectionsTransportType {
            switch self {
            case .automobile: return .automobile
            case .walking: return .walking
            case .transit: return .transit
            }
        }

        var icon: String {
            switch self {
            case .automobile: return "car.fill"
            case .walking: return "figure.walk"
            case .transit: return "tram.fill"
            }
        }
    }

    let source = CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671)
    let destination = CLLocationCoordinate2D(latitude: 35.6580, longitude: 139.7016)

    var body: some View {
        VStack(spacing: 0) {
            // 交通手段選択
            Picker("交通手段", selection: $selectedTransport) {
                ForEach(TransportType.allCases, id: \.self) { type in
                    Label(type.rawValue, systemImage: type.icon).tag(type)
                }
            }
            .pickerStyle(.segmented)
            .padding()
            .onChange(of: selectedTransport) { _, _ in
                Task {
                    await calculateRoute()
                }
            }

            // 地図
            ZStack {
                Map(position: $position) {
                    Marker("出発", systemImage: "location.fill", coordinate: source)
                        .tint(.green)
                    Marker("到着", systemImage: "mappin.circle.fill", coordinate: destination)
                        .tint(.red)

                    if let route {
                        MapPolyline(route.polyline)
                            .stroke(.blue, lineWidth: 5)
                    }
                }

                if isLoading {
                    ProgressView()
                }
            }

            // 経路情報
            if let route {
                RouteInfoPanel(route: route, transportType: selectedTransport)
            }
        }
        .task {
            await calculateRoute()
        }
    }

    private func calculateRoute() async {
        isLoading = true
        defer { isLoading = false }

        let request = MKDirections.Request()
        request.source = MKMapItem(placemark: MKPlacemark(coordinate: source))
        request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destination))
        request.transportType = selectedTransport.mkType

        let directions = MKDirections(request: request)

        do {
            let response = try await directions.calculate()
            route = response.routes.first

            if let route {
                position = .rect(route.polyline.boundingMapRect)
            }
        } catch {
            print("経路計算エラー: \(error)")
            route = nil
        }
    }
}

struct RouteInfoPanel: View {
    let route: MKRoute
    let transportType: TransportTypeDirectionsView.TransportType

    var body: some View {
        HStack(spacing: 20) {
            // 距離
            VStack {
                Image(systemName: "ruler")
                    .font(.title2)
                Text(formatDistance(route.distance))
                    .font(.headline)
                Text("距離")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }

            Divider()

            // 時間
            VStack {
                Image(systemName: "clock")
                    .font(.title2)
                Text(formatTime(route.expectedTravelTime))
                    .font(.headline)
                Text("所要時間")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }

            Divider()

            // 交通手段
            VStack {
                Image(systemName: transportType.icon)
                    .font(.title2)
                Text(transportType.rawValue)
                    .font(.headline)
                Text("移動手段")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
        }
        .padding()
        .background(.regularMaterial)
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

// MARK: - ターンバイターンナビゲーション

/// ターンバイターン案内を表示
struct TurnByTurnDirectionsView: View {
    @State private var route: MKRoute?
    @State private var position: MapCameraPosition = .automatic
    @State private var currentStepIndex = 0
    @State private var showSteps = false

    let source = CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671)
    let destination = CLLocationCoordinate2D(latitude: 35.6586, longitude: 139.7454)

    var body: some View {
        ZStack(alignment: .bottom) {
            Map(position: $position) {
                if let route {
                    MapPolyline(route.polyline)
                        .stroke(.blue, lineWidth: 5)

                    // 各ステップの開始点をマーク
                    ForEach(Array(route.steps.enumerated()), id: \.offset) { index, step in
                        if let firstPoint = step.polyline.points().first {
                            Annotation("", coordinate: firstPoint.coordinate) {
                                Circle()
                                    .fill(index == currentStepIndex ? .blue : .gray)
                                    .frame(width: 12, height: 12)
                                    .overlay {
                                        Circle()
                                            .stroke(.white, lineWidth: 2)
                                    }
                            }
                        }
                    }
                }
            }

            // ナビゲーションパネル
            if let route {
                VStack {
                    // 現在のステップ
                    if currentStepIndex < route.steps.count {
                        CurrentStepCard(
                            step: route.steps[currentStepIndex],
                            stepNumber: currentStepIndex + 1,
                            totalSteps: route.steps.count
                        )
                    }

                    // ステップリストボタン
                    Button {
                        showSteps.toggle()
                    } label: {
                        Label("全ステップを表示", systemImage: "list.bullet")
                    }
                    .buttonStyle(.borderedProminent)

                    // ナビゲーションボタン
                    HStack {
                        Button {
                            if currentStepIndex > 0 {
                                currentStepIndex -= 1
                                focusOnStep(route.steps[currentStepIndex])
                            }
                        } label: {
                            Image(systemName: "chevron.left")
                        }
                        .disabled(currentStepIndex == 0)

                        Spacer()

                        Text("\(currentStepIndex + 1) / \(route.steps.count)")
                            .font(.headline)

                        Spacer()

                        Button {
                            if currentStepIndex < route.steps.count - 1 {
                                currentStepIndex += 1
                                focusOnStep(route.steps[currentStepIndex])
                            }
                        } label: {
                            Image(systemName: "chevron.right")
                        }
                        .disabled(currentStepIndex == route.steps.count - 1)
                    }
                    .padding()
                }
                .padding()
                .background(.regularMaterial)
            }
        }
        .sheet(isPresented: $showSteps) {
            if let route {
                StepListView(steps: route.steps, currentStep: $currentStepIndex)
            }
        }
        .task {
            await calculateRoute()
        }
    }

    private func calculateRoute() async {
        let request = MKDirections.Request()
        request.source = MKMapItem(placemark: MKPlacemark(coordinate: source))
        request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destination))
        request.transportType = .automobile

        let directions = MKDirections(request: request)

        do {
            let response = try await directions.calculate()
            route = response.routes.first

            if let route {
                position = .rect(route.polyline.boundingMapRect)
            }
        } catch {
            print("経路計算エラー: \(error)")
        }
    }

    private func focusOnStep(_ step: MKRoute.Step) {
        let rect = step.polyline.boundingMapRect
        withAnimation {
            position = .rect(rect)
        }
    }
}

struct CurrentStepCard: View {
    let step: MKRoute.Step
    let stepNumber: Int
    let totalSteps: Int

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Image(systemName: stepIcon)
                    .font(.title)
                    .foregroundStyle(.blue)

                VStack(alignment: .leading) {
                    Text("ステップ \(stepNumber) / \(totalSteps)")
                        .font(.caption)
                        .foregroundStyle(.secondary)
                    Text(step.instructions.isEmpty ? "出発" : step.instructions)
                        .font(.headline)
                }

                Spacer()

                Text(formatDistance(step.distance))
                    .font(.title3)
                    .fontWeight(.semibold)
            }
        }
        .padding()
        .background(.white)
        .clipShape(RoundedRectangle(cornerRadius: 12))
        .shadow(radius: 4)
    }

    private var stepIcon: String {
        let instructions = step.instructions.lowercased()
        if instructions.contains("左") || instructions.contains("left") {
            return "arrow.turn.up.left"
        } else if instructions.contains("右") || instructions.contains("right") {
            return "arrow.turn.up.right"
        } else if instructions.contains("直進") || instructions.contains("straight") {
            return "arrow.up"
        } else if instructions.contains("到着") || instructions.contains("destination") {
            return "flag.fill"
        }
        return "arrow.forward"
    }

    private func formatDistance(_ meters: CLLocationDistance) -> String {
        if meters >= 1000 {
            return String(format: "%.1f km", meters / 1000)
        }
        return String(format: "%.0f m", meters)
    }
}

struct StepListView: View {
    let steps: [MKRoute.Step]
    @Binding var currentStep: Int
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            List {
                ForEach(Array(steps.enumerated()), id: \.offset) { index, step in
                    Button {
                        currentStep = index
                        dismiss()
                    } label: {
                        HStack {
                            Text("\(index + 1)")
                                .font(.caption)
                                .foregroundStyle(.white)
                                .frame(width: 24, height: 24)
                                .background(index == currentStep ? .blue : .gray)
                                .clipShape(Circle())

                            VStack(alignment: .leading) {
                                Text(step.instructions.isEmpty ? "出発" : step.instructions)
                                    .font(.body)
                                Text(formatDistance(step.distance))
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                            }
                        }
                    }
                    .buttonStyle(.plain)
                }
            }
            .navigationTitle("経路ステップ")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("閉じる") {
                        dismiss()
                    }
                }
            }
        }
    }

    private func formatDistance(_ meters: CLLocationDistance) -> String {
        if meters >= 1000 {
            return String(format: "%.1f km", meters / 1000)
        }
        return String(format: "%.0f m", meters)
    }
}

// MARK: - 複数経路の比較

/// 複数の代替経路を表示
struct AlternateRoutesView: View {
    @State private var routes: [MKRoute] = []
    @State private var selectedRoute: MKRoute?
    @State private var position: MapCameraPosition = .automatic

    let source = CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671)
    let destination = CLLocationCoordinate2D(latitude: 35.6580, longitude: 139.7016)

    var body: some View {
        VStack(spacing: 0) {
            Map(position: $position) {
                Marker("出発", coordinate: source)
                    .tint(.green)
                Marker("到着", coordinate: destination)
                    .tint(.red)

                ForEach(routes, id: \.name) { route in
                    MapPolyline(route.polyline)
                        .stroke(
                            selectedRoute?.name == route.name ? .blue : .gray.opacity(0.5),
                            lineWidth: selectedRoute?.name == route.name ? 5 : 3
                        )
                }
            }

            // 経路選択リスト
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 12) {
                    ForEach(routes, id: \.name) { route in
                        RouteOptionCard(
                            route: route,
                            isSelected: selectedRoute?.name == route.name
                        ) {
                            selectedRoute = route
                            position = .rect(route.polyline.boundingMapRect)
                        }
                    }
                }
                .padding()
            }
            .background(.regularMaterial)
        }
        .task {
            await calculateRoutes()
        }
    }

    private func calculateRoutes() async {
        let request = MKDirections.Request()
        request.source = MKMapItem(placemark: MKPlacemark(coordinate: source))
        request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destination))
        request.transportType = .automobile
        request.requestsAlternateRoutes = true

        let directions = MKDirections(request: request)

        do {
            let response = try await directions.calculate()
            routes = response.routes
            selectedRoute = routes.first

            if let route = selectedRoute {
                position = .rect(route.polyline.boundingMapRect)
            }
        } catch {
            print("経路計算エラー: \(error)")
        }
    }
}

struct RouteOptionCard: View {
    let route: MKRoute
    let isSelected: Bool
    let onSelect: () -> Void

    var body: some View {
        Button(action: onSelect) {
            VStack(alignment: .leading, spacing: 4) {
                Text(route.name)
                    .font(.headline)
                    .lineLimit(1)

                HStack {
                    Label(formatDistance(route.distance), systemImage: "ruler")
                    Label(formatTime(route.expectedTravelTime), systemImage: "clock")
                }
                .font(.caption)

                if route.hasTolls {
                    Label("有料道路", systemImage: "yensign.circle")
                        .font(.caption2)
                        .foregroundStyle(.orange)
                }
            }
            .padding()
            .background(isSelected ? Color.blue.opacity(0.1) : Color.gray.opacity(0.1))
            .overlay {
                RoundedRectangle(cornerRadius: 12)
                    .stroke(isSelected ? .blue : .clear, lineWidth: 2)
            }
            .clipShape(RoundedRectangle(cornerRadius: 12))
        }
        .buttonStyle(.plain)
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
            return "\(hours)h\(mins)m"
        }
        return "\(minutes)m"
    }
}

// MARK: - Preview

#Preview("Basic Directions") {
    BasicDirectionsView()
}

#Preview("Transport Types") {
    TransportTypeDirectionsView()
}

#Preview("Turn by Turn") {
    TurnByTurnDirectionsView()
}

#Preview("Alternate Routes") {
    AlternateRoutesView()
}
