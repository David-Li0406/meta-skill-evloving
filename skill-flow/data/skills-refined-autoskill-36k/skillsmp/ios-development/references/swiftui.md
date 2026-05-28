# SwiftUI Reference (iOS 17+)

Comprehensive SwiftUI patterns and best practices for iOS 17+.

## State Management

### @Observable Macro (iOS 17+)

The `@Observable` macro replaces `ObservableObject` for simpler state management:

```swift
import Observation

@Observable
class CounterState {
    var count = 0
    var isLoading = false

    // Computed properties work automatically
    var doubleCount: Int { count * 2 }
}
```

**Usage in Views**:

```swift
struct CounterView: View {
    // Use @State for owned observable objects
    @State private var state = CounterState()

    var body: some View {
        VStack {
            Text("Count: \(state.count)")
            Button("Increment") { state.count += 1 }
        }
    }
}
```

### Property Wrappers Comparison

| Wrapper | iOS 17+ Usage | Purpose |
|---------|---------------|---------|
| `@State` | With @Observable | View-owned mutable state |
| `@Binding` | Same | Two-way connection to parent state |
| `@Environment` | With @Observable | Dependency injection |
| `@Bindable` | New | Create bindings from @Observable |

### @Bindable for Two-Way Binding

```swift
@Observable
class FormState {
    var username = ""
    var email = ""
}

struct FormView: View {
    @Bindable var state: FormState

    var body: some View {
        Form {
            TextField("Username", text: $state.username)
            TextField("Email", text: $state.email)
        }
    }
}
```

## Navigation

### NavigationStack

```swift
struct ContentView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            List {
                NavigationLink("Go to Detail", value: "detail-1")
            }
            .navigationDestination(for: String.self) { id in
                DetailView(id: id)
            }
            .navigationTitle("Home")
        }
    }
}
```

### Programmatic Navigation

```swift
@Observable
class Router {
    var path = NavigationPath()

    func navigate<T: Hashable>(to destination: T) {
        path.append(destination)
    }

    func pop() {
        guard !path.isEmpty else { return }
        path.removeLast()
    }

    func popToRoot() {
        path.removeLast(path.count)
    }
}

// Usage
struct ContentView: View {
    @State private var router = Router()

    var body: some View {
        NavigationStack(path: $router.path) {
            HomeView()
                .environment(router)
        }
    }
}
```

### Navigation Destinations Enum

```swift
enum Destination: Hashable {
    case userDetail(userId: Int)
    case settings
    case profile
}

struct ContentView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            HomeView()
                .navigationDestination(for: Destination.self) { destination in
                    switch destination {
                    case .userDetail(let userId):
                        UserDetailView(userId: userId)
                    case .settings:
                        SettingsView()
                    case .profile:
                        ProfileView()
                    }
                }
        }
    }
}
```

## View Composition

### Custom View Modifiers

```swift
struct CardModifier: ViewModifier {
    var padding: CGFloat = 16
    var cornerRadius: CGFloat = 12

    func body(content: Content) -> some View {
        content
            .padding(padding)
            .background(.background)
            .clipShape(RoundedRectangle(cornerRadius: cornerRadius))
            .shadow(color: .black.opacity(0.1), radius: 4, y: 2)
    }
}

extension View {
    func cardStyle(padding: CGFloat = 16, cornerRadius: CGFloat = 12) -> some View {
        modifier(CardModifier(padding: padding, cornerRadius: cornerRadius))
    }
}

// Usage
Text("Hello")
    .cardStyle()
```

### View Builder Extensions

```swift
extension View {
    @ViewBuilder
    func `if`<Content: View>(_ condition: Bool, transform: (Self) -> Content) -> some View {
        if condition {
            transform(self)
        } else {
            self
        }
    }
}

// Usage
Text("Hello")
    .if(isHighlighted) { view in
        view.foregroundStyle(.blue)
    }
```

## Lists and Collections

### Lazy Loading

```swift
struct ItemListView: View {
    let items: [Item]

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 8) {
                ForEach(items) { item in
                    ItemRow(item: item)
                }
            }
            .padding()
        }
    }
}
```

### Sections with Headers

```swift
struct GroupedListView: View {
    let sections: [Section]

    var body: some View {
        List {
            ForEach(sections) { section in
                Section(section.title) {
                    ForEach(section.items) { item in
                        ItemRow(item: item)
                    }
                }
            }
        }
        .listStyle(.insetGrouped)
    }
}
```

### Swipe Actions

```swift
struct ItemRow: View {
    let item: Item
    let onDelete: () -> Void
    let onArchive: () -> Void

    var body: some View {
        Text(item.name)
            .swipeActions(edge: .trailing, allowsFullSwipe: true) {
                Button(role: .destructive, action: onDelete) {
                    Label("Delete", systemImage: "trash")
                }
            }
            .swipeActions(edge: .leading) {
                Button(action: onArchive) {
                    Label("Archive", systemImage: "archivebox")
                }
                .tint(.orange)
            }
    }
}
```

## Animations

### Implicit Animations

```swift
struct AnimatedView: View {
    @State private var isExpanded = false

    var body: some View {
        VStack {
            RoundedRectangle(cornerRadius: 12)
                .fill(.blue)
                .frame(height: isExpanded ? 200 : 100)
                .animation(.spring(duration: 0.3), value: isExpanded)

            Button("Toggle") {
                isExpanded.toggle()
            }
        }
    }
}
```

### Explicit Animations

```swift
struct ExplicitAnimationView: View {
    @State private var scale: CGFloat = 1.0

    var body: some View {
        Circle()
            .fill(.blue)
            .frame(width: 100, height: 100)
            .scaleEffect(scale)
            .onTapGesture {
                withAnimation(.bouncy) {
                    scale = scale == 1.0 ? 1.5 : 1.0
                }
            }
    }
}
```

### Transitions

```swift
struct TransitionView: View {
    @State private var showDetail = false

    var body: some View {
        VStack {
            if showDetail {
                DetailCard()
                    .transition(.asymmetric(
                        insertion: .move(edge: .trailing).combined(with: .opacity),
                        removal: .move(edge: .leading).combined(with: .opacity)
                    ))
            }

            Button("Toggle") {
                withAnimation {
                    showDetail.toggle()
                }
            }
        }
    }
}
```

## Async Operations

### Task Modifier

```swift
struct AsyncView: View {
    @State private var data: [Item] = []
    @State private var isLoading = true

    var body: some View {
        List(data) { item in
            Text(item.name)
        }
        .overlay {
            if isLoading {
                ProgressView()
            }
        }
        .task {
            await loadData()
        }
    }

    private func loadData() async {
        defer { isLoading = false }
        // Fetch data
    }
}
```

### Task with ID for Refresh

```swift
struct RefreshableView: View {
    @State private var userId: Int
    @State private var user: User?

    var body: some View {
        UserDetailView(user: user)
            .task(id: userId) {
                user = await fetchUser(id: userId)
            }
    }
}
```

## Previews

### #Preview Macro (iOS 17+)

```swift
#Preview {
    ContentView()
}

#Preview("Dark Mode") {
    ContentView()
        .preferredColorScheme(.dark)
}

#Preview("Large Text") {
    ContentView()
        .dynamicTypeSize(.xxxLarge)
}

// With traits
#Preview(traits: .sizeThatFitsLayout) {
    ItemRow(item: .preview)
        .padding()
}
```

### Preview Data

```swift
extension User {
    static let preview = User(
        id: 1,
        name: "Preview User",
        email: "preview@example.com"
    )

    static let previewList: [User] = [
        User(id: 1, name: "Alice", email: "alice@example.com"),
        User(id: 2, name: "Bob", email: "bob@example.com"),
    ]
}
```

## Environment Values

### Custom Environment Keys

```swift
private struct ThemeKey: EnvironmentKey {
    static let defaultValue: Theme = .light
}

extension EnvironmentValues {
    var theme: Theme {
        get { self[ThemeKey.self] }
        set { self[ThemeKey.self] = newValue }
    }
}

// Usage
struct ThemedView: View {
    @Environment(\.theme) private var theme

    var body: some View {
        Text("Hello")
            .foregroundStyle(theme.primaryColor)
    }
}

// Setting
ContentView()
    .environment(\.theme, .dark)
```

### Injecting @Observable Objects

```swift
@Observable
class AppState {
    var user: User?
    var isAuthenticated: Bool { user != nil }
}

// In App
@main
struct MyApp: App {
    @State private var appState = AppState()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(appState)
        }
    }
}

// Usage
struct ProfileView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        if let user = appState.user {
            Text(user.name)
        }
    }
}
```

## Performance Tips

1. **Use `@State` for view-local state** - Avoid unnecessary observable objects
2. **Prefer `LazyVStack`/`LazyHStack`** - For large collections
3. **Extract subviews** - Help SwiftUI optimize re-renders
4. **Use `equatable()` modifier** - When view equality check is expensive
5. **Avoid computed properties in body** - Extract to separate properties
6. **Use `task(id:)` instead of `onChange`** - For async operations on value changes
