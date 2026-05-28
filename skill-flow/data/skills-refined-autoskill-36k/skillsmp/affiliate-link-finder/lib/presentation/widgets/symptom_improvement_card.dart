import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class SymptomImprovementCard extends StatelessWidget {
  final String label;
  final double percentage; // 0.0 to 1.0 (for bar)
  final String changeText;
  final bool isImprovement; // e.g. decrease in impulsivity is improvement, increase in memory is improvement.
                            // Wireframe shows Down Arrow 15% for Impulsivity (Good) and Up Arrow 8% for Memory (Good).
                            // Both have green text.

  const SymptomImprovementCard({
    super.key,
    required this.label,
    required this.percentage,
    required this.changeText,
    required this.isImprovement,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    const valueColor = Color(0xFF10B981); // Emerald 500

    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: isDark ? AppColors.cardDark : Colors.white,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(
             color: isDark ? Colors.grey[800]! : Colors.grey[100]!,
          ),
        ),
        child: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  label,
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: isDark ? AppColors.textSecondaryDark : AppColors.textSecondaryLight,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                Text(
                  changeText,
                  style: const TextStyle(
                    color: valueColor,
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Stack(
               children: [
                 Container(
                   height: 8,
                   width: double.infinity,
                   decoration: BoxDecoration(
                     color: isDark ? Colors.grey[800] : Colors.grey[100],
                     borderRadius: BorderRadius.circular(999),
                   ),
                 ),
                 LayoutBuilder(
                   builder: (context, constraints) {
                     return Container(
                       height: 8,
                       width: constraints.maxWidth * percentage,
                       decoration: BoxDecoration(
                         color: label == 'Memory' ? AppColors.accentGreen : AppColors.primary,
                         borderRadius: BorderRadius.circular(999),
                       ),
                     );
                   },
                 ),
               ],
            ),
          ],
        ),
      ),
    );
  }
}
