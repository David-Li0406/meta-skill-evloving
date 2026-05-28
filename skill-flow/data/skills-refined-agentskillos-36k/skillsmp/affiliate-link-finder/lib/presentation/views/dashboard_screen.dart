import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../../config/locator.dart';
import '../../application/providers/auth_provider.dart';
import '../view_models/daily_stack_view_model.dart';
import '../widgets/medication_card.dart';
import '../widgets/daily_progress_card.dart';
import '../navigation/app_router.dart';
import '../../domain/entities/supplement_stack.dart';
import '../../domain/entities/supplement.dart';
import '../widgets/unified_bottom_nav.dart';
import '../theme/app_theme.dart';
import 'package:flutter/services.dart';
import '../widgets/skeleton_loader.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  late DailyStackViewModel _viewModel;
  // int _selectedIndex = 0; // Removed, handled by UnifiedBottomNav

  @override
  void initState() {
    super.initState();
    final authProvider = context.read<AuthProvider>();
    final userId = authProvider.user?.id ?? 'demo_user';
    _viewModel = locator.get<DailyStackViewModel>(param1: userId);
    _viewModel.initialize();
  }

  @override
  Widget build(BuildContext context) {
    // Determine greeting based on time (ViewModel has this logic too, but text might differ)
    // Using ViewModel's greeting logic

    final isDark = Theme.of(context).brightness == Brightness.dark;

    return ChangeNotifierProvider.value(
      value: _viewModel,
      child: Scaffold(
        backgroundColor:
            isDark ? AppColors.backgroundDark : AppColors.backgroundLight,
        body: SafeArea(
          child: Consumer<DailyStackViewModel>(
            builder: (context, viewModel, child) {
              if (viewModel.isLoading) {
                return _buildSkeleton(context);
              }

              if (viewModel.error != null) {
                return Center(child: Text('Error: ${viewModel.error}'));
              }

              final now = DateTime.now();
              final dateStr =
                  DateFormat("'TODAY', MMM d").format(now).toUpperCase();

              return CustomScrollView(
                slivers: [
                  SliverToBoxAdapter(
                    child: Padding(
                      padding: const EdgeInsets.all(24.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          // 1. Header Section
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      dateStr,
                                      style: const TextStyle(
                                        color: Colors.grey,
                                        fontSize: 12,
                                        fontWeight: FontWeight.bold,
                                        letterSpacing: 1.2,
                                      ),
                                    ),
                                    const SizedBox(height: 4),
                                    Text(
                                      '${viewModel.greeting}, Alex', // Name hardcoded as per spec "Good Morning, Alex" - ideally from AuthProvider
                                      style: TextStyle(
                                        color: isDark
                                            ? Colors.white
                                            : Colors.black87,
                                        fontSize: 28, // ~32px
                                        fontWeight: FontWeight.bold,
                                      ),
                                      maxLines: 1,
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                  ],
                                ),
                              ),
                              Row(
                                children: [
                                  Container(
                                    decoration: BoxDecoration(
                                      color: isDark
                                          ? const Color(0xFF1A1F2E)
                                          : Colors.grey[200],
                                      shape: BoxShape.circle,
                                    ),
                                    child: IconButton(
                                      icon: const Icon(Icons.search),
                                      color: isDark
                                          ? Colors.white
                                          : Colors.black54,
                                      onPressed: () => Navigator.pushNamed(
                                          context, AppRouter.globalSearch),
                                    ),
                                  ),
                                  const SizedBox(width: 8),
                                  Container(
                                    decoration: BoxDecoration(
                                      color: isDark
                                          ? const Color(0xFF1A1F2E)
                                          : Colors.grey[200],
                                      shape: BoxShape.circle,
                                    ),
                                    child: Consumer<AuthProvider>(
                                      builder: (context, auth, _) {
                                        final isPremium =
                                            auth.canAccess('stack_builder');
                                        return Stack(
                                          clipBehavior: Clip.none,
                                          children: [
                                            IconButton(
                                              icon: const Icon(
                                                  Icons.auto_awesome),
                                              color: AppColors.primaryGold,
                                              onPressed: () =>
                                                  Navigator.pushNamed(context,
                                                      AppRouter.stackBuilder),
                                            ),
                                            if (!isPremium)
                                              Positioned(
                                                top: 8,
                                                right: 8,
                                                child: Container(
                                                  padding:
                                                      const EdgeInsets.all(2),
                                                  decoration:
                                                      const BoxDecoration(
                                                    color:
                                                        AppColors.primaryGold,
                                                    shape: BoxShape.circle,
                                                  ),
                                                  child: const Icon(Icons.lock,
                                                      size: 8,
                                                      color: Colors.black),
                                                ),
                                              ),
                                          ],
                                        );
                                      },
                                    ),
                                  ),
                                ],
                              ),
                            ],
                          ),
                          const SizedBox(height: 32),

                          // 2. Daily Completion Progress
                          DailyProgressCard(
                            streakCount: viewModel.streakCount,
                            progress: viewModel.todayProgress,
                            isDark: isDark,
                          ),
                          const SizedBox(height: 32),

                          // Global Toggle
                          Align(
                            alignment: Alignment.centerRight,
                            child: TextButton.icon(
                              onPressed: viewModel.toggleAllExpansion,
                              icon: Icon(
                                viewModel.allCollapsed
                                    ? Icons.unfold_more
                                    : Icons.unfold_less,
                                size: 18,
                              ),
                              label: Text(
                                viewModel.allCollapsed
                                    ? "Expand All"
                                    : "Collapse All",
                                style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 12,
                                ),
                              ),
                              style: TextButton.styleFrom(
                                foregroundColor: AppColors.primaryGold,
                              ),
                            ),
                          ),
                          const SizedBox(height: 8),

                          // 3. Morning Focus
                          _buildSectionHeader(
                            context,
                            'Morning Focus',
                            viewModel,
                            stackId: 'morning',
                            timeBadge: viewModel
                                .getSlotTime('morning')
                                .format(context),
                            isNow: viewModel.greeting == 'Good Morning',
                          ),
                          const SizedBox(height: 16),
                          if (!viewModel.collapsedStackIds.contains('morning'))
                            ..._buildMedicationList(
                                viewModel.morningItems, viewModel, 'morning'),

                          const SizedBox(height: 32),

                          // 4. Afternoon Focus (if any)
                          if (viewModel.afternoonItems.isNotEmpty) ...[
                            _buildSectionHeader(
                              context,
                              'Afternoon Focus',
                              viewModel,
                              stackId: 'afternoon',
                              timeBadge: viewModel
                                  .getSlotTime('afternoon')
                                  .format(context),
                              isNow: viewModel.greeting == 'Good Afternoon',
                            ),
                            const SizedBox(height: 16),
                            if (!viewModel.collapsedStackIds
                                .contains('afternoon'))
                              ..._buildMedicationList(viewModel.afternoonItems,
                                  viewModel, 'afternoon'),
                            const SizedBox(height: 32),
                          ],

                          // 5. Evening Stack
                          _buildSectionHeader(
                            context,
                            'Evening Stack',
                            viewModel,
                            stackId: 'evening',
                            timeBadge: viewModel
                                .getSlotTime('evening')
                                .format(context),
                            isNow: viewModel.greeting == 'Good Evening',
                          ),
                          const SizedBox(height: 16),
                          if (!viewModel.collapsedStackIds.contains('evening'))
                            ..._buildMedicationList(
                                viewModel.eveningItems, viewModel, 'evening'),

                          const SizedBox(height: 32),

                          // 6. Night Stack (if any)
                          if (viewModel.nightItems.isNotEmpty) ...[
                            _buildSectionHeader(
                              context,
                              'Night Stack',
                              viewModel,
                              stackId: 'night',
                              timeBadge: viewModel
                                  .getSlotTime('night')
                                  .format(context),
                              isNow: viewModel.greeting == 'Good Night',
                            ),
                            const SizedBox(height: 16),
                            if (!viewModel.collapsedStackIds.contains('night'))
                              ..._buildMedicationList(
                                  viewModel.nightItems, viewModel, 'night'),
                          ],

                          const SizedBox(height: 80), // Bottom padding
                        ],
                      ),
                    ),
                  ),
                ],
              );
            },
          ),
        ),
        bottomNavigationBar: const UnifiedBottomNav(currentIndex: 0),
      ),
    );
  }

  Widget _buildSectionHeader(
      BuildContext context, String title, DailyStackViewModel viewModel,
      {required String stackId, bool isNow = false, String? timeBadge}) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final isCollapsed = viewModel.collapsedStackIds.contains(stackId);

    return GestureDetector(
      onTap: () => viewModel.toggleStackExpansion(stackId),
      behavior: HitTestBehavior.opaque,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Expanded(
            child: Row(
              children: [
                Text(
                  title,
                  style: TextStyle(
                    color: isDark ? Colors.white : Colors.black87,
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(width: 8),
                Icon(
                  isCollapsed
                      ? Icons.keyboard_arrow_down
                      : Icons.keyboard_arrow_up,
                  color: Colors.grey,
                  size: 20,
                ),
              ],
            ),
          ),
          if (isNow)
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
              decoration: BoxDecoration(
                color:
                    AppColors.primaryGold.withValues(alpha: 0.2), // Gold tint
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppColors.primaryGold),
              ),
              child: const Text(
                'NOW',
                style: TextStyle(
                  color: AppColors.primaryGold,
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                ),
              ),
            )
          else if (timeBadge != null)
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
              decoration: BoxDecoration(
                color: isDark
                    ? Colors.white.withValues(alpha: 0.1)
                    : Colors.grey[200],
                borderRadius: BorderRadius.circular(12),
              ),
              child: Text(
                timeBadge,
                style: const TextStyle(
                  color: Colors.grey,
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
        ],
      ),
    );
  }

  List<Widget> _buildMedicationList(List<StackItem> items,
      DailyStackViewModel viewModel, String sectionIdentifier) {
    if (items.isEmpty) {
      return [
        const Text('No medications scheduled',
            style: TextStyle(color: Colors.grey))
      ];
    }

    return items.map((item) {
      // item is StackItem
      final supplement = viewModel.getSupplement(item.supplementId);
      final isTaken = viewModel.isSupplementTaken(item.supplementId);
      final isSkipped = viewModel.isSupplementSkipped(item.supplementId);
      final isSnoozed = viewModel.isSupplementSnoozed(item.supplementId);
      final timeStatus = viewModel.getItemTimeStatus(item);

      String? statusText;
      Color? statusColor;

      if (isTaken) {
        statusText = 'Taken';
      } else if (isSkipped) {
        statusText = 'Skipped';
        statusColor = Colors.grey;
      } else if (isSnoozed) {
        statusText = 'Snoozed';
        statusColor = const Color(0xFF448AFF); // Blue
      } else if (timeStatus != null && timeStatus.contains('Overdue')) {
        statusText = timeStatus;
        statusColor = const Color(0xFFFF5252); // Red
      } else if (timeStatus != null) {
        statusText = timeStatus;
      }

      return MedicationCard(
        key: ValueKey('dash_${sectionIdentifier}_${item.supplementId}'),
        title: supplement?.name ?? 'Loading...',
        dosage: item.customDosage ?? supplement?.dosage ?? 'As directed',
        form: supplement?.form ?? 'Pill',
        icon: _getIconForType(supplement?.shapeIcon ?? 'pill'),
        iconColor: HexColor(supplement?.iconColor ?? '#FFB74D'),
        isTaken: isTaken,
        isSkipped: isSkipped,
        isUpcoming: false,
        statusText: statusText,
        statusColor: statusColor,
        onTap: () {
          if (supplement != null) {
            Navigator.pushNamed(context, AppRouter.supplementDetail,
                arguments: supplement);
          }
        },
        onTake: () async {
          // Play sound and haptic feedback
          HapticFeedback.mediumImpact();
          SystemSound.play(SystemSoundType.click);

          // Mark as taken
          await viewModel.markSupplementTaken(item.supplementId);

          // Show confirmation with streak
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Row(
                  children: [
                    const Icon(Icons.check_circle, color: Colors.white),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        'Success! That\'s ${viewModel.streakCount} days in a row!',
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                    ),
                  ],
                ),
                backgroundColor: AppColors.primaryGold,
                behavior: SnackBarBehavior.floating,
                duration: const Duration(seconds: 2),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
            );
          }
        },
        onMoreOptions: () => _showMedicationOptions(context, item, supplement),
      );
    }).toList();
  }

  void _showMedicationOptions(
      BuildContext context, StackItem item, Supplement? supplement) {
    showModalBottomSheet<void>(
      context: context,
      backgroundColor: Colors.transparent,
      builder: (context) => Container(
        decoration: BoxDecoration(
          color: Theme.of(context).scaffoldBackgroundColor,
          borderRadius: const BorderRadius.vertical(top: Radius.circular(20)),
        ),
        child: SafeArea(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(
                width: 40,
                height: 4,
                margin: const EdgeInsets.symmetric(vertical: 12),
                decoration: BoxDecoration(
                  color: Colors.grey[300],
                  borderRadius: BorderRadius.circular(2),
                ),
              ),
              ListTile(
                leading: const Icon(Icons.info_outline),
                title: const Text('View Details'),
                onTap: () {
                  Navigator.pop(context);
                  final supplement =
                      _viewModel.getSupplement(item.supplementId);
                  if (supplement != null) {
                    Navigator.pushNamed(context, AppRouter.supplementDetail,
                        arguments: supplement);
                  } else {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Details not available')),
                    );
                  }
                },
              ),
              ListTile(
                leading: const Icon(Icons.snooze),
                title: const Text('Snooze Reminder'),
                onTap: () {
                  Navigator.pop(context);
                  _viewModel.snoozeSupplement(item.supplementId);
                },
              ),
              ListTile(
                leading: const Icon(Icons.skip_next),
                title: const Text('Skip Dose'),
                onTap: () {
                  Navigator.pop(context);
                  _viewModel.markSupplementSkipped(item.supplementId,
                      reason: 'User Skipped');
                },
              ),
              ListTile(
                leading: const Icon(Icons.edit_outlined),
                title: const Text('Edit Schedule'),
                onTap: () {
                  Navigator.pop(context);
                  Navigator.pushNamed(context, AppRouter.stackBuilder);
                },
              ),
              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }

  IconData _getIconForType(String type) {
    switch (type.toLowerCase()) {
      case 'capsule':
        return Icons.circle; // Approximate for capsule if no specific icon
      case 'tablet':
        return Icons.circle_outlined;
      case 'liquid':
      case 'drop':
        return Icons.water_drop;
      case 'powder':
        return Icons.grain;
      case 'pill':
      default:
        return Icons.medication;
    }
  }
}

class HexColor extends Color {
  static int _getColorFromHex(String hexColor) {
    hexColor = hexColor.toUpperCase().replaceAll('#', '');
    if (hexColor.length == 6) {
      hexColor = 'FF$hexColor';
    }
    return int.parse(hexColor, radix: 16);
  }

  HexColor(final String hexColor) : super(_getColorFromHex(hexColor));
}

Widget _buildSkeleton(BuildContext context) {
  return const SingleChildScrollView(
    child: Padding(
      padding: EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  SkeletonLoader(height: 16, width: 100),
                  SizedBox(height: 8),
                  SkeletonLoader(height: 32, width: 200),
                ],
              ),
              SkeletonLoader(height: 40, width: 40, borderRadius: 20),
            ],
          ),
          SizedBox(height: 32),
          SkeletonLoader(height: 120, borderRadius: 16),
          SizedBox(height: 32),
          SkeletonLoader(height: 24, width: 150),
          SizedBox(height: 16),
          SkeletonLoader(height: 80, borderRadius: 16),
          SizedBox(height: 12),
          SkeletonLoader(height: 80, borderRadius: 16),
          SizedBox(height: 32),
          SkeletonLoader(height: 24, width: 150),
          SizedBox(height: 16),
          SkeletonLoader(height: 80, borderRadius: 16),
        ],
      ),
    ),
  );
}
