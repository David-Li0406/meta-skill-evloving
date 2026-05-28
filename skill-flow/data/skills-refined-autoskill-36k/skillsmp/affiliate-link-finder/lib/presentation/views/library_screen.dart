import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import '../theme/app_theme.dart';
import '../../utils/supplement_ui_helper.dart';
import '../widgets/unified_bottom_nav.dart';
import '../widgets/custom_supplement_form.dart';
import '../widgets/skeleton_loader.dart';
import '../view_models/library_view_model.dart';
import '../../config/locator.dart';
import '../../domain/entities/supplement.dart';
import '../../application/providers/auth_provider.dart';
import '../navigation/app_router.dart';

class LibraryScreen extends StatefulWidget {
  const LibraryScreen({super.key});

  @override
  State<LibraryScreen> createState() => _LibraryScreenState();
}

class _LibraryScreenState extends State<LibraryScreen> {
  late LibraryViewModel _viewModel;
  final TextEditingController _searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    final userId = authProvider.user?.id ?? 'demo_user';
    _viewModel = locator.get<LibraryViewModel>(param1: userId);
    _viewModel.initialize();

    _searchController.addListener(() {
      _viewModel.search(_searchController.text);
    });
  }

  @override
  void dispose() {
    _searchController.dispose();
    _viewModel.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    const primaryGold = AppColors.primaryGold;
    final bgColor =
        isDark ? AppColors.backgroundDark : AppColors.backgroundLight;

    return ChangeNotifierProvider.value(
      value: _viewModel,
      child: Scaffold(
        backgroundColor: bgColor,
        body: SafeArea(
          child: Consumer<LibraryViewModel>(
            builder: (context, viewModel, child) {
              return Column(
                children: [
                  // Header
                  Padding(
                    padding: const EdgeInsets.symmetric(
                        horizontal: 16, vertical: 12),
                    child: Row(
                      children: [
                        InkWell(
                          onTap: () => Navigator.pushReplacementNamed(
                              context, AppRouter.dashboard),
                          child: Container(
                            width: 50,
                            alignment: Alignment.centerLeft,
                            child: const Icon(
                                Icons
                                    .arrow_back, // Changed to arrow_back to match premium feel
                                size: 24,
                                color: AppColors.primaryGold),
                          ),
                        ),
                        Expanded(
                          child: Text(
                            'LIBRARY',
                            textAlign: TextAlign.center,
                            style: GoogleFonts.lexend(
                              fontWeight: FontWeight.bold,
                              fontSize: 16,
                              color:
                                  AppColors.primaryGold.withValues(alpha: 0.8),
                              letterSpacing: 2.0,
                            ),
                          ),
                        ),
                        Container(
                          width: 50,
                          alignment: Alignment.centerRight,
                          child: const Icon(Icons.bookmark_outline,
                              size: 24, color: AppColors.primaryGold),
                        ),
                      ],
                    ),
                  ),

                  // Loading State
                  if (viewModel.isLoading && viewModel.supplements.isEmpty)
                    Expanded(
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          children: [
                            const SkeletonLoader(
                                height: 52, borderRadius: 16), // Search bar
                            const SizedBox(height: 24),
                            Row(
                              children: List.generate(
                                  3,
                                  (index) => const Padding(
                                        padding: EdgeInsets.only(right: 8),
                                        child: SkeletonLoader(
                                            width: 80,
                                            height: 36,
                                            borderRadius: 18),
                                      )),
                            ),
                            const SizedBox(height: 32),
                            Expanded(
                              child: ListView.builder(
                                itemCount: 5,
                                itemBuilder: (context, index) => const Padding(
                                  padding: EdgeInsets.only(bottom: 12),
                                  child: SkeletonLoader(
                                      height: 80, borderRadius: 16),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    )
                  else ...[
                    // Selection Toggle (Recommended vs Avoid)
                    Padding(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 16, vertical: 8),
                      child: Container(
                        height: 48,
                        padding: const EdgeInsets.all(4),
                        decoration: BoxDecoration(
                          color: AppColors.cardBackground(isDark),
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(
                            color: AppColors.borderColor(isDark),
                          ),
                        ),
                        child: Row(
                          children: [
                            Expanded(
                              child: GestureDetector(
                                onTap: () =>
                                    viewModel.filterByStatus('beneficial'),
                                child: Container(
                                  decoration: BoxDecoration(
                                    color:
                                        viewModel.currentStatus == 'beneficial'
                                            ? (isDark
                                                ? const Color(0xFF2D3748)
                                                : Colors.white)
                                            : Colors.transparent,
                                    borderRadius: BorderRadius.circular(8),
                                    boxShadow:
                                        viewModel.currentStatus == 'beneficial'
                                            ? [
                                                BoxShadow(
                                                  color: Colors.black
                                                      .withValues(alpha: 0.05),
                                                  blurRadius: 4,
                                                  offset: const Offset(0, 2),
                                                )
                                              ]
                                            : null,
                                  ),
                                  alignment: Alignment.center,
                                  child: Text(
                                    'Recommended',
                                    style: GoogleFonts.lexend(
                                      fontSize: 13,
                                      fontWeight: viewModel.currentStatus ==
                                              'beneficial'
                                          ? FontWeight.bold
                                          : FontWeight.w500,
                                      color: viewModel.currentStatus ==
                                              'beneficial'
                                          ? (isDark
                                              ? Colors.white
                                              : const Color(0xFF0F172A))
                                          : Colors.grey,
                                    ),
                                  ),
                                ),
                              ),
                            ),
                            Expanded(
                              child: GestureDetector(
                                onTap: () => viewModel.filterByStatus('avoid'),
                                child: Container(
                                  decoration: BoxDecoration(
                                    color: viewModel.currentStatus == 'avoid'
                                        ? (isDark
                                            ? const Color(0xFF7F1D1D)
                                            : const Color(0xFFFEE2E2))
                                        : Colors.transparent,
                                    borderRadius: BorderRadius.circular(8),
                                    boxShadow:
                                        viewModel.currentStatus == 'avoid'
                                            ? [
                                                BoxShadow(
                                                  color: Colors.black
                                                      .withValues(alpha: 0.05),
                                                  blurRadius: 4,
                                                  offset: const Offset(0, 2),
                                                )
                                              ]
                                            : null,
                                  ),
                                  alignment: Alignment.center,
                                  child: Text(
                                    'Avoid List',
                                    style: GoogleFonts.lexend(
                                      fontSize: 13,
                                      fontWeight:
                                          viewModel.currentStatus == 'avoid'
                                              ? FontWeight.bold
                                              : FontWeight.w500,
                                      color: viewModel.currentStatus == 'avoid'
                                          ? (isDark
                                              ? Colors.white
                                              : const Color(0xFF991B1B))
                                          : Colors.grey,
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                    Expanded(
                      child: SingleChildScrollView(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            // Filter Chips: Categories
                            if (viewModel.categories.isNotEmpty) ...[
                              Padding(
                                padding: const EdgeInsets.symmetric(
                                    horizontal: 20, vertical: 4),
                                child: Text(
                                  'CATEGORIES',
                                  style: GoogleFonts.lexend(
                                    color: isDark
                                        ? const Color(0xFF64748B)
                                        : const Color(0xFF94A3B8),
                                    fontSize: 10,
                                    fontWeight: FontWeight.bold,
                                    letterSpacing: 1.5,
                                  ),
                                ),
                              ),
                              SingleChildScrollView(
                                scrollDirection: Axis.horizontal,
                                padding: const EdgeInsets.symmetric(
                                    horizontal: 16, vertical: 8),
                                child: Row(
                                  children: [
                                    _buildFilterChip(
                                      context,
                                      Icons.all_inclusive,
                                      'All',
                                      viewModel.selectedCategory == null,
                                      primaryGold,
                                      () => viewModel.filterByCategory(null),
                                    ),
                                    const SizedBox(width: 8),
                                    ...viewModel.categories.map((category) {
                                      return Padding(
                                        padding:
                                            const EdgeInsets.only(right: 8),
                                        child: _buildFilterChip(
                                          context,
                                          SupplementUIHelper.getIconForCategory(
                                              category),
                                          category,
                                          viewModel.selectedCategory ==
                                              category,
                                          primaryGold,
                                          () => viewModel
                                              .filterByCategory(category),
                                        ),
                                      );
                                    }),
                                  ],
                                ),
                              ),
                            ],

                            // Search Bar
                            Padding(
                              padding: const EdgeInsets.symmetric(
                                  horizontal: 16, vertical: 8),
                              child: Row(
                                children: [
                                  Expanded(
                                    child: Container(
                                      height: 52,
                                      decoration: BoxDecoration(
                                        color: AppColors.cardBackground(isDark),
                                        borderRadius: BorderRadius.circular(16),
                                        border: Border.all(
                                          color: AppColors.borderColor(isDark),
                                        ),
                                        boxShadow: [
                                          BoxShadow(
                                            color: Colors.black
                                                .withValues(alpha: 0.05),
                                            blurRadius: 10,
                                            offset: const Offset(0, 4),
                                          ),
                                        ],
                                      ),
                                      child: Row(
                                        children: [
                                          const Padding(
                                            padding: EdgeInsets.only(
                                                left: 16, right: 8),
                                            child: Icon(Icons.search,
                                                color: Color(0xFF9DA8B9)),
                                          ),
                                          Expanded(
                                            child: TextField(
                                              controller: _searchController,
                                              decoration: const InputDecoration(
                                                hintText:
                                                    'Search supplements...',
                                                hintStyle: TextStyle(
                                                    color: Color(0xFF9DA8B9),
                                                    fontSize: 15),
                                                border: InputBorder.none,
                                                isDense: true,
                                              ),
                                              style: GoogleFonts.lexend(
                                                color: isDark
                                                    ? Colors.white
                                                    : AppColors
                                                        .textPrimaryLight,
                                              ),
                                            ),
                                          ),
                                          if (_searchController.text.isNotEmpty)
                                            IconButton(
                                              icon: const Icon(Icons.clear,
                                                  color: Color(0xFF9DA8B9)),
                                              onPressed: () {
                                                _searchController.clear();
                                                viewModel.clearFilters();
                                              },
                                            ),
                                          Padding(
                                            padding:
                                                const EdgeInsets.only(right: 8),
                                            child: IconButton(
                                              icon: const Icon(Icons.tune,
                                                  color: AppColors.primaryGold),
                                              onPressed: () =>
                                                  _showFiltersDrawer(context),
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            ),

                            // Section Header
                            Padding(
                              padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
                              child: Row(
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceBetween,
                                children: [
                                  Text(
                                    viewModel.currentStatus == 'avoid'
                                        ? 'Substances to Avoid'
                                        : (viewModel.selectedCategory ??
                                            'All Supplements'),
                                    style: GoogleFonts.lexend(
                                      fontWeight: FontWeight.bold,
                                      fontSize: 18,
                                      color: isDark
                                          ? Colors.white
                                          : const Color(0xFF0F172A),
                                    ),
                                  ),
                                  Text(
                                    'Showing ${viewModel.supplements.length} items',
                                    style: GoogleFonts.lexend(
                                      color: isDark
                                          ? const Color(0xFF64748B)
                                          : const Color(0xFF94A3B8),
                                      fontSize: 11,
                                      fontWeight: FontWeight.w500,
                                    ),
                                  ),
                                ],
                              ),
                            ),

                            // Supplement Cards
                            if (viewModel.supplements.isEmpty)
                              Padding(
                                padding: const EdgeInsets.all(32),
                                child: Center(
                                  child: Column(
                                    children: [
                                      const Icon(Icons.search_off,
                                          size: 48, color: Colors.grey),
                                      const SizedBox(height: 16),
                                      Text(
                                        'No supplements found',
                                        style: GoogleFonts.lexend(
                                            color:
                                                AppColors.textTertiary(isDark),
                                            fontSize: 16),
                                      ),
                                    ],
                                  ),
                                ),
                              )
                            else
                              Padding(
                                padding:
                                    const EdgeInsets.symmetric(horizontal: 16),
                                child: Column(
                                  children:
                                      viewModel.supplements.map((supplement) {
                                    return Padding(
                                      padding: const EdgeInsets.only(
                                          bottom: 8), // Reduced spacing
                                      child: _buildSupplementCard(
                                        context,
                                        supplement: supplement,
                                        isDark: isDark,
                                      ),
                                    );
                                  }).toList(),
                                ),
                              ),
                            const SizedBox(height: 80),
                          ],
                        ),
                      ),
                    ),
                  ],
                ],
              );
            },
          ),
        ),
        bottomNavigationBar: const UnifiedBottomNav(currentIndex: 2),
        floatingActionButton: FloatingActionButton(
          onPressed: () => _showCustomSupplementForm(context),
          backgroundColor: AppColors.primaryGold,
          foregroundColor: Colors.black,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
          ),
          child: const Icon(Icons.add_task),
        ),
      ),
    );
  }

  void _showCustomSupplementForm(BuildContext context) {
    showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => CustomSupplementForm(
        onSave: (name, category, dosage, timeOfDay, benefits) async {
          final messenger = ScaffoldMessenger.of(context);
          try {
            await _viewModel.createCustomSupplement(
              name: name,
              category: category,
              dosage: dosage,
              timeOfDay: timeOfDay,
              benefits: benefits,
            );
            messenger.showSnackBar(
              const SnackBar(content: Text('Custom supplement created!')),
            );
          } catch (e) {
            messenger.showSnackBar(
              SnackBar(content: Text('Failed to create: $e')),
            );
          }
        },
      ),
    );
  }

  void _showAddToStackSheet(BuildContext context, Supplement supplement) {
    final viewModel =
        context.read<LibraryViewModel>(); // Capture VM from parent context
    final isDark = Theme.of(context).brightness == Brightness.dark;
    showModalBottomSheet<void>(
      context: context,
      backgroundColor: Colors.transparent,
      builder: (sheetContext) => Container(
        decoration: BoxDecoration(
          color: AppColors.cardBackground(isDark),
          borderRadius: const BorderRadius.vertical(top: Radius.circular(20)),
        ),
        padding: const EdgeInsets.all(24),
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Add to Stack',
                style: GoogleFonts.lexend(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: isDark ? Colors.white : const Color(0xFF0F172A),
                ),
              ),
              const SizedBox(height: 8),
              Text(
                'Select which stack to add ${supplement.name}',
                style: GoogleFonts.lexend(
                  fontSize: 14,
                  color: isDark ? Colors.grey[400] : Colors.grey[600],
                ),
              ),
              const SizedBox(height: 24),
              _buildStackOption(
                context,
                '🌅 Morning Stack',
                'Best for focus and energy',
                () {
                  Navigator.pop(context);
                  final messenger = ScaffoldMessenger.of(context);
                  messenger.showSnackBar(
                    SnackBar(
                      backgroundColor: AppColors.primaryGold,
                      content: Text('Added ${supplement.name} to Morning Stack',
                          style: const TextStyle(color: Colors.black)),
                    ),
                  );
                  viewModel
                      .addToStack(supplement, 'Morning Stack')
                      .catchError((Object e) {
                    messenger.showSnackBar(
                      SnackBar(content: Text('Error syncing: $e')),
                    );
                  });
                },
              ),
              const SizedBox(height: 12),
              _buildStackOption(
                context,
                '☀️ Afternoon Stack',
                'Sustained focus and energy',
                () {
                  Navigator.pop(context);
                  final messenger = ScaffoldMessenger.of(context);
                  messenger.showSnackBar(
                    SnackBar(
                      backgroundColor: AppColors.primaryGold,
                      content: Text(
                          'Added ${supplement.name} to Afternoon Stack',
                          style: const TextStyle(color: Colors.black)),
                    ),
                  );
                  viewModel
                      .addToStack(supplement, 'Afternoon Stack')
                      .catchError((Object e) {
                    messenger.showSnackBar(
                      SnackBar(content: Text('Error syncing: $e')),
                    );
                  });
                },
              ),
              const SizedBox(height: 12),
              _buildStackOption(
                context,
                '🌇 Evening Stack',
                'For relaxation and recovery',
                () {
                  Navigator.pop(context);
                  final messenger = ScaffoldMessenger.of(context);
                  messenger.showSnackBar(
                    SnackBar(
                      backgroundColor: AppColors.primaryGold,
                      content: Text('Added ${supplement.name} to Evening Stack',
                          style: const TextStyle(color: Colors.black)),
                    ),
                  );
                  viewModel
                      .addToStack(supplement, 'Evening Stack')
                      .catchError((Object e) {
                    messenger.showSnackBar(
                      SnackBar(content: Text('Error syncing: $e')),
                    );
                  });
                },
              ),
              const SizedBox(height: 12),
              _buildStackOption(
                context,
                '🌙 Night Stack',
                'Sleep support',
                () {
                  Navigator.pop(context);
                  final messenger = ScaffoldMessenger.of(context);
                  messenger.showSnackBar(
                    SnackBar(
                      backgroundColor: AppColors.primaryGold,
                      content: Text('Added ${supplement.name} to Night Stack',
                          style: const TextStyle(color: Colors.black)),
                    ),
                  );
                  viewModel
                      .addToStack(supplement, 'Night Stack')
                      .catchError((Object e) {
                    messenger.showSnackBar(
                      SnackBar(content: Text('Error syncing: $e')),
                    );
                  });
                },
              ),
              const SizedBox(height: 24),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildStackOption(
    BuildContext context,
    String title,
    String description,
    VoidCallback onTap,
  ) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          border: Border.all(
            color: isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0),
          ),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: GoogleFonts.lexend(
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                      color: isDark ? Colors.white : const Color(0xFF0F172A),
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    description,
                    style: GoogleFonts.lexend(
                      fontSize: 13,
                      color: isDark ? Colors.grey[400] : Colors.grey[600],
                    ),
                  ),
                ],
              ),
            ),
            const Icon(Icons.arrow_forward_ios, size: 16),
          ],
        ),
      ),
    );
  }

  Widget _buildFilterChip(
    BuildContext context,
    IconData icon,
    String label,
    bool isSelected,
    Color primary,
    VoidCallback onTap,
  ) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final bgSelected = primary;
    final bgUnselected = isDark ? const Color(0xFF1C2633) : Colors.white;
    const textSelected = Colors.white;
    final textUnselected =
        isDark ? const Color(0xFFcbd5e1) : const Color(0xFF475569);
    final borderUnselected =
        isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0);

    return GestureDetector(
      onTap: onTap,
      child: Container(
        height: 36,
        padding: const EdgeInsets.symmetric(horizontal: 16),
        decoration: BoxDecoration(
          color: isSelected ? bgSelected : bgUnselected,
          borderRadius: BorderRadius.circular(999),
          border: isSelected ? null : Border.all(color: borderUnselected),
          boxShadow: isSelected
              ? [
                  BoxShadow(
                      color: primary.withValues(alpha: 0.3),
                      blurRadius: 4,
                      offset: const Offset(0, 2))
                ]
              : null,
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon,
                size: 18, color: isSelected ? textSelected : textUnselected),
            const SizedBox(width: 8),
            Text(
              label,
              style: GoogleFonts.lexend(
                color: isSelected ? textSelected : textUnselected,
                fontSize: 12,
                fontWeight: isSelected ? FontWeight.w600 : FontWeight.w500,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSupplementCard(
    BuildContext context, {
    required Supplement supplement,
    required bool isDark,
  }) {
    final isGold = supplement.evidenceLevel?.toLowerCase() == 'high';

    return InkWell(
      onTap: () => Navigator.pushNamed(context, AppRouter.supplementDetail,
          arguments: supplement),
      borderRadius: BorderRadius.circular(16),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        decoration: BoxDecoration(
          color: AppColors.cardBackground(isDark),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(
            color: supplement.status == 'avoid'
                ? (isDark
                    ? const Color(0xFF7F1D1D).withValues(alpha: 0.5)
                    : const Color(0xFFFCA5A5))
                : (isGold
                    ? AppColors.primaryGold.withValues(alpha: 0.3)
                    : AppColors.primaryGold.withValues(alpha: 0.05)),
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.03),
              blurRadius: 10,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: Row(
          children: [
            // Small Leading Illustration
            _buildPillIllustration(supplement, isSmall: true),
            const SizedBox(width: 16),

            // Name and Category
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Row(
                    children: [
                      Flexible(
                        child: Text(
                          supplement.name,
                          overflow: TextOverflow.ellipsis,
                          style: GoogleFonts.lexend(
                            fontWeight: FontWeight.bold,
                            fontSize: 14,
                            color:
                                isDark ? Colors.white : const Color(0xFF0F172A),
                          ),
                        ),
                      ),
                      if (isGold) ...[
                        const SizedBox(width: 6),
                        const Icon(Icons.verified,
                            color: AppColors.primaryGold, size: 14),
                      ],
                      if (supplement.isCustom) ...[
                        const SizedBox(width: 6),
                        Container(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 6, vertical: 2),
                          decoration: BoxDecoration(
                            color: AppColors.primaryGold.withValues(alpha: 0.1),
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: Text(
                            'CUSTOM',
                            style: GoogleFonts.lexend(
                              fontSize: 8,
                              fontWeight: FontWeight.bold,
                              color: AppColors.primaryGold,
                            ),
                          ),
                        ),
                      ],
                    ],
                  ),
                  Text(
                    supplement.category,
                    overflow: TextOverflow.ellipsis,
                    maxLines: 1,
                    style: GoogleFonts.lexend(
                      fontSize: 11,
                      color: isDark ? Colors.grey[400] : Colors.grey[500],
                    ),
                  ),
                ],
              ),
            ),

            // Delete button for custom items
            if (supplement.isCustom)
              IconButton(
                icon: const Icon(Icons.delete_outline,
                    size: 18, color: Colors.grey),
                onPressed: () async {
                  final messenger = ScaffoldMessenger.of(context);
                  try {
                    await _viewModel.deleteCustomSupplement(supplement.id);
                    messenger.showSnackBar(
                      const SnackBar(content: Text('Supplement deleted')),
                    );
                  } catch (e) {
                    messenger.showSnackBar(
                      SnackBar(content: Text('Delete failed: $e')),
                    );
                  }
                },
              ),

            // Focus Level (Stars)
            if (supplement.status != 'avoid')
              Row(
                children: List.generate(
                  5,
                  (index) => Icon(
                    index < supplement.focusLevel
                        ? Icons.star
                        : Icons.star_border,
                    color: AppColors.primaryGold,
                    size: 10, // Slightly smaller to fit 5 stars
                  ),
                ),
              )
            else
              const Icon(Icons.warning_amber_rounded,
                  color: Color(0xFFEF4444), size: 16),
            const SizedBox(width: 12),

            // Action Button
            SizedBox(
              height: 32,
              child: ElevatedButton(
                onPressed: supplement.status == 'avoid'
                    ? () => Navigator.pushNamed(
                        context, AppRouter.supplementDetail,
                        arguments: supplement)
                    : () => _showAddToStackSheet(context, supplement),
                style: ElevatedButton.styleFrom(
                  backgroundColor: supplement.status == 'avoid'
                      ? (isDark
                          ? const Color(0xFF991B1B)
                          : const Color(0xFFFEE2E2))
                      : AppColors.primaryGold,
                  foregroundColor: supplement.status == 'avoid'
                      ? (isDark ? Colors.white : const Color(0xFF991B1B))
                      : Colors.white,
                  elevation: 0,
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8)),
                ),
                child: Text(
                  supplement.status == 'avoid' ? 'WHY?' : 'ADD',
                  style: GoogleFonts.lexend(
                      fontWeight: FontWeight.bold, fontSize: 11),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPillIllustration(Supplement supplement, {bool isSmall = false}) {
    final color = Color(int.parse(
        (supplement.colorHex ?? '#D4A411').replaceFirst('#', '0xFF')));
    final isCapsule = supplement.shapeIcon == 'capsule';

    return Container(
      width: isSmall ? 32 : 40,
      height: isSmall ? 32 : 60,
      decoration: BoxDecoration(
        color: supplement.status == 'avoid'
            ? const Color(0xFFEF4444).withValues(alpha: 0.1)
            : color.withValues(alpha: 0.8),
        borderRadius: BorderRadius.circular(isCapsule && !isSmall ? 20 : 8),
        boxShadow: [
          BoxShadow(
            color: supplement.status == 'avoid'
                ? const Color(0xFFEF4444).withValues(alpha: 0.1)
                : color.withValues(alpha: 0.2),
            blurRadius: isSmall ? 5 : 15,
            spreadRadius: isSmall ? 1 : 2,
          ),
        ],
      ),
      child: Center(
        child: Icon(
          supplement.status == 'avoid'
              ? Icons.block
              : (isCapsule ? Icons.wb_sunny_outlined : Icons.track_changes),
          color: supplement.status == 'avoid'
              ? const Color(0xFFEF4444)
              : Colors.white70,
          size: isSmall ? 14 : 20,
        ),
      ),
    );
  }

  void _showFiltersDrawer(BuildContext context) {
    final viewModel = context.read<LibraryViewModel>();
    final isDark = Theme.of(context).brightness == Brightness.dark;

    showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => Container(
        height: MediaQuery.of(context).size.height * 0.75,
        decoration: BoxDecoration(
          color: isDark ? AppColors.backgroundDark : Colors.white,
          borderRadius: const BorderRadius.vertical(top: Radius.circular(32)),
        ),
        child: Column(
          children: [
            const SizedBox(height: 12),
            Container(
              width: 40,
              height: 4,
              decoration: BoxDecoration(
                color: Colors.grey[300],
                borderRadius: BorderRadius.circular(2),
              ),
            ),
            Expanded(
              child: ListView(
                padding: const EdgeInsets.all(24),
                children: [
                  Text(
                    'Advanced Filters',
                    style: GoogleFonts.lexend(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 32),
                  _buildFilterSection(
                    'Evidence Strength',
                    ['High', 'Moderate', 'Low'],
                    viewModel.evidenceStrength,
                    (val) => viewModel.filterByEvidence(val),
                    isDark,
                  ),
                  const SizedBox(height: 24),
                  _buildFilterSection(
                    'Stimulant Compatible',
                    ['Safe', 'Caution'],
                    viewModel.stimulantCompatible == null
                        ? null
                        : (viewModel.stimulantCompatible! ? 'Safe' : 'Caution'),
                    (val) => viewModel.filterByStimulant(val == 'Safe'),
                    isDark,
                  ),
                  const SizedBox(height: 24),
                  _buildFilterSection(
                    'Form',
                    ['Capsule', 'Tablet', 'Liquid', 'Powder'],
                    viewModel.form,
                    (val) => viewModel.filterByForm(val),
                    isDark,
                  ),
                  const SizedBox(height: 40),
                  Row(
                    children: [
                      Expanded(
                        child: TextButton(
                          onPressed: () {
                            viewModel.clearFilters();
                            Navigator.pop(context);
                          },
                          child: Text(
                            'Clear All',
                            style: GoogleFonts.lexend(
                              color: Colors.grey,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ),
                      Expanded(
                        child: ElevatedButton(
                          onPressed: () => Navigator.pop(context),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: AppColors.primaryGold,
                            foregroundColor: Colors.black,
                            padding: const EdgeInsets.symmetric(vertical: 16),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(16),
                            ),
                          ),
                          child: Text(
                            'Show Results',
                            style:
                                GoogleFonts.lexend(fontWeight: FontWeight.bold),
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFilterSection(
    String title,
    List<String> options,
    String? selectedValue,
    void Function(String) onSelect,
    bool isDark,
  ) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title.toUpperCase(),
          style: GoogleFonts.lexend(
            fontSize: 10,
            fontWeight: FontWeight.bold,
            letterSpacing: 1.5,
            color: AppColors.primaryGold.withValues(alpha: 0.7),
          ),
        ),
        const SizedBox(height: 12),
        Wrap(
          spacing: 10,
          runSpacing: 10,
          children: options.map((option) {
            final isSelected =
                selectedValue?.toLowerCase() == option.toLowerCase();
            return GestureDetector(
              onTap: () => onSelect(option),
              child: Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                decoration: BoxDecoration(
                  color: isSelected
                      ? AppColors.primaryGold
                      : (isDark ? Colors.white12 : Colors.grey[100]),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(
                    color: isSelected
                        ? AppColors.primaryGold
                        : (isDark ? Colors.white24 : Colors.grey[300]!),
                  ),
                ),
                child: Text(
                  option,
                  style: GoogleFonts.lexend(
                    fontSize: 13,
                    fontWeight: isSelected ? FontWeight.bold : FontWeight.w500,
                    color: isSelected
                        ? Colors.black
                        : (isDark ? Colors.white70 : Colors.grey[700]),
                  ),
                ),
              ),
            );
          }).toList(),
        ),
      ],
    );
  }
}
