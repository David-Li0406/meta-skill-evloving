# Accessibility Reference

Accessibility implementation guidelines for iOS apps.

## VoiceOver Support

### Accessibility Labels

```swift
struct ProductCard: View {
    let product: Product

    var body: some View {
        VStack {
            Image(product.imageName)
                .accessibilityHidden(true)  // Decorative image

            Text(product.name)

            Text(product.price, format: .currency(code: "JPY"))
        }
        .accessibilityElement(children: .combine)
        .accessibilityLabel("\(product.name), \(product.price)円")
    }
}
```

### Accessibility Hints

```swift
Button("Add to Cart") {
    addToCart()
}
.accessibilityHint("Adds this item to your shopping cart")
```

### Accessibility Actions

```swift
struct ItemRow: View {
    let item: Item
    let onDelete: () -> Void
    let onEdit: () -> Void

    var body: some View {
        Text(item.name)
            .accessibilityAction(named: "Delete") {
                onDelete()
            }
            .accessibilityAction(named: "Edit") {
                onEdit()
            }
    }
}
```

### Accessibility Value

```swift
Slider(value: $volume, in: 0...100)
    .accessibilityValue("\(Int(volume))%")
    .accessibilityLabel("Volume")
```

### Custom Rotor

```swift
struct ArticleListView: View {
    let articles: [Article]
    @State private var selectedIndex = 0

    var body: some View {
        List(articles) { article in
            ArticleRow(article: article)
        }
        .accessibilityRotor("Headlines") {
            ForEach(articles) { article in
                AccessibilityRotorEntry(article.title, id: article.id)
            }
        }
    }
}
```

## Dynamic Type

### Scaled Fonts

```swift
struct ContentView: View {
    var body: some View {
        VStack {
            // Scales automatically
            Text("Title")
                .font(.title)

            Text("Body text")
                .font(.body)

            // Custom font with scaling
            Text("Custom")
                .font(.custom("MyFont", size: 16, relativeTo: .body))
        }
    }
}
```

### Dynamic Type Size Limits

```swift
struct CompactView: View {
    @Environment(\.dynamicTypeSize) var dynamicTypeSize

    var body: some View {
        Text("Content")
            .dynamicTypeSize(...DynamicTypeSize.accessibility2)  // Limit max size
    }
}
```

### Layout Adaptation

```swift
struct AdaptiveLayout: View {
    @Environment(\.dynamicTypeSize) var dynamicTypeSize

    var body: some View {
        if dynamicTypeSize.isAccessibilitySize {
            // Stack vertically for larger text
            VStack(alignment: .leading) {
                icon
                textContent
            }
        } else {
            // Horizontal layout for normal sizes
            HStack {
                icon
                textContent
            }
        }
    }
}
```

## Color and Contrast

### System Colors

```swift
struct ThemedView: View {
    var body: some View {
        VStack {
            Text("Primary")
                .foregroundStyle(.primary)  // Adapts to light/dark

            Text("Secondary")
                .foregroundStyle(.secondary)

            Rectangle()
                .fill(.background)  // System background
        }
    }
}
```

### High Contrast Support

```swift
struct ContrastAwareView: View {
    @Environment(\.colorSchemeContrast) var contrast

    var body: some View {
        Text("Content")
            .foregroundStyle(contrast == .increased ? .primary : .secondary)
    }
}
```

### Color Blindness

```swift
// Use patterns in addition to colors
struct StatusIndicator: View {
    let status: Status

    var body: some View {
        HStack {
            Image(systemName: status.iconName)
            Text(status.label)
        }
        .foregroundStyle(status.color)
        .accessibilityLabel(status.accessibilityLabel)
    }
}

enum Status {
    case success, warning, error

    var iconName: String {
        switch self {
        case .success: return "checkmark.circle.fill"
        case .warning: return "exclamationmark.triangle.fill"
        case .error: return "xmark.circle.fill"
        }
    }

    var accessibilityLabel: String {
        switch self {
        case .success: return "Success"
        case .warning: return "Warning"
        case .error: return "Error"
        }
    }
}
```

## Motion and Animation

### Reduce Motion

```swift
struct AnimatedView: View {
    @Environment(\.accessibilityReduceMotion) var reduceMotion
    @State private var isAnimating = false

    var body: some View {
        Circle()
            .scaleEffect(isAnimating ? 1.5 : 1.0)
            .animation(
                reduceMotion ? nil : .spring(),
                value: isAnimating
            )
    }
}
```

### Prefer Cross-Fade

```swift
struct TransitionView: View {
    @Environment(\.accessibilityReduceMotion) var reduceMotion
    @State private var showContent = false

    var body: some View {
        Group {
            if showContent {
                ContentView()
                    .transition(reduceMotion ? .opacity : .slide)
            }
        }
        .animation(.default, value: showContent)
    }
}
```

## Accessibility Traits

```swift
struct CustomButton: View {
    let title: String
    let action: () -> Void

    var body: some View {
        Text(title)
            .padding()
            .background(Color.blue)
            .accessibilityAddTraits(.isButton)
            .onTapGesture(perform: action)
    }
}

struct HeaderView: View {
    let text: String

    var body: some View {
        Text(text)
            .font(.headline)
            .accessibilityAddTraits(.isHeader)
    }
}

struct ToggleView: View {
    @Binding var isOn: Bool

    var body: some View {
        HStack {
            Text("Setting")
            Spacer()
            Image(systemName: isOn ? "checkmark" : "xmark")
        }
        .accessibilityElement(children: .combine)
        .accessibilityAddTraits(isOn ? [.isSelected] : [])
        .onTapGesture { isOn.toggle() }
    }
}
```

## Focus Management

### Focus State

```swift
struct LoginForm: View {
    @State private var email = ""
    @State private var password = ""
    @FocusState private var focusedField: Field?

    enum Field {
        case email, password
    }

    var body: some View {
        Form {
            TextField("Email", text: $email)
                .focused($focusedField, equals: .email)

            SecureField("Password", text: $password)
                .focused($focusedField, equals: .password)

            Button("Login") {
                login()
            }
        }
        .onSubmit {
            if focusedField == .email {
                focusedField = .password
            } else {
                login()
            }
        }
    }
}
```

### Accessibility Focus

```swift
struct AlertView: View {
    @AccessibilityFocusState private var isFocused: Bool
    @Binding var isPresented: Bool
    let message: String

    var body: some View {
        if isPresented {
            VStack {
                Text(message)
                    .accessibilityFocused($isFocused)

                Button("OK") {
                    isPresented = false
                }
            }
            .onAppear {
                isFocused = true
            }
        }
    }
}
```

## Testing Accessibility

### Accessibility Inspector

1. Open Xcode > Developer Tools > Accessibility Inspector
2. Point to elements in Simulator
3. Verify labels, hints, and traits

### XCTest Accessibility

```swift
func test_productCard_hasCorrectAccessibility() {
    let app = XCUIApplication()
    app.launch()

    let productCard = app.staticTexts["ProductName"]
    XCTAssertTrue(productCard.exists)

    let label = productCard.label
    XCTAssertTrue(label.contains("ProductName"))
    XCTAssertTrue(label.contains("¥"))
}
```

## Checklist

### Essential

- [ ] All interactive elements have accessibility labels
- [ ] Images have descriptions or are marked decorative
- [ ] Dynamic Type is supported
- [ ] VoiceOver navigation is logical

### Recommended

- [ ] Accessibility hints for non-obvious actions
- [ ] Reduce Motion is respected
- [ ] Color is not the only indicator
- [ ] Focus order is logical
- [ ] Custom controls announce state changes

### Advanced

- [ ] Custom rotors for complex content
- [ ] Semantic grouping with `accessibilityElement(children:)`
- [ ] Accessibility notifications for dynamic updates
- [ ] Support for external keyboards
