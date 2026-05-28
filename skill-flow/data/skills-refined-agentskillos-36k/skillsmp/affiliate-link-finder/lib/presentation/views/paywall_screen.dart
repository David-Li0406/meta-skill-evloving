import 'package:flutter/material.dart';
import '../../config/locator.dart';
import '../../application/view_models/subscription_view_model.dart';
import 'package:provider/provider.dart';

class PaywallScreen extends StatelessWidget {
  final String? returnTo;

  const PaywallScreen({super.key, this.returnTo});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => locator<SubscriptionViewModel>(),
      child: Scaffold(
        body: Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              colors: [
                Theme.of(context).primaryColor.withValues(alpha: 0.1),
                Theme.of(context).scaffoldBackgroundColor,
              ],
            ),
          ),
          child: SafeArea(
            child: CustomScrollView(
              slivers: [
                _buildAppBar(context),
                SliverPadding(
                  padding: const EdgeInsets.all(24.0),
                  sliver: SliverList(
                    delegate: SliverChildListDelegate([
                      _buildHeader(),
                      const SizedBox(height: 32),
                      _buildValuePill('Unlock Deep Performance Insights'),
                      _buildValuePill('Unlimited Supplement Stacks'),
                      _buildValuePill('Priority Med Interaction Checker'),
                      _buildValuePill('Expert-Verified ADHD Science Hub'),
                      const SizedBox(height: 40),
                      _buildPricingSection(context),
                      const SizedBox(height: 32),
                      _buildFooter(context),
                    ]),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildAppBar(BuildContext context) {
    return SliverAppBar(
      backgroundColor: Colors.transparent,
      elevation: 0,
      leading: IconButton(
        icon: const Icon(Icons.close),
        onPressed: () => Navigator.pop(context),
      ),
      actions: [
        TextButton(
          onPressed: () {}, // Restore purchase logic
          child: const Text('Restore'),
        ),
      ],
    );
  }

  Widget _buildHeader() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
          decoration: BoxDecoration(
            color: Colors.amber.withValues(alpha: 0.2),
            borderRadius: BorderRadius.circular(20),
          ),
          child: const Text(
            'SUMMER SALE: 40% OFF',
            style: TextStyle(
              color: Colors.amber,
              fontWeight: FontWeight.bold,
              fontSize: 12,
            ),
          ),
        ),
        const SizedBox(height: 16),
        const Text(
          'Reach Your Full Potential',
          style: TextStyle(
            fontSize: 32,
            fontWeight: FontWeight.bold,
            letterSpacing: -1,
          ),
        ),
        const SizedBox(height: 12),
        const Text(
          'Join 10,000+ focused individuals using ADHD Supps Pro to optimize their daily routine.',
          style: TextStyle(
            fontSize: 16,
            color: Colors.grey,
            height: 1.4,
          ),
        ),
      ],
    );
  }

  Widget _buildValuePill(String title) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
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
          const Icon(Icons.check_circle, color: Colors.green),
          const SizedBox(width: 16),
          Expanded(
            child: Text(
              title,
              style: const TextStyle(
                fontWeight: FontWeight.w600,
                fontSize: 15,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPricingSection(BuildContext context) {
    return Column(
      children: [
        _buildPlanCard(
          context,
          'Annual Pro',
          '\$4.99/mo',
          'Billed as \$59.99/year',
          isPopular: true,
        ),
        const SizedBox(height: 16),
        _buildPlanCard(
          context,
          'Monthly Pro',
          '\$9.99/mo',
          'Cancel anytime',
          isPopular: false,
        ),
      ],
    );
  }

  Widget _buildPlanCard(
    BuildContext context,
    String title,
    String price,
    String subtitle, {
    bool isPopular = false,
  }) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: isPopular ? Theme.of(context).primaryColor : Colors.white,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(
          color:
              isPopular ? Theme.of(context).primaryColor : Colors.grey.shade200,
          width: 2,
        ),
      ),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: TextStyle(
                    color: isPopular ? Colors.white : Colors.black,
                    fontWeight: FontWeight.bold,
                    fontSize: 18,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  subtitle,
                  style: TextStyle(
                    color: isPopular
                        ? Colors.white.withValues(alpha: 0.8)
                        : Colors.grey,
                    fontSize: 13,
                  ),
                ),
              ],
            ),
          ),
          Text(
            price,
            style: TextStyle(
              color: isPopular ? Colors.white : Colors.black,
              fontWeight: FontWeight.bold,
              fontSize: 22,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildFooter(BuildContext context) {
    return Column(
      children: [
        SizedBox(
          width: double.infinity,
          height: 60,
          child: ElevatedButton(
            onPressed: () async {
              final scaffoldMessenger = ScaffoldMessenger.of(context);
              final viewModel = context.read<SubscriptionViewModel>();
              final authProvider = context.read<AuthProvider>();

              await viewModel.purchaseSubscription('pro_annual');

              if (viewModel.isSubscribed) {
                await authProvider.refreshEntitlements();

                if (context.mounted) {
                  if (returnTo != null) {
                    Navigator.pushReplacementNamed(context, returnTo!);
                  } else {
                    Navigator.pop(context);
                  }
                }
              } else if (viewModel.error != null) {
                scaffoldMessenger.showSnackBar(
                  SnackBar(content: Text(viewModel.error!)),
                );
              }
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Theme.of(context).primaryColor,
              foregroundColor: Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(16),
              ),
              elevation: 0,
            ),
            child: const Text(
              'Start 7-Day Free Trial',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ),
        const SizedBox(height: 20),
        const Text(
          'Secured with Stripe. Terms & Privacy Apply.',
          style: TextStyle(
            fontSize: 12,
            color: Colors.grey,
          ),
        ),
      ],
    );
  }
}
