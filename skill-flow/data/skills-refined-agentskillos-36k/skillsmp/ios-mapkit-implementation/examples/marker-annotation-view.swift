// MARK: - Marker & Annotation View Example
// iOS 17+ SwiftUI MapKit マーカーとアノテーション

import SwiftUI
import MapKit

// MARK: - 基本的なマーカー

/// Markerの基本的な使用例
struct BasicMarkerView: View {
    var body: some View {
        Map {
            // テキストラベルのマーカー
            Marker("東京駅", coordinate: .tokyoStation)

            // システムイメージ付きマーカー
            Marker("渋谷駅", systemImage: "tram.fill", coordinate: .shibuyaStation)
                .tint(.purple)

            // モノグラムマーカー
            Marker("A", monogram: Text("A"), coordinate: .shinjukuStation)
                .tint(.orange)
        }
    }
}

// MARK: - カスタムAnnotation

/// Annotationでカスタムビューを表示
struct CustomAnnotationView: View {
    let places: [AnnotatedPlace] = [
        AnnotatedPlace(name: "カフェ", coordinate: .tokyoStation, rating: 4.5, image: "cup.and.saucer.fill"),
        AnnotatedPlace(name: "レストラン", coordinate: .shibuyaStation, rating: 4.2, image: "fork.knife"),
        AnnotatedPlace(name: "ホテル", coordinate: .shinjukuStation, rating: 4.8, image: "bed.double.fill")
    ]

    var body: some View {
        Map {
            ForEach(places) { place in
                Annotation(place.name, coordinate: place.coordinate) {
                    PlaceBadge(place: place)
                }
            }
        }
    }
}

struct AnnotatedPlace: Identifiable {
    let id = UUID()
    let name: String
    let coordinate: CLLocationCoordinate2D
    let rating: Double
    let image: String
}

struct PlaceBadge: View {
    let place: AnnotatedPlace

    var body: some View {
        VStack(spacing: 4) {
            Image(systemName: place.image)
                .font(.title2)
                .foregroundStyle(.white)
                .padding(8)
                .background(.blue)
                .clipShape(Circle())

            Text(place.name)
                .font(.caption2)
                .fontWeight(.medium)

            HStack(spacing: 2) {
                Image(systemName: "star.fill")
                    .font(.caption2)
                    .foregroundStyle(.yellow)
                Text(String(format: "%.1f", place.rating))
                    .font(.caption2)
            }
        }
        .padding(6)
        .background(.white)
        .clipShape(RoundedRectangle(cornerRadius: 8))
        .shadow(radius: 2)
    }
}

// MARK: - 選択可能なマーカー

/// マーカー選択機能
struct SelectableMarkerView: View {
    @State private var selectedPlace: SelectablePlace?

    let places: [SelectablePlace] = [
        SelectablePlace(name: "東京タワー", coordinate: CLLocationCoordinate2D(latitude: 35.6586, longitude: 139.7454)),
        SelectablePlace(name: "スカイツリー", coordinate: CLLocationCoordinate2D(latitude: 35.7101, longitude: 139.8107)),
        SelectablePlace(name: "浅草寺", coordinate: CLLocationCoordinate2D(latitude: 35.7148, longitude: 139.7967))
    ]

    var body: some View {
        VStack(spacing: 0) {
            Map(selection: $selectedPlace) {
                ForEach(places) { place in
                    Marker(place.name, systemImage: "mappin.circle.fill", coordinate: place.coordinate)
                        .tint(selectedPlace == place ? .red : .blue)
                        .tag(place)
                }
            }

            // 選択情報パネル
            if let place = selectedPlace {
                HStack {
                    VStack(alignment: .leading) {
                        Text(place.name)
                            .font(.headline)
                        Text("緯度: \(place.coordinate.latitude, specifier: "%.4f")")
                            .font(.caption)
                        Text("経度: \(place.coordinate.longitude, specifier: "%.4f")")
                            .font(.caption)
                    }

                    Spacer()

                    Button("詳細") {
                        // 詳細画面へ遷移
                    }
                    .buttonStyle(.borderedProminent)
                }
                .padding()
                .background(.regularMaterial)
            }
        }
    }
}

struct SelectablePlace: Identifiable, Equatable, Hashable {
    let id = UUID()
    let name: String
    let coordinate: CLLocationCoordinate2D

    static func == (lhs: SelectablePlace, rhs: SelectablePlace) -> Bool {
        lhs.id == rhs.id
    }

    func hash(into hasher: inout Hasher) {
        hasher.combine(id)
    }
}

// MARK: - カテゴリ別マーカー

/// カテゴリでフィルタリングできるマーカー
struct CategoryMarkerView: View {
    @State private var selectedCategories: Set<MarkerCategory> = Set(MarkerCategory.allCases)

    let categorizedPlaces: [CategorizedPlace] = [
        CategorizedPlace(name: "カフェA", coordinate: CLLocationCoordinate2D(latitude: 35.680, longitude: 139.765), category: .cafe),
        CategorizedPlace(name: "カフェB", coordinate: CLLocationCoordinate2D(latitude: 35.682, longitude: 139.768), category: .cafe),
        CategorizedPlace(name: "レストランA", coordinate: CLLocationCoordinate2D(latitude: 35.679, longitude: 139.762), category: .restaurant),
        CategorizedPlace(name: "ショップA", coordinate: CLLocationCoordinate2D(latitude: 35.681, longitude: 139.770), category: .shop)
    ]

    var body: some View {
        VStack(spacing: 0) {
            // カテゴリフィルター
            ScrollView(.horizontal, showsIndicators: false) {
                HStack {
                    ForEach(MarkerCategory.allCases, id: \.self) { category in
                        Toggle(isOn: Binding(
                            get: { selectedCategories.contains(category) },
                            set: { isOn in
                                if isOn {
                                    selectedCategories.insert(category)
                                } else {
                                    selectedCategories.remove(category)
                                }
                            }
                        )) {
                            Label(category.rawValue, systemImage: category.systemImage)
                        }
                        .toggleStyle(.button)
                        .tint(category.color)
                    }
                }
                .padding()
            }

            // 地図
            Map {
                ForEach(filteredPlaces) { place in
                    Marker(place.name, systemImage: place.category.systemImage, coordinate: place.coordinate)
                        .tint(place.category.color)
                }
            }
        }
    }

    private var filteredPlaces: [CategorizedPlace] {
        categorizedPlaces.filter { selectedCategories.contains($0.category) }
    }
}

struct CategorizedPlace: Identifiable {
    let id = UUID()
    let name: String
    let coordinate: CLLocationCoordinate2D
    let category: MarkerCategory
}

enum MarkerCategory: String, CaseIterable {
    case cafe = "カフェ"
    case restaurant = "レストラン"
    case shop = "ショップ"

    var systemImage: String {
        switch self {
        case .cafe: return "cup.and.saucer.fill"
        case .restaurant: return "fork.knife"
        case .shop: return "bag.fill"
        }
    }

    var color: Color {
        switch self {
        case .cafe: return .brown
        case .restaurant: return .orange
        case .shop: return .purple
        }
    }
}

// MARK: - アニメーションマーカー

/// アニメーション付きAnnotation
struct AnimatedAnnotationView: View {
    @State private var isAnimating = false

    let coordinate = CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671)

    var body: some View {
        Map {
            Annotation("パルス", coordinate: coordinate) {
                ZStack {
                    // パルスエフェクト
                    Circle()
                        .fill(.blue.opacity(0.3))
                        .frame(width: isAnimating ? 60 : 30, height: isAnimating ? 60 : 30)
                        .opacity(isAnimating ? 0 : 1)

                    // 中心マーカー
                    Circle()
                        .fill(.blue)
                        .frame(width: 20, height: 20)
                        .overlay {
                            Circle()
                                .stroke(.white, lineWidth: 2)
                        }
                }
            }
        }
        .onAppear {
            withAnimation(.easeOut(duration: 1.5).repeatForever(autoreverses: false)) {
                isAnimating = true
            }
        }
    }
}

// MARK: - クラスター表示

/// 多数のマーカーをクラスター表示
struct ClusterAnnotationView: View {
    let clusters: [MarkerCluster] = [
        MarkerCluster(center: CLLocationCoordinate2D(latitude: 35.68, longitude: 139.76), count: 15),
        MarkerCluster(center: CLLocationCoordinate2D(latitude: 35.66, longitude: 139.70), count: 8),
        MarkerCluster(center: CLLocationCoordinate2D(latitude: 35.69, longitude: 139.72), count: 23)
    ]

    var body: some View {
        Map {
            ForEach(clusters) { cluster in
                Annotation("", coordinate: cluster.center) {
                    ClusterBadge(count: cluster.count)
                }
            }
        }
    }
}

struct MarkerCluster: Identifiable {
    let id = UUID()
    let center: CLLocationCoordinate2D
    let count: Int
}

struct ClusterBadge: View {
    let count: Int

    var body: some View {
        ZStack {
            Circle()
                .fill(clusterColor)
                .frame(width: clusterSize, height: clusterSize)

            Text("\(count)")
                .font(.caption.bold())
                .foregroundStyle(.white)
        }
    }

    private var clusterSize: CGFloat {
        let base: CGFloat = 30
        let scale = min(CGFloat(count) / 10, 2)
        return base + (scale * 10)
    }

    private var clusterColor: Color {
        switch count {
        case 0..<10: return .green
        case 10..<20: return .orange
        default: return .red
        }
    }
}

// MARK: - 座標拡張

extension CLLocationCoordinate2D {
    static let tokyoStation = CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671)
    static let shibuyaStation = CLLocationCoordinate2D(latitude: 35.6580, longitude: 139.7016)
    static let shinjukuStation = CLLocationCoordinate2D(latitude: 35.6896, longitude: 139.7006)
}

// MARK: - Preview

#Preview("Basic Markers") {
    BasicMarkerView()
}

#Preview("Custom Annotations") {
    CustomAnnotationView()
}

#Preview("Selectable Markers") {
    SelectableMarkerView()
}

#Preview("Category Markers") {
    CategoryMarkerView()
}

#Preview("Animated Annotation") {
    AnimatedAnnotationView()
}

#Preview("Cluster Annotation") {
    ClusterAnnotationView()
}
