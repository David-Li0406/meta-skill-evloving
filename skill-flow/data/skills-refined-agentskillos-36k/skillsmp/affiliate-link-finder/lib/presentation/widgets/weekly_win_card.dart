import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:cached_network_image/cached_network_image.dart';

class WeeklyWinCard extends StatelessWidget {
  final int streakDays;
  final double focusImprovement;

  const WeeklyWinCard({
    super.key,
    required this.streakDays,
    required this.focusImprovement,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Container(
      clipBehavior: Clip.antiAlias,
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF1C2027) : Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: isDark ? 0.3 : 0.1),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
        border: Border.all(
          color: AppColors.primary.withValues(alpha: 0.2),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Hero Image
          Container(
            height: 180,
            decoration: const BoxDecoration(
              image: DecorationImage(
                image: CachedNetworkImageProvider(
                    'https://lh3.googleusercontent.com/aida-public/AB6AXuBVHwiwS1N_25BZq-s9mst15_yTJ3Q5L6iPXcYO0Bu_OIvXgxn8kQO59NMvTSavE0lfm6LvA2feUBmgEDKZ1K9ZAatHyNEMo0gZ8f1gwDHFZ_srI1vgF8EDij1FH72nHK58LCPl4Uwav0gFLXyx21fN6_G92_1AJAoZ2UqPVEZdyW7qbRoFhqZJvy0RnYxXKsJecug_KFQy5CSzNqvcHtekORwj3IXyN50ors8BcKTtvDx6UZvEh9YDWNnw925k7Gc_0drgYIdA_hM'),
                fit: BoxFit.cover,
              ),
            ),
            child: Stack(
              children: [
                Positioned.fill(
                  child: Container(
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        begin: Alignment.bottomCenter,
                        end: Alignment.topCenter,
                        colors: [
                          (isDark ? const Color(0xFF1C2027) : Colors.white)
                              .withValues(alpha: 0.8),
                          Colors.transparent,
                        ],
                      ),
                    ),
                  ),
                ),
                Positioned(
                  bottom: 16,
                  left: 16,
                  child: Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                    decoration: BoxDecoration(
                      color: AppColors.primary,
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Text(
                      'CHAMPION',
                      style: GoogleFonts.lexend(
                        color: Colors.white,
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                        letterSpacing: 1.0,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),

          // Content
          Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(
                    height:
                        8), // Assuming previous const was okay or not related to Text
                Text(
                  'WEEKLY WIN',
                  style: GoogleFonts.lexend(
                    color: AppColors.primary,
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1.5,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  '$streakDays Day Streak!',
                  style: GoogleFonts.lexend(
                    color: isDark ? Colors.white : const Color(0xFF0F172A),
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    letterSpacing: -0.5,
                  ),
                ),
                const SizedBox(height: 12),
                RichText(
                  text: TextSpan(
                    style: GoogleFonts.lexend(
                      color:
                          isDark ? Colors.grey[400] : const Color(0xFF64748B),
                      fontSize: 16,
                      height: 1.5,
                      // fontFamily: 'Lexend', // Removed invalid arg
                    ),
                    children: [
                      const TextSpan(
                          text:
                              "You've been incredibly consistent this week. Your average focus levels are up by "),
                      TextSpan(
                        text: "${focusImprovement.toStringAsFixed(0)}%",
                        style: const TextStyle(
                          color: AppColors.accentGreen,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const TextSpan(text: " compared to last week."),
                    ],
                  ),
                ),
                const SizedBox(height: 16),
                Row(
                  children: [
                    const Icon(Icons.trending_up,
                        color: AppColors.primary, size: 16),
                    const SizedBox(width: 8),
                    Text(
                      'Keep this momentum going!',
                      style: GoogleFonts.lexend(
                        color: AppColors.primary,
                        fontSize: 14,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
