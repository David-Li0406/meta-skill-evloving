import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../navigation/app_router.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/app_theme.dart';
import '../../application/providers/auth_provider.dart';
import '../../application/view_models/safety_view_model.dart';
import '../../config/locator.dart';

class OnboardingStackSetupScreen extends StatefulWidget {
  const OnboardingStackSetupScreen({super.key});

  @override
  State<OnboardingStackSetupScreen> createState() =>
      _OnboardingStackSetupScreenState();
}

class _OnboardingStackSetupScreenState extends State<OnboardingStackSetupScreen>
    with SingleTickerProviderStateMixin {
  // Mock data for search/suggestions
  final TextEditingController _searchController = TextEditingController();
  late SafetyViewModel _safetyViewModel;

  int _walkthroughStep = 0; // 0: None, 1: Search, 2: Add, 3: Review
  late AnimationController _pulseController;

  @override
  void initState() {
    super.initState();
    final authProvider = context.read<AuthProvider>();
    final userId = authProvider.user?.id ?? 'onboarding_user';
    _safetyViewModel = locator.get<SafetyViewModel>(param1: userId);

    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat(reverse: true);

    // Initial check for default onboarding items
    _safetyViewModel.checkInteractions(['vyvanse_id', 'vitamin_d3_id']);

    // Start walkthrough after a short delay
    Future.delayed(const Duration(milliseconds: 500), () {
      if (mounted) setState(() => _walkthroughStep = 1);
    });
  }

  @override
  void dispose() {
    _safetyViewModel.dispose();
    _pulseController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    const bgDark = Color(
        0xFF161d2b); // Matches handoff card-dark or background-dark #101622
    const bgLight = Color(0xFFF8F8F6);
    const primaryGold = AppColors.primaryGold;
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Stack(
      children: [
        Scaffold(
          backgroundColor: isDark ? bgDark : bgLight,
          appBar: AppBar(
            title: const Text('Quick Setup',
                style: TextStyle(fontWeight: FontWeight.bold)),
            centerTitle: true,
            backgroundColor: isDark ? bgDark : bgLight,
            foregroundColor: isDark ? Colors.white : const Color(0xFF111418),
            leading: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Container(
                decoration: BoxDecoration(
                  color: isDark
                      ? Colors.white.withValues(alpha: 0.05)
                      : Colors.black.withValues(alpha: 0.05),
                  shape: BoxShape.circle,
                ),
                child: IconButton(
                  icon: const Icon(Icons.arrow_back_ios_new, size: 18),
                  onPressed: () => Navigator.pop(context),
                ),
              ),
            ),
            actions: [
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Container(
                  decoration: BoxDecoration(
                    color: isDark
                        ? Colors.white.withValues(alpha: 0.05)
                        : Colors.black.withValues(alpha: 0.05),
                    shape: BoxShape.circle,
                  ),
                  child: IconButton(
                    icon: const Icon(Icons.help_outline,
                        color: AppColors.primaryGold),
                    onPressed: () {},
                  ),
                ),
              ),
            ],
            elevation: 0,
          ),
          body: SafeArea(
            child: Column(
              children: [
                // Progress Indicator
                Padding(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  child: Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            'Step 2 of 3: Routine Building',
                            style: TextStyle(
                              color:
                                  isDark ? Colors.grey[400] : Colors.grey[600],
                              fontSize: 14,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                          const Text(
                            '65%',
                            style: TextStyle(
                              color: primaryGold,
                              fontWeight: FontWeight.bold,
                              fontSize: 14,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      ClipRRect(
                        borderRadius: BorderRadius.circular(10),
                        child: LinearProgressIndicator(
                          value: 0.65,
                          minHeight: 8,
                          backgroundColor: isDark
                              ? Colors.white.withValues(alpha: 0.1)
                              : Colors.grey[200], // emerald-900/30
                          valueColor: const AlwaysStoppedAnimation<Color>(
                              AppColors.primaryGold),
                        ),
                      ),
                    ],
                  ),
                ),

                Expanded(
                  child: SingleChildScrollView(
                    padding: const EdgeInsets.only(
                        bottom: 120), // Clearance for bottom bar
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Headline
                        Padding(
                          padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
                          child: Text(
                            'Let’s build your stack',
                            style: TextStyle(
                              color: isDark
                                  ? Colors.white
                                  : const Color(0xFF111418),
                              fontSize: 30,
                              fontWeight: FontWeight.bold,
                              letterSpacing: -0.5,
                              height: 1.1,
                            ),
                          ),
                        ),
                        Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 16),
                          child: Text(
                            'Search and add the supplements you already take to check for interactions.',
                            style: TextStyle(
                              color:
                                  isDark ? Colors.grey[400] : Colors.grey[600],
                              fontSize: 16,
                              height: 1.5,
                            ),
                          ),
                        ),

                        // Search Bar
                        Padding(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 16, vertical: 24),
                          child: Container(
                            height: 56,
                            decoration: BoxDecoration(
                              color: isDark
                                  ? const Color(0xFF161d2b)
                                      .withValues(alpha: 0.2)
                                  : Colors.white,
                              borderRadius: BorderRadius.circular(12),
                              boxShadow: [
                                if (!isDark)
                                  BoxShadow(
                                      color:
                                          Colors.black.withValues(alpha: 0.05),
                                      blurRadius: 4,
                                      offset: const Offset(0, 2)),
                              ],
                            ),
                            child: Row(
                              children: [
                                Padding(
                                  padding: const EdgeInsets.symmetric(
                                      horizontal: 16),
                                  child: Icon(Icons.search,
                                      color: isDark
                                          ? AppColors.primaryGold
                                              .withValues(alpha: 0.5)
                                          : Colors.grey[400]),
                                ),
                                Expanded(
                                  child: TextField(
                                    controller: _searchController,
                                    decoration: InputDecoration(
                                      hintText:
                                          'Search supplements (e.g. Omega-3)',
                                      hintStyle: TextStyle(
                                        color: isDark
                                            ? AppColors.primaryGold
                                                .withValues(alpha: 0.8)
                                            : Colors.grey[400],
                                      ),
                                      border: InputBorder.none,
                                    ),
                                    style: TextStyle(
                                        color: isDark
                                            ? Colors.white
                                            : Colors.black),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),

                        // Suggested Pairs
                        Padding(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 16, vertical: 8),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                'SUGGESTED ADHD PAIRS',
                                style: TextStyle(
                                  color: isDark
                                      ? AppColors.primaryGold
                                          .withValues(alpha: 0.6)
                                      : Colors.grey[500],
                                  fontSize: 12,
                                  fontWeight: FontWeight.bold,
                                  letterSpacing: 1.2,
                                ),
                              ),
                              const Text(
                                'View All',
                                style: TextStyle(
                                  color: primaryGold,
                                  fontSize: 12,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                          ),
                        ),

                        SingleChildScrollView(
                          scrollDirection: Axis.horizontal,
                          padding: const EdgeInsets.symmetric(horizontal: 16),
                          child: Row(
                            children: [
                              _buildSuggestionCard(
                                context,
                                title: 'L-Theanine + Caffeine',
                                subtitle: 'For jitters-free focus',
                                icon: Icons.bolt,
                                iconColor: primaryGold,
                                iconBg: primaryGold.withValues(alpha: 0.1),
                              ),
                              const SizedBox(width: 16),
                              _buildSuggestionCard(
                                context,
                                title: 'Magnesium + Vit D3',
                                subtitle: 'Optimal absorption combo',
                                icon: Icons.nightlight_round, // nightlight
                                iconColor: Colors.blue,
                                iconBg: Colors.blue.withValues(alpha: 0.1),
                              ),
                            ],
                          ),
                        ),

                        const SizedBox(height: 32),

                        // Time Buckets - Current Routine
                        Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 16),
                          child: Text(
                            'CURRENT ROUTINE',
                            style: TextStyle(
                              color: isDark
                                  ? AppColors.primaryGold.withValues(alpha: 0.6)
                                  : Colors.grey[500],
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                              letterSpacing: 1.2,
                            ),
                          ),
                        ),
                        const SizedBox(height: 16),

                        // Morning Stack Card
                        _buildRoutineCard(
                          context,
                          title: 'Morning Stack',
                          subtitle: '2 supplements added',
                          icon: Icons.wb_sunny,
                          iconColor: Colors.amber,
                          iconBg: isDark
                              ? Colors.amber.withValues(alpha: 0.2)
                              : Colors.amber.withValues(alpha: 0.1),
                          isDark: isDark,
                          primaryColor: primaryGold,
                          children: [
                            Wrap(
                              spacing: 8,
                              runSpacing: 8,
                              children: [
                                _buildSupplementTag('Vyvanse (30mg)', isDark),
                                _buildSupplementTag('Vitamin D3', isDark),
                                _buildAddTag(isDark, primaryGold),
                              ],
                            ),
                          ],
                        ),

                        const SizedBox(height: 16),

                        // Evening Stack Card
                        _buildRoutineCard(
                          context,
                          title: 'Evening Stack',
                          subtitle: '0 supplements added',
                          icon: Icons.dark_mode,
                          iconColor: Colors.indigo,
                          iconBg: isDark
                              ? Colors.indigo.withValues(alpha: 0.2)
                              : Colors.indigo.withValues(alpha: 0.1),
                          isDark: isDark,
                          primaryColor: primaryGold,
                          children: [],
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
          bottomSheet:
              _buildBottomSheet(context, isDark, primaryGold, bgDark, bgLight),
        ),
        if (_walkthroughStep > 0) _buildWalkthroughOverlay(),
      ],
    );
  }

  Widget _buildWalkthroughOverlay() {
    return Stack(
      children: [
        // Dimmed Background
        Positioned.fill(
          child: GestureDetector(
            onTap: () {
              setState(() {
                if (_walkthroughStep < 3) {
                  _walkthroughStep++;
                } else {
                  _walkthroughStep = 0;
                }
              });
            },
            child: Container(
              color: Colors.black.withValues(alpha: 0.7),
            ),
          ),
        ),
        // Instructional Content
        if (_walkthroughStep == 1)
          Positioned(
            top: 240,
            left: 24,
            right: 24,
            child: _buildWalkthroughStep(
              'Step 1: Browse the Library',
              'Search for supplements you already take or browse our evidence-based library.',
              Icons.search,
            ),
          ),
        if (_walkthroughStep == 2)
          Positioned(
            top: 400,
            left: 24,
            right: 24,
            child: _buildWalkthroughStep(
              'Step 2: Add to Your Stack',
              'Tap "Add" or any suggested pair to include it in your daily routine.',
              Icons.add_circle_outline,
            ),
          ),
        if (_walkthroughStep == 3)
          Positioned(
            bottom: 220,
            left: 24,
            right: 24,
            child: _buildWalkthroughStep(
              'Step 3: Safety Guard',
              'We automatically check for interactions between your meds and supplements.',
              Icons.security,
            ),
          ),
        // "Got it" Button
        Positioned(
          bottom: 140,
          left: 100,
          right: 100,
          child: Center(
            child: Text(
              'Tap anywhere to continue',
              style: GoogleFonts.lexend(
                color: Colors.white70,
                fontSize: 12,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildWalkthroughStep(
      String title, String description, IconData icon) {
    return Column(
      children: [
        Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: AppColors.primaryGold,
            shape: BoxShape.circle,
            boxShadow: [
              BoxShadow(
                color: AppColors.primaryGold.withValues(alpha: 0.5),
                blurRadius: 20,
                spreadRadius: 5,
              ),
            ],
          ),
          child: Icon(icon, color: Colors.black, size: 24),
        ),
        const SizedBox(height: 16),
        Text(
          title,
          textAlign: TextAlign.center,
          style: GoogleFonts.lexend(
            color: Colors.white,
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 8),
        Text(
          description,
          textAlign: TextAlign.center,
          style: GoogleFonts.lexend(
            color: Colors.white70,
            fontSize: 14,
            height: 1.5,
          ),
        ),
      ],
    );
  }

  Widget _buildBottomSheet(BuildContext context, bool isDark,
      Color primaryColor, Color bgDark, Color bgLight) {
    return Container(
      color: isDark
          ? bgDark.withValues(alpha: 0.95)
          : bgLight.withValues(alpha: 0.95),
      padding: const EdgeInsets.all(16),
      child: SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            // Safety Banner
            Consumer<SafetyViewModel>(
              builder: (context, safetyViewModel, child) {
                final hasInteractions =
                    safetyViewModel.currentInteractions.isNotEmpty;
                final bannerColor =
                    hasInteractions ? Colors.amber : primaryColor;

                return Container(
                  margin: const EdgeInsets.only(bottom: 16),
                  padding:
                      const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  decoration: BoxDecoration(
                    color: bannerColor.withValues(alpha: isDark ? 0.05 : 0.1),
                    border:
                        Border.all(color: bannerColor.withValues(alpha: 0.2)),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Row(
                    children: [
                      Icon(
                          hasInteractions
                              ? Icons.warning_amber_rounded
                              : Icons.verified_user,
                          color: bannerColor),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              hasInteractions
                                  ? 'SAFETY ALERT'
                                  : 'SAFETY SHIELD ACTIVE',
                              style: TextStyle(
                                color: bannerColor,
                                fontWeight: FontWeight.bold,
                                fontSize: 10,
                                letterSpacing: 0.5,
                              ),
                            ),
                            const SizedBox(height: 2),
                            Text(
                              hasInteractions
                                  ? 'Potential interaction detected in your stack.'
                                  : 'Interaction Check: No risks found.',
                              style: TextStyle(
                                color: isDark
                                    ? bannerColor.withValues(alpha: 0.7)
                                    : Colors.grey[600],
                                fontSize: 11,
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                          ],
                        ),
                      ),
                      if (hasInteractions)
                        IconButton(
                          icon: Icon(Icons.info, color: bannerColor, size: 20),
                          onPressed: () {
                            Navigator.pushNamed(
                              context,
                              AppRouter.safetyInteractionDetail,
                              arguments:
                                  safetyViewModel.currentInteractions.first,
                            );
                          },
                        )
                      else
                        Icon(Icons.info, color: bannerColor, size: 20),
                    ],
                  ),
                );
              },
            ),

            // Finish Button
            SizedBox(
              width: double.infinity,
              height: 56,
              child: ElevatedButton(
                onPressed: () async {
                  final auth = context.read<AuthProvider>();
                  final user = auth.user;
                  if (user != null) {
                    await auth.updateProfile(
                        user.copyWith(hasCompletedOnboarding: true));
                  }
                  if (mounted) {
                    Navigator.pushNamedAndRemoveUntil(
                        context, AppRouter.dashboard, (route) => false);
                  }
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primaryGold,
                  foregroundColor: Colors.black,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                  elevation: 0,
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      'Finish & Start Tracking',
                      style: GoogleFonts.lexend(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(width: 8),
                    const Icon(Icons.arrow_forward,
                        size: 22, fontWeight: FontWeight.bold),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSuggestionCard(
    BuildContext context, {
    required String title,
    required String subtitle,
    required IconData icon,
    required Color iconColor,
    required Color iconBg,
  }) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Container(
      width: 200,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isDark
            ? const Color(0xFF161d2b).withValues(alpha: 0.5)
            : Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
            color: isDark
                ? Colors.white.withValues(alpha: 0.1)
                : Colors.grey[100]!),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration:
                    BoxDecoration(color: iconBg, shape: BoxShape.circle),
                child: Icon(icon, size: 20, color: iconColor),
              ),
              Container(
                padding: const EdgeInsets.all(4),
                decoration: BoxDecoration(
                  color: AppColors.primaryGold,
                  shape: BoxShape.circle,
                  boxShadow: [
                    BoxShadow(
                        color: Colors.black.withValues(alpha: 0.1),
                        blurRadius: 4,
                        offset: const Offset(0, 2)),
                  ],
                ),
                child:
                    const Icon(Icons.add, size: 16, color: Color(0xFF102216)),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Text(
            title,
            style: TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 14,
              color: isDark ? Colors.white : Colors.black87,
            ),
          ),
          const SizedBox(height: 2),
          Text(
            subtitle,
            style: TextStyle(
              color: isDark ? Colors.grey[400] : Colors.grey[500],
              fontSize: 11,
              fontStyle: FontStyle.italic,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildRoutineCard(
    BuildContext context, {
    required String title,
    required String subtitle,
    required IconData icon,
    required Color iconColor,
    required Color iconBg,
    required bool isDark,
    required Color primaryColor,
    required List<Widget> children,
  }) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isDark
            ? const Color(0xFF161d2b).withValues(alpha: 0.5) // Updated dark bg
            : Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: title == 'Morning Stack'
              ? primaryColor.withValues(alpha: 0.4)
              : (isDark
                  ? Colors.white.withValues(alpha: 0.1)
                  : Colors.grey[100]!),
          width: title == 'Morning Stack' ? 2 : 1,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Container(
                    width: 40,
                    height: 40,
                    decoration:
                        BoxDecoration(color: iconBg, shape: BoxShape.circle),
                    child: Icon(icon, size: 20, color: iconColor),
                  ),
                  const SizedBox(width: 12),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        title,
                        style: TextStyle(
                          color:
                              isDark ? Colors.white : const Color(0xFF111418),
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      Text(
                        subtitle,
                        style: TextStyle(
                          color: isDark ? Colors.grey[400] : Colors.grey[500],
                          fontSize: 12,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
              Icon(Icons.chevron_right,
                  color: isDark ? Colors.grey[600] : Colors.grey[300]),
            ],
          ),
          if (children.isNotEmpty) ...[
            const SizedBox(height: 16),
            ...children,
          ],
        ],
      ),
    );
  }

  Widget _buildSupplementTag(String label, bool isDark) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: isDark ? Colors.white.withValues(alpha: 0.1) : Colors.grey[100],
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color:
              isDark ? Colors.white.withValues(alpha: 0.1) : Colors.grey[200]!,
        ),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            label,
            style: TextStyle(
              color: isDark ? Colors.white : const Color(0xFF111418),
              fontSize: 12,
              fontWeight: FontWeight.w500,
            ),
          ),
          const SizedBox(width: 8),
          Icon(Icons.close,
              size: 14, color: isDark ? Colors.white70 : Colors.black54),
        ],
      ),
    );
  }

  Widget _buildAddTag(bool isDark, Color primaryColor) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: Colors.transparent,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: primaryColor.withValues(alpha: 0.6),
          style: BorderStyle.none,
        ),
        // Use a simple workaround for dashed effect or just colored text
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(Icons.add, size: 14, color: primaryColor),
          const SizedBox(width: 4),
          Text(
            'Tap to add',
            style: TextStyle(
              color: primaryColor,
              fontSize: 12,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }
}
