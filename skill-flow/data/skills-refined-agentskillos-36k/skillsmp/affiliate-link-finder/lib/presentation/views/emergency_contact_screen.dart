import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import '../../utils/logger.dart';
import '../theme/app_theme.dart';

class EmergencyContactScreen extends StatelessWidget {
  const EmergencyContactScreen({super.key});

  Future<void> _makeCall(String number) async {
    final Uri launchUri = Uri(
      scheme: 'tel',
      path: number,
    );
    if (await canLaunchUrl(launchUri)) {
      await launchUrl(launchUri);
    } else {
      // In a real app, show error dialog
      AppLogger.e('Could not launch $launchUri');
    }
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Emergency Support'),
        centerTitle: true,
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            // Warning Banner
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.red.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Colors.red.withValues(alpha: 0.3)),
              ),
              child: Row(
                children: [
                  const Icon(Icons.warning_amber_rounded,
                      color: Colors.red, size: 32),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Text(
                      'If you are experiencing a life-threatening medical emergency, please call emergency services immediately.',
                      style: TextStyle(
                        color: isDark ? Colors.red[200] : Colors.red[800],
                        fontSize: 14,
                        height: 1.4,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 32),

            // Emergency Services Button (Big Red Button)
            SizedBox(
              width: double.infinity,
              height: 72,
              child: ElevatedButton.icon(
                onPressed: () => _makeCall('911'), // Localize this in real app
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.red,
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20),
                  ),
                  elevation: 4,
                  shadowColor: Colors.red.withValues(alpha: 0.4),
                ),
                icon: const Icon(Icons.emergency, size: 32),
                label: const Text(
                  'Call Emergency Services',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Poison Control / Crisis Line
            _buildContactCard(
              context,
              title: 'Poison Control Center',
              subtitle: 'For accidental overdoses or interactions',
              number: '1-800-222-1222', // US Poison Control
              icon: Icons.local_hospital,
              color: Colors.orange,
              isDark: isDark,
            ),
            const SizedBox(height: 12),

            _buildContactCard(
              context,
              title: 'Suicide & Crisis Lifeline',
              subtitle: 'Free and confidential support 24/7',
              number: '988',
              icon: Icons.favorite,
              color: Colors.purple,
              isDark: isDark,
            ),

            const SizedBox(height: 32),
            const Divider(),
            const SizedBox(height: 32),

            // Personal Contacts Header
            Row(
              children: [
                Text(
                  'Your Contacts',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: isDark ? Colors.white : Colors.black87,
                  ),
                ),
                const Spacer(),
                IconButton(
                  icon: const Icon(Icons.edit),
                  onPressed: () {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                          content: Text('Edit contacts coming soon')),
                    );
                  },
                ),
              ],
            ),
            const SizedBox(height: 16),

            // Doctor / Pharmacy Placeholders
            _buildContactCard(
              context,
              title: 'Dr. Sarah Chen (Psychiatrist)',
              subtitle: 'Primary Prescriber',
              number: '555-0123',
              icon: Icons.calendar_today, // Appointment/Doctor icon
              color: AppColors.primary,
              isDark: isDark,
            ),
            const SizedBox(height: 12),
            _buildContactCard(
              context,
              title: 'CVS Pharmacy #4122',
              subtitle: 'On Main St.',
              number: '555-0199',
              icon: Icons.local_pharmacy,
              color: Colors.green,
              isDark: isDark,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildContactCard(
    BuildContext context, {
    required String title,
    required String subtitle,
    required String number,
    required IconData icon,
    required Color color,
    required bool isDark,
  }) {
    return Container(
      decoration: BoxDecoration(
        color: isDark ? Colors.white.withValues(alpha: 0.05) : Colors.grey[100],
        borderRadius: BorderRadius.circular(16),
      ),
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
        leading: Container(
          padding: const EdgeInsets.all(10),
          decoration: BoxDecoration(
            color: color.withValues(alpha: 0.1),
            shape: BoxShape.circle,
          ),
          child: Icon(icon, color: color),
        ),
        title: Text(
          title,
          style: TextStyle(
            fontWeight: FontWeight.bold,
            color: isDark ? Colors.white : Colors.black87,
          ),
        ),
        subtitle: Text(
          subtitle,
          style: TextStyle(
            color: isDark ? Colors.grey[400] : Colors.grey[600],
          ),
        ),
        trailing: Container(
          decoration: BoxDecoration(
            color: Colors.green.withValues(alpha: 0.1),
            shape: BoxShape.circle,
          ),
          child: IconButton(
            icon: const Icon(Icons.phone, color: Colors.green),
            onPressed: () => _makeCall(number),
          ),
        ),
      ),
    );
  }
}
