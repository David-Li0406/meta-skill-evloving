import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/app_theme.dart';
import '../navigation/app_router.dart';

class LateDoseTriageScreen extends StatefulWidget {
  const LateDoseTriageScreen({super.key});

  @override
  State<LateDoseTriageScreen> createState() => _LateDoseTriageScreenState();
}

class _LateDoseTriageScreenState extends State<LateDoseTriageScreen> {
  int _selectedOption = 0; // 0: Took now, 1: Skipped, 2: Took on time

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    const primaryGold = AppColors.primaryGold;
    final bgColor = isDark
        ? AppColors.backgroundPremiumDark
        : AppColors.backgroundPremiumLight;
    final surfaceColor = isDark ? const Color(0xFF1E1E1E) : Colors.white;

    return Scaffold(
      backgroundColor: bgColor,
      body: SafeArea(
        child: Column(
          children: [
            // Handle and App Bar
            Padding(
              padding: const EdgeInsets.only(top: 12, bottom: 8),
              child: Column(
                children: [
                  Container(
                    width: 48,
                    height: 4,
                    decoration: BoxDecoration(
                      color: isDark
                          ? Colors.white.withValues(alpha: 0.1)
                          : Colors.grey[300],
                      borderRadius: BorderRadius.circular(2),
                    ),
                  ),
                  const SizedBox(height: 12),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 24),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const SizedBox(width: 60), // Spacer
                        Text(
                          'TRIAGE',
                          style: GoogleFonts.lexend(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                            letterSpacing: 2.0,
                            color: isDark ? Colors.white : Colors.black,
                          ),
                        ),
                        SizedBox(
                          width: 60,
                          child: Align(
                            alignment: Alignment.centerRight,
                            child: TextButton(
                              onPressed: () => Navigator.pushReplacementNamed(
                                  context, AppRouter.dashboard),
                              child: Text(
                                'Close',
                                style: GoogleFonts.lexend(
                                  color: primaryGold,
                                  fontWeight: FontWeight.bold,
                                  fontSize: 14,
                                ),
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),

            Expanded(
              child: SingleChildScrollView(
                padding:
                    const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                child: Column(
                  children: [
                    // Hero Icon
                    Stack(
                      alignment: Alignment.center,
                      children: [
                        Container(
                          width: 100,
                          height: 100,
                          decoration: BoxDecoration(
                            color: primaryGold.withValues(alpha: 0.1),
                            shape: BoxShape.circle,
                            border: Border.all(
                                color: primaryGold.withValues(alpha: 0.2)),
                          ),
                          child: const Icon(
                            Icons.timer_outlined,
                            size: 48,
                            color: primaryGold,
                          ),
                        ),
                        Positioned(
                          bottom: 0,
                          right: 0,
                          child: Container(
                            padding: const EdgeInsets.all(4),
                            decoration: BoxDecoration(
                              color: bgColor,
                              shape: BoxShape.circle,
                            ),
                            child: Container(
                              width: 20,
                              height: 20,
                              decoration: BoxDecoration(
                                color: Colors.redAccent,
                                shape: BoxShape.circle,
                                border: Border.all(
                                  color: bgColor,
                                  width: 2,
                                ),
                              ),
                              child: const Icon(Icons.priority_high,
                                  size: 12, color: Colors.white),
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 32),

                    // Headlines
                    Text(
                      'Late Entry Detected',
                      textAlign: TextAlign.center,
                      style: GoogleFonts.lexend(
                        fontSize: 28,
                        fontWeight: FontWeight.w800,
                        height: 1.1,
                        color: isDark ? Colors.white : Colors.black,
                      ),
                    ),
                    const SizedBox(height: 12),
                    Text(
                      'Log current status to maintain adherence data.',
                      textAlign: TextAlign.center,
                      style: GoogleFonts.lexend(
                        fontSize: 14,
                        color: Colors.grey,
                      ),
                    ),
                    const SizedBox(height: 48),

                    // Options
                    Column(
                      children: [
                        _buildOptionCard(
                          isDark: isDark,
                          index: 0,
                          icon: Icons.bolt,
                          title: 'I took it just now',
                          subtitle: 'Updates your active concentration loop',
                          primaryGold: primaryGold,
                          surfaceColor: surfaceColor,
                        ),
                        const SizedBox(height: 16),
                        _buildOptionCard(
                          isDark: isDark,
                          index: 1,
                          icon: Icons.block_flipped,
                          title: 'Skipping this one',
                          subtitle: 'Safety first • Reset for next window',
                          primaryGold: primaryGold,
                          surfaceColor: surfaceColor,
                        ),
                        const SizedBox(height: 16),
                        _buildOptionCard(
                          isDark: isDark,
                          index: 2,
                          icon: Icons.history,
                          title: 'I actually took it on time',
                          subtitle: 'Fixing historical adherence record',
                          primaryGold: primaryGold,
                          surfaceColor: surfaceColor,
                        ),
                      ],
                    ),

                    const SizedBox(height: 32),

                    // Safety Tip
                    Container(
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        color: primaryGold.withValues(alpha: 0.05),
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(
                            color: primaryGold.withValues(alpha: 0.1)),
                      ),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Icon(
                            Icons.privacy_tip_outlined,
                            size: 20,
                            color: primaryGold,
                          ),
                          const SizedBox(width: 16),
                          Expanded(
                            child: Text(
                              'Accurate logging ensures your personalized focus predictions remain precise.',
                              style: GoogleFonts.lexend(
                                fontSize: 13,
                                height: 1.4,
                                color: isDark
                                    ? Colors.grey[400]
                                    : Colors.grey[700],
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),

            // Footer
            Container(
              padding: const EdgeInsets.fromLTRB(24, 0, 24, 40),
              child: SizedBox(
                width: double.infinity,
                height: 64,
                child: ElevatedButton(
                  onPressed: () {
                    final decision = _selectedOption == 0
                        ? 'Took medication late'
                        : (_selectedOption == 1
                            ? 'Skipped dose'
                            : 'Took on time');

                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text('Logged: $decision',
                            style: GoogleFonts.lexend()),
                        backgroundColor: primaryGold,
                      ),
                    );

                    Future.delayed(const Duration(milliseconds: 500), () {
                      if (context.mounted) {
                        Navigator.pushReplacementNamed(
                            context, AppRouter.dashboard);
                      }
                    });
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: primaryGold,
                    foregroundColor: Colors.black,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(32),
                    ),
                    elevation: 8,
                    shadowColor: primaryGold.withValues(alpha: 0.4),
                  ),
                  child: Text(
                    'Confirm Decision',
                    style: GoogleFonts.lexend(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildOptionCard({
    required bool isDark,
    required int index,
    required IconData icon,
    required String title,
    required String subtitle,
    required Color primaryGold,
    required Color surfaceColor,
  }) {
    final isSelected = _selectedOption == index;
    final borderColor = isSelected
        ? primaryGold
        : (isDark ? Colors.white.withValues(alpha: 0.05) : Colors.grey[200]!);
    final bgColor =
        isSelected ? primaryGold.withValues(alpha: 0.05) : surfaceColor;

    return InkWell(
      onTap: () => setState(() => _selectedOption = index),
      borderRadius: BorderRadius.circular(24),
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: bgColor,
          borderRadius: BorderRadius.circular(24),
          border: Border.all(color: borderColor, width: isSelected ? 2 : 1),
          boxShadow: isSelected
              ? [
                  BoxShadow(
                    color: primaryGold.withValues(alpha: 0.1),
                    blurRadius: 10,
                    offset: const Offset(0, 4),
                  )
                ]
              : null,
        ),
        child: Row(
          children: [
            Container(
              width: 48,
              height: 48,
              decoration: BoxDecoration(
                color: isSelected
                    ? primaryGold.withValues(alpha: 0.1)
                    : (isDark
                        ? Colors.black.withValues(alpha: 0.2)
                        : Colors.grey[100]),
                borderRadius: BorderRadius.circular(16),
              ),
              child: Icon(
                icon,
                color: isSelected ? primaryGold : Colors.grey,
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
                    style: GoogleFonts.lexend(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: isDark ? Colors.white : Colors.black,
                    ),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    subtitle,
                    style: GoogleFonts.lexend(
                      fontSize: 12,
                      color: Colors.grey,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(width: 12),
            Container(
              width: 24,
              height: 24,
              decoration: BoxDecoration(
                color: isSelected ? primaryGold : Colors.transparent,
                shape: BoxShape.circle,
                border: Border.all(
                  color: isSelected
                      ? primaryGold
                      : Colors.grey.withValues(alpha: 0.3),
                  width: 2,
                ),
              ),
              child: isSelected
                  ? const Icon(Icons.check, size: 14, color: Colors.black)
                  : null,
            ),
          ],
        ),
      ),
    );
  }
}
