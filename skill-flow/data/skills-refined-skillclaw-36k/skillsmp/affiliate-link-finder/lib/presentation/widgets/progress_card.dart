import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class ProgressCard extends StatelessWidget {
  final double progress; // 0.0 to 1.0
  final int streakDays;

  const ProgressCard({
    super.key,
    required this.progress,
    required this.streakDays,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: const BoxDecoration(
        color: Colors.transparent, // Background handled by parent or transparent
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Daily Completion',
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    "You're on a $streakDays-day streak! 🔥",
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          color: Theme.of(context).brightness == Brightness.dark
                              ? AppColors.textSecondaryDark
                              : AppColors.textSecondaryLight,
                        ),
                  ),
                ],
              ),
              Text(
                '${(progress * 100).toInt()}%',
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      color: AppColors.primary,
                      fontWeight: FontWeight.bold,
                    ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          // Progress Bar
          Stack(
            children: [
              Container(
                height: 16,
                width: double.infinity,
                decoration: BoxDecoration(
                  color: Theme.of(context).brightness == Brightness.dark
                      ? Colors.grey[800]
                      : Colors.grey[200],
                  borderRadius: BorderRadius.circular(999),
                ),
              ),
              LayoutBuilder(
                builder: (context, constraints) {
                  return Container(
                    height: 16,
                    width: constraints.maxWidth * progress,
                    decoration: BoxDecoration(
                      color: AppColors.primary,
                      borderRadius: BorderRadius.circular(999),
                    ),
                  );
                },
              ),
              // Stripes overlay (simplified implementation using a repeating gradient shader or just opacity)
              // For simplicity and performance, we can skip complex shader for now or use a simple gradient
              Positioned.fill(
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(999),
                  child: Container(
                    width: double.infinity,
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                        colors: [
                          Colors.white.withValues(alpha: 0.15),
                          Colors.transparent,
                        ],
                        stops: const [0.0, 0.5],
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              _buildLabel(context, '0%'),
              _buildLabel(context, '50%'),
              _buildLabel(context, '100%'),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildLabel(BuildContext context, String text) {
    return Text(
      text,
      style: Theme.of(context).textTheme.labelSmall?.copyWith(
            color: Theme.of(context).brightness == Brightness.dark
                ? AppColors.textSecondaryDark
                : AppColors.textSecondaryLight,
            fontWeight: FontWeight.w500,
          ),
    );
  }
}
