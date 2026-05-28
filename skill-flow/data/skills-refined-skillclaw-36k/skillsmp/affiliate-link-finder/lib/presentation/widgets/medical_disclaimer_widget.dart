import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/app_theme.dart';

class MedicalDisclaimerWidget extends StatelessWidget {
  final bool isDark;
  final bool isChecked;
  final ValueChanged<bool?> onChecked;

  const MedicalDisclaimerWidget({
    super.key,
    required this.isDark,
    required this.isChecked,
    required this.onChecked,
  });

  @override
  Widget build(BuildContext context) {
    final titleColor = isDark ? Colors.white : const Color(0xFF111713);
    final textColor = isDark ? Colors.grey[300] : Colors.grey[700];
    final cardColor = isDark ? const Color(0xFF1a2920) : Colors.white;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.amber.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.amber.withValues(alpha: 0.5)),
            ),
            child: const Row(
              children: [
                Icon(Icons.warning_amber_rounded, color: Colors.amber),
                SizedBox(width: 12),
                Text(
                  'Critical Medical Information',
                  style: TextStyle(
                    color: Colors.amber,
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),
          Text(
            'Medical Disclaimer',
            style: GoogleFonts.lexend(
              color: titleColor,
              fontSize: 28,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 16),
          _buildTextSection(
              'Not Medical Advice',
              'This application is an informational tool and does not provide medical advice, diagnosis, or treatment.',
              textColor!),
          const SizedBox(height: 16),
          _buildBulletPoint(
              'Consult your doctor before starting any new supplement or medication.',
              textColor),
          _buildBulletPoint(
              'Never disregard professional medical advice because of something you read here.',
              textColor),
          _buildBulletPoint(
              'In case of a medical emergency, call your doctor or emergency services immediately.',
              textColor),
          const SizedBox(height: 24),
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: cardColor,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(
                color: isChecked
                    ? AppColors.accentGreen
                    : (isDark ? Colors.grey[800]! : Colors.grey[200]!),
              ),
            ),
            child: Row(
              children: [
                Checkbox(
                  value: isChecked,
                  onChanged: onChecked,
                  activeColor: AppColors.accentGreen,
                  checkColor: const Color(0xFF112117),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(4),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    'I have read and understand this medical disclaimer and agree to use this app responsibly.',
                    style: TextStyle(
                      color: isDark ? Colors.white : Colors.black,
                      fontSize: 14,
                      fontWeight:
                          isChecked ? FontWeight.bold : FontWeight.normal,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTextSection(String title, String content, Color textColor) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title.toUpperCase(),
          style: const TextStyle(
            color: AppColors.accentGreen,
            fontSize: 12,
            fontWeight: FontWeight.bold,
            letterSpacing: 1.2,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          content,
          style: TextStyle(
            color: textColor,
            fontSize: 16,
            height: 1.5,
          ),
        ),
      ],
    );
  }

  Widget _buildBulletPoint(String text, Color textColor) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('• ',
              style: TextStyle(
                  color: AppColors.accentGreen,
                  fontSize: 18,
                  fontWeight: FontWeight.bold)),
          Expanded(
            child: Text(
              text,
              style: TextStyle(color: textColor, fontSize: 15, height: 1.4),
            ),
          ),
        ],
      ),
    );
  }
}
