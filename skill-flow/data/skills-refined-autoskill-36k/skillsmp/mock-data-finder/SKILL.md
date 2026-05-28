---
name: mock-data-finder
description: Find and remove silent mock data fallbacks in Android/iOS screens. Use when screens show fake data, when debugging why real API data isn't loading, or to ensure proper error handling instead of mock fallbacks.
allowed-tools: Read, Grep, Glob, Edit
---

# Mock Data Finder

## Purpose
Find Android and iOS screens that silently fall back to mock data when API calls fail, hiding real errors from users and developers.

## Why This Matters

Silent mock data fallbacks:
- Hide API errors making debugging difficult
- Show fake data to users (misleading)
- Prevent proper error handling/retry UI
- Make it impossible to know if API is working

## Detection Patterns

### Android (Kotlin)

Look for catch blocks that load mock data:

```kotlin
// BAD: Silent fallback to mock
} catch (e: Exception) {
    state = state.copy(
        loading = false,
        data = getMockData()  // User sees fake data!
    )
}

// GOOD: Show error, let user retry
} catch (e: Exception) {
    Log.e("Screen", "API failed", e)
    state = state.copy(
        loading = false,
        error = "Failed to load: ${e.message}"
    )
}
```

### Search Commands

Find mock data in Android:
```bash
# Find getMock functions
grep -r "getMock" apps/android/ --include="*.kt"

# Find mock fallbacks in catch blocks
grep -rn "catch.*Exception" apps/android/ --include="*.kt" -A 5 | grep -i mock

# Find hardcoded test data
grep -rn "listOf\|arrayOf" apps/android/*/ui/screens/ --include="*.kt" | grep -E "(id.*=.*\".*-\"|test|mock|fake)"
```

Find mock data in iOS:
```bash
# Find mock/preview data
grep -r "mock\|Mock\|preview\|Preview" apps/ios/ --include="*.swift"

# Find catch blocks with fallbacks
grep -rn "catch" apps/ios/ --include="*.swift" -A 3
```

## Common Mock Data Patterns

### Pattern 1: getMockXxx() Function
```kotlin
fun getMockDashboard(): Dashboard {
    return Dashboard(
        items = listOf(
            Item(id = "mock-1", name = "Test Item")
        )
    )
}
```

### Pattern 2: Inline Mock in Catch
```kotlin
catch (e: Exception) {
    val mockData = listOf(
        User(id = "u1", name = "John Doe"),
        User(id = "u2", name = "Jane Doe")
    )
    state = state.copy(users = mockData)
}
```

### Pattern 3: Conditional Mock Fallback
```kotlin
val data = apiResponse ?: getMockData()
// or
val data = if (apiResponse.isEmpty()) getMockData() else apiResponse
```

## Fix Pattern

Replace mock fallbacks with proper error handling:

```kotlin
// BEFORE
fun loadData() {
    scope.launch {
        state = state.copy(loading = true)
        try {
            val data = apiService.getData()
            state = state.copy(loading = false, data = data)
        } catch (e: Exception) {
            // Silent mock fallback - BAD!
            state = state.copy(loading = false, data = getMockData())
        }
    }
}

// AFTER
fun loadData() {
    scope.launch {
        state = state.copy(loading = true, error = null)
        try {
            val data = apiService.getData()
            state = state.copy(loading = false, data = data)
        } catch (e: Exception) {
            // Log error and show to user - GOOD!
            Log.e("ScreenName", "Failed to load data", e)
            state = state.copy(
                loading = false,
                error = "Failed to load data: ${e.message}"
            )
        }
    }
}
```

## Checklist

When reviewing a screen:

- [ ] No `getMock*()` functions called in production code
- [ ] Catch blocks log errors with `Log.e()`
- [ ] Catch blocks set `error` state, not mock data
- [ ] UI has error state display (error banner, retry button)
- [ ] No hardcoded test IDs (`"test-1"`, `"mock-id"`, etc.)

## Files to Check

Common locations for mock data:

**Android:**
- `apps/android/**/ui/screens/*.kt` - Screen composables
- `apps/android/**/ui/viewmodels/*.kt` - ViewModels
- `apps/android/**/data/repository/*.kt` - Repositories

**iOS:**
- `apps/ios/**/Views/*.swift` - SwiftUI views
- `apps/ios/**/ViewModels/*.swift` - ViewModels
- `apps/ios/**/Services/*.swift` - API services
