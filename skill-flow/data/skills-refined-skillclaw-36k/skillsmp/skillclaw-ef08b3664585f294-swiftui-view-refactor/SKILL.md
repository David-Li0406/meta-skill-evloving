---
name: swiftui-view-refactor
description: Use this skill when you need to refactor and review SwiftUI view files for consistent structure, dependency injection, and Observation usage.
---

# SwiftUI View Refactor

## Overview
Apply a consistent structure and dependency pattern to SwiftUI views, focusing on ordering, Model-View (MV) patterns, careful view model handling, and correct Observation usage.

## Core Guidelines

### 1) View Ordering (Top → Bottom)
- Environment
- `private`/`public` `let`
- `@State` / other stored properties
- Computed `var` (non-view)
- `init`
- `body`
- Computed view builders / other view helpers
- Helper / async functions

### 2) Prefer MV (Model-View) Patterns
- Default to MV: Views are lightweight state expressions; models/services own business logic.
- Favor `@State`, `@Environment`, `@Query`, and `task`/`onChange` for orchestration.
- Inject services and shared models via `@Environment`; keep views small and composable.
- Split large views into subviews rather than introducing a view model.

### 3) Split Large Bodies and View Properties
- If `body` grows beyond a screen or has multiple logical sections, split it into smaller subviews.
- Extract large computed view properties (`var header: some View { ... }`) into dedicated `View` types when they carry state or complex branching.
- It's fine to keep related subviews as computed view properties in the same file; extract to a standalone `View` struct only when it structurally makes sense or when reuse is intended.
- Prefer passing small inputs (data, bindings, callbacks) over reusing the entire parent view state.

## Examples

### Extracting a Section
```swift
var body: some View {
    VStack(alignment: .leading, spacing: 16) {
        HeaderSection(title: title, isPinned: isPinned)
        DetailsSection(details: details)
        ActionsSection(onSave: onSave, onCancel: onCancel)
    }
}
```

### Long Body → Shorter Body + Computed Views in the Same File
```swift
var body: some View {
    List {
        header
        filters
        results
        footer
    }
}

private var header: some View {
    VStack(alignment: .leading, spacing: 6) {
        Text(title).font(.title2)
        Text(subtitle).font(.subheadline)
    }
}
```