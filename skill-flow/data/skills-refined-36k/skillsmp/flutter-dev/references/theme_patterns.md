# Theme and Styling Patterns

Advanced theming, styling, and design patterns for Flutter applications.

## Complete Theme Configuration

```dart
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter App',
      theme: _buildLightTheme(),
      darkTheme: _buildDarkTheme(),
      themeMode: ThemeMode.system,
      home: const HomeScreen(),
    );
  }

  ThemeData _buildLightTheme() {
    final ColorScheme colorScheme = ColorScheme.fromSeed(
      seedColor: Colors.deepPurple,
      brightness: Brightness.light,
    );

    return ThemeData(
      useMaterial3: true,
      colorScheme: colorScheme,
      
      // Text theme
      textTheme: const TextTheme(
        displayLarge: TextStyle(
          fontSize: 57,
          fontWeight: FontWeight.bold,
          letterSpacing: -0.25,
        ),
        displayMedium: TextStyle(
          fontSize: 45,
          fontWeight: FontWeight.bold,
        ),
        titleLarge: TextStyle(
          fontSize: 22,
          fontWeight: FontWeight.w500,
        ),
        bodyLarge: TextStyle(
          fontSize: 16,
          height: 1.5,
        ),
        bodyMedium: TextStyle(
          fontSize: 14,
          height: 1.4,
        ),
        labelSmall: TextStyle(
          fontSize: 11,
          letterSpacing: 0.5,
        ),
      ),
      
      // Component themes
      appBarTheme: AppBarTheme(
        centerTitle: true,
        elevation: 0,
        backgroundColor: colorScheme.surface,
        foregroundColor: colorScheme.onSurface,
      ),
      
      cardTheme: CardTheme(
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
      
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          padding: const EdgeInsets.symmetric(
            horizontal: 24,
            vertical: 12,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      ),
      
      inputDecorationTheme: InputDecorationTheme(
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
        ),
        filled: true,
      ),
      
      // Custom extensions
      extensions: const [
        CustomColors(
          success: Color(0xFF4CAF50),
          warning: Color(0xFFFFC107),
          danger: Color(0xFFF44336),
        ),
      ],
    );
  }

  ThemeData _buildDarkTheme() {
    final ColorScheme colorScheme = ColorScheme.fromSeed(
      seedColor: Colors.deepPurple,
      brightness: Brightness.dark,
    );

    return ThemeData(
      useMaterial3: true,
      colorScheme: colorScheme,
      // Similar configuration as light theme
    );
  }
}
```

## Custom Theme Extension

```dart
@immutable
class CustomColors extends ThemeExtension<CustomColors> {
  const CustomColors({
    required this.success,
    required this.warning,
    required this.danger,
  });

  final Color? success;
  final Color? warning;
  final Color? danger;

  @override
  CustomColors copyWith({
    Color? success,
    Color? warning,
    Color? danger,
  }) {
    return CustomColors(
      success: success ?? this.success,
      warning: warning ?? this.warning,
      danger: danger ?? this.danger,
    );
  }

  @override
  CustomColors lerp(ThemeExtension<CustomColors>? other, double t) {
    if (other is! CustomColors) return this;
    return CustomColors(
      success: Color.lerp(success, other.success, t),
      warning: Color.lerp(warning, other.warning, t),
      danger: Color.lerp(danger, other.danger, t),
    );
  }
}

// Usage in widgets
class StatusBadge extends StatelessWidget {
  final String status;
  
  const StatusBadge({super.key, required this.status});

  @override
  Widget build(BuildContext context) {
    final customColors = Theme.of(context).extension<CustomColors>()!;
    
    Color backgroundColor;
    switch (status) {
      case 'success':
        backgroundColor = customColors.success!;
        break;
      case 'warning':
        backgroundColor = customColors.warning!;
        break;
      case 'danger':
        backgroundColor = customColors.danger!;
        break;
      default:
        backgroundColor = Theme.of(context).colorScheme.surface;
    }
    
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(16),
      ),
      child: Text(
        status,
        style: TextStyle(
          color: Theme.of(context).colorScheme.onSurface,
        ),
      ),
    );
  }
}
```

## Dynamic Theme Switching

```dart
class ThemeProvider extends ChangeNotifier {
  ThemeMode _themeMode = ThemeMode.system;
  
  ThemeMode get themeMode => _themeMode;
  
  void setThemeMode(ThemeMode mode) {
    _themeMode = mode;
    notifyListeners();
  }
  
  void toggleTheme() {
    if (_themeMode == ThemeMode.light) {
      _themeMode = ThemeMode.dark;
    } else {
      _themeMode = ThemeMode.light;
    }
    notifyListeners();
  }
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final ThemeProvider _themeProvider = ThemeProvider();

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: _themeProvider,
      builder: (context, child) {
        return MaterialApp(
          theme: _buildLightTheme(),
          darkTheme: _buildDarkTheme(),
          themeMode: _themeProvider.themeMode,
          home: HomeScreen(themeProvider: _themeProvider),
        );
      },
    );
  }
  
  // _buildLightTheme and _buildDarkTheme methods...
}

// In your screen
class SettingsScreen extends StatelessWidget {
  final ThemeProvider themeProvider;
  
  const SettingsScreen({super.key, required this.themeProvider});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Settings')),
      body: SwitchListTile(
        title: const Text('Dark Mode'),
        value: themeProvider.themeMode == ThemeMode.dark,
        onChanged: (value) {
          themeProvider.setThemeMode(
            value ? ThemeMode.dark : ThemeMode.light,
          );
        },
      ),
    );
  }
}
```

## WidgetStateProperty Styling

```dart
class StyledButton extends StatelessWidget {
  final VoidCallback onPressed;
  final String label;
  
  const StyledButton({
    super.key,
    required this.onPressed,
    required this.label,
  });

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      style: ButtonStyle(
        backgroundColor: WidgetStateProperty.resolveWith<Color>(
          (Set<WidgetState> states) {
            if (states.contains(WidgetState.disabled)) {
              return Colors.grey;
            }
            if (states.contains(WidgetState.pressed)) {
              return Colors.deepPurple.shade700;
            }
            if (states.contains(WidgetState.hovered)) {
              return Colors.deepPurple.shade400;
            }
            return Colors.deepPurple;
          },
        ),
        foregroundColor: WidgetStateProperty.all(Colors.white),
        padding: WidgetStateProperty.all(
          const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
        ),
        elevation: WidgetStateProperty.resolveWith<double>(
          (Set<WidgetState> states) {
            if (states.contains(WidgetState.pressed)) {
              return 8;
            }
            if (states.contains(WidgetState.hovered)) {
              return 4;
            }
            return 2;
          },
        ),
        shape: WidgetStateProperty.all(
          RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      ),
      onPressed: onPressed,
      child: Text(label),
    );
  }
}
```

## Responsive Typography

```dart
class ResponsiveText extends StatelessWidget {
  final String text;
  final TextStyle? baseStyle;
  
  const ResponsiveText({
    super.key,
    required this.text,
    this.baseStyle,
  });

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final double fontSize = _getFontSize(constraints.maxWidth);
        
        return Text(
          text,
          style: (baseStyle ?? const TextStyle()).copyWith(
            fontSize: fontSize,
          ),
        );
      },
    );
  }
  
  double _getFontSize(double width) {
    if (width < 600) {
      return 14; // Mobile
    } else if (width < 1200) {
      return 16; // Tablet
    } else {
      return 18; // Desktop
    }
  }
}
```

## Google Fonts Integration

```dart
// Add to pubspec.yaml: google_fonts: ^latest

import 'package:google_fonts/google_fonts.dart';

ThemeData _buildTheme() {
  return ThemeData(
    textTheme: GoogleFonts.robotoTextTheme(),
    
    // Or customize individual styles
    textTheme: TextTheme(
      displayLarge: GoogleFonts.oswald(
        fontSize: 57,
        fontWeight: FontWeight.bold,
      ),
      titleLarge: GoogleFonts.roboto(
        fontSize: 22,
        fontWeight: FontWeight.w500,
      ),
      bodyMedium: GoogleFonts.openSans(
        fontSize: 14,
      ),
    ),
  );
}

// Or use directly in widgets
Text(
  'Hello World',
  style: GoogleFonts.lato(
    fontSize: 24,
    fontWeight: FontWeight.bold,
  ),
)
```

## Glassmorphism Effect

```dart
class GlassCard extends StatelessWidget {
  final Widget child;
  final double blur;
  final double opacity;
  
  const GlassCard({
    super.key,
    required this.child,
    this.blur = 10,
    this.opacity = 0.2,
  });

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(16),
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: blur, sigmaY: blur),
        child: Container(
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(opacity),
            borderRadius: BorderRadius.circular(16),
            border: Border.all(
              color: Colors.white.withOpacity(0.2),
              width: 1.5,
            ),
          ),
          child: child,
        ),
      ),
    );
  }
}
```

## Color Palette Generator

```dart
class ColorPalette {
  static List<Color> generatePalette(Color seedColor) {
    final HSLColor hsl = HSLColor.fromColor(seedColor);
    
    return [
      hsl.withLightness(0.95).toColor(), // 50
      hsl.withLightness(0.90).toColor(), // 100
      hsl.withLightness(0.80).toColor(), // 200
      hsl.withLightness(0.70).toColor(), // 300
      hsl.withLightness(0.60).toColor(), // 400
      hsl.withLightness(0.50).toColor(), // 500
      hsl.withLightness(0.40).toColor(), // 600
      hsl.withLightness(0.30).toColor(), // 700
      hsl.withLightness(0.20).toColor(), // 800
      hsl.withLightness(0.10).toColor(), // 900
    ];
  }
}
```

## Design Tokens Pattern

```dart
class DesignTokens {
  // Spacing
  static const double spacing1 = 4.0;
  static const double spacing2 = 8.0;
  static const double spacing3 = 12.0;
  static const double spacing4 = 16.0;
  static const double spacing5 = 24.0;
  static const double spacing6 = 32.0;
  
  // Border Radius
  static const double radiusSmall = 4.0;
  static const double radiusMedium = 8.0;
  static const double radiusLarge = 12.0;
  static const double radiusXLarge = 16.0;
  
  // Elevation
  static const double elevationLow = 2.0;
  static const double elevationMedium = 4.0;
  static const double elevationHigh = 8.0;
  
  // Animation Duration
  static const Duration durationFast = Duration(milliseconds: 150);
  static const Duration durationMedium = Duration(milliseconds: 300);
  static const Duration durationSlow = Duration(milliseconds: 500);
}

// Usage
Container(
  padding: const EdgeInsets.all(DesignTokens.spacing4),
  decoration: BoxDecoration(
    borderRadius: BorderRadius.circular(DesignTokens.radiusMedium),
  ),
)
```
