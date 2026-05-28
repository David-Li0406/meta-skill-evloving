import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../widgets/recovery_header_card.dart';
import '../widgets/weekly_overview_timeline.dart';
import '../navigation/app_router.dart';

class StreakRecoveryScreen extends StatelessWidget {
  const StreakRecoveryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      backgroundColor:
          isDark ? AppColors.backgroundPremiumDark : AppColors.backgroundLight,
      body: SafeArea(
        child: Column(
          children: [
            // Header
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  IconButton(
                    icon: const Icon(Icons.close),
                    color: isDark ? Colors.grey[400] : Colors.grey[600],
                    onPressed: () => Navigator.pushNamedAndRemoveUntil(
                        context, AppRouter.dashboard, (route) => false),
                  ),
                  Text(
                    'Rest & Recharge',
                    style: TextStyle(
                      color: isDark ? Colors.white : Colors.black,
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(width: 48), // Spacer
                ],
              ),
            ),

            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.symmetric(horizontal: 24),
                child: Column(
                  children: [
                    const RecoveryHeaderCard(),

                    const SizedBox(height: 24),

                    Text(
                      "Life happens! You're still on your journey.",
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: isDark ? Colors.white : Colors.black,
                        fontSize: 32,
                        fontWeight: FontWeight.bold,
                        height: 1.1,
                      ),
                    ),

                    const SizedBox(height: 12),

                    Text(
                      "Your journey isn't a straight line, and that's okay. You didn't lose progress; you just took a breath. Your routine is waiting whenever you're ready.",
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: isDark ? Colors.grey[400] : Colors.grey[600],
                        fontSize: 16,
                        height: 1.5,
                      ),
                    ),

                    const SizedBox(height: 32),

                    // Stats Row
                    Row(
                      children: [
                        Expanded(
                          child: _buildStatCard(
                            context,
                            'Total Days Mindful',
                            '42',
                            isProtected: true,
                          ),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          child: _buildStatCard(
                            context,
                            "Today's Focus",
                            'Morning Stack',
                            subtext: '3 supplements',
                          ),
                        ),
                      ],
                    ),

                    const SizedBox(height: 32),

                    const WeeklyOverviewTimeline(),

                    const SizedBox(height: 32),

                    // Actions
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton.icon(
                        onPressed: () => Navigator.pushNamedAndRemoveUntil(
                            context, AppRouter.dashboard, (route) => false),
                        icon: const Icon(Icons.bolt),
                        label: const Text('Jump Back In'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppColors.primaryGold,
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(vertical: 16),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(16),
                          ),
                          elevation: 8,
                          shadowColor:
                              AppColors.primaryGold.withValues(alpha: 0.2),
                          textStyle: const TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),

                    const SizedBox(height: 12),

                    SizedBox(
                      width: double.infinity,
                      child: OutlinedButton(
                        onPressed: () => Navigator.pushNamedAndRemoveUntil(
                            context, AppRouter.dashboard, (route) => false),
                        style: OutlinedButton.styleFrom(
                          side: BorderSide(
                            color:
                                isDark ? Colors.grey[700]! : Colors.grey[300]!,
                            width: 2,
                          ),
                          foregroundColor:
                              isDark ? Colors.grey[300] : Colors.grey[700],
                          padding: const EdgeInsets.symmetric(vertical: 16),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(16),
                          ),
                          textStyle: const TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                        child: const Text('Quick Check-in Only'),
                      ),
                    ),

                    const SizedBox(height: 48),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatCard(BuildContext context, String label, String value,
      {bool isProtected = false, String? subtext}) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: isDark
            ? AppColors.primaryGold.withValues(alpha: 0.1)
            : Colors.grey[100],
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isDark
              ? AppColors.primaryGold.withValues(alpha: 0.2)
              : Colors.grey[200]!,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label,
            style: TextStyle(
              color: isDark ? Colors.grey[400] : Colors.grey[600],
              fontSize: 14,
              fontWeight: FontWeight.w500,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            value,
            style: TextStyle(
              color: isDark ? Colors.white : Colors.black,
              fontSize: isProtected
                  ? 32
                  : 24, // Slight adjustment for "Morning Stack" length
              fontWeight: FontWeight.bold,
              height: 1.1,
            ),
          ),
          const SizedBox(height: 4),
          if (isProtected)
            const Row(
              children: [
                Icon(Icons.trending_up, color: Color(0xFF0BDA16), size: 14),
                SizedBox(width: 4),
                Text(
                  'STREAK PROTECTED',
                  style: TextStyle(
                    color: Color(0xFF0BDA16),
                    fontSize: 10,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          if (subtext != null)
            Text(
              subtext,
              style: const TextStyle(
                color: AppColors.primaryGold,
                fontSize: 12,
                fontWeight: FontWeight.w500,
              ),
            ),
        ],
      ),
    );
  }
}
