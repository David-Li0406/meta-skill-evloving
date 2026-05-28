// MARK: - Basic Map View Example
// iOS 17+ SwiftUI MapKit 基本的な地図表示

import SwiftUI
import MapKit

// MARK: - 基本的な地図表示

/// 最もシンプルな地図表示
struct SimpleMapView: View {
    var body: some View {
        Map()
    }
}

// MARK: - カメラ位置制御

/// カメラ位置を制御する地図
struct CameraControlMapView: View {
    // カメラ位置の状態
    @State private var position: MapCameraPosition = .automatic

    var body: some View {
        Map(position: $position)
            .onAppear {
                // 東京駅を中心に表示
                position = .region(MKCoordinateRegion(
                    center: CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671),
                    span: MKCoordinateSpan(latitudeDelta: 0.01, longitudeDelta: 0.01)
                ))
            }
    }
}

// MARK: - 地図スタイル

/// 様々な地図スタイルの切り替え
struct MapStyleView: View {
    @State private var selectedStyle: MapStyleOption = .standard

    enum MapStyleOption: String, CaseIterable {
        case standard = "標準"
        case satellite = "衛星"
        case hybrid = "ハイブリッド"
    }

    var body: some View {
        VStack(spacing: 0) {
            // スタイル選択
            Picker("スタイル", selection: $selectedStyle) {
                ForEach(MapStyleOption.allCases, id: \.self) { style in
                    Text(style.rawValue).tag(style)
                }
            }
            .pickerStyle(.segmented)
            .padding()

            // 地図
            Map()
                .mapStyle(mapStyle)
        }
    }

    private var mapStyle: MapStyle {
        switch selectedStyle {
        case .standard:
            return .standard(elevation: .realistic)
        case .satellite:
            return .imagery
        case .hybrid:
            return .hybrid(elevation: .realistic)
        }
    }
}

// MARK: - 地図コントロール

/// 地図コントロール（コンパス、スケール、ユーザー位置ボタン）
struct MapControlsView: View {
    @State private var position: MapCameraPosition = .userLocation(fallback: .automatic)

    var body: some View {
        Map(position: $position) {
            // ユーザーの現在地を表示
            UserAnnotation()
        }
        .mapControls {
            // ユーザー位置ボタン
            MapUserLocationButton()

            // コンパス（地図が回転している時に表示）
            MapCompass()

            // スケールバー（ズーム時に表示）
            MapScaleView()

            // 2D/3D切り替え
            MapPitchToggle()
        }
    }
}

// MARK: - 3Dカメラビュー

/// 3Dカメラアングルで表示
struct Camera3DMapView: View {
    @State private var position: MapCameraPosition = .camera(
        MapCamera(
            centerCoordinate: CLLocationCoordinate2D(latitude: 35.6586, longitude: 139.7454),
            distance: 1000,
            heading: 45,
            pitch: 60
        )
    )

    var body: some View {
        Map(position: $position)
            .mapStyle(.standard(elevation: .realistic))
    }
}

// MARK: - インタラクション制御

/// インタラクションモードを制限した地図
struct LimitedInteractionMapView: View {
    var body: some View {
        VStack {
            Text("パンとズームのみ可能")
                .font(.caption)
                .foregroundStyle(.secondary)

            Map(interactionModes: [.pan, .zoom])
                .mapStyle(.standard)
        }
    }
}

// MARK: - カメラ変更の監視

/// カメラ変更を監視する地図
struct CameraMonitoringMapView: View {
    @State private var position: MapCameraPosition = .automatic
    @State private var currentRegion: MKCoordinateRegion?

    var body: some View {
        VStack {
            Map(position: $position)
                .onMapCameraChange { context in
                    currentRegion = context.region
                }

            if let region = currentRegion {
                VStack(alignment: .leading) {
                    Text("中心: \(region.center.latitude, specifier: "%.4f"), \(region.center.longitude, specifier: "%.4f")")
                    Text("スパン: \(region.span.latitudeDelta, specifier: "%.4f")")
                }
                .font(.caption)
                .padding()
                .background(.regularMaterial)
            }
        }
    }
}

// MARK: - POIフィルタリング

/// POI（Point of Interest）をフィルタリング
struct POIFilteredMapView: View {
    var body: some View {
        Map()
            .mapStyle(.standard(
                pointsOfInterest: .including([
                    .restaurant,
                    .cafe,
                    .hotel,
                    .publicTransport
                ])
            ))
    }
}

// MARK: - 地図の境界制限

/// 表示範囲を制限した地図
struct BoundedMapView: View {
    // 東京周辺に制限
    let tokyoBounds = MapCameraBounds(
        centerCoordinateBounds: MKCoordinateRegion(
            center: CLLocationCoordinate2D(latitude: 35.6762, longitude: 139.6503),
            span: MKCoordinateSpan(latitudeDelta: 0.5, longitudeDelta: 0.5)
        ),
        minimumDistance: 500,
        maximumDistance: 50000
    )

    var body: some View {
        Map(bounds: tokyoBounds)
    }
}

// MARK: - プレビュー

#Preview("Simple Map") {
    SimpleMapView()
}

#Preview("Camera Control") {
    CameraControlMapView()
}

#Preview("Map Styles") {
    MapStyleView()
}

#Preview("Map Controls") {
    MapControlsView()
}

#Preview("3D Camera") {
    Camera3DMapView()
}
