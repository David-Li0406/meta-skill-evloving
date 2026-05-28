// MARK: - Marker and Annotation View Example
// macOS 14+ SwiftUI マーカーとアノテーション

import SwiftUI
import MapKit

// MARK: - 基本的なマーカー表示

/// 基本的なマーカーを表示するView
struct BasicMarkerView: View {
    @State private var position: MapCameraPosition = .automatic

    var body: some View {
        Map(position: $position) {
            // 基本マーカー
            Marker("東京駅", coordinate: .tokyoStation)

            // システムイメージ付きマーカー
            Marker("渋谷駅", systemImage: "tram.fill", coordinate: .shibuya)
                .tint(.purple)

            // モノグラムマーカー
            Marker("新宿", monogram: Text("新"), coordinate: .shinjuku)
                .tint(.green)
        }
        .mapStyle(.standard)
        .mapControls {
            MapCompass()
            MapScaleView()
            MapZoomStepper()
        }
    }
}

// MARK: - カスタムアノテーション

/// カスタムアノテーションを表示するView
struct CustomAnnotationView: View {
    @State private var position: MapCameraPosition = .automatic

    var body: some View {
        Map(position: $position) {
            // カスタムアノテーション
            Annotation("カフェ", coordinate: .shibuya) {
                VStack(spacing: 4) {
                    Image(systemName: "cup.and.saucer.fill")
                        .font(.title2)
                        .foregroundStyle(.brown)
                    Text("人気カフェ")
                        .font(.caption)
                }
                .padding(8)
                .background(.white)
                .clipShape(RoundedRectangle(cornerRadius: 8))
                .shadow(radius: 2)
            }

            // アンカー位置を指定したアノテーション
            Annotation("レストラン", coordinate: .shinjuku, anchor: .bottom) {
                VStack(spacing: 0) {
                    Image(systemName: "fork.knife")
                        .font(.title2)
                        .foregroundStyle(.orange)
                        .padding(8)
                        .background(.white)
                        .clipShape(Circle())
                        .shadow(radius: 2)

                    // 矢印部分
                    Image(systemName: "triangle.fill")
                        .font(.caption2)
                        .foregroundStyle(.white)
                        .rotationEffect(.degrees(180))
                        .offset(y: -4)
                }
            }
        }
        .mapStyle(.standard)
    }
}

// MARK: - 動的マーカー

/// 動的に追加・削除できるマーカー
struct DynamicMarkersView: View {
    @State private var position: MapCameraPosition = .region(MKCoordinateRegion(
        center: CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671),
        span: MKCoordinateSpan(latitudeDelta: 0.05, longitudeDelta: 0.05)
    ))
    @State private var markers: [MapMarker] = [
        MapMarker(id: UUID(), name: "東京駅", coordinate: .tokyoStation, color: .red)
    ]
    @State private var selectedMarker: MapMarker?

    var body: some View {
        VStack {
            Map(position: $position, selection: $selectedMarker) {
                ForEach(markers) { marker in
                    Marker(marker.name, coordinate: marker.coordinate)
                        .tint(marker.color)
                        .tag(marker)
                }
            }
            .mapStyle(.standard)
            .mapControls {
                MapCompass()
                MapScaleView()
            }

            // コントロール
            HStack {
                Button("マーカー追加") {
                    addRandomMarker()
                }
                .buttonStyle(.bordered)

                Button("選択を削除") {
                    if let selected = selectedMarker {
                        markers.removeAll { $0.id == selected.id }
                        selectedMarker = nil
                    }
                }
                .buttonStyle(.bordered)
                .disabled(selectedMarker == nil)

                Button("全削除") {
                    markers.removeAll()
                    selectedMarker = nil
                }
                .buttonStyle(.bordered)

                Spacer()

                Text("マーカー数: \(markers.count)")
                    .foregroundStyle(.secondary)
            }
            .padding()
        }
    }

    private func addRandomMarker() {
        let center = CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671)
        let newCoordinate = CLLocationCoordinate2D(
            latitude: center.latitude + Double.random(in: -0.02...0.02),
            longitude: center.longitude + Double.random(in: -0.02...0.02)
        )
        let colors: [Color] = [.red, .blue, .green, .orange, .purple, .pink]
        let marker = MapMarker(
            id: UUID(),
            name: "スポット \(markers.count + 1)",
            coordinate: newCoordinate,
            color: colors.randomElement() ?? .red
        )
        markers.append(marker)
    }
}

// MARK: - マーカーデータモデル

struct MapMarker: Identifiable, Hashable {
    let id: UUID
    let name: String
    let coordinate: CLLocationCoordinate2D
    let color: Color

    func hash(into hasher: inout Hasher) {
        hasher.combine(id)
    }

    static func == (lhs: MapMarker, rhs: MapMarker) -> Bool {
        lhs.id == rhs.id
    }
}

// MARK: - 選択可能なアノテーション

/// 選択するとポップアップが表示されるアノテーション
struct SelectableAnnotationView: View {
    @State private var position: MapCameraPosition = .automatic
    @State private var selectedPlace: Place?

    let places: [Place] = [
        Place(id: 1, name: "東京駅", coordinate: .tokyoStation, description: "東京の中心駅"),
        Place(id: 2, name: "渋谷駅", coordinate: .shibuya, description: "若者の街の中心"),
        Place(id: 3, name: "新宿駅", coordinate: .shinjuku, description: "世界一の乗降客数")
    ]

    var body: some View {
        Map(position: $position, selection: $selectedPlace) {
            ForEach(places) { place in
                Marker(place.name, coordinate: place.coordinate)
                    .tint(.blue)
                    .tag(place)
            }
        }
        .mapStyle(.standard)
        .safeAreaInset(edge: .bottom) {
            if let place = selectedPlace {
                PlaceDetailCard(place: place) {
                    selectedPlace = nil
                }
                .padding()
                .transition(.move(edge: .bottom))
            }
        }
        .animation(.spring(), value: selectedPlace)
    }
}

// MARK: - 場所データモデル

struct Place: Identifiable, Hashable {
    let id: Int
    let name: String
    let coordinate: CLLocationCoordinate2D
    let description: String

    func hash(into hasher: inout Hasher) {
        hasher.combine(id)
    }

    static func == (lhs: Place, rhs: Place) -> Bool {
        lhs.id == rhs.id
    }
}

// MARK: - 詳細カード

struct PlaceDetailCard: View {
    let place: Place
    let onDismiss: () -> Void

    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(place.name)
                    .font(.headline)
                Text(place.description)
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }

            Spacer()

            Button(action: onDismiss) {
                Image(systemName: "xmark.circle.fill")
                    .foregroundStyle(.secondary)
            }
            .buttonStyle(.plain)
        }
        .padding()
        .background(.regularMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}

// MARK: - ユーザー位置アノテーション

/// ユーザー位置を表示するView
struct UserLocationAnnotationView: View {
    @State private var position: MapCameraPosition = .userLocation(fallback: .automatic)

    var body: some View {
        Map(position: $position) {
            // ユーザー位置表示
            UserAnnotation()

            // 他のマーカー
            Marker("東京駅", coordinate: .tokyoStation)
        }
        .mapStyle(.standard)
        .mapControls {
            MapUserLocationButton()
            MapCompass()
            MapScaleView()
        }
    }
}

// MARK: - カスタムオーバーレイ

/// オーバーレイを表示するView
struct OverlayAnnotationView: View {
    @State private var position: MapCameraPosition = .automatic

    var body: some View {
        Map(position: $position) {
            // マーカー
            Marker("中心", coordinate: .tokyoStation)
                .tint(.red)

            // 円形オーバーレイ
            MapCircle(center: .tokyoStation, radius: 500)
                .foregroundStyle(.blue.opacity(0.2))
                .stroke(.blue, lineWidth: 2)

            // ポリゴンオーバーレイ
            MapPolygon(coordinates: [
                CLLocationCoordinate2D(latitude: 35.69, longitude: 139.76),
                CLLocationCoordinate2D(latitude: 35.69, longitude: 139.78),
                CLLocationCoordinate2D(latitude: 35.67, longitude: 139.78),
                CLLocationCoordinate2D(latitude: 35.67, longitude: 139.76)
            ])
            .foregroundStyle(.green.opacity(0.2))
            .stroke(.green, lineWidth: 2)
        }
        .mapStyle(.standard)
    }
}

// MARK: - 座標拡張

extension CLLocationCoordinate2D {
    static let tokyoStation = CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671)
    static let shibuya = CLLocationCoordinate2D(latitude: 35.6580, longitude: 139.7016)
    static let shinjuku = CLLocationCoordinate2D(latitude: 35.6896, longitude: 139.7006)
}

// MARK: - Preview

#Preview("Basic Markers") {
    BasicMarkerView()
        .frame(width: 600, height: 400)
}

#Preview("Custom Annotations") {
    CustomAnnotationView()
        .frame(width: 600, height: 400)
}

#Preview("Dynamic Markers") {
    DynamicMarkersView()
        .frame(width: 600, height: 500)
}

#Preview("Selectable Annotations") {
    SelectableAnnotationView()
        .frame(width: 600, height: 500)
}

#Preview("Overlay Annotations") {
    OverlayAnnotationView()
        .frame(width: 600, height: 400)
}
