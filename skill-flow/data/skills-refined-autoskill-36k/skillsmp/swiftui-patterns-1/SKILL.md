---
name: swiftui-patterns
description: "Expert SwiftUI decisions: property wrapper selection (@State vs @StateObject vs @ObservedObject gotchas), navigation architecture (NavigationStack vs NavigationSplitView), performance traps (body recomputation, identity), and platform-specific patterns for tvOS focus. Use when building SwiftUI views for iOS/tvOS, debugging view update issues, or choosing navigation patterns. Trigger keywords: SwiftUI, @State, @StateObject, @ObservedObject, NavigationStack, sheet, animation, tvOS focus, view identity, body"
version: "3.0.0"
---

# SwiftUI Patterns — Expert Decisions

Expert decision frameworks for SwiftUI choices that require experience. Claude knows SwiftUI syntax — this skill provides the judgment calls that prevent subtle bugs.

---

## Decision Trees

### Property Wrapper Selection

```
Who creates the object?
├─ This view creates it
│  └─ Is it a value type (struct, primitive)?
│     ├─ YES → @State
│     └─ NO (class/ObservableObject)
│        └─ iOS 17+?
│           ├─ YES → @Observable class + var (no wrapper)
│           └─ NO → @StateObject
│
└─ Parent passes it down
   └─ Is it an ObservableObject?
      ├─ YES → @ObservedObject
      └─ NO
         └─ Need two-way binding?
            ├─ YES → @Binding
            └─ NO → Regular parameter
```

**The @StateObject vs @ObservedObject trap**: Using `@ObservedObject` for a locally-created object causes recreation on EVERY view update. State vanishes randomly.

```swift
// ❌ BROKEN — viewModel recreated on parent rerender
struct BadView: View {
    @ObservedObject var viewModel = UserViewModel()  // WRONG
}

// ✅ CORRECT — viewModel survives view updates
struct GoodView: View {
    @StateObject private var viewModel = UserViewModel()
}
```

### Navigation Pattern Selection

```
How many columns needed?
├─ 1 column (stack-based)
│  └─ NavigationStack with .navigationDestination
│
├─ 2 columns (list → detail)
│  └─ NavigationSplitView (2 column)
│     └─ iPad: sidebar + detail
│     └─ iPhone: collapses to stack
│
└─ 3 columns (sidebar → list → detail)
   └─ NavigationSplitView (3 column)
      └─ Mail/Files app pattern
```

**NavigationStack gotcha**: `navigationDestination(for:)` must be attached to a view INSIDE the NavigationStack, not on the NavigationStack itself. Wrong placement = silent failure.

```swift
// ❌ WRONG — destination outside stack hierarchy
NavigationStack {
    ContentView()
}
.navigationDestination(for: Item.self) { ... } // Never triggers!

// ✅ CORRECT — destination inside stack
NavigationStack {
    ContentView()
        .navigationDestination(for: Item.self) { item in
            DetailView(item: item)
        }
}
```

### Sheet vs FullScreenCover vs NavigationLink

```
Is it a modal workflow? (user must complete or cancel)
├─ YES
│  └─ Should user see parent context?
│     ├─ YES → .sheet (can dismiss by swiping)
│     └─ NO → .fullScreenCover (must tap button)
│
└─ NO (progressive disclosure in same flow)
   └─ NavigationLink / .navigationDestination
```

**Sheet state gotcha**: Sheet content is created BEFORE presentation. @StateObject inside sheet reinitializes on each presentation.

```swift
// ❌ PROBLEM — viewModel resets each time sheet opens
.sheet(isPresented: $show) {
    SheetView()  // New @StateObject created each time
}

// ✅ SOLUTION — pass data or use item binding
.sheet(item: $selectedItem) { item in
    SheetView(item: item)  // Item drives content
}
```

---

## NEVER Do

### View Identity & Performance

**NEVER** use AnyView unless absolutely necessary:
```swift
// ❌ Destroys view identity — state lost, animations break
func makeView() -> AnyView {
    if condition {
        return AnyView(ViewA())
    } else {
        return AnyView(ViewB())
    }
}

// ✅ Use @ViewBuilder — preserves identity
@ViewBuilder
func makeView() -> some View {
    if condition {
        ViewA()
    } else {
        ViewB()
    }
}
```

**NEVER** compute expensive values in body:
```swift
// ❌ Recomputed on EVERY view update
var body: some View {
    let processed = expensiveComputation(data)  // Runs constantly
    Text(processed)
}

// ✅ Use .task or computed property with caching
var body: some View {
    Text(cachedResult)
        .task(id: data) {
            cachedResult = await expensiveComputation(data)
        }
}
```

**NEVER** change view identity during animation:
```swift
// ❌ Animation breaks — different views
if isExpanded {
    ExpandedCard()  // One view
} else {
    CompactCard()   // Different view
}

// ✅ Same view, different state — smooth animation
CardView(isExpanded: isExpanded)
    .animation(.spring(), value: isExpanded)
```

### State Management

**NEVER** mutate @Published from background thread:
```swift
// ❌ Undefined behavior — sometimes works, sometimes crashes
Task.detached {
    viewModel.items = newItems  // Background thread!
}

// ✅ Always MainActor for @Published
Task { @MainActor in
    viewModel.items = newItems
}
// Or mark entire ViewModel as @MainActor
```

**NEVER** use .onAppear for async data loading:
```swift
// ❌ No cancellation, runs multiple times
.onAppear {
    Task { await loadData() }  // Not cancelled on disappear
}

// ✅ Use .task — automatic cancellation
.task {
    await loadData()  // Cancelled when view disappears
}
```

**NEVER** store derived state that should be computed:
```swift
// ❌ State duplication — can become inconsistent
@State private var items: [Item] = []
@State private var itemCount: Int = 0  // Derived from items!

// ✅ Compute derived values
@State private var items: [Item] = []
var itemCount: Int { items.count }
```

### Lists & ForEach

**NEVER** use array index as id:
```swift
// ❌ Bugs when array changes — wrong rows update
ForEach(items.indices, id: \.self) { index in
    ItemRow(item: items[index])
}

// ✅ Use stable identifier
ForEach(items) { item in  // Requires Identifiable
    ItemRow(item: item)
}
// Or explicit id
ForEach(items, id: \.stableId) { item in ... }
```

**NEVER** put List inside ScrollView:
```swift
// ❌ Double scrolling, broken behavior
ScrollView {
    List(items) { ... }
}

// ✅ List handles its own scrolling
List(items) { item in
    ItemRow(item: item)
}
```

---

## iOS/tvOS Platform Patterns

### tvOS Focus System

```swift
#if os(tvOS)
struct TVCardView: View {
    @Environment(\.isFocused) var isFocused

    var body: some View {
        VStack {
            Image(item.image)
            Text(item.title)
        }
        .scaleEffect(isFocused ? 1.1 : 1.0)
        .animation(.easeInOut(duration: 0.15), value: isFocused)
        // tvOS: 10ft viewing distance = larger touch targets
        .frame(width: 300, height: 400)
    }
}

struct TVRowView: View {
    @FocusState private var focusedIndex: Int?

    var body: some View {
        ScrollView(.horizontal) {
            HStack(spacing: 48) {  // tvOS needs larger spacing
                ForEach(items.indices, id: \.self) { index in
                    TVCardView(item: items[index])
                        .focusable()
                        .focused($focusedIndex, equals: index)
                }
            }
            .padding(.horizontal, 90)  // Safe area for overscan
        }
        .onAppear { focusedIndex = 0 }
    }
}
#endif
```

**tvOS gotcha**: Focus system REQUIRES explicit `.focusable()` on custom views. Without it, remote navigation skips the view entirely.

### Adaptive Layout Decision

```swift
struct AdaptiveView: View {
    @Environment(\.horizontalSizeClass) var sizeClass

    var body: some View {
        // iPhone portrait: compact, iPad/iPhone landscape: regular
        if sizeClass == .compact {
            VStack { content }
        } else {
            HStack { sidebar; content }
        }
    }
}

// Or use ViewThatFits for automatic selection
ViewThatFits {
    HStack { wideContent }  // Try first
    VStack { narrowContent } // Fallback
}
```

---

## Performance Patterns

### Preventing Unnecessary Redraws

```swift
// ✅ Equatable conformance for diffing
struct ItemRow: View, Equatable {
    let item: Item

    static func == (lhs: Self, rhs: Self) -> Bool {
        lhs.item.id == rhs.item.id &&
        lhs.item.name == rhs.item.name
    }

    var body: some View {
        Text(item.name)
    }
}

// ✅ Extract child views to isolate updates
struct ParentView: View {
    @StateObject var viewModel = ParentViewModel()

    var body: some View {
        VStack {
            // Only rerenders when header data changes
            HeaderView(title: viewModel.title)
            // Only rerenders when items change
            ItemList(items: viewModel.items)
        }
    }
}
```

### Lazy Loading Patterns

```swift
// ✅ LazyVStack for large lists — views created on demand
ScrollView {
    LazyVStack {
        ForEach(items) { item in
            ItemRow(item: item)  // Created when scrolled into view
        }
    }
}

// ✅ task(id:) for dependent async work
.task(id: searchQuery) {
    // Automatically cancels previous task when searchQuery changes
    results = await search(searchQuery)
}
```

---

## Common Gotchas

### Sheet/Alert Binding Timing

```swift
// ❌ PROBLEM — item is nil when sheet renders
@State var selectedItem: Item?

.sheet(isPresented: Binding(
    get: { selectedItem != nil },
    set: { if !$0 { selectedItem = nil } }
)) {
    ItemDetail(item: selectedItem!)  // Crash! nil during transition
}

// ✅ SOLUTION — use item binding
.sheet(item: $selectedItem) { item in
    ItemDetail(item: item)  // item guaranteed non-nil
}
```

### GeometryReader Sizing

```swift
// ❌ GeometryReader expands to fill available space
VStack {
    GeometryReader { geo in
        Text("Small text")  // But GeometryReader takes ALL space
    }
    Text("Never visible")  // Pushed off screen
}

// ✅ Wrap in fixed-size container or use sparingly
VStack {
    Text("Visible")
    Text("Also visible")
}
.background(
    GeometryReader { geo in
        Color.clear.onAppear { size = geo.size }
    }
)
```

### Animation + State Change Timing

```swift
// ❌ State change THEN animation — no animation occurs
showDetail = true
withAnimation { }  // Nothing to animate

// ✅ State change INSIDE withAnimation
withAnimation(.spring()) {
    showDetail = true  // This change gets animated
}
```

---

## Quick Reference

### Property Wrapper Cheat Sheet

| Wrapper | Creates | Survives Update | Use Case |
|---------|---------|-----------------|----------|
| @State | ✅ | ✅ | View-local value types |
| @StateObject | ✅ | ✅ | View-owned ObservableObject |
| @ObservedObject | ❌ | ❌ | Parent-passed ObservableObject |
| @Binding | ❌ | N/A | Two-way value connection |
| @EnvironmentObject | ❌ | N/A | App-wide shared state |

### Modifier Order Matters

```swift
// Different results!
Text("A").padding().background(.red)  // Red includes padding
Text("B").background(.red).padding()  // Red only behind text
```

Common order: content modifiers → padding → background → frame → position
