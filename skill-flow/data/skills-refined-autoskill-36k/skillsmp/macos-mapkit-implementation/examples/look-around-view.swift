// MARK: - Look Around View Example
// macOS 14+ SwiftUI Look Around プレビュー

import SwiftUI
import MapKit

// MARK: - Look Around View

/// Look Aroundプレビューを表示するView
struct LookAroundView: View {
    @State private var position: MapCameraPosition = .automatic
    @State private var selectedCoordinate: CLLocationCoordinate2D = .tokyoStation
    @State private var lookAroundScene: MKLookAroundScene?
    @State private var isLoadingScene = false
    @State private var showLookAround = false

    var body: some View {
        HSplitView {
            // 地図
            VStack {
                Map(position: $position) {
                    Marker("選択地点", coordinate: selectedCoordinate)
                        .tint(.blue)
                }
                .mapStyle(.standard)
                .mapControls {
                    MapCompass()
                    MapScaleView()
                    MapZoomStepper()
                }
                .onTapGesture { location in
                    // タップ位置の座標を取得（簡易実装）
                    // 実際のアプリではMapReaderを使用して正確な座標を取得
                }

                // 場所選択
                HStack {
                    Button("東京駅") {
                        selectLocation(.tokyoStation)
                    }
                    Button("渋谷駅") {
                        selectLocation(.shibuya)
                    }
                    Button("新宿駅") {
                        selectLocation(.shinjuku)
                    }
                }
                .padding()
            }

            // Look Aroundパネル
            VStack(alignment: .leading, spacing: 16) {
                Text("Look Around")
                    .font(.headline)

                if isLoadingScene {
                    VStack {
                        ProgressView()
                        Text("シーンを読み込み中...")
                            .foregroundStyle(.secondary)
                    }
                    .frame(maxWidth: .infinity, minHeight: 250)
                } else if let scene = lookAroundScene {
                    // Look Aroundプレビュー
                    LookAroundPreview(initialScene: scene)
                        .frame(height: 250)
                        .clipShape(RoundedRectangle(cornerRadius: 12))

                    // 注意事項
                    Text("macOS制限: フルスクリーンナビゲーションボタンが表示されない場合があります")
                        .font(.caption)
                        .foregroundStyle(.secondary)

                    Button("大きく表示") {
                        showLookAround = true
                    }
                    .buttonStyle(.borderedProminent)
                } else {
                    ContentUnavailableView(
                        "Look Around利用不可",
                        systemImage: "eye.slash",
                        description: Text("この場所ではLook Aroundが利用できません")
                    )
                    .frame(height: 250)

                    // フォールバック: 衛星画像
                    GroupBox("代替: 衛星画像") {
                        Map(position: .constant(.camera(MapCamera(
                            centerCoordinate: selectedCoordinate,
                            distance: 200,
                            heading: 0,
                            pitch: 60
                        )))) {
                            Marker("", coordinate: selectedCoordinate)
                        }
                        .mapStyle(.imagery)
                        .frame(height: 150)
                        .clipShape(RoundedRectangle(cornerRadius: 8))
                    }
                }

                Spacer()
            }
            .padding()
            .frame(minWidth: 300, maxWidth: 400)
        }
        .task {
            await loadLookAroundScene(for: selectedCoordinate)
        }
        .sheet(isPresented: $showLookAround) {
            if let scene = lookAroundScene {
                LookAroundFullScreenView(scene: scene)
            }
        }
    }

    private func selectLocation(_ coordinate: CLLocationCoordinate2D) {
        selectedCoordinate = coordinate
        position = .region(MKCoordinateRegion(
            center: coordinate,
            span: MKCoordinateSpan(latitudeDelta: 0.005, longitudeDelta: 0.005)
        ))
        Task {
            await loadLookAroundScene(for: coordinate)
        }
    }

    private func loadLookAroundScene(for coordinate: CLLocationCoordinate2D) async {
        isLoadingScene = true
        lookAroundScene = nil

        let request = MKLookAroundSceneRequest(coordinate: coordinate)

        do {
            lookAroundScene = try await request.scene
        } catch {
            lookAroundScene = nil
        }

        isLoadingScene = false
    }
}

// MARK: - Look Around フルスクリーンView

/// Look Aroundを大きく表示するView
struct LookAroundFullScreenView: View {
    let scene: MKLookAroundScene
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        VStack(spacing: 0) {
            // ヘッダー
            HStack {
                Text("Look Around")
                    .font(.headline)
                Spacer()
                Button("閉じる") {
                    dismiss()
                }
            }
            .padding()

            // Look Aroundプレビュー
            LookAroundPreview(initialScene: scene)
        }
        .frame(minWidth: 600, minHeight: 500)
    }
}

// MARK: - Look Around + 地図連携View

/// 地図とLook Aroundを連携させるView
struct MapWithLookAroundView: View {
    @State private var position: MapCameraPosition = .automatic
    @State private var selectedMapItem: MKMapItem?
    @State private var lookAroundScene: MKLookAroundScene?

    let landmarks: [MKMapItem] = {
        // サンプルランドマーク
        let tokyo = MKMapItem(placemark: MKPlacemark(coordinate: .tokyoStation))
        tokyo.name = "東京駅"

        let shibuya = MKMapItem(placemark: MKPlacemark(coordinate: .shibuya))
        shibuya.name = "渋谷駅"

        let shinjuku = MKMapItem(placemark: MKPlacemark(coordinate: .shinjuku))
        shinjuku.name = "新宿駅"

        return [tokyo, shibuya, shinjuku]
    }()

    var body: some View {
        VStack(spacing: 0) {
            // 地図
            Map(position: $position, selection: $selectedMapItem) {
                ForEach(landmarks, id: \.self) { landmark in
                    Marker(landmark.name ?? "", coordinate: landmark.placemark.coordinate)
                }
            }
            .mapStyle(.standard)
            .mapControls {
                MapCompass()
                MapScaleView()
            }
            .onChange(of: selectedMapItem) { _, newItem in
                if let item = newItem {
                    Task {
                        await loadScene(for: item.placemark.coordinate)
                    }
                }
            }

            // Look Aroundプレビュー（下部）
            if let scene = lookAroundScene {
                LookAroundPreview(initialScene: scene)
                    .frame(height: 200)
            } else if selectedMapItem != nil {
                HStack {
                    ProgressView()
                    Text("Look Aroundを読み込み中...")
                }
                .frame(height: 200)
                .frame(maxWidth: .infinity)
                .background(.regularMaterial)
            }
        }
    }

    private func loadScene(for coordinate: CLLocationCoordinate2D) async {
        lookAroundScene = nil
        let request = MKLookAroundSceneRequest(coordinate: coordinate)
        lookAroundScene = try? await request.scene
    }
}

// MARK: - 座標拡張

extension CLLocationCoordinate2D {
    static let tokyoStation = CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671)
    static let shibuya = CLLocationCoordinate2D(latitude: 35.6580, longitude: 139.7016)
    static let shinjuku = CLLocationCoordinate2D(latitude: 35.6896, longitude: 139.7006)
}

// MARK: - Preview

#Preview("Look Around") {
    LookAroundView()
        .frame(width: 900, height: 600)
}

#Preview("Map with Look Around") {
    MapWithLookAroundView()
        .frame(width: 600, height: 700)
}
