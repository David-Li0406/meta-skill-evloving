import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../application/view_models/trophy_room_view_model.dart';
import '../../application/providers/auth_provider.dart';
import '../../config/locator.dart';
import '../../domain/entities/gamification.dart';
import '../theme/app_theme.dart';

class TrophyRoomScreen extends StatelessWidget {
  const TrophyRoomScreen({super.key});

  static Widget withProvider() {
    return Consumer<AuthProvider>(
      builder: (context, auth, _) {
        final userId = auth.user?.id ?? 'user_1';
        return ChangeNotifierProvider(
          create: (_) => locator<TrophyRoomViewModel>(param1: userId),
          child: const TrophyRoomScreen(),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    const primaryGold = AppColors.primaryGold;
    const bgDark = Color(0xFF190F23);
    const bgLight = Color(0xFFF7F5F8);

    return Scaffold(
      backgroundColor: isDark ? bgDark : bgLight,
      body: Consumer<TrophyRoomViewModel>(
        builder: (context, viewModel, child) {
          if (viewModel.isLoading) {
            return const Center(
                child: CircularProgressIndicator(color: primaryGold));
          }
          final profile = viewModel.profile;
          if (profile == null) {
            return const Center(child: Text('Failed to load profile'));
          }

          return Stack(
            children: [
              CustomScrollView(
                slivers: [
                  _buildAppBar(context, isDark, primaryGold),
                  SliverToBoxAdapter(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        _buildProgressHeader(isDark, primaryGold, profile),
                        const SizedBox(height: 24),
                        _buildRecentWins(
                            isDark, primaryGold, viewModel.recentWins),
                        const SizedBox(height: 32),
                        _buildTrophyGrid(
                            isDark, primaryGold, viewModel.allGridBadges),
                        const SizedBox(
                            height: 120), // Bottom padding for fixed button
                      ],
                    ),
                  ),
                ],
              ),
              Positioned(
                left: 24,
                right: 24,
                bottom: 32,
                child: _buildContinueButton(primaryGold),
              ),
            ],
          );
        },
      ),
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
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: isDark
                ? Colors.white.withValues(alpha: 0.05)
                : Colors.black.withValues(alpha: 0.05),
            shape: BoxShape.circle,
          ),
          child: Icon(Icons.arrow_back_ios_new,
              size: 18, color: isDark ? Colors.white : Colors.black),
        ),
        onPressed: () => Navigator.pop(context),
      ),
      title: Text(
        'Trophy Room',
        style: GoogleFonts.lexend(
          color: isDark ? Colors.white : Colors.black,
          fontSize: 18,
          fontWeight: FontWeight.bold,
        ),
      ),
      centerTitle: true,
      actions: [
        Padding(
          padding: const EdgeInsets.only(right: 16),
          child: Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              color: isDark
                  ? Colors.white.withValues(alpha: 0.05)
                  : Colors.black.withValues(alpha: 0.05),
              shape: BoxShape.circle,
            ),
            child: Icon(Icons.share,
                size: 20, color: isDark ? Colors.white : Colors.black),
          ),
        ),
      ],
    );
  }

  Widget _buildProgressHeader(
      bool isDark, Color primary, GamificationProfile profile) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Your Legend',
                    style: GoogleFonts.lexend(
                      color: isDark ? Colors.white : Colors.black,
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    'Level ${profile.level} ${profile.levelTitle}',
                    style: GoogleFonts.lexend(
                      color: isDark
                          ? const Color(0xFF94A3B8)
                          : const Color(0xFF64748B),
                      fontSize: 14,
                    ),
                  ),
                ],
              ),
              Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  Text(
                    '${profile.earnedBadgesCount}/${profile.totalBadgesCount}',
                    style: GoogleFonts.lexend(
                      color: primary,
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    'BADGES',
                    style: GoogleFonts.lexend(
                      color: isDark
                          ? const Color(0xFF94A3B8)
                          : const Color(0xFF64748B),
                      fontSize: 10,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 1.5,
                    ),
                  ),
                ],
              ),
            ],
          ),
          const SizedBox(height: 16),
          LayoutBuilder(builder: (context, constraints) {
            final progressWidth =
                constraints.maxWidth * profile.progress.clamp(0.0, 1.0);
            return ClipRRect(
              borderRadius: BorderRadius.circular(10),
              child: Stack(
                children: [
                  Container(
                    height: 12,
                    width: double.infinity,
                    color: isDark
                        ? Colors.white.withValues(alpha: 0.1)
                        : Colors.black.withValues(alpha: 0.05),
                  ),
                  Container(
                    height: 12,
                    width: progressWidth,
                    decoration: BoxDecoration(
                      color: primary,
                      boxShadow: [
                        BoxShadow(
                          color: primary.withValues(alpha: 0.5),
                          blurRadius: 10,
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            );
          }),
          const SizedBox(height: 8),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                '${profile.xpToNextLevel - profile.currentXp} XP to Level ${profile.level + 1}',
                style: GoogleFonts.lexend(
                  color: isDark
                      ? Colors.white.withValues(alpha: 0.7)
                      : Colors.black.withValues(alpha: 0.7),
                  fontSize: 11,
                  fontWeight: FontWeight.w500,
                ),
              ),
              Text(
                '${(profile.progress * 100).toInt()}% Mastery',
                style: GoogleFonts.lexend(
                  color: isDark
                      ? Colors.white.withValues(alpha: 0.7)
                      : Colors.black.withValues(alpha: 0.7),
                  fontSize: 11,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildRecentWins(
      bool isDark, Color primary, List<GamificationBadge> badges) {
    if (badges.isEmpty) return const SizedBox.shrink();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24),
          child: Text(
            'LATEST WINS',
            style: GoogleFonts.lexend(
              color: primary,
              fontSize: 12,
              fontWeight: FontWeight.bold,
              letterSpacing: 1.5,
            ),
          ),
        ),
        const SizedBox(height: 16),
        SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          padding: const EdgeInsets.symmetric(horizontal: 24),
          child: Row(
            children: badges
                .map((badge) => Padding(
                      padding: const EdgeInsets.only(right: 24),
                      child: _buildWinBadge(
                        isDark,
                        badge: badge,
                        glow: true,
                      ),
                    ))
                .toList(),
          ),
        ),
      ],
    );
  }

  Widget _buildWinBadge(bool isDark,
      {required GamificationBadge badge, bool glow = false}) {
    return Column(
      children: [
        Container(
          width: 80,
          height: 80,
          padding: const EdgeInsets.all(3),
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [badge.color, badge.color.withValues(alpha: 0.6)],
            ),
            boxShadow: glow
                ? [
                    BoxShadow(
                      color: badge.color.withValues(alpha: 0.4),
                      blurRadius: 15,
                    ),
                  ]
                : [],
          ),
          child: Container(
            decoration: BoxDecoration(
              color: isDark ? const Color(0xFF190F23) : const Color(0xFFF7F5F8),
              shape: BoxShape.circle,
              border: Border.all(
                color: isDark
                    ? Colors.white.withValues(alpha: 0.2)
                    : Colors.black.withValues(alpha: 0.1),
                width: 2,
              ),
            ),
            child: Icon(
              badge.icon,
              color: badge.color,
              size: 32,
            ),
          ),
        ),
        const SizedBox(height: 12),
        Text(
          badge.title.split(' ').join('\n'), // Break lines for circle badges
          textAlign: TextAlign.center,
          style: GoogleFonts.lexend(
            color: isDark ? Colors.white : Colors.black,
            fontSize: 12,
            fontWeight: FontWeight.bold,
            height: 1.1,
          ),
        ),
      ],
    );
  }

  Widget _buildTrophyGrid(
      bool isDark, Color primary, List<GamificationBadge> badges) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Trophy Case',
            style: GoogleFonts.lexend(
              color: isDark ? Colors.white : Colors.black,
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 24),
          GridView.count(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            crossAxisCount: 2,
            mainAxisSpacing: 16,
            crossAxisSpacing: 16,
            childAspectRatio: 0.85,
            children: badges
                .map((badge) => _buildTrophyCard(
                      isDark,
                      primary: primary,
                      badge: badge,
                    ))
                .toList(),
          ),
        ],
      ),
    );
  }

  Widget _buildTrophyCard(bool isDark,
      {required Color primary, required GamificationBadge badge}) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: badge.isLocked
            ? (isDark
                ? Colors.white.withValues(alpha: 0.05)
                : Colors.black.withValues(alpha: 0.03))
            : (isDark ? Colors.white.withValues(alpha: 0.03) : Colors.white),
        borderRadius: BorderRadius.circular(24),
        border: Border.all(
          color: isDark
              ? Colors.white.withValues(alpha: 0.1)
              : Colors.black.withValues(alpha: 0.05),
        ),
      ),
      child: Opacity(
        opacity: badge.isLocked ? 0.7 : 1.0,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Stack(
              clipBehavior: Clip.none,
              children: [
                Container(
                  width: 64,
                  height: 64,
                  decoration: BoxDecoration(
                    color: badge.isLocked
                        ? Colors.white.withValues(alpha: 0.1)
                        : badge.color.withValues(alpha: 0.2),
                    shape: BoxShape.circle,
                    border: badge.isLocked
                        ? null
                        : Border.all(
                            color: badge.color,
                            width: 2,
                          ),
                    boxShadow: !badge.isLocked
                        ? [
                            BoxShadow(
                              color: badge.color.withValues(alpha: 0.4),
                              blurRadius: 10,
                            ),
                          ]
                        : null,
                  ),
                  child: Icon(
                    badge.icon,
                    color: badge.isLocked
                        ? (isDark
                            ? Colors.white.withValues(alpha: 0.4)
                            : Colors.black.withValues(alpha: 0.4))
                        : badge.color,
                    size: 32,
                  ),
                ),
                if (badge.isLocked)
                  Positioned(
                    bottom: -4,
                    right: -4,
                    child: Container(
                      padding: const EdgeInsets.all(4),
                      decoration: BoxDecoration(
                        color: isDark
                            ? const Color(0xFF190F23)
                            : const Color(0xFFF7F5F8),
                        shape: BoxShape.circle,
                        border: Border.all(
                          color: isDark
                              ? Colors.white.withValues(alpha: 0.2)
                              : Colors.black.withValues(alpha: 0.1),
                        ),
                      ),
                      child: Icon(
                        Icons.lock,
                        size: 14,
                        color: isDark
                            ? Colors.white.withValues(alpha: 0.6)
                            : Colors.black.withValues(alpha: 0.6),
                      ),
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 12),
            Text(
              badge.title,
              textAlign: TextAlign.center,
              style: GoogleFonts.lexend(
                color: isDark ? Colors.white : Colors.black,
                fontSize: 14,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              !badge.isLocked ? badge.subtitle.toUpperCase() : badge.subtitle,
              textAlign: TextAlign.center,
              style: GoogleFonts.lexend(
                color: badge.isLocked
                    ? (isDark
                        ? Colors.white.withValues(alpha: 0.5)
                        : Colors.black.withValues(alpha: 0.5))
                    : badge.color,
                fontSize: 10,
                fontWeight:
                    badge.isLocked ? FontWeight.normal : FontWeight.bold,
                fontStyle: badge.isLocked ? FontStyle.italic : FontStyle.normal,
              ),
            ),
            const SizedBox(height: 12),
            if (badge.isLocked) ...[
              ClipRRect(
                borderRadius: BorderRadius.circular(4),
                child: LinearProgressIndicator(
                  value: badge.progress,
                  backgroundColor: isDark
                      ? Colors.white.withValues(alpha: 0.1)
                      : Colors.black.withValues(alpha: 0.05),
                  valueColor: AlwaysStoppedAnimation<Color>(badge.color),
                  minHeight: 4,
                ),
              ),
              const SizedBox(height: 4),
              Text(
                '${badge.currentValue}/${badge.targetValue}',
                style: GoogleFonts.lexend(
                  color: isDark
                      ? Colors.white.withValues(alpha: 0.5)
                      : Colors.black.withValues(alpha: 0.5),
                  fontSize: 10,
                ),
              ),
              const SizedBox(height: 4),
              Text(
                '+${badge.xpReward} XP',
                style: GoogleFonts.lexend(
                  color: primary,
                  fontSize: 10,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ] else ...[
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                decoration: BoxDecoration(
                  color: badge.color.withValues(alpha: 0.2),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  badge.tier.name.toUpperCase(),
                  style: GoogleFonts.lexend(
                    color: badge.color,
                    fontSize: 8,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildContinueButton(Color primary) {
    return Container(
      height: 64,
      decoration: BoxDecoration(
        color: primary,
        borderRadius: BorderRadius.circular(32),
        boxShadow: [
          BoxShadow(
            color: primary.withValues(alpha: 0.3),
            blurRadius: 16,
            offset: const Offset(0, 8),
          ),
        ],
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.rocket_launch, color: Colors.white),
          const SizedBox(width: 8),
          Text(
            'Continue Progress',
            style: GoogleFonts.lexend(
              color: Colors.white,
              fontSize: 16,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }
}
