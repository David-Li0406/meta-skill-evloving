---
name: ios-development
description: |
  This skill should be used when the user asks to "build iOS app",
  "create SwiftUI view", "implement MVVM", "write XCTest",
  "set up SwiftData", "use Alamofire", "configure Moya",
  "add accessibility", "set up CI/CD", "fix iOS bug",
  "iOS アプリを作成", "SwiftUI で実装", "MVVM で設計",
  "テストを書く", "アクセシビリティ対応", "fastlane を設定".
  Provides iOS 17+ development guidance with SwiftUI, MVVM,
  Alamofire/Moya networking, accessibility, and CI/CD.
---

# iOS Development

Comprehensive iOS app development skill for iOS 17+ with SwiftUI, MVVM architecture, and modern Swift practices.

## Overview

**Target Platform**: iOS 17+ / Swift 5.9+

**Core Technologies**:
- UI Framework: SwiftUI (primary), UIKit (when needed)
- Architecture: MVVM with Repository pattern
- Data: SwiftData (recommended), Core Data
- Networking: Alamofire / Moya
- Testing: XCTest

## Quick Start

### New Project Setup

To create a new iOS project:

1. Open Xcode and select "Create New Project"
2. Choose "App" template with SwiftUI interface
3. Set minimum deployment target to iOS 17.0
4. Enable Swift strict concurrency checking in Build Settings

### Existing Project Analysis

To analyze an existing project structure:

```bash
bash scripts/project-analyzer.sh /path/to/project
```

## SwiftUI Essentials

### State Management (iOS 17+)

Use `@Observable` macro for state management:

```swift
@Observable
class ViewModel {
    var items: [Item] = []
    var isLoading = false
}

struct ContentView: View {
    @State private var viewModel = ViewModel()

    var body: some View {
        List(viewModel.items) { item in
            Text(item.name)
        }
    }
}
```

### Navigation

Use `NavigationStack` with type-safe navigation:

```swift
@Observable
class Router {
    var path = NavigationPath()

    func navigate(to destination: Destination) {
        path.append(destination)
    }
}

struct ContentView: View {
    @State private var router = Router()

    var body: some View {
        NavigationStack(path: $router.path) {
            // content
        }
        .environment(router)
    }
}
```

For detailed SwiftUI patterns, see [references/swiftui.md](references/swiftui.md).

## MVVM Architecture

### Layer Structure

```
Presentation Layer
├── View (SwiftUI Views)
└── ViewModel (@Observable classes)

Domain Layer
├── Model (Data structures)
└── UseCase (Business logic)

Data Layer
├── Repository (Data access abstraction)
└── DataSource (API, Database)
```

### ViewModel Design

```swift
@Observable
class UserListViewModel {
    private(set) var users: [User] = []
    private(set) var isLoading = false
    private(set) var error: Error?

    private let repository: UserRepositoryProtocol

    init(repository: UserRepositoryProtocol) {
        self.repository = repository
    }

    @MainActor
    func loadUsers() async {
        isLoading = true
        defer { isLoading = false }

        do {
            users = try await repository.fetchUsers()
        } catch {
            self.error = error
        }
    }
}
```

For detailed MVVM patterns, see [references/mvvm.md](references/mvvm.md).

## Data Persistence

### SwiftData (Recommended for iOS 17+)

```swift
@Model
class Item {
    var name: String
    var createdAt: Date

    init(name: String) {
        self.name = name
        self.createdAt = .now
    }
}

// In App
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: Item.self)
    }
}
```

For detailed data layer patterns, see [references/data-layer.md](references/data-layer.md).

## Networking

### Moya Setup

```swift
enum UserAPI {
    case getUsers
    case getUser(id: Int)
    case createUser(name: String, email: String)
}

extension UserAPI: TargetType {
    var baseURL: URL { URL(string: "https://api.example.com")! }

    var path: String {
        switch self {
        case .getUsers: return "/users"
        case .getUser(let id): return "/users/\(id)"
        case .createUser: return "/users"
        }
    }

    var method: Moya.Method {
        switch self {
        case .getUsers, .getUser: return .get
        case .createUser: return .post
        }
    }
    // ... other requirements
}
```

For detailed networking patterns, see [references/networking.md](references/networking.md).

## Testing Basics

### ViewModel Testing

```swift
@MainActor
final class UserListViewModelTests: XCTestCase {
    func test_loadUsers_success() async {
        // Arrange
        let mockRepository = MockUserRepository()
        mockRepository.usersToReturn = [User(id: 1, name: "Test")]
        let viewModel = UserListViewModel(repository: mockRepository)

        // Act
        await viewModel.loadUsers()

        // Assert
        XCTAssertEqual(viewModel.users.count, 1)
        XCTAssertFalse(viewModel.isLoading)
    }
}
```

For detailed testing patterns, see [references/testing.md](references/testing.md).

## Accessibility

### Essential Practices

```swift
struct ItemRow: View {
    let item: Item

    var body: some View {
        HStack {
            Image(systemName: item.icon)
                .accessibilityHidden(true)

            Text(item.name)
        }
        .accessibilityElement(children: .combine)
        .accessibilityLabel(item.name)
        .accessibilityHint("Double tap to view details")
    }
}
```

Key accessibility requirements:
- Add accessibility labels to all interactive elements
- Support Dynamic Type with `.dynamicTypeSize()` modifier
- Test with VoiceOver enabled
- Ensure sufficient color contrast

For detailed accessibility guidelines, see [references/accessibility.md](references/accessibility.md).

## CI/CD

### Xcode Cloud

To set up Xcode Cloud:

1. Navigate to Product > Xcode Cloud > Create Workflow
2. Configure build triggers (push, PR, tag)
3. Add test action for unit tests
4. Configure archive and distribution

### fastlane

```ruby
# Fastfile
default_platform(:ios)

platform :ios do
  lane :test do
    run_tests(scheme: "MyApp")
  end

  lane :beta do
    build_app(scheme: "MyApp")
    upload_to_testflight
  end
end
```

For detailed CI/CD setup, see [references/cicd.md](references/cicd.md).

## Code Quality Checklist

Before submitting code, verify:

- [ ] All public APIs have documentation comments
- [ ] ViewModels use `@MainActor` for UI updates
- [ ] Network calls handle errors appropriately
- [ ] Accessibility labels are added to interactive elements
- [ ] Unit tests cover critical business logic
- [ ] No force unwrapping (`!`) without safety checks
- [ ] Memory management: no retain cycles in closures

## Additional Resources

### Reference Files

- **[references/swiftui.md](references/swiftui.md)** - SwiftUI patterns and iOS 17+ features
- **[references/mvvm.md](references/mvvm.md)** - MVVM architecture details
- **[references/data-layer.md](references/data-layer.md)** - SwiftData and Core Data
- **[references/networking.md](references/networking.md)** - Alamofire / Moya patterns
- **[references/testing.md](references/testing.md)** - XCTest and mocking
- **[references/accessibility.md](references/accessibility.md)** - Accessibility implementation
- **[references/cicd.md](references/cicd.md)** - CI/CD configuration

### Example Files

- **[examples/swiftui-components.swift](examples/swiftui-components.swift)** - SwiftUI component examples
- **[examples/mvvm-pattern.swift](examples/mvvm-pattern.swift)** - Complete MVVM implementation
- **[examples/moya-networking.swift](examples/moya-networking.swift)** - Moya networking setup
- **[examples/unit-test-example.swift](examples/unit-test-example.swift)** - Unit test examples

### Utility Scripts

- **[scripts/project-analyzer.sh](scripts/project-analyzer.sh)** - Analyze iOS project structure
