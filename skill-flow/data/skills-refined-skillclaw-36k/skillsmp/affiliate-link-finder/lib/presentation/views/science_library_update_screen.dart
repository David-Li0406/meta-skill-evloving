import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class ScienceLibraryUpdateScreen extends StatelessWidget {
  const ScienceLibraryUpdateScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    const primaryColor = AppColors.primary;

    // Background colors
    final Color bgColor =
        isDark ? const Color(0xFF101622) : const Color(0xFFF6F7F8);
    final Color cardColor = isDark ? const Color(0xFF1A1D24) : Colors.white;
    final Color textColor = isDark ? Colors.white : const Color(0xFF0F172A);
    final Color textSecondary =
        isDark ? const Color(0xFF94A3B8) : const Color(0xFF475569);

    return Scaffold(
      backgroundColor: bgColor,
      body: SafeArea(
        child: Column(
          children: [
            // Header / Eyebrow
            Padding(
              padding: const EdgeInsets.only(top: 32, bottom: 16),
              child: Text(
                'SCIENCE REFRESH',
                style: TextStyle(
                  fontSize: 11,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 2.0,
                  color: primaryColor.withValues(alpha: isDark ? 1.0 : 0.8),
                ),
              ),
            ),

            // Hero Section (Scrollable part if needed, but fitting to single screen mostly)
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.symmetric(horizontal: 24),
                child: Column(
                  children: [
                    // Illustration
                    Padding(
                      padding: const EdgeInsets.symmetric(vertical: 24),
                      child: Stack(
                        alignment: Alignment.center,
                        children: [
                          // Glow Effect
                          Container(
                            width: 256,
                            height: 256,
                            decoration: BoxDecoration(
                              color:
                                  primaryColor.withValues(alpha: isDark ? 0.1 : 0.2),
                              shape: BoxShape.circle,
                              boxShadow: [
                                BoxShadow(
                                  color: primaryColor.withValues(alpha: 0.2),
                                  blurRadius: 60,
                                  spreadRadius: 20,
                                ),
                              ],
                            ),
                          ),
                          // Hero Image (Placeholder for the 3D magnifying glass)
                          Container(
                            width: 200,
                            height: 200,
                            decoration: BoxDecoration(
                              color: isDark
                                  ? const Color(0xFF282E39)
                                  : Colors.blue.shade50,
                              borderRadius: BorderRadius.circular(24),
                              gradient: LinearGradient(
                                begin: Alignment.topLeft,
                                end: Alignment.bottomRight,
                                colors: isDark
                                    ? [
                                        const Color(0xFF384354),
                                        const Color(0xFF1c2027)
                                      ]
                                    : [Colors.blue.shade100, Colors.white],
                              ),
                            ),
                            child: const Icon(
                              Icons.manage_search_rounded, // Fallback icon
                              size: 100,
                              color: primaryColor,
                            ),
                            // In a real app, use Image.network or specific asset
                            // child: Image.network("https://lh3.googleusercontent.com/...", fit: BoxFit.contain),
                          ),
                        ],
                      ),
                    ),

                    // Headline
                    Text(
                      'New Research In!',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 32,
                        fontWeight: FontWeight.w800,
                        color: textColor,
                        height: 1.1,
                        letterSpacing: -0.5,
                      ),
                    ),
                    const SizedBox(height: 16),
                    // Body Text
                    Text(
                      'We’ve updated our library with the latest clinical studies on ADHD management.',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w500,
                        color: textSecondary,
                        height: 1.5,
                      ),
                    ),

                    const SizedBox(height: 32),

                    // Updates List Card
                    Container(
                      decoration: BoxDecoration(
                        color: cardColor,
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(
                          color: isDark
                              ? Colors.white.withValues(alpha: 0.05)
                              : Colors.grey.shade200,
                        ),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withValues(alpha: 0.03),
                            blurRadius: 10,
                            offset: const Offset(0, 4),
                          ),
                        ],
                      ),
                      child: Column(
                        children: [
                          _buildListItem(
                            isDark: isDark,
                            primaryColor: primaryColor,
                            textColor: textColor,
                            textSecondary: textSecondary,
                            icon: Icons.science_outlined,
                            title: '3 New Supplements Added',
                            subtitle: 'Clinical efficacy review',
                          ),
                          Divider(
                              height: 1,
                              color: isDark
                                  ? Colors.white.withValues(alpha: 0.05)
                                  : Colors.grey.shade100,
                              indent: 20,
                              endIndent: 20),
                          _buildListItem(
                            isDark: isDark,
                            primaryColor: primaryColor,
                            textColor: textColor,
                            textSecondary: textSecondary,
                            icon: Icons.health_and_safety_outlined,
                            title: 'Updated Safety Guidelines',
                            subtitle: 'Adderall interaction update',
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 24),
                  ],
                ),
              ),
            ),

            // Bottom Actions
            Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                children: [
                  SizedBox(
                    width: double.infinity,
                    height: 56,
                    child: ElevatedButton(
                      onPressed: () {
                        Navigator.pop(
                            context); // Close for now, logic needed to open specific tab
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                              content: Text('Science Library updated!')),
                        );
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: primaryColor,
                        foregroundColor: Colors.white,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(28),
                        ),
                        elevation: 8,
                        shadowColor: primaryColor.withValues(alpha: 0.4),
                      ),
                      child: const Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            'View New Science',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          SizedBox(width: 8),
                          Icon(Icons.arrow_forward_rounded, size: 20),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),
                  TextButton(
                    onPressed: () => Navigator.pop(context),
                    child: Text(
                      'Maybe Later',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w600,
                        color: textSecondary,
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

  Widget _buildListItem({
    required bool isDark,
    required Color primaryColor,
    required Color textColor,
    required Color textSecondary,
    required IconData icon,
    required String title,
    required String subtitle,
  }) {
    return InkWell(
      onTap: () {},
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Row(
          children: [
            Container(
              width: 48,
              height: 48,
              decoration: BoxDecoration(
                color: isDark
                    ? const Color(0xFF282e39)
                    : primaryColor.withValues(alpha: 0.1),
                shape: BoxShape.circle,
              ),
              child: Icon(
                icon,
                color: primaryColor,
                size: 24,
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: TextStyle(
                      fontSize: 15,
                      fontWeight: FontWeight.bold,
                      color: textColor,
                    ),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    subtitle,
                    style: TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.w500,
                      color: textSecondary,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(width: 12),
            Container(
              width: 10,
              height: 10,
              decoration: BoxDecoration(
                color: const Color(0xFF0bdA5e),
                shape: BoxShape.circle,
                boxShadow: [
                  BoxShadow(
                    color: const Color(0xFF0bdA5e).withValues(alpha: 0.4),
                    blurRadius: 8,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
