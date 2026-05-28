---
name: performance-optimization
description: Use this skill when debugging performance issues, optimizing slow screens, or reducing memory usage in Swift/iOS applications.
---

# Performance Optimization — Expert Decisions

This skill provides techniques and frameworks for optimizing performance in Swift and iOS applications, focusing on profiling, memory management, and rendering efficiency.

## Best Practices

1. **Profile First**: Always use Instruments to identify bottlenecks before optimizing.
2. **Memory Management**: Understand ARC, avoid retain cycles, and manage memory efficiently.
3. **Lazy Loading**: Defer expensive operations and use lazy properties when appropriate.
4. **Efficient Collections**: Choose the right data structures and operations for performance.
5. **UI Performance**: Optimize rendering with techniques like cell reuse and background processing.
6. **Concurrency**: Use GCD or Swift Concurrency for background tasks without blocking the main thread.

## Decision Trees

### Should You Optimize?

```
When should you invest in optimization?
├─ User-facing latency issue (visible stutter/delay)
│  └─ YES — Profile and fix
│     Measure first, optimize second
│
├─ Premature concern ("this might be slow")
│  └─ NO — Wait for evidence
│     Write clean code, profile later
│
├─ Battery drain complaints
│  └─ YES — Use Energy Diagnostics
│     Focus on background work, location, network
│
├─ Memory warnings / crashes
│  └─ YES — Use Allocations + Leaks
│     Find retain cycles, unbounded caches
│
└─ App store reviews mention slowness
   └─ YES — Profile real scenarios
      User perception matters
```

### Profiling Tool Selection

```
What are you measuring?
├─ Slow UI / frame drops
│  └─ Time Profiler + View Debugger
│     Find expensive work on main thread
│
├─ Memory growth / leaks
│  └─ Allocations + Leaks instruments
│     Track object lifetimes, find cycles
│
├─ Network performance
│  └─ Network instrument + Charles/Proxyman
│     Latency, payload size, request count
│
├─ Disk I/O issues
│  └─ File Activity instrument
│     Excessive reads/writes
│
├─ Battery drain
│  └─ Energy Log instrument
│     CPU wake, location, networking
│
└─ GPU / rendering
   └─ Core Animation instrument
      Offscreen rendering, overdraw
```

## Performance Guidelines

- Minimize work on the main thread, especially UI updates.
- Use Instruments Time Profiler to find CPU hotspots.
- Monitor memory usage with Allocations and Leaks instruments.
- Optimize images and assets for size and loading.
- Cache expensive computations when possible.
- Avoid unnecessary view updates in SwiftUI with proper state management.

## SwiftUI View Update Strategy

```
View is re-rendering too often?
├─ Caused by parent state changes
│  └─ Extract to separate view
│     Child doesn't depend on changing state
│
├─ Complex computed body
│  └─ Cache expensive computations
│     Use ViewModel or memoization
│
├─ List items all updating
│  └─ Check view identity
│     Use stable IDs, not indices
│
├─ Observable causing cascading updates
│  └─ Split into multiple @Published
│     Or use computed properties
│
└─ Animation causing constant redraws
   └─ Use drawingGroup() or limit scope
      Rasterize stable content
```

## Memory Management Decision

```
How to fix memory issues?
├─ Steady growth during use
│  └─ Check caches and collections
│     Add eviction, use NSCache
│
├─ Growth tied to navigation
│  └─ Check retain cycles
│     weak self in closures, delegates
│
├─ Large spikes on specific screens
│  └─ Downsample images
│     Load at display size, not full resolution
│
├─ Memory not released after screen dismissal
│  └─ Debug object lifecycle
│     deinit not called = retain cycle
│
└─ Background memory pressure
   └─ Respond to didReceiveMemoryWarning
      Clear caches, release non-essential data
```

## Essential Patterns

### Efficient List View

```swift
struct EfficientListView: View {
    let items: [Item]

    var body: some View {
        ScrollView {
            LazyVStack(spacing: 12) {  // Lazy = on-demand creation
                ForEach(items) { item in
                    ItemRow(item: item)
                        .id(item.id)  // Stable identity
                }
            }
        }
    }
}

// Equatable row prevents unnecessary updates
struct ItemRow: View, Equatable {
    let item: Item

    var body: some View {
        HStack {
            AsyncImage(url: item.imageURL) { image in
                image.resizable().aspectRatio(contentMode: .fill)
            } placeholder: {
                Color.gray.opacity(0.3)
            }
            .frame(width: 60, height: 60)
            .clipShape(RoundedRectangle(cornerRadius: 8))

            VStack(alignment: .leading) {
                Text(item.title).font(.headline)
                Text(item.subtitle).font(.caption).foregroundColor(.secondary)
            }
        }
    }

    static func == (lhs: ItemRow, rhs: ItemRow) -> Bool {
        lhs.item.id == rhs.item.id &&
        lhs.item.title == rhs.item.title &&
        lhs.item.subtitle == rhs.item.subtitle
    }
}
```

### Memory-Safe ViewModel

```swift
@MainActor
final class ViewModel: ObservableObject {
    @Published private(set) var items: [Item] = []
    @Published private(set) var isLoading = false

    private var cancellables = Set<AnyCancellable>()
    private var loadTask: Task<Void, Never>?

    func load() {
        loadTask?.cancel()  // Cancel previous

        loadTask = Task {
            guard !Task.isCancelled else { return }

            isLoading = true
            defer { isLoading = false }

            do {
                let items = try await API.fetchItems()
                guard !Task.isCancelled else { return }
                self.items = items
            } catch {
                // Handle error
            }
        }
    }

    deinit {
        loadTask?.cancel()
        cancellables.removeAll()
    }
}
```

### Quick Reference

#### Instruments Selection

| Issue | Instrument | What to Look For |
|-------|------------|------------------|
| Slow UI | Time Profiler | Heavy main thread work |
| Memory leak | Leaks | Leaked objects |
| Memory growth | Allocations | Growing categories |
| Battery | Energy Log | Wake frequency |
| Network | Network | Request count, size |
| Disk | File Activity | Excessive I/O |
| GPU | Core Animation | Offscreen renders |

#### SwiftUI Performance Checklist

| Issue | Solution |
|-------|----------|
| Slow list scrolling | Use LazyVStack/LazyVGrid |
| All items re-render | Stable IDs, Equatable rows |
| Heavy body computation | Move to ViewModel |
| Cascading @Published updates | Split or use computed |
| Animation jank | Use drawingGroup() |

#### Memory Management

| Pattern | Prevent Issue |
|---------|---------------|
| [weak self] in closures | Retain cycles |
| Timer.invalidate() in deinit | Timer leaks |
| Remove observers in deinit | Observer leaks |
| NSCache with limits | Unbounded cache growth |
| Image downsampling | Memory spikes |