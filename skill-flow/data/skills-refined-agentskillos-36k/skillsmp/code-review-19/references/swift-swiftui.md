# SwiftUI Code Review Guide

Review points specific to SwiftUI (iOS 17+).

## State Management

### @Observable (iOS 17+)

```swift
// PREFERRED: Use @Observable for iOS 17+
@Observable
@MainActor
class ViewModel {
    var items: [Item] = []
    var selectedItem: Item?
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

### @State Usage

```swift
// CORRECT: @State for view-owned value types
struct CounterView: View {
    @State private var count = 0

    var body: some View {
        Button("Count: \(count)") {
            count += 1
        }
    }
}

// INCORRECT: @State for external data
struct BadView: View {
    @State private var users = fetchUsers()  // Wrong - use @Observable ViewModel
}
```

### @Binding

```swift
// Pass binding for child view to modify parent state
struct ParentView: View {
    @State private var text = ""

    var body: some View {
        ChildView(text: $text)
    }
}

struct ChildView: View {
    @Binding var text: String

    var body: some View {
        TextField("Enter text", text: $text)
    }
}
```

### Environment

```swift
// Share data through environment
@Observable
class AppState {
    var user: User?
    var theme: Theme = .system
}

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

struct ContentView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        Text(appState.user?.name ?? "Guest")
    }
}
```

## Navigation

### NavigationStack (iOS 16+)

```swift
// PREFERRED: Type-safe navigation
enum Destination: Hashable {
    case detail(Item)
    case settings
    case profile(User)
}

struct ContentView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            List(items) { item in
                NavigationLink(value: Destination.detail(item)) {
                    Text(item.name)
                }
            }
            .navigationDestination(for: Destination.self) { destination in
                switch destination {
                case .detail(let item):
                    ItemDetailView(item: item)
                case .settings:
                    SettingsView()
                case .profile(let user):
                    ProfileView(user: user)
                }
            }
        }
    }
}
```

### Programmatic Navigation

```swift
@Observable
class Router {
    var path = NavigationPath()

    func navigate(to destination: Destination) {
        path.append(destination)
    }

    func popToRoot() {
        path.removeLast(path.count)
    }

    func pop() {
        guard !path.isEmpty else { return }
        path.removeLast()
    }
}
```

## View Composition

### Extract Subviews

```swift
// BEFORE: Monolithic view
struct BadItemRow: View {
    let item: Item

    var body: some View {
        HStack {
            AsyncImage(url: item.imageURL) { image in
                image.resizable().aspectRatio(contentMode: .fill)
            } placeholder: {
                Color.gray
            }
            .frame(width: 50, height: 50)
            .clipShape(RoundedRectangle(cornerRadius: 8))

            VStack(alignment: .leading) {
                Text(item.name)
                    .font(.headline)
                Text(item.description)
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }

            Spacer()

            if item.isFavorite {
                Image(systemName: "heart.fill")
                    .foregroundStyle(.red)
            }
        }
    }
}

// AFTER: Composed subviews
struct ItemRow: View {
    let item: Item

    var body: some View {
        HStack {
            ItemThumbnail(url: item.imageURL)
            ItemInfo(name: item.name, description: item.description)
            Spacer()
            FavoriteIndicator(isFavorite: item.isFavorite)
        }
    }
}

struct ItemThumbnail: View {
    let url: URL?

    var body: some View {
        AsyncImage(url: url) { image in
            image.resizable().aspectRatio(contentMode: .fill)
        } placeholder: {
            Color.gray
        }
        .frame(width: 50, height: 50)
        .clipShape(RoundedRectangle(cornerRadius: 8))
    }
}
```

### ViewBuilder for Custom Containers

```swift
struct Card<Content: View>: View {
    @ViewBuilder let content: Content

    var body: some View {
        content
            .padding()
            .background(.regularMaterial)
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .shadow(radius: 2)
    }
}

// Usage
Card {
    VStack {
        Text("Title")
        Text("Description")
    }
}
```

## Performance Patterns

### Stable Identifiers

```swift
// BAD: Using index as ID
ForEach(items.indices, id: \.self) { index in
    ItemRow(item: items[index])  // All rows re-render on change
}

// GOOD: Using stable ID
ForEach(items) { item in  // Item: Identifiable
    ItemRow(item: item)  // Only changed rows re-render
}
```

### Equatable Views

```swift
// Help SwiftUI skip unnecessary updates
struct ItemRow: View, Equatable {
    let item: Item

    static func == (lhs: ItemRow, rhs: ItemRow) -> Bool {
        lhs.item.id == rhs.item.id &&
        lhs.item.name == rhs.item.name
    }

    var body: some View {
        Text(item.name)
    }
}
```

### Lazy Containers

```swift
// Use Lazy variants for large collections
LazyVStack {  // Only renders visible items
    ForEach(items) { item in
        ItemRow(item: item)
    }
}

LazyVGrid(columns: columns) {
    ForEach(items) { item in
        ItemCell(item: item)
    }
}
```

## Async Patterns

### .task Modifier

```swift
struct ContentView: View {
    @State private var viewModel = ContentViewModel()

    var body: some View {
        List(viewModel.items) { item in
            ItemRow(item: item)
        }
        .task {
            // Automatically cancelled when view disappears
            await viewModel.loadItems()
        }
        .task(id: viewModel.filter) {
            // Re-runs when filter changes
            await viewModel.applyFilter()
        }
        .refreshable {
            await viewModel.refresh()
        }
    }
}
```

### Loading States

```swift
struct ContentView: View {
    @State private var viewModel = ContentViewModel()

    var body: some View {
        Group {
            if viewModel.isLoading && viewModel.items.isEmpty {
                ProgressView()
            } else if let error = viewModel.error {
                ErrorView(error: error) {
                    Task { await viewModel.retry() }
                }
            } else if viewModel.items.isEmpty {
                EmptyStateView()
            } else {
                ItemList(items: viewModel.items)
            }
        }
        .task {
            await viewModel.loadItems()
        }
    }
}
```

## Accessibility

### Essential Modifiers

```swift
struct ItemRow: View {
    let item: Item
    let onTap: () -> Void

    var body: some View {
        Button(action: onTap) {
            HStack {
                Image(systemName: item.icon)
                    .accessibilityHidden(true)  // Decorative

                Text(item.name)
            }
        }
        .accessibilityLabel(item.name)
        .accessibilityHint("Double tap to view details")
        .accessibilityAddTraits(.isButton)
    }
}
```

### Dynamic Type Support

```swift
struct AdaptiveLayout: View {
    @Environment(\.dynamicTypeSize) private var typeSize

    var body: some View {
        if typeSize >= .accessibility1 {
            // Stack vertically for large text
            VStack { content }
        } else {
            // Horizontal for normal text
            HStack { content }
        }
    }
}
```

## Review Checklist

### State Management
- [ ] Using `@Observable` (iOS 17+) instead of `ObservableObject`
- [ ] `@State` only for view-owned value types
- [ ] `@MainActor` on ViewModels
- [ ] Environment used for shared app state

### Navigation
- [ ] Using `NavigationStack` (not deprecated `NavigationView`)
- [ ] Type-safe navigation with `navigationDestination`
- [ ] Router pattern for complex navigation

### Composition
- [ ] Views decomposed into smaller components
- [ ] Reusable components extracted
- [ ] `@ViewBuilder` for custom containers

### Performance
- [ ] Stable identifiers in `ForEach`
- [ ] `Lazy` containers for large collections
- [ ] No expensive computations in view body

### Async
- [ ] `.task` modifier for async work
- [ ] Loading/error states handled
- [ ] `.refreshable` for pull-to-refresh

### Accessibility
- [ ] Accessibility labels on interactive elements
- [ ] Dynamic Type supported
- [ ] VoiceOver tested
