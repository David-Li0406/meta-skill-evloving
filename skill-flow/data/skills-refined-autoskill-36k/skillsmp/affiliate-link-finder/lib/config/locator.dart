import 'package:get_it/get_it.dart';
import 'package:shared_preferences/shared_preferences.dart';

// --- Domain ---
import 'package:adhd_supplement_app/domain/repositories/auth_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/supplement_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/stack_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/log_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/symptom_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/streak_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/gamification_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/safety_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/settings_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/article_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/community_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/referral_repository.dart';
import 'package:adhd_supplement_app/domain/services/billing_service.dart';
import 'package:adhd_supplement_app/domain/services/interaction_service.dart';
import 'package:adhd_supplement_app/domain/services/analytics_service.dart';

// --- Infrastructure ---
import 'package:adhd_supplement_app/infrastructure/repositories/firebase_auth_repository.dart';
import 'package:adhd_supplement_app/infrastructure/repositories/firebase_supplement_repository.dart';
import 'package:adhd_supplement_app/infrastructure/repositories/firebase_stack_repository.dart';
import 'package:adhd_supplement_app/infrastructure/repositories/firebase_log_repository.dart';
import 'package:adhd_supplement_app/infrastructure/repositories/firebase_symptom_repository.dart';
import 'package:adhd_supplement_app/infrastructure/repositories/firebase_streak_repository.dart';
import 'package:adhd_supplement_app/infrastructure/repositories/firebase_gamification_repository.dart';
import 'package:adhd_supplement_app/infrastructure/repositories/firebase_safety_repository.dart';
import 'package:adhd_supplement_app/infrastructure/repositories/firebase_article_repository.dart';
import 'package:adhd_supplement_app/infrastructure/repositories/firebase_community_repository.dart';
import 'package:adhd_supplement_app/infrastructure/repositories/firebase_referral_repository.dart';
import 'package:adhd_supplement_app/infrastructure/repositories/perplexity_repository.dart';
import 'package:adhd_supplement_app/infrastructure/repositories/shared_prefs_settings_repository.dart';
import 'package:adhd_supplement_app/infrastructure/services/revenue_cat_billing_service.dart';
import 'package:adhd_supplement_app/infrastructure/services/fda_interaction_service.dart';
import 'package:adhd_supplement_app/infrastructure/services/firebase_analytics_service.dart';
import 'package:adhd_supplement_app/infrastructure/services/notification_service.dart';
import 'package:adhd_supplement_app/infrastructure/services/streak_service.dart';
import 'package:adhd_supplement_app/infrastructure/services/url_service.dart';
import 'package:adhd_supplement_app/infrastructure/services/sound_service.dart';
import 'package:adhd_supplement_app/infrastructure/services/report_pdf_service.dart';
import 'package:adhd_supplement_app/infrastructure/services/seeding_service.dart';
import 'package:adhd_supplement_app/infrastructure/services/perplexity_service.dart';

// --- Application ---
import 'package:adhd_supplement_app/application/providers/auth_provider.dart';
import 'package:adhd_supplement_app/application/services/haptic_service.dart';
import 'package:adhd_supplement_app/application/view_models/supplement_view_model.dart';
import 'package:adhd_supplement_app/application/view_models/safety_view_model.dart';
import 'package:adhd_supplement_app/application/view_models/symptom_checkin_viewmodel.dart';
import 'package:adhd_supplement_app/application/view_models/subscription_view_model.dart';
import 'package:adhd_supplement_app/application/view_models/privacy_view_model.dart';
import 'package:adhd_supplement_app/application/view_models/notification_history_view_model.dart';
import 'package:adhd_supplement_app/application/view_models/persistent_reminders_view_model.dart';
import 'package:adhd_supplement_app/application/view_models/focus_buddies_view_model.dart';
import 'package:adhd_supplement_app/application/view_models/trophy_room_view_model.dart';
import 'package:adhd_supplement_app/application/view_models/community_view_model.dart';
import 'package:adhd_supplement_app/application/view_models/history_log_view_model.dart';
import 'package:adhd_supplement_app/application/view_models/article_detail_view_model.dart';
import 'package:adhd_supplement_app/application/view_models/science_hub_view_model.dart';
import 'package:adhd_supplement_app/application/view_models/refer_friend_view_model.dart';
import 'package:adhd_supplement_app/application/view_models/nightly_reflection_view_model.dart';
import 'package:adhd_supplement_app/application/view_models/doctor_export_view_model.dart';
import 'package:adhd_supplement_app/application/view_models/chemist_view_model.dart';
import 'package:adhd_supplement_app/application/view_models/theme_view_model.dart';
import 'package:adhd_supplement_app/application/view_models/insights_view_model.dart';
import 'package:adhd_supplement_app/application/view_models/global_search_view_model.dart';
import 'package:adhd_supplement_app/application/view_models/pill_matcher_view_model.dart';

// --- Presentation ---
import 'package:adhd_supplement_app/presentation/view_models/daily_stack_view_model.dart';
import 'package:adhd_supplement_app/presentation/view_models/library_view_model.dart';
import 'package:adhd_supplement_app/presentation/view_models/stack_builder_view_model.dart';

final locator = GetIt.instance;

Future<void> setupLocator() async {
  final prefs = await SharedPreferences.getInstance();

  _setupCore(prefs);
  _setupInfrastructure(prefs);
  _setupApplication();
  _setupViewModels();
}

void _setupCore(SharedPreferences prefs) {
  locator.registerLazySingleton<SettingsRepository>(
      () => SharedPrefsSettingsRepository(prefs));
  locator.registerLazySingleton<HapticService>(() => HapticService());
  locator.registerLazySingleton<SoundService>(() => SoundService());
  locator.registerLazySingleton<UrlService>(() => UrlService());
  locator.registerLazySingleton<ReportPdfService>(() => ReportPdfService());
  locator.registerLazySingleton<SeedingService>(() => SeedingService());
}

void _setupInfrastructure(SharedPreferences prefs) {
  // Services
  locator
      .registerLazySingleton<BillingService>(() => RevenueCatBillingService());
  locator.registerLazySingleton<AnalyticsService>(
      () => FirebaseAnalyticsService());
  locator
      .registerLazySingleton<NotificationService>(() => NotificationService());
  locator
      .registerLazySingleton<InteractionService>(() => FDAInteractionService());
  locator.registerLazySingleton<StreakService>(() => StreakService());
  locator.registerLazySingleton<PerplexityService>(() => PerplexityService());

  // Repositories
  locator.registerLazySingleton<AuthRepository>(() => FirebaseAuthRepository());
  locator.registerLazySingleton<SupplementRepository>(
      () => FirebaseSupplementRepository());
  locator
      .registerLazySingleton<StackRepository>(() => FirebaseStackRepository());
  locator.registerLazySingleton<LogRepository>(
      () => FirebaseLogRepository(prefs: prefs));
  locator.registerLazySingleton<SymptomRepository>(
      () => FirebaseSymptomRepository());
  locator.registerLazySingleton<StreakRepository>(
      () => FirebaseStreakRepository());
  locator.registerLazySingleton<GamificationRepository>(
      () => FirebaseGamificationRepository());
  locator.registerLazySingleton<SafetyRepository>(
      () => FirebaseSafetyRepository());
  locator
      .registerLazySingleton<ArticleRepository>(() => FirebaseArticleRepository(
            perplexityService: locator<PerplexityService>(),
          ));
  locator.registerLazySingleton<CommunityRepository>(
      () => FirebaseCommunityRepository());
  locator.registerLazySingleton<ReferralRepository>(
      () => FirebaseReferralRepository());
  locator.registerLazySingleton<PerplexityRepository>(
      () => PerplexityRepositoryImpl(locator<PerplexityService>()));
}

void _setupApplication() {
  locator.registerLazySingleton(
      () => AuthProvider(locator<AuthRepository>(), locator<BillingService>()));
}

void _setupViewModels() {
  // Singleton ViewModels
  locator.registerLazySingleton(
      () => ThemeViewModel(locator<SettingsRepository>()));
  locator.registerFactory(() => SubscriptionViewModel());
  locator.registerFactory(() => PillMatcherViewModel());
  locator.registerFactory(() => PrivacyViewModel());
  locator.registerFactory(() => NotificationHistoryViewModel());

  // Factory ViewModels (Basic)
  locator.registerFactory(() => SupplementViewModel(
        locator<SupplementRepository>(),
        locator<UrlService>(),
        locator<AnalyticsService>(),
      ));
  locator.registerFactory(() => PersistentRemindersViewModel(
        locator<SettingsRepository>(),
        locator<NotificationService>(),
      ));
  locator.registerFactory(
      () => CommunityViewModel(locator<CommunityRepository>()));
  locator.registerFactory(
      () => ArticleDetailViewModel(locator<ArticleRepository>()));
  locator
      .registerFactory(() => ScienceHubViewModel(locator<ArticleRepository>()));
  locator.registerFactory(
      () => ReferFriendViewModel(locator<ReferralRepository>()));
  locator
      .registerFactory(() => ChemistViewModel(locator<PerplexityRepository>()));

  // Parametric ViewModels (Require userId)
  locator.registerFactoryParam<DailyStackViewModel, String, void>(
    (userId, _) => DailyStackViewModel(
      stackRepository: locator<StackRepository>(),
      logRepository: locator<LogRepository>(),
      supplementRepository: locator<SupplementRepository>(),
      settingsRepository: locator<SettingsRepository>(),
      notificationService: locator<NotificationService>(),
      authRepository: locator<AuthRepository>(),
      analyticsService: locator<AnalyticsService>(),
      soundService: locator<SoundService>(),
      userId: userId,
    ),
  );

  locator.registerFactoryParam<LibraryViewModel, String, void>(
    (userId, _) => LibraryViewModel(
      supplementRepository: locator<SupplementRepository>(),
      stackRepository: locator<StackRepository>(),
      userId: userId,
    ),
  );

  locator.registerFactoryParam<TrophyRoomViewModel, String, void>(
    (userId, _) =>
        TrophyRoomViewModel(locator<GamificationRepository>(), userId),
  );

  locator.registerFactoryParam<HistoryLogViewModel, String, void>(
    (userId, _) => HistoryLogViewModel(
      logRepository: locator<LogRepository>(),
      stackRepository: locator<StackRepository>(),
      userId: userId,
    ),
  );

  locator.registerFactoryParam<SymptomCheckInViewModel, String, void>(
    (userId, _) => SymptomCheckInViewModel(
      repository: locator<SymptomRepository>(),
      userId: userId,
    ),
  );

  locator.registerFactoryParam<SafetyViewModel, String, void>(
    (userId, _) => SafetyViewModel(
      repository: locator<SafetyRepository>(),
      userId: userId,
    ),
  );

  locator.registerFactoryParam<FocusBuddiesViewModel, String, void>(
    (userId, _) => FocusBuddiesViewModel(
      locator<AuthRepository>(),
      locator<LogRepository>(),
    ),
  );

  locator.registerFactoryParam<NightlyReflectionViewModel, String, void>(
    (userId, _) => NightlyReflectionViewModel(
      logRepository: locator<LogRepository>(),
      userId: userId,
    ),
  );

  locator.registerFactoryParam<DoctorExportViewModel, String, void>(
    (userId, _) => DoctorExportViewModel(
      logRepository: locator<LogRepository>(),
      authRepository: locator<AuthRepository>(),
      pdfService: locator<ReportPdfService>(),
      userId: userId,
    ),
  );

  locator.registerFactoryParam<InsightsViewModel, String, void>(
    (userId, _) => InsightsViewModel(
      logRepository: locator<LogRepository>(),
      userId: userId,
    ),
  );

  locator.registerFactoryParam<GlobalSearchViewModel, String, void>(
    (userId, _) => GlobalSearchViewModel(
      supplementRepository: locator<SupplementRepository>(),
      stackRepository: locator<StackRepository>(),
      userId: userId,
    ),
  );

  locator.registerFactoryParam<StackBuilderViewModel, String, void>(
    (userId, _) => StackBuilderViewModel(
      stackRepository: locator<StackRepository>(),
      supplementRepository: locator<SupplementRepository>(),
      safetyViewModel: locator<SafetyViewModel>(param1: userId),
      userId: userId,
    ),
  );
}
