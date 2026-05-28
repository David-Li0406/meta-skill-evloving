# ADR 0008: Screen Architecture and Component Organization

**Date:** 2026-01-19  
**Status:** Accepted  
**Deciders:** Development Team

## Context

With 32 implemented screens, we needed a consistent structure for:
- Screen files (StatelessWidget vs StatefulWidget)
- Reusable widgets extraction
- Theme application
- Dark mode support

## Decision

### Directory Structure

```
lib/presentation/
├── views/              # Full screens
│   ├── auth/           # Login, Signup
│   ├── dashboard_screen.dart
│   ├── daily_stack_screen.dart
│   └── ... (32 screens)
├── widgets/            # Reusable components
│   ├── up_next_card.dart
│   ├── daily_stack_item.dart
│   └── ... (20+ widgets)
├── view_models/        # State management
│   ├── daily_stack_view_model.dart
│   └── ...
├── navigation/         # Routing
│   └── app_router.dart
└── theme/              # Styling
    └── app_theme.dart
```

### Screen Pattern

```dart
class DailyStackScreen extends StatefulWidget {
  const DailyStackScreen({super.key});
  
  @override
  State<DailyStackScreen> createState() => _DailyStackScreenState();
}

class _DailyStackScreenState extends State<DailyStackScreen> {
  late SomeViewModel _viewModel;
  
  @override
  void initState() { /* Initialize ViewModel */ }
  
  @override
  void dispose() { _viewModel.dispose(); }
  
  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    return ChangeNotifierProvider.value(
      value: _viewModel,
      child: Scaffold(/* ... */),
    );
  }
}
```

### Dark Mode Pattern

Every screen checks theme brightness and applies appropriate colors:

```dart
final isDark = Theme.of(context).brightness == Brightness.dark;
final bgColor = isDark ? AppColors.backgroundDark : AppColors.backgroundLight;
```

## Screen Categories

| Count | Category | Examples |
|-------|----------|----------|
| 2 | Auth | Login, Signup |
| 4 | Onboarding | Grace Period, Goals, Medication, Stack Setup |
| 3 | Core | Dashboard, Daily Stack, Insights |
| 4 | Gamification | Trophy Room, Level Up, Streak Saved/Recovery |
| 4 | Settings | Profile, Privacy, Reminders, App Appearance |
| 15 | Feature | Library, Stack Builder, History, Community, etc. |

## Consequences

**Positive:**
- Consistent code patterns across screens
- Easy to onboard new developers
- Clear separation between screens and reusable widgets
- Automatic dark mode support

**Negative:**
- Some boilerplate in each screen
- Widget extraction requires judgment calls
