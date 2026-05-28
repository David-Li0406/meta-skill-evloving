import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:url_launcher/url_launcher.dart';
import '../theme/app_theme.dart';
import '../navigation/app_router.dart';

class NotificationReliabilitySetupScreen extends StatefulWidget {
  const NotificationReliabilitySetupScreen({super.key});

  @override
  State<NotificationReliabilitySetupScreen> createState() =>
      _NotificationReliabilitySetupScreenState();
}

class _NotificationReliabilitySetupScreenState
    extends State<NotificationReliabilitySetupScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController _pulseController;
  late Animation<double> _pulseAnimation;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 3),
    )..repeat(reverse: true);

    _pulseAnimation = Tween<double>(begin: 1.0, end: 1.05).animate(
      CurvedAnimation(parent: _pulseController, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _pulseController.dispose();
    super.dispose();
  }

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
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios_new,
              color: isDark ? Colors.white : Colors.black),
          onPressed: () =>
              Navigator.pushReplacementNamed(context, AppRouter.dashboard),
        ),
        title: Text(
          'RELIABILITY',
          style: GoogleFonts.lexend(
            color: isDark ? Colors.white : Colors.black,
            fontSize: 14,
            fontWeight: FontWeight.bold,
            letterSpacing: 2.0,
          ),
        ),
        centerTitle: true,
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.fromLTRB(24, 24, 24, 40),
                child: Column(
                  children: [
                    // Hero Illustration
                    Padding(
                      padding: const EdgeInsets.symmetric(vertical: 32),
                      child: Stack(
                        alignment: Alignment.center,
                        children: [
                          Container(
                            width: 180,
                            height: 180,
                            decoration: BoxDecoration(
                              color: primaryGold.withValues(alpha: 0.1),
                              shape: BoxShape.circle,
                            ),
                          ),
                          Stack(
                            clipBehavior: Clip.none,
                            children: [
                              Container(
                                padding: const EdgeInsets.all(32),
                                decoration: BoxDecoration(
                                  color: surfaceColor,
                                  borderRadius: BorderRadius.circular(32),
                                  border: Border.all(
                                    color: primaryGold.withValues(alpha: 0.2),
                                  ),
                                  boxShadow: [
                                    BoxShadow(
                                      color:
                                          Colors.black.withValues(alpha: 0.1),
                                      blurRadius: 30,
                                      offset: const Offset(0, 15),
                                    ),
                                  ],
                                ),
                                child: const Icon(
                                  Icons.notifications_active_outlined,
                                  size: 64,
                                  color: primaryGold,
                                ),
                              ),
                              Positioned(
                                bottom: -12,
                                right: -12,
                                child: AnimatedBuilder(
                                  animation: _pulseAnimation,
                                  builder: (context, child) {
                                    return Transform.scale(
                                      scale: _pulseAnimation.value,
                                      child: child,
                                    );
                                  },
                                  child: Container(
                                    padding: const EdgeInsets.all(10),
                                    decoration: BoxDecoration(
                                      color: primaryGold,
                                      borderRadius: BorderRadius.circular(16),
                                      border: Border.all(
                                        color: bgColor,
                                        width: 4,
                                      ),
                                      boxShadow: [
                                        BoxShadow(
                                          color: primaryGold.withValues(
                                              alpha: 0.4),
                                          blurRadius: 15,
                                          offset: const Offset(0, 5),
                                        ),
                                      ],
                                    ),
                                    child: const Icon(
                                      Icons.lock_clock_outlined,
                                      size: 28,
                                      color: Colors.black,
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),

                    // Headline
                    Text(
                      "Don't Miss a Nudge",
                      textAlign: TextAlign.center,
                      style: GoogleFonts.lexend(
                        color: isDark ? Colors.white : Colors.black,
                        fontSize: 28,
                        fontWeight: FontWeight.w800,
                        height: 1.1,
                      ),
                    ),
                    const SizedBox(height: 16),
                    Text(
                      "ADHD brains rely on external cues. Let's ensure your phone doesn't silence your critical health loops.",
                      textAlign: TextAlign.center,
                      style: GoogleFonts.lexend(
                        color: Colors.grey,
                        fontSize: 15,
                        height: 1.5,
                      ),
                    ),
                    const SizedBox(height: 48),

                    // Step 1
                    _buildStepCard(
                      context,
                      isDark: isDark,
                      number: '1',
                      title: 'Tap "Configure Flow"',
                      subtitle: 'Opens system notification relay',
                      trailing: const Icon(
                        Icons.touch_app_outlined,
                        color: primaryGold,
                        size: 20,
                      ),
                      primaryGold: primaryGold,
                      surfaceColor: surfaceColor,
                    ),
                    const SizedBox(height: 16),

                    // Step 2
                    _buildStepCard(
                      context,
                      isDark: isDark,
                      number: '2',
                      title: 'Enable Full Relays',
                      subtitle: 'Toggle persistent status to ON',
                      trailing: Container(
                        width: 44,
                        height: 24,
                        decoration: BoxDecoration(
                          color: primaryGold,
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Align(
                          alignment: Alignment.centerRight,
                          child: Container(
                            margin: const EdgeInsets.all(2),
                            width: 20,
                            height: 20,
                            decoration: const BoxDecoration(
                              color: Colors.black,
                              shape: BoxShape.circle,
                            ),
                          ),
                        ),
                      ),
                      primaryGold: primaryGold,
                      surfaceColor: surfaceColor,
                    ),
                  ],
                ),
              ),
            ),

            // Fixed Bottom Actions
            Container(
              padding: const EdgeInsets.fromLTRB(24, 0, 24, 40),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  SizedBox(
                    width: double.infinity,
                    height: 64,
                    child: ElevatedButton(
                      onPressed: () async {
                        final uri = Uri.parse('app-settings:');
                        if (await canLaunchUrl(uri)) {
                          await launchUrl(uri);
                        }
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: primaryGold,
                        foregroundColor: Colors.black,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(32),
                        ),
                        elevation: 12,
                        shadowColor: primaryGold.withValues(alpha: 0.4),
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            'Configure Flow',
                            style: GoogleFonts.lexend(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(width: 12),
                          const Icon(Icons.settings_suggest, size: 22),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),
                  TextButton(
                    onPressed: () => Navigator.pushReplacementNamed(
                        context, AppRouter.dashboard),
                    child: Text(
                      'Dismiss for now',
                      style: GoogleFonts.lexend(
                        color: Colors.grey,
                        fontSize: 14,
                        fontWeight: FontWeight.w600,
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

  Widget _buildStepCard(
    BuildContext context, {
    required bool isDark,
    required String number,
    required String title,
    required String subtitle,
    required Widget trailing,
    required Color primaryGold,
    required Color surfaceColor,
  }) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: surfaceColor,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(
          color: primaryGold.withValues(alpha: 0.1),
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Row(
        children: [
          Container(
            width: 52,
            height: 52,
            decoration: BoxDecoration(
              color: primaryGold.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(16),
            ),
            child: Center(
              child: Text(
                number,
                style: GoogleFonts.lexend(
                  color: primaryGold,
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
          const SizedBox(width: 20),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: GoogleFonts.lexend(
                    color: isDark ? Colors.white : Colors.black,
                    fontSize: 15,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  subtitle,
                  style: GoogleFonts.lexend(
                    color: Colors.grey,
                    fontSize: 12,
                  ),
                ),
              ],
            ),
          ),
          trailing,
        ],
      ),
    );
  }
}
