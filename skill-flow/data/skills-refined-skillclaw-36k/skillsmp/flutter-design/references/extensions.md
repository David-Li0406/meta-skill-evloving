# ThemeExtension Patterns

Custom theme extensions for design tokens beyond Material's ColorScheme and TextTheme.

---

## Why ThemeExtension?

Use when you need:

- Custom color semantics (success, warning, info colors)
- Brand-specific tokens not in ColorScheme
- Custom spacing/sizing that should vary by theme
- Semantic aliases (e.g., `cardBackground`, `divider`)

---

## Basic ThemeExtension

```dart
class AppColors extends ThemeExtension<AppColors> {
  final Color success;
  final Color warning;
  final Color info;
  final Color cardBackground;
  final Color divider;

  const AppColors({
    required this.success,
    required this.warning,
    required this.info,
    required this.cardBackground,
    required this.divider,
  });

  @override
  AppColors copyWith({
    Color? success,
    Color? warning,
    Color? info,
    Color? cardBackground,
    Color? divider,
  }) {
    return AppColors(
      success: success ?? this.success,
      warning: warning ?? this.warning,
      info: info ?? this.info,
      cardBackground: cardBackground ?? this.cardBackground,
      divider: divider ?? this.divider,
    );
  }

  @override
  AppColors lerp(ThemeExtension<AppColors>? other, double t) {
    if (other is! AppColors) return this;
    return AppColors(
      success: Color.lerp(success, other.success, t)!,
      warning: Color.lerp(warning, other.warning, t)!,
      info: Color.lerp(info, other.info, t)!,
      cardBackground: Color.lerp(cardBackground, other.cardBackground, t)!,
      divider: Color.lerp(divider, other.divider, t)!,
    );
  }

  // Light theme
  static const light = AppColors(
    success: Color(0xFF16A34A),
    warning: Color(0xFFD97706),
    info: Color(0xFF2563EB),
    cardBackground: Colors.white,
    divider: Color(0xFFE2E8F0),
  );

  // Dark theme
  static const dark = AppColors(
    success: Color(0xFF4ADE80),
    warning: Color(0xFFFBBF24),
    info: Color(0xFF60A5FA),
    cardBackground: Color(0xFF1E293B),
    divider: Color(0xFF334155),
  );
}
```

---

## Register in ThemeData

```dart
ThemeData(
  useMaterial3: true,
  colorScheme: colorScheme,
  extensions: [
    AppColors.light,
    // Add more extensions as needed
  ],
)

// Dark theme
ThemeData(
  useMaterial3: true,
  colorScheme: darkColorScheme,
  extensions: [
    AppColors.dark,
  ],
)
```

---

## Access via Extension

```dart
extension BuildContextX on BuildContext {
  AppColors get appColors => Theme.of(this).extension<AppColors>()!;
}

// Usage
Container(color: context.appColors.success)
Divider(color: context.appColors.divider)
```

---

## Spacing Extension Example

```dart
class AppDimensions extends ThemeExtension<AppDimensions> {
  final double cardRadius;
  final double buttonRadius;
  final double inputRadius;
  final EdgeInsets screenPadding;

  const AppDimensions({
    required this.cardRadius,
    required this.buttonRadius,
    required this.inputRadius,
    required this.screenPadding,
  });

  @override
  AppDimensions copyWith({
    double? cardRadius,
    double? buttonRadius,
    double? inputRadius,
    EdgeInsets? screenPadding,
  }) {
    return AppDimensions(
      cardRadius: cardRadius ?? this.cardRadius,
      buttonRadius: buttonRadius ?? this.buttonRadius,
      inputRadius: inputRadius ?? this.inputRadius,
      screenPadding: screenPadding ?? this.screenPadding,
    );
  }

  @override
  AppDimensions lerp(ThemeExtension<AppDimensions>? other, double t) {
    if (other is! AppDimensions) return this;
    return AppDimensions(
      cardRadius: lerpDouble(cardRadius, other.cardRadius, t)!,
      buttonRadius: lerpDouble(buttonRadius, other.buttonRadius, t)!,
      inputRadius: lerpDouble(inputRadius, other.inputRadius, t)!,
      screenPadding: EdgeInsets.lerp(screenPadding, other.screenPadding, t)!,
    );
  }

  static const standard = AppDimensions(
    cardRadius: 12,
    buttonRadius: 8,
    inputRadius: 8,
    screenPadding: EdgeInsets.all(16),
  );
}
```

---

## Combined Context Extension

```dart
extension BuildContextX on BuildContext {
  // Theme
  ThemeData get theme => Theme.of(this);
  ColorScheme get colors => theme.colorScheme;
  TextTheme get textTheme => theme.textTheme;
  bool get isDark => theme.brightness == Brightness.dark;
  
  // Custom extensions
  AppColors get appColors => theme.extension<AppColors>()!;
  AppDimensions get dimensions => theme.extension<AppDimensions>()!;
}

// Usage
Container(
  padding: context.dimensions.screenPadding,
  decoration: BoxDecoration(
    color: context.appColors.cardBackground,
    borderRadius: BorderRadius.circular(context.dimensions.cardRadius),
  ),
)
```
