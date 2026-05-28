# Optimization & Stability Plan

## Goal
Improve the codebase's long-term maintainability, performance, and ADHD-friendly UX polish without adding new functional features.

## Proposed Changes

### 1. Architectural Stability
#### [MODIFY] [locator.dart](file:///Users/lycanbeats/Desktop/adhd_supplement_app/lib/config/locator.dart)
Split into functional modules or at least group registrations logically with comments.

#### [NEW] [logger.dart](file:///Users/lycanbeats/Desktop/adhd_supplement_app/lib/utils/logger.dart)
Introduce a centralized `AppLogger` that uses the `logger` package or structured `print` wrappers to replace `debugPrint`.

#### [NEW] [failure.dart](file:///Users/lycanbeats/Desktop/adhd_supplement_app/lib/domain/errors/failure.dart)
Introduce a typed `Failure` system (e.g., `ServerFailure`, `CacheFailure`, `AuthFailure`) to replace generic `Exception` throws.

### 2. Performance & Asset Optimization
#### [MODIFY] Multiple Screens
Replace `NetworkImage` with `CachedNetworkImage` (add dependency `cached_network_image`) for better performance and offline support.

#### [MODIFY] [firebase_log_repository.dart](file:///Users/lycanbeats/Desktop/adhd_supplement_app/lib/infrastructure/repositories/firebase_log_repository.dart) & Others
Refactor Firestore fetch logic to use a unified "Resilient Fetch" helper that handles server/cache fallback gracefully.

### 3. ADHD UX Polish
#### [NEW] [skeleton_loaders.dart](file:///Users/lycanbeats/Desktop/adhd_supplement_app/lib/presentation/widgets/skeleton_loader.dart)
Implement skeleton loaders for the Daily Stack and Insights screens to provide smoother "loading-to-loaded" transitions.

#### [MODIFY] [daily_stack_view_model.dart](file:///Users/lycanbeats/Desktop/adhd_supplement_app/lib/presentation/view_models/daily_stack_view_model.dart)
Add `HapticFeedback` triggers for successful "Quick Take" actions.

### 4. Testing Infrastructure
#### [MODIFY] [daily_stack_screen_test.dart](file:///Users/lycanbeats/Desktop/adhd_supplement_app/test/widget/daily_stack_screen_test.dart)
Fix the common "Multiple providers" or "Missing locator" errors in widget tests by creating a `test_utils.dart` wrapper for test environments.

## Verification Plan

### Automated Tests
- Fix existing widget tests: `flutter test test/widget/`
- Verify image caching logic doesn't break offline mode.

### Manual Verification
- Visual audit of skeleton loaders.
- Verify haptic feedback on physical device (if applicable) or via logs.
