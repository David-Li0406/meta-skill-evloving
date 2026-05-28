# Architecture

This project follows a **Hexagonal Architecture** (Clean Architecture) pattern adapted for Flutter to ensure strict separation of concerns, testability, and maintainability.

## Layers

### 1. Domain (`lib/domain/`)
The core of the application. Contains business logic, entities, and interfaces (ports). **It has NO dependencies** on Flutter or other layers.
- **Entities**: Core business objects (e.g., `Supplement`, `Stack`, `UserGoal`).
- **Failures**: Definition of domain errors.
- **Repositories (Ports)**: Interfaces defining how to access data.

### 2. Application (`lib/application/`)
Orchestrates the domain logic.
- **Use Cases**: Specific business actions (e.g., `AddSupplementToStack`, `CompleteDailyCheckIn`).
- **View Models / Notifiers**: Manages state for the UI, converting domain entities to presentation data.

### 3. Infrastructure (`lib/infrastructure/`)
Implements the interfaces defined in the domain layer.
- **Repositories (Adapters)**: Implementation of domain repositories (e.g., `SupabaseSupplementRepository`, `LocalSettingsRepository`).
- **Data Sources**: Direct access to APIs, databases, or device features.
- **DTOs**: Data Transfer Objects for serialization/deserialization.

### 4. Presentation (`lib/presentation/`)
The UI layer, containing widgets and pages.
- **Views (Screens)**: Full-page widgets (e.g., `DailyStackScreen`, `InsightsScreen`).
- **Widgets**: Reusable UI components (e.g., `WeeklyWinCard`, `PillPreviewWidget`).
- **Theme**: App styling, colors, and fonts (`AppTheme`).

## Key Screens Implemented

- **Onboarding**: Goal Selection, Medication Safety (Simplified 3-step flow).
- **Dashboard**: Daily Stack with Time Urgency & Swipe-to-take, Level Up, Insights.
- **Library**: Supplement browser with interaction checks.
- **Reminders**: Persistent Nudge system with Evening Summaries.
- **Safety**: Safety Shield & Interaction Detail.
- **Review**: Weekly Review Summary.

## Design System

The app uses a custom design system with specific color palettes for different modes:
- **Default**: Slate/Blue/White.
- **Forest**: Dark greens for Daily Stack.
- **Streak**: Vibrant blues and flames.
- **Safety**: Amber warnings.
- **Celebration**: Gold and Purple.

## ADHD UX Principles

To accommodate users with ADHD, the app follows specific UI/UX patterns:
- **Low Friction**: Multi-step actions are collapsed into single gestures (e.g., Swipe-to-take).
- **Time Anchoring**: Abstract slots are converted to relative countdowns to solve time blindness.
- **Aggressive Persistency**: Reminders use nudge sequences (multi-stage) rather than single alerts.
- **Progress Preservation**: 4:00 AM rollover ensures streaks aren't broken by late-night productivity/insomnia.

## Development

- **Dependency Injection**: Managed via `get_it` in `lib/config/locator.dart`.
- **State Management**: `Provider` / `ChangeNotifier`.
- **Navigation**: Standard Navigator 2.0 or Named Routes (currently direct navigation via `ScreenSelector` for dev).
