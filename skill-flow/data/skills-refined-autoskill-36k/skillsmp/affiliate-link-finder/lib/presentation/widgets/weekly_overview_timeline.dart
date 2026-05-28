import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class WeeklyOverviewTimeline extends StatelessWidget {
  const WeeklyOverviewTimeline({super.key});

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: isDark ? Colors.white.withValues(alpha: 0.05) : Colors.grey[100],
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'WEEKLY OVERVIEW',
            style: TextStyle(
              color: isDark ? const Color(0xFF9DA8B9) : Colors.grey[500],
              fontSize: 12,
              fontWeight: FontWeight.bold,
              letterSpacing: 1.2,
            ),
          ),
          const SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              _buildDayItem('M', DayStatus.completed),
              _buildDayItem('T', DayStatus.completed),
              _buildDayItem('W', DayStatus.completed),
              _buildDayItem('T', DayStatus.rest, isSelected: true),
              _buildDayItem('F', DayStatus.upcoming),
              _buildDayItem('S', DayStatus.upcoming),
              _buildDayItem('S', DayStatus.upcoming),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildDayItem(String day, DayStatus status,
      {bool isSelected = false}) {
    Color bgColor;
    Color textColor;
    Widget bottomIndicator;

    switch (status) {
      case DayStatus.completed:
        bgColor = AppColors.primaryGold;
        textColor = Colors.white;
        bottomIndicator = const Icon(Icons.check_circle,
            color: AppColors.primaryGold, size: 14);
        break;
      case DayStatus.rest:
        bgColor = isSelected
            ? AppColors.primaryGold.withValues(alpha: 0.2)
            : Colors.transparent;
        textColor = AppColors.primaryGold;
        bottomIndicator =
            const Icon(Icons.coffee, color: AppColors.primaryGold, size: 14);
        break;
      case DayStatus.upcoming:
        bgColor = const Color(0xFF334155); // Slate 700ish for dark mode
        textColor = const Color(0xFF64748B); // Slate 500
        bottomIndicator = Container(
            margin: const EdgeInsets.only(top: 4),
            width: 4,
            height: 4,
            decoration: BoxDecoration(
                color: const Color(0xFF334155),
                borderRadius: BorderRadius.circular(2)));
        break;
    }

    if (status == DayStatus.rest && isSelected) {
      return Column(
        children: [
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              color: bgColor,
              shape: BoxShape.circle,
              border: Border.all(
                  color: AppColors.primaryGold.withValues(alpha: 0.4),
                  width: 2),
              boxShadow: [
                BoxShadow(
                  color: AppColors.primaryGold.withValues(alpha: 0.1),
                  blurRadius: 8,
                  offset: const Offset(0, 4),
                ),
              ],
            ),
            alignment: Alignment.center,
            child: Text(
              day,
              style: TextStyle(
                color: textColor,
                fontSize: 12,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          const SizedBox(height: 4),
          bottomIndicator,
        ],
      );
    }

    return Column(
      children: [
        Container(
          width: 32,
          height: 32,
          decoration: BoxDecoration(
            color: bgColor,
            shape: BoxShape.circle,
          ),
          alignment: Alignment.center,
          child: Text(
            day,
            style: TextStyle(
              color: textColor,
              fontSize: 12,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
        const SizedBox(height: 4),
        bottomIndicator,
      ],
    );
  }
}

enum DayStatus {
  completed,
  rest,
  upcoming,
}
