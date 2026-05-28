import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'dart:math' as math;
import '../../config/locator.dart';
import '../../application/view_models/insights_view_model.dart';
import '../../application/providers/auth_provider.dart';
import '../theme/app_theme.dart';
import '../navigation/app_router.dart';
import '../widgets/unified_bottom_nav.dart';
import '../widgets/skeleton_loader.dart';
import 'package:fl_chart/fl_chart.dart';

/// The main Insights screen.
///
/// Displays the user's current streak and consistency in a gamified, LOW-DOSE information layout.
///
/// Key Features:
/// - **Hero Streak Card**: Prominent display of current streak with ember animation.
/// - **Consistency Bar**: Visual progress towards the 80% consistency goal.
/// - **Encouragement**: Dynamic text to boost motivation.
class InsightsScreen extends StatelessWidget {
  final InsightsViewModel? viewModel;

  const InsightsScreen({super.key, this.viewModel});

  @override
  Widget build(BuildContext context) {
    // Get UserId from AuthProvider to inject into ViewModel
    final userId = context.read<AuthProvider>().user?.id ?? '';

    return ChangeNotifierProvider<InsightsViewModel>(
      create: (_) => viewModel ?? locator<InsightsViewModel>(param1: userId),
      child: const _InsightsContent(),
    );
  }
}

class _InsightsContent extends StatelessWidget {
  const _InsightsContent();

  @override
  Widget build(BuildContext context) {
    final viewModel = context.watch<InsightsViewModel>();
    final isDark = Theme.of(context).brightness == Brightness.dark;
    const primaryGold = AppColors.primaryGold;
    const bgLight = AppColors.backgroundPremiumLight;
    const bgDark = AppColors.backgroundPremiumDark;

    return Scaffold(
      backgroundColor: isDark ? bgDark : bgLight,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios_new),
          onPressed: () =>
              Navigator.pushReplacementNamed(context, AppRouter.dashboard),
        ),
        title: Text(
          'Insights',
          style: GoogleFonts.lexend(fontWeight: FontWeight.bold, fontSize: 18),
        ),
        centerTitle: true,
      ),
      body: viewModel.isLoading
          ? const SingleChildScrollView(
              physics: NeverScrollableScrollPhysics(),
              child: Padding(
                padding: EdgeInsets.symmetric(horizontal: 20, vertical: 20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Header skeleton
                    SkeletonLoader(
                      height: 28,
                      width: 200,
                      borderRadius: 8,
                    ),
                    SizedBox(height: 8),
                    SkeletonLoader(
                      height: 16,
                      width: 150,
                      borderRadius: 6,
                    ),
                    SizedBox(height: 32),
                    // Streak hero skeleton
                    SkeletonLoader(
                      height: 280,
                      borderRadius: 24,
                    ),
                    SizedBox(height: 16),
                    // Consistency card skeleton
                    SkeletonLoader(
                      height: 180,
                      borderRadius: 24,
                    ),
                    SizedBox(height: 16),
                    // Export button skeleton
                    SkeletonLoader(
                      height: 56,
                      borderRadius: 16,
                    ),
                  ],
                ),
              ),
            )
          : SingleChildScrollView(
              physics: const BouncingScrollPhysics(),
              child: Padding(
                padding:
                    const EdgeInsets.symmetric(horizontal: 20, vertical: 20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Encourage Text / Header
                    Text(
                      viewModel.encouragementText,
                      style: GoogleFonts.lexend(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: isDark ? Colors.white : Colors.black,
                        height: 1.2,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Here is your progress so far.',
                      style: GoogleFonts.lexend(
                        fontSize: 14,
                        color: Colors.grey[600],
                      ),
                    ),
                    const SizedBox(height: 32),

                    // Streak Card (Hero)
                    _buildStreakHero(
                        context, viewModel.streakCount, isDark, primaryGold),
                    const SizedBox(height: 16),

                    // Consistency Card
                    _buildConsistencyCard(context, viewModel.consistencyScore,
                        isDark, primaryGold),
                    const SizedBox(height: 16),

                    // Weekly Focus Trends
                    _buildFocusTrendsCard(context, viewModel.weeklyFocusScores,
                        isDark, primaryGold),
                    const SizedBox(height: 16),

                    // Science Hub Nudge
                    _buildScienceNudge(context, isDark),
                    const SizedBox(height: 16),

                    // Export Button
                    SizedBox(
                      width: double.infinity,
                      height: 56,
                      child: ElevatedButton.icon(
                        onPressed: () => Navigator.pushNamed(
                            context, AppRouter.doctorExport),
                        icon: const Icon(Icons.description_outlined),
                        label: Text('Export Report for Doctor',
                            style: GoogleFonts.lexend(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                            )),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: primaryGold,
                          foregroundColor: Colors.black,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(16),
                          ),
                          elevation: 0,
                        ),
                      ),
                    ),
                    const SizedBox(height: 100), // Bottom padding
                  ],
                ),
              ),
            ),
      bottomNavigationBar: const UnifiedBottomNav(currentIndex: 4),
    );
  }

  Widget _buildStreakHero(
      BuildContext context, int streak, bool isDark, Color primaryGold) {
    return Container(
      width: double.infinity,
      height: 280, // Fixed height for animation containment
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF1E1E1E) : Colors.white,
        borderRadius: BorderRadius.circular(24),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Stack(
        children: [
          // Background Embers
          Positioned.fill(
            child: ClipRRect(
              borderRadius: BorderRadius.circular(24),
              child: const _StreakEmberAnimation(),
            ),
          ),

          // Content
          Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: primaryGold.withValues(alpha: 0.1),
                    shape: BoxShape.circle,
                    boxShadow: [
                      BoxShadow(
                        color: primaryGold.withValues(alpha: 0.2),
                        blurRadius: 20,
                        spreadRadius: 5,
                      )
                    ],
                  ),
                  child: const Text('🔥', style: TextStyle(fontSize: 48)),
                ),
                const SizedBox(height: 24),
                Text(
                  '$streak Day Streak',
                  style: GoogleFonts.lexend(
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                    color: isDark ? Colors.white : Colors.black,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  'You are building a powerful habit!',
                  textAlign: TextAlign.center,
                  style: GoogleFonts.lexend(
                    fontSize: 14,
                    color: Colors.grey[600],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildConsistencyCard(BuildContext context, double consistency,
      bool isDark, Color primaryGold) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF1E1E1E) : Colors.white,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(
          color: isDark
              ? Colors.white.withValues(alpha: 0.05)
              : Colors.transparent,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            '30-Day Consistency',
            style: GoogleFonts.lexend(
              fontSize: 16,
              fontWeight: FontWeight.w600,
              color: isDark ? Colors.white : Colors.black,
            ),
          ),
          const SizedBox(height: 20),
          Stack(
            children: [
              Container(
                height: 24,
                width: double.infinity,
                decoration: BoxDecoration(
                  color: isDark ? Colors.grey[800] : Colors.grey[200],
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              LayoutBuilder(
                builder: (context, constraints) {
                  return Container(
                    height: 24,
                    width: constraints.maxWidth * (consistency / 100),
                    decoration: BoxDecoration(
                      color: primaryGold,
                      borderRadius: BorderRadius.circular(12),
                    ),
                  );
                },
              ),
            ],
          ),
          const SizedBox(height: 12),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                '${consistency.toStringAsFixed(0)}%',
                style: GoogleFonts.lexend(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: primaryGold,
                ),
              ),
              Text(
                'Target: 80%+',
                style: GoogleFonts.lexend(
                  fontSize: 12,
                  color: Colors.grey[500],
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildFocusTrendsCard(BuildContext context, List<double> focusScores,
      bool isDark, Color primaryGold) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF1E1E1E) : Colors.white,
        borderRadius: BorderRadius.circular(24),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'Weekly Focus Trend',
                style: GoogleFonts.lexend(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                  color: isDark ? Colors.white : Colors.black,
                ),
              ),
              Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: AppColors.accentGreen.withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  '7-Day View',
                  style: GoogleFonts.lexend(
                    fontSize: 10,
                    fontWeight: FontWeight.bold,
                    color: AppColors.accentGreen,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 32),
          SizedBox(
            height: 180,
            child: LineChart(
              LineChartData(
                gridData: const FlGridData(show: false),
                titlesData: const FlTitlesData(show: false),
                borderData: FlBorderData(show: false),
                minX: 0,
                maxX: 6,
                minY: 0,
                maxY: 5,
                lineBarsData: [
                  LineChartBarData(
                    spots: focusScores.asMap().entries.map((e) {
                      return FlSpot(
                          e.key.toDouble(), e.value == 0 ? 0.2 : e.value);
                    }).toList(),
                    isCurved: true,
                    gradient: LinearGradient(
                      colors: [primaryGold, primaryGold.withValues(alpha: 0.5)],
                    ),
                    barWidth: 4,
                    isStrokeCapRound: true,
                    dotData: const FlDotData(show: false),
                    belowBarData: BarAreaData(
                      show: true,
                      gradient: LinearGradient(
                        colors: [
                          primaryGold.withValues(alpha: 0.2),
                          primaryGold.withValues(alpha: 0.0),
                        ],
                        begin: Alignment.topCenter,
                        end: Alignment.bottomCenter,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: ['M', 'T', 'W', 'T', 'F', 'S', 'S']
                .map((day) => Text(
                      day,
                      style: GoogleFonts.lexend(
                        fontSize: 12,
                        color: Colors.grey[500],
                        fontWeight: FontWeight.w500,
                      ),
                    ))
                .toList(),
          ),
        ],
      ),
    );
  }

  Widget _buildScienceNudge(BuildContext context, bool isDark) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: isDark
              ? [const Color(0xFF2C3E50), const Color(0xFF000000)]
              : [const Color(0xFFE0EAFC), const Color(0xFFCFDEF3)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(24),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.science_outlined, color: AppColors.primaryBlue),
              const SizedBox(width: 8),
              Text(
                'Scientific Insight',
                style: GoogleFonts.lexend(
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                  color: AppColors.primaryBlue,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Text(
            'Did you know? Magnesium supports over 300 enzymatic reactions in your body, many of which are responsible for neurotransmitter production.',
            style: GoogleFonts.lexend(
              fontSize: 15,
              fontWeight: FontWeight.w500,
              color:
                  isDark ? Colors.white.withValues(alpha: 0.9) : Colors.black87,
              height: 1.4,
            ),
          ),
          const SizedBox(height: 16),
          TextButton(
            onPressed: () =>
                Navigator.pushReplacementNamed(context, AppRouter.scienceHub),
            style: TextButton.styleFrom(
              padding: EdgeInsets.zero,
              minimumSize: Size.zero,
              tapTargetSize: MaterialTapTargetSize.shrinkWrap,
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  'Explore Science Hub',
                  style: GoogleFonts.lexend(
                    fontSize: 13,
                    fontWeight: FontWeight.bold,
                    color: AppColors.primaryBlue,
                  ),
                ),
                const Icon(Icons.arrow_forward,
                    size: 14, color: AppColors.primaryBlue),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// Local Widget for Ember Animation
class _StreakEmberAnimation extends StatefulWidget {
  const _StreakEmberAnimation();

  @override
  State<_StreakEmberAnimation> createState() => _StreakEmberAnimationState();
}

class _StreakEmberAnimationState extends State<_StreakEmberAnimation>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  final List<_Ember> _embers = [];
  final math.Random _random = math.Random();

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 10), // Long loop
    )..repeat();

    // Generate initial embers
    for (int i = 0; i < 20; i++) {
      _embers.add(_generateEmber());
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  _Ember _generateEmber() {
    return _Ember(
      x: _random.nextDouble(), // 0.0 to 1.0
      y: _random.nextDouble(), // 0.0 to 1.0 (starts anywhere)
      speed: 0.05 + _random.nextDouble() * 0.1, // Random speed
      size: 2.0 + _random.nextDouble() * 4.0, // Random size
      opacity: 0.1 + _random.nextDouble() * 0.4, // Random opacity
    );
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return CustomPaint(
          painter: _EmberPainter(_embers, _controller.value),
          size: Size.infinite,
        );
      },
    );
  }
}

class _Ember {
  double x;
  double y;
  final double speed;
  final double size;
  final double opacity;

  _Ember({
    required this.x,
    required this.y,
    required this.speed,
    required this.size,
    required this.opacity,
  });
}

class _EmberPainter extends CustomPainter {
  final List<_Ember> embers;
  final double animationValue;

  _EmberPainter(this.embers, this.animationValue);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..color = AppColors.primaryGold;

    for (var ember in embers) {
      // Simulate movement: Move UP (decrease Y)
      // We use animationValue to tick, but simple "looping" is better manually or via controller time
      // Here we just use the controller as a "tick" driver, but update positions logic relative to frame?
      // Actually, standard CustomPainter animation usually interpolates.
      // Let's rely on simple interpolation loops:

      // Calculate y position based on time
      // Since controller repeats 0->1, we can create a continuous flow
      // effectiveY = (initialY - (speed * time)) % 1.0
      // To make them independent, we can't easily use single global time.
      // So we just "jitter" them based on global time for a simple effect.

      // Better check: Let's assume (y - speed) wraps around 1.0
      // We animate ember.y in real-time? No, paint shouldn't modify state.
      // Let's use a deterministic approach based on `animationValue`?
      // No, that makes them all sync.

      // Simplified approach: Render based on (ember.y - animationValue * ember.speed * 20) % 1.0
      double dy = (ember.y - (animationValue * 5 * ember.speed)) % 1.2;
      // Allow it to go slightly below 0 (upto -0.2) then wrap to 1.0
      if (dy < -0.1) dy += 1.1; // wrap logic roughly

      final yPos = size.height * dy;
      final xPos = size.width * ember.x;

      paint.color = AppColors.primaryGold.withValues(alpha: ember.opacity);
      canvas.drawCircle(Offset(xPos, yPos), ember.size, paint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
