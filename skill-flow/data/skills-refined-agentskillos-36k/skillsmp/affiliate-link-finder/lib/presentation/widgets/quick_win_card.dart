import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class QuickWinColors {
  final Color backgroundColor;
  final Color darkBackgroundColor;
  final Color iconBackgroundColor;
  final Color darkIconBackgroundColor;
  final Color iconColor;
  final Color darkIconColor;
  final Color highlightColor;
  final Color darkHighlightColor;

  const QuickWinColors({
    required this.backgroundColor,
    required this.darkBackgroundColor,
    required this.iconBackgroundColor,
    required this.darkIconBackgroundColor,
    required this.iconColor,
    required this.darkIconColor,
    required this.highlightColor,
    required this.darkHighlightColor,
  });
}

class QuickWinCard extends StatelessWidget {
  final String title;
  final String descriptionPrefix;
  final String descriptionHighlight;
  final String descriptionSuffix;
  final IconData icon;
  final QuickWinColors colors;
  final bool showGlow;

  const QuickWinCard({
    super.key,
    required this.title,
    required this.descriptionPrefix,
    required this.descriptionHighlight,
    required this.descriptionSuffix,
    required this.icon,
    required this.colors,
    this.showGlow = false,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      clipBehavior: Clip.antiAlias,
      decoration: BoxDecoration(
        color: isDark ? colors.darkBackgroundColor : colors.backgroundColor,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isDark ? Colors.white.withValues(alpha: 0.05) : Colors.grey.withValues(alpha: 0.1),
        ),
        boxShadow: [
          BoxShadow(
             color: Colors.black.withValues(alpha: 0.02),
             blurRadius: 4,
             offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Stack(
        children: [
           if (showGlow)
            Positioned(
              right: -20,
              top: -20,
              child: Container(
                width: 100,
                height: 100,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: (isDark ? colors.darkIconColor : colors.iconColor).withValues(alpha: 0.1),
                  boxShadow: [
                    BoxShadow(
                      color: (isDark ? colors.darkIconColor : colors.iconColor).withValues(alpha: 0.2),
                      blurRadius: 40,
                      spreadRadius: 10,
                    ),
                  ],
                ),
              ),
            ),
            
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  width: 48,
                  height: 48,
                  decoration: BoxDecoration(
                    color: isDark ? colors.darkIconBackgroundColor : colors.iconBackgroundColor,
                    shape: BoxShape.circle,
                  ),
                  child: Icon(
                    icon,
                    color: isDark ? colors.darkIconColor : colors.iconColor,
                    size: 24,
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        title,
                        style: Theme.of(context).textTheme.bodySmall?.copyWith(
                              color: isDark ? AppColors.textSecondaryDark : AppColors.textSecondaryLight,
                              fontWeight: FontWeight.w600,
                            ),
                      ),
                      const SizedBox(height: 4),
                      RichText(
                        text: TextSpan(
                          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                color: isDark ? AppColors.textPrimaryDark : AppColors.textPrimaryLight,
                                fontWeight: FontWeight.bold,
                                height: 1.3,
                              ),
                          children: [
                            TextSpan(text: descriptionPrefix),
                            TextSpan(
                              text: descriptionHighlight,
                              style: TextStyle(
                                color: isDark ? colors.darkHighlightColor : colors.highlightColor,
                              ),
                            ),
                            TextSpan(text: descriptionSuffix),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
