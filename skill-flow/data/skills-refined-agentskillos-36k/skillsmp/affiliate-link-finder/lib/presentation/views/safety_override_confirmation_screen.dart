import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../application/view_models/safety_view_model.dart';
import '../../domain/entities/supplement_interaction.dart';
import '../theme/app_theme.dart';

class SafetyOverrideConfirmationScreen extends StatefulWidget {
  final SupplementInteraction interaction;

  const SafetyOverrideConfirmationScreen({
    super.key,
    required this.interaction,
  });

  @override
  State<SafetyOverrideConfirmationScreen> createState() =>
      _SafetyOverrideConfirmationScreenState();
}

class _SafetyOverrideConfirmationScreenState
    extends State<SafetyOverrideConfirmationScreen> {
  bool _isOverrideLoading = false;

  Future<void> _handleOverride() async {
    setState(() => _isOverrideLoading = true);

    try {
      final safetyViewModel = context.read<SafetyViewModel>();
      // Log with a default reason since the UI text explicitly says "Confirmed with Doctor"
      await safetyViewModel.overrideInteraction(
          widget.interaction.id, "Confirmed with Doctor (Quick Action)");

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Safety override logged. Please consult your doctor.'),
          backgroundColor: Colors.orange,
        ),
      );

      Navigator.pop(context, true);
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e'), backgroundColor: Colors.red),
      );
    } finally {
      if (mounted) setState(() => _isOverrideLoading = false);
    }
  }

  void _handleReschedule() {
    // For now, this acts as "Cancel" / "Don't add conflicting item"
    Navigator.pop(context, false);
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    // Using a Scaffold with a dark background to simulate the "modal" feel on a dedicated screen
    return Scaffold(
      backgroundColor: isDark
          ? const Color(0xFF101622)
          : const Color(
              0xFF101622), // Always dark background for the "modal" look against dark app or distinct contrast
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 380),
                child: Container(
                  decoration: BoxDecoration(
                    color: isDark ? const Color(0xFF1C2027) : Colors.white,
                    borderRadius: BorderRadius.circular(24),
                    border: Border.all(
                      color: isDark ? Colors.grey[800]! : Colors.grey[200]!,
                    ),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withValues(alpha: 0.3),
                        blurRadius: 20,
                        offset: const Offset(0, 10),
                      ),
                    ],
                  ),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      // Header Section
                      Padding(
                        padding: const EdgeInsets.fromLTRB(24, 32, 24, 8),
                        child: Column(
                          children: [
                            Container(
                              width: 64,
                              height: 64,
                              decoration: BoxDecoration(
                                color: AppColors.warningAmber.withValues(alpha: 0.1),
                                shape: BoxShape.circle,
                              ),
                              child: const Icon(
                                Icons.warning_amber_rounded,
                                color: AppColors.warningAmber,
                                size: 36,
                              ),
                            ),
                            const SizedBox(height: 16),
                            Text(
                              'Safety Notice',
                              style: TextStyle(
                                fontSize: 24,
                                fontWeight: FontWeight.bold,
                                color: isDark ? Colors.white : Colors.grey[900],
                                letterSpacing: -0.5,
                              ),
                            ),
                          ],
                        ),
                      ),

                      // Interaction Details Box
                      Padding(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 24, vertical: 16),
                        child: Container(
                          padding: const EdgeInsets.all(16),
                          decoration: BoxDecoration(
                            color: AppColors.warningAmber.withValues(alpha: 0.05),
                            borderRadius: BorderRadius.circular(16),
                            border: Border.all(
                                color: AppColors.warningAmber.withValues(alpha: 0.1)),
                          ),
                          child: Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Padding(
                                padding: EdgeInsets.only(top: 2),
                                child: Icon(
                                  Icons
                                      .medication_liquid_outlined, // Closest match to design
                                  color: AppColors.warningAmber,
                                  size: 20,
                                ),
                              ),
                              const SizedBox(width: 12),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      'Interaction Detected',
                                      style: TextStyle(
                                        fontSize: 14,
                                        fontWeight: FontWeight.w600,
                                        color: isDark
                                            ? Colors.grey[200]
                                            : Colors.grey[800],
                                      ),
                                    ),
                                    const SizedBox(height: 4),
                                    Text(
                                      widget.interaction.description,
                                      style: TextStyle(
                                        fontSize: 14,
                                        height: 1.5,
                                        color: isDark
                                            ? const Color(0xFF9DA8B9)
                                            : Colors.grey[600],
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),

                      // Recommendation Text
                      Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 24),
                        child: Text(
                          "We recommend waiting 60 minutes before logging this supplement.",
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.w500,
                            color: isDark
                                ? const Color(0xFF9DA8B9)
                                : Colors.grey[500],
                          ),
                        ),
                      ),

                      const SizedBox(height: 24),

                      // Action Buttons
                      Padding(
                        padding: const EdgeInsets.fromLTRB(24, 0, 24, 24),
                        child: Column(
                          children: [
                            // Primary Action: Reschedule
                            SizedBox(
                              width: double.infinity,
                              height: 56,
                              child: ElevatedButton(
                                onPressed: _handleReschedule,
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: AppColors.primary,
                                  foregroundColor: Colors.white,
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(16),
                                  ),
                                  elevation: 4,
                                  shadowColor:
                                      AppColors.primary.withValues(alpha: 0.3),
                                ),
                                child: const Row(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: [
                                    Icon(Icons.schedule, size: 20),
                                    SizedBox(width: 8),
                                    Text(
                                      'Reschedule for 1 hour later',
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                            const SizedBox(height: 12),

                            // Secondary Action: Override
                            SizedBox(
                              width: double.infinity,
                              height: 56,
                              child: TextButton(
                                onPressed:
                                    _isOverrideLoading ? null : _handleOverride,
                                style: TextButton.styleFrom(
                                  foregroundColor: isDark
                                      ? Colors.grey[400]
                                      : Colors.grey[500],
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(16),
                                  ),
                                ),
                                child: _isOverrideLoading
                                    ? const SizedBox(
                                        width: 20,
                                        height: 20,
                                        child: CircularProgressIndicator(
                                            strokeWidth: 2),
                                      )
                                    : const Text(
                                        'Log anyway (Confirmed with Doctor)',
                                        style: TextStyle(
                                          fontSize: 14,
                                          fontWeight: FontWeight.w600,
                                        ),
                                      ),
                              ),
                            ),
                          ],
                        ),
                      ),

                      // Footer Text
                      Padding(
                        padding: const EdgeInsets.only(bottom: 24),
                        child: Text(
                          'Your health configurations can be updated in Settings.',
                          style: TextStyle(
                            fontSize: 12,
                            color: isDark ? Colors.grey[600] : Colors.grey[400],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
