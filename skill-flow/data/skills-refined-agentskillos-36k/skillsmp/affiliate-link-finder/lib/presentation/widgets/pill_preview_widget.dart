import 'package:flutter/material.dart';

enum PillShape { round, capsule, oval }
enum PillTexture { solid, clear, pearl }

class PillPreviewWidget extends StatelessWidget {
  final PillShape shape;
  final Color color;
  final PillTexture texture;

  const PillPreviewWidget({
    super.key,
    required this.shape,
    required this.color,
    required this.texture,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Container(
        width: _getWidth(),
        height: _getHeight(),
        decoration: BoxDecoration(
          color: _getEffectiveColor(),
          shape: shape == PillShape.round ? BoxShape.circle : BoxShape.rectangle,
          borderRadius: shape == PillShape.round ? null : _getBorderRadius(),
          border: texture == PillTexture.clear 
              ? Border.all(color: Colors.white.withValues(alpha: 0.5), width: 1.5)
              : null,
          gradient: texture == PillTexture.pearl
              ? LinearGradient(
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  colors: [
                    color.withValues(alpha: 0.8),
                    color,
                    Colors.white.withValues(alpha: 0.8), // Highlight for pearl
                    color,
                  ],
                  stops: const [0.0, 0.4, 0.5, 1.0],
                )
              : null,
          boxShadow: [
            BoxShadow(
              color: color.withValues(alpha: texture == PillTexture.clear ? 0.2 : 0.6),
              blurRadius: 20,
              offset: const Offset(0, 10),
            ),
            // Reflection/Shine for 3D effect
            if (texture != PillTexture.clear)
            BoxShadow(
              color: Colors.white.withValues(alpha: 0.3),
              blurRadius: 2,
              offset: const Offset(-2, -2),
              spreadRadius: 0,
            ),
          ],
        ),
        // Inner "shine" or details
        child: ClipRRect(
          borderRadius: shape == PillShape.round 
            ? BorderRadius.circular(100) 
            : (_getBorderRadius() ?? BorderRadius.zero),
          child: Stack(
            children: [
               // Top highlight simulated
               Positioned(
                 top: 5,
                 left: 10,
                 right: 10,
                 height: _getHeight() / 2,
                 child: Container(
                   decoration: BoxDecoration(
                     gradient: LinearGradient(
                       begin: Alignment.topCenter,
                       end: Alignment.bottomCenter,
                       colors: [
                         Colors.white.withValues(alpha: texture == PillTexture.clear ? 0.4 : 0.2),
                         Colors.transparent,
                       ],
                     ),
                     borderRadius: BorderRadius.circular(50),
                   ),
                 ),
               ),
               
               // For capsule/two-tone simulation if we wanted (keeping it single color for now based on options)
            ],
          ),
        ),
      ),
    );
  }

  Color _getEffectiveColor() {
    if (texture == PillTexture.clear) {
      return color.withValues(alpha: 0.2); // Translucent
    }
    return color;
  }

  double _getWidth() {
    switch (shape) {
      case PillShape.round: return 120;
      case PillShape.capsule: return 160;
      case PillShape.oval: return 160;
    }
  }

  double _getHeight() {
    switch (shape) {
      case PillShape.round: return 120;
      case PillShape.capsule: return 70; // Thinner
      case PillShape.oval: return 100; // Thicker than capsule
    }
  }

  BorderRadius? _getBorderRadius() {
    switch (shape) {
      case PillShape.round: return null;
      case PillShape.capsule: return BorderRadius.circular(100);
      case PillShape.oval: return const BorderRadius.all(Radius.elliptical(160, 100)); // Oval-ish
    }
  }
}
