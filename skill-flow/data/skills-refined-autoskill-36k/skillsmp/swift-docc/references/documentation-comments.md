# Documentation Comments Reference

Complete reference for Swift documentation comments used with DocC.

## Comment Syntax

### Triple-Slash Comments (`///`)

The primary syntax for documentation comments:

```swift
/// A brief description of the symbol.
///
/// Additional details in a separate paragraph.
/// This creates a "Discussion" section in DocC.
func myFunction() { }
```

### Block Comments (`/** */`)

Alternative syntax for longer documentation:

```swift
/**
 A brief description of the symbol.

 Additional details in a separate paragraph.
 Useful for very long documentation.
 */
func myFunction() { }
```

## Parameter Documentation

### Single Parameter

```swift
/// - Parameter name: Description of the parameter.
func greet(name: String) { }
```

### Multiple Parameters

```swift
/// - Parameters:
///   - x: The x-coordinate.
///   - y: The y-coordinate.
///   - z: The z-coordinate (optional).
func setPosition(x: Double, y: Double, z: Double = 0) { }
```

## Return Value

```swift
/// - Returns: A greeting message for the given name.
func greet(name: String) -> String { }
```

## Throws Documentation

```swift
/// - Throws: `NetworkError.timeout` if the request takes too long.
///           `NetworkError.noConnection` if offline.
func fetchData() async throws { }
```

## Callout Directives

### Note
```swift
/// - Note: This method is thread-safe.
```

### Important
```swift
/// - Important: Call on main thread only.
```

### Warning
```swift
/// - Warning: May cause data loss if interrupted.
```

### Tip
```swift
/// - Tip: Use caching for better performance.
```

### Precondition
```swift
/// - Precondition: Array must not be empty.
```

### Postcondition
```swift
/// - Postcondition: The file will be closed.
```

### Requires
```swift
/// - Requires: iOS 17.0 or later.
```

### Invariant
```swift
/// - Invariant: Count is always non-negative.
```

### Complexity
```swift
/// - Complexity: O(n) where n is the array length.
```

### SeeAlso
```swift
/// - SeeAlso: ``RelatedType``, ``anotherMethod()``
```

### Since / Version
```swift
/// - Since: 2.0
/// - Version: 3.1.0
```

### Author
```swift
/// - Author: Development Team
```

## Symbol Links

### Link to Type
```swift
/// See ``MyClass`` for more details.
```

### Link to Method
```swift
/// Use ``configure(with:)`` to set up.
```

### Link to Property
```swift
/// Check ``isEnabled`` before calling.
```

### Link with Custom Text
```swift
/// See <doc:GettingStarted> for setup instructions.
```

## Code Examples

### Inline Code
```swift
/// Set `isEnabled` to `true` to activate.
```

### Code Block
```swift
/// ## Example
///
/// ```swift
/// let manager = DataManager()
/// try await manager.save(data)
/// ```
```

## Topics Section

Organize related symbols:

```swift
/// ## Topics
///
/// ### Creating Instances
/// - ``init()``
/// - ``init(name:)``
///
/// ### Configuration
/// - ``configure(with:)``
/// - ``reset()``
///
/// ### Properties
/// - ``name``
/// - ``isEnabled``
```

## Availability Annotations

Document platform requirements:

```swift
/// - Available: iOS 17.0+, macOS 14.0+
///
/// @available(iOS 17.0, macOS 14.0, *)
func newFeature() { }
```

## Deprecation

```swift
/// - Deprecated: Use ``newMethod()`` instead.
@available(*, deprecated, renamed: "newMethod")
func oldMethod() { }
```

## Complete Example

```swift
/// A service for managing user authentication.
///
/// Use `AuthService` to handle sign-in, sign-out, and session management
/// throughout the application lifecycle.
///
/// ## Overview
///
/// The auth service provides a centralized way to manage user credentials
/// and authentication state. It automatically persists sessions to Keychain.
///
/// ## Example
///
/// ```swift
/// let auth = AuthService.shared
///
/// do {
///     let user = try await auth.signIn(email: "user@example.com", password: "...")
///     print("Welcome, \(user.name)!")
/// } catch {
///     print("Sign in failed: \(error)")
/// }
/// ```
///
/// ## Topics
///
/// ### Authentication
/// - ``signIn(email:password:)``
/// - ``signOut()``
/// - ``currentUser``
///
/// ### Session Management
/// - ``refreshSession()``
/// - ``isSessionValid``
///
/// - Note: All methods are thread-safe and can be called from any queue.
/// - Important: Ensure proper error handling for network failures.
/// - SeeAlso: ``User``, ``AuthError``
@Observable
final class AuthService {
    /// The shared singleton instance.
    static let shared = AuthService()

    /// The currently authenticated user, if any.
    ///
    /// This property is `nil` when no user is signed in.
    private(set) var currentUser: User?

    /// Signs in a user with email and password.
    ///
    /// - Parameters:
    ///   - email: The user's email address.
    ///   - password: The user's password.
    ///
    /// - Returns: The authenticated ``User`` object.
    ///
    /// - Throws: ``AuthError/invalidCredentials`` if authentication fails.
    ///           ``AuthError/networkError`` if connection fails.
    ///
    /// - Precondition: Email must be a valid email format.
    @MainActor
    func signIn(email: String, password: String) async throws -> User {
        // Implementation
    }
}
```
