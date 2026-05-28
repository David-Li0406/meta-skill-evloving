---
name: Performance Optimizer
description: Find and fix performance issues in Leavn - main thread blocking, heavy View body computation, missing lazy loading, inefficient list rendering
allowed-tools: Read, Edit, Grep, Glob
---

# Performance Optimizer

## Instructions

Optimize Leavn app performance:

1. **Find main thread operations**:
   - Search for regex in View body
   - Find CGContext/UIGraphicsImageRenderer in Views
   - Look for `DispatchQueue.main.async` chains
   - Check for heavy computation in computed properties

2. **Fix patterns**:
   ```swift
   // BEFORE - Main thread blocking
   let result = expensiveRegex()

   // AFTER - Background
   Task.detached {
       let result = await expensiveWork()
       await MainActor.run { updateUI(result) }
   }
   ```

3. **Add lazy loading**:
   - Use `.onAppear` with viewport tracking
   - LazyVStack for long lists
   - Defer AI transformations until visible

4. **Optimize lookups**:
   ```swift
   // BEFORE - O(n)
   array.contains { $0.id == id }

   // AFTER - O(1)
   private lazy var idSet = Set(array.map(\.id))
   idSet.contains(id)
   ```

5. **Cache computations**:
   - Move from View to ViewModel
   - Invalidate cache on data change
   - Use `didSet` observers

Use this skill when: UI is laggy, scrolling stutters, app feels slow, CPU usage high
