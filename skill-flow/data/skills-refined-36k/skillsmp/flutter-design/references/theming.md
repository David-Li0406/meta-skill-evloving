# Flutter Theming

Comprehensive ThemeData and ColorScheme patterns for Flutter apps.

---

## Complete ThemeData Setup

```dart
import 'package:flutter/material.dart';

class AppTheme {
  static ThemeData light() {
    final colorScheme = ColorScheme.fromSeed(
      seedColor: const Color(0xFF2563EB), // Brand blue
      brightness: Brightness.light,
    );
    
    return ThemeData(
      useMaterial3: true,
      colorScheme: colorScheme,
      textTheme: _textTheme(colorScheme),
      appBarTheme: _appBarTheme(colorScheme),
      cardTheme: _cardTheme(colorScheme),
      inputDecorationTheme: _inputTheme(colorScheme),
      elevatedButtonTheme: _elevatedButtonTheme(colorScheme),
      outlinedButtonTheme: _outlinedButtonTheme(colorScheme),
      textButtonTheme: _textButtonTheme(colorScheme),
    );
  }
  
  static ThemeData dark() {
    final colorScheme = ColorScheme.fromSeed(
      seedColor: const Color(0xFF2563EB),
      brightness: Brightness.dark,
    );
    
    return ThemeData(
      useMaterial3: true,
      colorScheme: colorScheme,
      textTheme: _textTheme(colorScheme),
      appBarTheme: _appBarTheme(colorScheme),
      cardTheme: _cardTheme(colorScheme),
      inputDecorationTheme: _inputTheme(colorScheme),
      elevatedButtonTheme: _elevatedButtonTheme(colorScheme),
      outlinedButtonTheme: _outlinedButtonTheme(colorScheme),
      textButtonTheme: _textButtonTheme(colorScheme),
    );
  }
}
```

---

## Custom ColorScheme

When you need more control than `fromSeed`:

```dart
ColorScheme(
  brightness: Brightness.light,
  primary: const Color(0xFF2563EB),
  onPrimary: Colors.white,
  primaryContainer: const Color(0xFFDBEAFE),
  onPrimaryContainer: const Color(0xFF1E3A5F),
  secondary: const Color(0xFF64748B),
  onSecondary: Colors.white,
  surface: Colors.white,
  onSurface: const Color(0xFF0F172A),
  surfaceContainerHighest: const Color(0xFFF1F5F9),
  outline: const Color(0xFFCBD5E1),
  error: const Color(0xFFDC2626),
  onError: Colors.white,
)
```

---

## AppBar Theme

```dart
static AppBarTheme _appBarTheme(ColorScheme colors) {
  return AppBarTheme(
    elevation: 0,
    scrolledUnderElevation: 1,
    backgroundColor: colors.surface,
    foregroundColor: colors.onSurface,
    titleTextStyle: TextStyle(
      color: colors.onSurface,
      fontSize: 18,
      fontWeight: FontWeight.w600,
    ),
  );
}
```

---

## Card Theme

```dart
static CardTheme _cardTheme(ColorScheme colors) {
  return CardTheme(
    elevation: 0,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(12),
      side: BorderSide(color: colors.outline.withOpacity(0.2)),
    ),
    color: colors.surface,
  );
}
```

---

## Input Decoration Theme

```dart
static InputDecorationTheme _inputTheme(ColorScheme colors) {
  return InputDecorationTheme(
    filled: true,
    fillColor: colors.surface,
    contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
    border: OutlineInputBorder(
      borderRadius: BorderRadius.circular(8),
      borderSide: BorderSide(color: colors.outline),
    ),
    enabledBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(8),
      borderSide: BorderSide(color: colors.outline),
    ),
    focusedBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(8),
      borderSide: BorderSide(color: colors.primary, width: 2),
    ),
    errorBorder: OutlineInputBorder(
      borderRadius: BorderRadius.circular(8),
      borderSide: BorderSide(color: colors.error),
    ),
    hintStyle: TextStyle(color: colors.onSurface.withOpacity(0.5)),
  );
}
```

---

## Button Themes

```dart
static ElevatedButtonThemeData _elevatedButtonTheme(ColorScheme colors) {
  return ElevatedButtonThemeData(
    style: ElevatedButton.styleFrom(
      backgroundColor: colors.primary,
      foregroundColor: colors.onPrimary,
      elevation: 0,
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8),
      ),
      textStyle: const TextStyle(
        fontSize: 14,
        fontWeight: FontWeight.w600,
      ),
    ),
  );
}

static OutlinedButtonThemeData _outlinedButtonTheme(ColorScheme colors) {
  return OutlinedButtonThemeData(
    style: OutlinedButton.styleFrom(
      foregroundColor: colors.primary,
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8),
      ),
      side: BorderSide(color: colors.outline),
      textStyle: const TextStyle(
        fontSize: 14,
        fontWeight: FontWeight.w600,
      ),
    ),
  );
}

static TextButtonThemeData _textButtonTheme(ColorScheme colors) {
  return TextButtonThemeData(
    style: TextButton.styleFrom(
      foregroundColor: colors.primary,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      textStyle: const TextStyle(
        fontSize: 14,
        fontWeight: FontWeight.w600,
      ),
    ),
  );
}
```

---

## BuildContext Extensions

```dart
extension BuildContextX on BuildContext {
  ThemeData get theme => Theme.of(this);
  ColorScheme get colors => theme.colorScheme;
  TextTheme get textTheme => theme.textTheme;
  
  // Convenience
  bool get isDark => theme.brightness == Brightness.dark;
}

// Usage
Text('Hello', style: context.textTheme.bodyLarge)
Container(color: context.colors.primary)
```
