import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import 'package:cached_network_image/cached_network_image.dart';

class RecoveryHeaderCard extends StatelessWidget {
  const RecoveryHeaderCard({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      height: 250,
      decoration: BoxDecoration(
        color: AppColors.backgroundPremiumDark,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: AppColors.primaryGold.withValues(alpha: 0.15),
            blurRadius: 20,
            spreadRadius: 0,
          ),
        ],
        image: const DecorationImage(
          image: CachedNetworkImageProvider(
            'https://lh3.googleusercontent.com/aida-public/AB6AXuAURUrlhNHu4EDNycDi82Ij5LgIPR7s7c4Vj1Bt6wns5I8xZtAp9gNFxwRJ1HsSczt3j1CmWn68Kp2EAtowHesRmYDvJsSQp6bXOHE50KV6wQYeyuiq48rD2Fly57YxH7mOzMOEvFExbn1YhfLkEtBy7YwWydZYjoGP-k5vwNkpNK0UGYeIvSDDsCoYvz2_PNxJ8c4jVi8QgcXXTrCqJxcGh5xT0f0hkH0h9QNUs54LbsNQyCRd8B-Rv0nZb8eBegm8HO0dga1kPI4',
          ),
          fit: BoxFit.cover,
        ),
      ),
      child: Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(16),
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              Colors.transparent,
              const Color(0xFF221910).withValues(alpha: 0.8),
            ],
            stops: const [0.5, 1.0],
          ),
        ),
        child: const Column(
          mainAxisAlignment: MainAxisAlignment.end,
          children: [
            Icon(
              Icons
                  .battery_charging_full, // Closest match to battery_charging_80
              color: AppColors.primaryGold,
              size: 48,
            ),
            SizedBox(height: 8),
            Text(
              'BATTERY REPLENISHED',
              style: TextStyle(
                color: AppColors.primaryGold,
                fontSize: 14,
                fontWeight: FontWeight.w500,
                letterSpacing: 2.0,
              ),
            ),
            SizedBox(height: 24),
          ],
        ),
      ),
    );
  }
}
