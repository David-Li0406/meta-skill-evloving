import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../config/locator.dart';
import '../../application/view_models/pill_matcher_view_model.dart';
import '../theme/app_theme.dart';
import '../widgets/pill_preview_widget.dart';

class VisualPillMatcherScreen extends StatelessWidget {
  const VisualPillMatcherScreen({super.key});

  static Widget withProvider() {
    return ChangeNotifierProvider(
      create: (_) => locator<PillMatcherViewModel>(),
      child: const VisualPillMatcherScreen(),
    );
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    const primaryGold = AppColors.primaryGold;
    final viewModel = Provider.of<PillMatcherViewModel>(context, listen: false);

    return Scaffold(
      backgroundColor: isDark
          ? AppColors.backgroundPremiumDark
          : AppColors.backgroundPremiumLight,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: Icon(Icons.close, color: isDark ? Colors.white : Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
        title: Text(
          'VISUAL PILL MATCHER',
          style: GoogleFonts.lexend(
            color: isDark ? Colors.white : Colors.black,
            fontSize: 16,
            fontWeight: FontWeight.bold,
            letterSpacing: 1.0,
          ),
        ),
        centerTitle: true,
        actions: [
          IconButton(
            icon: const Icon(Icons.help_outline, color: primaryGold),
            onPressed: () {},
          ),
        ],
      ),
      body: Consumer<PillMatcherViewModel>(
        builder: (context, viewModel, child) {
          if (viewModel.isAnalyzing) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const CircularProgressIndicator(color: primaryGold),
                  const SizedBox(height: 24),
                  Text(
                    'Analyzing Pill Structure...',
                    style: GoogleFonts.lexend(
                      color: isDark ? Colors.white : Colors.black,
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'AI logic identifying shape and color',
                    style: GoogleFonts.lexend(
                      color: isDark ? Colors.grey : Colors.grey[700],
                      fontSize: 12,
                    ),
                  ),
                ],
              ),
            );
          }

          return SingleChildScrollView(
            child: Column(
              children: [
                // Preview Card
                Padding(
                  padding: const EdgeInsets.all(16),
                  child: Container(
                    clipBehavior: Clip.antiAlias,
                    decoration: BoxDecoration(
                      color: const Color(
                          0xFF1C2027), // Specific dark color from wireframe
                      borderRadius: BorderRadius.circular(20),
                      border: Border.all(
                          color: Colors.white.withValues(alpha: 0.1)),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withValues(alpha: 0.3),
                          blurRadius: 20,
                          offset: const Offset(0, 10),
                        ),
                      ],
                    ),
                    child: Column(
                      children: [
                        // Preview Area with Gradient
                        Stack(
                          alignment: Alignment.center,
                          children: [
                            Container(
                              height: 240,
                              decoration: const BoxDecoration(
                                gradient: LinearGradient(
                                  begin: Alignment.topLeft,
                                  end: Alignment.bottomRight,
                                  colors: [
                                    Color(0xFF1A2230),
                                    Color(0xFF0A0E14),
                                  ],
                                ),
                              ),
                            ),
                            // Background glow effect
                            Positioned.fill(
                              child: Container(
                                decoration: BoxDecoration(
                                  gradient: RadialGradient(
                                    colors: [
                                      viewModel.selectedColor
                                          .withValues(alpha: 0.2),
                                      Colors.transparent,
                                    ],
                                    radius: 0.7,
                                  ),
                                ),
                              ),
                            ),

                            // 3D Pill Preview
                            PillPreviewWidget(
                              shape: viewModel.selectedShape,
                              color: viewModel.selectedColor,
                              texture: viewModel.selectedTexture,
                            ),

                            // Camera/Scan Button
                            Positioned(
                              top: 16,
                              right: 16,
                              child: GestureDetector(
                                onTap: () =>
                                    _showScanOptions(context, viewModel),
                                child: Container(
                                  padding: const EdgeInsets.all(12),
                                  decoration: BoxDecoration(
                                    color: primaryGold.withValues(alpha: 0.2),
                                    shape: BoxShape.circle,
                                    border: Border.all(
                                        color: primaryGold, width: 1.5),
                                  ),
                                  child: const Icon(Icons.camera_alt,
                                      color: primaryGold, size: 20),
                                ),
                              ),
                            ),

                            // Label
                            Positioned(
                              bottom: 16,
                              right: 16,
                              child: Container(
                                padding: const EdgeInsets.symmetric(
                                    horizontal: 12, vertical: 6),
                                decoration: BoxDecoration(
                                  color: Colors.white.withValues(alpha: 0.05),
                                  borderRadius: BorderRadius.circular(20),
                                  border: Border.all(
                                      color:
                                          Colors.white.withValues(alpha: 0.1)),
                                ),
                                child: Row(
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    const Icon(Icons.view_in_ar,
                                        color: Colors.white, size: 14),
                                    const SizedBox(width: 6),
                                    Text(
                                      '3D PREVIEW',
                                      style: GoogleFonts.lexend(
                                        color: Colors.white,
                                        fontSize: 10,
                                        fontWeight: FontWeight.bold,
                                        letterSpacing: 1.0,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                          ],
                        ),

                        // Info Section
                        Container(
                          padding: const EdgeInsets.all(20),
                          width: double.infinity,
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'Morning Focus',
                                style: GoogleFonts.lexend(
                                  color: Colors.white,
                                  fontSize: 20,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              const SizedBox(height: 4),
                              Row(
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceBetween,
                                children: [
                                  Text(
                                    'Matches your physical supplement',
                                    style: GoogleFonts.lexend(
                                      color: Colors.grey[400],
                                      fontSize: 13,
                                    ),
                                  ),
                                  const Text(
                                    'ACTIVE',
                                    style: TextStyle(
                                      color: primaryGold,
                                      fontSize: 12,
                                      fontWeight: FontWeight.bold,
                                      letterSpacing: 0.5,
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
                ),

                // Shape Selector
                _buildSectionHeader(context, 'Shape'),
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  child: Row(
                    children: [
                      _buildShapeOption(
                          context, viewModel, PillShape.round, 'Round'),
                      const SizedBox(width: 12),
                      _buildShapeOption(
                          context, viewModel, PillShape.capsule, 'Capsule'),
                      const SizedBox(width: 12),
                      _buildShapeOption(
                          context, viewModel, PillShape.oval, 'Oval'),
                    ],
                  ),
                ),

                // Color Selector
                const SizedBox(height: 24),
                _buildSectionHeader(context, 'Color'),
                SizedBox(
                  height: 60,
                  child: ListView.separated(
                    padding: const EdgeInsets.symmetric(horizontal: 16),
                    scrollDirection: Axis.horizontal,
                    itemCount: viewModel.presetColors.length,
                    separatorBuilder: (_, __) => const SizedBox(width: 12),
                    itemBuilder: (context, index) {
                      final color = viewModel.presetColors[index];
                      final isSelected = viewModel.selectedColor == color;
                      return GestureDetector(
                        onTap: () => viewModel.setColor(color),
                        child: Container(
                          width: 48,
                          height: 48,
                          decoration: BoxDecoration(
                            color: color,
                            shape: BoxShape.circle,
                            border: isSelected
                                ? Border.all(color: primaryGold, width: 2)
                                : Border.all(
                                    color: Colors.grey[800]!, width: 1),
                            boxShadow: isSelected
                                ? [
                                    BoxShadow(
                                        color: color.withValues(alpha: 0.4),
                                        blurRadius: 8,
                                        spreadRadius: 1)
                                  ]
                                : null,
                          ),
                          child: isSelected
                              ? Center(
                                  child: Container(
                                    width: 40,
                                    height: 40,
                                    decoration: BoxDecoration(
                                      color: color,
                                      shape: BoxShape.circle,
                                      border: Border.all(
                                          color: isDark
                                              ? AppColors.backgroundDark
                                              : Colors.white,
                                          width: 2),
                                    ),
                                  ),
                                )
                              : null,
                        ),
                      );
                    },
                  ),
                ),

                // Gradient Slider Mockup
                Padding(
                  padding: const EdgeInsets.fromLTRB(16, 16, 16, 0),
                  child: Container(
                    height: 48,
                    decoration: BoxDecoration(
                      gradient: const LinearGradient(
                        colors: [
                          Color(0xFFFF4B4B), // Red
                          Color(0xFFFF9F00), // Orange/Yellow
                          Color(0xFF00D084), // Green
                          primaryGold, // Gold/Blue
                          Color(0xFF7B61FF), // Purple
                        ],
                      ),
                      borderRadius: BorderRadius.circular(24),
                      border: Border.all(
                          color: Colors.white.withValues(alpha: 0.1)),
                    ),
                    child: Stack(
                      alignment: Alignment.centerLeft,
                      children: [
                        // Mock Slider Thumb
                        Positioned(
                          left: 100,
                          child: Container(
                            width: 32,
                            height: 32,
                            decoration: BoxDecoration(
                              color: Colors.white,
                              shape: BoxShape.circle,
                              boxShadow: const [
                                BoxShadow(
                                    color: Colors.black26,
                                    blurRadius: 4,
                                    offset: Offset(0, 2)),
                              ],
                              border: Border.all(
                                  color: AppColors.backgroundDark, width: 2),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),

                // Texture Selector
                const SizedBox(height: 24),
                _buildSectionHeader(context, 'Texture'),
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  child: Row(
                    children: [
                      _buildTextureOption(context, viewModel, PillTexture.solid,
                          'Solid', Icons.texture),
                      const SizedBox(width: 12),
                      _buildTextureOption(context, viewModel, PillTexture.clear,
                          'Clear', Icons.water_drop), // Opacity/Water drop
                      const SizedBox(width: 12),
                      _buildTextureOption(context, viewModel, PillTexture.pearl,
                          'Pearl', Icons.auto_awesome),
                    ],
                  ),
                ),

                const SizedBox(height: 120), // Bottom spacing
              ],
            ),
          );
        },
      ),
      bottomNavigationBar: Container(
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(
          color: isDark
              ? AppColors.backgroundDark.withValues(alpha: 0.9)
              : Colors.white.withValues(alpha: 0.9),
          border: Border(
              top: BorderSide(
                  color: isDark
                      ? Colors.white.withValues(alpha: 0.05)
                      : Colors.grey[200]!)),
        ),
        child: SizedBox(
          width: double.infinity,
          height: 56,
          child: ElevatedButton(
            onPressed: () {
              // TODO: Return actual data or save via ViewModel
              viewModel.savePillAppearance(); // Assume ViewModel has this
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Pill appearance saved!')),
              );
              Navigator.pop(context);
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: primaryGold,
              foregroundColor: Colors.black,
              elevation: 8,
              shadowColor: primaryGold.withValues(alpha: 0.4),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(16),
              ),
            ),
            child: Text(
              'Save Appearance',
              style: GoogleFonts.lexend(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ),
      ),
    );
  }

  void _showScanOptions(BuildContext context, PillMatcherViewModel viewModel) {
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
              ListTile(
                leading: const Icon(Icons.camera_alt),
                title: const Text('Take Photo'),
                onTap: () {
                  Navigator.pop(context);
                  viewModel.scanPill();
                },
              ),
              ListTile(
                leading: const Icon(Icons.photo_library),
                title: const Text('Choose from Gallery'),
                onTap: () {
                  Navigator.pop(context);
                  viewModel.pickFromGallery();
                },
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSectionHeader(BuildContext context, String title) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      child: Align(
        alignment: Alignment.centerLeft,
        child: Text(
          title,
          style: GoogleFonts.lexend(
            color: Theme.of(context).brightness == Brightness.dark
                ? Colors.white
                : Colors.black,
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }

  Widget _buildShapeOption(BuildContext context, PillMatcherViewModel viewModel,
      PillShape shape, String label) {
    final isSelected = viewModel.selectedShape == shape;
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Expanded(
      child: GestureDetector(
        onTap: () => viewModel.setShape(shape),
        child: AspectRatio(
          aspectRatio: 1,
          child: Container(
            decoration: BoxDecoration(
              color: isSelected
                  ? (isDark
                      ? Colors.white.withValues(alpha: 0.05)
                      : Colors.blue.withValues(alpha: 0.05))
                  : (isDark
                      ? Colors.white.withValues(alpha: 0.02)
                      : Colors.grey.withValues(alpha: 0.05)),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(
                color: isSelected
                    ? AppColors.primaryGold
                    : (isDark
                        ? Colors.white.withValues(alpha: 0.1)
                        : Colors.grey[300]!),
                width: isSelected ? 2 : 1,
              ),
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                _buildShapeIcon(shape),
                const SizedBox(height: 12),
                Text(
                  label,
                  style: GoogleFonts.lexend(
                    color: isSelected
                        ? (isDark ? Colors.white : AppColors.primaryGold)
                        : Colors.grey,
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildShapeIcon(PillShape shape) {
    switch (shape) {
      case PillShape.round:
        return Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: Colors.grey.withValues(alpha: 0.3)));
      case PillShape.capsule:
        return Container(
            width: 50,
            height: 26,
            decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(100),
                color: Colors.grey.withValues(alpha: 0.3)));
      case PillShape.oval:
        return Container(
            width: 50,
            height: 32,
            decoration: BoxDecoration(
                borderRadius: const BorderRadius.all(Radius.elliptical(50, 32)),
                color: Colors.grey.withValues(alpha: 0.3)));
    }
  }

  Widget _buildTextureOption(
      BuildContext context,
      PillMatcherViewModel viewModel,
      PillTexture texture,
      String label,
      IconData icon) {
    final isSelected = viewModel.selectedTexture == texture;
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Expanded(
      child: GestureDetector(
        onTap: () => viewModel.setTexture(texture),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 24),
          decoration: BoxDecoration(
            color: isSelected
                ? AppColors.primaryGold.withValues(alpha: 0.1)
                : (isDark
                    ? Colors.white.withValues(alpha: 0.05)
                    : Colors.grey.withValues(alpha: 0.05)),
            borderRadius: BorderRadius.circular(16),
            border: Border.all(
              color: isSelected
                  ? AppColors.primaryGold
                  : (isDark
                      ? Colors.white.withValues(alpha: 0.1)
                      : Colors.grey[300]!),
              width: isSelected ? 2 : 1,
            ),
          ),
          child: Column(
            children: [
              Icon(
                icon,
                color: isSelected ? AppColors.primaryGold : Colors.grey,
                size: 28,
              ),
              const SizedBox(height: 8),
              Text(
                label,
                style: GoogleFonts.lexend(
                  color: isSelected
                      ? (isDark ? Colors.white : AppColors.primaryGold)
                      : Colors.grey,
                  fontSize: 12,
                  fontWeight: isSelected ? FontWeight.bold : FontWeight.w500,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
