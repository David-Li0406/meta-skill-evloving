// MARK: - Local Search View Example
// macOS 14+ SwiftUI ローカル検索

import SwiftUI
import MapKit

// MARK: - ローカル検索View

/// 周辺検索を行うView
struct LocalSearchView: View {
    @State private var position: MapCameraPosition = .region(MKCoordinateRegion(
        center: CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671),
        span: MKCoordinateSpan(latitudeDelta: 0.05, longitudeDelta: 0.05)
    ))
    @State private var searchResults: [MKMapItem] = []
    @State private var selectedItem: MKMapItem?
    @State private var searchQuery = ""
    @State private var isSearching = false

    var body: some View {
        HSplitView {
            // 地図
            Map(position: $position, selection: $selectedItem) {
                ForEach(searchResults, id: \.self) { item in
                    Marker(item.name ?? "Unknown", coordinate: item.placemark.coordinate)
                        .tint(.orange)
                }
            }
            .mapStyle(.standard)
            .mapControls {
                MapCompass()
                MapScaleView()
                MapZoomStepper()
            }
            .onChange(of: selectedItem) { _, newItem in
                if let item = newItem {
                    withAnimation {
                        position = .item(item)
                    }
                }
            }

            // 検索パネル
            VStack(alignment: .leading, spacing: 16) {
                Text("周辺検索")
                    .font(.headline)

                // 検索フィールド
                HStack {
                    TextField("検索キーワード", text: $searchQuery)
                        .textFieldStyle(.roundedBorder)
                        .onSubmit {
                            Task {
                                await search()
                            }
                        }

                    Button {
                        Task {
                            await search()
                        }
                    } label: {
                        Image(systemName: "magnifyingglass")
                    }
                    .disabled(searchQuery.isEmpty || isSearching)
                }

                // クイック検索ボタン
                HStack(spacing: 8) {
                    QuickSearchButton(query: "カフェ", icon: "cup.and.saucer.fill") {
                        searchQuery = "カフェ"
                        Task { await search() }
                    }
                    QuickSearchButton(query: "レストラン", icon: "fork.knife") {
                        searchQuery = "レストラン"
                        Task { await search() }
                    }
                    QuickSearchButton(query: "コンビニ", icon: "cart.fill") {
                        searchQuery = "コンビニ"
                        Task { await search() }
                    }
                }

                Divider()

                // 検索結果
                if isSearching {
                    HStack {
                        ProgressView()
                        Text("検索中...")
                            .foregroundStyle(.secondary)
                    }
                } else if searchResults.isEmpty && !searchQuery.isEmpty {
                    ContentUnavailableView(
                        "結果なし",
                        systemImage: "magnifyingglass",
                        description: Text("「\(searchQuery)」の検索結果はありません")
                    )
                } else {
                    List(searchResults, id: \.self, selection: $selectedItem) { item in
                        SearchResultRow(item: item)
                    }
                }
            }
            .padding()
            .frame(minWidth: 280, maxWidth: 350)
        }
    }

    private func search() async {
        guard !searchQuery.isEmpty else { return }

        isSearching = true

        let request = MKLocalSearch.Request()
        request.naturalLanguageQuery = searchQuery

        // 現在の表示領域を検索範囲に設定
        if case let .region(region) = position {
            request.region = region
        }

        let search = MKLocalSearch(request: request)

        do {
            let response = try await search.start()
            searchResults = response.mapItems
        } catch {
            searchResults = []
        }

        isSearching = false
    }
}

// MARK: - クイック検索ボタン

struct QuickSearchButton: View {
    let query: String
    let icon: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Label(query, systemImage: icon)
                .font(.caption)
        }
        .buttonStyle(.bordered)
        .controlSize(.small)
    }
}

// MARK: - 検索結果行

struct SearchResultRow: View {
    let item: MKMapItem

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(item.name ?? "不明な場所")
                .font(.headline)

            if let address = item.placemark.title {
                Text(address)
                    .font(.caption)
                    .foregroundStyle(.secondary)
                    .lineLimit(2)
            }

            if let phone = item.phoneNumber {
                Label(phone, systemImage: "phone")
                    .font(.caption)
                    .foregroundStyle(.blue)
            }
        }
        .padding(.vertical, 4)
    }
}

// MARK: - 検索サジェスト付きView

/// 検索サジェストを提供するView
struct SearchWithSuggestionsView: View {
    @State private var position: MapCameraPosition = .automatic
    @State private var searchText = ""
    @State private var suggestions: [MKLocalSearchCompletion] = []
    @State private var searchResults: [MKMapItem] = []
    @State private var completer = SearchCompleter()

    var body: some View {
        HSplitView {
            // 地図
            Map(position: $position) {
                ForEach(searchResults, id: \.self) { item in
                    Marker(item.name ?? "Unknown", coordinate: item.placemark.coordinate)
                }
            }
            .mapStyle(.standard)

            // 検索パネル
            VStack(alignment: .leading, spacing: 16) {
                Text("場所を検索")
                    .font(.headline)

                TextField("検索", text: $searchText)
                    .textFieldStyle(.roundedBorder)
                    .onChange(of: searchText) { _, newValue in
                        completer.search(query: newValue)
                    }

                // サジェスト表示
                if !completer.results.isEmpty, searchText.count > 0 {
                    GroupBox("候補") {
                        ScrollView {
                            VStack(alignment: .leading, spacing: 0) {
                                ForEach(completer.results, id: \.self) { suggestion in
                                    Button {
                                        Task {
                                            await selectSuggestion(suggestion)
                                        }
                                    } label: {
                                        VStack(alignment: .leading, spacing: 2) {
                                            Text(suggestion.title)
                                                .font(.callout)
                                            Text(suggestion.subtitle)
                                                .font(.caption)
                                                .foregroundStyle(.secondary)
                                        }
                                        .padding(.vertical, 6)
                                        .frame(maxWidth: .infinity, alignment: .leading)
                                    }
                                    .buttonStyle(.plain)
                                    Divider()
                                }
                            }
                        }
                        .frame(maxHeight: 200)
                    }
                }

                // 検索結果
                if !searchResults.isEmpty {
                    GroupBox("結果") {
                        List(searchResults, id: \.self) { item in
                            VStack(alignment: .leading) {
                                Text(item.name ?? "不明")
                                    .font(.callout)
                                if let address = item.placemark.title {
                                    Text(address)
                                        .font(.caption)
                                        .foregroundStyle(.secondary)
                                }
                            }
                        }
                    }
                }

                Spacer()
            }
            .padding()
            .frame(minWidth: 280, maxWidth: 350)
        }
    }

    private func selectSuggestion(_ suggestion: MKLocalSearchCompletion) async {
        let request = MKLocalSearch.Request(completion: suggestion)
        let search = MKLocalSearch(request: request)

        do {
            let response = try await search.start()
            searchResults = response.mapItems
            searchText = suggestion.title

            if let firstItem = response.mapItems.first {
                position = .item(firstItem)
            }
        } catch {
            searchResults = []
        }
    }
}

// MARK: - SearchCompleter

@Observable
final class SearchCompleter: NSObject, MKLocalSearchCompleterDelegate {
    var results: [MKLocalSearchCompletion] = []
    private let completer = MKLocalSearchCompleter()

    override init() {
        super.init()
        completer.delegate = self
        completer.resultTypes = [.address, .pointOfInterest]
    }

    func search(query: String) {
        completer.queryFragment = query
    }

    nonisolated func completerDidUpdateResults(_ completer: MKLocalSearchCompleter) {
        Task { @MainActor in
            results = completer.results
        }
    }

    nonisolated func completer(_ completer: MKLocalSearchCompleter, didFailWithError error: Error) {
        Task { @MainActor in
            results = []
        }
    }
}

// MARK: - Preview

#Preview("Local Search") {
    LocalSearchView()
        .frame(width: 900, height: 600)
}

#Preview("Search with Suggestions") {
    SearchWithSuggestionsView()
        .frame(width: 900, height: 600)
}
