# MKLocalSearch Reference

MKLocalSearchを使用した周辺検索とPOI検索の詳細ガイド。

## MKLocalSearch.Request

検索リクエストを構成。

### 基本的な設定

```swift
let request = MKLocalSearch.Request()

// 自然言語クエリ
request.naturalLanguageQuery = "カフェ"

// 検索範囲
request.region = MKCoordinateRegion(
    center: CLLocationCoordinate2D(latitude: 35.6762, longitude: 139.6503),
    span: MKCoordinateSpan(latitudeDelta: 0.1, longitudeDelta: 0.1)
)
```

### 結果タイプの指定

```swift
// アドレスのみ
request.resultTypes = .address

// POI（Point of Interest）のみ
request.resultTypes = .pointOfInterest

// 両方
request.resultTypes = [.address, .pointOfInterest]
```

### POIカテゴリフィルター

```swift
// 特定のカテゴリのみ
request.pointOfInterestFilter = MKPointOfInterestFilter(including: [
    .restaurant,
    .cafe,
    .bakery
])

// 特定のカテゴリを除外
request.pointOfInterestFilter = MKPointOfInterestFilter(excluding: [
    .parking,
    .gasStation
])

// 全てのカテゴリ
request.pointOfInterestFilter = .includingAll

// カテゴリなし
request.pointOfInterestFilter = .excludingAll
```

### 主要なPOIカテゴリ

```swift
// 飲食
MKPointOfInterestCategory.restaurant     // レストラン
MKPointOfInterestCategory.cafe           // カフェ
MKPointOfInterestCategory.bakery         // ベーカリー
MKPointOfInterestCategory.brewery        // ブルワリー
MKPointOfInterestCategory.winery         // ワイナリー
MKPointOfInterestCategory.foodMarket     // 食品市場
MKPointOfInterestCategory.nightlife      // ナイトライフ

// 交通
MKPointOfInterestCategory.airport        // 空港
MKPointOfInterestCategory.publicTransport // 公共交通
MKPointOfInterestCategory.parking        // 駐車場
MKPointOfInterestCategory.gasStation     // ガソリンスタンド
MKPointOfInterestCategory.evCharger      // EV充電器
MKPointOfInterestCategory.carRental      // レンタカー

// 宿泊・観光
MKPointOfInterestCategory.hotel          // ホテル
MKPointOfInterestCategory.museum         // 博物館
MKPointOfInterestCategory.theater        // 劇場
MKPointOfInterestCategory.movieTheater   // 映画館
MKPointOfInterestCategory.nationalPark   // 国立公園
MKPointOfInterestCategory.park           // 公園
MKPointOfInterestCategory.beach          // ビーチ
MKPointOfInterestCategory.zoo            // 動物園
MKPointOfInterestCategory.aquarium       // 水族館
MKPointOfInterestCategory.campground     // キャンプ場

// 買い物
MKPointOfInterestCategory.store          // 店舗
MKPointOfInterestCategory.pharmacy       // 薬局

// 医療・サービス
MKPointOfInterestCategory.hospital       // 病院
MKPointOfInterestCategory.police         // 警察
MKPointOfInterestCategory.fireStation    // 消防署
MKPointOfInterestCategory.postOffice     // 郵便局
MKPointOfInterestCategory.bank           // 銀行
MKPointOfInterestCategory.atm            // ATM

// スポーツ・フィットネス
MKPointOfInterestCategory.stadium        // スタジアム
MKPointOfInterestCategory.fitnessCenter  // フィットネスセンター
MKPointOfInterestCategory.golf           // ゴルフ

// 教育
MKPointOfInterestCategory.school         // 学校
MKPointOfInterestCategory.university     // 大学
MKPointOfInterestCategory.library        // 図書館

// その他
MKPointOfInterestCategory.laundry        // ランドリー
MKPointOfInterestCategory.marina         // マリーナ
MKPointOfInterestCategory.convention     // コンベンション
```

## MKLocalSearch

検索を実行。

### 基本的な使用

```swift
func searchNearby(query: String, region: MKCoordinateRegion) async throws -> [MKMapItem] {
    let request = MKLocalSearch.Request()
    request.naturalLanguageQuery = query
    request.region = region

    let search = MKLocalSearch(request: request)
    let response = try await search.start()

    return response.mapItems
}
```

### カテゴリ検索

```swift
func searchByCategory(
    category: MKPointOfInterestCategory,
    region: MKCoordinateRegion
) async throws -> [MKMapItem] {
    let request = MKLocalSearch.Request()
    request.region = region
    request.resultTypes = .pointOfInterest
    request.pointOfInterestFilter = MKPointOfInterestFilter(including: [category])

    let search = MKLocalSearch(request: request)
    let response = try await search.start()

    return response.mapItems
}
```

### 複合検索

```swift
func searchRestaurantsNearby(
    query: String,
    coordinate: CLLocationCoordinate2D,
    radius: CLLocationDistance = 1000
) async throws -> [MKMapItem] {
    let request = MKLocalSearch.Request()
    request.naturalLanguageQuery = query
    request.region = MKCoordinateRegion(
        center: coordinate,
        latitudinalMeters: radius * 2,
        longitudinalMeters: radius * 2
    )
    request.resultTypes = .pointOfInterest
    request.pointOfInterestFilter = MKPointOfInterestFilter(including: [
        .restaurant,
        .cafe
    ])

    let search = MKLocalSearch(request: request)
    let response = try await search.start()

    return response.mapItems
}
```

## MKMapItem

検索結果の各アイテム。

### 主要プロパティ

```swift
let mapItem: MKMapItem

// 場所情報
mapItem.placemark              // MKPlacemark
mapItem.name                   // 名前
mapItem.phoneNumber            // 電話番号
mapItem.url                    // Webサイト

// 位置
mapItem.placemark.coordinate   // CLLocationCoordinate2D

// POI情報
mapItem.pointOfInterestCategory // MKPointOfInterestCategory?

// 時間帯
mapItem.timeZone               // TimeZone?
```

### MKPlacemark 詳細

```swift
let placemark = mapItem.placemark

// 住所
placemark.thoroughfare         // 通り名
placemark.subThoroughfare      // 番地
placemark.locality             // 市区町村
placemark.administrativeArea   // 都道府県
placemark.postalCode           // 郵便番号
placemark.country              // 国

// フォーマット済み住所
placemark.title               // 完全な住所文字列
```

### Apple Mapsで開く

```swift
func openInMaps(mapItem: MKMapItem) {
    mapItem.openInMaps(launchOptions: [
        MKLaunchOptionsDirectionsModeKey: MKLaunchOptionsDirectionsModeDriving
    ])
}

// 経路オプション
MKLaunchOptionsDirectionsModeDriving   // 車
MKLaunchOptionsDirectionsModeWalking   // 徒歩
MKLaunchOptionsDirectionsModeTransit   // 公共交通
```

## MKLocalSearchCompleter

検索サジェスト（オートコンプリート）を提供。

### 基本的な使用

```swift
@MainActor
@Observable
final class SearchCompleterViewModel: NSObject, MKLocalSearchCompleterDelegate {
    var completions: [MKLocalSearchCompletion] = []
    var isSearching = false

    private let completer = MKLocalSearchCompleter()

    override init() {
        super.init()
        completer.delegate = self
        completer.resultTypes = [.address, .pointOfInterest, .query]
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
```

### 結果タイプの設定

```swift
// 住所のみ
completer.resultTypes = .address

// POIのみ
completer.resultTypes = .pointOfInterest

// クエリ候補
completer.resultTypes = .query

// 全て
completer.resultTypes = [.address, .pointOfInterest, .query]
```

### 検索範囲の設定

```swift
// 地域を限定
completer.region = MKCoordinateRegion(
    center: CLLocationCoordinate2D(latitude: 35.6762, longitude: 139.6503),
    span: MKCoordinateSpan(latitudeDelta: 0.5, longitudeDelta: 0.5)
)

// POIフィルター
completer.pointOfInterestFilter = MKPointOfInterestFilter(including: [
    .restaurant,
    .cafe
])
```

### MKLocalSearchCompletion

```swift
let completion: MKLocalSearchCompletion

// タイトルとサブタイトル
completion.title              // "東京駅"
completion.subtitle           // "東京都千代田区丸の内1丁目"

// ハイライト範囲
completion.titleHighlightRanges    // [NSValue] タイトル内のマッチ範囲
completion.subtitleHighlightRanges // [NSValue] サブタイトル内のマッチ範囲
```

### Completionから検索を実行

```swift
func search(completion: MKLocalSearchCompletion) async throws -> [MKMapItem] {
    let request = MKLocalSearch.Request(completion: completion)

    let search = MKLocalSearch(request: request)
    let response = try await search.start()

    return response.mapItems
}
```

## SwiftUI統合

### 検索バーと結果表示

```swift
struct SearchView: View {
    @State private var viewModel = SearchCompleterViewModel()
    @State private var searchText = ""
    @State private var selectedItems: [MKMapItem] = []

    var body: some View {
        VStack {
            // 検索バー
            TextField("場所を検索", text: $searchText)
                .textFieldStyle(.roundedBorder)
                .padding()
                .onChange(of: searchText) { _, newValue in
                    viewModel.search(query: newValue)
                }

            // サジェストリスト
            if !viewModel.completions.isEmpty {
                List(viewModel.completions, id: \.title) { completion in
                    VStack(alignment: .leading) {
                        Text(completion.title)
                            .font(.body)
                        Text(completion.subtitle)
                            .font(.caption)
                            .foregroundStyle(.secondary)
                    }
                    .onTapGesture {
                        Task {
                            selectedItems = try await search(completion: completion)
                        }
                    }
                }
            }

            // 地図
            Map {
                ForEach(selectedItems, id: \.self) { item in
                    Marker(item.name ?? "", coordinate: item.placemark.coordinate)
                }
            }
        }
    }

    private func search(completion: MKLocalSearchCompletion) async throws -> [MKMapItem] {
        let request = MKLocalSearch.Request(completion: completion)
        let search = MKLocalSearch(request: request)
        let response = try await search.start()
        return response.mapItems
    }
}
```

### カテゴリボタン

```swift
struct CategorySearchView: View {
    @State private var selectedCategory: MKPointOfInterestCategory?
    @State private var searchResults: [MKMapItem] = []

    let categories: [(MKPointOfInterestCategory, String, String)] = [
        (.restaurant, "レストラン", "fork.knife"),
        (.cafe, "カフェ", "cup.and.saucer"),
        (.hotel, "ホテル", "bed.double"),
        (.parking, "駐車場", "p.square"),
        (.gasStation, "ガソリン", "fuelpump")
    ]

    var body: some View {
        VStack {
            // カテゴリボタン
            ScrollView(.horizontal, showsIndicators: false) {
                HStack {
                    ForEach(categories, id: \.0) { category, name, icon in
                        Button {
                            selectedCategory = category
                            Task {
                                await searchByCategory(category)
                            }
                        } label: {
                            Label(name, systemImage: icon)
                                .padding(.horizontal, 12)
                                .padding(.vertical, 8)
                                .background(selectedCategory == category ? .blue : .gray.opacity(0.2))
                                .foregroundStyle(selectedCategory == category ? .white : .primary)
                                .clipShape(Capsule())
                        }
                    }
                }
                .padding()
            }

            // 結果リスト
            List(searchResults, id: \.self) { item in
                VStack(alignment: .leading) {
                    Text(item.name ?? "Unknown")
                        .font(.headline)
                    Text(item.placemark.title ?? "")
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }
            }
        }
    }

    private func searchByCategory(_ category: MKPointOfInterestCategory) async {
        let request = MKLocalSearch.Request()
        request.resultTypes = .pointOfInterest
        request.pointOfInterestFilter = MKPointOfInterestFilter(including: [category])
        // 現在地周辺を検索（実際は位置情報から取得）
        request.region = MKCoordinateRegion(
            center: CLLocationCoordinate2D(latitude: 35.6762, longitude: 139.6503),
            span: MKCoordinateSpan(latitudeDelta: 0.05, longitudeDelta: 0.05)
        )

        let search = MKLocalSearch(request: request)

        do {
            let response = try await search.start()
            searchResults = response.mapItems
        } catch {
            searchResults = []
        }
    }
}
```

## エラーハンドリング

### MKError

| コード | 名前 | 説明 |
|--------|------|------|
| 1 | `unknown` | 不明なエラー |
| 2 | `serverFailure` | サーバーエラー |
| 3 | `loadingThrottled` | リクエスト制限 |
| 4 | `placemarkNotFound` | 場所が見つからない |

### エラー処理パターン

```swift
func searchSafely(query: String, region: MKCoordinateRegion) async -> Result<[MKMapItem], SearchError> {
    let request = MKLocalSearch.Request()
    request.naturalLanguageQuery = query
    request.region = region

    let search = MKLocalSearch(request: request)

    do {
        let response = try await search.start()
        return .success(response.mapItems)
    } catch let error as MKError {
        switch error.code {
        case .placemarkNotFound:
            return .failure(.noResults)
        case .serverFailure:
            return .failure(.serverError)
        case .loadingThrottled:
            return .failure(.rateLimited)
        default:
            return .failure(.unknown(error))
        }
    } catch {
        return .failure(.unknown(error))
    }
}

enum SearchError: Error {
    case noResults
    case serverError
    case rateLimited
    case unknown(Error)
}
```

## ベストプラクティス

### デバウンス

```swift
@Observable
final class DebouncedSearchViewModel {
    var searchText = ""
    var results: [MKMapItem] = []

    private var searchTask: Task<Void, Never>?

    func search() {
        searchTask?.cancel()

        searchTask = Task {
            // 300ms待機
            try? await Task.sleep(for: .milliseconds(300))

            guard !Task.isCancelled else { return }

            await performSearch()
        }
    }

    private func performSearch() async {
        guard !searchText.isEmpty else {
            results = []
            return
        }

        let request = MKLocalSearch.Request()
        request.naturalLanguageQuery = searchText

        let search = MKLocalSearch(request: request)

        do {
            let response = try await search.start()
            results = response.mapItems
        } catch {
            results = []
        }
    }
}
```

### キャッシュ

```swift
actor SearchCache {
    private var cache: [String: [MKMapItem]] = [:]
    private let maxCacheSize = 100

    func search(query: String, region: MKCoordinateRegion) async throws -> [MKMapItem] {
        let key = "\(query)-\(region.center.latitude)-\(region.center.longitude)"

        if let cached = cache[key] {
            return cached
        }

        let request = MKLocalSearch.Request()
        request.naturalLanguageQuery = query
        request.region = region

        let search = MKLocalSearch(request: request)
        let response = try await search.start()

        // キャッシュサイズ管理
        if cache.count >= maxCacheSize {
            cache.removeAll()
        }

        cache[key] = response.mapItems

        return response.mapItems
    }
}
```
