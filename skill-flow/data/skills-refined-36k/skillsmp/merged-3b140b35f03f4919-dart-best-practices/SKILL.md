---
name: dart-best-practices
description: Use this skill when you want to ensure clean and maintainable Dart code.
---

# Dart Best Practices

## **Priority: P1 (OPERATIONAL)**

Best practices for writing clean, maintainable Dart code.

- **Scoping**:
  - No global variables.
  - Private globals (if required) must start with `_`.
- **Immutability**: Use `const` > `final` > `var`.
- **Config**: Use `--dart-define` for secrets. Never hardcode API keys.
- **Naming**: Follow [effective-dart](https://dart.dev/guides/language/effective-dart) (PascalCase classes, camelCase members).

```dart
import 'models/user.dart'; // Good
import 'package:app/models/user.dart'; // Avoid local absolute
```