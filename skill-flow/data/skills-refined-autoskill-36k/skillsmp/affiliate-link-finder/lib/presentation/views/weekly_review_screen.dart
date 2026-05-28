import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import 'package:google_fonts/google_fonts.dart';
import '../widgets/weekly_win_card.dart';
import '../widgets/consistency_tracker.dart';
import '../widgets/focus_comparison_chart.dart';

import 'package:provider/provider.dart';
import '../../application/providers/auth_provider.dart';
import '../../application/view_models/weekly_review_view_model.dart';

class WeeklyReviewScreen extends StatelessWidget {
  const WeeklyReviewScreen({super.key});

  static Widget withProvider() {
    return Consumer<AuthProvider>(
      builder: (context, auth, _) => ChangeNotifierProvider(
        create: (_) => WeeklyReviewViewModel.withParams(auth.user?.id ?? '')
          ..fetchWeeklyStats(),
        child: const WeeklyReviewScreen(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Consumer<WeeklyReviewViewModel>(
      builder: (context, viewModel, child) {
        if (viewModel.isLoading) {
          return const Scaffold(
            body: Center(child: CircularProgressIndicator()),
          );
        }

        return Scaffold(
          backgroundColor:
              isDark ? AppColors.backgroundDark : AppColors.backgroundLight,
          body: Stack(
            children: [
              // Confetti Background Pattern
              Positioned.fill(
                child: CustomPaint(
                  painter: ConfettiPatternPainter(
                    color: isDark
                        ? Colors.white.withValues(alpha: 0.05)
                        : Colors.black.withValues(alpha: 0.05),
                  ),
                ),
              ),

              Column(
                children: [
                  // Top App Bar Area
                  Container(
                    padding: EdgeInsets.only(
                      top: MediaQuery.of(context).padding.top + 8,
                      left: 16,
                      right: 16,
                      bottom: 8,
                    ),
                    color: (isDark
                            ? AppColors.backgroundDark
                            : AppColors.backgroundLight)
                        .withValues(alpha: 0.8),
                    child: Row(
                      children: [
                        IconButton(
                          icon: Icon(Icons.close,
                              color: isDark ? Colors.white : Colors.black),
                          onPressed: () => Navigator.pop(context),
                        ),
                        Expanded(
                          child: Text(
                            'Weekly Review',
                            textAlign: TextAlign.center,
                            style: GoogleFonts.lexend(
                              color: isDark ? Colors.white : Colors.black,
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                        IconButton(
                          icon: const Icon(Icons.auto_awesome,
                              color: AppColors.primary),
                          onPressed: () {
                            // Show insights or tips
                            showDialog<void>(
                              context: context,
                              builder: (context) => AlertDialog(
                                title: const Text('AI Analysis'),
                                content: Text(
                                    'Your consistency has improved by ${viewModel.focusImprovement.toStringAsFixed(1)}% compared to last week. Great job maintaining your streak!'),
                                actions: [
                                  TextButton(
                                    onPressed: () => Navigator.pop(context),
                                    child: const Text('Close'),
                                  ),
                                ],
                              ),
                            );
                          },
                        ),
                      ],
                    ),
                  ),

                  // Scrolling Content
                  Expanded(
                    child: SingleChildScrollView(
                      padding: const EdgeInsets.only(bottom: 100),
                      child: Column(
                        children: [
                          Padding(
                            padding: const EdgeInsets.all(16.0),
                            child: WeeklyWinCard(
                              streakDays: viewModel.streakDays,
                              focusImprovement: viewModel.focusImprovement,
                            ),
                          ),
                          ConsistencyTracker(
                            consistencyMap: viewModel.consistencyMap,
                          ),
                          const SizedBox(height: 16),
                          const FocusComparisonChart(),

                          // Weekly Tip
                          Padding(
                            padding: const EdgeInsets.all(16.0),
                            child: Container(
                              padding: const EdgeInsets.all(16),
                              decoration: BoxDecoration(
                                color: AppColors.primary.withValues(alpha: 0.1),
                                borderRadius: BorderRadius.circular(16),
                                border: Border.all(
                                    color: AppColors.primary
                                        .withValues(alpha: 0.1)),
                              ),
                              child: Row(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const Icon(Icons.lightbulb,
                                      color: AppColors.primary),
                                  const SizedBox(width: 12),
                                  Expanded(
                                    child: Column(
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      children: [
                                        Text(
                                          'Weekly Tip',
                                          style: GoogleFonts.lexend(
                                            color: AppColors.primary,
                                            fontWeight: FontWeight.bold,
                                            fontSize: 14,
                                          ),
                                        ),
                                        const SizedBox(height: 4),
                                        Text(
                                          'Taking your supplement with a high-protein breakfast improved your focus score by ${viewModel.focusImprovement.toStringAsFixed(0)}% this week. Try to keep this habit!',
                                          style: GoogleFonts.lexend(
                                            color: isDark
                                                ? Colors.grey[400]
                                                : Colors.grey[700],
                                            fontSize: 12,
                                            height: 1.4,
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),

              // Fixed Bottom Bar
              Positioned(
                left: 0,
                right: 0,
                bottom: 0,
                child: Container(
                  padding: EdgeInsets.fromLTRB(
                      16, 16, 16, MediaQuery.of(context).padding.bottom + 16),
                  decoration: BoxDecoration(
                    color: (isDark
                            ? AppColors.backgroundDark
                            : AppColors.backgroundLight)
                        .withValues(alpha: 0.95),
                    border: Border(
                      top: BorderSide(
                          color: isDark ? Colors.white12 : Colors.grey[200]!),
                    ),
                  ),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      SizedBox(
                        width: double.infinity,
                        height: 56,
                        child: ElevatedButton(
                          onPressed: () {
                            // Show share options dialog
                            showDialog<void>(
                              context: context,
                              builder: (context) => AlertDialog(
                                title: const Text('Share Weekly Progress'),
                                content: const Text(
                                  'Share your weekly supplement progress with your doctor, accountability partner, or social media.',
                                ),
                                actions: [
                                  TextButton(
                                    onPressed: () => Navigator.pop(context),
                                    child: const Text('Cancel'),
                                  ),
                                  TextButton(
                                    onPressed: () {
                                      Navigator.pop(context);
                                      ScaffoldMessenger.of(context)
                                          .showSnackBar(
                                        const SnackBar(
                                          content: Text('Progress shared!'),
                                        ),
                                      );
                                    },
                                    child: const Text('Share'),
                                  ),
                                ],
                              ),
                            );
                          },
                          style: ElevatedButton.styleFrom(
                            backgroundColor: AppColors.primary,
                            foregroundColor: Colors.white,
                            elevation: 8,
                            shadowColor:
                                AppColors.primary.withValues(alpha: 0.4),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(16),
                            ),
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Icon(Icons.share, size: 20),
                              const SizedBox(width: 8),
                              Text(
                                // Removed const due to google_fonts usage check if needed
                                'Share Progress',
                                style: GoogleFonts.lexend(
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                      const SizedBox(height: 12),
                      TextButton(
                        onPressed: () => Navigator.pop(context),
                        child: Text(
                          'Dismiss',
                          style: GoogleFonts.lexend(
                            color: isDark ? Colors.grey[500] : Colors.grey[500],
                            fontSize: 14,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}

class ConfettiPatternPainter extends CustomPainter {
  final Color color;

  ConfettiPatternPainter({required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..style = PaintingStyle.fill;

    // Draw a repeatable dot pattern
    const double spacing = 40.0;
    for (double y = 0; y < size.height; y += spacing) {
      for (double x = 0; x < size.width; x += spacing) {
        // Add some randomness or offset if desired, but grid is simple
        double offsetX = (y / spacing).round() % 2 == 0 ? 0 : spacing / 2;
        canvas.drawCircle(Offset(x + offsetX, y), 1.5, paint);
      }
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
