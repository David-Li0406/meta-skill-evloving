# ADR 002: Refinement & Developer Handoff Strategy

## Context
As the project moves rapidly through phases (Engagement -> Safety -> Support), complex logic and system health checks (permissions, battery optimization) are being implemented. These features often require specific states to verify (e.g., "battery optimization disabled") which are hard to reproduce manually. Additionally, the backend logic for triggers (Nudges, XP) needs to be communicated clearly to the backend team.

## Decision
We decided to implement a **"Developer Handoff & Refinement" strategy** that exposes these internal logic loops and system checks as first-class UI screens, accessible via a "Developer Tools" section in the app.

### 1. Dedicated Verification Screens
Instead of abstract logic, we built full UI implementations for:
- **System Health Hub**: Visualizes permission states.
- **Science Update**: Visualizes the content update flow.
- **Developer Handoff**: A specific screen documenting the backend logic *within the app itself*.

### 2. In-App Documentation
We treat the application as its own documentation. The `DeveloperHandoffLogicTriggersScreen` serves as a "living spec" that:
- Shows the exact logic loops (e.g., `if (user.inactive > 5m)`).
- defining the expected data sync frequency (Real-time vs Polling).
- Visualization of the state machine.

### 3. Accessible Entry Point
These screens are exposed via a "Developer Tools" section in the `UserProfileScreen`.
- **Why**: Allows instant access for QA and Stakeholders without needing special builds or deep-linking knowledge.
- **Production Safety**: This section is marked "Debug Only" and can be easily hidden behind a flag or removed in release builds.

## Consequences
### Positive
- **Faster Verification**: Safety features and permissions can be UI-tested immediately.
- **Better Communication**: Backend engineers see exactly what the frontend expects via the "Blueprint" screen.
- **Reduced Ambiguity**: "Reference implementations" for screens like Science Update are now code, not just Figma files.

### Negative
- **App Bloat**: Adds slightly to bundle size (negligible for text/UI code).
- **Cleanup**: Must ensure these routes are secured or removed before App Store submission.

## Status
Accepted and Implemented (Phase 4 Refinement)
