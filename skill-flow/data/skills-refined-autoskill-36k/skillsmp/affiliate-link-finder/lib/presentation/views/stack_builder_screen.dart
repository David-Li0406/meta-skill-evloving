import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/app_theme.dart';
import '../widgets/stack_drop_zone.dart';
import '../widgets/library_item.dart';
import '../widgets/safety_alert_banner.dart';
import '../../application/view_models/safety_view_model.dart';
import '../navigation/app_router.dart';
import '../widgets/stack_presets_modal.dart';
import '../../utils/supplement_ui_helper.dart';
import '../view_models/stack_builder_view_model.dart';

class StackBuilderScreen extends StatefulWidget {
  const StackBuilderScreen({super.key});

  @override
  State<StackBuilderScreen> createState() => _StackBuilderScreenState();
}

class _StackBuilderScreenState extends State<StackBuilderScreen> {
  // Helper to map supplements to library items
  List<LibraryItemData> _getLibraryItemData(StackBuilderViewModel viewModel) {
    return viewModel.availableSupplements.map((s) {
      return LibraryItemData(
        id: s.id,
        name: s.name,
        dosage: s.defaultDosage ?? '',
        icon: SupplementUIHelper.getIconForCategory(s.category),
        iconColor: SupplementUIHelper.getColorForCategory(s.category),
        iconBgColor: SupplementUIHelper.getColorForCategory(s.category)
            .withValues(alpha: 0.1),
      );
    }).toList();
  }

  // Helper to map stack items to library items for the drop zone
  List<LibraryItemData> _getCurrentStackData(StackBuilderViewModel viewModel) {
    if (viewModel.currentStack == null) return [];

    return viewModel.currentStack!.items.map((item) {
      final s = viewModel.availableSupplements.firstWhere(
        (supp) => supp.id == item.supplementId,
        orElse: () =>
            throw Exception('Supplement not found for ${item.supplementId}'),
      );

      return LibraryItemData(
        id: s.id,
        name: s.name,
        dosage: item.customDosage ?? s.defaultDosage ?? '',
        icon: SupplementUIHelper.getIconForCategory(s.category),
        iconColor: SupplementUIHelper.getColorForCategory(s.category),
        iconBgColor: SupplementUIHelper.getColorForCategory(s.category)
            .withValues(alpha: 0.1),
      );
    }).toList();
  }

  Future<void> _handleSave(StackBuilderViewModel viewModel) async {
    final success = await viewModel.saveStack();
    if (mounted) {
      if (success) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Routine optimization active! 🎉'),
            backgroundColor: AppColors.primary,
          ),
        );
        Navigator.pop(context);
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(viewModel.error ?? 'Error saving stack'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  void _handleItemDropped(
      StackBuilderViewModel viewModel, String supplementId) {
    final supplement = viewModel.availableSupplements.firstWhere(
      (s) => s.id == supplementId,
    );
    viewModel.addItem(supplement);
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final bgColor =
        isDark ? AppColors.backgroundDark : AppColors.backgroundLight;
    final safetyViewModel = context.watch<SafetyViewModel>();
    final viewModel = context.watch<StackBuilderViewModel>();

    final libraryItems = _getLibraryItemData(viewModel);
    final currentStackData = _getCurrentStackData(viewModel);

    return Scaffold(
      backgroundColor: bgColor,
      body: SafeArea(
        child: viewModel.isLoading
            ? const Center(child: CircularProgressIndicator())
            : Stack(
                children: [
                  Column(
                    children: [
                      // Top App Bar
                      Padding(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 16, vertical: 12),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            IconButton(
                              icon: Icon(Icons.arrow_back,
                                  color: isDark ? Colors.white : Colors.black),
                              onPressed: () => Navigator.pop(context),
                            ),
                            Text(
                              'Stack Builder',
                              style: Theme.of(context)
                                  .textTheme
                                  .titleLarge
                                  ?.copyWith(
                                    fontWeight: FontWeight.bold,
                                    color: isDark
                                        ? Colors.white
                                        : AppColors.textPrimaryLight,
                                  ),
                            ),
                            Row(
                              children: [
                                IconButton(
                                  icon: const Icon(Icons.auto_awesome,
                                      color: AppColors.primaryGold),
                                  onPressed: () =>
                                      _showPresetsSheet(context, viewModel),
                                  tooltip: 'Archetype Presets',
                                ),
                                TextButton(
                                  onPressed: viewModel.isLoading
                                      ? null
                                      : () => _handleSave(viewModel),
                                  child: viewModel.isLoading
                                      ? const SizedBox(
                                          width: 20,
                                          height: 20,
                                          child: CircularProgressIndicator(
                                              strokeWidth: 2),
                                        )
                                      : const Text(
                                          'Save',
                                          style: TextStyle(
                                            color: AppColors.primary,
                                            fontWeight: FontWeight.bold,
                                            fontSize: 16,
                                          ),
                                        ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),

                      Expanded(
                        child: viewModel.error != null
                            ? Center(
                                child: Padding(
                                  padding: const EdgeInsets.all(20.0),
                                  child: Column(
                                    mainAxisSize: MainAxisSize.min,
                                    children: [
                                      Text(
                                        viewModel.error!,
                                        textAlign: TextAlign.center,
                                        style:
                                            const TextStyle(color: Colors.red),
                                      ),
                                      const SizedBox(height: 16),
                                      ElevatedButton(
                                        onPressed: () => viewModel.initialize(),
                                        child: const Text('Retry'),
                                      ),
                                    ],
                                  ),
                                ),
                              )
                            : SingleChildScrollView(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    // Slot Selector
                                    SingleChildScrollView(
                                      scrollDirection: Axis.horizontal,
                                      padding: const EdgeInsets.symmetric(
                                          horizontal: 16, vertical: 8),
                                      child: Row(
                                        children: [
                                          _buildSlotTab('morning', '🌅',
                                              viewModel, isDark),
                                          const SizedBox(width: 8),
                                          _buildSlotTab('afternoon', '☀️',
                                              viewModel, isDark),
                                          const SizedBox(width: 8),
                                          _buildSlotTab('evening', '🌇',
                                              viewModel, isDark),
                                          const SizedBox(width: 8),
                                          _buildSlotTab(
                                              'night', '🌙', viewModel, isDark),
                                        ],
                                      ),
                                    ),

                                    // Stack Profile Visualization (The "Why")
                                    if (viewModel.currentStack != null &&
                                        viewModel
                                            .currentStack!.items.isNotEmpty)
                                      Padding(
                                        padding: const EdgeInsets.symmetric(
                                            horizontal: 16, vertical: 8),
                                        child: Row(
                                          mainAxisAlignment:
                                              MainAxisAlignment.spaceAround,
                                          children: [
                                            _buildBenefitIndicator(
                                                'FOCUS',
                                                Icons.psychology,
                                                AppColors.primary,
                                                0.8),
                                            _buildBenefitIndicator('ENERGIZE',
                                                Icons.bolt, Colors.amber, 0.6),
                                            _buildBenefitIndicator('CALM',
                                                Icons.spa, Colors.green, 0.7),
                                          ],
                                        ),
                                      ),

                                    // Safety Alert Banner (Dynamic)
                                    if (safetyViewModel
                                        .currentInteractions.isNotEmpty)
                                      Padding(
                                        padding: const EdgeInsets.all(16.0),
                                        child: SafetyAlertBanner(
                                          interaction: safetyViewModel
                                              .currentInteractions.first,
                                          onLearnMore: () {
                                            Navigator.pushNamed(
                                              context,
                                              AppRouter.safetyInteractionDetail,
                                              arguments: safetyViewModel
                                                  .currentInteractions.first,
                                            );
                                          },
                                        ),
                                      ),

                                    // Library Section Header
                                    Padding(
                                      padding: const EdgeInsets.symmetric(
                                          horizontal: 16, vertical: 8),
                                      child: Row(
                                        mainAxisAlignment:
                                            MainAxisAlignment.spaceBetween,
                                        children: [
                                          Text(
                                            'Library',
                                            style: Theme.of(context)
                                                .textTheme
                                                .titleLarge
                                                ?.copyWith(
                                                  fontWeight: FontWeight.bold,
                                                  color: isDark
                                                      ? Colors.white
                                                      : AppColors
                                                          .textPrimaryLight,
                                                ),
                                          ),
                                          TextButton(
                                            onPressed: () =>
                                                Navigator.pushNamed(
                                                    context, AppRouter.library),
                                            child: const Text(
                                              'View All',
                                              style: TextStyle(
                                                color: AppColors.primary,
                                                fontSize: 12,
                                                fontWeight: FontWeight.w600,
                                              ),
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),

                                    // Search Bar for Library
                                    Padding(
                                      padding: const EdgeInsets.symmetric(
                                          horizontal: 16, vertical: 8),
                                      child: Container(
                                        height: 44,
                                        decoration: BoxDecoration(
                                          color: isDark
                                              ? AppColors.cardDark
                                              : Colors.white,
                                          borderRadius:
                                              BorderRadius.circular(12),
                                          border: Border.all(
                                            color: isDark
                                                ? Colors.white
                                                    .withValues(alpha: 0.1)
                                                : Colors.grey[300]!,
                                          ),
                                        ),
                                        child: TextField(
                                          onChanged: (v) =>
                                              viewModel.updateSearchQuery(v),
                                          decoration: InputDecoration(
                                            hintText: 'Search supplements...',
                                            hintStyle: TextStyle(
                                              fontSize: 14,
                                              color: isDark
                                                  ? Colors.white54
                                                  : Colors.grey,
                                            ),
                                            prefixIcon: const Icon(Icons.search,
                                                size: 20,
                                                color: AppColors.primary),
                                            border: InputBorder.none,
                                            contentPadding:
                                                const EdgeInsets.symmetric(
                                                    vertical: 10),
                                          ),
                                          style: TextStyle(
                                            color: isDark
                                                ? Colors.white
                                                : Colors.black,
                                            fontSize: 14,
                                          ),
                                        ),
                                      ),
                                    ),

                                    // Horizontal Library List
                                    SizedBox(
                                      height: 120,
                                      child: ListView.separated(
                                        padding: const EdgeInsets.symmetric(
                                            horizontal: 16),
                                        scrollDirection: Axis.horizontal,
                                        itemCount: libraryItems.length,
                                        separatorBuilder: (context, index) =>
                                            const SizedBox(width: 12),
                                        itemBuilder: (context, index) {
                                          final item = libraryItems[index];
                                          return LibraryItem(
                                            id: item.id,
                                            name: item.name,
                                            dosage: item.dosage,
                                            icon: item.icon,
                                            iconColor: item.iconColor,
                                            iconBgColor: item.iconBgColor,
                                            onTap: () async {
                                              final supplement = viewModel
                                                  .availableSupplements
                                                  .firstWhere(
                                                      (s) => s.id == item.id);
                                              Navigator.pushNamed(
                                                context,
                                                AppRouter.supplementDetail,
                                                arguments: supplement,
                                              );
                                            },
                                          );
                                        },
                                      ),
                                    ),

                                    // Drop Zone Section Header
                                    Padding(
                                      padding: const EdgeInsets.fromLTRB(
                                          16, 16, 16, 12),
                                      child: Row(
                                        mainAxisAlignment:
                                            MainAxisAlignment.spaceBetween,
                                        children: [
                                          Column(
                                            crossAxisAlignment:
                                                CrossAxisAlignment.start,
                                            children: [
                                              Text(
                                                viewModel.currentStack?.name ??
                                                    '${viewModel.selectedSlot.capitalize()} Stack',
                                                style: Theme.of(context)
                                                    .textTheme
                                                    .headlineSmall
                                                    ?.copyWith(
                                                      fontWeight:
                                                          FontWeight.bold,
                                                      color: isDark
                                                          ? Colors.white
                                                          : Colors.black,
                                                      fontSize: 22,
                                                    ),
                                              ),
                                              const SizedBox(height: 2),
                                              Text(
                                                'Routine for ${viewModel.selectedSlot.capitalize()}',
                                                style: const TextStyle(
                                                  color: AppColors
                                                      .textSecondaryDark,
                                                  fontSize: 12,
                                                ),
                                              ),
                                            ],
                                          ),
                                          IconButton(
                                            icon: const Icon(Icons.edit,
                                                color:
                                                    AppColors.textSecondaryDark,
                                                size: 18),
                                            onPressed: () =>
                                                _showEditStackMetaDialog(
                                                    context, viewModel),
                                          ),
                                        ],
                                      ),
                                    ),

                                    // Drop Zone
                                    Padding(
                                      padding: const EdgeInsets.symmetric(
                                          horizontal: 16),
                                      child: StackDropZone(
                                        currentItems: currentStackData,
                                        instructionText:
                                            'Drag supplements here to build your ${viewModel.selectedSlot.toLowerCase()} routine.',
                                        onItemDropped: (id) =>
                                            _handleItemDropped(viewModel, id),
                                        onItemRemoved: (index) =>
                                            viewModel.removeItem(index),
                                        onReorder: (oldIndex, newIndex) =>
                                            viewModel.reorderItems(
                                                oldIndex, newIndex),
                                        onItemTap: (index) =>
                                            _showEditDosageSheet(
                                                context, viewModel, index),
                                      ),
                                    ),

                                    // Real-time Intelligence Logic
                                    if (viewModel.stackInsight != null)
                                      Padding(
                                        padding: const EdgeInsets.all(16.0),
                                        child: AnimatedContainer(
                                          duration:
                                              const Duration(milliseconds: 400),
                                          padding: const EdgeInsets.all(16),
                                          decoration: BoxDecoration(
                                            color: AppColors.primaryGold
                                                .withValues(alpha: 0.1),
                                            borderRadius:
                                                BorderRadius.circular(16),
                                            border: Border.all(
                                                color: AppColors.primaryGold
                                                    .withValues(alpha: 0.2)),
                                          ),
                                          child: Row(
                                            children: [
                                              const Icon(Icons.lightbulb,
                                                  color: AppColors.primaryGold,
                                                  size: 20),
                                              const SizedBox(width: 12),
                                              Expanded(
                                                child: Text(
                                                  viewModel.stackInsight!,
                                                  style: TextStyle(
                                                    color: isDark
                                                        ? Colors.white
                                                            .withValues(
                                                                alpha: 0.9)
                                                        : Colors.black87,
                                                    fontSize: 13,
                                                    height: 1.4,
                                                  ),
                                                ),
                                              ),
                                            ],
                                          ),
                                        ),
                                      ),

                                    // Footer Stats
                                    Padding(
                                      padding: const EdgeInsets.symmetric(
                                          horizontal: 16, vertical: 16),
                                      child: Row(
                                        mainAxisAlignment:
                                            MainAxisAlignment.spaceBetween,
                                        children: [
                                          Text(
                                            'Total Items: ${viewModel.currentStack?.items.length ?? 0}',
                                            style: const TextStyle(
                                              color:
                                                  AppColors.textSecondaryDark,
                                              fontWeight: FontWeight.w600,
                                              fontSize: 12,
                                            ),
                                          ),
                                          Row(
                                            children: [
                                              const Text(
                                                'Safety Status: ',
                                                style: TextStyle(
                                                  color: AppColors
                                                      .textSecondaryDark,
                                                  fontWeight: FontWeight.w600,
                                                  fontSize: 12,
                                                ),
                                              ),
                                              Text(
                                                safetyViewModel.isLoading
                                                    ? 'Checking...'
                                                    : (safetyViewModel
                                                            .currentInteractions
                                                            .isEmpty
                                                        ? 'All Clear'
                                                        : 'Alert'),
                                                style: TextStyle(
                                                  color: safetyViewModel
                                                          .currentInteractions
                                                          .isEmpty
                                                      ? Colors.green
                                                      : Colors.amber,
                                                  fontWeight: FontWeight.bold,
                                                  fontSize: 12,
                                                ),
                                              ),
                                            ],
                                          ),
                                        ],
                                      ),
                                    ),

                                    const SizedBox(
                                        height: 100), // Bottom padding
                                  ],
                                ),
                              ),
                      ),
                    ],
                  ),

                  // Floating Action Button
                  Positioned(
                    bottom: 24,
                    left: 0,
                    right: 0,
                    child: Center(
                      child: ElevatedButton.icon(
                        onPressed: () {
                          if (safetyViewModel.currentInteractions.isNotEmpty) {
                            Navigator.pushNamed(
                              context,
                              AppRouter.safetyInteractionDetail,
                              arguments:
                                  safetyViewModel.currentInteractions.first,
                            );
                          } else {
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(
                                content: Text(
                                    'Analysis Complete: No interactions found.'),
                                backgroundColor: Colors.green,
                                duration: Duration(seconds: 2),
                              ),
                            );
                          }
                        },
                        icon: Icon(
                            safetyViewModel.currentInteractions.isNotEmpty
                                ? Icons.warning
                                : Icons.check_circle,
                            size: 24),
                        label: Text(
                          safetyViewModel.currentInteractions.isNotEmpty
                              ? 'Analyze Warnings'
                              : 'Analyze Stack',
                          style: const TextStyle(
                              fontSize: 16, fontWeight: FontWeight.bold),
                        ),
                        style: ElevatedButton.styleFrom(
                          backgroundColor:
                              safetyViewModel.currentInteractions.isEmpty
                                  ? AppColors.primary
                                  : Colors.amber[700],
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(
                              horizontal: 32, vertical: 16),
                          shape: const StadiumBorder(),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
      ),
    );
  }

  void _showEditDosageSheet(
      BuildContext context, StackBuilderViewModel viewModel, int index) {
    if (viewModel.currentStack == null) return;
    final item = viewModel.currentStack!.items[index];
    final supplement = viewModel.availableSupplements.firstWhere(
      (s) => s.id == item.supplementId,
      orElse: () => throw Exception('Supplement not found'),
    );

    final dosageController = TextEditingController(
        text: item.customDosage ?? supplement.defaultDosage);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => Container(
        padding: EdgeInsets.only(
          bottom: MediaQuery.of(context).viewInsets.bottom + 24,
          left: 24,
          right: 24,
          top: 24,
        ),
        decoration: BoxDecoration(
          color: isDark ? const Color(0xFF1E242E) : Colors.white,
          borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Customize ${supplement.name}',
              style: GoogleFonts.lexend(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: isDark ? Colors.white : Colors.black,
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: dosageController,
              autofocus: true,
              style: TextStyle(color: isDark ? Colors.white : Colors.black),
              decoration: InputDecoration(
                labelText: 'Dosage Instructions',
                labelStyle: const TextStyle(color: AppColors.primary),
                hintText: 'e.g., 500mg once daily',
                hintStyle:
                    TextStyle(color: isDark ? Colors.white38 : Colors.grey),
                enabledBorder: UnderlineInputBorder(
                  borderSide: BorderSide(
                    color: isDark ? Colors.white24 : Colors.grey[300]!,
                  ),
                ),
                focusedBorder: const UnderlineInputBorder(
                  borderSide: BorderSide(color: AppColors.primary),
                ),
              ),
            ),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                onPressed: () {
                  viewModel.updateItemDosage(
                      item.supplementId, dosageController.text);
                  Navigator.pop(context);
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary,
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                child: const Text('Update Reward',
                    style: TextStyle(fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showEditStackMetaDialog(
      BuildContext context, StackBuilderViewModel viewModel) {
    if (viewModel.currentStack == null) return;

    final nameController =
        TextEditingController(text: viewModel.currentStack!.name);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => Container(
        padding: EdgeInsets.only(
          bottom: MediaQuery.of(context).viewInsets.bottom + 24,
          left: 24,
          right: 24,
          top: 24,
        ),
        decoration: BoxDecoration(
          color: isDark ? const Color(0xFF1E242E) : Colors.white,
          borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Edit Routine Details',
              style: GoogleFonts.lexend(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: isDark ? Colors.white : Colors.black,
              ),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: nameController,
              autofocus: true,
              style: TextStyle(color: isDark ? Colors.white : Colors.black),
              decoration: InputDecoration(
                labelText: 'Routine Name',
                labelStyle: const TextStyle(color: AppColors.primary),
                hintText: 'e.g., Pre-Workout, Early Bird',
                hintStyle:
                    TextStyle(color: isDark ? Colors.white38 : Colors.grey),
                enabledBorder: UnderlineInputBorder(
                  borderSide: BorderSide(
                    color: isDark ? Colors.white24 : Colors.grey[300]!,
                  ),
                ),
                focusedBorder: const UnderlineInputBorder(
                  borderSide: BorderSide(color: AppColors.primary),
                ),
              ),
            ),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                onPressed: () {
                  viewModel.updateStackMeta(nameController.text);
                  Navigator.pop(context);
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary,
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                child: const Text('Save Details',
                    style: TextStyle(fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSlotTab(
      String slot, String emoji, StackBuilderViewModel viewModel, bool isDark) {
    final isSelected = viewModel.selectedSlot == slot;
    return GestureDetector(
      onTap: () => viewModel.selectSlot(slot),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          color: isSelected
              ? AppColors.primary
              : (isDark
                  ? Colors.white.withValues(alpha: 0.05)
                  : Colors.grey[200]),
          borderRadius: BorderRadius.circular(20),
          border: Border.all(
            color: isSelected ? AppColors.primary : Colors.transparent,
          ),
        ),
        child: Row(
          children: [
            Text(emoji, style: const TextStyle(fontSize: 14)),
            const SizedBox(width: 6),
            Text(
              slot.capitalize(),
              style: TextStyle(
                color: isSelected
                    ? Colors.white
                    : (isDark ? Colors.white70 : Colors.black87),
                fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                fontSize: 13,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildBenefitIndicator(
      String label, IconData icon, Color color, double level) {
    return Column(
      children: [
        Container(
          padding: const EdgeInsets.all(10),
          decoration: BoxDecoration(
            color: color.withValues(alpha: 0.1),
            shape: BoxShape.circle,
          ),
          child: Icon(icon, color: color, size: 20),
        ),
        const SizedBox(height: 4),
        Text(
          label,
          style: GoogleFonts.lexend(
            fontSize: 9,
            fontWeight: FontWeight.bold,
            color: color.withValues(alpha: 0.8),
            letterSpacing: 0.5,
          ),
        ),
      ],
    );
  }

  void _showPresetsSheet(
      BuildContext context, StackBuilderViewModel viewModel) {
    showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => StackPresetsModal(
        onSelect: (archetype) {
          viewModel.applyPreset(archetype);
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Applied ${archetype.capitalize()} preset! ✨'),
              backgroundColor: AppColors.primary,
              duration: const Duration(seconds: 2),
            ),
          );
        },
      ),
    );
  }
}
