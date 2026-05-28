# ローカル検索 (MKLocalSearch)

MKLocalSearchを使用した周辺検索APIリファレンス。

## MKLocalSearch.Request

### 基本設定

```swift
let request = MKLocalSearch.Request()
request.naturalLanguageQuery = "カフェ"
request.region = mapView.region
```

### プロパティ

| プロパティ | 型 | 説明 |
|-----------|---|------|
| `naturalLanguageQuery` | `String?` | 検索クエリ |
| `region` | `MKCoordinateRegion` | 検索範囲 |
| `resultTypes` | `MKLocalSearch.ResultType` | 結果タイプ |
| `pointOfInterestFilter` | `MKPointOfInterestFilter?` | POIフィルター |

### ResultType

```swift
request.resultTypes = .pointOfInterest  // POIのみ
request.resultTypes = .address          // 住所のみ
request.resultTypes = [.pointOfInterest, .address]  // 両方
```

### POIフィルター

```swift
// 特定のカテゴリのみ
request.pointOfInterestFilter = MKPointOfInterestFilter(including: [.restaurant, .cafe])

// 特定のカテゴリを除外
request.pointOfInterestFilter = MKPointOfInterestFilter(excluding: [.gasStation])
```

## 検索実行

### async/await

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

### Completion Handler

```swift
func searchNearby(query: String, region: MKCoordinateRegion, completion: @escaping (Result<[MKMapItem], Error>) -> Void) {
    let request = MKLocalSearch.Request()
    request.naturalLanguageQuery = query
    request.region = region

    let search = MKLocalSearch(request: request)
    search.start { response, error in
        if let error {
            completion(.failure(error))
            return
        }

        guard let response else {
            completion(.failure(SearchError.noResponse))
            return
        }

        completion(.success(response.mapItems))
    }
}
```

## MKMapItem

### プロパティ

| プロパティ | 型 | 説明 |
|-----------|---|------|
| `name` | `String?` | 名前 |
| `phoneNumber` | `String?` | 電話番号 |
| `url` | `URL?` | ウェブサイト |
| `placemark` | `MKPlacemark` | 場所情報 |
| `pointOfInterestCategory` | `MKPointOfInterestCategory?` | POIカテゴリ |
| `timeZone` | `TimeZone?` | タイムゾーン |
| `isCurrentLocation` | `Bool` | 現在地かどうか |

### placemark プロパティ

| プロパティ | 説明 |
|-----------|------|
| `coordinate` | 座標 |
| `title` | 住所文字列 |
| `name` | 場所名 |
| `thoroughfare` | 通り名 |
| `subThoroughfare` | 番地 |
| `locality` | 市区町村 |
| `administrativeArea` | 都道府県 |
| `postalCode` | 郵便番号 |
| `country` | 国 |

## MKLocalSearchCompleter

リアルタイム検索サジェスト。

### 基本実装

```swift
@Observable
final class SearchCompleter: NSObject, MKLocalSearchCompleterDelegate {
    var results: [MKLocalSearchCompletion] = []
    var isSearching = false

    private let completer = MKLocalSearchCompleter()

    override init() {
        super.init()
        completer.delegate = self
        completer.resultTypes = [.address, .pointOfInterest]
    }

    func search(query: String) {
        isSearching = true
        completer.queryFragment = query
    }

    func cancel() {
        completer.cancel()
        isSearching = false
    }

    // MARK: - MKLocalSearchCompleterDelegate

    nonisolated func completerDidUpdateResults(_ completer: MKLocalSearchCompleter) {
        Task { @MainActor in
            results = completer.results
            isSearching = false
        }
    }

    nonisolated func completer(_ completer: MKLocalSearchCompleter, didFailWithError error: Error) {
        Task { @MainActor in
            results = []
            isSearching = false
        }
    }
}
```

### 地域を設定

```swift
completer.region = MKCoordinateRegion(
    center: CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671),
    span: MKCoordinateSpan(latitudeDelta: 0.1, longitudeDelta: 0.1)
)
```

## MKLocalSearchCompletion

サジェスト結果。

### プロパティ

| プロパティ | 型 | 説明 |
|-----------|---|------|
| `title` | `String` | タイトル |
| `subtitle` | `String` | サブタイトル |
| `titleHighlightRanges` | `[NSValue]` | ハイライト範囲 |
| `subtitleHighlightRanges` | `[NSValue]` | ハイライト範囲 |

### サジェストから検索

```swift
func search(completion: MKLocalSearchCompletion) async throws -> [MKMapItem] {
    let request = MKLocalSearch.Request(completion: completion)
    let search = MKLocalSearch(request: request)
    let response = try await search.start()
    return response.mapItems
}
```

## POIカテゴリ

### 主要カテゴリ

| カテゴリ | 説明 |
|---------|------|
| `.restaurant` | レストラン |
| `.cafe` | カフェ |
| `.bakery` | ベーカリー |
| `.hotel` | ホテル |
| `.hospital` | 病院 |
| `.pharmacy` | 薬局 |
| `.bank` | 銀行 |
| `.atm` | ATM |
| `.gasStation` | ガソリンスタンド |
| `.evCharger` | EV充電器 |
| `.parking` | 駐車場 |
| `.publicTransport` | 公共交通機関 |
| `.airport` | 空港 |
| `.store` | 店舗 |
| `.laundry` | ランドリー |
| `.postOffice` | 郵便局 |
| `.school` | 学校 |
| `.university` | 大学 |
| `.library` | 図書館 |
| `.museum` | 博物館 |
| `.theater` | 劇場 |
| `.park` | 公園 |
| `.zoo` | 動物園 |
| `.stadium` | スタジアム |
| `.beach` | ビーチ |

## 検索結果の表示

### SwiftUI

```swift
@State private var searchResults: [MKMapItem] = []
@State private var selectedItem: MKMapItem?

var body: some View {
    Map(position: $position, selection: $selectedItem) {
        ForEach(searchResults, id: \.self) { item in
            Marker(item.name ?? "Unknown", coordinate: item.placemark.coordinate)
                .tint(.orange)
                .tag(item)
        }
    }
}
```

### リスト表示

```swift
List(searchResults, id: \.self, selection: $selectedItem) { item in
    VStack(alignment: .leading) {
        Text(item.name ?? "不明")
            .font(.headline)

        if let address = item.placemark.title {
            Text(address)
                .font(.caption)
                .foregroundStyle(.secondary)
        }

        if let phone = item.phoneNumber {
            Label(phone, systemImage: "phone")
                .font(.caption)
        }
    }
}
```

## エラーハンドリング

### MKError

| コード | 説明 | 対処 |
|-------|------|------|
| `.unknown` | 不明なエラー | リトライ |
| `.serverFailure` | サーバーエラー | リトライ |
| `.loadingThrottled` | レート制限 | 待機してリトライ |
| `.placemarkNotFound` | 場所が見つからない | クエリを変更 |

### エラーハンドリング例

```swift
func searchNearby(query: String, region: MKCoordinateRegion) async throws -> [MKMapItem] {
    do {
        let request = MKLocalSearch.Request()
        request.naturalLanguageQuery = query
        request.region = region

        let search = MKLocalSearch(request: request)
        let response = try await search.start()

        return response.mapItems
    } catch let error as MKError {
        switch error.code {
        case .placemarkNotFound:
            return []  // 結果なし
        case .serverFailure:
            throw SearchError.serverError
        case .loadingThrottled:
            throw SearchError.rateLimited
        default:
            throw SearchError.unknown(error)
        }
    }
}

enum SearchError: Error {
    case serverError
    case rateLimited
    case unknown(Error)
}
```

## 使用上の注意

1. **レート制限** - 短時間に多数のリクエストを送らない
2. **地域指定** - 適切な検索範囲を設定
3. **キャンセル** - 不要になった検索はキャンセル
4. **言語** - システム言語に応じた結果が返る
5. **結果数** - 返される結果数に制限がある
