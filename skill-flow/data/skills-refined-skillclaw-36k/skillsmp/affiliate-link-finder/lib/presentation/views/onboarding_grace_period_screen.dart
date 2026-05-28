import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../navigation/app_router.dart';
import 'package:cached_network_image/cached_network_image.dart';

class OnboardingGracePeriodScreen extends StatelessWidget {
  const OnboardingGracePeriodScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      backgroundColor:
          isDark ? AppColors.backgroundDark : AppColors.backgroundLight,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: Padding(
          padding: const EdgeInsets.only(left: 16),
          child: Center(
            child: CircleAvatar(
              backgroundColor: isDark ? Colors.grey[800] : Colors.grey[200],
              radius: 20,
              child: IconButton(
                icon: Icon(
                  Icons.arrow_back_ios_new,
                  color: isDark ? Colors.white : Colors.black,
                  size: 16,
                ),
                padding: EdgeInsets.zero,
                onPressed: () {},
              ),
            ),
          ),
        ),
        title: Text(
          'Grace Day Philosophy',
          style: TextStyle(
            color: isDark ? Colors.white : Colors.black,
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
        centerTitle: true,
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Progress Bar Area
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      Text(
                        'Step 3 of 4',
                        style: TextStyle(
                          color: isDark ? Colors.white : Colors.black,
                          fontSize: 16,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                      Text(
                        '75% Complete',
                        style: TextStyle(
                          color: isDark ? Colors.grey[400] : Colors.grey[500],
                          fontSize: 14,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Container(
                    height: 8,
                    width: double.infinity,
                    decoration: BoxDecoration(
                      color: isDark ? Colors.grey[800] : Colors.grey[200],
                      borderRadius: BorderRadius.circular(999),
                    ),
                    child: FractionallySizedBox(
                      alignment: Alignment.centerLeft,
                      widthFactor: 0.75,
                      child: Container(
                        decoration: BoxDecoration(
                          color: AppColors.primary,
                          borderRadius: BorderRadius.circular(999),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),

            Expanded(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 24),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    // Hero Illustration
                    SizedBox(
                      width: 300,
                      height: 300,
                      child: Stack(
                        alignment: Alignment.center,
                        children: [
                          // Blur Effect
                          Container(
                            width: 280,
                            height: 280,
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              color: AppColors.primary
                                  .withValues(alpha: isDark ? 0.2 : 0.1),
                            ),
                          ),
                          // Image
                          Container(
                            width: 250,
                            height: 250,
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(24),
                              image: const DecorationImage(
                                image: CachedNetworkImageProvider(
                                  'https://lh3.googleusercontent.com/aida-public/AB6AXuCEKRevVdokOjFtFZvmgLdF8d_XggCSOWA8CgNp72pCfqV2jX6lj0_jbLWDth-3k1BnGNUfDRUeeAeFykEbYysmc9A13Np-e9ONWM9CenQ1GC24jycAAAO5-XUXbgBa-0XYdBSc9RiUUQ8Nq1w5Pt8BypRIx5aNyG0YdAueulirzo_SS9maP3ft_L8N9NbEujaoXx95tSu9QHJCY83pqpHW6ivG1APvJBPKJttkqNyhqG9TF0v3C8BB3GoSW28sOnf3HuA4OJCTRAQ',
                                ),
                                fit: BoxFit.contain,
                              ),
                            ),
                          ),
                          // Overlay Icons (fallback/enhancement)
                          // Note: The image url likely already contains the heart/flame composition.
                          // But I'll add them if the image fails or just rely on the image.
                          // The wireframe HTML has an image + overlay icons.
                          // I'll trust the visual from the wireframe screenshot which shows a nice composition.
                          // The image seems to be the main driver.
                        ],
                      ),
                    ),

                    const SizedBox(height: 32),

                    Text(
                      'Life happens.\nWe\'ve got you.',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: isDark ? Colors.white : Colors.black,
                        fontSize: 32,
                        fontWeight: FontWeight.bold,
                        height: 1.1,
                      ),
                    ),

                    const SizedBox(height: 16),

                    RichText(
                      textAlign: TextAlign.center,
                      text: TextSpan(
                        style: TextStyle(
                          color: isDark ? Colors.grey[300] : Colors.grey[600],
                          fontSize: 18,
                          height: 1.5,
                          fontFamily: 'Lexend', // Ensure font is consistent
                        ),
                        children: const [
                          TextSpan(text: 'We believe in '),
                          TextSpan(
                            text: 'Grace Days',
                            style: TextStyle(
                              color: AppColors.primary,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          TextSpan(
                              text:
                                  '. If you miss a dose, your streak doesn\'t reset. Our heart icon saves your flame so you can pick up right where you left off—no shame, just progress.'),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),

            // Bottom Action
            Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                children: [
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: () => Navigator.pushNamed(
                          context, AppRouter.onboardingGoals),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.primary,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(16),
                        ),
                        elevation: 8,
                        shadowColor: AppColors.primary.withValues(alpha: 0.25),
                        textStyle: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      child: const Text('Got it!'),
                    ),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    "You're almost there. Just one more step!",
                    style: TextStyle(
                      color: isDark ? Colors.grey[500] : Colors.grey[400],
                      fontSize: 14,
                    ),
                  ),
                  const SizedBox(height: 8),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
