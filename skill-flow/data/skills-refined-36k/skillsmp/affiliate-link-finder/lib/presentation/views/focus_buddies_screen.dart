import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../application/view_models/focus_buddies_view_model.dart';
import '../../config/locator.dart';
import '../theme/app_theme.dart';
import '../navigation/app_router.dart';

class FocusBuddiesScreen extends StatefulWidget {
  const FocusBuddiesScreen({super.key});

  static Widget withProvider() {
    return ChangeNotifierProvider(
      create: (_) => locator<FocusBuddiesViewModel>()..loadData(),
      child: const FocusBuddiesScreen(),
    );
  }

  @override
  State<FocusBuddiesScreen> createState() => _FocusBuddiesScreenState();
}

class _FocusBuddiesScreenState extends State<FocusBuddiesScreen> {
  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    const primaryGold = AppColors.primaryGold;
    // const bgDark = Color(0xFF190F23); // Old purple dark
    const bgDark = AppColors.backgroundPremiumDark;
    const bgLight = AppColors.backgroundPremiumLight;

    return Consumer<FocusBuddiesViewModel>(
      builder: (context, viewModel, child) {
        if (viewModel.isLoading) {
          return Scaffold(
            backgroundColor: isDark ? bgDark : bgLight,
            body: const Center(child: CircularProgressIndicator()),
          );
        }

        return Scaffold(
          backgroundColor: isDark ? bgDark : bgLight,
          body: Stack(
            children: [
              CustomScrollView(
                slivers: [
                  _buildAppBar(context, isDark, primaryGold),
                  SliverToBoxAdapter(
                    child: Padding(
                      padding: const EdgeInsets.fromLTRB(16, 16, 16, 120),
                      child: Column(
                        children: [
                          _buildTeamGoalProgress(
                              isDark, primaryGold, viewModel),
                          const SizedBox(height: 24),
                          _buildSplitViewLeaderboard(
                              isDark, primaryGold, viewModel),
                          const SizedBox(height: 24),
                          _buildXPStats(isDark, primaryGold, viewModel),
                          const SizedBox(height: 32),
                          _buildActivityFeed(isDark, primaryGold, viewModel),
                          const SizedBox(height: 40),
                          _buildCallToAction(isDark, primaryGold, viewModel),
                          const SizedBox(height: 16),
                          _buildSecondaryActions(isDark),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
          floatingActionButton: FloatingActionButton(
            backgroundColor: primaryGold,
            onPressed: () => _showInviteDialog(context, viewModel, primaryGold),
            child: const Icon(Icons.person_add, color: Colors.black),
          ),
        );
      },
    );
  }

  Widget _buildAppBar(BuildContext context, bool isDark, Color primary) {
    return SliverAppBar(
      backgroundColor: isDark
          ? const Color(0xFF190F23).withValues(alpha: 0.9)
          : const Color(0xFFF7F5F8).withValues(alpha: 0.9),
      pinned: true,
      elevation: 0,
      leading: IconButton(
        icon: Container(
          width: 48,
          height: 48,
          alignment: Alignment.center,
          child: Icon(Icons.arrow_back_ios_new, color: primary, size: 24),
        ),
        onPressed: () => Navigator.pop(context),
      ),
      title: Text(
        'Focus Buddies',
        style: GoogleFonts.lexend(
          color: isDark ? Colors.white : const Color(0xFF0F172A),
          fontSize: 18,
          fontWeight: FontWeight.bold,
        ),
      ),
      centerTitle: true,
      actions: [
        IconButton(
          icon: Container(
            width: 48,
            height: 48,
            alignment: Alignment.center,
            decoration: BoxDecoration(
              color: Colors.transparent,
              shape: BoxShape.circle,
              border: Border.all(color: Colors.transparent),
            ),
            child: Icon(Icons.settings, color: primary, size: 28),
          ),
          onPressed: () {
            Navigator.pushNamed(context, AppRouter.profile);
          },
        ),
      ],
    );
  }

  Widget _buildTeamGoalProgress(
      bool isDark, Color primary, FocusBuddiesViewModel viewModel) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: isDark ? primary.withValues(alpha: 0.1) : Colors.white,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(
          color: primary.withValues(alpha: 0.2),
        ),
        boxShadow: [
          BoxShadow(
            color: primary.withValues(alpha: 0.05),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Icon(Icons.group, color: primary, size: 24),
                  const SizedBox(width: 8),
                  Text(
                    'Shared Weekly Goal',
                    style: GoogleFonts.lexend(
                      color: isDark ? Colors.white : const Color(0xFF0F172A),
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
              Text(
                '${(viewModel.teamGoalProgress * 100).toInt()}%',
                style: GoogleFonts.lexend(
                  color: primary,
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          ClipRRect(
            borderRadius: BorderRadius.circular(6),
            child: Stack(
              children: [
                Container(
                  height: 12,
                  width: double.infinity,
                  color: isDark
                      ? Colors.white.withValues(alpha: 0.1)
                      : Colors.grey[200],
                ),
                Container(
                  height: 12,
                  width: MediaQuery.of(context).size.width *
                      0.8 *
                      viewModel.teamGoalProgress, // rough approx
                  decoration: BoxDecoration(
                    color: primary,
                    boxShadow: [
                      BoxShadow(
                        color: primary.withValues(alpha: 0.6),
                        blurRadius: 12,
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 12),
          Text(
            '${viewModel.sharedGoalDays}/${viewModel.totalDaysGoal} days completed this week. Keep it up!',
            style: GoogleFonts.lexend(
              color: isDark ? primary.withValues(alpha: 0.7) : Colors.grey[500],
              fontSize: 14,
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSplitViewLeaderboard(
      bool isDark, Color primary, FocusBuddiesViewModel viewModel) {
    return Row(
      children: [
        Expanded(
          child: _buildProfileCard(
            isDark,
            primary,
            'You', // Could use authName if available
            viewModel.userStreak.toString(),
            viewModel.userStreak >= viewModel.opponentStreak,
            viewModel.userImage,
            isUser: true,
          ),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12),
          child: Container(
            width: 40,
            height: 40,
            alignment: Alignment.center,
            decoration: BoxDecoration(
              color: primary,
              shape: BoxShape.circle,
              boxShadow: [
                BoxShadow(
                  color: primary.withValues(alpha: 0.4),
                  blurRadius: 10,
                  offset: const Offset(0, 4),
                ),
              ],
            ),
            child: Text(
              'VS',
              style: GoogleFonts.lexend(
                color: Colors.white,
                fontSize: 14,
                fontWeight: FontWeight.w900,
                fontStyle: FontStyle.italic,
              ),
            ),
          ),
        ),
        Expanded(
          child: _buildProfileCard(
            isDark,
            primary,
            viewModel.opponentName,
            viewModel.opponentStreak.toString(),
            viewModel.opponentStreak > viewModel.userStreak,
            viewModel.opponentImage,
            isUser: false,
          ),
        ),
      ],
    );
  }

  Widget _buildProfileCard(bool isDark, Color primary, String name,
      String streak, bool isLeading, String imageUrl,
      {required bool isUser}) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isDark ? Colors.white.withValues(alpha: 0.05) : Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color:
              isDark ? Colors.white.withValues(alpha: 0.1) : Colors.grey[200]!,
        ),
      ),
      child: Column(
        children: [
          Stack(
            clipBehavior: Clip.none,
            children: [
              Container(
                width: 80,
                height: 80,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  border: Border.all(
                    color: isUser
                        ? primary
                        : (isDark
                            ? Colors.white.withValues(alpha: 0.2)
                            : Colors.grey[300]!),
                    width: 4,
                  ),
                  image: DecorationImage(
                    image: CachedNetworkImageProvider(imageUrl),
                    fit: BoxFit.cover,
                  ),
                ),
              ),
              if (isUser)
                Positioned(
                  bottom: -8,
                  right: -8,
                  child: Container(
                    padding: const EdgeInsets.all(4),
                    decoration: const BoxDecoration(
                      color: Colors.orange,
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(Icons.local_fire_department,
                        color: Colors.white, size: 16),
                  ),
                ),
            ],
          ),
          const SizedBox(height: 16),
          Text(
            name,
            style: GoogleFonts.lexend(
              color: isDark ? Colors.white : const Color(0xFF0F172A),
              fontSize: 20,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 8),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.baseline,
            textBaseline: TextBaseline.alphabetic,
            children: [
              Text(
                streak,
                style: GoogleFonts.lexend(
                  color: isLeading
                      ? AppColors.primaryGold
                      : Colors.grey, // Gold for leader
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(width: 4),
              Text(
                'DAYS',
                style: GoogleFonts.lexend(
                  color: isLeading ? AppColors.primaryGold : Colors.grey,
                  fontSize: 10,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
          Text(
            'STREAK',
            style: TextStyle(
              color: isDark
                  ? Colors.white.withValues(alpha: 0.4)
                  : Colors.grey[400],
              fontSize: 10,
              fontWeight: FontWeight.bold,
              letterSpacing: 1.5,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildXPStats(
      bool isDark, Color primary, FocusBuddiesViewModel viewModel) {
    return Row(
      children: [
        Expanded(
          child: _buildStatCard(
            isDark,
            'Total Team XP',
            viewModel.teamXP,
            viewModel.teamGrowth,
            const Color(0xFF10B981),
          ),
        ),
        const SizedBox(width: 16),
        Expanded(
          child: _buildStatCard(
            isDark,
            'Days Active',
            viewModel.daysActive,
            viewModel.activeGrowth,
            const Color(0xFF10B981),
          ),
        ),
      ],
    );
  }

  Widget _buildStatCard(bool isDark, String label, String value, String growth,
      Color growthColor) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: isDark ? Colors.white.withValues(alpha: 0.05) : Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color:
              isDark ? Colors.white.withValues(alpha: 0.1) : Colors.grey[200]!,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label.toUpperCase(),
            style: GoogleFonts.lexend(
              color: isDark
                  ? Colors.white.withValues(alpha: 0.6)
                  : Colors.grey[500],
              fontSize: 10,
              fontWeight: FontWeight.bold,
              letterSpacing: 1,
            ),
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              Text(
                value,
                style: GoogleFonts.lexend(
                  color: isDark ? Colors.white : const Color(0xFF0F172A),
                  fontSize: 24,
                  fontWeight: FontWeight.w900,
                ),
              ),
              const SizedBox(width: 8),
              Text(
                growth,
                style: GoogleFonts.lexend(
                  color: growthColor,
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildActivityFeed(
      bool isDark, Color primary, FocusBuddiesViewModel viewModel) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'LIVE FEED',
          style: GoogleFonts.lexend(
            color: isDark ? Colors.white : const Color(0xFF0F172A),
            fontSize: 14,
            fontWeight: FontWeight.bold,
            letterSpacing: 1.5,
          ),
        ),
        const SizedBox(height: 16),
        ...viewModel.feedItems.map((item) {
          IconData icon;
          Color iconColor;
          Color bgColor;

          switch (item.iconType) {
            case FeedIconType.check:
              icon = Icons.check_circle;
              iconColor = const Color(0xFF10B981);
              bgColor = const Color(0xFF10B981).withValues(alpha: 0.1);
              break;
            case FeedIconType.notification:
              icon = Icons.notifications_active;
              iconColor = primary;
              bgColor = isDark
                  ? Colors.white.withValues(alpha: 0.05)
                  : Colors.grey[100]!;
              break;
            case FeedIconType.bolt:
              icon = Icons.bolt;
              iconColor = Colors.orange;
              bgColor = Colors.orange.withValues(alpha: 0.1);
              break;
          }

          return Padding(
            padding: const EdgeInsets.only(bottom: 12),
            child: _buildFeedItem(
              isDark,
              icon,
              iconColor,
              bgColor,
              item.text,
              isNotification: item.isActionable,
            ),
          );
        }),
      ],
    );
  }

  Widget _buildFeedItem(
      bool isDark, IconData icon, Color iconColor, Color bgColor, String text,
      {bool isNotification = false}) {
    // rudimentary parsing for bolding
    // final parts = text.split(' ');

    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: isNotification
              ? (isDark
                  ? Colors.white.withValues(alpha: 0.1)
                  : Colors.grey[200]!)
              : iconColor.withValues(alpha: 0.2),
        ),
      ),
      child: Row(
        children: [
          Icon(icon, color: iconColor, size: 24),
          const SizedBox(width: 12),
          Expanded(
            child: RichText(
              text: TextSpan(
                style: GoogleFonts.lexend(
                  color: isDark ? Colors.white : const Color(0xFF0F172A),
                  fontSize: 14,
                ),
                children: _parseFeedText(text, iconColor, isDark),
              ),
            ),
          ),
        ],
      ),
    );
  }

  List<TextSpan> _parseFeedText(
      String text, Color highlightColor, bool isDark) {
    if (text.contains('Morning Stack')) {
      return [
        const TextSpan(
            text: 'You', style: TextStyle(fontWeight: FontWeight.bold)),
        const TextSpan(text: ' logged Morning Stack! '),
        TextSpan(
            text: '+50 XP',
            style:
                TextStyle(color: highlightColor, fontWeight: FontWeight.bold)),
      ];
    } else if (text.contains('Alex')) {
      return [
        const TextSpan(
            text: 'Alex', style: TextStyle(fontWeight: FontWeight.bold)),
        const TextSpan(text: ' needs a nudge for Afternoon Stack.'),
      ];
    }
    return [TextSpan(text: text)];
  }

  Widget _buildCallToAction(
      bool isDark, Color primary, FocusBuddiesViewModel viewModel) {
    return Column(
      children: [
        SizedBox(
          width: double.infinity,
          height: 56,
          child: ElevatedButton(
            onPressed: () {
              // Show confirmation dialog before sending nudge
              showDialog<void>(
                context: context,
                builder: (context) => AlertDialog(
                  title: const Text('Send Nudge?'),
                  content: Text(
                    'This will send "Don\'t forget your stack!" notification to ${viewModel.opponentName}.',
                  ),
                  actions: [
                    TextButton(
                      onPressed: () => Navigator.pop(context),
                      child: const Text('Cancel'),
                    ),
                    TextButton(
                      onPressed: () async {
                        Navigator.pop(context);
                        await viewModel.sendNudge();
                        if (context.mounted) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text(
                                  'Nudge sent to ${viewModel.opponentName}! ⚡'),
                              backgroundColor: primary,
                            ),
                          );
                        }
                      },
                      child: const Text('Send'),
                    ),
                  ],
                ),
              );
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: primary,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(28),
              ),
              elevation: 4,
              shadowColor: primary.withValues(alpha: 0.4),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.bolt, color: Colors.white, size: 24),
                const SizedBox(width: 12),
                Text(
                  'Nudge ${viewModel.opponentName}',
                  style: GoogleFonts.lexend(
                    color: Colors.white,
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 12),
        Text(
          'Sends "Don\'t forget your stack!" alert',
          style: GoogleFonts.lexend(
            color:
                isDark ? Colors.white.withValues(alpha: 0.4) : Colors.grey[500],
            fontSize: 12,
            fontWeight: FontWeight.w500,
          ),
        ),
      ],
    );
  }

  Widget _buildSecondaryActions(bool isDark) {
    return Row(
      children: [
        Expanded(
          child: _buildSecondaryButton(
            isDark,
            Icons.share,
            'Share Stats',
            onTap: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text('Sharing team stats...'),
                ),
              );
            },
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: _buildSecondaryButton(
            isDark,
            Icons.history,
            'Log History',
            onTap: () {
              Navigator.pushNamed(context, AppRouter.historyLog);
            },
          ),
        ),
      ],
    );
  }

  Widget _buildSecondaryButton(bool isDark, IconData icon, String label,
      {required VoidCallback onTap}) {
    return Container(
      height: 48,
      decoration: BoxDecoration(
        color: isDark ? Colors.white.withValues(alpha: 0.1) : Colors.grey[200],
        borderRadius: BorderRadius.circular(24),
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(24),
          onTap: onTap,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon,
                  size: 20,
                  color: isDark ? Colors.white : const Color(0xFF334155)),
              const SizedBox(width: 8),
              Text(
                label,
                style: GoogleFonts.lexend(
                  color: isDark ? Colors.white : const Color(0xFF334155),
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _showInviteDialog(
      BuildContext context, FocusBuddiesViewModel viewModel, Color primary) {
    final emailController = TextEditingController();

    showDialog<void>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(
          'Invite Friend',
          style: GoogleFonts.lexend(
            fontWeight: FontWeight.bold,
          ),
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              'Enter email or username to invite a new accountability partner.',
              style: GoogleFonts.lexend(),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: emailController,
              decoration: const InputDecoration(
                hintText: 'Email or Username',
                border: OutlineInputBorder(),
              ),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text(
              'Cancel',
              style: GoogleFonts.lexend(
                color: Colors.grey,
              ),
            ),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              viewModel.addBuddy(emailController.text);
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content:
                      Text('Invitation sent to ${emailController.text}! 📩'),
                  backgroundColor: primary,
                ),
              );
            },
            child: Text(
              'Invite',
              style: GoogleFonts.lexend(
                fontWeight: FontWeight.bold,
                color: primary,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
