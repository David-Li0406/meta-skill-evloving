# ADHD-Friendly Standards Implementation Plan

> **Instructions**: Review each item below. Delete any items you don't want implemented. The remaining items will become the roadmap.

---

## ✅ Already Implemented
These features are already in the app (no action needed):

| Feature | Location |
|---------|----------|
| Quick Take swipe gesture | `DailyStackScreen` |
| Time urgency countdown labels | `UpNextCard`, time status helpers |
| Persistent nudge notifications | `NotificationService` |
| Simplified 3-step onboarding | `OnboardingGoalSelection`, etc. |
| 4:00 AM rollover logic | `LogRepository` |
| Dark mode support | `ThemeViewModel`, `AppTheme` |
| Progress indicators (streaks, XP) | `InsightsScreen`, `ProfileHeader` |
| Celebration animations | `CelebrationAnimation` widget |
| Single primary action per screen | Most screens follow this |

---

## 🔧 Level 1: Core UX/UI Enhancements

### 1.1 Reduced Motion Support
- [ ] Add `SettingsRepository.reduceMotion` preference
- [ ] Check `MediaQuery.disableAnimations` globally
- [ ] Disable confetti/celebration when reduced motion enabled
- **Effort**: Small | **Impact**: High for sensory-sensitive users

### 1.2 Haptic Feedback Toggle
- [ ] Add haptic toggle in Settings
- [ ] Gate all `HapticFeedback` calls behind preference
- **Effort**: Small | **Impact**: Medium

### 1.4 Font Size Customization
- [ ] Add font scale slider in AppAppearanceScreen (1.0x–1.5x)
- [ ] Apply via `MediaQuery.textScaleFactorOf` wrapper
- **Effort**: Medium | **Impact**: High for readability

---

## 🧭 Level 2: Navigation & Architecture

### 2.1 Global Search
- [ ] Add search icon to Dashboard AppBar
- [ ] Search supplements, stacks, articles by name
- **Effort**: Medium | **Impact**: High for finding items quickly

### 2.2 Resume Where Left Off
- [ ] Persist last visited route in SharedPreferences
- [ ] Restore on app launch (optional setting)
- **Effort**: Small | **Impact**: Medium

### 2.3 Recently Viewed
- [ ] Track last 5 supplements/articles viewed
- [ ] Show in Dashboard "Recently Viewed" section
- **Effort**: Medium | **Impact**: Medium

---

## ♿ Level 3: Accessibility



### 3.2 Focus Order Management
- [ ] Define `FocusNode` chains for forms
- [ ] Ensure logical tab order on StackBuilder
- **Effort**: Medium | **Impact**: High for keyboard users

### 3.3 Touch Target Size Audit
- [ ] Ensure all interactive elements ≥ 48x48 dp
- [ ] Fix any undersized buttons in SettingsTiles
- **Effort**: Small | **Impact**: High


---

## ⏱️ Level 4: ADHD-Specific Features

### 4.1 Flexible Focus Timer
- [ ] Create `FocusTimerWidget` with start/pause/reset
- [ ] No aggressive countdown styling
- [ ] Add to Daily Stack screen
- **Effort**: Medium | **Impact**: High for time blindness

### 4.2 Auto-Save for Notes/Reflections
- [ ] Implement 2-second debounce auto-save
- [ ] Show subtle "Saved" toast
- [ ] Apply to NightlyReflection, SymptomCheckin
- **Effort**: Small | **Impact**: High (no data loss)

### 4.3 Distraction-Free / Focus Mode
- [ ] Add toggle in Settings
- [ ] When enabled: hide nav bar, simplify UI
- [ ] Show only current stack items
- **Effort**: Medium | **Impact**: High for focus sessions

### 4.4 Notification Quiet Hours
- [ ] Add quiet hours time range in Settings
- [ ] Suppress non-critical notifications during range
- **Effort**: Small | **Impact**: Medium

---

## 🧪 Level 5: Testing & Validation

### 5.1 Accessibility Test Suite
- [ ] Add `flutter test` with accessibility checks
- [ ] Run `flutter analyze` with a11y lints
- **Effort**: Medium | **Impact**: Quality assurance

### 5.2 ADHD User Testing Checklist
- [ ] Create test script for real ADHD user feedback
- [ ] Document friction points
- **Effort**: Low (doc only) | **Impact**: Critical

---

## 📦 Recommended Packages (Not Yet Added)

| Package | Purpose | Priority |
|---------|---------|----------|
| `flutter_screenutil` | Responsive sizing | Optional |
| `easy_localization` | Multi-language | Future |
| `lottie` | Lightweight animations | Already used |
| `flutter_secure_storage` | Secure credential storage | Already used |

---

## Priority Tiers

**Tier 1 (Do First)**:
- 1.1 Reduced Motion
- 3.1 Semantic Labels Audit
- 4.2 Auto-Save

**Tier 2 (High Value)**:
- 1.3 High Contrast Theme
- 2.1 Global Search
- 4.1 Focus Timer

**Tier 3 (Nice to Have)**:
- 1.2 Haptic Toggle
- 2.2 Resume Where Left Off
- 4.4 Quiet Hours

---

> **Next Step**: Delete items you don't want, then I'll execute the remaining plan.
