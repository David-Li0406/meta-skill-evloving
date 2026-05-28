# Complete Combine Patterns Reference

<!-- Loading Trigger: Load this reference when implementing reactive data flows, bridging Combine with async/await, building custom publishers, or debugging memory leaks in Combine subscriptions -->

## Advanced Publisher Types

```swift
import Combine
import Foundation

// MARK: - Custom Publisher for Network Requests

struct NetworkPublisher<Output: Decodable>: Publisher {
    typealias Failure = NetworkError

    let request: URLRequest
    let session: URLSession
    let decoder: JSONDecoder

    func receive<S>(subscriber: S) where S: Subscriber, Failure == S.Failure, Output == S.Input {
        let subscription = NetworkSubscription(
            subscriber: subscriber,
            request: request,
            session: session,
            decoder: decoder
        )
        subscriber.receive(subscription: subscription)
    }
}

private final class NetworkSubscription<S: Subscriber, Output: Decodable>: Subscription
where S.Input == Output, S.Failure == NetworkError {

    private var subscriber: S?
    private var task: URLSessionDataTask?
    private let request: URLRequest
    private let session: URLSession
    private let decoder: JSONDecoder

    init(subscriber: S, request: URLRequest, session: URLSession, decoder: JSONDecoder) {
        self.subscriber = subscriber
        self.request = request
        self.session = session
        self.decoder = decoder
    }

    func request(_ demand: Subscribers.Demand) {
        guard demand > 0, subscriber != nil else { return }

        task = session.dataTask(with: request) { [weak self] data, response, error in
            guard let self = self, let subscriber = self.subscriber else { return }

            if let error = error {
                subscriber.receive(completion: .failure(.underlying(error)))
                return
            }

            guard let httpResponse = response as? HTTPURLResponse else {
                subscriber.receive(completion: .failure(.invalidResponse))
                return
            }

            guard (200...299).contains(httpResponse.statusCode) else {
                subscriber.receive(completion: .failure(.httpError(httpResponse.statusCode)))
                return
            }

            guard let data = data else {
                subscriber.receive(completion: .failure(.noData))
                return
            }

            do {
                let decoded = try self.decoder.decode(Output.self, from: data)
                _ = subscriber.receive(decoded)
                subscriber.receive(completion: .finished)
            } catch {
                subscriber.receive(completion: .failure(.decodingError(error)))
            }
        }

        task?.resume()
    }

    func cancel() {
        task?.cancel()
        subscriber = nil
    }
}

enum NetworkError: Error {
    case invalidResponse
    case httpError(Int)
    case noData
    case decodingError(Error)
    case underlying(Error)
}
```

## Comprehensive ViewModel Pattern

```swift
import Combine
import SwiftUI

// MARK: - Base ViewModel Protocol

protocol ViewModelProtocol: ObservableObject {
    associatedtype Input
    associatedtype Output

    func transform(input: Input) -> Output
}

// MARK: - Cancellable Store

final class CancellableStore {
    var cancellables = Set<AnyCancellable>()

    func store(_ cancellable: AnyCancellable) {
        cancellables.insert(cancellable)
    }

    func cancelAll() {
        cancellables.forEach { $0.cancel() }
        cancellables.removeAll()
    }
}

// MARK: - Search ViewModel with Full Pattern

@MainActor
final class SearchViewModel: ObservableObject {

    // MARK: - Input

    struct Input {
        let searchText: AnyPublisher<String, Never>
        let refresh: AnyPublisher<Void, Never>
        let loadMore: AnyPublisher<Void, Never>
        let itemSelected: AnyPublisher<SearchResult, Never>
    }

    // MARK: - Output

    struct Output {
        let results: AnyPublisher<[SearchResult], Never>
        let isLoading: AnyPublisher<Bool, Never>
        let error: AnyPublisher<Error?, Never>
        let isEmpty: AnyPublisher<Bool, Never>
        let selectedItem: AnyPublisher<SearchResult, Never>
    }

    // MARK: - Published State

    @Published private(set) var results: [SearchResult] = []
    @Published private(set) var isLoading = false
    @Published private(set) var error: Error?
    @Published var searchText = ""

    // MARK: - Private

    private let searchService: SearchServiceProtocol
    private var cancellables = Set<AnyCancellable>()
    private var currentPage = 1
    private var hasMorePages = true
    private let selectedItemSubject = PassthroughSubject<SearchResult, Never>()

    // MARK: - Init

    init(searchService: SearchServiceProtocol) {
        self.searchService = searchService
        setupSearchPipeline()
    }

    // MARK: - Transform

    func transform(input: Input) -> Output {
        // Handle search text changes
        input.searchText
            .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
            .removeDuplicates()
            .sink { [weak self] text in
                self?.searchText = text
                self?.performSearch(query: text, isRefresh: true)
            }
            .store(in: &cancellables)

        // Handle refresh
        input.refresh
            .sink { [weak self] in
                guard let self = self else { return }
                self.performSearch(query: self.searchText, isRefresh: true)
            }
            .store(in: &cancellables)

        // Handle load more
        input.loadMore
            .filter { [weak self] in
                guard let self = self else { return false }
                return !self.isLoading && self.hasMorePages
            }
            .sink { [weak self] in
                guard let self = self else { return }
                self.loadNextPage()
            }
            .store(in: &cancellables)

        // Handle item selection
        input.itemSelected
            .sink { [weak self] item in
                self?.selectedItemSubject.send(item)
            }
            .store(in: &cancellables)

        // Build output
        return Output(
            results: $results.eraseToAnyPublisher(),
            isLoading: $isLoading.eraseToAnyPublisher(),
            error: $error.eraseToAnyPublisher(),
            isEmpty: $results.map { $0.isEmpty }.eraseToAnyPublisher(),
            selectedItem: selectedItemSubject.eraseToAnyPublisher()
        )
    }

    // MARK: - Private Methods

    private func setupSearchPipeline() {
        $searchText
            .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
            .removeDuplicates()
            .filter { !$0.isEmpty }
            .sink { [weak self] query in
                self?.performSearch(query: query, isRefresh: true)
            }
            .store(in: &cancellables)
    }

    private func performSearch(query: String, isRefresh: Bool) {
        guard !query.isEmpty else {
            results = []
            return
        }

        if isRefresh {
            currentPage = 1
            hasMorePages = true
        }

        isLoading = true
        error = nil

        Task {
            do {
                let response = try await searchService.search(query: query, page: currentPage)

                if isRefresh {
                    results = response.results
                } else {
                    results.append(contentsOf: response.results)
                }

                hasMorePages = response.hasMorePages
                currentPage = response.currentPage

            } catch {
                self.error = error
            }

            isLoading = false
        }
    }

    private func loadNextPage() {
        currentPage += 1
        performSearch(query: searchText, isRefresh: false)
    }
}

// MARK: - Supporting Types

struct SearchResult: Identifiable, Hashable {
    let id: String
    let title: String
    let description: String
}

struct SearchResponse {
    let results: [SearchResult]
    let currentPage: Int
    let hasMorePages: Bool
}

protocol SearchServiceProtocol {
    func search(query: String, page: Int) async throws -> SearchResponse
}
```

## Subject Patterns and Best Practices

```swift
import Combine

// MARK: - Type-Safe Event System

enum AppEvent {
    case userLoggedIn(User)
    case userLoggedOut
    case cartUpdated(Cart)
    case notificationReceived(NotificationPayload)
    case networkStatusChanged(isConnected: Bool)
}

final class EventBus {
    static let shared = EventBus()

    // Single subject for all events
    private let eventSubject = PassthroughSubject<AppEvent, Never>()

    // Type-erased publisher for external access
    var events: AnyPublisher<AppEvent, Never> {
        eventSubject.eraseToAnyPublisher()
    }

    // Filtered publishers for specific events
    var userLoggedIn: AnyPublisher<User, Never> {
        events.compactMap { event in
            if case .userLoggedIn(let user) = event {
                return user
            }
            return nil
        }
        .eraseToAnyPublisher()
    }

    var userLoggedOut: AnyPublisher<Void, Never> {
        events.compactMap { event in
            if case .userLoggedOut = event {
                return ()
            }
            return nil
        }
        .eraseToAnyPublisher()
    }

    var cartUpdated: AnyPublisher<Cart, Never> {
        events.compactMap { event in
            if case .cartUpdated(let cart) = event {
                return cart
            }
            return nil
        }
        .eraseToAnyPublisher()
    }

    var networkStatus: AnyPublisher<Bool, Never> {
        events.compactMap { event in
            if case .networkStatusChanged(let isConnected) = event {
                return isConnected
            }
            return nil
        }
        .removeDuplicates()
        .eraseToAnyPublisher()
    }

    // MARK: - Send Events

    func send(_ event: AppEvent) {
        eventSubject.send(event)
    }

    private init() {}
}

// MARK: - CurrentValueSubject Wrapper for State

@propertyWrapper
final class PublishedState<Value> {
    private let subject: CurrentValueSubject<Value, Never>

    var wrappedValue: Value {
        get { subject.value }
        set { subject.send(newValue) }
    }

    var projectedValue: AnyPublisher<Value, Never> {
        subject.eraseToAnyPublisher()
    }

    init(wrappedValue: Value) {
        self.subject = CurrentValueSubject(wrappedValue)
    }
}

// MARK: - Usage Example

final class StateManager {
    @PublishedState var currentUser: User?
    @PublishedState var isOnboarded: Bool = false
    @PublishedState var selectedTheme: Theme = .system

    private var cancellables = Set<AnyCancellable>()

    init() {
        // React to state changes
        $currentUser
            .sink { user in
                print("User changed: \(user?.name ?? "nil")")
            }
            .store(in: &cancellables)
    }
}
```

## Combine Operators Deep Dive

```swift
import Combine

// MARK: - Custom Operators

extension Publisher {

    /// Retries with exponential backoff
    func retryWithBackoff(
        maxRetries: Int,
        initialDelay: TimeInterval = 1.0,
        maxDelay: TimeInterval = 60.0,
        scheduler: some Scheduler
    ) -> AnyPublisher<Output, Failure> {
        self.catch { error -> AnyPublisher<Output, Failure> in
            var currentRetry = 0

            return Deferred {
                if currentRetry >= maxRetries {
                    return Fail<Output, Failure>(error: error)
                        .eraseToAnyPublisher()
                }

                let delay = min(initialDelay * pow(2.0, Double(currentRetry)), maxDelay)
                currentRetry += 1

                return Just(())
                    .delay(for: .seconds(delay), scheduler: scheduler)
                    .flatMap { _ in self }
                    .eraseToAnyPublisher()
            }
            .eraseToAnyPublisher()
        }
        .eraseToAnyPublisher()
    }

    /// Share and replay the last value
    func shareReplay() -> AnyPublisher<Output, Failure> {
        multicast(subject: CurrentValueSubject<Output?, Failure>(nil))
            .autoconnect()
            .compactMap { $0 }
            .eraseToAnyPublisher()
    }

    /// Only emit if value passes predicate, otherwise complete
    func filterOrComplete(_ predicate: @escaping (Output) -> Bool) -> AnyPublisher<Output, Failure> {
        flatMap { value -> AnyPublisher<Output, Failure> in
            if predicate(value) {
                return Just(value).setFailureType(to: Failure.self).eraseToAnyPublisher()
            } else {
                return Empty().eraseToAnyPublisher()
            }
        }
        .eraseToAnyPublisher()
    }

    /// Map and unwrap optional, skipping nil values
    func compactMapAsync<T>(
        _ transform: @escaping (Output) async -> T?
    ) -> AnyPublisher<T, Failure> {
        flatMap { value -> AnyPublisher<T, Failure> in
            Future<T?, Failure> { promise in
                Task {
                    let result = await transform(value)
                    promise(.success(result))
                }
            }
            .compactMap { $0 }
            .eraseToAnyPublisher()
        }
        .eraseToAnyPublisher()
    }
}

extension Publisher where Failure == Never {

    /// Assign to a weak reference to avoid retain cycles
    func assignWeak<Root: AnyObject>(
        to keyPath: ReferenceWritableKeyPath<Root, Output>,
        on object: Root
    ) -> AnyCancellable {
        sink { [weak object] value in
            object?[keyPath: keyPath] = value
        }
    }

    /// Convert Never-failing publisher to async sequence
    var values: AsyncPublisher<Self> {
        AsyncPublisher(self)
    }
}

// MARK: - AsyncPublisher for Bridging

struct AsyncPublisher<P: Publisher>: AsyncSequence where P.Failure == Never {
    typealias Element = P.Output

    let publisher: P

    init(_ publisher: P) {
        self.publisher = publisher
    }

    func makeAsyncIterator() -> AsyncIterator {
        AsyncIterator(publisher: publisher)
    }

    struct AsyncIterator: AsyncIteratorProtocol {
        var iterator: AsyncStream<P.Output>.Iterator
        var cancellable: AnyCancellable?

        init(publisher: P) {
            var cancellable: AnyCancellable?
            let stream = AsyncStream<P.Output> { continuation in
                cancellable = publisher.sink { value in
                    continuation.yield(value)
                }
            }
            self.iterator = stream.makeAsyncIterator()
            self.cancellable = cancellable
        }

        mutating func next() async -> P.Output? {
            await iterator.next()
        }
    }
}
```

## Combine + Async/Await Bridges

```swift
import Combine

// MARK: - Publisher to Async

extension Publisher {

    /// Get first value from publisher
    func firstValue() async throws -> Output {
        try await withCheckedThrowingContinuation { continuation in
            var cancellable: AnyCancellable?
            var didResume = false

            cancellable = first()
                .sink(
                    receiveCompletion: { completion in
                        guard !didResume else { return }

                        switch completion {
                        case .finished:
                            // Value should have been received
                            break
                        case .failure(let error):
                            didResume = true
                            continuation.resume(throwing: error)
                        }
                        cancellable?.cancel()
                    },
                    receiveValue: { value in
                        guard !didResume else { return }
                        didResume = true
                        continuation.resume(returning: value)
                    }
                )
        }
    }

    /// Collect all values into array
    func collectValues() async throws -> [Output] {
        try await withCheckedThrowingContinuation { continuation in
            var values: [Output] = []
            var cancellable: AnyCancellable?

            cancellable = sink(
                receiveCompletion: { completion in
                    switch completion {
                    case .finished:
                        continuation.resume(returning: values)
                    case .failure(let error):
                        continuation.resume(throwing: error)
                    }
                    cancellable?.cancel()
                },
                receiveValue: { value in
                    values.append(value)
                }
            )
        }
    }
}

extension Publisher where Failure == Never {

    /// Get first value (never throws)
    func firstValue() async -> Output? {
        await withCheckedContinuation { continuation in
            var cancellable: AnyCancellable?
            var didResume = false

            cancellable = first()
                .sink { value in
                    guard !didResume else { return }
                    didResume = true
                    continuation.resume(returning: value)
                    cancellable?.cancel()
                }
        }
    }
}

// MARK: - Async to Publisher

extension AnyPublisher {

    /// Create publisher from async function
    static func fromAsync<T>(
        _ operation: @escaping () async throws -> T
    ) -> AnyPublisher<T, Error> where Output == T, Failure == Error {
        Deferred {
            Future { promise in
                Task {
                    do {
                        let result = try await operation()
                        promise(.success(result))
                    } catch {
                        promise(.failure(error))
                    }
                }
            }
        }
        .eraseToAnyPublisher()
    }

    /// Create publisher from async sequence
    static func fromAsyncSequence<S: AsyncSequence>(
        _ sequence: S
    ) -> AnyPublisher<S.Element, Error> where Output == S.Element, Failure == Error {
        let subject = PassthroughSubject<S.Element, Error>()

        Task {
            do {
                for try await element in sequence {
                    subject.send(element)
                }
                subject.send(completion: .finished)
            } catch {
                subject.send(completion: .failure(error))
            }
        }

        return subject.eraseToAnyPublisher()
    }
}

// MARK: - Task-Cancellable Bridge

final class CancellableTask<Output>: Cancellable {
    private var task: Task<Output, Error>?

    init(operation: @escaping () async throws -> Output) {
        task = Task {
            try await operation()
        }
    }

    func cancel() {
        task?.cancel()
    }

    var value: Output {
        get async throws {
            guard let task = task else {
                throw CancellationError()
            }
            return try await task.value
        }
    }
}

extension Publisher where Failure == Error {

    /// Subscribe with async handler
    func sinkAsync(
        receiveValue: @escaping (Output) async -> Void
    ) -> AnyCancellable {
        sink(
            receiveCompletion: { _ in },
            receiveValue: { value in
                Task {
                    await receiveValue(value)
                }
            }
        )
    }
}
```

## Memory Management Patterns

```swift
import Combine

// MARK: - Safe Subscription Manager

final class SubscriptionManager {
    private var cancellables = Set<AnyCancellable>()
    private let lock = NSLock()

    func store(_ cancellable: AnyCancellable) {
        lock.lock()
        defer { lock.unlock() }
        cancellables.insert(cancellable)
    }

    func cancel(where predicate: (AnyCancellable) -> Bool) {
        lock.lock()
        defer { lock.unlock() }
        cancellables = cancellables.filter { !predicate($0) }
    }

    func cancelAll() {
        lock.lock()
        defer { lock.unlock() }
        cancellables.forEach { $0.cancel() }
        cancellables.removeAll()
    }

    deinit {
        cancelAll()
    }
}

// MARK: - Scoped Subscriptions

extension AnyCancellable {

    /// Store in a Set while also allowing manual cancellation
    func store(
        in set: inout Set<AnyCancellable>,
        key: String,
        replacingExisting: Bool = true
    ) {
        if replacingExisting {
            // Cancel and remove any existing subscription with same key
            // (Requires tracking keys separately or using a dictionary)
        }
        store(in: &set)
    }
}

// MARK: - Auto-Cancelling Subscriptions

@propertyWrapper
struct AutoCancellingSubscription {
    private var cancellable: AnyCancellable?

    var wrappedValue: AnyCancellable? {
        get { cancellable }
        set {
            cancellable?.cancel()
            cancellable = newValue
        }
    }

    init() {
        cancellable = nil
    }
}

// MARK: - Usage with Auto-Cancellation

final class DetailViewModel: ObservableObject {
    @Published var item: Item?
    @Published var isLoading = false

    @AutoCancellingSubscription private var loadSubscription: AnyCancellable?

    private let service: ItemServiceProtocol

    init(service: ItemServiceProtocol) {
        self.service = service
    }

    func loadItem(id: String) {
        isLoading = true

        // Previous subscription automatically cancelled
        loadSubscription = service.fetchItem(id: id)
            .receive(on: DispatchQueue.main)
            .sink(
                receiveCompletion: { [weak self] completion in
                    self?.isLoading = false
                    if case .failure(let error) = completion {
                        print("Error: \(error)")
                    }
                },
                receiveValue: { [weak self] item in
                    self?.item = item
                }
            )
    }
}
```

## Testing Combine Code

```swift
import XCTest
import Combine
@testable import YourApp

// MARK: - Test Helpers

extension XCTestCase {

    /// Wait for publisher to emit expected values
    func awaitPublisher<T: Publisher>(
        _ publisher: T,
        timeout: TimeInterval = 1.0,
        file: StaticString = #file,
        line: UInt = #line
    ) throws -> T.Output {
        var result: Result<T.Output, Error>?
        let expectation = self.expectation(description: "Awaiting publisher")

        let cancellable = publisher
            .first()
            .sink(
                receiveCompletion: { completion in
                    switch completion {
                    case .finished:
                        break
                    case .failure(let error):
                        result = .failure(error)
                    }
                    expectation.fulfill()
                },
                receiveValue: { value in
                    result = .success(value)
                }
            )

        waitForExpectations(timeout: timeout)
        cancellable.cancel()

        let unwrappedResult = try XCTUnwrap(
            result,
            "Publisher did not produce a result",
            file: file,
            line: line
        )

        return try unwrappedResult.get()
    }

    /// Collect all values from publisher
    func collectValues<T: Publisher>(
        from publisher: T,
        during duration: TimeInterval = 0.1,
        file: StaticString = #file,
        line: UInt = #line
    ) -> [T.Output] {
        var values: [T.Output] = []
        let expectation = self.expectation(description: "Collecting values")

        let cancellable = publisher
            .sink(
                receiveCompletion: { _ in },
                receiveValue: { value in
                    values.append(value)
                }
            )

        DispatchQueue.main.asyncAfter(deadline: .now() + duration) {
            expectation.fulfill()
        }

        waitForExpectations(timeout: duration + 0.5)
        cancellable.cancel()

        return values
    }
}

// MARK: - Mock Publisher

final class MockPublisher<Output, Failure: Error>: Publisher {

    private let subject = PassthroughSubject<Output, Failure>()
    private(set) var subscriberCount = 0

    func receive<S>(subscriber: S) where S: Subscriber, Failure == S.Failure, Output == S.Input {
        subscriberCount += 1
        subject.receive(subscriber: subscriber)
    }

    func send(_ value: Output) {
        subject.send(value)
    }

    func send(completion: Subscribers.Completion<Failure>) {
        subject.send(completion: completion)
    }
}

// MARK: - Scheduler Mock

final class TestScheduler: Scheduler {
    typealias SchedulerTimeType = DispatchQueue.SchedulerTimeType
    typealias SchedulerOptions = DispatchQueue.SchedulerOptions

    var now: SchedulerTimeType {
        DispatchQueue.main.now
    }

    var minimumTolerance: SchedulerTimeType.Stride {
        DispatchQueue.main.minimumTolerance
    }

    private var scheduledActions: [(action: () -> Void, date: SchedulerTimeType)] = []

    func schedule(options: SchedulerOptions?, _ action: @escaping () -> Void) {
        action()
    }

    func schedule(
        after date: SchedulerTimeType,
        tolerance: SchedulerTimeType.Stride,
        options: SchedulerOptions?,
        _ action: @escaping () -> Void
    ) {
        scheduledActions.append((action, date))
    }

    func schedule(
        after date: SchedulerTimeType,
        interval: SchedulerTimeType.Stride,
        tolerance: SchedulerTimeType.Stride,
        options: SchedulerOptions?,
        _ action: @escaping () -> Void
    ) -> any Cancellable {
        scheduledActions.append((action, date))
        return AnyCancellable {}
    }

    func advance(by interval: TimeInterval = 0) {
        let targetTime = now.advanced(by: .seconds(interval))
        let actionsToRun = scheduledActions.filter { $0.date <= targetTime }
        scheduledActions.removeAll { $0.date <= targetTime }
        actionsToRun.forEach { $0.action() }
    }

    func runAllScheduledActions() {
        let actions = scheduledActions
        scheduledActions.removeAll()
        actions.forEach { $0.action() }
    }
}

// MARK: - ViewModel Tests

final class SearchViewModelTests: XCTestCase {

    var viewModel: SearchViewModel!
    var mockService: MockSearchService!
    var cancellables: Set<AnyCancellable>!

    override func setUp() {
        super.setUp()
        mockService = MockSearchService()
        viewModel = SearchViewModel(searchService: mockService)
        cancellables = []
    }

    override func tearDown() {
        cancellables = nil
        viewModel = nil
        mockService = nil
        super.tearDown()
    }

    func testSearchDebouncing() {
        let expectation = self.expectation(description: "Search debounced")
        var searchCallCount = 0

        mockService.onSearch = { _ in
            searchCallCount += 1
        }

        // Rapid typing simulation
        viewModel.searchText = "a"
        viewModel.searchText = "ab"
        viewModel.searchText = "abc"

        DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
            expectation.fulfill()
        }

        waitForExpectations(timeout: 1.0)

        // Should only have called search once due to debounce
        XCTAssertEqual(searchCallCount, 1)
    }

    func testResultsPublished() throws {
        let expectedResults = [
            SearchResult(id: "1", title: "Result 1", description: "Desc 1")
        ]

        mockService.mockResponse = SearchResponse(
            results: expectedResults,
            currentPage: 1,
            hasMorePages: false
        )

        viewModel.searchText = "test"

        let results = collectValues(from: viewModel.$results, during: 0.5)

        XCTAssertTrue(results.contains { $0 == expectedResults })
    }
}

// MARK: - Mock Service

final class MockSearchService: SearchServiceProtocol {
    var mockResponse: SearchResponse?
    var mockError: Error?
    var onSearch: ((String) -> Void)?

    func search(query: String, page: Int) async throws -> SearchResponse {
        onSearch?(query)

        if let error = mockError {
            throw error
        }

        return mockResponse ?? SearchResponse(results: [], currentPage: 1, hasMorePages: false)
    }
}
```

## Real-World Patterns

```swift
import Combine

// MARK: - Pagination with Combine

final class PaginatedDataSource<Item: Identifiable> {

    @Published private(set) var items: [Item] = []
    @Published private(set) var isLoading = false
    @Published private(set) var error: Error?
    @Published private(set) var hasMorePages = true

    private var currentPage = 0
    private var cancellables = Set<AnyCancellable>()

    private let fetchPage: (Int) -> AnyPublisher<PageResponse<Item>, Error>

    init(fetchPage: @escaping (Int) -> AnyPublisher<PageResponse<Item>, Error>) {
        self.fetchPage = fetchPage
    }

    func loadFirstPage() {
        currentPage = 0
        items = []
        hasMorePages = true
        loadNextPage()
    }

    func loadNextPage() {
        guard !isLoading, hasMorePages else { return }

        isLoading = true
        error = nil

        fetchPage(currentPage + 1)
            .receive(on: DispatchQueue.main)
            .sink(
                receiveCompletion: { [weak self] completion in
                    self?.isLoading = false
                    if case .failure(let error) = completion {
                        self?.error = error
                    }
                },
                receiveValue: { [weak self] response in
                    guard let self = self else { return }
                    self.items.append(contentsOf: response.items)
                    self.currentPage = response.page
                    self.hasMorePages = response.hasMore
                }
            )
            .store(in: &cancellables)
    }
}

struct PageResponse<Item> {
    let items: [Item]
    let page: Int
    let hasMore: Bool
}

// MARK: - Form Validation with Combine

final class FormValidator: ObservableObject {

    @Published var email = ""
    @Published var password = ""
    @Published var confirmPassword = ""

    @Published private(set) var emailError: String?
    @Published private(set) var passwordError: String?
    @Published private(set) var confirmPasswordError: String?
    @Published private(set) var isValid = false

    private var cancellables = Set<AnyCancellable>()

    init() {
        setupValidation()
    }

    private func setupValidation() {
        // Email validation
        $email
            .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
            .map { email -> String? in
                if email.isEmpty { return nil }
                let emailRegex = "[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,64}"
                let isValid = NSPredicate(format: "SELF MATCHES %@", emailRegex)
                    .evaluate(with: email)
                return isValid ? nil : "Invalid email format"
            }
            .assign(to: &$emailError)

        // Password validation
        $password
            .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
            .map { password -> String? in
                if password.isEmpty { return nil }
                if password.count < 8 { return "Password must be at least 8 characters" }
                if !password.contains(where: { $0.isNumber }) {
                    return "Password must contain a number"
                }
                return nil
            }
            .assign(to: &$passwordError)

        // Confirm password validation
        Publishers.CombineLatest($password, $confirmPassword)
            .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
            .map { password, confirm -> String? in
                if confirm.isEmpty { return nil }
                return password == confirm ? nil : "Passwords don't match"
            }
            .assign(to: &$confirmPasswordError)

        // Overall form validity
        Publishers.CombineLatest4(
            $email.map { !$0.isEmpty },
            $emailError.map { $0 == nil },
            $passwordError.map { $0 == nil },
            $confirmPasswordError.map { $0 == nil }
        )
        .map { hasEmail, emailValid, passwordValid, confirmValid in
            hasEmail && emailValid && passwordValid && confirmValid
        }
        .assign(to: &$isValid)
    }
}

// MARK: - Network State Publisher

enum NetworkState<T> {
    case idle
    case loading
    case loaded(T)
    case failed(Error)

    var isLoading: Bool {
        if case .loading = self { return true }
        return false
    }

    var value: T? {
        if case .loaded(let value) = self { return value }
        return nil
    }

    var error: Error? {
        if case .failed(let error) = self { return error }
        return nil
    }
}

extension Publisher {
    func mapToNetworkState() -> AnyPublisher<NetworkState<Output>, Never> {
        map { NetworkState.loaded($0) }
            .catch { Just(NetworkState.failed($0)) }
            .prepend(.loading)
            .eraseToAnyPublisher()
    }
}
```
