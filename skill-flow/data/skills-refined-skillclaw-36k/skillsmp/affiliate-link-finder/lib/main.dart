import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import 'package:provider/provider.dart';
import 'config/locator.dart';
import 'presentation/theme/app_theme.dart';
import 'presentation/navigation/app_router.dart';
import 'application/providers/auth_provider.dart';
import 'application/view_models/supplement_view_model.dart';
import 'application/view_models/safety_view_model.dart';
import 'application/view_models/persistent_reminders_view_model.dart';
import 'firebase_options.dart';
import 'application/view_models/theme_view_model.dart';
import 'utils/logger.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  bool firebaseInitialized = false;
  String? initializationError;

  // Initialize Firebase with error handling
  try {
    // Note: On web, this requires firebase_options.dart or manual configuration
    await Firebase.initializeApp(
      options: DefaultFirebaseOptions.currentPlatform,
    );
    firebaseInitialized = true;
    AppLogger.i('Firebase initialized successfully');

    // Initialize Crashlytics (disabled in debug mode)
    if (!kDebugMode) {
      FlutterError.onError =
          FirebaseCrashlytics.instance.recordFlutterFatalError;
      // Pass all uncaught asynchronous errors to Crashlytics
      PlatformDispatcher.instance.onError = (error, stack) {
        FirebaseCrashlytics.instance.recordError(error, stack, fatal: true);
        return true;
      };
    }
  } catch (e) {
    AppLogger.e('Firebase initialization error', e);
    initializationError = e.toString();
  }

  // Setup Dependency Injection only if Firebase is ready OR if we can handle the lack of it
  if (firebaseInitialized) {
    try {
      await setupLocator();
      // Services will be initialized in SplashScreen to improve startup time
    } catch (e) {
      AppLogger.e('Locator/Init setup error', e);
      initializationError ??= 'Setup error: $e';
    }
  }

  runApp(AdhdSupplementApp(
    isFirebaseReady: firebaseInitialized,
    initError: initializationError,
  ));
}

class AdhdSupplementApp extends StatelessWidget {
  final bool isFirebaseReady;
  final String? initError;

  const AdhdSupplementApp({
    super.key,
    required this.isFirebaseReady,
    this.initError,
  });

  @override
  Widget build(BuildContext context) {
    if (!isFirebaseReady) {
      return MaterialApp(
        debugShowCheckedModeBanner: false,
        theme: AppTheme.lightTheme,
        home: _FirebaseErrorScreen(errorMessage: initError),
      );
    }

    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => locator<SupplementViewModel>()),
        ChangeNotifierProvider(create: (_) => locator<AuthProvider>()),
        ChangeNotifierProxyProvider<AuthProvider, SafetyViewModel>(
          create: (_) => locator<SafetyViewModel>(param1: 'demo_user'),
          update: (_, auth, previous) =>
              locator<SafetyViewModel>(param1: auth.user?.id ?? 'demo_user'),
        ),
        ChangeNotifierProvider(
            create: (_) => locator<PersistentRemindersViewModel>()),
        ChangeNotifierProvider(create: (_) => locator<ThemeViewModel>()),
      ],
      child: Consumer<ThemeViewModel>(
        builder: (context, themeVM, _) => MaterialApp(
          title: 'Daily Stack',
          theme: AppTheme.lightTheme,
          darkTheme: AppTheme.darkTheme,
          initialRoute: AppRouter.splash,
          onGenerateInitialRoutes: (initialRoute) {
            return [
              AppRouter.generateRoute(RouteSettings(
                name: AppRouter.splash,
                arguments: {
                  'isFirebaseReady': isFirebaseReady,
                  'initError': initError,
                },
              )),
            ];
          },
          onGenerateRoute: AppRouter.generateRoute,
          builder: (context, child) {
            final scale = themeVM.fontScale;
            return MediaQuery(
              data: MediaQuery.of(context).copyWith(
                textScaler: TextScaler.linear(scale),
              ),
              child: child!,
            );
          },
        ),
      ),
    );
  }
}

class _FirebaseErrorScreen extends StatelessWidget {
  final String? errorMessage;

  const _FirebaseErrorScreen({this.errorMessage});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(
                Icons.cloud_off_rounded,
                size: 80,
                color: Color(0xFF6C63FF),
              ),
              const SizedBox(height: 24),
              const Text(
                'Connection Issue',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF2D3142),
                ),
              ),
              const SizedBox(height: 12),
              const Text(
                'We couldn\'t connect to our services. This might be due to a poor connection or maintenance.',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 16,
                  color: Color(0xFF9094A6),
                ),
              ),
              if (errorMessage != null && kDebugMode) ...[
                const SizedBox(height: 24),
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.red.withValues(alpha: 0.05),
                    borderRadius: BorderRadius.circular(8),
                    border:
                        Border.all(color: Colors.red.withValues(alpha: 0.1)),
                  ),
                  child: Text(
                    'Error: $errorMessage',
                    style: const TextStyle(
                      fontFamily: 'monospace',
                      fontSize: 12,
                      color: Colors.red,
                    ),
                  ),
                ),
              ],
              const SizedBox(height: 32),
              ElevatedButton(
                onPressed: () {
                  // This is a simple way to "restart" the app in Flutter
                  // For a real app, you might want more complex logic
                  // but for a fix, this is a clean way to retry.
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF6C63FF),
                  padding:
                      const EdgeInsets.symmetric(horizontal: 32, vertical: 12),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                child: const Text(
                  'Try Again',
                  style: TextStyle(color: Colors.white),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
