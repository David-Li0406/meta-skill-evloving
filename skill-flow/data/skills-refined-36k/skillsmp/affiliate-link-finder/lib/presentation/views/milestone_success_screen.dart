import 'package:flutter/material.dart';
import 'package:share_plus/share_plus.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/app_theme.dart';
import '../widgets/particles_background.dart';

class MilestoneSuccessScreen extends StatefulWidget {
  final int days;

  const MilestoneSuccessScreen({
    super.key,
    this.days = 30, // Default to 30 for MVP
  });

  @override
  State<MilestoneSuccessScreen> createState() => _MilestoneSuccessScreenState();
}

class _MilestoneSuccessScreenState extends State<MilestoneSuccessScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController _scaleController;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _scaleController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 800),
    );

    _scaleAnimation = CurvedAnimation(
      parent: _scaleController,
      curve: Curves.elasticOut,
    );

    _scaleController.forward();
  }

  @override
  void dispose() {
    _scaleController.dispose();
    super.dispose();
  }

  // ignore: unused_element
  void _shareMilestone() {
    Share.share(
      'I just hit a ${widget.days}-day streak on FocusStack! 🚀 Optimizing my ADHD routine one day at a time.',
      subject: 'My FocusStack Milestone',
    );
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      backgroundColor:
          isDark ? AppColors.backgroundDark : AppColors.backgroundLight,
      body: Stack(
        children: [
          // Background Glow/Particles
          Positioned.fill(
            child: Container(
              decoration: BoxDecoration(
                gradient: RadialGradient(
                  center: const Alignment(0, -0.3),
                  radius: 1.2,
                  colors: [
                    AppColors.primaryGold.withValues(alpha: 0.15),
                    Colors.transparent,
                  ],
                ),
              ),
            ),
          ),
          const Positioned.fill(
            child: ParticlesBackground(
              color: AppColors.primaryGold,
              particleCount: 40,
            ),
          ),

          SafeArea(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24.0),
              child: Column(
                children: [
                  const Spacer(),
                  // Bottle Illustration Card
                  ScaleTransition(
                    scale: _scaleAnimation,
                    child: Container(
                      width: double.infinity,
                      decoration: BoxDecoration(
                        color: isDark ? AppColors.cardDark : Colors.white,
                        borderRadius: BorderRadius.circular(32),
                        boxShadow: [
                          BoxShadow(
                            color: AppColors.primaryGold.withValues(alpha: 0.3),
                            blurRadius: 40,
                            offset: const Offset(0, 20),
                          ),
                        ],
                        border: Border.all(
                          color: AppColors.primaryGold.withValues(alpha: 0.2),
                        ),
                      ),
                      child: Column(
                        children: [
                          const SizedBox(height: 40),
                          // The "Shelf" and "Bottle"
                          Stack(
                            alignment: Alignment.center,
                            children: [
                              // Glow behind bottle
                              Container(
                                width: 140,
                                height: 180,
                                decoration: BoxDecoration(
                                  boxShadow: [
                                    BoxShadow(
                                      color: AppColors.primaryGold
                                          .withValues(alpha: 0.4),
                                      blurRadius: 100,
                                      spreadRadius: 20,
                                    ),
                                  ],
                                ),
                              ),
                              // Bottle Illustration (Placeholder for actual image/SVG)
                              Container(
                                width: 100,
                                height: 160,
                                decoration: BoxDecoration(
                                  color: AppColors.primaryGold
                                      .withValues(alpha: 0.9),
                                  borderRadius: BorderRadius.circular(12),
                                  boxShadow: const [
                                    BoxShadow(
                                      color: Colors.black26,
                                      blurRadius: 15,
                                      offset: Offset(0, 10),
                                    ),
                                  ],
                                ),
                                child: const Center(
                                  child: Icon(Icons.bolt,
                                      color: Colors.white, size: 48),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 32),
                          // Achievement Badge
                          Container(
                            padding: const EdgeInsets.symmetric(
                                horizontal: 16, vertical: 8),
                            decoration: BoxDecoration(
                              color: Colors.black.withValues(alpha: 0.1),
                              borderRadius: BorderRadius.circular(20),
                              border: Border.all(
                                  color: AppColors.primaryGold
                                      .withValues(alpha: 0.3)),
                            ),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                const Icon(Icons.star,
                                    color: AppColors.primaryGold, size: 16),
                                const SizedBox(width: 8),
                                Text(
                                  '7 DAY STREAK',
                                  style: GoogleFonts.lexend(
                                    fontWeight: FontWeight.bold,
                                    color: AppColors.primaryGold,
                                    fontSize: 12,
                                    letterSpacing: 1.0,
                                  ),
                                ),
                              ],
                            ),
                          ),
                          const SizedBox(height: 40),
                        ],
                      ),
                    ),
                  ),

                  const SizedBox(height: 48),

                  // Congratulations Text
                  Text(
                    'Your First Stack is Ready!',
                    textAlign: TextAlign.center,
                    style: GoogleFonts.lexend(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                      color: isDark ? Colors.white : AppColors.textPrimaryLight,
                      height: 1.2,
                    ),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'You\'ve successfully built your first focus protocol. Consistency is the secret to neuro-optimization.',
                    textAlign: TextAlign.center,
                    style: GoogleFonts.lexend(
                      fontSize: 16,
                      color: isDark ? Colors.grey[400] : Colors.grey[600],
                      height: 1.5,
                    ),
                  ),

                  const Spacer(),

                  // Action Buttons
                  SizedBox(
                    width: double.infinity,
                    height: 60,
                    child: ElevatedButton(
                      onPressed: () {
                        // Logic to navigate to nudge setup
                        Navigator.pushNamed(context, '/pill-matcher');
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.primaryGold,
                        foregroundColor: Colors.black,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(16),
                        ),
                        elevation: 8,
                        shadowColor:
                            AppColors.primaryGold.withValues(alpha: 0.4),
                      ),
                      child: Text(
                        'Schedule My First Nudge',
                        style: GoogleFonts.lexend(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),
                  TextButton(
                    onPressed: () => Navigator.pop(context),
                    child: Text(
                      'Not now, show my dashboard',
                      style: GoogleFonts.lexend(
                        color: Colors.grey,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                  const SizedBox(height: 24),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
