---
name: swiftui-components
description: SwiftUI component expert for building reusable views, custom modifiers, and view compositions. Use when creating new SwiftUI views, refactoring UI code, or building watchOS-specific interfaces.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# SwiftUI Components Expert

## Instructions

When building SwiftUI components:

1. Analyze the required component functionality
2. Check existing components for reuse opportunities
3. Follow watchOS design guidelines
4. Ensure accessibility support
5. Add appropriate previews

## watchOS SwiftUI Patterns

### Screen Size Considerations
- Apple Watch screens are small (40-49mm)
- Use vertical scrolling sparingly
- Prefer single-tap interactions
- Keep text concise

### Common Patterns

#### Action Button
```swift
struct ActionButton: View {
    let title: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(title)
                .frame(maxWidth: .infinity)
        }
        .buttonStyle(.borderedProminent)
    }
}
```

#### Status Card
```swift
struct StatusCard: View {
    let icon: String
    let title: String
    let value: String

    var body: some View {
        HStack {
            Image(systemName: icon)
                .foregroundStyle(.secondary)
            VStack(alignment: .leading) {
                Text(title)
                    .font(.caption2)
                    .foregroundStyle(.secondary)
                Text(value)
                    .font(.headline)
            }
            Spacer()
        }
        .padding(.vertical, 4)
    }
}
```

### State Management
```swift
// Use @Observable for view models (watchOS 10+)
@Observable
final class FeatureViewModel {
    var items: [Item] = []
    var isLoading = false

    func loadItems() async {
        isLoading = true
        defer { isLoading = false }
        // Load items...
    }
}
```

### Haptic Feedback
```swift
// Add haptics for important interactions
WKInterfaceDevice.current().play(.success)
WKInterfaceDevice.current().play(.failure)
WKInterfaceDevice.current().play(.notification)
```

## Best Practices
- Extract reusable components when used 2+ times
- Use SF Symbols for icons
- Support Dynamic Type
- Test on multiple watch sizes
- Keep view body under 100 lines
