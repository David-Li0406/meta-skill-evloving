import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../application/providers/auth_provider.dart';
import '../../application/view_models/history_log_view_model.dart';
import '../../domain/entities/daily_log.dart';
import '../navigation/app_router.dart';
import '../../presentation/theme/app_theme.dart';

class HistoryLogScreen extends StatefulWidget {
  const HistoryLogScreen({super.key});

  static Widget withProvider() {
    return Consumer<AuthProvider>(
      builder: (context, auth, _) => ChangeNotifierProvider(
        create: (_) =>
            HistoryLogViewModel.withParams(auth.user?.id ?? '')..fetchHistory(),
        child: const HistoryLogScreen(),
      ),
    );
  }

  @override
  State<HistoryLogScreen> createState() => _HistoryLogScreenState();
}

class _HistoryLogScreenState extends State<HistoryLogScreen> {
  String _selectedFilter = 'All';

  @override
  Widget build(BuildContext context) {
    const bgLight = Color(0xFFF5F8F6);
    const bgDark = Color(0xFF102216);
    const primaryGreen = Color(0xFF0DF259);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      backgroundColor: isDark ? bgDark : bgLight,
      appBar: AppBar(
        title: const Text('History',
            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
        centerTitle: true,
        backgroundColor: isDark
            ? bgDark.withValues(alpha: 0.9)
            : bgLight.withValues(alpha: 0.9),
        foregroundColor: isDark ? Colors.white : const Color(0xFF111418),
        elevation: 0,
        leading: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Container(
            decoration: BoxDecoration(
              color: isDark
                  ? Colors.white.withValues(alpha: 0.05)
                  : Colors.black.withValues(alpha: 0.05),
              shape: BoxShape.circle,
            ),
            child: IconButton(
              icon: const Icon(Icons.arrow_back_ios_new, size: 18),
              onPressed: () => Navigator.pop(context),
            ),
          ),
        ),
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 16),
            child: TextButton(
              onPressed: () {
                final viewModel =
                    Provider.of<HistoryLogViewModel>(context, listen: false);
                // Show confirmation dialog before resolving all
                showDialog<void>(
                  context: context,
                  builder: (ctx) => AlertDialog(
                    title: const Text('Resolve All?'),
                    content: const Text(
                      'This will mark all missed reminders as acknowledged. You can still view them in your history.',
                    ),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(ctx),
                        child: const Text('Cancel'),
                      ),
                      TextButton(
                        onPressed: () async {
                          Navigator.pop(ctx);
                          await viewModel.resolveAllMissed();
                          if (!context.mounted) return;
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(
                              content: Text('All items resolved'),
                              backgroundColor: AppColors.primaryGold,
                            ),
                          );
                        },
                        child: const Text('Resolve'),
                      ),
                    ],
                  ),
                );
              },
              style: TextButton.styleFrom(
                backgroundColor: AppColors.primaryGold.withValues(alpha: 0.2),
                foregroundColor: AppColors.primaryGold,
                padding:
                    const EdgeInsets.symmetric(horizontal: 16, vertical: 0),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(20),
                ),
              ),
              child: const Text('Resolve All',
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
            ),
          ),
        ],
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(60),
          child: SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.fromLTRB(16, 0, 16, 12),
            child: Row(
              children: [
                _buildFilterChip('All',
                    isSelected: _selectedFilter == 'All',
                    primaryGreen: primaryGreen,
                    isDark: isDark),
                const SizedBox(width: 8),
                _buildFilterChip('Missed',
                    isSelected: _selectedFilter == 'Missed',
                    primaryGreen: primaryGreen,
                    isDark: isDark),
                const SizedBox(width: 8),
                _buildFilterChip('Taken',
                    isSelected: _selectedFilter == 'Taken',
                    primaryGreen: primaryGreen,
                    isDark: isDark),
                const SizedBox(width: 8),
                _buildFilterChip('Dismissed',
                    isSelected: _selectedFilter == 'Dismissed',
                    primaryGreen: primaryGreen,
                    isDark: isDark),
              ],
            ),
          ),
        ),
      ),
      body: Stack(
        children: [
          Consumer<HistoryLogViewModel>(
            builder: (context, viewModel, child) {
              if (viewModel.isLoading) {
                return const Center(child: CircularProgressIndicator());
              }

              if (viewModel.recentLogs.isEmpty && viewModel.error == null) {
                return Center(
                  child: Text(
                    'No history yet',
                    style: TextStyle(
                      color: isDark ? Colors.grey[400] : Colors.grey[600],
                      fontSize: 16,
                    ),
                  ),
                );
              }

              // Group logs by day (Today, Yesterday, etc.)
              final today = DateTime.now();
              final yesterday = today.subtract(const Duration(days: 1));

              return SingleChildScrollView(
                padding: const EdgeInsets.fromLTRB(16, 16, 16, 100),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    if (viewModel.error != null)
                      Padding(
                        padding: const EdgeInsets.only(bottom: 16),
                        child: Text(
                          viewModel.error!,
                          style: const TextStyle(color: Colors.red),
                        ),
                      ),
                    ...viewModel.recentLogs.map((log) {
                      final isToday = log.date.year == today.year &&
                          log.date.month == today.month &&
                          log.date.day == today.day;
                      final isYesterday = log.date.year == yesterday.year &&
                          log.date.month == yesterday.month &&
                          log.date.day == yesterday.day;

                      String header = isToday
                          ? 'Today'
                          : (isYesterday
                              ? 'Yesterday'
                              : '${log.date.month}/${log.date.day}');

                      if (log.entries.isEmpty) return const SizedBox.shrink();

                      return Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const SizedBox(height: 8),
                          Text(
                            header,
                            style: const TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(height: 16),
                          ...log.entries.asMap().entries.map((entry) {
                            final index = entry.key;
                            final item = entry.value;
                            final isLast = index == log.entries.length - 1;

                            // Map LogStatus to internal _LogStatus enum if needed,
                            // or verify they match. _LogStatus is local to this file.
                            _LogStatus status;
                            switch (item.status) {
                              case LogStatus.taken:
                                status = _LogStatus.taken;
                                break;
                              case LogStatus.skipped:
                                status =
                                    _LogStatus.missed; // or dismissed/skipped
                                break;
                              case LogStatus.late:
                                status = _LogStatus
                                    .taken; // Treated as taken but late
                                break;
                            }
                            // If status is 'late', we can append to title or handling
                            String title =
                                'Supplement Log'; // Ideally fetched from Supplement ID
                            // Since LogEntry only has ID, we might need a way to look up name
                            // For now, we'll display the ID or generic text until we fetch Supplement details
                            // Optimization: ViewModel should probably join this data or we just show simplified view
                            title = 'Supplement Check-in';

                            return _buildTimelineItem(
                              status: status,
                              title:
                                  title, // Placeholder: Needs Supplement Name lookup
                              time:
                                  '${item.takenAt.hour}:${item.takenAt.minute.toString().padLeft(2, '0')}',
                              primaryGreen: primaryGreen,
                              isDark: isDark,
                              isFirst: index == 0,
                              isLastGroup: isLast,
                              // Add action button logic if needed for 'missed' items
                            );
                          }),
                          const SizedBox(height: 24),
                          Divider(
                              color: isDark
                                  ? Colors.white.withValues(alpha: 0.1)
                                  : Colors.grey[200]),
                          const SizedBox(height: 16),
                        ],
                      );
                    }),
                  ],
                ),
              );
            },
          ),

          // Custom Floating Bottom Bar
          Positioned(
            bottom: 24,
            left: 0,
            right: 0,
            child: Center(
              child: Container(
                margin: const EdgeInsets.symmetric(horizontal: 24),
                decoration: BoxDecoration(
                  color:
                      isDark ? bgDark.withValues(alpha: 0.9) : Colors.black87,
                  borderRadius: BorderRadius.circular(32),
                  border:
                      Border.all(color: Colors.white.withValues(alpha: 0.15)),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withValues(alpha: 0.3),
                      blurRadius: 20,
                      offset: const Offset(0, 10),
                    ),
                  ],
                ),
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    _buildNavButton(
                        Icons.home_filled,
                        false,
                        primaryGreen,
                        () => Navigator.pushNamedAndRemoveUntil(
                            context, AppRouter.dashboard, (route) => false)),
                    const SizedBox(width: 8),
                    _buildNavButton(Icons.history, true, primaryGreen, () {}),
                    const SizedBox(width: 8),
                    _buildNavButton(
                        Icons.leaderboard,
                        false,
                        primaryGreen,
                        () =>
                            Navigator.pushNamed(context, AppRouter.trophyRoom)),
                    const SizedBox(width: 8),
                    _buildNavButton(Icons.settings, false, primaryGreen,
                        () => Navigator.pushNamed(context, AppRouter.profile)),
                  ],
                ),
              ),
            ),
          )
        ],
      ),
    );
  }

  Widget _buildNavButton(
      IconData icon, bool isActive, Color primary, VoidCallback onTap) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 44,
        height: 44,
        decoration: BoxDecoration(
          color: isActive ? primary : Colors.white.withValues(alpha: 0.1),
          shape: BoxShape.circle,
        ),
        child: Icon(
          icon,
          color: isActive ? Colors.black : Colors.white,
          size: 22,
        ),
      ),
    );
  }

  Widget _buildFilterChip(String label,
      {required bool isSelected,
      required Color primaryGreen,
      required bool isDark}) {
    return GestureDetector(
      onTap: () => setState(() => _selectedFilter = label),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
        decoration: BoxDecoration(
          color: isSelected
              ? primaryGreen
              : (isDark
                  ? Colors.white.withValues(alpha: 0.1)
                  : Colors.grey[200]),
          borderRadius: BorderRadius.circular(20),
        ),
        child: Text(
          label,
          style: TextStyle(
            color: isSelected
                ? const Color(0xFF102216)
                : (isDark ? Colors.white : Colors.black87),
            fontWeight: FontWeight.bold,
            fontSize: 14,
          ),
        ),
      ),
    );
  }

  Widget _buildTimelineItem({
    required _LogStatus status,
    required String title,
    required String time,
    required Color primaryGreen,
    required bool isDark,
    bool isFirst = false,
    bool isLastGroup = false,
    Widget? actionButton,
    bool isFaded = false,
  }) {
    Color iconBg;
    Color iconColor;
    IconData icon;

    switch (status) {
      case _LogStatus.taken:
        iconBg = primaryGreen.withValues(alpha: 0.2);
        iconColor = primaryGreen;
        icon = Icons.check_circle;
        break;
      case _LogStatus.missed:
        iconBg = Colors.red.withValues(alpha: 0.2);
        iconColor = Colors.red.shade400;
        icon = Icons.cancel;
        break;
      case _LogStatus.active:
        iconBg = Colors.blue.withValues(alpha: 0.2);
        iconColor = Colors.blue.shade400;
        icon = Icons.notifications_active;
        break;
      case _LogStatus.dismissed:
        iconBg = isDark
            ? Colors.white.withValues(alpha: 0.2)
            : Colors.grey.withValues(alpha: 0.3);
        iconColor =
            isDark ? Colors.white.withValues(alpha: 0.5) : Colors.grey.shade600;
        icon = Icons.visibility_off;
        break;
    }

    return IntrinsicHeight(
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Timeline logic
          SizedBox(
            width: 48,
            child: Column(
              children: [
                if (!isFirst)
                  Container(
                      width: 2,
                      height: 12,
                      color: primaryGreen.withValues(
                          alpha: 0.3)), // Connector from top
                Container(
                  width: 32,
                  height: 32,
                  decoration: BoxDecoration(
                    color: iconBg,
                    shape: BoxShape.circle,
                  ),
                  child: Icon(icon, size: 18, color: iconColor),
                ),
                if (!isLastGroup)
                  Expanded(
                      child: Container(
                          width: 2,
                          color: isDark
                              ? Colors.white.withValues(alpha: 0.1)
                              : Colors.grey[300])),
              ],
            ),
          ),
          const SizedBox(width: 8),

          Expanded(
            child: Opacity(
              opacity: isFaded ? 0.6 : 1.0,
              child: Container(
                margin: const EdgeInsets.only(bottom: 16),
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: isDark
                      ? Colors.white.withValues(alpha: 0.05)
                      : Colors.white,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(
                      color: isDark
                          ? Colors.white.withValues(alpha: 0.05)
                          : Colors.grey[200]!),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          title,
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 16,
                            color: isDark ? Colors.white : Colors.black87,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Row(
                          children: [
                            Text(
                              time,
                              style: TextStyle(
                                color: isDark
                                    ? Colors.white.withValues(alpha: 0.5)
                                    : Colors.black54,
                                fontSize: 12,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            Text(
                              ' • ${status.name.toUpperCase()}',
                              style: TextStyle(
                                color: status == _LogStatus.missed
                                    ? Colors.red.shade400
                                    : (status == _LogStatus.active
                                        ? Colors.blue.shade400
                                        : (status == _LogStatus.taken
                                            ? primaryGreen
                                            : Colors.grey)),
                                fontSize: 12,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                    if (actionButton != null)
                      actionButton
                    else
                      Icon(Icons.more_vert,
                          color: isDark
                              ? Colors.white.withValues(alpha: 0.3)
                              : Colors.black26),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

enum _LogStatus { taken, missed, active, dismissed }
