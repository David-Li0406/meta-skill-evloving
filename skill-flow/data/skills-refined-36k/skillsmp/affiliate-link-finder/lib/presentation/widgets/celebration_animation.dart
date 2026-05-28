import 'dart:math';
import 'package:flutter/material.dart';
import '../../application/view_models/theme_view_model.dart';
import 'package:provider/provider.dart';

/// Celebration animation that plays when a supplement is marked as taken
class CelebrationAnimation extends StatefulWidget {
  final VoidCallback onComplete;

  const CelebrationAnimation({
    super.key,
    required this.onComplete,
  });

  @override
  State<CelebrationAnimation> createState() => _CelebrationAnimationState();
}

class _CelebrationAnimationState extends State<CelebrationAnimation>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  final List<_Particle> _particles = [];
  final Random _random = Random();

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    );

    // Check for reduced motion
    final settingsRepo = Provider.of<ThemeViewModel>(context, listen: false);
    final reduceMotion = settingsRepo.reducedMotion;
    // Also check system setting (this might need to happen in build or verify here)
    // Accessing mediaQuery in initState is unsafe unless we wait for post-frame,
    // but celebration usually happens on user action.

    if (reduceMotion) {
      // Don't animate, just complete immediately
      WidgetsBinding.instance.addPostFrameCallback((_) {
        widget.onComplete();
      });
      return;
    }

    // Generate particles
    for (int i = 0; i < 50; i++) {
      _particles.add(_Particle(
        color: _getRandomColor(),
        startX: 0.5,
        startY: 0.5,
        velocityX: (_random.nextDouble() - 0.5) * 2,
        velocityY: -_random.nextDouble() * 2 - 1,
        size: _random.nextDouble() * 12 + 6,
      ));
    }

    _controller.forward().then((_) {
      if (mounted) widget.onComplete();
    });
  }

  Color _getRandomColor() {
    final colors = [
      const Color(0xFFFFD700), // Gold
      const Color(0xFF4CAF50), // Green
      const Color(0xFF2196F3), // Blue
      const Color(0xFFFF9800), // Orange
      const Color(0xFFE91E63), // Pink
      const Color(0xFF9C27B0), // Purple
    ];
    return colors[_random.nextInt(colors.length)];
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return CustomPaint(
          painter: _ParticlePainter(
            particles: _particles,
            progress: _controller.value,
          ),
          size: Size.infinite,
        );
      },
    );
  }
}

class _Particle {
  final Color color;
  final double startX;
  final double startY;
  final double velocityX;
  final double velocityY;
  final double size;

  _Particle({
    required this.color,
    required this.startX,
    required this.startY,
    required this.velocityX,
    required this.velocityY,
    required this.size,
  });
}

class _ParticlePainter extends CustomPainter {
  final List<_Particle> particles;
  final double progress;

  _ParticlePainter({
    required this.particles,
    required this.progress,
  });

  @override
  void paint(Canvas canvas, Size size) {
    for (final particle in particles) {
      final x = size.width * particle.startX +
          particle.velocityX * size.width * progress;
      final y = size.height * particle.startY +
          particle.velocityY * size.height * progress +
          0.5 * 9.8 * progress * progress * size.height * 0.5; // Gravity

      final opacity = (1 - progress).clamp(0.0, 1.0);
      final paint = Paint()
        ..color = particle.color.withValues(alpha: opacity)
        ..style = PaintingStyle.fill;

      canvas.drawCircle(
        Offset(x, y),
        particle.size * (1 - progress * 0.5),
        paint,
      );
    }
  }

  @override
  bool shouldRepaint(_ParticlePainter oldDelegate) => true;
}
