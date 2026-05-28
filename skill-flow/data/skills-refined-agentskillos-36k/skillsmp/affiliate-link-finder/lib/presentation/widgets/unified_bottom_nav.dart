import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/app_theme.dart';
import '../navigation/app_router.dart';

class UnifiedBottomNav extends StatelessWidget {
  final int currentIndex;

  const UnifiedBottomNav({
    super.key,
    required this.currentIndex,
  });

  void _onItemTapped(BuildContext context, int index) {
    if (index == currentIndex) return;

    String routeName;
    switch (index) {
      case 0:
        routeName = AppRouter.dashboard;
        break;
      case 1:
        routeName = AppRouter.dailyStack; // "Stacks"
        break;
      case 2:
        routeName = AppRouter.library;
        break;
      case 3:
        routeName = AppRouter.scienceHub; // "Hub"
        break;
      case 4:
        routeName = AppRouter.profile;
        break;
      default:
        routeName = AppRouter.dashboard;
    }

    // Use pushReplacement to avoid building a huge stack, creating a "tab" feel
    // Exception: Maybe keep Dashboard as root? For now, simple replacement is consistent.
    Navigator.pushReplacementNamed(context, routeName);
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    const primaryColor = AppColors.primaryGold;
    final unselectedColor = isDark ? Colors.grey[500] : Colors.grey[400];
    final backgroundColor =
        (isDark ? const Color(0xFF221D10) : const Color(0xFFF8F8F6))
            .withValues(alpha: 0.95);

    return Container(
      decoration: BoxDecoration(
        color: backgroundColor,
        border: Border(
          top: BorderSide(
            color: isDark
                ? Colors.white.withValues(alpha: 0.1)
                : Colors.black.withValues(alpha: 0.05),
          ),
        ),
      ),
      child: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 8),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _buildNavItem(
                context,
                index: 0,
                icon: Icons.calendar_today,
                label: 'Today',
                isSelected: currentIndex == 0,
                primaryColor: primaryColor,
                unselectedColor: unselectedColor!,
              ),
              _buildNavItem(
                context,
                index: 1,
                icon: Icons.layers,
                label: 'Stacks',
                isSelected: currentIndex == 1,
                primaryColor: primaryColor,
                unselectedColor: unselectedColor,
              ),
              _buildNavItem(
                context,
                index: 2,
                icon: Icons.auto_stories,
                label: 'Library', // Moved to 3rd position (index 2)
                isSelected: currentIndex == 2,
                primaryColor: primaryColor,
                unselectedColor: unselectedColor,
              ),
              _buildNavItem(
                context,
                index: 3,
                icon: Icons.science_outlined,
                label: 'Hub', // Moved to 4th position (index 3)
                isSelected: currentIndex == 3,
                primaryColor: primaryColor,
                unselectedColor: unselectedColor,
              ),
              _buildNavItem(
                context,
                index: 4,
                icon: Icons.account_circle, // 'person'
                label: 'Profile',
                isSelected: currentIndex == 4,
                primaryColor: primaryColor,
                unselectedColor: unselectedColor,
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildNavItem(
    BuildContext context, {
    required int index,
    required IconData icon,
    required String label,
    required bool isSelected,
    required Color primaryColor,
    required Color unselectedColor,
  }) {
    return InkWell(
      onTap: () => _onItemTapped(context, index),
      borderRadius: BorderRadius.circular(12),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              icon,
              color: isSelected ? primaryColor : unselectedColor,
              size: 24,
            ),
            const SizedBox(height: 4),
            Text(
              label,
              style: GoogleFonts.lexend(
                fontSize: 10,
                fontWeight: FontWeight.bold,
                color: isSelected ? primaryColor : unselectedColor,
                letterSpacing: 0.5,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
