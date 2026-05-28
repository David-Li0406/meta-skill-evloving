import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import 'package:google_fonts/google_fonts.dart';

class FocusComparisonChart extends StatelessWidget {
  const FocusComparisonChart({super.key});

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: Text(
            'Focus Comparison',
            style: GoogleFonts.lexend(
              color: isDark ? Colors.white : const Color(0xFF0F172A),
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
        Padding(
          padding: const EdgeInsets.all(16),
          child: Container(
            padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(
              color: isDark ? const Color(0xFF1C2027) : Colors.white,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(
                color: isDark ? Colors.grey[800]! : Colors.grey[200]!,
              ),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withValues(alpha: 0.05),
                  blurRadius: 4,
                  offset: const Offset(0, 2),
                ),
              ],
            ),
            child: Column(
              children: [
                SizedBox(
                  height: 140,
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      // Last Week Bar
                      _buildBar(context,
                          label: 'LAST WEEK',
                          score: 72,
                          heightFactor: 0.65,
                          isCurrent: false,
                          isDark: isDark),

                      // This Week Bar
                      _buildBar(context,
                          label: 'THIS WEEK',
                          score: 83,
                          heightFactor: 0.85,
                          isCurrent: true,
                          isDark: isDark),
                    ],
                  ),
                ),

                // Divider
                Padding(
                  padding: const EdgeInsets.symmetric(vertical: 24),
                  child: Divider(
                      color: isDark ? Colors.white10 : Colors.grey[100]),
                ),

                // Footer Stats
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Peak Productivity',
                          style: GoogleFonts.lexend(
                            color: isDark ? Colors.grey[400] : Colors.grey[500],
                            fontSize: 12,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          'Thu @ 10:00 AM',
                          style: GoogleFonts.lexend(
                            color:
                                isDark ? Colors.white : const Color(0xFF0F172A),
                            fontSize: 14,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        Text(
                          'Weekly Score',
                          style: GoogleFonts.lexend(
                            color: isDark ? Colors.grey[400] : Colors.grey[500],
                            fontSize: 12,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Row(
                          children: [
                            const Icon(Icons.arrow_upward,
                                color: AppColors.accentGreen, size: 14),
                            const SizedBox(width: 4),
                            Text(
                              '83/100',
                              style: GoogleFonts.lexend(
                                color: AppColors.accentGreen,
                                fontSize: 14,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildBar(BuildContext context,
      {required String label,
      required int score,
      required double heightFactor,
      required bool isCurrent,
      required bool isDark}) {
    return Expanded(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          // Bar Container
          SizedBox(
            height: 100, // Fixed height area for bars
            child: Stack(
              alignment: Alignment.bottomCenter,
              children: [
                FractionallySizedBox(
                  heightFactor: heightFactor,
                  child: Container(
                    width: 60,
                    decoration: BoxDecoration(
                      color: isCurrent
                          ? AppColors.primary
                          : (isDark ? Colors.grey[700] : Colors.grey[300]),
                      borderRadius:
                          const BorderRadius.vertical(top: Radius.circular(8)),
                      boxShadow: isCurrent
                          ? [
                              BoxShadow(
                                color: AppColors.primary.withValues(alpha: 0.3),
                                blurRadius: 15,
                                spreadRadius: -2,
                                offset: const Offset(0, 0),
                              ),
                            ]
                          : null,
                    ),
                  ),
                ),
                Positioned(
                  top: (100 * (1 - heightFactor)) -
                      25, // Calculate roughly based on height
                  child: Text(
                    score.toString(),
                    style: GoogleFonts.lexend(
                      color: isCurrent
                          ? AppColors.primary
                          : (isDark ? Colors.grey[500] : Colors.grey[500]),
                      fontSize: 14,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 12),
          Text(
            label,
            style: GoogleFonts.lexend(
              color: isCurrent
                  ? AppColors.primary
                  : (isDark ? Colors.grey[500] : Colors.grey[500]),
              fontSize: 10,
              fontWeight: FontWeight.bold,
              letterSpacing: 0.5,
            ),
          ),
        ],
      ),
    );
  }
}
