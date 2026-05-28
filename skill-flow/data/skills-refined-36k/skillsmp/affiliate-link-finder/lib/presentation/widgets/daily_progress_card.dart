import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class DailyProgressCard extends StatelessWidget {
  final int streakCount;
  final double progress; // 0.0 to 1.0
  final bool isDark;

  const DailyProgressCard({
    super.key,
    required this.streakCount,
    required this.progress,
    required this.isDark,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF1A1F2E) : Colors.white,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(
          color: isDark
              ? Colors.white.withValues(alpha: 0.05)
              : Colors.grey.withValues(alpha: 0.1),
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Daily Completion',
            style: TextStyle(
              color: Colors.grey,
              fontSize: 14,
              fontWeight: FontWeight.w500,
            ),
          ),
          const SizedBox(height: 12),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              // Streak
              Expanded(
                child: Row(
                  children: [
                    const Text(
                      "You're on a ",
                      style: TextStyle(fontSize: 16),
                    ),
                    Flexible(
                      child: Text(
                        "$streakCount-day streak!",
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    const SizedBox(width: 4),
                    const Text("🔥", style: TextStyle(fontSize: 16)),
                  ],
                ),
              ),
              const SizedBox(width: 8),

              // Percentage
              Text(
                "${(progress * 100).round()}%",
                style: const TextStyle(
                  color: AppColors.primaryGold, // Gold
                  fontSize: 32,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),

          // Progress Bar
          Stack(
            children: [
              // Background
              Container(
                height: 12,
                width: double.infinity,
                decoration: BoxDecoration(
                  color: isDark
                      ? Colors.white.withValues(alpha: 0.1)
                      : Colors.grey[200],
                  borderRadius: BorderRadius.circular(6),
                ),
              ),
              // Fill
              LayoutBuilder(
                builder: (context, constraints) {
                  return Container(
                    height: 12,
                    width: constraints.maxWidth * progress,
                    decoration: BoxDecoration(
                      gradient: const LinearGradient(
                        colors: [AppColors.primaryGold, Color(0xFFFFD54F)],
                      ),
                      borderRadius: BorderRadius.circular(6),
                    ),
                  );
                },
              ),
            ],
          ),
          const SizedBox(height: 8),
          const Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text("0%", style: TextStyle(color: Colors.grey, fontSize: 10)),
              Text("50%", style: TextStyle(color: Colors.grey, fontSize: 10)),
              Text("100%", style: TextStyle(color: Colors.grey, fontSize: 10)),
            ],
          ),
        ],
      ),
    );
  }
}
