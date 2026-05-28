import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppColors {
  // Brand Gold Palette (Premium Path)
  static const Color primaryGold = Color(0xFFD4A411);
  static const Color backgroundPremiumDark = Color(0xFF221D10);
  static const Color backgroundPremiumLight = Color(0xFFF8F8F6);

  // Legacy/Utility Blue Palette
  static const Color primaryBlue = Color(0xFF136DEC);
  static const Color backgroundUtilityLight = Color(0xFFF6F7F8);
  static const Color backgroundUtilityDark = Color(0xFF101822);

  // Defaults (Currently mapping to Gold/Premium as per wireframes)
  static const Color primary = primaryGold;
  static const Color backgroundLight = backgroundPremiumLight;
  static const Color backgroundDark = backgroundPremiumDark;

  static const Color secondary = Color(0xFF64748B);
  static const Color cardDark =
      Color(0xFF2D2616); // Adjusted for Dark Brown theme
  static const Color cardLight = Color(0xFFFFFFFF);

  // Text Colors
  static const Color textPrimaryLight = Color(0xFF181611); // Darker brown-black
  static const Color textPrimaryDark = Color(0xFFFFFFFF);
  static const Color textSecondaryLight = Color(0xFF64748B);
  static const Color textSecondaryDark = Color(0xFF94A3B8);

  // Accents
  static const Color accentGreen = Color(0xFF0BDA1D);
  static const Color warningAmber = Color(0xFFFFC107);

  // Semantic Tokens
  static Color cardBackground(bool isDark) =>
      isDark ? const Color(0xFF2D2616) : Colors.white;
  static Color borderColor(bool isDark) =>
      isDark ? Colors.white.withValues(alpha: 0.05) : const Color(0xFFE2E8F0);
  static Color dividerColor(bool isDark) =>
      isDark ? Colors.white.withValues(alpha: 0.1) : const Color(0xFFF1F5F9);
  static Color textTertiary(bool isDark) => isDark
      ? const Color(0xFF94A3B8).withValues(alpha: 0.7)
      : Colors.grey[500]!;
}

class AppTheme {
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      scaffoldBackgroundColor: AppColors.backgroundLight,
      colorScheme: const ColorScheme.light(
        primary: AppColors.primary,
        surface: AppColors.cardLight,
        onSurface: AppColors.textPrimaryLight,
        secondary: AppColors.secondary,
      ),
      textTheme: GoogleFonts.lexendTextTheme().apply(
        bodyColor: AppColors.textPrimaryLight,
        displayColor: AppColors.textPrimaryLight,
      ),
      dividerTheme: DividerThemeData(
        color: AppColors.dividerColor(false),
        thickness: 1,
      ),
      cardTheme: CardThemeData(
        color: AppColors.cardBackground(false),
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: BorderSide(color: AppColors.borderColor(false)),
        ),
      ),
    );
  }

  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      scaffoldBackgroundColor: AppColors.backgroundDark,
      colorScheme: const ColorScheme.dark(
        primary: AppColors.primary,
        surface: AppColors.cardDark,
        onSurface: AppColors.textPrimaryDark,
        secondary: AppColors.secondary,
      ),
      textTheme: GoogleFonts.lexendTextTheme().apply(
        bodyColor: AppColors.textPrimaryDark,
        displayColor: AppColors.textPrimaryDark,
      ),
      dividerTheme: DividerThemeData(
        color: AppColors.dividerColor(true),
        thickness: 1,
      ),
      cardTheme: CardThemeData(
        color: AppColors.cardBackground(true),
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
          side: BorderSide(color: AppColors.borderColor(true)),
        ),
      ),
    );
  }
}
