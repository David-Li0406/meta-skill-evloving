import 'dart:ui';
import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import 'stack_item_card.dart';

// Definition of a draggable item data
class LibraryItemData {
  final String id;
  final String name;
  final String dosage;
  final IconData icon;
  final Color iconColor;
  final Color iconBgColor;

  LibraryItemData({
    required this.id,
    required this.name,
    required this.dosage,
    required this.icon,
    required this.iconColor,
    required this.iconBgColor,
  });
}

class StackDropZone extends StatefulWidget {
  final List<LibraryItemData> currentItems;
  final void Function(String) onItemDropped; // Now receives ID
  final void Function(int) onItemRemoved;
  final void Function(int, int)? onReorder;
  final void Function(int)? onItemTap;
  final String instructionText;

  const StackDropZone({
    super.key,
    required this.currentItems,
    required this.onItemDropped,
    required this.onItemRemoved,
    this.onReorder,
    this.onItemTap,
    this.instructionText = 'Drag supplements here to build your routine.',
  });

  @override
  State<StackDropZone> createState() => _StackDropZoneState();
}

class _StackDropZoneState extends State<StackDropZone> {
  bool _isHovering = false;

  @override
  Widget build(BuildContext context) {
    return DragTarget<String>(
      onWillAcceptWithDetails: (details) {
        setState(() => _isHovering = true);
        return true;
      },
      onLeave: (data) {
        setState(() => _isHovering = false);
      },
      onAcceptWithDetails: (details) {
        setState(() => _isHovering = false);
        widget.onItemDropped(details.data);
      },
      builder: (context, candidateData, rejectedData) {
        // unused isDark variable removed

        return AnimatedContainer(
          duration: const Duration(milliseconds: 300),
          width: double.infinity,
          constraints: const BoxConstraints(minHeight: 300),
          decoration: BoxDecoration(
            color: _isHovering
                ? AppColors.primary.withValues(alpha: 0.1)
                : AppColors.cardBackground(
                        Theme.of(context).brightness == Brightness.dark)
                    .withValues(alpha: 0.3),
            borderRadius: BorderRadius.circular(24),
            border: Border.all(
              color: _isHovering
                  ? AppColors.primary
                  : AppColors.secondary.withValues(alpha: 0.1),
              width: 2,
            ),
          ),
          child: Stack(
            children: [
              if (!_isHovering)
                Positioned.fill(
                  child: CustomPaint(
                    painter: _DashedBorderPainter(
                      color: AppColors.secondary.withValues(alpha: 0.1),
                      strokeWidth: 2,
                      gap: 6,
                    ),
                  ),
                ),
              Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  children: [
                    if (widget.currentItems.isEmpty)
                      Padding(
                        padding: const EdgeInsets.only(top: 80, bottom: 40),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Container(
                              padding: const EdgeInsets.all(20),
                              decoration: BoxDecoration(
                                color:
                                    AppColors.primary.withValues(alpha: 0.05),
                                shape: BoxShape.circle,
                              ),
                              child: Icon(
                                Icons.add_circle_outline,
                                size: 48,
                                color: AppColors.primary.withValues(alpha: 0.5),
                              ),
                            ),
                            const SizedBox(height: 16),
                            Text(
                              widget.instructionText,
                              textAlign: TextAlign.center,
                              style: TextStyle(
                                color: AppColors.textSecondaryDark
                                    .withValues(alpha: 0.8),
                                fontSize: 15,
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              'Drop items here to synchronize',
                              style: TextStyle(
                                color: AppColors.textSecondaryDark
                                    .withValues(alpha: 0.4),
                                fontSize: 12,
                              ),
                            ),
                          ],
                        ),
                      )
                    else ...[
                      ReorderableListView.builder(
                        shrinkWrap: true,
                        physics: const NeverScrollableScrollPhysics(),
                        itemCount: widget.currentItems.length,
                        onReorder: widget.onReorder ?? (oldIndex, newIndex) {},
                        itemBuilder: (context, index) {
                          final item = widget.currentItems[index];
                          return StackItemCard(
                            key: ValueKey(item.id),
                            name: item.name,
                            dosage: item.dosage,
                            icon: item.icon,
                            iconColor: item.iconColor,
                            iconBgColor: item.iconBgColor,
                            onRemove: () => widget.onItemRemoved(index),
                            onTap: widget.onItemTap != null
                                ? () => widget.onItemTap!(index)
                                : null,
                          );
                        },
                      ),
                    ],

                    // Drop Target Indicator at bottom when hovering OR when empty
                    if (_isHovering)
                      AnimatedOpacity(
                        opacity: _isHovering ? 1.0 : 0.0,
                        duration: const Duration(milliseconds: 200),
                        child: Container(
                          margin: const EdgeInsets.only(top: 12),
                          height: 56,
                          width: double.infinity,
                          decoration: BoxDecoration(
                            color: AppColors.primary.withValues(alpha: 0.2),
                            borderRadius: BorderRadius.circular(16),
                            border: Border.all(
                              color: AppColors.primary,
                              width: 2,
                            ),
                          ),
                          child: const Center(
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Icon(Icons.download, color: Colors.white),
                                SizedBox(width: 8),
                                Text(
                                  'Release to Add',
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 14,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ),
                  ],
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}

class _DashedBorderPainter extends CustomPainter {
  final Color color;
  final double strokeWidth;
  final double gap;

  _DashedBorderPainter(
      {required this.color, required this.strokeWidth, required this.gap});

  @override
  void paint(Canvas canvas, Size size) {
    final Paint paint = Paint()
      ..color = color
      ..strokeWidth = strokeWidth
      ..style = PaintingStyle.stroke;

    final Path path = Path()
      ..addRRect(RRect.fromRectAndRadius(
        Rect.fromLTWH(0, 0, size.width, size.height),
        const Radius.circular(16),
      ));

    final Path dashedPath = _dashPath(path, width: 10, space: gap);
    canvas.drawPath(dashedPath, paint);
  }

  Path _dashPath(Path source, {required double width, required double space}) {
    final Path dest = Path();
    for (final PathMetric metric in source.computeMetrics()) {
      double distance = 0;
      while (distance < metric.length) {
        dest.addPath(
          metric.extractPath(distance, distance + width),
          Offset.zero,
        );
        distance += width + space;
      }
    }
    return dest;
  }

  @override
  bool shouldRepaint(_DashedBorderPainter oldDelegate) {
    return oldDelegate.color != color;
  }
}
