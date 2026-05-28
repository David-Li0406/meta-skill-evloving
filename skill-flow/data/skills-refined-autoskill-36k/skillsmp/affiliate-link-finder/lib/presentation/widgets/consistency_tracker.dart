import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import 'package:google_fonts/google_fonts.dart';

class ConsistencyTracker extends StatelessWidget {
  final Map<String, int>
      consistencyMap; // Day -> Status (0:Missed, 1:Complete, 2:Grace)

  const ConsistencyTracker({
    super.key,
    required this.consistencyMap,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: Text(
            'Consistency Tracker',
            style: GoogleFonts.lexend(
              color: isDark ? Colors.white : const Color(0xFF0F172A),
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
        SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          child: Row(
            children: days.map((day) {
              final status = consistencyMap[day] ?? 0;
              final isComplete = status == 1;
              final isGrace = status == 2;

              return Padding(
                padding: const EdgeInsets.only(right: 12),
                child: _buildDayItem(context, day, isComplete, isGrace),
              );
            }).toList(),
          ),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: Row(
            children: [
              const Icon(Icons.favorite, color: AppColors.primary, size: 16),
              const SizedBox(width: 8),
              Expanded(
                child: Text(
                  'Grace Days help keep the streak alive when you need a break.',
                  style: GoogleFonts.lexend(
                    color: isDark ? Colors.grey[500] : const Color(0xFF94A3B8),
                    fontSize: 12,
                    fontStyle: FontStyle.italic,
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildDayItem(
      BuildContext context, String day, bool isComplete, bool isGraceDay) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    // Determine visuals based on state
    Color bgColor;
    Color borderColor;
    Color iconColor;
    IconData icon;

    if (isGraceDay) {
      bgColor = AppColors.primary.withValues(alpha: 0.1);
      borderColor = AppColors.primary.withValues(alpha: 0.3);
      iconColor = AppColors.primary;
      icon = Icons.favorite;
    } else if (isComplete) {
      bgColor = AppColors.accentGreen.withValues(alpha: 0.1);
      borderColor = AppColors.accentGreen.withValues(alpha: 0.3);
      iconColor = AppColors.accentGreen;
      icon = Icons.check_circle;
    } else {
      // Incomplete state fallback (not used in mock but good to have)
      bgColor = isDark ? Colors.grey[800]! : Colors.grey[100]!;
      borderColor = isDark ? Colors.grey[700]! : Colors.grey[300]!;
      iconColor = Colors.grey[400]!;
      icon = Icons.circle_outlined;
    }

    return Column(
      children: [
        Container(
          width: 48,
          height: 48,
          decoration: BoxDecoration(
            color: bgColor,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: borderColor),
          ),
          child: Icon(icon, color: iconColor, size: 24),
        ),
        const SizedBox(height: 8),
        Text(
          day,
          style: GoogleFonts.lexend(
            color: isDark ? Colors.grey[400] : const Color(0xFF64748B),
            fontSize: 12,
            fontWeight: FontWeight.w500,
          ),
        ),
      ],
    );
  }
}
