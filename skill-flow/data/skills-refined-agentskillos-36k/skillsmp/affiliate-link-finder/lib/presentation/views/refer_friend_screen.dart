import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import '../../config/locator.dart';
import '../../application/view_models/refer_friend_view_model.dart';
import '../../domain/entities/referral.dart';

class ReferFriendScreen extends StatefulWidget {
  const ReferFriendScreen({super.key});

  @override
  State<ReferFriendScreen> createState() => _ReferFriendScreenState();
}

class _ReferFriendScreenState extends State<ReferFriendScreen> {
  late ReferFriendViewModel _viewModel;

  @override
  void initState() {
    super.initState();
    _viewModel = locator<ReferFriendViewModel>();
    _viewModel.loadData();
  }

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider.value(
      value: _viewModel,
      child: Consumer<ReferFriendViewModel>(
        builder: (context, viewModel, child) {
          final isDark = Theme.of(context).brightness == Brightness.dark;
          const primaryGold = Color(0xFFD4A411);
          const bgLight = Color(0xFFF8F8F6);
          const bgDark = Color(0xFF181611);

          return Scaffold(
            backgroundColor: isDark ? bgDark : bgLight,
            body: viewModel.isLoading
                ? const Center(child: CircularProgressIndicator())
                : SafeArea(
                    child: SingleChildScrollView(
                      child: Column(
                        children: [
                          // Top App Bar
                          Padding(
                            padding: const EdgeInsets.all(16),
                            child: Row(
                              children: [
                                GestureDetector(
                                  onTap: () => Navigator.pop(context),
                                  child: Container(
                                    width: 48,
                                    height: 48,
                                    alignment: Alignment.centerLeft,
                                    child: Icon(
                                      Icons.arrow_back_ios,
                                      color:
                                          isDark ? Colors.white : Colors.black,
                                    ),
                                  ),
                                ),
                                Expanded(
                                  child: Text(
                                    'Refer a Friend',
                                    textAlign: TextAlign.center,
                                    style: TextStyle(
                                      color:
                                          isDark ? Colors.white : Colors.black,
                                      fontSize: 18,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                ),
                                const SizedBox(width: 48),
                              ],
                            ),
                          ),

                          // Header Image
                          Padding(
                            padding: const EdgeInsets.symmetric(horizontal: 16),
                            child: Container(
                              height: 256,
                              decoration: BoxDecoration(
                                borderRadius: BorderRadius.circular(16),
                                gradient: LinearGradient(
                                  begin: Alignment.topCenter,
                                  end: Alignment.bottomCenter,
                                  colors: [
                                    primaryGold.withValues(alpha: 0.1),
                                    primaryGold.withValues(alpha: 0.3),
                                  ],
                                ),
                                border: Border.all(
                                    color: primaryGold.withValues(alpha: 0.2)),
                                image: const DecorationImage(
                                  image: AssetImage(
                                    'assets/images/referral_hero.png',
                                  ),
                                  fit: BoxFit.cover,
                                  colorFilter: ColorFilter.mode(
                                    Colors.black26,
                                    BlendMode.darken,
                                  ),
                                ),
                              ),
                              child: Padding(
                                padding: const EdgeInsets.all(24),
                                child: Align(
                                  alignment: Alignment.bottomLeft,
                                  child: Container(
                                    padding: const EdgeInsets.symmetric(
                                        horizontal: 12, vertical: 6),
                                    decoration: BoxDecoration(
                                      color: primaryGold,
                                      borderRadius: BorderRadius.circular(999),
                                    ),
                                    child: const Text(
                                      'GROWTH PROGRAM',
                                      style: TextStyle(
                                        color: Colors.black,
                                        fontSize: 10,
                                        fontWeight: FontWeight.bold,
                                        letterSpacing: 1.5,
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ),

                          // Headline
                          Padding(
                            padding: const EdgeInsets.only(top: 32, bottom: 8),
                            child: Text(
                              'Better Together',
                              textAlign: TextAlign.center,
                              style: TextStyle(
                                color: isDark ? Colors.white : Colors.black,
                                fontSize: 32,
                                fontWeight: FontWeight.bold,
                                height: 1.1,
                              ),
                            ),
                          ),

                          // Body Text
                          Padding(
                            padding: const EdgeInsets.symmetric(
                                horizontal: 32, vertical: 8),
                            child: RichText(
                              textAlign: TextAlign.center,
                              text: TextSpan(
                                style: TextStyle(
                                  color: isDark
                                      ? Colors.white.withValues(alpha: 0.8)
                                      : Colors.black87,
                                  fontSize: 16,
                                  height: 1.5,
                                ),
                                children: const [
                                  TextSpan(text: 'Gift a friend '),
                                  TextSpan(
                                    text: '1 Month of Pro',
                                    style: TextStyle(
                                      color: primaryGold,
                                      fontWeight: FontWeight.w600,
                                    ),
                                  ),
                                  TextSpan(text: ' & earn a bonus '),
                                  TextSpan(
                                    text: 'Grace Day',
                                    style: TextStyle(
                                      color: primaryGold,
                                      fontWeight: FontWeight.w600,
                                    ),
                                  ),
                                  TextSpan(
                                      text: ' for your own habit streaks.'),
                                ],
                              ),
                            ),
                          ),

                          // Referral Code Field
                          if (viewModel.referralData != null)
                            Padding(
                              padding: const EdgeInsets.all(24),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Padding(
                                    padding: const EdgeInsets.only(
                                        left: 4, bottom: 8),
                                    child: Text(
                                      'Your Unique Referral Code',
                                      style: TextStyle(
                                        color: isDark
                                            ? Colors.white
                                                .withValues(alpha: 0.6)
                                            : Colors.black54,
                                        fontSize: 14,
                                        fontWeight: FontWeight.w500,
                                      ),
                                    ),
                                  ),
                                  Container(
                                    decoration: BoxDecoration(
                                      borderRadius: BorderRadius.circular(16),
                                      boxShadow: [
                                        BoxShadow(
                                          color: Colors.black
                                              .withValues(alpha: 0.2),
                                          blurRadius: 8,
                                          offset: const Offset(0, 4),
                                        ),
                                      ],
                                    ),
                                    child: Row(
                                      children: [
                                        Expanded(
                                          child: Container(
                                            height: 56,
                                            padding: const EdgeInsets.symmetric(
                                                horizontal: 16),
                                            decoration: BoxDecoration(
                                              color: const Color(0xFF27241C),
                                              border: Border.all(
                                                  color:
                                                      const Color(0xFF544D3B)),
                                              borderRadius:
                                                  const BorderRadius.only(
                                                topLeft: Radius.circular(16),
                                                bottomLeft: Radius.circular(16),
                                              ),
                                            ),
                                            child: Align(
                                              alignment: Alignment.centerLeft,
                                              child: Text(
                                                viewModel
                                                    .referralData!.referralCode,
                                                style: const TextStyle(
                                                  color: Colors.white,
                                                  fontSize: 18,
                                                  fontWeight: FontWeight.bold,
                                                  letterSpacing: 2,
                                                ),
                                              ),
                                            ),
                                          ),
                                        ),
                                        GestureDetector(
                                          onTap: () {
                                            Clipboard.setData(ClipboardData(
                                                text: viewModel.referralData!
                                                    .referralCode));
                                            ScaffoldMessenger.of(context)
                                                .showSnackBar(
                                              const SnackBar(
                                                content: Text(
                                                    'Referral code copied!'),
                                                backgroundColor: primaryGold,
                                                behavior:
                                                    SnackBarBehavior.floating,
                                              ),
                                            );
                                          },
                                          child: Container(
                                            width: 56,
                                            height: 56,
                                            decoration: BoxDecoration(
                                              color: const Color(0xFF27241C),
                                              border: Border.all(
                                                  color:
                                                      const Color(0xFF544D3B)),
                                              borderRadius:
                                                  const BorderRadius.only(
                                                topRight: Radius.circular(16),
                                                bottomRight:
                                                    Radius.circular(16),
                                              ),
                                            ),
                                            child: const Icon(
                                                Icons.content_copy,
                                                color: primaryGold),
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ],
                              ),
                            ),

                          // Share Button
                          Padding(
                            padding: const EdgeInsets.symmetric(horizontal: 24),
                            child: SizedBox(
                              width: double.infinity,
                              height: 56,
                              child: ElevatedButton.icon(
                                onPressed: viewModel.shareReferral,
                                icon: const Icon(Icons.share),
                                label: const Text('Share with a Buddy'),
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: primaryGold,
                                  foregroundColor: bgDark,
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(999),
                                  ),
                                  textStyle: const TextStyle(
                                    fontSize: 18,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                            ),
                          ),

                          // Your Impact Section
                          if (viewModel.referralData != null &&
                              viewModel.referralData!.referrals.isNotEmpty)
                            Padding(
                              padding: const EdgeInsets.all(24),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    children: [
                                      const Icon(Icons.groups,
                                          color: primaryGold, size: 24),
                                      const SizedBox(width: 8),
                                      Text(
                                        'Your Impact',
                                        style: TextStyle(
                                          color: isDark
                                              ? Colors.white
                                              : Colors.black,
                                          fontSize: 20,
                                          fontWeight: FontWeight.bold,
                                        ),
                                      ),
                                    ],
                                  ),
                                  const SizedBox(height: 16),

                                  // Referral History Items
                                  ...viewModel.referralData!.referrals
                                      .map((referral) => Padding(
                                            padding: const EdgeInsets.only(
                                                bottom: 12),
                                            child: _buildReferralItem(
                                              context,
                                              referral: referral,
                                              primaryGold: primaryGold,
                                              isDark: isDark,
                                            ),
                                          )),

                                  // Empty State Message
                                  Padding(
                                    padding: const EdgeInsets.only(top: 24),
                                    child: Text(
                                      'Invite more friends to unlock a 3-month Pro pass!',
                                      textAlign: TextAlign.center,
                                      style: TextStyle(
                                        color:
                                            Colors.white.withValues(alpha: 0.3),
                                        fontSize: 12,
                                        fontStyle: FontStyle.italic,
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            ),

                          const SizedBox(height: 32),
                        ],
                      ),
                    ),
                  ),
          );
        },
      ),
    );
  }

  Widget _buildReferralItem(
    BuildContext context, {
    required Referral referral,
    required Color primaryGold,
    required bool isDark,
  }) {
    return Opacity(
      opacity: referral.isActive ? 1.0 : 0.7,
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Colors.white.withValues(alpha: 0.05),
          border: Border.all(color: Colors.white.withValues(alpha: 0.1)),
          borderRadius: BorderRadius.circular(16),
        ),
        child: Row(
          children: [
            // Avatar
            Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: referral.isActive
                    ? primaryGold.withValues(alpha: 0.2)
                    : Colors.white.withValues(alpha: 0.1),
                shape: BoxShape.circle,
              ),
              child: Center(
                child: Text(
                  referral.initials,
                  style: TextStyle(
                    color: referral.isActive
                        ? primaryGold
                        : Colors.white.withValues(alpha: 0.4),
                    fontWeight: FontWeight.bold,
                    fontSize: 14,
                  ),
                ),
              ),
            ),
            const SizedBox(width: 12),

            // Name and Date
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    referral.name,
                    style: TextStyle(
                      color: referral.isActive
                          ? Colors.white
                          : Colors.white.withValues(alpha: 0.8),
                      fontWeight: FontWeight.w500,
                      fontSize: 15,
                    ),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    referral.date,
                    style: TextStyle(
                      color: Colors.white.withValues(alpha: 0.4),
                      fontSize: 12,
                    ),
                  ),
                ],
              ),
            ),

            // Status/Reward
            Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                if (referral.reward != null)
                  Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: primaryGold.withValues(alpha: 0.1),
                      borderRadius: BorderRadius.circular(999),
                    ),
                    child: Text(
                      referral.reward!,
                      style: TextStyle(
                        color: primaryGold,
                        fontSize: 11,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  )
                else
                  Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: Colors.white.withValues(alpha: 0.05),
                      borderRadius: BorderRadius.circular(999),
                    ),
                    child: Text(
                      referral.status,
                      style: TextStyle(
                        color: Colors.white.withValues(alpha: 0.4),
                        fontSize: 11,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                const SizedBox(height: 4),
                Text(
                  referral.status.toUpperCase(),
                  style: TextStyle(
                    color: Colors.white.withValues(alpha: 0.4),
                    fontSize: 10,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 0.5,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
