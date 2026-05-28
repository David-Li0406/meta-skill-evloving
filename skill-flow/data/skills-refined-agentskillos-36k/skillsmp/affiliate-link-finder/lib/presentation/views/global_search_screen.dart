import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import '../../config/locator.dart';
import '../../application/view_models/global_search_view_model.dart';
import '../../application/providers/auth_provider.dart';
import '../theme/app_theme.dart';
import '../navigation/app_router.dart';
import '../widgets/skeleton_loader.dart';
import '../../domain/entities/supplement.dart';
import '../../domain/entities/supplement_stack.dart';

class GlobalSearchScreen extends StatefulWidget {
  const GlobalSearchScreen({super.key});

  @override
  State<GlobalSearchScreen> createState() => _GlobalSearchScreenState();
}

class _GlobalSearchScreenState extends State<GlobalSearchScreen> {
  late GlobalSearchViewModel _viewModel;
  final TextEditingController _controller = TextEditingController();
  final FocusNode _focusNode = FocusNode();

  @override
  void initState() {
    super.initState();
    final userId = context.read<AuthProvider>().user?.id ?? '';
    _viewModel = locator<GlobalSearchViewModel>(param1: userId);

    // Auto-focus search bar
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _focusNode.requestFocus();
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    _focusNode.dispose();
    _viewModel.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    const primaryGold = AppColors.primaryGold;

    return ChangeNotifierProvider.value(
      value: _viewModel,
      child: Scaffold(
        backgroundColor: isDark
            ? AppColors.backgroundPremiumDark
            : AppColors.backgroundPremiumLight,
        appBar: AppBar(
          backgroundColor: Colors.transparent,
          elevation: 0,
          leading: IconButton(
            icon: Icon(Icons.arrow_back_ios_new,
                color: isDark ? Colors.white : Colors.black),
            onPressed: () => Navigator.pop(context),
          ),
          title: Text(
            'SEARCH',
            style: GoogleFonts.lexend(
              fontSize: 14,
              fontWeight: FontWeight.bold,
              letterSpacing: 1.5,
              color: isDark ? Colors.white : Colors.black,
            ),
          ),
          centerTitle: true,
        ),
        body: Column(
          children: [
            // Search Bar
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
              child: Container(
                decoration: BoxDecoration(
                  color: isDark ? const Color(0xFF2D2616) : Colors.white,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: primaryGold.withValues(alpha: 0.2)),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withValues(alpha: 0.1),
                      blurRadius: 10,
                      offset: const Offset(0, 4),
                    ),
                  ],
                ),
                child: TextField(
                  controller: _controller,
                  focusNode: _focusNode,
                  style: GoogleFonts.lexend(
                      color: isDark ? Colors.white : Colors.black),
                  decoration: InputDecoration(
                    hintText: 'Search supplements, stacks...',
                    hintStyle: GoogleFonts.lexend(color: Colors.grey),
                    contentPadding: const EdgeInsets.symmetric(
                        horizontal: 20, vertical: 16),
                    border: InputBorder.none,
                    prefixIcon: Icon(Icons.search,
                        color: isDark ? Colors.grey : Colors.grey[600]),
                    suffixIcon: _controller.text.isNotEmpty
                        ? IconButton(
                            icon: const Icon(Icons.clear, color: Colors.grey),
                            onPressed: () {
                              _controller.clear();
                              _viewModel.clear();
                            },
                          )
                        : null,
                  ),
                  onChanged: (value) {
                    _viewModel.updateQuery(value);
                    setState(() {}); // Update to show/hide clear button
                  },
                ),
              ),
            ),

            // Results
            Expanded(
              child: Consumer<GlobalSearchViewModel>(
                builder: (context, viewModel, child) {
                  // Loading state
                  if (viewModel.isLoading) {
                    return _buildLoadingSkeleton();
                  }

                  // Error state
                  if (viewModel.error != null) {
                    return Center(
                      child: Padding(
                        padding: const EdgeInsets.all(24),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            const Icon(Icons.error_outline,
                                color: Colors.grey, size: 48),
                            const SizedBox(height: 16),
                            Text(
                              viewModel.error!,
                              style: GoogleFonts.lexend(color: Colors.grey),
                              textAlign: TextAlign.center,
                            ),
                          ],
                        ),
                      ),
                    );
                  }

                  // Empty state
                  if (viewModel.isEmpty) {
                    return _buildEmptyState(isDark);
                  }

                  // No query yet
                  if (viewModel.query.isEmpty) {
                    return _buildInitialState(isDark);
                  }

                  // Results
                  return SingleChildScrollView(
                    padding: const EdgeInsets.symmetric(horizontal: 20),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Supplements
                        if (viewModel.supplementResults.isNotEmpty) ...[
                          _buildSectionHeader('Supplements',
                              viewModel.supplementResults.length, isDark),
                          const SizedBox(height: 12),
                          ...viewModel.supplementResults.map((supplement) =>
                              _buildSupplementCard(supplement, isDark)),
                          const SizedBox(height: 24),
                        ],

                        // Stacks
                        if (viewModel.stackResults.isNotEmpty) ...[
                          _buildSectionHeader('Your Stacks',
                              viewModel.stackResults.length, isDark),
                          const SizedBox(height: 12),
                          ...viewModel.stackResults
                              .map((stack) => _buildStackCard(stack, isDark)),
                          const SizedBox(height: 24),
                        ],

                        const SizedBox(height: 80), // Bottom padding
                      ],
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSectionHeader(String title, int count, bool isDark) {
    return Text(
      '$title ($count)',
      style: GoogleFonts.lexend(
        fontSize: 16,
        fontWeight: FontWeight.bold,
        color: isDark ? Colors.white : Colors.black,
      ),
    );
  }

  Widget _buildSupplementCard(Supplement supplement, bool isDark) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF1E1E1E) : Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isDark
              ? Colors.white.withValues(alpha: 0.1)
              : Colors.grey.shade200,
        ),
      ),
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        leading: Container(
          width: 48,
          height: 48,
          decoration: BoxDecoration(
            color: AppColors.primaryGold.withValues(alpha: 0.1),
            borderRadius: BorderRadius.circular(12),
          ),
          child: const Icon(Icons.medication, color: AppColors.primaryGold),
        ),
        title: Text(
          supplement.name,
          style: GoogleFonts.lexend(
            fontWeight: FontWeight.w600,
            color: isDark ? Colors.white : Colors.black,
          ),
        ),
        subtitle: Text(
          supplement.category,
          style: GoogleFonts.lexend(
            fontSize: 12,
            color: Colors.grey,
          ),
        ),
        trailing: Icon(Icons.arrow_forward_ios,
            size: 16, color: isDark ? Colors.grey : Colors.grey[600]),
        onTap: () {
          Navigator.pushNamed(
            context,
            AppRouter.supplementDetail,
            arguments: supplement,
          );
        },
      ),
    );
  }

  Widget _buildStackCard(SupplementStack stack, bool isDark) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      decoration: BoxDecoration(
        color: isDark ? const Color(0xFF1E1E1E) : Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isDark
              ? Colors.white.withValues(alpha: 0.1)
              : Colors.grey.shade200,
        ),
      ),
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        leading: Container(
          width: 48,
          height: 48,
          decoration: BoxDecoration(
            color: AppColors.primaryGold.withValues(alpha: 0.1),
            borderRadius: BorderRadius.circular(12),
          ),
          child: const Icon(Icons.layers, color: AppColors.primaryGold),
        ),
        title: Text(
          stack.name,
          style: GoogleFonts.lexend(
            fontWeight: FontWeight.w600,
            color: isDark ? Colors.white : Colors.black,
          ),
        ),
        subtitle: Text(
          '${stack.items.length} supplements • ${stack.timeOfDay}',
          style: GoogleFonts.lexend(
            fontSize: 12,
            color: Colors.grey,
          ),
        ),
        trailing: Icon(Icons.arrow_forward_ios,
            size: 16, color: isDark ? Colors.grey : Colors.grey[600]),
        onTap: () {
          Navigator.pushNamed(context, AppRouter.stackBuilder);
        },
      ),
    );
  }

  Widget _buildLoadingSkeleton() {
    return const Padding(
      padding: EdgeInsets.symmetric(horizontal: 20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SkeletonLoader(height: 20, width: 150, borderRadius: 8),
          SizedBox(height: 12),
          SkeletonLoader(height: 80, borderRadius: 16),
          SizedBox(height: 12),
          SkeletonLoader(height: 80, borderRadius: 16),
          SizedBox(height: 12),
          SkeletonLoader(height: 80, borderRadius: 16),
        ],
      ),
    );
  }

  Widget _buildEmptyState(bool isDark) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.search_off, size: 64, color: Colors.grey),
            const SizedBox(height: 16),
            Text(
              'No results found',
              style: GoogleFonts.lexend(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: isDark ? Colors.white : Colors.black,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Try searching for:',
              style: GoogleFonts.lexend(color: Colors.grey),
            ),
            const SizedBox(height: 16),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: ['Omega-3', 'Magnesium', 'L-Theanine', 'Caffeine']
                  .map((suggestion) => _buildSuggestionChip(suggestion, isDark))
                  .toList(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInitialState(bool isDark) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.search, size: 64, color: AppColors.primaryGold),
            const SizedBox(height: 16),
            Text(
              'Search for supplements',
              style: GoogleFonts.lexend(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: isDark ? Colors.white : Colors.black,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Find what you need quickly',
              style: GoogleFonts.lexend(color: Colors.grey),
            ),
            const SizedBox(height: 24),
            Text(
              'Popular searches:',
              style: GoogleFonts.lexend(
                fontSize: 14,
                fontWeight: FontWeight.w600,
                color: Colors.grey,
              ),
            ),
            const SizedBox(height: 12),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: ['Omega-3', 'Magnesium', 'L-Theanine', 'Caffeine']
                  .map((suggestion) => _buildSuggestionChip(suggestion, isDark))
                  .toList(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSuggestionChip(String text, bool isDark) {
    return GestureDetector(
      onTap: () {
        _controller.text = text;
        _viewModel.updateQuery(text);
      },
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          color: AppColors.primaryGold.withValues(alpha: 0.1),
          borderRadius: BorderRadius.circular(20),
          border:
              Border.all(color: AppColors.primaryGold.withValues(alpha: 0.3)),
        ),
        child: Text(
          text,
          style: GoogleFonts.lexend(
            color: AppColors.primaryGold,
            fontWeight: FontWeight.w500,
          ),
        ),
      ),
    );
  }
}
