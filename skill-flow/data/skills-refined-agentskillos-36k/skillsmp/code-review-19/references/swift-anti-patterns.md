# Swift Anti-Patterns

Common anti-patterns to identify during Swift code review.

## Critical Anti-Patterns

### 1. Force Unwrapping Without Safety

```swift
// ANTI-PATTERN
let user = users.first!  // Will crash if empty
let value = dictionary["key"]!  // Will crash if key missing

// CORRECT
guard let user = users.first else {
    return  // or handle empty case
}

if let value = dictionary["key"] {
    // use value
}
```

### 2. Retain Cycles in Closures

```swift
// ANTI-PATTERN
class ViewController {
    var onComplete: (() -> Void)?

    func setup() {
        onComplete = {
            self.dismiss(animated: true)  // Strong capture
        }
    }
}

// CORRECT
func setup() {
    onComplete = { [weak self] in
        self?.dismiss(animated: true)
    }
}
```

### 3. UI Updates from Background Thread

```swift
// ANTI-PATTERN
func loadData() async {
    let data = await fetchFromNetwork()
    self.items = data  // May not be on main thread!
}

// CORRECT
@MainActor
func loadData() async {
    let data = await fetchFromNetwork()
    self.items = data  // Guaranteed on main thread
}
```

### 4. Silent Error Swallowing

```swift
// ANTI-PATTERN
do {
    try performOperation()
} catch {
    // Empty catch - error is lost
}

// CORRECT
do {
    try performOperation()
} catch {
    logger.error("Operation failed: \(error)")
    throw error  // or handle appropriately
}
```

## High Priority Anti-Patterns

### 5. Massive View Controllers/ViewModels

```swift
// ANTI-PATTERN
class MassiveViewModel {
    // 500+ lines of code
    // Handles multiple unrelated concerns
    // Many different responsibilities
}

// CORRECT
// Split into focused components:
class UserListViewModel { /* user list logic */ }
class UserDetailViewModel { /* detail logic */ }
class UserFormViewModel { /* form logic */ }
```

### 6. God Objects

```swift
// ANTI-PATTERN
class AppManager {
    static let shared = AppManager()

    func login() { }
    func logout() { }
    func fetchUsers() { }
    func saveSettings() { }
    func playSound() { }
    // Does everything...
}

// CORRECT
class AuthService { /* auth only */ }
class UserRepository { /* users only */ }
class SettingsService { /* settings only */ }
class AudioPlayer { /* audio only */ }
```

### 7. Stringly Typed Code

```swift
// ANTI-PATTERN
func handleAction(_ action: String) {
    if action == "login" {
        // ...
    } else if action == "logout" {
        // ...
    }
}

NotificationCenter.default.post(name: NSNotification.Name("UserLoggedIn"), object: nil)

// CORRECT
enum Action {
    case login
    case logout
}

func handleAction(_ action: Action) {
    switch action {
    case .login: // ...
    case .logout: // ...
    }
}

extension Notification.Name {
    static let userLoggedIn = Notification.Name("UserLoggedIn")
}
```

### 8. Pyramid of Doom

```swift
// ANTI-PATTERN
if let user = getUser() {
    if let profile = user.profile {
        if let address = profile.address {
            if let city = address.city {
                print(city)
            }
        }
    }
}

// CORRECT
guard let user = getUser(),
      let profile = user.profile,
      let address = profile.address,
      let city = address.city else {
    return
}
print(city)
```

## Medium Priority Anti-Patterns

### 9. Callback Hell

```swift
// ANTI-PATTERN
func loadDashboard(completion: @escaping (Dashboard?) -> Void) {
    fetchUser { user in
        guard let user else { completion(nil); return }
        self.fetchPosts(for: user) { posts in
            guard let posts else { completion(nil); return }
            self.fetchComments(for: posts) { comments in
                completion(Dashboard(user: user, posts: posts, comments: comments))
            }
        }
    }
}

// CORRECT
func loadDashboard() async throws -> Dashboard {
    let user = try await fetchUser()
    let posts = try await fetchPosts(for: user)
    let comments = try await fetchComments(for: posts)
    return Dashboard(user: user, posts: posts, comments: comments)
}
```

### 10. Primitive Obsession

```swift
// ANTI-PATTERN
func createUser(name: String, email: String, phone: String, age: Int) {
    // Many primitive parameters
}

// CORRECT
struct UserInput {
    let name: String
    let email: Email  // Validated type
    let phone: PhoneNumber  // Validated type
    let age: Int
}

func createUser(_ input: UserInput) {
    // Single parameter with validated types
}
```

### 11. Boolean Blindness

```swift
// ANTI-PATTERN
func process(data: Data, shouldValidate: Bool, shouldCache: Bool, isAsync: Bool) {
    // Multiple boolean parameters - easy to mix up
}

process(data: data, shouldValidate: true, shouldCache: false, isAsync: true)

// CORRECT
struct ProcessingOptions: OptionSet {
    let rawValue: Int
    static let validate = ProcessingOptions(rawValue: 1 << 0)
    static let cache = ProcessingOptions(rawValue: 1 << 1)
    static let async = ProcessingOptions(rawValue: 1 << 2)
}

func process(data: Data, options: ProcessingOptions) {
    // Clear what each option means
}

process(data: data, options: [.validate, .async])
```

### 12. Inappropriate Intimacy

```swift
// ANTI-PATTERN
class UserViewModel {
    func saveUser() {
        // Directly accessing internal details of another class
        Database.shared.connection.tables["users"].insert(userData)
    }
}

// CORRECT
class UserViewModel {
    private let repository: UserRepository

    func saveUser() {
        repository.save(user)  // Uses abstraction
    }
}
```

## Low Priority Anti-Patterns

### 13. Magic Numbers/Strings

```swift
// ANTI-PATTERN
if status == 200 {
    // ...
}

view.frame = CGRect(x: 16, y: 32, width: 100, height: 44)

// CORRECT
enum HTTPStatus {
    static let ok = 200
}

enum Layout {
    static let horizontalPadding: CGFloat = 16
    static let verticalPadding: CGFloat = 32
    static let buttonWidth: CGFloat = 100
    static let buttonHeight: CGFloat = 44
}
```

### 14. Comments Explaining Bad Code

```swift
// ANTI-PATTERN
// Increment i by 1
i += 1

// Check if user is valid and has permission
if u != nil && u!.p == true && u!.a == 1 {
    // ...
}

// CORRECT
// No comment needed for clear code
counter += 1

if user.isValidWithPermission {
    // ...
}
```

### 15. Feature Envy

```swift
// ANTI-PATTERN
class OrderService {
    func calculateTotal(order: Order) -> Double {
        var total = 0.0
        for item in order.items {
            total += item.price * Double(item.quantity)
        }
        total -= order.discount
        total *= 1 + order.taxRate
        return total
    }
}

// CORRECT
class Order {
    func calculateTotal() -> Double {
        let subtotal = items.reduce(0) { $0 + $1.total }
        return (subtotal - discount) * (1 + taxRate)
    }
}
```

## Detection Tips

When reviewing code, look for:

1. **`!` operator** - Check if force unwrap is safe
2. **`self` in closures** - Check for weak/unowned
3. **DispatchQueue.main** - Consider @MainActor instead
4. **Empty catch blocks** - Errors should be handled
5. **Long functions** - Consider decomposition
6. **Many parameters** - Consider parameter objects
7. **Nested callbacks** - Consider async/await
8. **Hard-coded values** - Extract to constants
