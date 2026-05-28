import 'package:flutter/material.dart';

/// Night theme for MagentaLine EFB
/// Red-tinted for cockpit night vision preservation
class NightTheme {
  NightTheme._();

  // Dark backgrounds
  static const Color background = Color(0xFF121212);
  static const Color surface = Color(0xFF1E1E1E);
  static const Color surfaceVariant = Color(0xFF2C2C2C);

  // Red-tinted accent for night vision
  static const Color primary = Color(0xFFCF6679);       // Muted red
  static const Color secondary = Color(0xFFFF6B6B);     // Soft red accent
  static const Color error = Color(0xFFFF5252);

  // Text colors (red-tinted)
  static const Color textPrimary = Color(0xFFE0B0B0);   // Light red-tinted
  static const Color textSecondary = Color(0xFFA08080); // Muted red-tinted

  // Aviation-specific colors (dimmed for night)
  static const Color vfr = Color(0xFF66BB6A);           // Muted green
  static const Color mvfr = Color(0xFF42A5F5);          // Muted blue
  static const Color ifr = Color(0xFFEF5350);           // Muted red
  static const Color lifr = Color(0xFFAB47BC);          // Muted purple

  // Map colors (dimmed)
  static const Color routeLine = Color(0xFFFF4081);     // Dimmed magenta
  static const Color trackLine = Color(0xFF455A64);     // Dark gray
  static const Color airspaceClassB = Color(0xFF1565C0);
  static const Color airspaceClassC = Color(0xFF7B1FA2);
  static const Color airspaceClassD = Color(0xFF0277BD);
  static const Color airspaceRestricted = Color(0xFFC62828);

  static ThemeData get themeData => ThemeData(
    useMaterial3: true,
    brightness: Brightness.dark,
    colorScheme: ColorScheme.dark(
      primary: primary,
      secondary: secondary,
      surface: surface,
      error: error,
      onPrimary: Colors.black,
      onSecondary: Colors.black,
      onSurface: textPrimary,
    ),
    scaffoldBackgroundColor: background,

    // AppBar
    appBarTheme: const AppBarTheme(
      backgroundColor: surface,
      foregroundColor: textPrimary,
      elevation: 0,
    ),

    // Cards
    cardTheme: CardTheme(
      color: surface,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8),
        side: BorderSide(color: Colors.white.withOpacity(0.1)),
      ),
    ),

    // Buttons
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: primary.withOpacity(0.8),
        foregroundColor: Colors.black,
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
    ),

    // Input fields
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: surfaceVariant,
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8),
        borderSide: BorderSide.none,
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8),
        borderSide: const BorderSide(color: primary, width: 1),
      ),
      labelStyle: const TextStyle(color: textSecondary),
      hintStyle: const TextStyle(color: textSecondary),
    ),

    // Text - all red-tinted for night vision
    textTheme: const TextTheme(
      headlineLarge: TextStyle(
        fontSize: 32,
        fontWeight: FontWeight.bold,
        color: textPrimary,
      ),
      headlineMedium: TextStyle(
        fontSize: 24,
        fontWeight: FontWeight.bold,
        color: textPrimary,
      ),
      titleLarge: TextStyle(
        fontSize: 20,
        fontWeight: FontWeight.w600,
        color: textPrimary,
      ),
      titleMedium: TextStyle(
        fontSize: 16,
        fontWeight: FontWeight.w600,
        color: textPrimary,
      ),
      bodyLarge: TextStyle(
        fontSize: 16,
        color: textPrimary,
      ),
      bodyMedium: TextStyle(
        fontSize: 14,
        color: textPrimary,
      ),
      bodySmall: TextStyle(
        fontSize: 12,
        color: textSecondary,
      ),
      // Monospace for data display
      labelLarge: TextStyle(
        fontSize: 14,
        fontFamily: 'RobotoMono',
        color: textPrimary,
      ),
    ),

    // Icons - red-tinted
    iconTheme: const IconThemeData(
      color: textPrimary,
      size: 24,
    ),

    // Dividers
    dividerTheme: DividerThemeData(
      color: Colors.white.withOpacity(0.1),
      thickness: 1,
    ),

    // Chips
    chipTheme: ChipThemeData(
      backgroundColor: surfaceVariant,
      labelStyle: const TextStyle(color: textPrimary),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
    ),

    // Bottom navigation
    bottomNavigationBarTheme: const BottomNavigationBarThemeData(
      backgroundColor: surface,
      selectedItemColor: primary,
      unselectedItemColor: textSecondary,
    ),

    // Slider (for brightness control, etc.)
    sliderTheme: SliderThemeData(
      activeTrackColor: primary,
      inactiveTrackColor: surfaceVariant,
      thumbColor: primary,
      overlayColor: primary.withOpacity(0.2),
    ),

    // Switch
    switchTheme: SwitchThemeData(
      thumbColor: WidgetStateProperty.resolveWith((states) {
        if (states.contains(WidgetState.selected)) {
          return primary;
        }
        return textSecondary;
      }),
      trackColor: WidgetStateProperty.resolveWith((states) {
        if (states.contains(WidgetState.selected)) {
          return primary.withOpacity(0.5);
        }
        return surfaceVariant;
      }),
    ),
  );
}
