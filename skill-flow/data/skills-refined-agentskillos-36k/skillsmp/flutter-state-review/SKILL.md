---
name: flutter-state-review
description: Ensures Flutter strictly follows Cubit/Bloc-only, reactive state management with no Firebase calls in UI.
---

# Flutter State Review

## When to use this skill

- When reviewing Flux or UI code.
- When fixing bugs related to UI not updating.
- When refactoring "Spaghetti code" in Widgets.

## How to use it

1. **Ban Logic in UI**:
   - Ensure `build()` methods only contain `BlocBuilder`, `BlocListener`, or simple rendering logic.
   - **VIOLATION**: Calling `FirebaseFirestore.instance...` directly inside a Widget.
   - **VIOLATION**: Calling `setState` for business logic state.
2. **Review Bloc Dependencies**:
   - Blocs should depend on _Repositories_, not data sources directly.
   - Repositories should handle the data fetching/stream subscription.
3. **Stream Safety**:
   - Verify that data streams are properly managed (listened to in the Data layer, yielded as states in the Bloc).
   - Ensure streams are closed/cancelled when not needed (though Bloc usually handles this for subscriptions it manages).
4. **One-Way Data Flow**:
   - Action (UI) -> Event (Bloc) -> New State (Bloc) -> Rebuild (UI).
   - Ensure no side-effects bypass this flow.
