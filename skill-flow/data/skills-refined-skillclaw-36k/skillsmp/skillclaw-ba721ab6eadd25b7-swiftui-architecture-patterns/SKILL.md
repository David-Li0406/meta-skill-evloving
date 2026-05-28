---
name: swiftui-architecture-patterns
description: Use this skill when making expert decisions about SwiftUI architecture, including property wrappers, navigation patterns, and MVVM design choices for iOS/tvOS applications.
---

# SwiftUI Architecture Patterns — Expert Decisions

This skill provides expert frameworks for making architectural decisions in SwiftUI applications, covering property wrappers, navigation patterns, and MVVM design principles.

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

**The @StateObject vs @ObservedObject trap**: Using `@ObservedObject` for a locally-created object causes recreation on EVERY view update. State can vanish unexpectedly.

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

### NavigationPath vs Typed Array

```
Do you need heterogeneous routes?
├─ YES (different types in same stack)
│  └─ NavigationPath (type-erased)
│     path.append(User(...))
│     path.append(Product(...))
│
└─ NO (single route enum)
   └─ @State var path: [Route] = []
      Type-safe, debuggable, serializable
```

**Rule**: Prefer typed arrays unless you genuinely need mixed types. NavigationPath's type erasure complicates debugging.

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

**The trap**: Avoid putting API calls directly in ViewModel. This complicates testing and requires network mocking instead of simple service mocking.

### @StateObject Injection

```
Does ViewModel need dependencies from parent?
├─ NO → Direct initialization
│  @StateObject private var viewModel = UserViewModel()
│
└─ YES → How many dependencies?
   ├─ 1-2 → Init parameter
   │  init(userId: String) {
   │      _viewModel = StateObject(wrappedValue: UserViewModel(userId: userId))
   │  }
   │
   └─ Many → Factory/Container
      @StateObject private var viewModel: UserViewModel
      init() {
          _viewModel = StateObject(wrappedValue: UserViewModel())
      }
```