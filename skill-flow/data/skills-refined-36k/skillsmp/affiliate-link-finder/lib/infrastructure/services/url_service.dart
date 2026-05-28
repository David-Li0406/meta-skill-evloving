import 'package:url_launcher/url_launcher.dart';
import '../../utils/logger.dart';

typedef UrlLauncherFunc = Future<bool> Function(Uri url, {LaunchMode mode});

class UrlService {
  final UrlLauncherFunc? _launcher;

  UrlService({UrlLauncherFunc? launcher}) : _launcher = launcher;

  Future<bool> _launch(Uri url,
      {LaunchMode mode = LaunchMode.platformDefault}) async {
    if (_launcher != null) {
      return _launcher!(url, mode: mode);
    }
    return launchUrl(url, mode: mode);
  }

  /// Launches a referral link in an external browser.
  Future<void> launchReferral(String url) async {
    try {
      final Uri uri = Uri.parse(url);
      if (!await _launch(uri, mode: LaunchMode.externalApplication)) {
        AppLogger.e('Could not launch referral URL: $url');
        throw Exception('Could not launch $url');
      }
    } catch (e) {
      AppLogger.e('Error launching referral URL: $url', e);
      rethrow;
    }
  }

  /// Launches a scientific research link in an in-app browser view.
  /// Falls back to external browser if in-app view is unavailable.
  Future<void> launchInAppBrowser(String url) async {
    final Uri uri = Uri.parse(url);
    try {
      // Attempt in-app browser first for premium feel
      final bool launched = await _launch(
        uri,
        mode: LaunchMode.inAppBrowserView,
      );

      if (!launched) {
        AppLogger.w(
            'In-app browser failed to launch for $url, trying external...');
        await _launch(uri, mode: LaunchMode.externalApplication);
      }
    } catch (e) {
      AppLogger.e('In-app browser crash for $url, attempting fallback...', e);
      try {
        await _launch(uri, mode: LaunchMode.externalApplication);
      } catch (innerError) {
        AppLogger.e('Final fallback failed for $url', innerError);
        rethrow;
      }
    }
  }

  /// Generic URI launch with platform default.
  Future<void> launchUri(String url) async {
    try {
      final Uri uri = Uri.parse(url);
      if (!await _launch(uri, mode: LaunchMode.platformDefault)) {
        throw Exception('Could not launch $url');
      }
    } catch (e) {
      AppLogger.e('Error launching URI: $url', e);
      rethrow;
    }
  }
}
