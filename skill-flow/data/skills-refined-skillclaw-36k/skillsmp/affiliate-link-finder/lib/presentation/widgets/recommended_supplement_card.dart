import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import 'package:cached_network_image/cached_network_image.dart';

class RecommendedSupplementCard extends StatelessWidget {
  final String title;
  final String description;
  final IconData icon;
  final String imageUrl;
  final bool isAdded;
  final VoidCallback onActionTap;

  const RecommendedSupplementCard({
    super.key,
    required this.title,
    required this.description,
    required this.icon,
    required this.imageUrl,
    required this.isAdded,
    required this.onActionTap,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF1C2027) : Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isDark
              ? Colors.grey[800]!.withValues(alpha: 0.5)
              : Colors.grey[100]!,
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 4,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Content Side
          Expanded(
            flex: 3,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Icon(
                      icon,
                      color: isAdded ? AppColors.primary : Colors.grey,
                      size: 20,
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        title,
                        style: TextStyle(
                          color:
                              isDark ? Colors.white : const Color(0xFF111713),
                          fontSize:
                              16, // Adjusted to match visual hierarchy better
                          fontWeight: FontWeight.bold,
                          letterSpacing: -0.5,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                Text(
                  description,
                  style: TextStyle(
                    color: isDark ? const Color(0xFF9DA8B9) : Colors.grey[600],
                    fontSize: 13,
                    height: 1.4,
                  ),
                ),
                const SizedBox(height: 16),

                // Action Button
                InkWell(
                  onTap: onActionTap,
                  borderRadius: BorderRadius.circular(8),
                  child: Container(
                    height: 40,
                    padding: const EdgeInsets.symmetric(horizontal: 16),
                    decoration: BoxDecoration(
                      color: isAdded
                          ? AppColors.primary
                          : (isDark
                              ? const Color(0xFF282F39)
                              : Colors.grey[200]),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          isAdded ? Icons.check_circle : Icons.add_circle,
                          color: isAdded
                              ? Colors.white
                              : (isDark ? Colors.grey[300] : Colors.grey[700]),
                          size: 18,
                        ),
                        const SizedBox(width: 8),
                        Text(
                          isAdded ? 'Keep' : 'Add',
                          style: TextStyle(
                            color: isAdded
                                ? Colors.white
                                : (isDark
                                    ? Colors.grey[300]
                                    : Colors.grey[700]),
                            fontSize: 14,
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

          const SizedBox(width: 16),

          // Image Side
          Container(
            width: 100,
            height: 100,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(12),
              color: isDark ? const Color(0xFF282F39) : Colors.grey[100],
              image: DecorationImage(
                image: CachedNetworkImageProvider(imageUrl),
                fit: BoxFit.cover,
                // Apply optional filters if needed according to design, e.g. opacity for unselected
                // opacity: isAdded ? 1.0 : 0.5, // Wireframe suggests opacity change for unselected
                colorFilter: isAdded
                    ? null
                    : const ColorFilter.mode(Colors.grey, BlendMode.saturation),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
