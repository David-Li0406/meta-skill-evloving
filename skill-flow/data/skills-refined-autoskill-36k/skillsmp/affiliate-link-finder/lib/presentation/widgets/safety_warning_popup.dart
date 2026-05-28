import 'package:flutter/material.dart';
import 'package:adhd_supplement_app/domain/services/safety_guard.dart';
import 'package:adhd_supplement_app/domain/entities/medication.dart';

/// Widget that displays a safety warning popup dialog
class SafetyWarningPopup {
  /// Shows a warning dialog for medication interactions
  static Future<bool> show(
    BuildContext context, {
    required List<InteractionWarning> warnings,
  }) async {
    if (warnings.isEmpty) return true;

    final highestSeverity = SafetyGuard.getHighestSeverity(warnings);

    final result = await showDialog<bool>(
      context: context,
      barrierDismissible: false,
      builder: (context) => _WarningDialog(
        warnings: warnings,
        highestSeverity: highestSeverity ?? WarningSeverity.info,
      ),
    );

    return result ?? false;
  }
}

class _WarningDialog extends StatelessWidget {
  final List<InteractionWarning> warnings;
  final WarningSeverity highestSeverity;

  const _WarningDialog({
    required this.warnings,
    required this.highestSeverity,
  });

  Color _getSeverityColor() {
    switch (highestSeverity) {
      case WarningSeverity.danger:
        return const Color(0xFFFF1744);
      case WarningSeverity.warning:
        return const Color(0xFFFF9100);
      case WarningSeverity.caution:
        return const Color(0xFFFFD740);
      case WarningSeverity.info:
        return const Color(0xFF448AFF);
    }
  }

  IconData _getSeverityIcon() {
    switch (highestSeverity) {
      case WarningSeverity.danger:
        return Icons.dangerous;
      case WarningSeverity.warning:
        return Icons.warning;
      case WarningSeverity.caution:
        return Icons.info_outline;
      case WarningSeverity.info:
        return Icons.lightbulb_outline;
    }
  }

  @override
  Widget build(BuildContext context) {
    final color = _getSeverityColor();

    return Dialog(
      backgroundColor: const Color(0xFF1E1E1E),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20),
        side: BorderSide(color: color.withValues(alpha: 0.5), width: 2),
      ),
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            // Header Icon
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: color.withValues(alpha: 0.1),
                shape: BoxShape.circle,
                border: Border.all(color: color, width: 3),
              ),
              child: Icon(
                _getSeverityIcon(),
                color: color,
                size: 40,
              ),
            ),
            const SizedBox(height: 20),

            // Title
            Text(
              warnings.first.title,
              style: TextStyle(
                color: color,
                fontSize: 22,
                fontWeight: FontWeight.bold,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 16),

            // Warnings List
            ConstrainedBox(
              constraints: const BoxConstraints(maxHeight: 300),
              child: SingleChildScrollView(
                child: Column(
                  children: warnings
                      .map((warning) => Padding(
                            padding: const EdgeInsets.only(bottom: 16),
                            child: _WarningCard(warning: warning),
                          ))
                      .toList(),
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Action Buttons
            Row(
              children: [
                Expanded(
                  child: OutlinedButton(
                    onPressed: () => Navigator.pop(context, false),
                    style: OutlinedButton.styleFrom(
                      foregroundColor: Colors.white70,
                      side: const BorderSide(color: Colors.white30),
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    child: const Text('Go Back'),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: ElevatedButton(
                    onPressed: highestSeverity == WarningSeverity.danger
                        ? null
                        : () => Navigator.pop(context, true),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: highestSeverity == WarningSeverity.danger
                          ? Colors.grey
                          : color,
                      foregroundColor: Colors.black,
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    child: Text(
                      highestSeverity == WarningSeverity.danger
                          ? 'Blocked'
                          : 'Proceed Anyway',
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _WarningCard extends StatelessWidget {
  final InteractionWarning warning;

  const _WarningCard({required this.warning});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF2D2D2D),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.medication, color: Colors.white54, size: 16),
              const SizedBox(width: 8),
              Text(
                '${warning.supplementName} + ${warning.medicationName}',
                style: const TextStyle(
                  color: Colors.white70,
                  fontSize: 12,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Text(
            warning.description,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 14,
              height: 1.5,
            ),
          ),
          const SizedBox(height: 12),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: const Color(0xFF00E676).withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(
                color: const Color(0xFF00E676).withValues(alpha: 0.3),
              ),
            ),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Icon(
                  Icons.tips_and_updates,
                  color: Color(0xFF00E676),
                  size: 16,
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    warning.recommendation,
                    style: const TextStyle(
                      color: Color(0xFF00E676),
                      fontSize: 13,
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
}
