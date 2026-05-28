import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

import 'package:adhd_supplement_app/domain/services/adhd_interaction_guard.dart';

/// ADHD-Friendly Safety Guard UI Component
///
/// Allows users to check medication-supplement interactions
/// with clear visual warnings and timing recommendations.
class SafetyGuardWidget extends StatefulWidget {
  const SafetyGuardWidget({super.key});

  @override
  State<SafetyGuardWidget> createState() => _SafetyGuardWidgetState();
}

class _SafetyGuardWidgetState extends State<SafetyGuardWidget> {
  String? _selectedMedication;
  String? _selectedSupplement;
  Map<String, dynamic>? _interactionResult;

  // Available medications
  final List<String> _medications = [
    'None',
    ...ADHDInteractionGuard.stimulantMeds,
  ];

  // Available supplements
  final List<String> _supplements = [
    'Select a supplement',
    'Omega-3 (EPA/DHA)',
    'Magnesium Glycinate',
    'L-Theanine',
    'Zinc',
    'Vitamin C',
    'Ascorbic Acid',
    'Multivitamin',
    'Orange Extract',
    'Citrus Bioflavonoids',
  ];

  void _checkInteraction() {
    if (_selectedMedication == null ||
        _selectedSupplement == null ||
        _selectedMedication == 'None' ||
        _selectedSupplement == 'Select a supplement') {
      setState(() {
        _interactionResult = null;
      });
      return;
    }

    setState(() {
      _interactionResult = ADHDInteractionGuard.checkInteraction(
        _selectedMedication!,
        _selectedSupplement!,
      );
    });
  }

  Future<void> _launchSource() async {
    final url = Uri.parse(
      'https://pubmed.ncbi.nlm.nih.gov/16780290/', // Study on Vitamin C and amphetamine excretion
    );
    if (!await launchUrl(url, mode: LaunchMode.externalApplication)) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Could not open source link')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: const Color(0xFF1E1E1E),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          // Header
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: const Color(0xFF448AFF).withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: const Icon(
                  Icons.health_and_safety,
                  color: Color(0xFF448AFF),
                  size: 28,
                ),
              ),
              const SizedBox(width: 16),
              const Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Safety Guard',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 22,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    Text(
                      'Check medication interactions',
                      style: TextStyle(
                        color: Colors.white54,
                        fontSize: 14,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 24),

          // Medication Dropdown
          const Text(
            'Your ADHD Medication',
            style: TextStyle(
              color: Colors.white,
              fontSize: 16,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 8),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            decoration: BoxDecoration(
              color: const Color(0xFF2D2D2D),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.white12),
            ),
            child: DropdownButton<String>(
              value: _selectedMedication,
              hint: const Text(
                'Select your medication',
                style: TextStyle(color: Colors.white54, fontSize: 16),
              ),
              isExpanded: true,
              dropdownColor: const Color(0xFF2D2D2D),
              underline: const SizedBox.shrink(),
              style: const TextStyle(color: Colors.white, fontSize: 16),
              items: _medications.map((med) {
                return DropdownMenuItem(
                  value: med,
                  child: Text(med),
                );
              }).toList(),
              onChanged: (value) {
                setState(() {
                  _selectedMedication = value;
                });
                _checkInteraction();
              },
            ),
          ),
          const SizedBox(height: 20),

          // Supplement Dropdown
          const Text(
            'Supplement to Check',
            style: TextStyle(
              color: Colors.white,
              fontSize: 16,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 8),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            decoration: BoxDecoration(
              color: const Color(0xFF2D2D2D),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.white12),
            ),
            child: DropdownButton<String>(
              value: _selectedSupplement,
              hint: const Text(
                'Select a supplement',
                style: TextStyle(color: Colors.white54, fontSize: 16),
              ),
              isExpanded: true,
              dropdownColor: const Color(0xFF2D2D2D),
              underline: const SizedBox.shrink(),
              style: const TextStyle(color: Colors.white, fontSize: 16),
              items: _supplements.map((supp) {
                return DropdownMenuItem(
                  value: supp,
                  child: Text(supp),
                );
              }).toList(),
              onChanged: (value) {
                setState(() {
                  _selectedSupplement = value;
                });
                _checkInteraction();
              },
            ),
          ),
          const SizedBox(height: 24),

          // Interaction Result
          if (_interactionResult != null) ...[
            _buildInteractionCard(_interactionResult!),
          ],
        ],
      ),
    );
  }

  Widget _buildInteractionCard(Map<String, dynamic> result) {
    final isInteraction = result['risk'] == 'Moderate';
    final color =
        isInteraction ? const Color(0xFFFFAB40) : const Color(0xFF00E676);
    final icon =
        isInteraction ? Icons.warning_amber_rounded : Icons.check_circle;

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: color, width: 2),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header
          Row(
            children: [
              Icon(icon, color: color, size: 32),
              const SizedBox(width: 12),
              Expanded(
                child: Text(
                  result['warning'] as String? ?? 'No Interaction',
                  style: TextStyle(
                    color: color,
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),

          // Message
          Text(
            result['message'] as String,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 16,
              height: 1.5,
            ),
          ),
          const SizedBox(height: 16),

          // Timing Tip
          if (isInteraction) ...[
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFF2D2D2D),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Icon(
                    Icons.schedule,
                    color: Color(0xFF448AFF),
                    size: 24,
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Timing Tip',
                          style: TextStyle(
                            color: Color(0xFF448AFF),
                            fontSize: 14,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          result['recommendation'] as String,
                          style: const TextStyle(
                            color: Colors.white70,
                            fontSize: 15,
                            height: 1.4,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),

            // Source Link
            InkWell(
              onTap: _launchSource,
              child: Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 12,
                ),
                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.05),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.white12),
                ),
                child: const Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      Icons.open_in_new,
                      color: Colors.white54,
                      size: 16,
                    ),
                    SizedBox(width: 8),
                    Text(
                      'View Medical Source (PubMed)',
                      style: TextStyle(
                        color: Colors.white54,
                        fontSize: 13,
                        decoration: TextDecoration.underline,
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
          ],

          // Disclaimer (always shown with results)
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: const Color(0xFF2D2D2D).withValues(alpha: 0.5),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: Colors.white.withValues(alpha: 0.1)),
            ),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Icon(
                  Icons.info_outline,
                  color: Colors.white.withValues(alpha: 0.6),
                  size: 16,
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    'Disclaimer: This tool is for informational purposes only and is not medical advice. '
                    'Always consult with your prescribing physician or a pharmacist before starting any new supplement, '
                    'as individual chemistry varies.',
                    style: TextStyle(
                      color: Colors.white.withValues(alpha: 0.6),
                      fontSize: 12,
                      height: 1.4,
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
