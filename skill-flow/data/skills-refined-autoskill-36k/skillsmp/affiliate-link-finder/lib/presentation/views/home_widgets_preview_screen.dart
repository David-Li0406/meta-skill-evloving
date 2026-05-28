import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../theme/app_theme.dart';

class HomeWidgetsPreviewScreen extends StatefulWidget {
  const HomeWidgetsPreviewScreen({super.key});

  @override
  State<HomeWidgetsPreviewScreen> createState() =>
      _HomeWidgetsPreviewScreenState();
}

class _HomeWidgetsPreviewScreenState extends State<HomeWidgetsPreviewScreen>
    with SingleTickerProviderStateMixin {
  bool _showNextStack = true;
  bool _showProgressRing = true;
  bool _quickLogButton = false;
  String _selectedTheme = 'Glassmorphism';

  int _tutorialStep = 0;
  late AnimationController _pulseController;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat(reverse: true);

    _loadPreferences();

    // Auto-start tutorial if first time (could also be pref-based)
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_tutorialStep == 0) {
        // Only if not restored/set yet
        setState(() => _tutorialStep = 1);
      }
    });
  }

  Future<void> _loadPreferences() async {
    final prefs = await SharedPreferences.getInstance();
    if (!mounted) return;
    setState(() {
      _showNextStack = prefs.getBool('widget_show_next_stack') ?? true;
      _showProgressRing = prefs.getBool('widget_show_progress_ring') ?? true;
      _quickLogButton = prefs.getBool('widget_quick_log') ?? false;
      _selectedTheme = prefs.getString('widget_theme') ?? 'Glassmorphism';
    });
  }

  Future<void> _savePreference(String key, dynamic value) async {
    final prefs = await SharedPreferences.getInstance();
    if (value is bool) {
      await prefs.setBool(key, value);
    } else if (value is String) {
      await prefs.setString(key, value);
    }
  }

  @override
  void dispose() {
    _pulseController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // Force dark theme colors based on design provided
    const bgDark = AppColors.backgroundPremiumDark;
    const primaryGold = AppColors.primaryGold;
    final cardBg = Colors.grey[900]!; // Zinc 900 approx

    return Stack(
      children: [
        Scaffold(
          backgroundColor: bgDark,
          appBar: AppBar(
            title: Text('Customize Widget',
                style: GoogleFonts.lexend(fontWeight: FontWeight.bold)),
            backgroundColor: bgDark.withValues(alpha: 0.8),
            foregroundColor: Colors.white,
            elevation: 0,
            centerTitle: true,
            leading: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.1),
                  shape: BoxShape.circle,
                ),
                child: IconButton(
                  icon: const Icon(Icons.arrow_back, size: 20),
                  onPressed: () => Navigator.pop(context),
                ),
              ),
            ),
            actions: [
              IconButton(
                icon: const Icon(Icons.help_outline, color: primaryGold),
                onPressed: () {},
              ),
            ],
          ),
          body: SafeArea(
            child: Column(
              children: [
                Expanded(
                  child: SingleChildScrollView(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const SizedBox(height: 16),
                        Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 16),
                          child: Text(
                            'Live Preview',
                            style: GoogleFonts.lexend(
                              color: Colors.grey,
                              fontSize: 14,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                        ),
                        const SizedBox(height: 16),

                        // Widget Carousel
                        SingleChildScrollView(
                          scrollDirection: Axis.horizontal,
                          padding: const EdgeInsets.symmetric(horizontal: 16),
                          child: Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              _buildSmallWidgetPreview(primaryGold, cardBg),
                              const SizedBox(width: 16),
                              _buildMediumWidgetPreview(primaryGold, cardBg),
                            ],
                          ),
                        ),

                        const SizedBox(height: 32),

                        // Features Section
                        Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 16),
                          child: Text(
                            'Widget Features',
                            style: GoogleFonts.lexend(
                              color: Colors.white,
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                        const SizedBox(height: 16),
                        Container(
                          margin: const EdgeInsets.symmetric(horizontal: 16),
                          decoration: BoxDecoration(
                            color: const Color(0xFF18181B), // Zinc 900
                            borderRadius: BorderRadius.circular(16),
                          ),
                          child: Column(
                            children: [
                              _buildToggleRow(
                                icon: Icons.layers,
                                title: 'Show Next Stack',
                                subtitle: 'Display upcoming supplement info',
                                value: _showNextStack,
                                onChanged: (v) {
                                  setState(() => _showNextStack = v);
                                  _savePreference('widget_show_next_stack', v);
                                },
                                primaryGold: primaryGold,
                              ),
                              Divider(
                                  height: 1,
                                  color: Colors.white.withValues(alpha: 0.05)),
                              _buildToggleRow(
                                icon: Icons.cached,
                                title: 'Show Progress Ring',
                                subtitle: 'Visualize daily completion',
                                value: _showProgressRing,
                                onChanged: (v) {
                                  setState(() => _showProgressRing = v);
                                  _savePreference(
                                      'widget_show_progress_ring', v);
                                },
                                primaryGold: primaryGold,
                              ),
                              Divider(
                                  height: 1,
                                  color: Colors.white.withValues(alpha: 0.05)),
                              _buildToggleRow(
                                icon: Icons.add_circle_outline,
                                title: 'Quick Log Button',
                                subtitle:
                                    'Log intake directly from home screen',
                                value: _quickLogButton,
                                onChanged: (v) {
                                  setState(() => _quickLogButton = v);
                                  _savePreference('widget_quick_log', v);
                                },
                                primaryGold: primaryGold,
                              ),
                            ],
                          ),
                        ),

                        const SizedBox(height: 32),

                        // Theme Selector
                        Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 16),
                          child: Text(
                            'Choose Theme',
                            style: GoogleFonts.lexend(
                              color: Colors.white,
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                        const SizedBox(height: 16),
                        Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 16),
                          child: GridView.count(
                            shrinkWrap: true,
                            physics: const NeverScrollableScrollPhysics(),
                            crossAxisCount: 2,
                            mainAxisSpacing: 12,
                            crossAxisSpacing: 12,
                            childAspectRatio: 1.4,
                            children: [
                              GestureDetector(
                                onTap: () {
                                  setState(
                                      () => _selectedTheme = 'Glassmorphism');
                                  _savePreference(
                                      'widget_theme', 'Glassmorphism');
                                },
                                child: _buildThemeOption(
                                  'Glassmorphism',
                                  primaryGold,
                                  isSelected: _selectedTheme == 'Glassmorphism',
                                  child: Stack(
                                    children: [
                                      Container(
                                        decoration: const BoxDecoration(
                                          image: DecorationImage(
                                            image: NetworkImage(
                                                'https://lh3.googleusercontent.com/aida-public/AB6AXuCAZKCVASRPep6HK8h-8b-3MiOxBYw4HZ6dIqouISEOOCIrfpgpsgJR6qMBMMTWlnMV8fE_GF_hM-t9L-NiZcJF5p6NLScE4VG_FO0IioP-sHRImbT6Q0QfjsoVBism-_yQ-z0vZoC5ig8u3IoV8K77c16rL6Hvk7Y46u4UhyHIcZobcZ2nPaVEmR7LyFyyjKYU7bs8DgI-wO1USCN1wwQTJAfb1knwjDo3i71OQl1DwCryGt3NfVt854NrkQMD9OsxYgQXR8K0J3w'),
                                            fit: BoxFit.cover,
                                          ),
                                        ),
                                      ),
                                      Container(
                                        decoration: BoxDecoration(
                                          color: Colors.black
                                              .withValues(alpha: 0.2),
                                          border: Border.all(
                                              color: Colors.white
                                                  .withValues(alpha: 0.2)),
                                        ),
                                        margin: const EdgeInsets.all(8),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                              GestureDetector(
                                onTap: () {
                                  setState(() => _selectedTheme = 'Dark');
                                  _savePreference('widget_theme', 'Dark');
                                },
                                child: _buildThemeOption(
                                  'Dark',
                                  primaryGold,
                                  isSelected: _selectedTheme == 'Dark',
                                  child: Container(
                                    color: const Color(0xFF09090B), // Zinc 950
                                    alignment: Alignment.center,
                                    child: Container(
                                      width: 50,
                                      height: 30,
                                      decoration: BoxDecoration(
                                        color: const Color(0xFF27272A),
                                        borderRadius: BorderRadius.circular(4),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              GestureDetector(
                                onTap: () {
                                  setState(() => _selectedTheme = 'Light');
                                  _savePreference('widget_theme', 'Light');
                                },
                                child: _buildThemeOption(
                                  'Light',
                                  primaryGold,
                                  isSelected: _selectedTheme == 'Light',
                                  child: Container(
                                    color: const Color(0xFFF8FAFC), // Slate 50
                                    alignment: Alignment.center,
                                    child: Container(
                                      width: 50,
                                      height: 30,
                                      decoration: BoxDecoration(
                                        color: const Color(0xFFE2E8F0),
                                        borderRadius: BorderRadius.circular(4),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              GestureDetector(
                                onTap: () {
                                  setState(() => _selectedTheme = 'Vibrant');
                                  _savePreference('widget_theme', 'Vibrant');
                                },
                                child: _buildThemeOption(
                                  'Vibrant',
                                  primaryGold,
                                  isSelected: _selectedTheme == 'Vibrant',
                                  child: Container(
                                    decoration: const BoxDecoration(
                                      gradient: LinearGradient(
                                        colors: [
                                          Colors.orange,
                                          Colors.pinkAccent
                                        ],
                                        begin: Alignment.bottomLeft,
                                        end: Alignment.topRight,
                                      ),
                                    ),
                                    alignment: Alignment.center,
                                    child: Container(
                                      width: 50,
                                      height: 30,
                                      decoration: BoxDecoration(
                                        color:
                                            Colors.white.withValues(alpha: 0.3),
                                        borderRadius: BorderRadius.circular(4),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),

                        const SizedBox(height: 32),

                        // Instructions
                        Container(
                          margin: const EdgeInsets.symmetric(horizontal: 16),
                          padding: const EdgeInsets.all(16),
                          decoration: BoxDecoration(
                            color: primaryGold.withValues(alpha: 0.1),
                            border: Border.all(
                                color: primaryGold.withValues(alpha: 0.2)),
                            borderRadius: BorderRadius.circular(16),
                          ),
                          child: Row(
                            children: [
                              const Icon(Icons.info, color: primaryGold),
                              const SizedBox(width: 12),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      'How to Add',
                                      style: GoogleFonts.lexend(
                                        color: primaryGold,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                    const SizedBox(height: 4),
                                    const Text(
                                      'Press and hold an empty area on your home screen, tap the (+) button, and search for "ADHD Supps".',
                                      style: TextStyle(
                                        color: Colors.grey,
                                        fontSize: 12,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(height: 120), // Bottom padding
                      ],
                    ),
                  ),
                ),

                // Footer
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: bgDark.withValues(alpha: 0.9),
                    border: Border(
                      top: BorderSide(
                          color: Colors.white.withValues(alpha: 0.1)),
                    ),
                  ),
                  child: Column(
                    children: [
                      SizedBox(
                        width: double.infinity,
                        height: 56,
                        child: ElevatedButton(
                          onPressed: () {
                            // Show tutorial dialog with platform-specific instructions
                            showDialog<void>(
                              context: context,
                              builder: (context) => AlertDialog(
                                title: const Text('Add Widget Tutorial'),
                                content: const SingleChildScrollView(
                                  child: Column(
                                    mainAxisSize: MainAxisSize.min,
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        'iOS Instructions:',
                                        style: TextStyle(
                                            fontWeight: FontWeight.bold),
                                      ),
                                      SizedBox(height: 8),
                                      Text(
                                          '1. Long press on your home screen\n2. Tap the "+" button in the top left\n3. Search for "FocusStack"\n4. Select your preferred widget size\n5. Tap "Add Widget"'),
                                      SizedBox(height: 16),
                                      Text(
                                        'Android Instructions:',
                                        style: TextStyle(
                                            fontWeight: FontWeight.bold),
                                      ),
                                      SizedBox(height: 8),
                                      Text(
                                          '1. Long press on your home screen\n2. Tap "Widgets"\n3. Find "FocusStack"\n4. Drag your preferred widget to the home screen'),
                                    ],
                                  ),
                                ),
                                actions: [
                                  TextButton(
                                    onPressed: () => Navigator.pop(context),
                                    child: const Text('Got It'),
                                  ),
                                ],
                              ),
                            );
                          },
                          style: ElevatedButton.styleFrom(
                            backgroundColor: primaryGold,
                            foregroundColor: bgDark,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(16),
                            ),
                            elevation: 0,
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Icon(Icons.add,
                                  fontWeight: FontWeight.bold),
                              const SizedBox(width: 8),
                              Text(
                                'Add to Home Screen',
                                style: GoogleFonts.lexend(
                                    fontWeight: FontWeight.bold, fontSize: 16),
                              ),
                            ],
                          ),
                        ),
                      ),
                      const SizedBox(height: 12),
                      Text(
                        'SYNCED WITH APPLE HEALTH',
                        style: GoogleFonts.lexend(
                          color: Colors.grey,
                          fontSize: 10,
                          fontWeight: FontWeight.bold,
                          letterSpacing: 1.5,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
        if (_tutorialStep > 0) _buildTutorialOverlay(primaryGold, bgDark),
      ],
    );
  }

  Widget _buildTutorialOverlay(Color primaryGold, Color bgDark) {
    String message = '';
    double top = 0;
    double? bottom;

    switch (_tutorialStep) {
      case 1:
        message = 'Welcome! First, customize your widget features here.';
        top = 340; // Approx below preview
        break;
      case 2:
        message = 'Then, choose a theme that fits your style.';
        top = 540; // Approx above themes
        break;
      case 3:
        message = 'Finally, tap here to see how to add it to your Home Screen.';
        bottom = 100;
        break;
    }

    return Material(
      color: Colors.black54,
      child: InkWell(
        onTap: () {
          setState(() {
            if (_tutorialStep < 3) {
              _tutorialStep++;
            } else {
              _tutorialStep = 0;
            }
          });
        },
        child: Stack(
          children: [
            Center(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 40),
                child: Column(
                  mainAxisAlignment: bottom != null
                      ? MainAxisAlignment.end
                      : MainAxisAlignment.start,
                  children: [
                    if (bottom == null) SizedBox(height: top),
                    Container(
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        color: bgDark,
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(color: primaryGold, width: 2),
                        boxShadow: [
                          BoxShadow(
                            color: primaryGold.withValues(alpha: 0.3),
                            blurRadius: 20,
                          ),
                        ],
                      ),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text(
                            message,
                            textAlign: TextAlign.center,
                            style: GoogleFonts.lexend(
                              color: Colors.white,
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(height: 16),
                          Text(
                            'Tap anywhere to continue',
                            style: GoogleFonts.lexend(
                              color: primaryGold.withValues(alpha: 0.7),
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                    ),
                    if (bottom != null) SizedBox(height: bottom),
                  ],
                ),
              ),
            ),
            Positioned(
              top: 50,
              right: 20,
              child: TextButton(
                onPressed: () => setState(() => _tutorialStep = 0),
                child: Text('Skip',
                    style: GoogleFonts.lexend(
                        color: Colors.white70, fontSize: 16)),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSmallWidgetPreview(Color primary, Color bg) {
    return Column(
      children: [
        Container(
          width: 150,
          height: 150,
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            color: bg,
            borderRadius: BorderRadius.circular(32),
            border: Border.all(color: Colors.white.withValues(alpha: 0.1)),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.3),
                blurRadius: 10,
                offset: const Offset(0, 5),
              ),
            ],
          ),
          child: Stack(
            children: [
              // Gradient Overlay
              Positioned.fill(
                child: DecoratedBox(
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                      colors: [
                        primary.withValues(alpha: 0.1),
                        Colors.transparent
                      ],
                    ),
                  ),
                ),
              ),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Icon(Icons.medication, color: primary, size: 20),
                      Container(
                        width: 30,
                        height: 30,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          border: Border.all(
                              color: primary.withValues(alpha: 0.3), width: 2),
                        ),
                        alignment: Alignment.center,
                        child: Container(
                          width: 14,
                          height: 14,
                          decoration: BoxDecoration(
                            color: primary,
                            shape: BoxShape.circle,
                          ),
                        ),
                      ),
                    ],
                  ),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '85%',
                        style: GoogleFonts.lexend(
                          color: Colors.white,
                          fontSize: 28,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      Text(
                        'Daily Goal',
                        style: GoogleFonts.lexend(
                          color: Colors.grey[400],
                          fontSize: 12,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ],
          ),
        ),
        const SizedBox(height: 12),
        const Text(
          'Small (2x2)',
          style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
        ),
        Text(
          'Compact summary',
          style: GoogleFonts.lexend(color: Colors.grey[600], fontSize: 12),
        ),
      ],
    );
  }

  Widget _buildMediumWidgetPreview(Color primary, Color bg) {
    return Column(
      children: [
        Container(
          width: 300,
          height: 150,
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            color: bg,
            borderRadius: BorderRadius.circular(32),
            border: Border.all(color: Colors.white.withValues(alpha: 0.1)),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.3),
                blurRadius: 10,
                offset: const Offset(0, 5),
              ),
            ],
          ),
          child: Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'UP NEXT',
                          style: GoogleFonts.lexend(
                            color: primary,
                            fontSize: 10,
                            fontWeight: FontWeight.bold,
                            letterSpacing: 1.0,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Text(
                          'Vitamin D3 + Omega 3',
                          style: GoogleFonts.lexend(
                            color: Colors.white,
                            fontSize: 28,
                            fontWeight: FontWeight.bold,
                            height: 1.1,
                          ),
                          maxLines: 2,
                        ),
                      ],
                    ),
                    Row(
                      children: [
                        Icon(Icons.schedule, color: Colors.grey[400], size: 16),
                        const SizedBox(width: 4),
                        Text(
                          '12:30 PM',
                          style: GoogleFonts.lexend(
                              color: Colors.grey[400], fontSize: 12),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 16),
              SizedBox(
                width: 70,
                height: 70,
                child: Stack(
                  alignment: Alignment.center,
                  children: [
                    CircularProgressIndicator(
                      value: 0.75,
                      strokeWidth: 6,
                      backgroundColor: Colors.grey[800],
                      valueColor: AlwaysStoppedAnimation<Color>(primary),
                    ),
                    Text(
                      '75%',
                      style: GoogleFonts.lexend(
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                        fontSize: 14,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 12),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16),
          child: Text(
            'Medium (4x2)',
            style: GoogleFonts.lexend(
                color: Colors.white, fontWeight: FontWeight.bold),
          ),
        ),
        Text(
          'Detailed schedule',
          style: GoogleFonts.lexend(color: Colors.grey[600], fontSize: 12),
        ),
      ],
    );
  }

  Widget _buildToggleRow({
    required IconData icon,
    required String title,
    required String subtitle,
    required bool value,
    required ValueChanged<bool> onChanged,
    required Color primaryGold,
  }) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: primaryGold.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Icon(icon, color: primaryGold, size: 20),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: GoogleFonts.lexend(
                    color: Colors.white,
                    fontWeight: FontWeight.w600,
                    fontSize: 15,
                  ),
                ),
                Text(
                  subtitle,
                  style: GoogleFonts.lexend(
                    color: Colors.grey[400],
                    fontSize: 12,
                  ),
                ),
              ],
            ),
          ),
          Switch(
            value: value,
            onChanged: onChanged,
            activeThumbColor: primaryGold,
            activeTrackColor: primaryGold.withValues(alpha: 0.5),
            inactiveThumbColor: Colors.grey[300],
            inactiveTrackColor: Colors.grey[700],
          ),
        ],
      ),
    );
  }

  Widget _buildThemeOption(String name, Color primary,
      {required Widget child, required bool isSelected}) {
    return GestureDetector(
      onTap: () => setState(() => _selectedTheme = name),
      child: Container(
        decoration: BoxDecoration(
          color: const Color(0xFF18181B),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(
            color: isSelected ? primary : Colors.transparent,
            width: 2,
          ),
        ),
        padding: const EdgeInsets.all(8),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Expanded(
              child: ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: SizedBox(
                  width: double.infinity,
                  child: child,
                ),
              ),
            ),
            const SizedBox(height: 8),
            Text(
              name,
              style: const TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.bold,
                fontSize: 12,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
