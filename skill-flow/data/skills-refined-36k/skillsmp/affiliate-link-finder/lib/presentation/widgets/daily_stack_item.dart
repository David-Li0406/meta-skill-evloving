import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class DailyStackItem extends StatelessWidget {
  final String name;
  final String details;
  final IconData icon;
  final bool isTaken;
  final bool isSkipped;
  final VoidCallback onTap;
  final VoidCallback? onLongPress;
  final VoidCallback? onInfoTap;

  const DailyStackItem({
    super.key,
    required this.name,
    required this.details,
    required this.icon,
    this.isTaken = false,
    this.isSkipped = false,
    required this.onTap,
    this.onLongPress,
    this.onInfoTap,
    this.timeStatus,
  });

  final String? timeStatus;

  @override
  Widget build(BuildContext context) {
    // Capture theme brightness
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final cardColor = isDark ? AppColors.cardDark : AppColors.cardLight;
    final borderColor = isDark
        ? Colors.white.withValues(alpha: 0.05)
        : Colors.black.withValues(alpha: 0.05);
    final textColor = isDark ? Colors.white : AppColors.textPrimaryLight;
    final secondaryTextColor =
        isDark ? AppColors.textSecondaryDark : AppColors.textSecondaryLight;

    return GestureDetector(
      onLongPress: onLongPress,
      onTap: onTap, // Making the whole card tappable for toggle
      child: Opacity(
        opacity: isSkipped ? 0.6 : 1.0,
        child: Container(
          margin: const EdgeInsets.only(bottom: 12),
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: cardColor,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: borderColor),
            boxShadow: isDark
                ? null
                : [
                    BoxShadow(
                      color: Colors.black.withValues(alpha: 0.05),
                      blurRadius: 8,
                      offset: const Offset(0, 2),
                    ),
                  ],
          ),
          child: Stack(
            children: [
              // Three-dots options button (Left side)
              if (onLongPress != null)
                Positioned(
                  top: 8,
                  left: -8,
                  child: IconButton(
                    icon: Icon(
                      Icons.more_vert,
                      size: 20,
                      color: isDark ? Colors.white38 : Colors.black26,
                    ),
                    onPressed: onLongPress,
                  ),
                ),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Row(
                      children: [
                        Container(
                          width: 40,
                          height: 40,
                          decoration: BoxDecoration(
                            color: AppColors.primaryGold.withValues(alpha: 0.2),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Icon(icon,
                              color: AppColors.primaryGold, size: 22),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Row(
                                children: [
                                  Flexible(
                                    child: Text(
                                      name,
                                      style: TextStyle(
                                        color: textColor,
                                        fontSize: 14,
                                        fontWeight: FontWeight.w600,
                                      ),
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                  ),
                                  if (onInfoTap != null) ...[
                                    const SizedBox(width: 4),
                                    GestureDetector(
                                      onTap: onInfoTap,
                                      child: Icon(Icons.info_outline,
                                          size: 14,
                                          color: AppColors.primaryGold
                                              .withValues(alpha: 0.6)),
                                    ),
                                  ],
                                ],
                              ),
                              const SizedBox(height: 2),
                              Text(
                                details,
                                style: TextStyle(
                                  color: secondaryTextColor,
                                  fontSize: 12,
                                ),
                                overflow: TextOverflow.ellipsis,
                              ),
                              if (timeStatus != null) ...[
                                const SizedBox(height: 4),
                                Text(
                                  timeStatus!,
                                  style: const TextStyle(
                                    color: AppColors.primaryGold,
                                    fontSize: 12,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ],
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(width: 8),
                  InkWell(
                    onTap: onTap,
                    borderRadius: BorderRadius.circular(99),
                    child: AnimatedContainer(
                      duration: const Duration(milliseconds: 200),
                      width: 32,
                      height: 32,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: isSkipped
                            ? Colors.grey.withValues(alpha: 0.1)
                            : Colors.transparent,
                        border: Border.all(
                          color: isTaken
                              ? AppColors.accentGreen.withValues(alpha: 0.4)
                              : isSkipped
                                  ? Colors.grey.withValues(alpha: 0.4)
                                  : (isDark
                                      ? Colors.white.withValues(alpha: 0.1)
                                      : Colors.black.withValues(alpha: 0.1)),
                          width: 2,
                        ),
                      ),
                      child: isTaken
                          ? const Center(
                              child: Icon(Icons.check,
                                  color: AppColors.accentGreen, size: 20))
                          : isSkipped
                              ? const Center(
                                  child: Icon(Icons.close,
                                      color: Colors.grey, size: 20))
                              : null,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
