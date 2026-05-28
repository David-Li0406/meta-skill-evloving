// MARK: - Basic Map View Example
// macOS 14+ SwiftUI Map 基本的な地図表示

import SwiftUI
import MapKit

// MARK: - 基本的な地図表示

/// シンプルな地図表示View
struct BasicMapView: View {
    @State private var position: MapCameraPosition = .automatic

    var body: some View {
        Map(position: $position) {
            // マーカーを追加
            Marker("東京駅", coordinate: .tokyoStation)
                .tint(.red)
        }
        .mapStyle(.standard)
        .mapControls {
            MapUserLocationButton()
            MapCompass()
            MapScaleView()
            MapZoomStepper() // macOS向けズームコントロール
        }
    }
}

// MARK: - カメラ位置制御

/// カメラ位置を制御するView
struct CameraControlMapView: View {
    @State private var position: MapCameraPosition = .region(MKCoordinateRegion(
        center: CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671),
        span: MKCoordinateSpan(latitudeDelta: 0.05, longitudeDelta: 0.05)
    ))

    var body: some View {
        VStack {
            Map(position: $position) {
                Marker("東京駅", coordinate: .tokyoStation)
            }

            HStack(spacing: 12) {
                Button("東京駅") {
                    withAnimation {
                        position = .region(MKCoordinateRegion(
                            center: .tokyoStation,
                            span: MKCoordinateSpan(latitudeDelta: 0.01, longitudeDelta: 0.01)
                        ))
                    }
                }

                Button("渋谷駅") {
                    withAnimation {
                        position = .region(MKCoordinateRegion(
                            center: .shibuya,
                            span: MKCoordinateSpan(latitudeDelta: 0.01, longitudeDelta: 0.01)
                        ))
                    }
                }

                Button("3Dビュー") {
                    withAnimation {
                        position = .camera(MapCamera(
                            centerCoordinate: .tokyoStation,
                            distance: 1000,
                            heading: 45,
                            pitch: 60
                        ))
                    }
                }
            }
            .padding()
        }
    }
}

// MARK: - 地図スタイル切り替え

/// 地図スタイルを切り替えるView
struct MapStyleSwitcherView: View {
    @State private var position: MapCameraPosition = .automatic
    @State private var selectedStyle: MapStyleOption = .standard

    enum MapStyleOption: String, CaseIterable {
        case standard = "標準"
        case hybrid = "ハイブリッド"
        case imagery = "衛星写真"
        case realistic = "3D建物"
    }

    var body: some View {
        VStack {
            Map(position: $position) {
                Marker("現在地", coordinate: .tokyoStation)
            }
            .mapStyle(mapStyle)
            .mapControls {
                MapCompass()
                MapScaleView()
                MapZoomStepper()
            }

            Picker("地図スタイル", selection: $selectedStyle) {
                ForEach(MapStyleOption.allCases, id: \.self) { style in
                    Text(style.rawValue).tag(style)
                }
            }
            .pickerStyle(.segmented)
            .padding()
        }
    }

    private var mapStyle: MapStyle {
        switch selectedStyle {
        case .standard:
            return .standard
        case .hybrid:
            return .hybrid
        case .imagery:
            return .imagery
        case .realistic:
            return .standard(elevation: .realistic)
        }
    }
}

// MARK: - ユーザー位置追従

/// ユーザー位置を追従するView
struct UserLocationMapView: View {
    @State private var position: MapCameraPosition = .userLocation(fallback: .automatic)
    @State private var locationManager = LocationManager()

    var body: some View {
        VStack {
            Map(position: $position) {
                UserAnnotation()
            }
            .mapControls {
                MapUserLocationButton()
                MapCompass()
                MapScaleView()
            }
            .onAppear {
                locationManager.requestAuthorization()
            }

            if let location = locationManager.location {
                VStack(alignment: .leading, spacing: 4) {
                    Text("緯度: \(location.coordinate.latitude, specifier: "%.6f")")
                    Text("経度: \(location.coordinate.longitude, specifier: "%.6f")")
                }
                .font(.caption)
                .padding()
            }
        }
    }
}

// MARK: - インタラクションモード

/// インタラクションモードを制限するView
struct LimitedInteractionMapView: View {
    @State private var position: MapCameraPosition = .automatic

    var body: some View {
        Map(position: $position, interactionModes: [.pan, .zoom]) {
            // 回転と傾きを無効化
            Marker("固定表示", coordinate: .tokyoStation)
        }
        .mapStyle(.standard)
    }
}

// MARK: - カメラ変更検知

/// カメラ変更を検知するView
struct CameraChangeDetectionView: View {
    @State private var position: MapCameraPosition = .automatic
    @State private var visibleRegion: MKCoordinateRegion?

    var body: some View {
        VStack {
            Map(position: $position) {
                Marker("東京駅", coordinate: .tokyoStation)
            }
            .onMapCameraChange { context in
                visibleRegion = context.region
            }

            if let region = visibleRegion {
                VStack(alignment: .leading, spacing: 4) {
                    Text("中心: \(region.center.latitude, specifier: "%.4f"), \(region.center.longitude, specifier: "%.4f")")
                    Text("範囲: \(region.span.latitudeDelta, specifier: "%.4f") x \(region.span.longitudeDelta, specifier: "%.4f")")
                }
                .font(.caption)
                .padding()
            }
        }
    }
}

// MARK: - 座標拡張

extension CLLocationCoordinate2D {
    static let tokyoStation = CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671)
    static let shibuya = CLLocationCoordinate2D(latitude: 35.6580, longitude: 139.7016)
    static let shinjuku = CLLocationCoordinate2D(latitude: 35.6896, longitude: 139.7006)
}

// MARK: - 簡易LocationManager

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

    nonisolated func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        Task { @MainActor in
            location = locations.last
        }
    }

    nonisolated func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        Task { @MainActor in
            authorizationStatus = manager.authorizationStatus
            if authorizationStatus == .authorized || authorizationStatus == .authorizedAlways {
                startUpdating()
            }
        }
    }
}

// MARK: - Preview

#Preview("Basic Map") {
    BasicMapView()
        .frame(width: 600, height: 400)
}

#Preview("Camera Control") {
    CameraControlMapView()
        .frame(width: 600, height: 500)
}

#Preview("Map Style Switcher") {
    MapStyleSwitcherView()
        .frame(width: 600, height: 500)
}

#Preview("Camera Change Detection") {
    CameraChangeDetectionView()
        .frame(width: 600, height: 500)
}
