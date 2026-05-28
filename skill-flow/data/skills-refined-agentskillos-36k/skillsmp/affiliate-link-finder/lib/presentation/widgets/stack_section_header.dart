import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class StackSectionHeader extends StatelessWidget {
  final String title;
  final String? time;
  final bool isNow;

  const StackSectionHeader({
    super.key,
    required this.title,
    this.time,
    this.isNow = false,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              Text(
                title,
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.bold,
                      color: isDark ? AppColors.textPrimaryDark : AppColors.textPrimaryLight,
                    ),
              ),
              if (time == null && !isNow) ...[
                // If it's the "Evening Stack" header in the wireframe, it has a title + time on the right.
                // But the wireframe for "Morning Focus" has "Now" badge.
              ],
            ],
          ),
          if (isNow)
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
              decoration: BoxDecoration(
                color: AppColors.primary.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(999),
              ),
              child: const Text(
                'NOW',
                style: TextStyle(
                  color: AppColors.primary,
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 1.0,
                ),
              ),
            )
          else if (time != null)
            Text(
              time!,
              style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: isDark ? AppColors.textSecondaryDark : AppColors.textSecondaryLight,
                    fontWeight: FontWeight.w500,
                  ),
            ),
        ],
      ),
    );
  }
}
