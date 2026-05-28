import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class SupplementCard extends StatelessWidget {
  final String title;
  final String description;
  final String dosage;
  final String benefit;
  final int rating; // 0-5
  final List<String> tags;
  final String
      imageUrl; // For scaffold we might just use colors or placeholders if net image fails
  final Color imagePlaceholderColor;

  const SupplementCard({
    super.key,
    required this.title,
    required this.description,
    required this.dosage,
    required this.benefit,
    required this.rating,
    required this.tags,
    this.imageUrl = '',
    this.imagePlaceholderColor = Colors.grey,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: AppColors.cardBackground(isDark),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: AppColors.borderColor(isDark),
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 4,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      clipBehavior: Clip.antiAlias,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Banner Image Area
          Container(
            height: 140,
            width: double.infinity,
            color: imagePlaceholderColor,
            child: Stack(
              fit: StackFit.expand,
              children: [
                if (imageUrl.isNotEmpty)
                  Image.network(
                    imageUrl,
                    fit: BoxFit.cover,
                    errorBuilder: (ctx, err, stack) =>
                        Container(color: imagePlaceholderColor),
                  ),

                // Gradient Overlay
                Container(
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.topCenter,
                      end: Alignment.bottomCenter,
                      colors: [
                        Colors.transparent,
                        Colors.black.withValues(alpha: 0.6)
                      ],
                    ),
                  ),
                ),

                // High Evidence Tag
                Positioned(
                  left: 16,
                  bottom: 16,
                  child: Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: AppColors.primary.withValues(alpha: 0.9),
                      borderRadius: BorderRadius.circular(4),
                    ),
                    child: const Text(
                      'HIGH EVIDENCE',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                        letterSpacing: 1.0,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),

          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Header
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            benefit,
                            style: const TextStyle(
                              color: AppColors.primary,
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                              letterSpacing: 0.5,
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            title,
                            style: TextStyle(
                              color: isDark
                                  ? Colors.white
                                  : AppColors.textPrimaryLight,
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                    ),
                    Row(
                      children: List.generate(5, (index) {
                        return Icon(
                          Icons.star,
                          size: 16,
                          color:
                              index < rating ? Colors.amber : Colors.grey[400],
                        );
                      }),
                    ),
                  ],
                ),

                const SizedBox(height: 8),
                Text(
                  description,
                  style: TextStyle(
                    color: AppColors.textTertiary(isDark),
                    fontSize: 14,
                    height: 1.5,
                  ),
                ),

                const SizedBox(height: 12),

                // Tags
                Wrap(
                  spacing: 16,
                  runSpacing: 8,
                  children: tags.map((tag) {
                    IconData icon = Icons.check_circle;
                    if (tag.contains('food')) icon = Icons.restaurant;
                    if (tag.contains('bio')) icon = Icons.bolt;
                    if (tag.contains('Cognitive')) icon = Icons.psychology;
                    if (tag.contains('Daily')) icon = Icons.schedule;
                    if (tag.contains('Stimulant')) icon = Icons.medication;

                    return Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(icon,
                            size: 16, color: AppColors.textTertiary(isDark)),
                        const SizedBox(width: 6),
                        Text(
                          tag,
                          style: TextStyle(
                            color: AppColors.textTertiary(isDark),
                            fontSize: 12,
                          ),
                        ),
                      ],
                    );
                  }).toList(),
                ),

                const SizedBox(height: 16),
                Divider(color: AppColors.dividerColor(isDark)),
                const SizedBox(height: 16),

                // Footer
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'DAILY DOSAGE',
                          style: TextStyle(
                            color: AppColors.textTertiary(isDark),
                            fontSize: 10,
                            fontWeight: FontWeight.bold,
                            letterSpacing: 0.5,
                          ),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          dosage,
                          style: TextStyle(
                            color: isDark
                                ? Colors.white
                                : AppColors.textPrimaryLight,
                            fontSize: 14,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ],
                    ),
                    ElevatedButton.icon(
                      onPressed: () {},
                      icon: const Icon(Icons.add, size: 18),
                      label: const Text('Quick Add'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.primary,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(
                            horizontal: 16, vertical: 10),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                        elevation: 4,
                        shadowColor: AppColors.primary.withValues(alpha: 0.4),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
