import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../navigation/app_router.dart';

class MedicalDisclaimerScreen extends StatelessWidget {
  const MedicalDisclaimerScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      backgroundColor:
          isDark ? AppColors.backgroundDark : AppColors.backgroundLight,
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: SingleChildScrollView(
                padding:
                    const EdgeInsets.symmetric(horizontal: 24, vertical: 32),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const SizedBox(height: 20),
                    Center(
                      child: Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: AppColors.primary.withValues(alpha: 0.1),
                          shape: BoxShape.circle,
                        ),
                        child: const Icon(
                          Icons.health_and_safety_outlined,
                          color: AppColors.primary,
                          size: 64,
                        ),
                      ),
                    ),
                    const SizedBox(height: 32),
                    Text(
                      'Medical Disclaimer',
                      style: TextStyle(
                        fontSize: 32,
                        fontWeight: FontWeight.bold,
                        color: isDark ? Colors.white : Colors.black,
                        letterSpacing: -0.5,
                      ),
                    ),
                    const SizedBox(height: 16),
                    Text(
                      'Please read this carefully before you begin your journey with Daily Stack.',
                      style: TextStyle(
                        fontSize: 18,
                        color: isDark ? Colors.grey[300] : Colors.grey[700],
                        height: 1.4,
                      ),
                    ),
                    const SizedBox(height: 32),
                    _buildDisclaimerCard(
                      context,
                      isDark,
                      'Not Medical Advice',
                      'Daily Stack is an educational resource. The information provided is for informational purposes only and is not intended as medical advice, diagnosis, or treatment.',
                    ),
                    const SizedBox(height: 16),
                    _buildDisclaimerCard(
                      context,
                      isDark,
                      'Consult Your Physician',
                      'Always seek the advice of your physician or other qualified health provider before starting any new supplement, especially if you have an existing medical condition or are taking prescription medications.',
                    ),
                    const SizedBox(height: 16),
                    _buildDisclaimerCard(
                      context,
                      isDark,
                      'Personal Responsibility',
                      'By using this application, you acknowledge that you are responsible for your own health decisions and that Daily Stack is not liable for any adverse effects resulting from use of the information provided.',
                    ),
                    const SizedBox(height: 40),
                  ],
                ),
              ),
            ),
            _buildActionArea(context, isDark),
          ],
        ),
      ),
    );
  }

  Widget _buildDisclaimerCard(
      BuildContext context, bool isDark, String title, String content) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: isDark ? AppColors.cardDark : Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isDark
              ? Colors.white.withValues(alpha: 0.05)
              : Colors.grey.withValues(alpha: 0.1),
        ),
        boxShadow: [
          if (!isDark)
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.05),
              blurRadius: 10,
              offset: const Offset(0, 4),
            ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: const TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              color: AppColors.primary,
            ),
          ),
          const SizedBox(height: 12),
          Text(
            content,
            style: TextStyle(
              fontSize: 15,
              color: isDark ? Colors.grey[400] : Colors.grey[600],
              height: 1.5,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildActionArea(BuildContext context, bool isDark) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: isDark ? AppColors.backgroundDark : AppColors.backgroundLight,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.1),
            blurRadius: 20,
            offset: const Offset(0, -5),
          ),
        ],
      ),
      child: SizedBox(
        width: double.infinity,
        height: 60,
        child: ElevatedButton(
          onPressed: () => Navigator.pushReplacementNamed(
            context,
            AppRouter.onboardingGoals,
          ),
          style: ElevatedButton.styleFrom(
            backgroundColor: AppColors.primary,
            foregroundColor: Colors.white,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
            ),
            elevation: 0,
          ),
          child: const Text(
            'I Understand & Agree',
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      ),
    );
  }
}
