import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../application/view_models/subscription_view_model.dart';
import '../theme/app_theme.dart';

class SubscriptionScreen extends StatefulWidget {
  const SubscriptionScreen({super.key});

  static Widget withProvider() {
    return ChangeNotifierProvider(
      create: (_) => SubscriptionViewModel(),
      child: const SubscriptionScreen(),
    );
  }

  @override
  State<SubscriptionScreen> createState() => _SubscriptionScreenState();
}

class _SubscriptionScreenState extends State<SubscriptionScreen> {
  bool _isYearly = true;

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    const primaryGold = AppColors.primaryGold;
    const bgDark = AppColors.backgroundPremiumDark;

    return Scaffold(
      backgroundColor: isDark
          ? AppColors.backgroundPremiumDark
          : AppColors.backgroundPremiumLight,
      appBar: AppBar(
        backgroundColor: (isDark
                ? AppColors.backgroundPremiumDark
                : AppColors.backgroundPremiumLight)
            .withValues(alpha: 0.9),
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.close, color: Colors.grey),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          'FOCUSSTACK PRO',
          style: GoogleFonts.lexend(
            fontWeight: FontWeight.bold,
            fontSize: 16,
            letterSpacing: 2.0,
            color: AppColors.primaryGold,
          ),
        ),
        centerTitle: true,
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 16),
            child: Consumer<SubscriptionViewModel>(
                builder: (context, viewModel, _) {
              return TextButton(
                onPressed: viewModel.isLoading
                    ? null
                    : () async {
                        await viewModel.restorePurchases();
                        if (!mounted) return;

                        if (viewModel.isSubscribed) {
                          // ignore: use_build_context_synchronously
                          ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(
                                  content: Text('Purchases Restored!')));

                          if (!mounted) return;
                          Future.delayed(const Duration(seconds: 1), () {
                            if (mounted) {
                              // ignore: use_build_context_synchronously
                              Navigator.pop(context);
                            }
                          });
                        }
                      },
                child: Text(
                  'Restore',
                  style: GoogleFonts.lexend(
                    color: AppColors.primaryGold,
                    fontSize: 14,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              );
            }),
          ),
        ],
      ),
      body:
          Consumer<SubscriptionViewModel>(builder: (context, viewModel, child) {
        if (viewModel.isLoading) {
          return const Center(
              child: CircularProgressIndicator(color: AppColors.primaryGold));
        }

        if (viewModel.error != null) {
          WidgetsBinding.instance.addPostFrameCallback((_) {
            ScaffoldMessenger.of(context)
                .showSnackBar(SnackBar(content: Text(viewModel.error!)));
          });
        }

        return Stack(
          children: [
            SingleChildScrollView(
              padding: const EdgeInsets.only(bottom: 180),
              child: Column(
                children: [
                  // Headline Section
                  Padding(
                    padding: const EdgeInsets.fromLTRB(24, 32, 24, 16),
                    child: Column(
                      children: [
                        Text(
                          'Unlock Your Full Potential',
                          textAlign: TextAlign.center,
                          style: GoogleFonts.lexend(
                            fontSize: 32,
                            fontWeight: FontWeight.bold,
                            height: 1.1,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Optimize your routine with clinical-grade tools',
                          textAlign: TextAlign.center,
                          style: GoogleFonts.lexend(
                            fontSize: 16,
                            color: Colors.grey[400],
                          ),
                        ),
                      ],
                    ),
                  ),

                  // Social Proof
                  Padding(
                    padding: const EdgeInsets.symmetric(vertical: 8),
                    child: Column(
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            _buildAvatar(primaryGold.withValues(alpha: 0.2)),
                            _buildAvatar(primaryGold.withValues(alpha: 0.3)),
                            _buildAvatar(primaryGold.withValues(alpha: 0.4)),
                          ],
                        ),
                        const SizedBox(height: 12),
                        Container(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 16, vertical: 6),
                          decoration: BoxDecoration(
                            color: primaryGold.withValues(alpha: 0.1),
                            borderRadius: BorderRadius.circular(999),
                            border: Border.all(
                                color: primaryGold.withValues(alpha: 0.2)),
                          ),
                          child: Text(
                            'Joined by 10,000+ Focus Masters',
                            style: GoogleFonts.lexend(
                              color: AppColors.primaryGold,
                              fontSize: 14,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),

                  // Features List
                  Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      children: [
                        _buildFeatureCard(
                          icon: Icons.health_and_safety,
                          title: 'Advanced Safety Interaction Checker',
                          description:
                              'Cross-reference supplements with common medications safely.',
                          primaryGold: primaryGold,
                          isDark: isDark,
                        ),
                        const SizedBox(height: 16),
                        _buildFeatureCard(
                          icon: Icons.assignment,
                          title: 'Detailed Doctor Export Reports',
                          description:
                              'Generate professional PDFs of your stack to share with specialists.',
                          primaryGold: primaryGold,
                          isDark: isDark,
                        ),
                        const SizedBox(height: 16),
                        _buildFeatureCard(
                          icon: Icons.calendar_today,
                          title: 'Unlimited Grace Days',
                          description:
                              'Maintain your streak even on rest days or when life gets busy.',
                          primaryGold: primaryGold,
                          isDark: isDark,
                        ),
                        const SizedBox(height: 16),
                        _buildFeatureCard(
                          icon: Icons.menu_book,
                          title: 'Exclusive Science Library Content',
                          description:
                              'Deep dives into the latest ADHD research and biohacking data.',
                          primaryGold: primaryGold,
                          isDark: isDark,
                        ),
                      ],
                    ),
                  ),

                  // Pricing Toggle
                  Padding(
                    padding: const EdgeInsets.fromLTRB(16, 40, 16, 24),
                    child: Column(
                      children: [
                        Container(
                          height: 48,
                          padding: const EdgeInsets.all(4),
                          decoration: BoxDecoration(
                            color: Colors.white.withValues(alpha: 0.05),
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(
                                color: Colors.white.withValues(alpha: 0.1)),
                          ),
                          child: Row(
                            children: [
                              _buildPricingToggle(
                                  'Monthly', !_isYearly, false, primaryGold),
                              _buildPricingToggle(
                                  'Yearly', _isYearly, true, primaryGold),
                            ],
                          ),
                        ),
                        const SizedBox(height: 32),
                        Column(
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  _isYearly ? '\$79.99' : '\$9.99',
                                  style: GoogleFonts.lexend(
                                    fontSize: 28,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.white,
                                  ),
                                ),
                                Text(
                                  _isYearly ? ' / year' : ' / month',
                                  style: GoogleFonts.lexend(
                                    fontSize: 14,
                                    color: Colors.grey[400],
                                  ),
                                ),
                              ],
                            ),
                            if (_isYearly) ...[
                              const SizedBox(height: 4),
                              Text(
                                'Saves \$40 per year compared to monthly',
                                style: GoogleFonts.lexend(
                                  fontSize: 12,
                                  color: primaryGold,
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                            ],
                          ],
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),

            // Sticky Footer CTA
            Positioned(
              bottom: 0,
              left: 0,
              right: 0,
              child: Container(
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                    colors: [
                      bgDark.withValues(alpha: 0),
                      bgDark,
                      bgDark,
                    ],
                  ),
                ),
                padding: const EdgeInsets.fromLTRB(24, 40, 24, 16),
                child: SafeArea(
                  child: Column(
                    children: [
                      SizedBox(
                        width: double.infinity,
                        height: 56,
                        child: ElevatedButton(
                          onPressed: viewModel.isLoading
                              ? null
                              : () async {
                                  await viewModel.purchaseSubscription(
                                      _isYearly ? 'annual_pro' : 'monthly_pro');

                                  if (!mounted) return;

                                  if (viewModel.isSubscribed) {
                                    // ignore: use_build_context_synchronously
                                    ScaffoldMessenger.of(context).showSnackBar(
                                        const SnackBar(
                                            content: Text(
                                                'Welcome to FocusStack Pro!')));

                                    if (!mounted) return;
                                    Future.delayed(const Duration(seconds: 1),
                                        () {
                                      if (mounted) {
                                        // ignore: use_build_context_synchronously
                                        Navigator.pop(context);
                                      }
                                    });
                                  }
                                },
                          style: ElevatedButton.styleFrom(
                            backgroundColor: primaryGold,
                            foregroundColor: Colors.black,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                            textStyle: GoogleFonts.lexend(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                            elevation: 8,
                            shadowColor: primaryGold.withValues(alpha: 0.3),
                          ),
                          child: viewModel.isLoading
                              ? const SizedBox(
                                  height: 24,
                                  width: 24,
                                  child: CircularProgressIndicator(
                                      color: Colors.black, strokeWidth: 2))
                              : Text(
                                  'Start 7-Day Free Trial',
                                  style: GoogleFonts.lexend(),
                                ),
                        ),
                      ),
                      const SizedBox(height: 16),
                      Text(
                        'CANCEL ANYTIME • TERMS & PRIVACY APPLY',
                        textAlign: TextAlign.center,
                        style: GoogleFonts.lexend(
                          fontSize: 10,
                          color: Colors.grey[600],
                          letterSpacing: 1.5,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        );
      }),
    );
  }

  Widget _buildAvatar(Color color) {
    return Container(
      width: 36,
      height: 36,
      margin: const EdgeInsets.symmetric(horizontal: 4),
      decoration: BoxDecoration(
        color: color,
        shape: BoxShape.circle,
        border: Border.all(color: const Color(0xFF181611), width: 3),
      ),
    );
  }

  Widget _buildFeatureCard({
    required IconData icon,
    required String title,
    required String description,
    required Color primaryGold,
    required bool isDark,
  }) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.05),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.white.withValues(alpha: 0.1)),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: primaryGold.withValues(alpha: 0.2),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(icon, color: primaryGold, size: 24),
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
                    fontWeight: FontWeight.w600,
                    color: Colors.white,
                    height: 1.2,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  description,
                  style: GoogleFonts.lexend(
                    fontSize: 14,
                    color: Colors.grey[400],
                    height: 1.4,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPricingToggle(
      String label, bool isSelected, bool hasBadge, Color primaryGold) {
    return Expanded(
      child: GestureDetector(
        onTap: () => setState(() => _isYearly = label == 'Yearly'),
        child: Stack(
          clipBehavior: Clip.none,
          children: [
            Container(
              height: 40,
              decoration: BoxDecoration(
                color: isSelected
                    ? Colors.white.withValues(alpha: 0.1)
                    : Colors.transparent,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Center(
                child: Text(
                  label,
                  style: GoogleFonts.lexend(
                    fontSize: 14,
                    fontWeight: FontWeight.w500,
                    color: isSelected ? Colors.white : Colors.grey[400],
                  ),
                ),
              ),
            ),
            if (hasBadge)
              Positioned(
                top: -4,
                right: -4,
                child: Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                  decoration: BoxDecoration(
                    color: primaryGold,
                    borderRadius: BorderRadius.circular(999),
                    boxShadow: [
                      BoxShadow(
                        color: primaryGold.withValues(alpha: 0.3),
                        blurRadius: 8,
                      ),
                    ],
                  ),
                  child: Text(
                    'BEST VALUE',
                    style: GoogleFonts.lexend(
                      fontSize: 9,
                      fontWeight: FontWeight.bold,
                      color: Colors.black,
                      letterSpacing: 0.5,
                    ),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
