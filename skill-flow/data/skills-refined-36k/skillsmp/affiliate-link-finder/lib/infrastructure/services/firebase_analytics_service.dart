import 'package:adhd_supplement_app/domain/services/analytics_service.dart';
import '../../utils/logger.dart';
import 'package:firebase_analytics/firebase_analytics.dart';

class FirebaseAnalyticsService implements AnalyticsService {
  final FirebaseAnalytics _analytics = FirebaseAnalytics.instance;

  @override
  Future<void> logEvent(String name, {Map<String, dynamic>? parameters}) async {
    AppLogger.d('Analytics: Log Event -> $name, Params: $parameters');
    await _analytics.logEvent(name: name, parameters: parameters);
  }

  @override
  Future<void> logScreenView(String screenName) async {
    AppLogger.d('Analytics: Screen View -> $screenName');
    await _analytics.logEvent(
      name: 'screen_view',
      parameters: {'screen_name': screenName},
    );
  }

  @override
  Future<void> setUserId(String userId) async {
    AppLogger.d('Analytics: Set User ID -> $userId');
    await _analytics.setUserId(id: userId);
  }

  @override
  Future<void> setUserProperty(String name, String value) async {
    AppLogger.d('Analytics: Set User Property -> $name : $value');
    await _analytics.setUserProperty(name: name, value: value);
  }
}
