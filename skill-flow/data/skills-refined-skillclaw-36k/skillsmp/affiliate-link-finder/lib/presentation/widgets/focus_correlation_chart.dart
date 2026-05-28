import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class FocusCorrelationChart extends StatelessWidget {
  const FocusCorrelationChart({super.key});

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    
    return AspectRatio(
      aspectRatio: 1.4,
      child: Stack(
        children: [
          // Bar Chart (Consistency)
          BarChart(
            BarChartData(
              alignment: BarChartAlignment.spaceAround,
              maxY: 20,
              barTouchData: BarTouchData(enabled: false),
              titlesData: FlTitlesData(
                show: true,
                bottomTitles: AxisTitles(
                  sideTitles: SideTitles(
                    showTitles: true,
                    getTitlesWidget: (value, meta) {
                       const style = TextStyle(
                        color: Colors.grey,
                        fontWeight: FontWeight.bold,
                        fontSize: 12,
                      );
                      String text;
                      switch (value.toInt()) {
                        case 0:
                          text = 'W1';
                          break;
                        case 1:
                          text = 'W2';
                          break;
                        case 2:
                          text = 'W3';
                          break;
                        case 3:
                          text = 'W4';
                          break;
                        default:
                          text = '';
                      }
                      return SideTitleWidget(
                        axisSide: meta.axisSide,
                        space: 16,
                        child: Text(text, style: style),
                      );
                    },
                    reservedSize: 40,
                  ),
                ),
                leftTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
              ),
              borderData: FlBorderData(show: false),
              gridData: FlGridData(
                show: true,
                drawVerticalLine: false,
                horizontalInterval: 5,
                getDrawingHorizontalLine: (value) {
                  return FlLine(
                    color: isDark ? Colors.grey.withValues(alpha: 0.1) : Colors.grey.withValues(alpha: 0.2),
                    strokeWidth: 1,
                    dashArray: [5, 5],
                  );
                },
              ),
              barGroups: [
                _makeGroupData(0, 12, isDark),
                _makeGroupData(1, 14, isDark),
                _makeGroupData(2, 11, isDark),
                _makeGroupData(3, 16, isDark),
                _makeGroupData(4, 15, isDark),
                _makeGroupData(5, 17, isDark),
                _makeGroupData(6, 15.5, isDark),
              ],
            ),
          ),
          
          // Line Chart Overlay (Focus)
          // We can't strictly overlay FlCharts easily without maintaining aspect ratio and scales perfectly.
          // Since LineChart and BarChart might have different scales, we need to be careful.
          // For this scaffold, I will overlay a transparent LineChart.
          LineChart(
            LineChartData(
              minY: 0,
              maxY: 20,
              lineTouchData: const LineTouchData(enabled: false),
              titlesData: const FlTitlesData(show: false),
              borderData: FlBorderData(show: false),
              gridData: const FlGridData(show: false),
              lineBarsData: [
                LineChartBarData(
                  spots: const [
                    FlSpot(0.2, 8),
                    FlSpot(1.2, 12),
                    FlSpot(2.2, 6),
                    FlSpot(3.2, 14),
                    FlSpot(4.2, 11),
                    FlSpot(5.2, 16),
                    FlSpot(6.2, 13),
                  ],
                  isCurved: true,
                  color: AppColors.primary,
                  barWidth: 3,
                  isStrokeCapRound: true,
                  dotData: FlDotData(
                    show: true,
                    getDotPainter: (spot, percent, barData, index) {
                      // Only show dots on specific points to match wireframe approximation
                      if (index == 1 || index == 5 || index == 6) {
                         return FlDotCirclePainter(
                          radius: 4,
                          color: AppColors.primary,
                          strokeWidth: 2,
                          strokeColor: isDark ? AppColors.cardDark : Colors.white,
                        );
                      }
                      return FlDotCirclePainter(radius: 0, color: Colors.transparent);
                    },
                  ),
                  belowBarData: BarAreaData(show: false),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  BarChartGroupData _makeGroupData(int x, double y, bool isDark) {
    return BarChartGroupData(
      x: x,
      barRods: [
        BarChartRodData(
          toY: y,
          color: AppColors.accentGreen.withValues(alpha: 0.8),
          width: 24,
          borderRadius: const BorderRadius.all(Radius.circular(4)), 
          gradient: LinearGradient(
            begin: Alignment.bottomCenter,
            end: Alignment.topCenter,
            colors: [
              AppColors.accentGreen.withValues(alpha: 0.2),
              AppColors.accentGreen.withValues(alpha: 0.8),
            ],
          ),
        ),
      ],
    );
  }
}
