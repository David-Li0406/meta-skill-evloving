import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import 'package:cached_network_image/cached_network_image.dart';

class SafetyDetailScreen extends StatelessWidget {
  const SafetyDetailScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      backgroundColor: isDark ? AppColors.backgroundDark : Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: Icon(Icons.arrow_back_ios_new,
              color: isDark ? Colors.white : const Color(0xFF111418), size: 20),
          onPressed: () {},
        ),
        title: Text(
          'Safety Detail',
          style: TextStyle(
            color: isDark ? Colors.white : const Color(0xFF111418),
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Warning Banner
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: isDark
                      ? AppColors.warningAmber.withValues(alpha: 0.3)
                      : AppColors.warningAmber.withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(
                    color: isDark
                        ? AppColors.warningAmber.withValues(alpha: 0.5)
                        : Colors.amber.shade100,
                  ),
                ),
                child: Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(8),
                      decoration: BoxDecoration(
                        color: isDark
                            ? AppColors.warningAmber
                            : Colors.amber.shade100,
                        shape: BoxShape.circle,
                      ),
                      child: Icon(
                        Icons.warning_amber_rounded,
                        color: isDark ? Colors.white : Colors.amber.shade800,
                        size: 28,
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'INTERACTION DETECTED',
                            style: TextStyle(
                              color: isDark
                                  ? Colors.amber.shade200
                                  : Colors.amber.shade900,
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                              letterSpacing: 1.0,
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'Moderate Severity • Reduced Efficacy',
                            style: TextStyle(
                              color: isDark
                                  ? Colors.amber.shade100
                                  : Colors.amber.shade800,
                              fontSize: 14,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),

            // Headline
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 16, 16, 4),
              child: Text(
                'Vitamin C + Stimulant Medication',
                style: TextStyle(
                  color: isDark ? Colors.white : const Color(0xFF111418),
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  height: 1.2,
                  letterSpacing: -0.5,
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Text(
                'Commonly found in multivitamins and orange juice.',
                style: TextStyle(
                  color: isDark ? Colors.grey[400] : const Color(0xFF617289),
                  fontSize: 14,
                ),
              ),
            ),

            // Hero Illustration
            Padding(
              padding: const EdgeInsets.all(16),
              child: Container(
                height: 180,
                width: double.infinity,
                decoration: BoxDecoration(
                  color: isDark ? Colors.grey[800] : Colors.white,
                  borderRadius: BorderRadius.circular(16),
                  image: const DecorationImage(
                    image: CachedNetworkImageProvider(
                        'https://lh3.googleusercontent.com/aida-public/AB6AXuB-adbbLnJNcnGxGmQL1P9ncwbUp45axu7D2yFB-m-2uxE0VVb2Ok6VSu3GxQMCr7fzx5DI4qjoc3qVpw9EdO730wePvqFf-gABNDQZkgQNjOp58eMDVPnJOEbn15qMvbUUkwsVcLeFyitO02G8w3k9PGnBx-zZn7OMu_-km7q9jCq6AJq7OmnAm0prExDvYUo1K0FC5HArZK3u31Pm8Q51h0l9qmMxw9EXnkQpZB7uSmBljuhjilgoZ6GMlsjo7IKpKYBf9Houiak'),
                    fit: BoxFit.cover,
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withValues(alpha: 0.05),
                      blurRadius: 10,
                      offset: const Offset(0, 4),
                    ),
                  ],
                  border: Border.all(
                    color: isDark ? Colors.grey[800]! : Colors.grey[100]!,
                  ),
                ),
                alignment: Alignment.bottomLeft,
                child: Container(
                  padding: const EdgeInsets.all(16),
                  decoration: const BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.topCenter,
                      end: Alignment.bottomCenter,
                      colors: [Colors.transparent, Colors.black45],
                    ),
                    borderRadius:
                        BorderRadius.vertical(bottom: Radius.circular(16)),
                  ),
                  child: const Text(
                    'Detailed Interaction Analysis',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 14, // Matches wireframe class text-sm
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ),
              ),
            ),

            // Solution Card
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Container(
                clipBehavior: Clip.antiAlias,
                decoration: BoxDecoration(
                  color: isDark
                      ? const Color(0xFF111827)
                      : Colors.white, // dark:bg-gray-900
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(
                    color: AppColors.primary.withValues(alpha: 0.2),
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black
                          .withValues(alpha: 0.05), // shadow-lg equivalent-ish
                      blurRadius: 10,
                      offset: const Offset(0, 4),
                    ),
                  ],
                ),
                child: Column(
                  children: [
                    // Header
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 16, vertical: 8),
                      color: AppColors.primary,
                      width: double.infinity,
                      child: const Row(
                        children: [
                          Icon(Icons.check_circle,
                              color: Colors.white, size: 16),
                          SizedBox(width: 8),
                          Text(
                            'THE SOLUTION',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                              letterSpacing: 1.5,
                            ),
                          ),
                        ],
                      ),
                    ),
                    // Content
                    Padding(
                      padding: const EdgeInsets.all(20),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Wait 2 Hours',
                            style: TextStyle(
                              color: isDark
                                  ? Colors.white
                                  : const Color(0xFF111418),
                              fontSize: 24,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            'Take Vitamin C at least 2 hours before or after your stimulant medication to ensure full absorption.',
                            style: TextStyle(
                              color: isDark
                                  ? Colors.grey[300]
                                  : const Color(0xFF617289),
                              fontSize: 16,
                              height: 1.5,
                            ),
                          ),
                          const SizedBox(height: 20),
                          SizedBox(
                            width: double.infinity,
                            height: 48,
                            child: ElevatedButton(
                              onPressed: () {},
                              style: ElevatedButton.styleFrom(
                                backgroundColor: AppColors.primary,
                                foregroundColor: Colors.white,
                                elevation: 0,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(8),
                                ),
                              ),
                              child: const Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Icon(Icons.calendar_today, size: 20),
                                  SizedBox(width: 8),
                                  Text(
                                    'Add to Schedule',
                                    style: TextStyle(
                                      fontSize: 16,
                                      fontWeight: FontWeight.w600,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),

            // Risk Section
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 24, 16, 12),
              child: Row(
                children: [
                  Icon(Icons.error, color: Colors.amber[700], size: 24),
                  const SizedBox(width: 8),
                  Text(
                    'The Risk',
                    style: TextStyle(
                      color: isDark ? Colors.white : const Color(0xFF111418),
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: isDark
                      ? Colors.grey[800]!.withValues(alpha: 0.5)
                      : const Color(0xFFF9FAFB), // gray-50
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  'Ascorbic acid (Vitamin C) increases GI acidity, which blocks the absorption of amphetamine-based medications. It also acidifies the urine, causing the medication to be flushed from your system faster than intended.',
                  style: TextStyle(
                    color: isDark ? Colors.grey[300] : const Color(0xFF617289),
                    fontSize: 16,
                    height: 1.5,
                  ),
                ),
              ),
            ),

            // Science Section
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 24, 16, 16),
              child: Row(
                children: [
                  const Icon(Icons.science, color: AppColors.primary, size: 24),
                  const SizedBox(width: 8),
                  Text(
                    'The Science',
                    style: TextStyle(
                      color: isDark ? Colors.white : const Color(0xFF111418),
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
            Padding(
              padding: const EdgeInsets.only(left: 16, right: 16, bottom: 40),
              child: Column(
                children: [
                  _buildSciencePoint(context, 'pH Sensitivity',
                      'Stimulants are alkaline. Higher stomach acidity from Vitamin C prevents the medication from crossing into the bloodstream.'),
                  const SizedBox(height: 16),
                  _buildSciencePoint(context, 'Renal Clearance',
                      'Acidified urine increases the rate at which the kidneys filter out amphetamine salts, shortening the duration of effect.'),
                  const SizedBox(height: 16),
                  _buildSciencePoint(context, 'Metabolic Impact',
                      'The interaction can reduce effective medication levels by up to 30-50% in sensitive individuals.'),
                ],
              ),
            ),

            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }

  Widget _buildSciencePoint(
      BuildContext context, String title, String description) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Padding(
          padding: EdgeInsets.only(top: 6),
          child: Icon(Icons.fiber_manual_record,
              color: AppColors.primary, size: 12),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: TextStyle(
                  color: isDark ? Colors.white : const Color(0xFF111418),
                  fontWeight: FontWeight.w600,
                  fontSize: 16,
                ),
              ),
              const SizedBox(height: 4),
              Text(
                description,
                style: TextStyle(
                  color: isDark ? Colors.grey[400] : const Color(0xFF617289),
                  fontSize: 14,
                  height: 1.4,
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
