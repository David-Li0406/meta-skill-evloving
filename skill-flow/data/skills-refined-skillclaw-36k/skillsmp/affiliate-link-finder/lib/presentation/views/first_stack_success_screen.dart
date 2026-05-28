import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/app_theme.dart';
import '../navigation/app_router.dart';

class FirstStackSuccessScreen extends StatelessWidget {
  const FirstStackSuccessScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    const primaryGold = AppColors.primaryGold;

    return Scaffold(
      backgroundColor:
          isDark ? AppColors.backgroundPremiumDark : AppColors.backgroundLight,
      appBar: AppBar(
        backgroundColor: isDark
            ? AppColors.backgroundPremiumDark
            : AppColors.backgroundLight,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: primaryGold),
          onPressed: () => Navigator.pop(context),
        ),
        centerTitle: true,
        title: Text(
          'SUCCESS',
          style: GoogleFonts.lexend(
            color: primaryGold.withValues(alpha: 0.8),
            fontSize: 14,
            fontWeight: FontWeight.bold,
            letterSpacing: 2.0,
          ),
        ),
      ),
      body: Column(
        children: [
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Column(
                children: [
                  const SizedBox(height: 16),

                  // Hero Illustration (Bottle on Shelf)
                  SizedBox(
                    height: 320,
                    child: Stack(
                      alignment: Alignment.center,
                      children: [
                        // Confetti Decorations
                        Positioned(
                          top: 40,
                          left: 40,
                          child: Icon(Icons.celebration,
                              color: primaryGold.withValues(alpha: 0.4),
                              size: 32),
                        ),
                        Positioned(
                          top: 80,
                          right: 48,
                          child: Icon(Icons.star,
                              color: primaryGold.withValues(alpha: 0.6),
                              size: 24),
                        ),
                        Positioned(
                          bottom: 80,
                          left: 60,
                          child: Icon(Icons.favorite,
                              color: primaryGold.withValues(alpha: 0.3),
                              size: 28),
                        ),

                        // Glow
                        Container(
                          width: 200,
                          height: 200,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            color: primaryGold.withValues(alpha: 0.2),
                          ),
                        ),

                        // Shelf Card
                        Container(
                          width: double.infinity,
                          constraints: const BoxConstraints(maxWidth: 320),
                          padding: const EdgeInsets.all(32),
                          decoration: BoxDecoration(
                            color: isDark
                                ? AppColors.backgroundPremiumDark
                                    .withValues(alpha: 0.5)
                                : Colors.white,
                            borderRadius: BorderRadius.circular(24),
                            border: Border.all(
                              color: primaryGold.withValues(alpha: 0.1),
                            ),
                            boxShadow: [
                              BoxShadow(
                                color: primaryGold.withValues(alpha: 0.05),
                                blurRadius: 20,
                                offset: const Offset(0, 10),
                              ),
                            ],
                          ),
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              // Bottle
                              Container(
                                width: 128,
                                height: 176,
                                decoration: BoxDecoration(
                                  borderRadius: BorderRadius.circular(16),
                                  gradient: const LinearGradient(
                                    begin: Alignment.topCenter,
                                    end: Alignment.bottomCenter,
                                    colors: [
                                      AppColors.primaryGold,
                                      Color(0xFFB38A0E),
                                    ],
                                  ),
                                  boxShadow: [
                                    BoxShadow(
                                      color:
                                          Colors.black.withValues(alpha: 0.2),
                                      blurRadius: 10,
                                      offset: const Offset(0, 4),
                                    ),
                                  ],
                                ),
                                child: Stack(
                                  children: [
                                    // Shine
                                    Positioned(
                                      right: -16,
                                      top: 0,
                                      bottom: 0,
                                      width: 32,
                                      child: Container(
                                        color:
                                            Colors.white.withValues(alpha: 0.2),
                                      ),
                                    ),
                                    // Label
                                    Column(
                                      children: [
                                        Container(
                                          width: double.infinity,
                                          padding: const EdgeInsets.symmetric(
                                              vertical: 8),
                                          color: Colors.white
                                              .withValues(alpha: 0.9),
                                          child: Column(
                                            children: [
                                              Text(
                                                'MORNING FOCUS',
                                                style: GoogleFonts.lexend(
                                                  fontSize: 10,
                                                  fontWeight: FontWeight.bold,
                                                  color: AppColors.primaryGold,
                                                  letterSpacing: 0.5,
                                                ),
                                              ),
                                              const SizedBox(height: 4),
                                              Container(
                                                width: 32,
                                                height: 2,
                                                color: AppColors.primaryGold
                                                    .withValues(alpha: 0.4),
                                              ),
                                            ],
                                          ),
                                        ),
                                        Expanded(
                                          child: Center(
                                            child: Icon(
                                              Icons.wb_sunny,
                                              color: Colors.white
                                                  .withValues(alpha: 0.9),
                                              size: 48,
                                            ),
                                          ),
                                        ),
                                      ],
                                    ),
                                  ],
                                ),
                              ),
                              const SizedBox(height: 16),
                              // Shelf Base
                              Container(
                                width: 160,
                                height: 12,
                                decoration: BoxDecoration(
                                  color: isDark
                                      ? const Color(0xFF332C1A)
                                      : const Color(0xFFE5E5E0),
                                  borderRadius: BorderRadius.circular(999),
                                ),
                              ),
                              const SizedBox(height: 16),
                              Text(
                                'ADDED TO SHELF',
                                style: GoogleFonts.lexend(
                                  fontSize: 12,
                                  fontWeight: FontWeight.w500,
                                  color: primaryGold.withValues(alpha: 0.8),
                                  letterSpacing: 2.0,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),

                  const SizedBox(height: 24),

                  // Headline
                  Text(
                    'Your First Stack is Ready!',
                    textAlign: TextAlign.center,
                    style: GoogleFonts.lexend(
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                      color: isDark ? Colors.white : const Color(0xFF181611),
                      height: 1.1,
                    ),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    "You've taken the first step toward a clearer mind and a more focused day.",
                    textAlign: TextAlign.center,
                    style: GoogleFonts.lexend(
                      fontSize: 16,
                      color: isDark
                          ? Colors.white.withValues(alpha: 0.7)
                          : const Color(0xFF181611).withValues(alpha: 0.7),
                      height: 1.5,
                    ),
                  ),

                  const SizedBox(height: 32),

                  // Goal Badge
                  Container(
                    padding: const EdgeInsets.symmetric(
                        horizontal: 24, vertical: 12),
                    decoration: BoxDecoration(
                      color: primaryGold.withValues(alpha: 0.1),
                      borderRadius: BorderRadius.circular(999),
                      border: Border.all(
                        color: primaryGold.withValues(alpha: 0.2),
                      ),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Container(
                          width: 40,
                          height: 40,
                          decoration: const BoxDecoration(
                            color: primaryGold,
                            shape: BoxShape.circle,
                          ),
                          child: const Icon(Icons.bolt, color: Colors.white),
                        ),
                        const SizedBox(width: 16),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'GOAL SET',
                              style: GoogleFonts.lexend(
                                fontSize: 10,
                                fontWeight: FontWeight.bold,
                                color: primaryGold,
                                letterSpacing: 1.5,
                              ),
                            ),
                            Text(
                              '7 Day Streak',
                              style: GoogleFonts.lexend(
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                                color: isDark
                                    ? Colors.white
                                    : const Color(0xFF181611),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),

          // Footer Actions
          Container(
            padding: const EdgeInsets.fromLTRB(24, 24, 24, 40),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.bottomCenter,
                end: Alignment.topCenter,
                colors: [
                  isDark
                      ? AppColors.backgroundPremiumDark
                      : AppColors.backgroundLight,
                  (isDark
                          ? AppColors.backgroundPremiumDark
                          : AppColors.backgroundLight)
                      .withValues(alpha: 0),
                ],
              ),
            ),
            child: Column(
              children: [
                SizedBox(
                  width: double.infinity,
                  height: 56,
                  child: ElevatedButton.icon(
                    onPressed: () {
                      Navigator.pushNamed(context, AppRouter.reminders);
                    },
                    icon: const Icon(Icons.notifications_active),
                    label: const Text('Schedule My First Nudge'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: primaryGold,
                      foregroundColor: Colors.white,
                      textStyle: GoogleFonts.lexend(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                      ),
                      elevation: 8,
                      shadowColor: primaryGold.withValues(alpha: 0.3),
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                TextButton(
                  onPressed: () {
                    Navigator.pushNamedAndRemoveUntil(
                        context, AppRouter.dashboard, (route) => false);
                  },
                  child: Text(
                    'Not now, show my dashboard',
                    style: GoogleFonts.lexend(
                      fontSize: 14,
                      fontWeight: FontWeight.w500,
                      color: isDark
                          ? Colors.white.withValues(alpha: 0.5)
                          : const Color(0xFF181611).withValues(alpha: 0.5),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
