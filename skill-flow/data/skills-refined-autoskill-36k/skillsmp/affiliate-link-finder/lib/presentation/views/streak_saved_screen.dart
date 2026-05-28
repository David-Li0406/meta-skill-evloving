import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../widgets/grace_period_card.dart';
import '../navigation/app_router.dart';

class StreakSavedScreen extends StatelessWidget {
  const StreakSavedScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Force dark mode look if desired, or respect system. The wireframe has both light/dark,
    // user prompt usually implies functionality, checking prompt: "Streak Saved - ADHD Supplement Tracker"
    // The prompt HTML has `dark:bg-background-dark`. I'll support both.

    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      backgroundColor:
          isDark ? AppColors.backgroundDark : AppColors.backgroundLight,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.close),
          color: AppColors.primaryBlue,
          onPressed: () => Navigator.pushNamedAndRemoveUntil(
              context, AppRouter.dashboard, (route) => false),
        ),
        title: Text(
          'Streak Saved',
          style: TextStyle(
            color: isDark ? Colors.white : Colors.black,
            fontWeight: FontWeight.bold,
          ),
        ),
        centerTitle: true,
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.symmetric(horizontal: 24),
                child: Column(
                  children: [
                    const SizedBox(height: 24),

                    // Flame Visualization
                    Center(
                      child: Stack(
                        alignment: Alignment.bottomRight,
                        children: [
                          Container(
                            width: 256,
                            height: 256,
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              color:
                                  AppColors.primaryBlue.withValues(alpha: 0.1),
                              boxShadow: [
                                BoxShadow(
                                  color: AppColors.primaryBlue
                                      .withValues(alpha: 0.3),
                                  blurRadius: 60,
                                  spreadRadius: 10,
                                ),
                              ],
                            ),
                            child: const Center(
                              child: Icon(
                                Icons.local_fire_department,
                                size: 120,
                                color: AppColors.primaryBlue,
                              ),
                            ),
                          ),

                          // Heart Badge
                          Container(
                            margin:
                                const EdgeInsets.only(bottom: 16, right: 16),
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: AppColors.primaryBlue,
                              shape: BoxShape.circle,
                              border: Border.all(
                                color: isDark
                                    ? AppColors.backgroundDark
                                    : AppColors.backgroundLight,
                                width: 4,
                              ),
                              boxShadow: const [
                                BoxShadow(
                                  color: Colors.black26,
                                  blurRadius: 10,
                                  offset: Offset(0, 4),
                                ),
                              ],
                            ),
                            child: const Icon(
                              Icons.favorite,
                              color: Colors.white,
                              size: 32,
                            ),
                          ),
                        ],
                      ),
                    ),

                    const SizedBox(height: 48), // Spacing after flame

                    // Headline
                    Text(
                      '14 Day Streak',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: isDark ? Colors.white : Colors.black,
                        fontSize: 40,
                        fontWeight: FontWeight.bold,
                        height: 1.1,
                      ),
                    ),

                    const SizedBox(height: 8),

                    // Grace Day Label
                    const Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.auto_fix_high,
                            color: AppColors.primaryBlue, size: 20),
                        SizedBox(width: 8),
                        Text(
                          'Grace Day Applied',
                          style: TextStyle(
                            color: AppColors.primaryBlue,
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ],
                    ),

                    const SizedBox(height: 24),

                    // Body Text
                    Text(
                      "Don't sweat it! ADHD life happens. We protected your momentum so you can keep moving forward.",
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color:
                            isDark ? const Color(0xFF9DA8B9) : Colors.grey[600],
                        fontSize: 18,
                        height: 1.5,
                      ),
                    ),

                    const SizedBox(height: 40),

                    // Status Card
                    const GracePeriodCard(),

                    const SizedBox(height: 40),
                  ],
                ),
              ),
            ),

            // Bottom Button
            Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                children: [
                  SizedBox(
                    width: double.infinity,
                    height: 56,
                    child: ElevatedButton(
                      onPressed: () => Navigator.pushNamedAndRemoveUntil(
                          context, AppRouter.dashboard, (route) => false),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.primaryBlue,
                        foregroundColor: Colors.white,
                        elevation: 8,
                        shadowColor:
                            AppColors.primaryBlue.withValues(alpha: 0.25),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(16),
                        ),
                      ),
                      child: const Text(
                        'Back to Today',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    "You're doing great. One step at a time.",
                    style: TextStyle(
                      color: isDark ? Colors.grey[600] : Colors.grey[400],
                      fontSize: 12,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
