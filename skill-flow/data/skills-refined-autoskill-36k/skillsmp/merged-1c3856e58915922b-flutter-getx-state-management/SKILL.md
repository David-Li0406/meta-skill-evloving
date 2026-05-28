---
name: flutter-getx-state-management
description: Use this skill for simple and powerful reactive state management in Flutter applications using GetX.
---

# GetX State Management

## **Priority: P0 (CRITICAL)**

Reactive and lightweight state management that separates business logic from UI using `GetX`.

## Structure

```text
lib/app/modules/home/
├── controllers/
│   └── home_controller.dart
├── bindings/
│   └── home_binding.dart
└── views/
    └── home_view.dart
```

## Implementation Guidelines

- **Controllers**: Extend `GetxController` to store logic and state variables.
- **Reactivity**:
  - Use `.obs` for observable variables (e.g., `final count = 0.obs;`).
  - Wrap UI in `Obx(() => ...)` to listen for changes.
  - For simple state, use `update()` in the controller and `GetBuilder` in the UI.
- **Dependency Injection**:
  - **Bindings**: Use the `Bindings` class to decouple DI from UI.
  - **Lazy Load**: Prefer `Get.lazyPut(() => Controller())` in Bindings.
  - **Lifecycle**: Let GetX handle disposal; avoid `permanent: true`.
- **Hooks**: Use `onInit()`, `onReady()`, `onClose()` instead of `initState`/`dispose`.
- **Architecture**: Use `get_cli` for modular MVVM (data, models, modules).

## Anti-Patterns

- **Ctx in Logic**: Do not pass `BuildContext` to controllers.
- **Inline DI**: Avoid `Get.put()` in widgets; use Bindings + `Get.find`.
- **Fat Views**: Keep views as pure UI; delegate all logic to the controller.

## Code Example

```dart
class UserController extends GetxController {
  final name = "User".obs;
  void updateName(String val) => name.value = val;
}

class UserView extends GetView<UserController> {
  @override
  Widget build(ctx) => Scaffold(
    body: Obx(() => Text(controller.name.value)),
    floatingActionButton: FloatingActionButton(
      onPressed: () => controller.updateName("New"),
    ),
  );
}
```

## Related Topics

getx-navigation | layer-based-clean-architecture | dependency-injection