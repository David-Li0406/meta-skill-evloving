---
name: swiftui-navigation-mvvm-patterns
description: Use this skill when making expert decisions about SwiftUI patterns, navigation architecture, and MVVM design for iOS/tvOS applications.
---

# SwiftUI, Navigation, and MVVM Patterns — Expert Decisions

This skill provides expert frameworks for making decisions in SwiftUI regarding property wrappers, navigation patterns, and MVVM architecture. It helps prevent common pitfalls and optimizes app design.

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
└─ Parent passes it down
   └─ Is it an ObservableObject?
      ├─ YES → @ObservedObject
      └─ NO
         └─ Need two-way binding?
            ├─ YES → @Binding
            └─ NO → Regular parameter
```

### Navigation Architecture Selection

```
How complex is your navigation?
├─ Simple (linear flows, 1-3 screens)
│  └─ NavigationStack with inline NavigationLink
│     No Router needed
│
├─ Medium (multiple flows, deep linking required)
│  └─ NavigationStack + Router (ObservableObject)
│     Centralized navigation state
│
└─ Complex (tabs with independent stacks, cross-tab navigation)
   └─ Tab Coordinator + per-tab Routers
      Each tab maintains own NavigationPath
```

### ViewModel Pattern Selection

```
Does the screen have distinct, mutually exclusive states?
├─ YES (loading → loaded → error)
│  └─ State Enum Pattern
│     @Published var state: State = .idle
│     enum State { case idle, loading, loaded(Data), error(String) }
│
└─ NO (multiple independent properties)
   └─ Does the screen need form validation?
      ├─ YES → Combine Pattern (publishers for validation chains)
      └─ NO → Published Properties Pattern (simplest)
```

---

## Common Gotchas

### NavigationPath State

**NEVER** store NavigationPath in ViewModel without careful consideration:
```swift
// ❌ Coupling business logic to navigation
@MainActor
final class HomeViewModel: ObservableObject {
    @Published var path = NavigationPath()  // Wrong layer!
}

// ✅ Router/Coordinator owns navigation
@MainActor
final class Router: ObservableObject {
    @Published var path = NavigationPath()
}
```

### ViewModel Anti-Patterns

**NEVER** load data in ViewModel `init`:
```swift
// ❌ Starts loading before view appears
class BadViewModel: ObservableObject {
    init() {
        Task { await loadData() }  // Fire-and-forget in init
    }
}

// ✅ Load via .task modifier
struct GoodView: View {
    @StateObject var viewModel = GoodViewModel()
    var body: some View {
        content.task { await viewModel.loadData() }
    }
}
```

### Deep Link Handling Strategy

```
When does deep link arrive?
├─ App already running (warm start)
│  └─ Direct navigation via Router
│
└─ App launches from deep link (cold start)
   └─ Is view hierarchy ready?
      ├─ YES → Navigate immediately
      └─ NO → Queue pending deep link
         Handle in root view's .onAppear
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
```

### Lazy Loading Patterns

```swift
// ✅ LazyVStack for large lists
ScrollView {
    LazyVStack {
        ForEach(items) { item in
            ItemRow(item: item)  // Created when scrolled into view
        }
    }
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

### Navigation Architecture Comparison

| Pattern | Complexity | Deep Link Support | Testability |
|---------|------------|-------------------|-------------|
| Inline NavigationLink | Low | Manual | Low |
| Router with typed array | Medium | Good | High |
| NavigationPath | Medium | Good | Medium |
| Coordinator Pattern | High | Excellent | Excellent |

### ViewModel Checklist

- [ ] `@MainActor` on class
- [ ] `private(set)` on @Published properties
- [ ] Protocol-based dependencies with defaults
- [ ] CancellationError handled separately
- [ ] No UI types (Color, Font, etc.)
- [ ] No direct network/database calls
- [ ] Testable without UI framework