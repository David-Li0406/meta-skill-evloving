import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class CustomFabBottomNav extends StatelessWidget {
  final int selectedIndex;
  final void Function(int) onTap;
  final VoidCallback? onFabTap;

  const CustomFabBottomNav({
    super.key,
    required this.selectedIndex,
    required this.onTap,
    this.onFabTap,
  });

  @override
  Widget build(BuildContext context) {
    return Stack(
      alignment: Alignment.bottomCenter,
      clipBehavior: Clip.none,
      children: [
        // Background Bar
        Container(
          height: 80,
          decoration: BoxDecoration(
            color: AppColors.cardDark,
            border: Border(
                top: BorderSide(color: Colors.white.withValues(alpha: 0.1))),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _buildNavItem(Icons.dashboard, 'Today', 0),
              _buildNavItem(Icons.history, 'History', 1),
              const SizedBox(width: 48), // Spacer for FAB
              _buildNavItem(Icons.insights, 'Trends', 2),
              _buildNavItem(Icons.person, 'Profile', 3),
            ],
          ),
        ),

        // FAB
        Positioned(
          top: -28,
          child: Container(
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              boxShadow: [
                BoxShadow(
                  color: AppColors.primaryGold.withValues(alpha: 0.3),
                  blurRadius: 10,
                  offset: const Offset(0, 4),
                ),
              ],
            ),
            child: FloatingActionButton(
              onPressed: onFabTap,
              backgroundColor: AppColors.primaryGold,
              foregroundColor: AppColors.backgroundPremiumDark,
              elevation: 0,
              shape: const CircleBorder(),
              child: const Icon(Icons.add, size: 32),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildNavItem(IconData icon, String label, int index) {
    final isSelected = selectedIndex == index;
    final color = isSelected ? AppColors.primaryGold : const Color(0xFF9DB9A8);

    return InkWell(
      onTap: () => onTap(index),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, color: color, size: 28),
          const SizedBox(height: 4),
          Text(
            label,
            style: TextStyle(
              color: color,
              fontSize: 10,
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }
}
