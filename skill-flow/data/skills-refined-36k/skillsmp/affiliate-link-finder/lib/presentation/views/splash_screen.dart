import 'package:flutter/material.dart';
import '../../config/locator.dart';
import '../../domain/repositories/settings_repository.dart';
import '../../infrastructure/services/notification_service.dart';
import '../../infrastructure/services/seeding_service.dart';
import '../../domain/repositories/supplement_repository.dart';
import '../../utils/logger.dart';
import '../navigation/app_router.dart';
import '../theme/app_theme.dart';

class SplashScreen extends StatefulWidget {
  final bool isFirebaseReady;
  final String? initError;

  const SplashScreen({
    super.key,
    required this.isFirebaseReady,
    this.initError,
  });

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;
  String _loadingStatus = 'Initializing...';

  @override
  void initState() {
    super.initState();
    _controller =
        AnimationController(duration: const Duration(seconds: 2), vsync: this)
          ..repeat(reverse: true);
    _animation = CurvedAnimation(parent: _controller, curve: Curves.easeInOut);

    if (widget.isFirebaseReady) {
      _initializeApp();
    } else {
      // If Firebase failed, we can't really proceed with normal app flow,
      // but we might want to show the error screen logic handled in main.dart
      // For now, let's just log it.
      setState(() => _loadingStatus = 'Connection Error: ${widget.initError}');
    }
  }

  Future<void> _initializeApp() async {
    try {
      // 0. Seeding (Background - start as soon as Firebase is ready)
      _runBackgroundSeeding(); // Fire and forget

      // 1. Settings
      setState(() => _loadingStatus = 'Loading preferences...');
      await locator<SettingsRepository>()
          .init()
          .timeout(const Duration(seconds: 3));

      // 2. Notifications
      setState(() => _loadingStatus = 'Setting up reminders...');
      await locator<NotificationService>()
          .init()
          .timeout(const Duration(seconds: 5))
          .catchError((Object e) {
        AppLogger.w('Notification initialization timed out or failed', e);
      });

      // Minimum splash time for branding impact (optional)
      await Future<void>.delayed(const Duration(milliseconds: 1500));

      if (mounted) {
        // Navigate to Home (AuthWrapper)
        Navigator.of(context).pushReplacementNamed(AppRouter.home);
      }
    } catch (e) {
      AppLogger.e('Initialization failed during Splash', e);
      // Proceed anyway, maybe in offline mode
      if (mounted) {
        Navigator.of(context).pushReplacementNamed(AppRouter.home);
      }
    } finally {
      // Cancel any pending timers
      _controller.stop();
    }
  }

  void _runBackgroundSeeding() {
    // This runs in parallel
    final seeding = locator<SeedingService>();
    seeding.createTestUser('test@daily-stack.com', 'password123');

    seeding.seedSupplements().timeout(const Duration(seconds: 5)).then((_) {
      // Pre-fetch supplements into cache
      locator<SupplementRepository>().getAllSupplements();
    }).catchError((Object e) {
      AppLogger.w('Background task warning', e);
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.backgroundLight,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Logo / Branding
            ScaleTransition(
              scale: Tween<double>(begin: 0.9, end: 1.1).animate(_animation),
              child: Container(
                width: 120,
                height: 120,
                decoration: const BoxDecoration(
                    shape: BoxShape.circle,
                    color: AppColors.primaryGold,
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black12,
                        blurRadius: 20,
                        spreadRadius: 5,
                      )
                    ]),
                child: const Icon(
                  Icons.bolt,
                  size: 60,
                  color: Colors.white,
                ),
              ),
            ),
            const SizedBox(height: 40),
            // Status Text
            Text(
              _loadingStatus,
              style: const TextStyle(
                color: Colors.grey,
                fontSize: 16,
                fontWeight: FontWeight.w500,
                letterSpacing: 0.5,
              ),
            ),
            const SizedBox(height: 20),
            // Subtle progress indicator
            const SizedBox(
              width: 100,
              child: LinearProgressIndicator(
                backgroundColor: Colors.black12,
                valueColor:
                    AlwaysStoppedAnimation<Color>(AppColors.primaryGold),
                minHeight: 2,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
