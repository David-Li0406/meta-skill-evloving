import 'package:flutter/material.dart';

/// Day theme for MagentaLine EFB
/// Optimized for outdoor cockpit visibility
class DayTheme {
  DayTheme._();

  static const Color primary = Color(0xFF1976D2);       // Blue
  static const Color secondary = Color(0xFFFF4081);     // Magenta accent
  static const Color surface = Color(0xFFFFFFFF);       // White
  static const Color background = Color(0xFFF5F5F5);    // Light gray
  static const Color error = Color(0xFFD32F2F);         // Red

  // Aviation-specific colors
  static const Color vfr = Color(0xFF4CAF50);           // Green
  static const Color mvfr = Color(0xFF2196F3);          // Blue
  static const Color ifr = Color(0xFFF44336);           // Red
  static const Color lifr = Color(0xFF9C27B0);          // Purple

  // Map colors
  static const Color routeLine = Color(0xFFFF00FF);     // Magenta course line
  static const Color trackLine = Color(0xFF607D8B);     // Gray track
  static const Color airspaceClassB = Color(0xFF2196F3);
  static const Color airspaceClassC = Color(0xFF9C27B0);
  static const Color airspaceClassD = Color(0xFF03A9F4);
  static const Color airspaceRestricted = Color(0xFFF44336);

  static ThemeData get themeData => ThemeData(
    useMaterial3: true,
    brightness: Brightness.light,
    colorScheme: ColorScheme.light(
      primary: primary,
      secondary: secondary,
      surface: surface,
      error: error,
    ),
    scaffoldBackgroundColor: background,

    // AppBar
    appBarTheme: const AppBarTheme(
      backgroundColor: primary,
      foregroundColor: Colors.white,
      elevation: 2,
    ),

    // Cards
    cardTheme: CardTheme(
      color: surface,
      elevation: 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8),
      ),
    ),

    // Buttons
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: primary,
        foregroundColor: Colors.white,
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
    ),

    // Input fields
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: Colors.white,
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8),
        borderSide: const BorderSide(color: primary, width: 2),
      ),
    ),

    // Text
    textTheme: const TextTheme(
      headlineLarge: TextStyle(
        fontSize: 32,
        fontWeight: FontWeight.bold,
        color: Colors.black87,
      ),
      headlineMedium: TextStyle(
        fontSize: 24,
        fontWeight: FontWeight.bold,
        color: Colors.black87,
      ),
      titleLarge: TextStyle(
        fontSize: 20,
        fontWeight: FontWeight.w600,
        color: Colors.black87,
      ),
      titleMedium: TextStyle(
        fontSize: 16,
        fontWeight: FontWeight.w600,
        color: Colors.black87,
      ),
      bodyLarge: TextStyle(
        fontSize: 16,
        color: Colors.black87,
      ),
      bodyMedium: TextStyle(
        fontSize: 14,
        color: Colors.black87,
      ),
      bodySmall: TextStyle(
        fontSize: 12,
        color: Colors.black54,
      ),
      // Monospace for data display
      labelLarge: TextStyle(
        fontSize: 14,
        fontFamily: 'RobotoMono',
        color: Colors.black87,
      ),
    ),

    // Icons
    iconTheme: const IconThemeData(
      color: Colors.black87,
      size: 24,
    ),

    // Dividers
    dividerTheme: const DividerThemeData(
      color: Colors.black12,
      thickness: 1,
    ),

    // Chips (for flight categories, etc.)
    chipTheme: ChipThemeData(
      backgroundColor: Colors.grey.shade200,
      labelStyle: const TextStyle(color: Colors.black87),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
    ),
  );
}
