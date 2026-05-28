# Feature Documentation Index

This directory contains comprehensive documentation for all features in the ADHD Supplement App.

## Core Feature Areas

### 📊 [Daily Stack & Logging](daily_stack_and_logging.md)
The heart of the app - routine tracking, intake logging, and streak management.
- `DailyStackViewModel`, `HistoryLogViewModel`, `LibraryViewModel`
- Daily logging, history browsing, supplement library

### 🛡️ [Safety & Interactions](safety_and_interactions.md)
Medication-supplement interaction checking and safety warnings.
- `SafetyGuard`, `ADHDInteractionGuard`, `SafetyViewModel`
- Interaction rules, warning severities, override flows

### 💰 [Affiliate & Monetization](affiliate_monetization.md)
Region-aware Amazon affiliate link generation for supplement purchases.
- `AffiliateService`, `UrlService`
- Multi-region support (US, UK, EU)

### 🔔 [Gamification & Notifications](gamification_and_notifications.md)
Retention systems including streaks, badges, and the notification history "Black Box."
- `NotificationHistoryViewModel`, `MilestoneSuccessScreen`
- Ethical gamification, grace periods

### 🚀 [Onboarding & Setup](onboarding_and_setup.md)
First-time user experience and stack configuration.
- `QuickSetupWizardScreen`, `OnboardingGoalSelectionScreen`, `OnboardingStackSetupScreen`
- Goal selection, grace period education

### 📈 [Symptom Tracking & Insights](symptom_tracking_and_insights.md)
Daily symptom check-ins and data visualization.
- `DailySymptomCheckinScreen`, `InsightsScreen`, `WeeklyReviewScreen`
- Mood/focus/energy tracking, correlation analysis

### 🤝 [Community & Social](community_and_social.md)
Peer support, referrals, and social learning features.
- `CommunityScreen`, `FocusBuddiesScreen`, `ReferFriendScreen`, `ScienceHubScreen`
- Body doubling, popular stacks, research articles

### ⚙️ [Settings & Account](settings_and_account.md)
User profile, privacy, subscription, and app customization.
- `UserProfileScreen`, `PrivacySettingsScreen`, `SubscriptionScreen`, `AppAppearanceScreen`
- GDPR compliance, theme selection, subscription management

### 🏆 [Streaks & Gamification](streaks_and_gamification.md)
Achievement system, badge unlocking, and streak mechanics.
- `TrophyRoomScreen`, `LevelUpScreen`, `StreakRecoveryScreen`
- Grace days, milestone celebrations

### 🩺 [Clinical Tools](clinical_tools.md)
Doctor communication and medication management features.
- `DoctorExportScreen`, `VisualPillMatcherScreen`, `LateDoseTriageScreen`
- PDF reports, pill identification, dose timing guidance

### 💬 [Help & Support](help_and_support.md)
In-app help resources and customer support access.
- `HelpAndSupportCenterScreen`, `ArticleDetailScreen`
- FAQ, tutorials, bug reporting

### 📡 [Offline & Error Handling](offline_and_error_handling.md)
Offline-first architecture and graceful error management.
- `OfflineErrorScreen`, `CloudSyncScreen`, `DeveloperHandoffScreen`
- Local-first storage, sync queuing

### 📱 [Additional Features](additional_features.md)
Dashboard, library, stack builder, and miscellaneous screens.
- `DashboardScreen`, `LibraryScreen`, `StackBuilderScreen`, `NotificationReliabilitySetupScreen`

## Related Documentation
- **ADRs**: Architectural decisions → `docs/adrs/`
- **Coding Standards**: → `Claude.md`
- **Task Tracking**: → artifact `task.md`
