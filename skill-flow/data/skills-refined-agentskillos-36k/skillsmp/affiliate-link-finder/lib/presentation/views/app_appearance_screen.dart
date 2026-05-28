import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../theme/app_theme.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../../domain/repositories/settings_repository.dart';
import '../../config/locator.dart';
import '../../application/view_models/theme_view_model.dart';
import 'package:provider/provider.dart';

class AppAppearanceScreen extends StatefulWidget {
  const AppAppearanceScreen({super.key});

  @override
  State<AppAppearanceScreen> createState() => _AppAppearanceScreenState();
}

class _AppAppearanceScreenState extends State<AppAppearanceScreen> {
  String _selectedWallpaper = 'Nature';
  String _selectedIcon = 'Dopamine Hit';
  bool _reducedMotion = false;
  bool _hapticEnabled = true;
  double _fontScale = 1.0;

  @override
  void initState() {
    super.initState();
    _loadPreferences();
  }

  Future<void> _loadPreferences() async {
    final prefs = await SharedPreferences.getInstance();
    final settingsRepo = locator<SettingsRepository>();

    if (!mounted) return;
    setState(() {
      _selectedWallpaper = prefs.getString('appearance_wallpaper') ?? 'Nature';
      _selectedIcon = prefs.getString('appearance_icon') ?? 'Dopamine Hit';
      _reducedMotion = settingsRepo.getReducedMotionEnabled();
      _hapticEnabled = settingsRepo.getHapticFeedbackEnabled();
      _fontScale = settingsRepo.getFontSizeScale();
    });
  }

  Future<void> _savePreference(String key, String value) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(key, value);
  }

  Future<void> _toggleReducedMotion(bool value) async {
    await Provider.of<ThemeViewModel>(context, listen: false)
        .updateReducedMotion(value);
    setState(() => _reducedMotion = value);
  }

  Future<void> _toggleHaptic(bool value) async {
    await Provider.of<ThemeViewModel>(context, listen: false)
        .updateHapticEnabled(value);
    setState(() => _hapticEnabled = value);
  }

  Future<void> _updateFontScale(double value) async {
    await Provider.of<ThemeViewModel>(context, listen: false)
        .updateFontScale(value);
    setState(() => _fontScale = value);
  }

  @override
  Widget build(BuildContext context) {
    // Colors from design
    const bgDark = AppColors.backgroundPremiumDark;
    const bgLight = AppColors.backgroundPremiumLight;
    const primaryGold = AppColors.primaryGold;

    final isDark = Theme.of(context).brightness == Brightness.dark;
    final bgColor = isDark ? bgDark : bgLight;

    return Scaffold(
      backgroundColor: bgColor,
      appBar: AppBar(
        backgroundColor: bgColor,
        foregroundColor: isDark ? Colors.white : AppColors.textPrimaryLight,
        elevation: 0,
        leading: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Container(
            decoration: BoxDecoration(
              color: primaryGold.withValues(alpha: 0.1),
              shape: BoxShape.circle,
            ),
            child: IconButton(
              icon: const Icon(Icons.arrow_back, size: 20),
              color: primaryGold,
              onPressed: () => Navigator.pop(context),
            ),
          ),
        ),
        title: Column(
          children: [
            Text(
              'App Appearance',
              style: GoogleFonts.lexend(
                color: isDark ? Colors.white : AppColors.textPrimaryLight,
                fontSize: 18,
                fontWeight: FontWeight.w900, // Extrabold
              ),
            ),
            Text(
              'Make it yours',
              style: GoogleFonts.lexend(
                color: AppColors.textTertiary(isDark),
                fontSize: 12,
                fontWeight: FontWeight.w500,
              ),
            ),
          ],
        ),
        centerTitle: true,
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: SingleChildScrollView(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Preview Header
                    Padding(
                      padding: const EdgeInsets.fromLTRB(16, 20, 16, 12),
                      child: Text(
                        'Preview on Home Screen',
                        style: GoogleFonts.lexend(
                          color: isDark
                              ? Colors.white
                              : AppColors.textPrimaryLight,
                          fontSize: 22,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                    ),

                    // Mockup Container
                    Container(
                      height: 340,
                      margin: const EdgeInsets.symmetric(horizontal: 16),
                      decoration: BoxDecoration(
                        color: Colors.grey[800],
                        borderRadius: BorderRadius.circular(24),
                        border: Border.all(
                            color: AppColors.borderColor(isDark), width: 4),
                        boxShadow: [
                          BoxShadow(
                              color: Colors.black.withValues(alpha: 0.4),
                              blurRadius: 20,
                              offset: const Offset(0, 10)),
                        ],
                        image: DecorationImage(
                          image: const CachedNetworkImageProvider(
                              'https://lh3.googleusercontent.com/aida-public/AB6AXuDQ-nxTxmGSXL3P2fZ-MUFeVo5aYTAjTQm5PuIca3EV9pqLy2l7UcW28rMGc5ojaEyhYC0m0dRzptKCWhTyp5JM33LMfothoqg2xhPz7icCMqLjtFOGCtumUW1-TUWbZ46KrCYP4TRkpcqoGXIh_iBVOsf-p-zHFjEL0b2t8x3o11MNM2tKYi8A8Xeib6ctj8PBXEHM8O9J9rOpXM9kizznS_woimoNpyke-cn54Fk516Jpcd7L5u-HZvor1piFvRXtRLOV8DjovrI'),
                          fit: BoxFit.cover,
                          colorFilter: ColorFilter.mode(
                              Colors.black.withValues(alpha: 0.2),
                              BlendMode.darken),
                        ),
                      ),
                      child: Column(
                        children: [
                          // Status Bar Mockup
                          Padding(
                            padding: const EdgeInsets.symmetric(
                                horizontal: 24, vertical: 16),
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Text('9:41',
                                    style: GoogleFonts.lexend(
                                        color: Colors.white,
                                        fontSize: 12,
                                        fontWeight: FontWeight.bold)),
                                const Row(
                                  children: [
                                    Icon(Icons.signal_cellular_alt,
                                        color: Colors.white, size: 14),
                                    SizedBox(width: 4),
                                    Icon(Icons.wifi,
                                        color: Colors.white, size: 14),
                                    SizedBox(width: 4),
                                    Icon(Icons.battery_full,
                                        color: Colors.white, size: 14),
                                  ],
                                ),
                              ],
                            ),
                          ),

                          // App Icon Preview
                          Expanded(
                            child: Center(
                              child: Column(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  Container(
                                    width: 80,
                                    height: 80,
                                    decoration: BoxDecoration(
                                      gradient: _getIconGradient(_selectedIcon),
                                      color: _selectedIcon == 'Minimalist'
                                          ? Colors.white
                                          : null,
                                      borderRadius: BorderRadius.circular(20),
                                      border: Border.all(
                                          color: Colors.white
                                              .withValues(alpha: 0.2),
                                          width: 2),
                                      boxShadow: [
                                        BoxShadow(
                                            color: Colors.black
                                                .withValues(alpha: 0.3),
                                            blurRadius: 15,
                                            offset: const Offset(0, 5)),
                                      ],
                                    ),
                                    child: Icon(
                                      _getIconData(_selectedIcon),
                                      color: _selectedIcon == 'Minimalist'
                                          ? Colors.black87
                                          : (_selectedIcon == 'Stealth Mode'
                                              ? Colors.white54
                                              : Colors.white),
                                      size: 40,
                                    ),
                                  ),
                                  const SizedBox(height: 8),
                                  Container(
                                    padding: const EdgeInsets.symmetric(
                                        horizontal: 8, vertical: 2),
                                    decoration: BoxDecoration(
                                      color:
                                          Colors.black.withValues(alpha: 0.2),
                                      borderRadius: BorderRadius.circular(10),
                                    ),
                                    child: Text(
                                      'FocusApp',
                                      style: GoogleFonts.lexend(
                                        color: Colors.white,
                                        fontSize: 11,
                                        fontWeight: FontWeight.w600,
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ),

                          // Pagination Dots
                          Padding(
                            padding: const EdgeInsets.only(bottom: 20),
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                _buildDot(true),
                                const SizedBox(width: 8),
                                _buildDot(false),
                                const SizedBox(width: 8),
                                _buildDot(false),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),

                    // Wallpaper Switcher
                    Padding(
                      padding: const EdgeInsets.symmetric(
                          vertical: 24, horizontal: 16),
                      child: Container(
                        height: 48,
                        decoration: BoxDecoration(
                          color: isDark ? Colors.grey[800] : Colors.grey[200],
                          borderRadius: BorderRadius.circular(24),
                        ),
                        child: Row(
                          children: [
                            _buildWallpaperOption('Light', isDark),
                            _buildWallpaperOption('Dark', isDark),
                            _buildWallpaperOption('Nature', isDark),
                          ],
                        ),
                      ),
                    ),

                    // Icon Selection Header
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 16),
                      child: Text(
                        'Choose your icon',
                        style: GoogleFonts.lexend(
                          color:
                              isDark ? Colors.white : const Color(0xFF111418),
                          fontSize: 18,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                    ),

                    const SizedBox(height: 16),

                    // Icon Grid
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 16),
                      child: GridView.count(
                        shrinkWrap: true,
                        physics: const NeverScrollableScrollPhysics(),
                        crossAxisCount: 2,
                        crossAxisSpacing: 16,
                        mainAxisSpacing: 16,
                        childAspectRatio: 1.1, // Adjust for card shape
                        children: [
                          _buildIconCard('Classic Focus', 'The original vibe',
                              Icons.psychology, isDark),
                          _buildIconCard('Minimalist', 'Clean & simple',
                              Icons.radio_button_checked, isDark),
                          _buildIconCard('Stealth Mode', 'Low distraction',
                              Icons.visibility_off, isDark),
                          _buildIconCard('Dopamine Hit', 'Burst of energy',
                              Icons.bolt, isDark),
                        ],
                      ),
                    ),

                    const SizedBox(height: 32),

                    // Accessibility Header
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 16),
                      child: Text(
                        'Accessibility & Sensory',
                        style: GoogleFonts.lexend(
                          color:
                              isDark ? Colors.white : const Color(0xFF111418),
                          fontSize: 18,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                    ),

                    const SizedBox(height: 16),

                    // Accessibility Controls
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 16),
                      child: Container(
                        decoration: BoxDecoration(
                          color: isDark ? Colors.grey[900] : Colors.white,
                          borderRadius: BorderRadius.circular(16),
                          border:
                              Border.all(color: AppColors.borderColor(isDark)),
                        ),
                        child: Column(
                          children: [
                            SwitchListTile(
                              title: Text('Reduced Motion',
                                  style: GoogleFonts.lexend(
                                    color: isDark ? Colors.white : Colors.black,
                                    fontWeight: FontWeight.w500,
                                  )),
                              subtitle: Text('Minimize animations & flashing',
                                  style: GoogleFonts.lexend(
                                    color: Colors.grey,
                                    fontSize: 12,
                                  )),
                              value: _reducedMotion,
                              activeThumbColor: primaryGold,
                              onChanged: _toggleReducedMotion,
                            ),
                            Divider(
                                height: 1,
                                color: isDark
                                    ? Colors.grey[800]
                                    : Colors.grey[200]),
                            SwitchListTile(
                              title: Text('Haptic Feedback',
                                  style: GoogleFonts.lexend(
                                    color: isDark ? Colors.white : Colors.black,
                                    fontWeight: FontWeight.w500,
                                  )),
                              subtitle: Text('Vibrate on interactions',
                                  style: GoogleFonts.lexend(
                                    color: Colors.grey,
                                    fontSize: 12,
                                  )),
                              value: _hapticEnabled,
                              activeThumbColor: primaryGold,
                              onChanged: _toggleHaptic,
                            ),
                            Divider(
                                height: 1,
                                color: isDark
                                    ? Colors.grey[800]
                                    : Colors.grey[200]),
                            Padding(
                              padding: const EdgeInsets.all(16.0),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    mainAxisAlignment:
                                        MainAxisAlignment.spaceBetween,
                                    children: [
                                      Text('Font Size Scaling',
                                          style: GoogleFonts.lexend(
                                            color: isDark
                                                ? Colors.white
                                                : Colors.black,
                                            fontWeight: FontWeight.w500,
                                          )),
                                      Text('${(_fontScale * 100).toInt()}%',
                                          style: GoogleFonts.lexend(
                                            color: primaryGold,
                                            fontWeight: FontWeight.bold,
                                          )),
                                    ],
                                  ),
                                  Slider(
                                    value: _fontScale,
                                    min: 0.8,
                                    max: 1.4,
                                    divisions: 6,
                                    activeColor: primaryGold,
                                    inactiveColor: isDark
                                        ? Colors.grey[700]
                                        : Colors.grey[300],
                                    onChanged: _updateFontScale,
                                  ),
                                  const Row(
                                    mainAxisAlignment:
                                        MainAxisAlignment.spaceBetween,
                                    children: [
                                      Text('Aa',
                                          style: TextStyle(
                                              fontSize: 12,
                                              color: Colors.grey)),
                                      Text('Aa',
                                          style: TextStyle(
                                              fontSize: 20,
                                              color: Colors.grey)),
                                    ],
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),

                    const SizedBox(
                        height: 120), // Bottom padding for fixed footer
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
      bottomSheet: Container(
        color: bgColor.withValues(alpha: 0.95), // Translucent background
        padding: const EdgeInsets.all(24),
        child: SafeArea(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                'iOS will show a system confirmation when you change the app icon.',
                textAlign: TextAlign.center,
                style: GoogleFonts.lexend(
                  color: isDark ? Colors.grey[400] : Colors.grey[500],
                  fontSize:
                      12, // Small text size 10px in design = ~12 in Flutter logical pixels roughly
                ),
              ),
              const SizedBox(height: 12),
              SizedBox(
                width: double.infinity,
                height: 56,
                child: ElevatedButton(
                  onPressed: () {
                    // TODO: Implement platform channel for icon change
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                          content: Text(
                              'Icon customization coming in next update!')),
                    );
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: primaryGold,
                    foregroundColor: Colors.black,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(28),
                    ),
                    elevation: 8,
                    shadowColor: primaryGold.withValues(alpha: 0.4),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(Icons.auto_fix_high,
                          size: 24), // magic_button proxy
                      const SizedBox(width: 8),
                      Text(
                        'Apply New Icon',
                        style: GoogleFonts.lexend(
                          fontSize: 16,
                          fontWeight: FontWeight.bold, // Extrabold proxy
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildDot(bool isActive) {
    return Container(
      width: 6,
      height: 6,
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: isActive ? 1.0 : 0.5),
        shape: BoxShape.circle,
      ),
    );
  }

  Widget _buildWallpaperOption(String label, bool isDark) {
    final isSelected = _selectedWallpaper == label;

    // In design, selected is white bg with pink text/shadow.
    // Dark mode: bg #22101b for selected
    final selectedBg = isDark ? const Color(0xFF22101B) : Colors.white;

    return Expanded(
      child: GestureDetector(
        onTap: () {
          setState(() => _selectedWallpaper = label);
          _savePreference('appearance_wallpaper', label);
        },
        child: Container(
          margin: const EdgeInsets.all(4),
          decoration: BoxDecoration(
            color: isSelected ? selectedBg : Colors.transparent,
            borderRadius: BorderRadius.circular(20),
            boxShadow: isSelected
                ? [
                    BoxShadow(
                        color: Colors.black.withValues(alpha: 0.05),
                        blurRadius: 4)
                  ]
                : null,
          ),
          alignment: Alignment.center,
          child: Text(
            label,
            style: GoogleFonts.lexend(
              color: isSelected
                  ? AppColors.primaryGold
                  : (isDark ? Colors.grey[400] : Colors.grey[500]),
              fontSize: 12,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildIconCard(
      String title, String subtitle, IconData icon, bool isDark) {
    final isSelected = _selectedIcon == title;
    const primaryGold = AppColors.primaryGold;

    final bgDark =
        const Color(0xFF1E293B).withValues(alpha: 0.5); // slate-800/50
    const bgLight = Color(0xFFF1F5F9); // slate-100

    final bgColor = isSelected
        ? primaryGold.withValues(alpha: isDark ? 0.2 : 0.1)
        : (isDark ? bgDark : bgLight);
    final borderColor = isSelected ? primaryGold : Colors.transparent;

    return GestureDetector(
      onTap: () {
        setState(() => _selectedIcon = title);
        _savePreference('appearance_icon', title);
      },
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: bgColor,
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: borderColor, width: 2),
          boxShadow: isSelected
              ? [
                  BoxShadow(
                      color: primaryGold.withValues(alpha: 0.2), blurRadius: 15)
                ]
              : null,
        ),
        child: Stack(
          children: [
            Column(
              children: [
                Expanded(
                  child: Container(
                    width: 64,
                    height: 64,
                    decoration: BoxDecoration(
                      gradient: _getIconGradient(title),
                      color: title == 'Minimalist' ? Colors.white : null,
                      borderRadius: BorderRadius.circular(16),
                      border: title == 'Minimalist'
                          ? Border.all(color: Colors.grey[300]!)
                          : null,
                      boxShadow: [
                        BoxShadow(
                            color: Colors.black.withValues(alpha: 0.1),
                            blurRadius: 8,
                            offset: const Offset(0, 4)),
                      ],
                    ),
                    child: Icon(
                      icon,
                      size: 32,
                      color: title == 'Minimalist'
                          ? Colors.grey[800]
                          : (title == 'Stealth Mode'
                              ? Colors.white54
                              : Colors.white),
                    ),
                  ),
                ),
                const SizedBox(height: 12),
                Text(
                  title,
                  style: GoogleFonts.lexend(
                    color: isDark ? Colors.white : const Color(0xFF111418),
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Text(
                  subtitle,
                  style: GoogleFonts.lexend(
                    color: title == 'Dopamine Hit' && isSelected
                        ? const Color(0xFFF20D93)
                        : (isDark ? Colors.grey[400] : Colors.grey[500]),
                    fontSize: 10,
                    fontWeight: title == 'Dopamine Hit' && isSelected
                        ? FontWeight.w600
                        : FontWeight.normal,
                  ),
                ),
              ],
            ),
            if (isSelected)
              Positioned(
                top: 0,
                right: 0,
                child: Container(
                  padding: const EdgeInsets.all(4),
                  decoration: const BoxDecoration(
                    color: primaryGold,
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(Icons.check, color: Colors.white, size: 10),
                ),
              ),
          ],
        ),
      ),
    );
  }

  LinearGradient? _getIconGradient(String title) {
    if (title == 'Dopamine Hit') {
      return const LinearGradient(
        colors: [Color(0xFFF20D93), Color(0xFF7C3AED)], // Pink to Purple
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
      );
    } else if (title == 'Classic Focus') {
      return const LinearGradient(
        colors: [Color(0xFF22C55E), Color(0xFF10B981)], // Green
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
      );
    } else if (title == 'Stealth Mode') {
      return const LinearGradient(
        colors: [Color(0xFF4B5563), Color(0xFF1F2937)], // Grey
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
      );
    }
    return null; // Minimalist is solid white
  }

  IconData _getIconData(String title) {
    if (title == 'Dopamine Hit') return Icons.bolt;
    if (title == 'Classic Focus') return Icons.psychology;
    if (title == 'Stealth Mode') return Icons.visibility_off;
    if (title == 'Minimalist') return Icons.radio_button_checked;
    return Icons.help;
  }
}
