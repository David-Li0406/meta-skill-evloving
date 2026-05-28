---
name: swift-coding-standards
description: Swift and SwiftUI coding standards and best practices. NOT for TypeScript/JavaScript.
---

# Swift Coding Standards & Best Practices

Swift-specific coding standards for iOS, macOS, and server-side Swift development.

## Code Quality Principles

### 1. Readability First
- Code is read more than written
- Clear variable and function names
- Self-documenting code preferred over comments
- Consistent formatting

### 2. KISS (Keep It Simple, Stupid)
- Simplest solution that works
- Avoid over-engineering
- No premature optimization
- Easy to understand > clever code

### 3. DRY (Don't Repeat Yourself)
- Extract common logic into functions
- Create reusable components
- Use protocol extensions for shared behavior
- Avoid copy-paste programming

### 4. YAGNI (You Aren't Gonna Need It)
- Don't build features before they're needed
- Avoid speculative generality
- Add complexity only when required
- Start simple, refactor when needed

## Swift Naming Conventions

### Types (PascalCase)

```swift
// GOOD: PascalCase for types
struct UserProfile { }
class NetworkManager { }
enum PaymentStatus { }
protocol DataProvider { }

// BAD: Other casing
struct userProfile { }  // camelCase
class network_manager { }  // snake_case
```

### Properties & Methods (camelCase)

```swift
// GOOD: camelCase for properties and methods
var userName: String
let isAuthenticated: Bool
func fetchMarketData() { }

// BAD: Other casing
var UserName: String  // PascalCase
var user_name: String  // snake_case
```

### Constants

```swift
// GOOD: Static constants in types
struct Constants {
    static let maxRetries = 3
    static let apiBaseURL = "https://api.example.com"
}

enum Dimension {
    static let defaultPadding: CGFloat = 16
    static let cornerRadius: CGFloat = 8
}

// BAD: Global constants
let kMaxRetries = 3  // Old Objective-C style
```

### Boolean Naming

```swift
// GOOD: is/has/can/should prefixes
var isLoading: Bool
var hasPermission: Bool
var canSubmit: Bool
var shouldRefresh: Bool

// BAD: Unclear boolean names
var loading: Bool
var permission: Bool
var submit: Bool
```

## Optionals Best Practices

### Guard Let (Early Exit)

```swift
// GOOD: Guard for early exit
func processUser(_ user: User?) {
    guard let user = user else {
        return
    }

    guard let email = user.email, !email.isEmpty else {
        print("Invalid email")
        return
    }

    // Continue with unwrapped values
    sendEmail(to: email)
}

// BAD: Nested if-let pyramid
func processUser(_ user: User?) {
    if let user = user {
        if let email = user.email {
            if !email.isEmpty {
                sendEmail(to: email)
            }
        }
    }
}
```

### Optional Chaining

```swift
// GOOD: Optional chaining
let count = user?.posts?.count ?? 0
let upperName = user?.name?.uppercased()

// GOOD: Map for transformations
let displayName = user.map { "\($0.firstName) \($0.lastName)" }
```

### Nil Coalescing

```swift
// GOOD: Default values
let name = user?.name ?? "Anonymous"
let age = user?.age ?? 0

// GOOD: Lazy default
let config = cachedConfig ?? loadDefaultConfig()
```

## Error Handling

### Result Type

```swift
// GOOD: Result type for operations that can fail
enum NetworkError: Error {
    case invalidURL
    case noData
    case decodingFailed
    case serverError(Int)
}

func fetchUser(id: String) async -> Result<User, NetworkError> {
    guard let url = URL(string: "https://api.example.com/users/\(id)") else {
        return .failure(.invalidURL)
    }

    do {
        let (data, response) = try await URLSession.shared.data(from: url)

        guard let httpResponse = response as? HTTPURLResponse else {
            return .failure(.noData)
        }

        guard httpResponse.statusCode == 200 else {
            return .failure(.serverError(httpResponse.statusCode))
        }

        let user = try JSONDecoder().decode(User.self, from: data)
        return .success(user)
    } catch {
        return .failure(.decodingFailed)
    }
}
```

### Do-Try-Catch

```swift
// GOOD: Proper error handling
func loadConfiguration() throws -> Configuration {
    let url = Bundle.main.url(forResource: "config", withExtension: "json")!
    let data = try Data(contentsOf: url)
    return try JSONDecoder().decode(Configuration.self, from: data)
}

// Usage
do {
    let config = try loadConfiguration()
    print(config)
} catch {
    print("Failed to load config: \(error)")
}
```

## Concurrency (async/await)

### Async Functions

```swift
// GOOD: Async/await pattern
func fetchMarkets() async throws -> [Market] {
    let url = URL(string: "https://api.example.com/markets")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode([Market].self, from: data)
}

// GOOD: Parallel execution
func fetchDashboardData() async throws -> DashboardData {
    async let markets = fetchMarkets()
    async let user = fetchCurrentUser()
    async let stats = fetchStats()

    return try await DashboardData(
        markets: markets,
        user: user,
        stats: stats
    )
}
```

### MainActor for UI Updates

```swift
// GOOD: MainActor for UI updates
@MainActor
class MarketViewModel: ObservableObject {
    @Published var markets: [Market] = []
    @Published var isLoading = false
    @Published var error: Error?

    func loadMarkets() async {
        isLoading = true
        defer { isLoading = false }

        do {
            markets = try await MarketService.shared.fetchMarkets()
        } catch {
            self.error = error
        }
    }
}
```

### Actors for Thread Safety

```swift
// GOOD: Actor for thread-safe state
actor CacheManager {
    private var cache: [String: Data] = [:]

    func get(_ key: String) -> Data? {
        cache[key]
    }

    func set(_ key: String, data: Data) {
        cache[key] = data
    }

    func clear() {
        cache.removeAll()
    }
}
```

## SwiftUI Best Practices

### View Structure

```swift
// GOOD: Clean view structure
struct MarketCardView: View {
    let market: Market
    let onTap: () -> Void

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            headerView
            descriptionView
            statsView
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(radius: 2)
        .onTapGesture(perform: onTap)
    }

    // GOOD: Extract subviews as computed properties
    private var headerView: some View {
        HStack {
            Text(market.name)
                .font(.headline)
            Spacer()
            StatusBadge(status: market.status)
        }
    }

    private var descriptionView: some View {
        Text(market.description)
            .font(.subheadline)
            .foregroundColor(.secondary)
            .lineLimit(2)
    }

    private var statsView: some View {
        HStack {
            Label("\(market.volume)", systemImage: "chart.bar")
            Spacer()
            Label(market.endDate.formatted(), systemImage: "calendar")
        }
        .font(.caption)
        .foregroundColor(.secondary)
    }
}
```

### State Management

```swift
// GOOD: Appropriate property wrappers
struct ContentView: View {
    // Local state
    @State private var searchText = ""
    @State private var isShowingSheet = false

    // Observable object
    @StateObject private var viewModel = MarketViewModel()

    // Environment
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject private var appState: AppState

    var body: some View {
        // ...
    }
}

// GOOD: Binding for child views
struct SearchBar: View {
    @Binding var text: String

    var body: some View {
        TextField("Search...", text: $text)
    }
}
```

### Preview Providers

```swift
// GOOD: Multiple preview configurations
#Preview("Default") {
    MarketCardView(market: .preview) { }
}

#Preview("Loading") {
    MarketCardView(market: .preview) { }
        .redacted(reason: .placeholder)
}

#Preview("Dark Mode") {
    MarketCardView(market: .preview) { }
        .preferredColorScheme(.dark)
}
```

## Protocol-Oriented Design

### Protocol with Default Implementation

```swift
// GOOD: Protocol with extension
protocol Identifiable {
    var id: String { get }
}

protocol Timestamped {
    var createdAt: Date { get }
    var updatedAt: Date { get }
}

extension Timestamped {
    var isRecent: Bool {
        updatedAt > Date().addingTimeInterval(-3600) // Last hour
    }
}

// GOOD: Protocol composition
typealias Entity = Identifiable & Timestamped & Codable

struct Market: Entity {
    let id: String
    let name: String
    let createdAt: Date
    let updatedAt: Date
}
```

### Dependency Injection with Protocols

```swift
// GOOD: Protocol for testability
protocol MarketServiceProtocol {
    func fetchMarkets() async throws -> [Market]
    func createMarket(_ market: Market) async throws -> Market
}

class MarketService: MarketServiceProtocol {
    func fetchMarkets() async throws -> [Market] {
        // Real implementation
    }

    func createMarket(_ market: Market) async throws -> Market {
        // Real implementation
    }
}

// For testing
class MockMarketService: MarketServiceProtocol {
    var marketsToReturn: [Market] = []
    var shouldThrowError = false

    func fetchMarkets() async throws -> [Market] {
        if shouldThrowError { throw TestError.mock }
        return marketsToReturn
    }

    func createMarket(_ market: Market) async throws -> Market {
        if shouldThrowError { throw TestError.mock }
        return market
    }
}
```

## File Organization

### Project Structure

```
MyApp/
├── App/
│   ├── MyAppApp.swift
│   └── AppDelegate.swift
├── Features/
│   ├── Markets/
│   │   ├── Views/
│   │   │   ├── MarketListView.swift
│   │   │   └── MarketDetailView.swift
│   │   ├── ViewModels/
│   │   │   └── MarketViewModel.swift
│   │   └── Models/
│   │       └── Market.swift
│   └── Auth/
│       ├── Views/
│       ├── ViewModels/
│       └── Models/
├── Core/
│   ├── Network/
│   │   ├── APIClient.swift
│   │   └── Endpoints.swift
│   ├── Storage/
│   │   └── UserDefaults+Extensions.swift
│   └── Utilities/
│       └── DateFormatter+Extensions.swift
├── Resources/
│   ├── Assets.xcassets
│   └── Localizable.strings
└── Tests/
    ├── UnitTests/
    └── UITests/
```

### File Naming

```
Views/MarketListView.swift          # Views end with View
ViewModels/MarketViewModel.swift    # ViewModels end with ViewModel
Models/Market.swift                 # Models are singular nouns
Services/MarketService.swift        # Services end with Service
Extensions/String+Validation.swift  # Extensions use + notation
Protocols/DataProviding.swift       # Protocols use -ing or -able
```

## Extensions

### Organizing Extensions

```swift
// GOOD: Extensions in separate files
// String+Validation.swift
extension String {
    var isValidEmail: Bool {
        let regex = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/
        return self.wholeMatch(of: regex) != nil
    }

    var isValidPassword: Bool {
        count >= 8 && contains(where: \.isUppercase) && contains(where: \.isNumber)
    }
}

// Date+Formatting.swift
extension Date {
    var relativeString: String {
        let formatter = RelativeDateTimeFormatter()
        return formatter.localizedString(for: self, relativeTo: Date())
    }
}
```

## Code Smells to Avoid

### 1. Force Unwrapping

```swift
// BAD: Force unwrap
let name = user!.name

// GOOD: Safe unwrap
guard let name = user?.name else { return }
```

### 2. Massive View Controllers/Views

```swift
// BAD: Everything in one view
struct MassiveView: View {
    // 500 lines of code
}

// GOOD: Composed smaller views
struct ComposedView: View {
    var body: some View {
        VStack {
            HeaderView()
            ContentView()
            FooterView()
        }
    }
}
```

### 3. Stringly Typed Code

```swift
// BAD: Magic strings
NotificationCenter.default.post(name: NSNotification.Name("UserLoggedIn"), object: nil)

// GOOD: Type-safe notifications
extension Notification.Name {
    static let userLoggedIn = Notification.Name("userLoggedIn")
}
NotificationCenter.default.post(name: .userLoggedIn, object: nil)
```

### 4. Ignoring Errors

```swift
// BAD: Ignoring errors
try? doSomethingRisky()

// GOOD: Handle or propagate
do {
    try doSomethingRisky()
} catch {
    logger.error("Failed: \(error)")
    // Handle appropriately
}
```

## Comments & Documentation

### Documentation Comments

```swift
/// Fetches markets from the API with optional filtering.
///
/// - Parameters:
///   - status: Filter by market status. Pass `nil` for all statuses.
///   - limit: Maximum number of results. Default is 20.
/// - Returns: An array of markets matching the criteria.
/// - Throws: `NetworkError` if the request fails.
///
/// ## Example
/// ```swift
/// let markets = try await fetchMarkets(status: .active, limit: 10)
/// ```
func fetchMarkets(status: MarketStatus?, limit: Int = 20) async throws -> [Market] {
    // Implementation
}
```

### MARK Comments

```swift
// MARK: - Properties

private let service: MarketService
@Published var markets: [Market] = []

// MARK: - Lifecycle

init(service: MarketService) {
    self.service = service
}

// MARK: - Public Methods

func loadMarkets() async {
    // ...
}

// MARK: - Private Methods

private func processMarkets(_ markets: [Market]) {
    // ...
}
```

---

**Remember**: Swift encourages safe, expressive, and performant code. Leverage the type system, optionals, and protocols to write code that's both elegant and robust.
