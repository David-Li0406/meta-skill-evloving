---
name: swift-ios-expert
description: Use this skill when you need expert guidance in Swift and SwiftUI development for iOS and macOS applications, ensuring best practices and modern features are applied.
---

# Skill body

## Core Concepts

### Modern Swift Features (5.9+)
- Async/await concurrency
- Actors for thread safety
- Property wrappers
- Result builders
- Protocols and generics
- Value types vs reference types
- Automatic Reference Counting (ARC)
- Macros (Swift 5.9+)

### SwiftUI
- Declarative UI framework
- State management
- View composition
- Layout system
- Animations
- Navigation
- Use @State, @Binding, @ObservedObject, and @StateObject for state management
- Leverage @Environment for dependency injection
- Use ViewModifiers for reusable view styling

### Combine
- Reactive programming
- Publishers and subscribers
- Operators
- Error handling

## Architecture
- Follow MVVM architecture pattern
- Use struct-based code where appropriate
- SwiftUI-first approach with UIKit as fallback
- Implement clean separation of concerns

## Best Practices
- Produce clear, readable SwiftUI code using the latest versions
- Focus on readability over performance
- Leave no TODOs or placeholders
- Optimize view rendering and use lazy loading for large data sets
- Implement proper caching strategies
- Follow Apple Human Interface Guidelines and accessibility standards

## Testing
- Use XCTest for unit testing and XCUITest for UI testing
- Write comprehensive test coverage
- Test on multiple device sizes

## Security
- Use encryption for sensitive data
- Store credentials in Keychain
- Implement biometric authentication where appropriate
- Follow Apple security guidelines

## Swift Syntax Examples

### Basics and Optionals
```swift
// Variables and constants
var mutableValue = 42
let constantValue = 100

// Optionals
var optionalName: String? = "Alice"

// Optional binding
if let name = optionalName {
    print("Hello, \(name)")
}

// Optional chaining
let length = optionalName?.count

// Nil coalescing
let displayName = optionalName ?? "Unknown"

// Guard statement
func greet(person: String?) {
    guard let name = person else {
        print("No name provided")
        return
    }
    print("Hello, \(name)")
}
```

### Functions and Closures
```swift
// Function with labeled parameters
func greet(person: String, from hometown: String) -> String {
    return "Hello \(person) from \(hometown)!"
}

// Closures
let numbers = [1, 2, 3, 4, 5]
let doubled = numbers.map { $0 * 2 }
let evens = numbers.filter { $0 % 2 == 0 }
let sum = numbers.reduce(0, +)

// Trailing closure
numbers.forEach { number in
    print(number)
}

// Capture values
func makeIncrementer(step: Int) -> () -> Int {
    var total = 0
    return {
        total += step
        return total
    }
}
```

### Structs and Classes
```swift
// Struct (value type, preferred)
struct User {
    let id: UUID
    var name: String
    var email: String

    // Computed property
    var displayName: String {
        name.isEmpty ? "Anonymous" : name
    }

    // Method
    mutating func updateEmail(_ newEmail: String) {
        email = newEmail
    }
}

// Class (reference type)
class ViewController {
    var title: String?
    weak var delegate: ViewControllerDelegate?
}
```