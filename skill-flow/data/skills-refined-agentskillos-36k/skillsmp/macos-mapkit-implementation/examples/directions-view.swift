// MARK: - Directions View Example
// macOS 14+ SwiftUI 経路検索・表示

import SwiftUI
import MapKit

// MARK: - 経路検索View

/// 経路検索と表示を行うView
struct DirectionsView: View {
    @State private var position: MapCameraPosition = .automatic
    @State private var route: MKRoute?
    @State private var isCalculating = false
    @State private var errorMessage: String?

    @State private var sourceCoordinate: CLLocationCoordinate2D = .tokyoStation
    @State private var destinationCoordinate: CLLocationCoordinate2D = .shibuya

    var body: some View {
        HSplitView {
            // 地図表示
            Map(position: $position) {
                // 出発地マーカー
                Marker("出発地", systemImage: "location.fill", coordinate: sourceCoordinate)
                    .tint(.green)

                // 目的地マーカー
                Marker("目的地", systemImage: "flag.fill", coordinate: destinationCoordinate)
                    .tint(.red)

                // 経路表示
                if let route {
                    MapPolyline(route.polyline)
                        .stroke(.blue, lineWidth: 5)
                }
            }
            .mapStyle(.standard)
            .mapControls {
                MapCompass()
                MapScaleView()
                MapZoomStepper()
            }

            // サイドパネル
            VStack(alignment: .leading, spacing: 16) {
                Text("経路検索")
                    .font(.headline)

                // 場所選択
                GroupBox("場所") {
                    VStack(alignment: .leading, spacing: 8) {
                        Picker("出発地", selection: $sourceCoordinate) {
                            Text("東京駅").tag(CLLocationCoordinate2D.tokyoStation)
                            Text("渋谷駅").tag(CLLocationCoordinate2D.shibuya)
                            Text("新宿駅").tag(CLLocationCoordinate2D.shinjuku)
                        }

                        Picker("目的地", selection: $destinationCoordinate) {
                            Text("東京駅").tag(CLLocationCoordinate2D.tokyoStation)
                            Text("渋谷駅").tag(CLLocationCoordinate2D.shibuya)
                            Text("新宿駅").tag(CLLocationCoordinate2D.shinjuku)
                        }
                    }
                }

                // 検索ボタン
                Button {
                    Task {
                        await calculateRoute()
                    }
                } label: {
                    HStack {
                        if isCalculating {
                            ProgressView()
                                .scaleEffect(0.8)
                        }
                        Text(isCalculating ? "計算中..." : "経路を検索")
                    }
                    .frame(maxWidth: .infinity)
                }
                .buttonStyle(.borderedProminent)
                .disabled(isCalculating || sourceCoordinate == destinationCoordinate)

                // エラー表示
                if let error = errorMessage {
                    Text(error)
                        .foregroundStyle(.red)
                        .font(.caption)
                }

                // 経路情報
                if let route {
                    GroupBox("経路情報") {
                        VStack(alignment: .leading, spacing: 8) {
                            LabeledContent("距離", value: formatDistance(route.distance))
                            LabeledContent("所要時間", value: formatDuration(route.expectedTravelTime))
                            LabeledContent("交通手段", value: transportTypeName(route.transportType))
                        }
                    }

                    // ターンバイターン案内
                    GroupBox("案内") {
                        ScrollView {
                            VStack(alignment: .leading, spacing: 8) {
                                ForEach(Array(route.steps.enumerated()), id: \.offset) { index, step in
                                    if !step.instructions.isEmpty {
                                        HStack(alignment: .top, spacing: 8) {
                                            Text("\(index + 1)")
                                                .font(.caption)
                                                .foregroundStyle(.secondary)
                                                .frame(width: 20)

                                            VStack(alignment: .leading, spacing: 2) {
                                                Text(step.instructions)
                                                    .font(.callout)
                                                Text(formatDistance(step.distance))
                                                    .font(.caption)
                                                    .foregroundStyle(.secondary)
                                            }
                                        }
                                        Divider()
                                    }
                                }
                            }
                        }
                        .frame(maxHeight: 200)
                    }
                }

                Spacer()
            }
            .padding()
            .frame(minWidth: 280, maxWidth: 350)
        }
    }

    // MARK: - Private Methods

    private func calculateRoute() async {
        isCalculating = true
        errorMessage = nil

        do {
            let request = MKDirections.Request()
            request.source = MKMapItem(placemark: MKPlacemark(coordinate: sourceCoordinate))
            request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destinationCoordinate))
            request.transportType = .automobile
            request.requestsAlternateRoutes = false

            let directions = MKDirections(request: request)
            let response = try await directions.calculate()

            if let calculatedRoute = response.routes.first {
                route = calculatedRoute

                // 経路全体が見えるようにカメラを調整
                let rect = calculatedRoute.polyline.boundingMapRect
                position = .rect(rect)
            } else {
                errorMessage = "経路が見つかりませんでした"
            }
        } catch let error as MKError {
            switch error.code {
            case .directionsNotFound:
                errorMessage = "この区間の経路が見つかりません"
            case .serverFailure:
                errorMessage = "サーバーエラーが発生しました"
            default:
                errorMessage = "経路検索に失敗しました: \(error.localizedDescription)"
            }
        } catch {
            errorMessage = "エラー: \(error.localizedDescription)"
        }

        isCalculating = false
    }

    private func formatDistance(_ meters: CLLocationDistance) -> String {
        if meters >= 1000 {
            return String(format: "%.1f km", meters / 1000)
        } else {
            return String(format: "%.0f m", meters)
        }
    }

    private func formatDuration(_ seconds: TimeInterval) -> String {
        let hours = Int(seconds) / 3600
        let minutes = (Int(seconds) % 3600) / 60

        if hours > 0 {
            return "\(hours)時間\(minutes)分"
        } else {
            return "\(minutes)分"
        }
    }

    private func transportTypeName(_ type: MKDirectionsTransportType) -> String {
        switch type {
        case .automobile: return "自動車"
        case .walking: return "徒歩"
        case .transit: return "公共交通機関"
        default: return "その他"
        }
    }
}

// MARK: - 交通手段選択付き経路検索View

/// 交通手段を選択できる経路検索View
struct TransportTypeDirectionsView: View {
    @State private var position: MapCameraPosition = .automatic
    @State private var routes: [MKRoute] = []
    @State private var isWalking = false  // 交通手段切り替え
    @State private var isCalculating = false

    private var selectedTransportType: MKDirectionsTransportType {
        isWalking ? .walking : .automobile
    }

    var body: some View {
        VStack {
            // 交通手段選択
            Picker("交通手段", selection: $isWalking) {
                Text("自動車").tag(false)
                Text("徒歩").tag(true)
            }
            .pickerStyle(.segmented)
            .padding()
            .onChange(of: isWalking) {
                Task {
                    await calculateRoute()
                }
            }

            // 地図
            Map(position: $position) {
                Marker("東京駅", coordinate: .tokyoStation)
                    .tint(.green)
                Marker("渋谷駅", coordinate: .shibuya)
                    .tint(.red)

                ForEach(Array(routes.enumerated()), id: \.offset) { index, route in
                    MapPolyline(route.polyline)
                        .stroke(index == 0 ? .blue : .gray.opacity(0.5), lineWidth: index == 0 ? 5 : 3)
                }
            }
            .mapControls {
                MapCompass()
                MapScaleView()
            }

            // 経路リスト
            if !routes.isEmpty {
                List(Array(routes.enumerated()), id: \.offset) { index, route in
                    HStack {
                        VStack(alignment: .leading) {
                            Text("ルート \(index + 1)")
                                .font(.headline)
                            Text("\(formatDistance(route.distance)) • \(formatDuration(route.expectedTravelTime))")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                        Spacer()
                        if index == 0 {
                            Text("推奨")
                                .font(.caption)
                                .padding(.horizontal, 8)
                                .padding(.vertical, 4)
                                .background(.blue)
                                .foregroundStyle(.white)
                                .clipShape(Capsule())
                        }
                    }
                }
                .frame(height: 150)
            }
        }
        .task {
            await calculateRoute()
        }
    }

    private func calculateRoute() async {
        isCalculating = true

        let request = MKDirections.Request()
        request.source = MKMapItem(placemark: MKPlacemark(coordinate: .tokyoStation))
        request.destination = MKMapItem(placemark: MKPlacemark(coordinate: .shibuya))
        request.transportType = selectedTransportType
        request.requestsAlternateRoutes = true

        let directions = MKDirections(request: request)

        do {
            let response = try await directions.calculate()
            routes = response.routes

            if let firstRoute = routes.first {
                let rect = firstRoute.polyline.boundingMapRect
                position = .rect(rect)
            }
        } catch {
            routes = []
        }

        isCalculating = false
    }

    private func formatDistance(_ meters: CLLocationDistance) -> String {
        meters >= 1000 ? String(format: "%.1f km", meters / 1000) : String(format: "%.0f m", meters)
    }

    private func formatDuration(_ seconds: TimeInterval) -> String {
        let minutes = Int(seconds) / 60
        return "\(minutes)分"
    }
}

// MARK: - 座標拡張

extension CLLocationCoordinate2D: Equatable {
    public static func == (lhs: CLLocationCoordinate2D, rhs: CLLocationCoordinate2D) -> Bool {
        lhs.latitude == rhs.latitude && lhs.longitude == rhs.longitude
    }

    static let tokyoStation = CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671)
    static let shibuya = CLLocationCoordinate2D(latitude: 35.6580, longitude: 139.7016)
    static let shinjuku = CLLocationCoordinate2D(latitude: 35.6896, longitude: 139.7006)
}

extension CLLocationCoordinate2D: Hashable {
    public func hash(into hasher: inout Hasher) {
        hasher.combine(latitude)
        hasher.combine(longitude)
    }
}

// MARK: - Preview

#Preview("Directions") {
    DirectionsView()
        .frame(width: 900, height: 600)
}

#Preview("Transport Type Selection") {
    TransportTypeDirectionsView()
        .frame(width: 600, height: 700)
}
