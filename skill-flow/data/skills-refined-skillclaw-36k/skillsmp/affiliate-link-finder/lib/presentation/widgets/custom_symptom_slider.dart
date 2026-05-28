import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class CustomSymptomSlider extends StatelessWidget {
  final String label;
  final String startEmoji;
  final String endEmoji;
  final double value; // 0.0 to 1.0
  final ValueChanged<double> onChanged;

  const CustomSymptomSlider({
    super.key,
    required this.label,
    required this.startEmoji,
    required this.endEmoji,
    required this.value,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final percentage = (value * 100).toInt();

    return Column(
      children: [
        // Label Row
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              children: [
                Text(
                  '$label: ',
                  style: TextStyle(
                    color: isDark ? Colors.white : Colors.black,
                    fontSize: 16,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                Text(
                  '$startEmoji to $endEmoji',
                  style: const TextStyle(fontSize: 16),
                ),
              ],
            ),
            Text(
              '$percentage%',
              style: TextStyle(
                color: isDark ? Colors.grey[400] : Colors.grey[600],
                fontSize: 14,
                fontWeight: FontWeight.w500,
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),

        // Slider Track
        LayoutBuilder(
          builder: (context, constraints) {
            return GestureDetector(
              onTapDown: (details) =>
                  _updateValue(details.localPosition.dx, constraints.maxWidth),
              onHorizontalDragUpdate: (details) =>
                  _updateValue(details.localPosition.dx, constraints.maxWidth),
              child: Container(
                height: 30, // Hit area height
                color: Colors.transparent, // Invisible hit area
                alignment: Alignment.center,
                child: Stack(
                  alignment: Alignment.centerLeft,
                  clipBehavior: Clip.none,
                  children: [
                    // Track Background
                    Container(
                      height: 6,
                      width: double.infinity,
                      decoration: BoxDecoration(
                        color:
                            isDark ? const Color(0xFF3B4554) : Colors.grey[200],
                        borderRadius: BorderRadius.circular(999),
                      ),
                    ),

                    // Active Track
                    Container(
                      height: 6,
                      width: constraints.maxWidth * value,
                      decoration: BoxDecoration(
                        color: AppColors.primary,
                        borderRadius: BorderRadius.circular(999),
                      ),
                    ),

                    // Thumb
                    Positioned(
                      left: (constraints.maxWidth * value) -
                          12, // Center the 24px thumb
                      child: Container(
                        width: 24,
                        height: 24,
                        decoration: BoxDecoration(
                          color: Colors.white,
                          shape: BoxShape.circle,
                          border:
                              Border.all(color: AppColors.primary, width: 2),
                          boxShadow: [
                            BoxShadow(
                              color: Colors.black.withValues(alpha: 0.2),
                              blurRadius: 4,
                              offset: const Offset(0, 2),
                            ),
                          ],
                        ),
                        alignment: Alignment.center,
                        child: Container(
                          width: 8,
                          height: 8,
                          decoration: const BoxDecoration(
                            color: AppColors.primary,
                            shape: BoxShape.circle,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            );
          },
        ),
      ],
    );
  }

  void _updateValue(double dx, double maxWidth) {
    final newValue = (dx / maxWidth).clamp(0.0, 1.0);
    onChanged(newValue);
  }
}
