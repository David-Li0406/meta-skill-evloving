import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class NudgeTimelineWidget extends StatelessWidget {
  const NudgeTimelineWidget({super.key});

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF1E242E) : Colors.white, // Slightly lighter dark background for card
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isDark ? Colors.grey[800]! : Colors.grey[200]!,
        ),
      ),
      child: Column(
        children: [
          SizedBox(
            height: 80,
            child: Stack(
              alignment: Alignment.center,
              children: [
                // Background Track
                Container(
                  height: 4,
                  width: double.infinity,
                  decoration: BoxDecoration(
                    color: isDark ? Colors.grey[700] : Colors.grey[200],
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
                
                // Active Progress (up to center)
                Positioned(
                  left: 0,
                  right: MediaQuery.of(context).size.width * 0.4, // Roughly to center
                  child: Container(
                    height: 4,
                    decoration: BoxDecoration(
                      color: AppColors.primary,
                      borderRadius: BorderRadius.circular(2),
                    ),
                  ),
                ),
                
                // -15m Marker
                Positioned(
                  left: 60,
                  bottom: 30,
                  child: _buildMarker(context, '-15M', isActive: true, isSmall: true),
                ),
                
                // Dose Marker (Center)
                Positioned(
                  left: 0,
                  right: 0,
                  bottom: 25,
                  child: Center(
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Container(
                          width: 32,
                          height: 32,
                          decoration: BoxDecoration(
                            color: isDark ? const Color(0xFF101822) : Colors.white,
                            shape: BoxShape.circle,
                            border: Border.all(color: AppColors.primary, width: 4),
                            boxShadow: [
                              BoxShadow(
                                color: AppColors.primary.withValues(alpha: 0.3),
                                blurRadius: 8,
                                offset: const Offset(0, 4),
                              ),
                            ],
                          ),
                          child: const Icon(
                            Icons.medication,
                            color: AppColors.primary,
                            size: 16,
                          ),
                        ),
                        const SizedBox(height: 8),
                        const Text(
                          'DOSE',
                          style: TextStyle(
                            color: AppColors.primary,
                            fontSize: 10,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                
                // +5m Marker
                Positioned(
                  right: 100,
                  bottom: 30,
                  child: _buildMarker(context, '+5M', isActive: true, isSmall: true),
                ),
                
                 // +10m Marker
                Positioned(
                  right: 60,
                  bottom: 30,
                  child: _buildMarker(context, '+10M', isActive: false, isSmall: true),
                ),
                
                 // +15m Marker
                Positioned(
                  right: 20,
                  bottom: 30,
                  child: _buildMarker(context, '+15M', isActive: false, isSmall: true),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),
          Text(
            '"Nudges occur every 5 minutes until you confirm."',
            textAlign: TextAlign.center,
            style: TextStyle(
              color: isDark ? Colors.grey[500] : Colors.grey[500],
              fontSize: 12,
              fontStyle: FontStyle.italic,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMarker(BuildContext context, String label, {required bool isActive, required bool isSmall}) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: isSmall ? 16 : 24,
          height: isSmall ? 16 : 24,
          decoration: BoxDecoration(
            color: isActive ? AppColors.primary : (isDark ? Colors.grey[700]!.withValues(alpha: 0.5) : Colors.grey[300]),
            shape: BoxShape.circle,
            border: Border.all(
              color: isDark ? const Color(0xFF101822) : Colors.white,
              width: 3,
            ),
          ),
        ),
        const SizedBox(height: 8),
        Text(
          label,
          style: TextStyle(
            color: isActive 
                ? (isDark ? Colors.grey[400] : Colors.grey[600]) // Text color for active/past markers
                : (isDark ? Colors.grey[700] : Colors.grey[400]),
            fontSize: 10,
            fontWeight: FontWeight.bold,
          ),
        ),
      ],
    );
  }
}
