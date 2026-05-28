# ADR 0007: Centralized Navigation with AppRouter

**Date:** 2026-01-19  
**Status:** Accepted  
**Deciders:** Development Team

## Context

With 32 screens and complex flows (onboarding, gamification, settings), navigation needed to be:
- Type-safe with named routes
- Centrally managed for easy discovery
- Consistent across all screens

## Decision

Create a centralized `AppRouter` class with:
- Static route constants
- `generateRoute` switch for MaterialPageRoute creation
- Helper methods for common navigation patterns

### Implementation

```dart
class AppRouter {
  // Route names
  static const String login = '/login';
  static const String dashboard = '/dashboard';
  static const String onboardingGoals = '/onboarding/goals';
  // ... 25+ more routes

  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case login:
        return MaterialPageRoute(builder: (_) => const LoginScreen());
      case dashboard:
        return MaterialPageRoute(builder: (_) => const DashboardScreen());
      // ...
    }
  }

  // Navigation helpers
  static void navigateToHome(BuildContext context) {
    Navigator.pushNamedAndRemoveUntil(context, dashboard, (route) => false);
  }
}
```

### Usage in Screens

```dart
Navigator.pushNamed(context, AppRouter.historyLog);
AppRouter.navigateToHome(context);
```

## Consequences

**Positive:**
- Single source of truth for routes
- Compile-time safety with constants
- Easy to add new routes
- Consistent navigation helpers

**Negative:**
- Large switch statement as app grows
- No compile-time argument validation

## Route Categories

| Category | Routes |
|----------|--------|
| Auth | login, signup |
| Onboarding | gracePeriod, goals, medicationSafety, stackSetup |
| Core | dashboard, dailyStack, insights |
| Gamification | trophyRoom, levelUp, streakSaved, streakRecovery |
| Settings | profile, privacySettings, reminders, appAppearance |
