import 'package:flutter/material.dart';
import 'dart:math';
import '../theme/app_theme.dart';

class ParticlesBackground extends StatelessWidget {
  final Color? color;
  final int? particleCount;

  const ParticlesBackground({
    super.key,
    this.color,
    this.particleCount,
  });

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        // Sparkle 1 (Top Left)
        Positioned(
          top: MediaQuery.of(context).size.height * 0.25,
          left: MediaQuery.of(context).size.width * 0.25,
          child: _buildSparkle(4, 4),
        ),
        // Sparkle 2 (Top Right)
        Positioned(
          top: MediaQuery.of(context).size.height * 0.33,
          right: 40,
          child: _buildSparkle(8, 8),
        ),
        // Sparkle 3 (Bottom Left)
        Positioned(
          bottom: MediaQuery.of(context).size.height * 0.25,
          left: 40,
          child: _buildSparkle(6, 6),
        ),
        // Sparkle 4 (Top Right High)
        Positioned(
          top: 40,
          right: MediaQuery.of(context).size.width * 0.25,
          child: _buildSparkle(8, 8),
        ),
        // Sparkle 5 (Bottom Right)
        Positioned(
          bottom: MediaQuery.of(context).size.height * 0.33,
          right: 80,
          child: _buildSparkle(4, 4),
        ),

        // Geometric Shapes
        Positioned(
          top: 40,
          left: 40,
          child: Transform.rotate(
            angle: pi / 4,
            child: Container(
              width: 12,
              height: 12,
              color: AppColors.primaryGold.withValues(alpha: 0.6),
            ),
          ),
        ),
        Positioned(
          top: 160,
          right: 48,
          child: Transform.rotate(
            angle: 12 * pi / 180,
            child: Container(
              width: 8,
              height: 16,
              color: AppColors.primaryBlue.withValues(alpha: 0.6),
            ),
          ),
        ),
        Positioned(
          bottom: 160,
          left: 80,
          child: Transform.rotate(
            angle: 110 * pi / 180,
            child: Container(
              width: 16,
              height: 8,
              color: AppColors.primaryGold.withValues(alpha: 0.6),
            ),
          ),
        ),
        Positioned(
          top: MediaQuery.of(context).size.height * 0.5,
          right: 16,
          child: Container(
            width: 12,
            height: 12,
            decoration: BoxDecoration(
              color: AppColors.primaryGold.withValues(alpha: 0.6),
              shape: BoxShape.circle,
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildSparkle(double width, double height) {
    return Container(
      width: width,
      height: height,
      decoration: BoxDecoration(
        color: (color ?? Colors.white).withValues(alpha: 0.6),
        shape: BoxShape.circle,
      ),
    );
  }
}
