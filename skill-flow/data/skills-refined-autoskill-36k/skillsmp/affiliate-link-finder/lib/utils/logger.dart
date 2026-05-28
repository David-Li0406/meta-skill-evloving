import 'package:flutter/foundation.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';

/// Centralized logger for the application.
/// Wraps debugPrint to ensure logs are only shown in debug mode
/// and provides a consistent structure for logging.
class AppLogger {
  // Prevent instantiation
  AppLogger._();

  /// Logs a debug message.
  static void d(String message, [dynamic error, StackTrace? stackTrace]) {
    if (kDebugMode) {
      debugPrint(
          '🐛 [DEBUG] ${DateTime.now().toIso8601String().split('T').last} | $message');
      if (error != null) debugPrint('   Error: $error');
      if (stackTrace != null) debugPrint('   Stack: $stackTrace');
    }
  }

  /// Logs an info message.
  static void i(String message) {
    if (kDebugMode) {
      debugPrint(
          'ℹ️ [INFO] ${DateTime.now().toIso8601String().split('T').last} | $message');
    }
  }

  /// Logs a warning message.
  static void w(String message, [dynamic error]) {
    if (kDebugMode) {
      debugPrint(
          '⚠️ [WARN] ${DateTime.now().toIso8601String().split('T').last} | $message');
      if (error != null) debugPrint('   Error: $error');
    } else {
      // Log to Crashlytics in production (if available)
      try {
        FirebaseCrashlytics.instance.log('WARN: $message ${error ?? ''}');
      } catch (_) {
        // Firebase not initialized
      }
    }
  }

  /// Logs an error message.
  static void e(String message, [dynamic error, StackTrace? stackTrace]) {
    // Always print errors locally in debug
    if (kDebugMode) {
      debugPrint(
          '❌ [ERROR] ${DateTime.now().toIso8601String().split('T').last} | $message');
      if (error != null) debugPrint('   Error: $error');
      if (stackTrace != null) debugPrint('   Stack: $stackTrace');
    }

    // Send errors to Crashlytics in production (if available)
    if (!kDebugMode) {
      try {
        FirebaseCrashlytics.instance.recordError(
          error ?? message,
          stackTrace,
          reason: message,
          fatal: false,
        );
      } catch (_) {
        // Firebase not initialized
      }
    }
  }
}
