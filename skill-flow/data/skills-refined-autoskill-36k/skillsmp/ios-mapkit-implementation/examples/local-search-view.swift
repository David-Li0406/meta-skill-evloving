// MARK: - Local Search View Example
// iOS 17+ SwiftUI MapKit 周辺検索

import SwiftUI
import MapKit

// MARK: - 基本的な周辺検索

/// テキスト検索で周辺のスポットを表示
struct BasicLocalSearchView: View {
    @State private var searchText = ""
    @State private var searchResults: [MKMapItem] = []
    @State private var position: MapCameraPosition = .region(MKCoordinateRegion(
        center: CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671),
        span: MKCoordinateSpan(latitudeDelta: 0.05, longitudeDelta: 0.05)
    ))
    @State private var isSearching = false

    var body: some View {
        VStack(spacing: 0) {
            // 検索バー
            HStack {
                Image(systemName: "magnifyingglass")
                    .foregroundStyle(.secondary)

                TextField("周辺を検索", text: $searchText)
                    .textFieldStyle(.plain)
                    .onSubmit {
                        Task {
                            await search()
                        }
                    }

                if isSearching {
                    ProgressView()
                        .scaleEffect(0.8)
                } else if !searchText.isEmpty {
                    Button {
                        searchText = ""
                        searchResults = []
                    } label: {
                        Image(systemName: "xmark.circle.fill")
                            .foregroundStyle(.secondary)
                    }
                }
            }
            .padding()
            .background(.regularMaterial)

            // 地図
            Map(position: $position) {
                ForEach(searchResults, id: \.self) { item in
                    Marker(
                        item.name ?? "Unknown",
                        coordinate: item.placemark.coordinate
                    )
                    .tint(.red)
                }
            }
        }
    }

    private func search() async {
        guard !searchText.isEmpty else { return }

        isSearching = true
        defer { isSearching = false }

        let request = MKLocalSearch.Request()
        request.naturalLanguageQuery = searchText
        request.region = MKCoordinateRegion(
            center: CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671),
            span: MKCoordinateSpan(latitudeDelta: 0.1, longitudeDelta: 0.1)
        )

        let search = MKLocalSearch(request: request)

        do {
            let response = try await search.start()
            searchResults = response.mapItems
        } catch {
            print("検索エラー: \(error)")
            searchResults = []
        }
    }
}

// MARK: - カテゴリ検索

/// POIカテゴリでフィルタリング
struct CategorySearchView: View {
    @State private var selectedCategory: POICategory?
    @State private var searchResults: [MKMapItem] = []
    @State private var position: MapCameraPosition = .region(MKCoordinateRegion(
        center: CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671),
        span: MKCoordinateSpan(latitudeDelta: 0.02, longitudeDelta: 0.02)
    ))
    @State private var isSearching = false

    enum POICategory: String, CaseIterable {
        case restaurant = "レストラン"
        case cafe = "カフェ"
        case hotel = "ホテル"
        case parking = "駐車場"
        case gasStation = "ガソリン"
        case hospital = "病院"

        var mkCategory: MKPointOfInterestCategory {
            switch self {
            case .restaurant: return .restaurant
            case .cafe: return .cafe
            case .hotel: return .hotel
            case .parking: return .parking
            case .gasStation: return .gasStation
            case .hospital: return .hospital
            }
        }

        var icon: String {
            switch self {
            case .restaurant: return "fork.knife"
            case .cafe: return "cup.and.saucer"
            case .hotel: return "bed.double"
            case .parking: return "p.square"
            case .gasStation: return "fuelpump"
            case .hospital: return "cross"
            }
        }

        var color: Color {
            switch self {
            case .restaurant: return .orange
            case .cafe: return .brown
            case .hotel: return .purple
            case .parking: return .blue
            case .gasStation: return .green
            case .hospital: return .red
            }
        }
    }

    var body: some View {
        VStack(spacing: 0) {
            // カテゴリボタン
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 12) {
                    ForEach(POICategory.allCases, id: \.self) { category in
                        CategoryButton(
                            category: category,
                            isSelected: selectedCategory == category
                        ) {
                            if selectedCategory == category {
                                selectedCategory = nil
                                searchResults = []
                            } else {
                                selectedCategory = category
                                Task {
                                    await searchByCategory(category)
                                }
                            }
                        }
                    }
                }
                .padding()
            }
            .background(.regularMaterial)

            // 地図
            ZStack {
                Map(position: $position) {
                    ForEach(searchResults, id: \.self) { item in
                        Marker(
                            item.name ?? "",
                            systemImage: selectedCategory?.icon ?? "mappin",
                            coordinate: item.placemark.coordinate
                        )
                        .tint(selectedCategory?.color ?? .red)
                    }
                }

                if isSearching {
                    ProgressView()
                        .scaleEffect(1.5)
                        .padding()
                        .background(.regularMaterial)
                        .clipShape(RoundedRectangle(cornerRadius: 8))
                }
            }

            // 結果リスト
            if !searchResults.isEmpty {
                List(searchResults, id: \.self) { item in
                    HStack {
                        Image(systemName: selectedCategory?.icon ?? "mappin")
                            .foregroundStyle(selectedCategory?.color ?? .red)

                        VStack(alignment: .leading) {
                            Text(item.name ?? "Unknown")
                                .font(.headline)
                            if let address = item.placemark.title {
                                Text(address)
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                                    .lineLimit(1)
                            }
                        }
                    }
                }
                .frame(height: 200)
            }
        }
    }

    private func searchByCategory(_ category: POICategory) async {
        isSearching = true
        defer { isSearching = false }

        let request = MKLocalSearch.Request()
        request.region = MKCoordinateRegion(
            center: CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671),
            span: MKCoordinateSpan(latitudeDelta: 0.02, longitudeDelta: 0.02)
        )
        request.resultTypes = .pointOfInterest
        request.pointOfInterestFilter = MKPointOfInterestFilter(including: [category.mkCategory])

        let search = MKLocalSearch(request: request)

        do {
            let response = try await search.start()
            searchResults = response.mapItems
        } catch {
            print("検索エラー: \(error)")
            searchResults = []
        }
    }
}

struct CategoryButton: View {
    let category: CategorySearchView.POICategory
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            VStack(spacing: 4) {
                Image(systemName: category.icon)
                    .font(.title2)
                Text(category.rawValue)
                    .font(.caption)
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 8)
            .background(isSelected ? category.color.opacity(0.2) : Color.gray.opacity(0.1))
            .foregroundStyle(isSelected ? category.color : .primary)
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .overlay {
                RoundedRectangle(cornerRadius: 12)
                    .stroke(isSelected ? category.color : .clear, lineWidth: 2)
            }
        }
        .buttonStyle(.plain)
    }
}

// MARK: - 検索サジェスト

/// MKLocalSearchCompleterを使用したオートコンプリート
struct SearchCompleterView: View {
    @State private var viewModel = SearchCompleterViewModel()
    @State private var searchText = ""
    @State private var selectedResults: [MKMapItem] = []
    @State private var position: MapCameraPosition = .automatic

    var body: some View {
        VStack(spacing: 0) {
            // 検索入力
            TextField("場所を検索", text: $searchText)
                .textFieldStyle(.roundedBorder)
                .padding()
                .onChange(of: searchText) { _, newValue in
                    viewModel.search(query: newValue)
                }

            // サジェストリスト
            if !viewModel.completions.isEmpty && selectedResults.isEmpty {
                List(viewModel.completions, id: \.title) { completion in
                    Button {
                        Task {
                            await selectCompletion(completion)
                        }
                    } label: {
                        VStack(alignment: .leading) {
                            Text(completion.title)
                                .font(.body)
                            Text(completion.subtitle)
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                    .buttonStyle(.plain)
                }
                .listStyle(.plain)
            }

            // 地図
            Map(position: $position) {
                ForEach(selectedResults, id: \.self) { item in
                    Marker(item.name ?? "", coordinate: item.placemark.coordinate)
                        .tint(.red)
                }
            }
        }
    }

    private func selectCompletion(_ completion: MKLocalSearchCompletion) async {
        let request = MKLocalSearch.Request(completion: completion)
        let search = MKLocalSearch(request: request)

        do {
            let response = try await search.start()
            selectedResults = response.mapItems

            if let first = response.mapItems.first {
                position = .region(MKCoordinateRegion(
                    center: first.placemark.coordinate,
                    span: MKCoordinateSpan(latitudeDelta: 0.01, longitudeDelta: 0.01)
                ))
            }

            searchText = completion.title
            viewModel.completions = []
        } catch {
            print("検索エラー: \(error)")
        }
    }
}

@MainActor
@Observable
final class SearchCompleterViewModel: NSObject, MKLocalSearchCompleterDelegate {
    var completions: [MKLocalSearchCompletion] = []
    var isSearching = false

    private let completer = MKLocalSearchCompleter()

    override init() {
        super.init()
        completer.delegate = self
        completer.resultTypes = [.address, .pointOfInterest]
    }

    func search(query: String) {
        guard !query.isEmpty else {
            completions = []
            return
        }

        isSearching = true
        completer.queryFragment = query
    }

    // MARK: - MKLocalSearchCompleterDelegate

    nonisolated func completerDidUpdateResults(_ completer: MKLocalSearchCompleter) {
        Task { @MainActor in
            completions = completer.results
            isSearching = false
        }
    }

    nonisolated func completer(_ completer: MKLocalSearchCompleter, didFailWithError error: Error) {
        Task { @MainActor in
            isSearching = false
            completions = []
        }
    }
}

// MARK: - 選択可能な検索結果

/// 検索結果を選択して詳細を表示
struct SelectableSearchResultView: View {
    @State private var searchText = ""
    @State private var searchResults: [MKMapItem] = []
    @State private var selectedItem: MKMapItem?
    @State private var position: MapCameraPosition = .automatic

    var body: some View {
        VStack(spacing: 0) {
            // 検索バー
            HStack {
                TextField("検索", text: $searchText)
                    .textFieldStyle(.roundedBorder)

                Button("検索") {
                    Task {
                        await search()
                    }
                }
                .buttonStyle(.borderedProminent)
            }
            .padding()

            // 地図
            Map(position: $position, selection: $selectedItem) {
                ForEach(searchResults, id: \.self) { item in
                    Marker(item.name ?? "", coordinate: item.placemark.coordinate)
                        .tag(item)
                }
            }

            // 選択された場所の詳細
            if let item = selectedItem {
                SelectedItemDetail(item: item) {
                    item.openInMaps()
                }
            }
        }
    }

    private func search() async {
        guard !searchText.isEmpty else { return }

        let request = MKLocalSearch.Request()
        request.naturalLanguageQuery = searchText

        let search = MKLocalSearch(request: request)

        do {
            let response = try await search.start()
            searchResults = response.mapItems

            // 全結果が見えるように調整
            if !searchResults.isEmpty {
                let coordinates = searchResults.map { $0.placemark.coordinate }
                let minLat = coordinates.map(\.latitude).min() ?? 0
                let maxLat = coordinates.map(\.latitude).max() ?? 0
                let minLon = coordinates.map(\.longitude).min() ?? 0
                let maxLon = coordinates.map(\.longitude).max() ?? 0

                let center = CLLocationCoordinate2D(
                    latitude: (minLat + maxLat) / 2,
                    longitude: (minLon + maxLon) / 2
                )
                let span = MKCoordinateSpan(
                    latitudeDelta: (maxLat - minLat) * 1.5 + 0.01,
                    longitudeDelta: (maxLon - minLon) * 1.5 + 0.01
                )

                position = .region(MKCoordinateRegion(center: center, span: span))
            }
        } catch {
            print("検索エラー: \(error)")
        }
    }
}

struct SelectedItemDetail: View {
    let item: MKMapItem
    let onOpenInMaps: () -> Void

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(item.name ?? "Unknown")
                .font(.headline)

            if let address = item.placemark.title {
                Text(address)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
            }

            if let phone = item.phoneNumber {
                Label(phone, systemImage: "phone")
                    .font(.caption)
            }

            if let url = item.url {
                Link(destination: url) {
                    Label("Webサイト", systemImage: "globe")
                        .font(.caption)
                }
            }

            Button("Apple Mapsで開く", action: onOpenInMaps)
                .buttonStyle(.borderedProminent)
                .frame(maxWidth: .infinity)
        }
        .padding()
        .background(.regularMaterial)
    }
}

// MARK: - Preview

#Preview("Basic Search") {
    BasicLocalSearchView()
}

#Preview("Category Search") {
    CategorySearchView()
}

#Preview("Search Completer") {
    SearchCompleterView()
}

#Preview("Selectable Results") {
    SelectableSearchResultView()
}
