import 'package:flutter/material.dart';
import '../../domain/entities/supplement_interaction.dart';
import '../theme/app_theme.dart';
import '../navigation/app_router.dart';

class SafetyInteractionDetailScreen extends StatelessWidget {
  final SupplementInteraction interaction;

  const SafetyInteractionDetailScreen({
    super.key,
    required this.interaction,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      backgroundColor: isDark ? AppColors.backgroundDark : Colors.white,
      appBar: AppBar(
        title: const Text('Safety Interaction'),
        centerTitle: true,
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.close),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Severity Header
            _buildSeverityHeader(interaction.severity),
            const SizedBox(height: 32),

            // Interaction Description
            Text(
              'Interaction Details',
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: isDark ? Colors.white : Colors.black,
                  ),
            ),
            const SizedBox(height: 12),
            Text(
              interaction.description,
              style: TextStyle(
                fontSize: 16,
                height: 1.5,
                color: isDark ? Colors.grey[300] : Colors.grey[700],
              ),
            ),
            const SizedBox(height: 32),

            // Recommendations
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: _getSeverityColor(interaction.severity)
                    .withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(
                  color: _getSeverityColor(interaction.severity)
                      .withValues(alpha: 0.3),
                ),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(
                        Icons.info_outline,
                        color: _getSeverityColor(interaction.severity),
                      ),
                      const SizedBox(width: 12),
                      Text(
                        'Recommendation',
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          color: _getSeverityColor(interaction.severity),
                          fontSize: 16,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Text(
                    interaction.recommendation,
                    style: TextStyle(
                      fontSize: 15,
                      height: 1.4,
                      color: isDark ? Colors.white : Colors.black,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 32),

            // Scientific References
            if (interaction.scientificReferences.isNotEmpty) ...[
              Text(
                'Scientific References',
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                      color: isDark ? Colors.white : Colors.black,
                    ),
              ),
              const SizedBox(height: 12),
              ...interaction.scientificReferences.map((ref) => Padding(
                    padding: const EdgeInsets.only(bottom: 8),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('• ', style: TextStyle(fontSize: 18)),
                        Expanded(
                          child: Text(
                            ref,
                            style: TextStyle(
                              fontSize: 14,
                              color:
                                  isDark ? Colors.grey[400] : Colors.grey[600],
                              fontStyle: FontStyle.italic,
                            ),
                          ),
                        ),
                      ],
                    ),
                  )),
            ],

            const SizedBox(height: 48),

            // Actions
            SizedBox(
              width: double.infinity,
              height: 56,
              child: ElevatedButton(
                onPressed: () {
                  // Navigate to override confirmation or just back
                  Navigator.pop(context);
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary,
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                ),
                child: const Text(
                  'I Understand',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                ),
              ),
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              height: 56,
              child: OutlinedButton(
                onPressed: () {
                  // Navigate to override confirmation screen with interaction data
                  Navigator.pushNamed(
                    context,
                    AppRouter.safetyOverrideConfirmation,
                    arguments: interaction,
                  );
                },
                style: OutlinedButton.styleFrom(
                  foregroundColor: Colors.red[400],
                  side: BorderSide(color: Colors.red[400]!),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                ),
                child: const Text('Override Warning'),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSeverityHeader(InteractionSeverity severity) {
    final color = _getSeverityColor(severity);
    final icon = _getSeverityIcon(severity);
    final label = _getSeverityLabel(severity);

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(vertical: 24),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(24),
      ),
      child: Column(
        children: [
          Icon(icon, color: color, size: 48),
          const SizedBox(height: 12),
          Text(
            label,
            style: TextStyle(
              color: color,
              fontSize: 20,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }

  Color _getSeverityColor(InteractionSeverity severity) {
    switch (severity) {
      case InteractionSeverity.critical:
        return Colors.red;
      case InteractionSeverity.caution:
        return Colors.orange;
      case InteractionSeverity.stable:
        return Colors.blue;
    }
  }

  IconData _getSeverityIcon(InteractionSeverity severity) {
    switch (severity) {
      case InteractionSeverity.critical:
        return Icons.warning_amber_rounded;
      case InteractionSeverity.caution:
        return Icons.info_outline;
      case InteractionSeverity.stable:
        return Icons.check_circle_outline;
    }
  }

  String _getSeverityLabel(InteractionSeverity severity) {
    switch (severity) {
      case InteractionSeverity.critical:
        return 'CRITICAL WARNING';
      case InteractionSeverity.caution:
        return 'CAUTION ADVISED';
      case InteractionSeverity.stable:
        return 'STABLE';
    }
  }
}
