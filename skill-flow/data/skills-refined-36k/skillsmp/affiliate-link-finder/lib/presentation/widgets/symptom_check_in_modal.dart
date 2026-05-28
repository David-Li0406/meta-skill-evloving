import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import 'custom_symptom_slider.dart';

class SymptomCheckInModal extends StatefulWidget {
  const SymptomCheckInModal({super.key});

  @override
  State<SymptomCheckInModal> createState() => _SymptomCheckInModalState();
}

class _SymptomCheckInModalState extends State<SymptomCheckInModal> {
  double focusValue = 0.65;
  double energyValue = 0.40;
  double moodValue = 0.80;

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final bgColor =
        isDark ? AppColors.backgroundDark : AppColors.backgroundLight;
    final textColor = isDark ? Colors.white : Colors.black;

    return Container(
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.2),
            blurRadius: 20,
            offset: const Offset(0, -5),
          ),
        ],
      ),
      child: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            // Handle
            Center(
              child: Container(
                margin: const EdgeInsets.only(top: 12, bottom: 24),
                width: 48,
                height: 6,
                decoration: BoxDecoration(
                  color: isDark ? const Color(0xFF3B4554) : Colors.grey[300],
                  borderRadius: BorderRadius.circular(999),
                ),
              ),
            ),

            // Header
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24),
              child: Column(
                children: [
                  Text(
                    'How are you feeling?',
                    style: TextStyle(
                      color: textColor,
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Checking in helps track your progress',
                    style: TextStyle(
                      color: isDark ? Colors.grey[400] : Colors.grey[500],
                      fontSize: 14,
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 24),

            // Progress Dots
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                _buildProgressDot(true),
                const SizedBox(width: 8),
                _buildProgressDot(true),
                const SizedBox(width: 8),
                _buildProgressDot(true),
              ],
            ),

            const SizedBox(height: 32),

            // Sliders
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24),
              child: Column(
                children: [
                  CustomSymptomSlider(
                    label: 'Focus',
                    startEmoji: '😫',
                    endEmoji: '🤩',
                    value: focusValue,
                    onChanged: (val) => setState(() => focusValue = val),
                  ),
                  const SizedBox(height: 24),
                  CustomSymptomSlider(
                    label: 'Energy',
                    startEmoji: '🥱',
                    endEmoji: '⚡️',
                    value: energyValue,
                    onChanged: (val) => setState(() => energyValue = val),
                  ),
                  const SizedBox(height: 24),
                  CustomSymptomSlider(
                    label: 'Mood',
                    startEmoji: '😔',
                    endEmoji: '😊',
                    value: moodValue,
                    onChanged: (val) => setState(() => moodValue = val),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 40),

            // Actions
            Padding(
              padding: const EdgeInsets.fromLTRB(
                  24, 0, 24, 40), // Bottom padding for safety
              child: Column(
                children: [
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: () => Navigator.of(context).pop(),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.primary,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(16),
                        ),
                        elevation: 8,
                        shadowColor: AppColors.primary.withValues(alpha: 0.4),
                      ),
                      child: const Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            'Done',
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          SizedBox(width: 8),
                          Icon(Icons.celebration, size: 20),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 12),
                  TextButton(
                    onPressed: () => Navigator.of(context).pop(),
                    child: Text(
                      'Skip for now',
                      style: TextStyle(
                        color: isDark ? Colors.grey[400] : Colors.grey[500],
                        fontSize: 14,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildProgressDot(bool active) {
    return Container(
      width: 48,
      height: 6,
      decoration: BoxDecoration(
        color: active
            ? AppColors.primary
            : (Theme.of(context).brightness == Brightness.dark
                ? const Color(0xFF3B4554)
                : Colors.grey[300]),
        borderRadius: BorderRadius.circular(999),
      ),
    );
  }
}
