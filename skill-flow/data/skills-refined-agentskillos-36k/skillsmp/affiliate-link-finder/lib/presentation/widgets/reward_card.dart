import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class RewardCard extends StatelessWidget {
  const RewardCard({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: Colors.white.withValues(alpha: 0.2)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.2),
            blurRadius: 20,
            spreadRadius: 5,
          ),
        ],
      ),
      child: Column(
        children: [
          // Header
          Row(
            children: [
              Container(
                width: 48,
                height: 48,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(16),
                  gradient: const LinearGradient(
                    begin: Alignment.bottomLeft,
                    end: Alignment.topRight,
                    colors: [
                      AppColors.primaryBlue,
                      Color(0xFFC084FC), // purple-400
                    ],
                  ),
                ),
                child: const Icon(Icons.card_giftcard,
                    color: Colors.white, size: 24),
              ),
              const SizedBox(width: 16),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Unlocked Reward',
                    style: TextStyle(
                      color: Colors.grey[400],
                      fontSize: 14,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                  const Text(
                    'New Custom Pill Shape',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ],
          ),
          const SizedBox(height: 16),

          // Inner Item
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.white.withValues(alpha: 0.05),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
            ),
            child: Row(
              children: [
                Container(
                  width: 40,
                  height: 40,
                  decoration: BoxDecoration(
                    color: AppColors.primaryGold.withValues(alpha: 0.2),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child:
                      const Icon(Icons.pentagon, color: AppColors.primaryGold),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Gemstone Shape',
                        style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                          fontSize: 14,
                        ),
                      ),
                      Text(
                        'Available in your stack editor',
                        style: TextStyle(
                          color: Colors.grey[400],
                          fontSize: 12,
                        ),
                      ),
                    ],
                  ),
                ),
                const Icon(Icons.verified, color: AppColors.primaryGold),
              ],
            ),
          ),

          const SizedBox(height: 16),

          // XP Text
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.stars, color: AppColors.primaryGold, size: 16),
              const SizedBox(width: 8),
              Text(
                '+500 EXPERIENCE POINTS',
                style: TextStyle(
                  color: AppColors.primaryGold.withValues(alpha: 0.8),
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 0.5,
                ),
              ),
              const SizedBox(width: 8),
              const Icon(Icons.stars, color: AppColors.primaryGold, size: 16),
            ],
          ),
        ],
      ),
    );
  }
}
