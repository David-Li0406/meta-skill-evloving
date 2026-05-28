import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'dart:async';
import '../../config/locator.dart';
import '../../application/view_models/nightly_reflection_view_model.dart';
import '../navigation/app_router.dart';
import '../../application/providers/auth_provider.dart';

class NightlyReflectionScreen extends StatefulWidget {
  const NightlyReflectionScreen({super.key});

  @override
  State<NightlyReflectionScreen> createState() =>
      _NightlyReflectionScreenState();
}

class _NightlyReflectionScreenState extends State<NightlyReflectionScreen> {
  NightlyReflectionViewModel? _viewModel;
  Timer? _debounceTimer;

  void _onJournalChanged() {
    if (_viewModel == null) return;

    _debounceTimer?.cancel();
    _debounceTimer = Timer(const Duration(seconds: 2), () async {
      final success = await _viewModel!.saveReflection(isAutoSave: true);
      if (success && mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Reflection saved'),
            backgroundColor: Color(0xFF7F06F9), // primaryPurple
            duration: Duration(milliseconds: 1000),
            behavior: SnackBarBehavior.floating,
            width: 200,
          ),
        );
      }
    });
  }

  @override
  void initState() {
    super.initState();
    // Defer initialization to build or post-frame where context is available
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (mounted) {
        final authProvider = context.read<AuthProvider>();
        final userId = authProvider.user?.id ?? '';
        setState(() {
          _viewModel = locator<NightlyReflectionViewModel>(param1: userId);
        });
        _viewModel?.loadTodayReflection().then((_) {
          // Add listener after loading initial data
          _viewModel?.journalController.addListener(_onJournalChanged);
        });
      }
    });
  }

  @override
  void dispose() {
    _debounceTimer?.cancel();
    _viewModel?.journalController.removeListener(_onJournalChanged);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // Hardcoded theme colors based on design
    const bgDark = Color(0xFF0C0812);
    const bgLight = Color(
        0xFFF7F5F8); // Fallback for light mode if needed, though design is dark heavy
    const primaryPurple = Color(0xFF7F06F9);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final scaffoldBg = isDark ? bgDark : bgLight;
    final textColor = isDark ? Colors.white : const Color(0xFF0F172A);
    final subTextColor =
        isDark ? Colors.white.withValues(alpha: 0.6) : const Color(0xFF475569);
    final cardBg = isDark
        ? Colors.white.withValues(alpha: 0.05)
        : Colors.white.withValues(alpha: 0.5);
    final cardBorder =
        isDark ? Colors.white.withValues(alpha: 0.1) : const Color(0xFFE2E8F0);

    // If ViewModel not initialized yet (waiting for post frame)
    if (_viewModel == null) {
      return Scaffold(backgroundColor: scaffoldBg, body: const SizedBox());
    }

    return ChangeNotifierProvider.value(
      value: _viewModel!,
      child: Consumer<NightlyReflectionViewModel>(
        builder: (context, viewModel, child) {
          if (viewModel.isSaving) {
            return Scaffold(
              backgroundColor: scaffoldBg,
              body: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const CircularProgressIndicator(color: primaryPurple),
                    const SizedBox(height: 16),
                    Text(
                      'Saving your reflection...',
                      style: TextStyle(color: textColor),
                    ),
                  ],
                ),
              ),
            );
          }

          return Scaffold(
            backgroundColor: scaffoldBg,
            body: Stack(
              children: [
                // Background Glows (Ambient)
                if (isDark) ...[
                  Positioned(
                    top: -100,
                    right: -100,
                    child: Container(
                      width: 300,
                      height: 300,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: primaryPurple.withValues(alpha: 0.15),
                        gradient: RadialGradient(
                          colors: [
                            primaryPurple.withValues(alpha: 0.2),
                            Colors.transparent
                          ],
                        ),
                      ),
                    ),
                  ),
                  Positioned(
                    bottom: -50,
                    left: -50,
                    child: Container(
                      width: 200,
                      height: 200,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        gradient: RadialGradient(
                          colors: [
                            primaryPurple.withValues(alpha: 0.1),
                            Colors.transparent
                          ],
                        ),
                      ),
                    ),
                  ),
                ],

                SafeArea(
                  child: Column(
                    children: [
                      // Header
                      Padding(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 16, vertical: 8),
                        child: Row(
                          children: [
                            Container(
                              width: 40,
                              height: 40,
                              decoration: BoxDecoration(
                                color: isDark
                                    ? Colors.white.withValues(alpha: 0.05)
                                    : Colors.black.withValues(alpha: 0.05),
                                shape: BoxShape.circle,
                              ),
                              child: IconButton(
                                icon: Icon(Icons.close,
                                    color: textColor, size: 20),
                                onPressed: () => Navigator.pop(context),
                              ),
                            ),
                            Expanded(
                              child: Text(
                                'Nightly Reflection',
                                textAlign: TextAlign.center,
                                style: TextStyle(
                                  color: textColor,
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                            const SizedBox(width: 40), // Balance
                          ],
                        ),
                      ),

                      if (viewModel.isLoading)
                        const Expanded(
                            child: Center(child: CircularProgressIndicator()))
                      else
                        Expanded(
                          child: SingleChildScrollView(
                            padding: const EdgeInsets.all(24),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.stretch,
                              children: [
                                const SizedBox(height: 16),
                                Text(
                                  'Time to rest, Alex',
                                  textAlign: TextAlign.center,
                                  style: TextStyle(
                                    color: textColor,
                                    fontSize: 32,
                                    fontWeight: FontWeight.bold,
                                    letterSpacing: -0.5,
                                  ),
                                ),
                                const SizedBox(height: 8),
                                Text(
                                  "Let's wind down for a peaceful night.",
                                  textAlign: TextAlign.center,
                                  style: TextStyle(
                                    color: subTextColor,
                                    fontSize: 16,
                                  ),
                                ),

                                const SizedBox(height: 40),

                                // Focus Section
                                Text(
                                  'How did your focus feel today?',
                                  style: TextStyle(
                                    color: textColor,
                                    fontSize: 18,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                const SizedBox(height: 16),
                                Container(
                                  padding: const EdgeInsets.all(24),
                                  decoration: BoxDecoration(
                                    color: cardBg,
                                    borderRadius: BorderRadius.circular(24),
                                    border: Border.all(color: cardBorder),
                                  ),
                                  child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.stretch,
                                    children: [
                                      Row(
                                        mainAxisAlignment:
                                            MainAxisAlignment.spaceBetween,
                                        children: [
                                          Text(
                                            'QUIET',
                                            style: TextStyle(
                                              color: subTextColor,
                                              fontSize: 12,
                                              fontWeight: FontWeight.w600,
                                              letterSpacing: 1.0,
                                            ),
                                          ),
                                          const Text(
                                            'HYPERFOCUSED',
                                            style: TextStyle(
                                              color: primaryPurple,
                                              fontSize: 12,
                                              fontWeight: FontWeight.w600,
                                              letterSpacing: 1.0,
                                            ),
                                          ),
                                        ],
                                      ),
                                      const SizedBox(height: 24),
                                      // Custom Slider
                                      SliderTheme(
                                        data: SliderTheme.of(context).copyWith(
                                          activeTrackColor: primaryPurple,
                                          inactiveTrackColor: isDark
                                              ? Colors.white
                                                  .withValues(alpha: 0.1)
                                              : Colors.grey[300],
                                          thumbColor: Colors.white,
                                          thumbShape:
                                              const RoundSliderThumbShape(
                                                  enabledThumbRadius: 12,
                                                  elevation: 4),
                                          overlayColor: primaryPurple
                                              .withValues(alpha: 0.2),
                                          trackHeight: 6,
                                        ),
                                        child: Slider(
                                          value: viewModel.focusValue,
                                          onChanged: viewModel.updateFocusValue,
                                        ),
                                      ),
                                      const SizedBox(height: 16),
                                      Text(
                                        _getFocusLabel(viewModel.focusValue),
                                        textAlign: TextAlign.center,
                                        style: TextStyle(
                                          color: subTextColor,
                                          fontSize: 14,
                                          fontStyle: FontStyle.italic,
                                        ),
                                      ),
                                    ],
                                  ),
                                ),

                                const SizedBox(height: 32),

                                // Journal Section
                                Text(
                                  "One thing you're proud of?",
                                  style: TextStyle(
                                    color: textColor,
                                    fontSize: 18,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                const SizedBox(height: 16),
                                Container(
                                  height: 140,
                                  padding: const EdgeInsets.all(20),
                                  decoration: BoxDecoration(
                                    color: cardBg,
                                    borderRadius: BorderRadius.circular(24),
                                    border: Border.all(color: cardBorder),
                                  ),
                                  child: Stack(
                                    children: [
                                      TextField(
                                        controller: viewModel.journalController,
                                        maxLines: null,
                                        expands: true,
                                        textAlignVertical:
                                            TextAlignVertical.top,
                                        style: TextStyle(
                                            color: textColor, fontSize: 16),
                                        decoration: InputDecoration(
                                          border: InputBorder.none,
                                          hintText:
                                              'A small win, a moment of clarity, or just showing up...',
                                          hintStyle: TextStyle(
                                              color: subTextColor.withValues(
                                                  alpha: 0.5)),
                                          contentPadding:
                                              const EdgeInsets.only(bottom: 32),
                                        ),
                                      ),
                                      Positioned(
                                        bottom: 0,
                                        right: 0,
                                        child: GestureDetector(
                                          onTap: () {
                                            ScaffoldMessenger.of(context)
                                                .showSnackBar(
                                              const SnackBar(
                                                  content: Text(
                                                      'Voice recording coming soon!')),
                                            );
                                          },
                                          child: Icon(Icons.mic,
                                              color: subTextColor, size: 24),
                                        ),
                                      ),
                                    ],
                                  ),
                                ),

                                const SizedBox(height: 32),

                                // Sleep Ready Section
                                Container(
                                  padding: const EdgeInsets.all(20),
                                  decoration: BoxDecoration(
                                    color: primaryPurple.withValues(alpha: 0.1),
                                    borderRadius: BorderRadius.circular(24),
                                    border: Border.all(
                                        color: primaryPurple.withValues(
                                            alpha: 0.2)),
                                  ),
                                  child: Row(
                                    children: [
                                      Container(
                                        width: 40,
                                        height: 40,
                                        decoration: BoxDecoration(
                                          color: primaryPurple.withValues(
                                              alpha: 0.2),
                                          shape: BoxShape.circle,
                                        ),
                                        child: const Icon(Icons.bedtime,
                                            color: primaryPurple, size: 20),
                                      ),
                                      const SizedBox(width: 16),
                                      Expanded(
                                        child: Column(
                                          crossAxisAlignment:
                                              CrossAxisAlignment.start,
                                          children: [
                                            Text(
                                              'Sleep Ready',
                                              style: TextStyle(
                                                color: textColor,
                                                fontSize: 16,
                                                fontWeight: FontWeight.bold,
                                              ),
                                            ),
                                            Text(
                                              'Dim interface & mute alerts',
                                              style: TextStyle(
                                                color: subTextColor,
                                                fontSize: 12,
                                              ),
                                            ),
                                          ],
                                        ),
                                      ),
                                      Switch(
                                        value: viewModel.isSleepReady,
                                        onChanged: viewModel.toggleSleepReady,
                                        activeThumbColor: primaryPurple,
                                        activeTrackColor: primaryPurple
                                            .withValues(alpha: 0.5),
                                      ),
                                    ],
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),

                      // Footer buttons
                      Container(
                        padding: const EdgeInsets.all(24),
                        decoration: BoxDecoration(
                          gradient: LinearGradient(
                            begin: Alignment.bottomCenter,
                            end: Alignment.topCenter,
                            colors: [
                              scaffoldBg,
                              scaffoldBg.withValues(alpha: 0),
                            ],
                          ),
                        ),
                        child: Column(
                          children: [
                            SizedBox(
                              width: double.infinity,
                              height: 64,
                              child: ElevatedButton(
                                onPressed: () {
                                  // Navigate to Daily Stack screen filtered for Evening
                                  Navigator.pushNamed(
                                    context,
                                    AppRouter.dailyStack,
                                    arguments: {'filter': 'Evening'},
                                  );
                                },
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: primaryPurple,
                                  foregroundColor: Colors.white,
                                  elevation: 8,
                                  shadowColor:
                                      primaryPurple.withValues(alpha: 0.3),
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(32),
                                  ),
                                ),
                                child: const Row(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: [
                                    Icon(Icons.medication),
                                    SizedBox(width: 12),
                                    Text(
                                      'Take Evening Stack',
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                            const SizedBox(height: 12),
                            SizedBox(
                              width: double.infinity,
                              height: 64,
                              child: TextButton(
                                onPressed: () async {
                                  final success =
                                      await viewModel.saveReflection();
                                  if (success && context.mounted) {
                                    Navigator.pop(context);
                                    ScaffoldMessenger.of(context).showSnackBar(
                                      const SnackBar(
                                        content: Text(
                                            'Nightly reflection saved. Sleep well!'),
                                        backgroundColor: primaryPurple,
                                        behavior: SnackBarBehavior.floating,
                                      ),
                                    );
                                  }
                                },
                                style: TextButton.styleFrom(
                                  foregroundColor: subTextColor,
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(32),
                                    side: BorderSide(color: cardBorder),
                                  ),
                                ),
                                child: const Text(
                                  'Save & Close',
                                  style: TextStyle(
                                    fontSize: 16,
                                    fontWeight: FontWeight.w600,
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  String _getFocusLabel(double value) {
    if (value < 0.2) return '"I tried my best, but struggled"';
    if (value < 0.4) return '"It was a bit shaky today"';
    if (value < 0.6) return '"I felt mostly balanced today"';
    if (value < 0.8) return '"I was really dialed in!"';
    return '"Hyperfocused machine mode!"';
  }
}
