import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../domain/entities/supplement.dart';
import '../theme/app_theme.dart';

class DosageCalculatorCard extends StatefulWidget {
  final Supplement supplement;
  final bool isDark;

  const DosageCalculatorCard({
    super.key,
    required this.supplement,
    required this.isDark,
  });

  @override
  State<DosageCalculatorCard> createState() => _DosageCalculatorCardState();
}

class _DosageCalculatorCardState extends State<DosageCalculatorCard> {
  double _currentWeight = 70; // Default weight in kg

  String? _calculateDosage() {
    final dosageMap = widget.supplement.dosageByWeight;
    if (dosageMap == null || dosageMap.isEmpty) return null;

    for (var entry in dosageMap.entries) {
      final range = entry.key; // e.g., "50-70" or "70-90"
      final parts = range.split('-');
      if (parts.length == 2) {
        final min =
            double.tryParse(parts[0].replaceAll(RegExp(r'[^0-9.]'), ''));
        final max =
            double.tryParse(parts[1].replaceAll(RegExp(r'[^0-9.]'), ''));

        if (min != null && max != null) {
          if (_currentWeight >= min && _currentWeight < max) {
            return entry.value;
          }
        }
      }
    }

    // Fallback logic for edge cases
    return null;
  }

  @override
  Widget build(BuildContext context) {
    if (widget.supplement.dosageByWeight == null) {
      return const SizedBox.shrink();
    }

    final calculatedDosage = _calculateDosage();
    const primaryGold = AppColors.primaryGold;

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: widget.isDark ? const Color(0xFF2D2616) : Colors.white,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(
          color: primaryGold.withValues(alpha: 0.2),
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: primaryGold.withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: const Icon(Icons.calculate_outlined,
                    color: primaryGold, size: 20),
              ),
              const SizedBox(width: 12),
              Text(
                'Dosage Calculator',
                style: GoogleFonts.lexend(
                  color: widget.isDark ? Colors.white : Colors.black,
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          Text(
            'Your Weight: ${_currentWeight.round()} kg',
            style: GoogleFonts.lexend(
              color: widget.isDark ? Colors.grey[300] : Colors.grey[800],
              fontSize: 15,
            ),
          ),
          SliderTheme(
            data: SliderTheme.of(context).copyWith(
              activeTrackColor: primaryGold,
              inactiveTrackColor: primaryGold.withValues(alpha: 0.2),
              thumbColor: primaryGold,
              overlayColor: primaryGold.withValues(alpha: 0.1),
            ),
            child: Slider(
              value: _currentWeight,
              min: 40,
              max: 120,
              divisions: 80,
              onChanged: (value) {
                setState(() {
                  _currentWeight = value;
                });
              },
            ),
          ),
          const SizedBox(height: 16),
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: primaryGold.withValues(alpha: 0.05),
              borderRadius: BorderRadius.circular(16),
            ),
            child: Column(
              children: [
                Text(
                  'RECOMMENDED DOSAGE',
                  style: GoogleFonts.lexend(
                    color: primaryGold,
                    fontSize: 10,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1.5,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  calculatedDosage ?? 'Outside standard range*',
                  style: GoogleFonts.lexend(
                    color: widget.isDark ? Colors.white : Colors.black,
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                if (widget.supplement.dosageFrequency != null) ...[
                  const SizedBox(height: 4),
                  Text(
                    widget.supplement.dosageFrequency!,
                    style: GoogleFonts.lexend(
                      color: Colors.grey,
                      fontSize: 14,
                    ),
                  ),
                ],
              ],
            ),
          ),
          if (widget.supplement.dosageWarnings != null &&
              widget.supplement.dosageWarnings!.isNotEmpty) ...[
            const SizedBox(height: 16),
            ...widget.supplement.dosageWarnings!.map((warning) => Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Icon(Icons.info_outline,
                          size: 14, color: Colors.amber),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          warning,
                          style: GoogleFonts.lexend(
                            color: Colors.grey,
                            fontSize: 12,
                          ),
                        ),
                      ),
                    ],
                  ),
                )),
          ],
          const SizedBox(height: 8),
          Text(
            '*Calculations are based on representative clinical data. Consult your doctor for personal medical advice.',
            style: GoogleFonts.lexend(
              color: Colors.grey,
              fontSize: 10,
              fontStyle: FontStyle.italic,
            ),
          ),
        ],
      ),
    );
  }
}
