import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import '../../domain/entities/daily_log.dart';
import '../../domain/repositories/log_repository.dart';
import '../../utils/date_utils.dart';
import '../../utils/logger.dart';

class FirebaseLogRepository implements LogRepository {
  final FirebaseFirestore _firestore;
  final SharedPreferences? _prefs;

  // In-memory cache: "userId_dateStr" -> DailyLog
  final Map<String, DailyLog> _memoryCache = {};

  // Local storage key prefix
  static const String _spPrefix = 'log_cache_';

  FirebaseLogRepository(
      {FirebaseFirestore? firestore, SharedPreferences? prefs})
      : _firestore = firestore ?? FirebaseFirestore.instance,
        _prefs = prefs;

  @override
  Future<List<DailyLog>> getLogsByDateRange(
      String userId, DateTime start, DateTime end) async {
    try {
      final snapshot = await _firestore
          .collection('logs')
          .where('userId', isEqualTo: userId)
          .where('date', isGreaterThanOrEqualTo: start.toIso8601String())
          .where('date', isLessThanOrEqualTo: end.toIso8601String())
          .orderBy('date', descending: true)
          .get(const GetOptions(source: Source.serverAndCache))
          .timeout(const Duration(seconds: 3));

      return snapshot.docs
          .map((doc) => DailyLog.fromJson({...doc.data(), 'id': doc.id}))
          .toList();
    } catch (e) {
      AppLogger.w('Fetching logs from cache (offline)', e);
      try {
        final snapshot = await _firestore
            .collection('logs')
            .where('userId', isEqualTo: userId)
            .where('date', isGreaterThanOrEqualTo: start.toIso8601String())
            .where('date', isLessThanOrEqualTo: end.toIso8601String())
            .get(const GetOptions(source: Source.cache));
        return snapshot.docs
            .map((doc) => DailyLog.fromJson({...doc.data(), 'id': doc.id}))
            .toList();
      } catch (cacheErr) {
        AppLogger.e('Log cache failure', cacheErr);
        return [];
      }
    }
  }

  @override
  Future<DailyLog?> getLogForDate(String userId, DateTime date) async {
    try {
      final dateStr = _dateOnlyString(date);
      final cacheKey = '${userId}_$dateStr';

      // 1. Check Memory Cache
      if (_memoryCache.containsKey(cacheKey)) {
        AppLogger.d('Returning log from memory cache (0ms)');
        return _memoryCache[cacheKey];
      }

      // 2. Check SharedPreferences Cache (Survivability through restarts)
      if (_prefs != null) {
        final localData = _prefs!.getString('$_spPrefix$cacheKey');
        if (localData != null) {
          try {
            final log = DailyLog.fromJson(
                jsonDecode(localData) as Map<String, dynamic>);
            _memoryCache[cacheKey] = log;
            AppLogger.d('Returning log from local SharedPreferences (5ms)');
            return log;
          } catch (e) {
            AppLogger.w('Failed to decode local log cache', e);
          }
        }
      }

      final snapshot = await _firestore
          .collection('logs')
          .where('userId', isEqualTo: userId)
          .where('date', isEqualTo: dateStr)
          .limit(1)
          .get(const GetOptions(source: Source.serverAndCache))
          .timeout(const Duration(seconds: 3));

      if (snapshot.docs.isEmpty) return null;

      final log = DailyLog.fromJson(
          {...snapshot.docs.first.data(), 'id': snapshot.docs.first.id});

      // Update Caches
      _updateLocalCache(cacheKey, log);
      return log;
    } catch (e) {
      AppLogger.w('Fetching log for date from cache', e);
      try {
        final dateStr = _dateOnlyString(date);
        final snapshot = await _firestore
            .collection('logs')
            .where('userId', isEqualTo: userId)
            .where('date', isEqualTo: dateStr)
            .limit(1)
            .get(const GetOptions(source: Source.cache));
        if (snapshot.docs.isEmpty) return null;
        return DailyLog.fromJson(
            {...snapshot.docs.first.data(), 'id': snapshot.docs.first.id});
      } catch (cacheErr) {
        AppLogger.e('Log date cache failure', cacheErr);
        return null;
      }
    }
  }

  @override
  Future<void> saveLog(DailyLog log) async {
    final dateStr = _dateOnlyString(log.date);
    final cacheKey = '${log.userId}_$dateStr';

    // 1. Immediate local persistence for maximum reliability
    _updateLocalCache(cacheKey, log);

    try {
      if (log.id.isEmpty) {
        await _firestore.collection('logs').add(log.toJson());
      } else {
        await _firestore.collection('logs').doc(log.id).set(log.toJson());
      }
    } catch (e) {
      AppLogger.e('Error saving log to Firestore', e);
      // We don't throw here if we have local persistence, as it satisfies the immediate need
      // but we log it for debug.
    }
  }

  void _updateLocalCache(String key, DailyLog log) {
    _memoryCache[key] = log;
    if (_prefs != null) {
      _prefs!.setString('$_spPrefix$key', jsonEncode(log.toJson()));
    }
  }

  @override
  Future<int> getStreakCount(String userId) async {
    try {
      // Get recent logs ordered by date descending
      final logs = await getRecentLogs(userId, 90); // Check last 90 days

      if (logs.isEmpty) return 0;

      int streak = 0;
      DateTime checkDate = DateTime.now();

      for (final log in logs) {
        final logDate = log.date;
        final daysDiff = checkDate.difference(logDate).inDays;

        // Check if this log is for yesterday or the current streak date
        if (daysDiff == streak || (streak == 0 && daysDiff == 0)) {
          // Check if at least one supplement was taken
          final hasTaken =
              log.entries.any((entry) => entry.status == LogStatus.taken);
          if (hasTaken) {
            streak++;
            checkDate = logDate.subtract(const Duration(days: 1));
          } else {
            break; // Streak broken
          }
        } else {
          break; // Gap in dates
        }
      }

      return streak;
    } catch (e) {
      AppLogger.w('Failed to calculate streak (likely offline)', e);
      return 0;
    }
  }

  @override
  Future<List<DailyLog>> getRecentLogs(String userId, int days) async {
    try {
      final startDate = DateTime.now().subtract(Duration(days: days));
      return getLogsByDateRange(userId, startDate, DateTime.now());
    } catch (e) {
      throw Exception('Failed to fetch recent logs: $e');
    }
  }

  @override
  Stream<DailyLog?> watchTodayLog(String userId) {
    // Use logical date (4 AM rollover) instead of raw DateTime.now()
    final today = getLogicalDateString();

    return _firestore
        .collection('logs')
        .where('userId', isEqualTo: userId)
        .where('date', isEqualTo: today)
        .limit(1)
        .snapshots()
        .map((snapshot) {
      if (snapshot.docs.isEmpty) return null;
      return DailyLog.fromJson(
          {...snapshot.docs.first.data(), 'id': snapshot.docs.first.id});
    });
  }

  @override
  Future<void> clearAllLogs(String userId) async {
    try {
      final batch = _firestore.batch();
      final snapshots = await _firestore
          .collection('logs')
          .where('userId', isEqualTo: userId)
          .get();

      for (var doc in snapshots.docs) {
        batch.delete(doc.reference);
      }

      await batch.commit();
    } catch (e) {
      throw Exception('Failed to clear logs: $e');
    }
  }

  String _dateOnlyString(DateTime date) {
    return DateTime(date.year, date.month, date.day)
        .toIso8601String()
        .split('T')
        .first;
  }
}
