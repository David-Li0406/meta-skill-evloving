# AI Coding Standards - ADHD Supplement App (Flutter)

## Overview
**Version**: 2.0 (Hardened Flutter Standard)
**Goal**: Build a professional, secure, and accessible health-focused app that meets 2026 App Store requirements.

## 1. Modular Architecture (Feature-First)
Organize code by feature to prevent "Hyperfocus Debt" and ensure scalability.

```
lib/
 ├── features/
 │   ├── supplements/       # Domain, Data, & UI for browsing
 │   ├── tracker/           # Daily logging & reminders
 │   └── safety/            # Interaction logic & meds check
 ├── core/                  # Shared themes, network, & DI
 └── shared/                # Global widgets (Buttons, Icons)
```

## 2. State Management (2026 Standard)
- **Riverpod 3.0 (Recommended)**: Use for its Offline Persistence API.
    - *Scenario*: User logs supplements in a basement (no signal) -> Save locally -> Sync later.
- **BLoC 9.0 (Enterprise)**: Use for complex multi-step forms or strict medical audit trails.
- **Avoid**: `setState` for anything beyond trivial UI toggles.

## 3. Mandatory Testing
Testing is non-negotiable for safety and referral integrity.

- **Unit Tests**: Every "Safety Guard" function must have a test case.
    - Example: `test('Adderall + Vit C returns High Risk')`.
- **Widget Tests**: Ensure "Buy on Amazon" buttons are always visible/clickable (Minimum size 48x48).
- **Integration Tests**: Verify full flows: "Open App -> Find Zinc -> Click Buy".

## 4. Platform Compliance (16KB & NDK)
Critical for May 2026 Android requirements.

- **Gradle**: Version 8.5.1 or higher.
- **NDK**: Version r28 or higher.
- **Verification**: Run `flutter build appbundle --analyze-size` and check for "16kb segment alignment".

## 5. Security & Accessibility (Health App Standard)
- **Local Encryption**: Use `flutter_secure_storage` or encrypted Hive box for medication names. NEVER store plain text medical data.
- **Accessibility (WCAG 2.1 AA)**:
    - **Contrast**: Minimum 4.5:1 ratio.
    - **Modes**: Provide "Low Stimulation Mode" (muted colors, no animations).
    - **Touch Targets**: Minimum 48x48 pixels.

## 6. Error Handling (Result Pattern)
Avoid unchecked exceptions. Use the `Result<T>` pattern for graceful handling.

```dart
// Standardized return type
typedef Result<T> = (T? data, Exception? error);

Future<Result<List<Supplement>>> fetchSupplements() async {
  try {
    final data = await api.get();
    return (data, null);
  } catch (e) {
    return (null, Exception('Check your internet connection'));
  }
}
```

## 7. UX & Cognitive Load (ADHD Specific)
- **Rule of 3**: Max 3 primary actions per screen.
- **Feedback**: Immediate Haptic/Visual feedback for every interaction.
- **Navigation**: Preference for flat navigation over deep stacks.

## Project Structure (Legacy to Feature-First Migration Guide)
*Refer to Section 1 for the target structure. Current `lib/presentation`, `lib/domain` structure should be refactored into `lib/features` gradually.*

## Documentation
- **ADRs**: Store architectural decisions in `docs/adrs/`.
- **Agents**: Rules and Skills located in `.agent/`.
- **Task Tracking**: implementation status in `task.md`.
