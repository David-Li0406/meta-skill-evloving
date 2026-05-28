import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../domain/services/safety_guard.dart';
import '../../domain/entities/medication.dart';

class MedicationSafetyAlert extends StatelessWidget {
  final List<InteractionWarning> warnings;
  final bool isDark;

  const MedicationSafetyAlert({
    super.key,
    required this.warnings,
    required this.isDark,
  });

  @override
  Widget build(BuildContext context) {
    if (warnings.isEmpty) return const SizedBox.shrink();

    // Determine highest severity for overall styling
    final highestSeverity = SafetyGuard.getHighestSeverity(warnings);
    final alertColor = _getSeverityColor(highestSeverity);

    return Container(
      margin: const EdgeInsets.only(bottom: 24),
      decoration: BoxDecoration(
        color: alertColor.withValues(alpha: 0.05),
        borderRadius: BorderRadius.circular(24),
        border: Border.all(
          color: alertColor.withValues(alpha: 0.3),
          width: 2,
        ),
      ),
      clipBehavior: Clip.antiAlias,
      child: Column(
        children: [
          // Header
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
            color: alertColor.withValues(alpha: 0.1),
            child: Row(
              children: [
                Icon(
                  _getSeverityIcon(highestSeverity),
                  color: alertColor,
                  size: 20,
                ),
                const SizedBox(width: 12),
                Text(
                  _getSeverityLabel(highestSeverity),
                  style: GoogleFonts.lexend(
                    color: alertColor,
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1.0,
                  ),
                ),
              ],
            ),
          ),

          // Warnings List
          Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                ...warnings.map((warning) => Padding(
                      padding: const EdgeInsets.only(bottom: 16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'With ${warning.medicationName}:',
                            style: GoogleFonts.lexend(
                              color: isDark ? Colors.white : Colors.black,
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            warning.description,
                            style: GoogleFonts.lexend(
                              color:
                                  isDark ? Colors.grey[300] : Colors.grey[700],
                              fontSize: 14,
                              height: 1.5,
                            ),
                          ),
                          const SizedBox(height: 12),
                          Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Icon(Icons.lightbulb_outline,
                                  size: 16, color: alertColor),
                              const SizedBox(width: 8),
                              Expanded(
                                child: Text(
                                  warning.recommendation,
                                  style: GoogleFonts.lexend(
                                    color: alertColor,
                                    fontSize: 13,
                                    fontWeight: FontWeight.w600,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    )),
                const Divider(),
                const SizedBox(height: 8),
                Row(
                  children: [
                    const Icon(Icons.medical_services_outlined,
                        size: 14, color: Colors.grey),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        'Always consult your prescribing physician before adding new supplements to your medication regimen.',
                        style: GoogleFonts.lexend(
                          color: Colors.grey,
                          fontSize: 11,
                          fontStyle: FontStyle.italic,
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Color _getSeverityColor(WarningSeverity? severity) {
    switch (severity) {
      case WarningSeverity.danger:
        return const Color(0xFFEF4444); // Red
      case WarningSeverity.warning:
        return const Color(0xFFF59E0B); // Amber
      case WarningSeverity.caution:
        return const Color(0xFF3B82F6); // Blue
      default:
        return const Color(0xFF10B981); // Green
    }
  }

  IconData _getSeverityIcon(WarningSeverity? severity) {
    switch (severity) {
      case WarningSeverity.danger:
        return Icons.gpp_maybe;
      case WarningSeverity.warning:
        return Icons.warning_amber_rounded;
      case WarningSeverity.caution:
        return Icons.info_outline;
      default:
        return Icons.check_circle_outline;
    }
  }

  String _getSeverityLabel(WarningSeverity? severity) {
    switch (severity) {
      case WarningSeverity.danger:
        return 'CRITICAL INTERACTION';
      case WarningSeverity.warning:
        return 'MEDICATION ALERT';
      case WarningSeverity.caution:
        return 'TIMING CONSIDERATION';
      default:
        return 'SAFETY CHECKED';
    }
  }
}
