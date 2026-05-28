import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class StackItemCard extends StatefulWidget {
  final String name;
  final String dosage;
  final IconData icon;
  final Color iconColor;
  final Color iconBgColor;
  final VoidCallback onRemove;
  final VoidCallback? onTap;

  const StackItemCard({
    super.key,
    required this.name,
    required this.dosage,
    required this.icon,
    required this.iconColor,
    required this.iconBgColor,
    required this.onRemove,
    this.onTap,
  });

  @override
  State<StackItemCard> createState() => _StackItemCardState();
}

class _StackItemCardState extends State<StackItemCard>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 300),
    );
    _animation = CurvedAnimation(parent: _controller, curve: Curves.easeOut);
    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: _animation,
      child: SlideTransition(
        position: Tween<Offset>(
          begin: const Offset(0, -0.2),
          end: Offset.zero,
        ).animate(_animation),
        child: Container(
          margin: const EdgeInsets.only(bottom: 8),
          decoration: BoxDecoration(
            color: AppColors.cardDark,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.05),
                blurRadius: 2,
                offset: const Offset(0, 1),
              ),
            ],
          ),
          child: InkWell(
            onTap: widget.onTap,
            borderRadius: BorderRadius.circular(12),
            child: Padding(
              padding: const EdgeInsets.all(12),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Row(
                      children: [
                        Container(
                          width: 32,
                          height: 32,
                          decoration: BoxDecoration(
                            color: widget.iconBgColor,
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Icon(widget.icon,
                              color: widget.iconColor, size: 20),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                widget.name,
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontSize: 14,
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                              Row(
                                children: [
                                  Flexible(
                                    child: Text(
                                      widget.dosage.isEmpty
                                          ? 'No dosage set'
                                          : widget.dosage,
                                      maxLines: 1,
                                      overflow: TextOverflow.ellipsis,
                                      style: const TextStyle(
                                        color: AppColors.textSecondaryDark,
                                        fontSize: 12,
                                      ),
                                    ),
                                  ),
                                  if (widget.onTap != null) ...[
                                    const SizedBox(width: 4),
                                    const Icon(Icons.edit_outlined,
                                        size: 12, color: AppColors.primary),
                                  ],
                                ],
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                  IconButton(
                    onPressed: widget.onRemove,
                    icon: const Icon(Icons.remove_circle_outline,
                        color: AppColors.textSecondaryDark, size: 20),
                    style: IconButton.styleFrom(
                      hoverColor: Colors.red.withValues(alpha: 0.1),
                      highlightColor: Colors.red.withValues(alpha: 0.2),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
