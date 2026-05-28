import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class LevelBadge extends StatelessWidget {
  final int level;
  final String title;

  const LevelBadge({
    super.key,
    required this.level,
    required this.title,
  });

  @override
  Widget build(BuildContext context) {
    return Stack(
      alignment: Alignment.center,
      clipBehavior: Clip.none,
      children: [
        // Glow Effect
        Container(
          width: 250,
          height: 250,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: AppColors.primaryGold.withValues(alpha: 0.2),
          ),
        ),

        // Main Badge Container
        Container(
          width: 224, // w-56
          height: 224, // h-56
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [
                AppColors.primaryGold.withValues(alpha: 0.5),
                AppColors.primaryGold,
                AppColors.primaryGold.withValues(alpha: 0.8),
              ],
            ),
            border: Border.all(
              color: Colors.white.withValues(alpha: 0.3),
              width: 6,
            ),
            boxShadow: [
              BoxShadow(
                color: AppColors.primaryGold.withValues(alpha: 0.4),
                blurRadius: 50,
                spreadRadius: 10,
              ),
            ],
          ),
          child: Stack(
            children: [
              // Inner dashed border area (Simulated with Container for now, CustomPainter for dashes is complex)
              // Using a simple circular border with opacity as a placeholder for the dashed effect
              Positioned.fill(
                child: Container(
                  margin: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    border: Border.all(
                      color: Colors.white.withValues(alpha: 0.4),
                      width: 2,
                    ),
                  ),
                ),
              ),

              Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      'LEVEL',
                      style: Theme.of(context).textTheme.labelSmall?.copyWith(
                            color: AppColors.primaryGold.withValues(alpha: 0.8),
                            fontWeight: FontWeight.w900,
                            letterSpacing: 2.0,
                          ),
                    ),
                    Text(
                      '$level',
                      style: Theme.of(context).textTheme.displayLarge?.copyWith(
                        color: Colors.white,
                        fontSize: 96,
                        fontWeight: FontWeight.w900,
                        height: 1.0,
                        shadows: [
                          BoxShadow(
                            color: Colors.black.withValues(alpha: 0.2),
                            blurRadius: 10,
                            offset: const Offset(0, 4),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),

        // Bottom Title Pill
        Positioned(
          bottom: -16,
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withValues(alpha: 0.2),
                  blurRadius: 10,
                  offset: const Offset(0, 4),
                ),
              ],
            ),
            child: Text(
              title,
              style: const TextStyle(
                color: AppColors.textPrimaryLight,
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ),
      ],
    );
  }
}
