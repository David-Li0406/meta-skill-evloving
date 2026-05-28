# ADR 0018: Unified Navigation Structure

**Date:** 2026-01-20  
**Status:** Accepted  
**Deciders:** Development Team

## Context

The application initially used multiple navigation styles across its various phases, including a FAB-based bottom nav on some screens and inconsistent navigation patterns on others. This created a fragmented user experience and navigation dead-ends when moving between core screens.

## Decision

Implement a unified, app-wide **5-item Bottom Navigation Bar** (`UnifiedBottomNav`) to replace all legacy navigation components on root-level screens.

The tabs are defined as:
1. **Today**: Dashboard (Check-ins, Summary).
2. **Stacks**: Daily Stack (The core checklist).
3. **Insights**: Success Stats (Charts and long-term trends).
4. **Library**: Supplement Discovery & Science Hub.
5. **Profile**: User Settings & Achievements.

## Rationale
- **Cognitive Load**: A single, consistent navigation pattern reduces the effort required for ADHD users to navigate the app.
- **Wireframe Alignment**: Aligns with the "Developer Handoff" specifications for a standardized navigation footer.
- **Navigation Flux**: Eliminates dead-ends by ensuring the main app states are always one tap away.
- **UI Consistency**: Standardizes the "Deep Focus" visual style (Gold Theme) across the footer.

## Consequences

**Positive:**
- Consistent user experience across all 5 main functional areas.
- Reduced code complexity by centralizing navigation logic in `UnifiedBottomNav`.
- Easier onboarding as users learn a single navigation paradigm.

**Negative:**
- Reduces available screen real estate on mobile devices.
- Requires careful handling of the back button stack to avoid navigation loops.

## Alternatives Considered

| Option | Rejected Because |
|--------|------------------|
| Floating Action Button (FAB) Nav | Difficult to scale beyond 2-3 actions; creates visual clutter over important list content. |
| Drawer-only Navigation | Too many taps to reach core features like "Stacks" or "Insights". |
| Adaptive Navigation | Increased implementation complexity; doesn't provide the stable "anchor" needed for ADHD friendliness. |
