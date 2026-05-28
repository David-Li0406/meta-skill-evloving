# Project Roadmap & Remaining Tasks

This document serves as the primary reference for pending implementation tasks for the ADHD Supplement App. It consolidates technical debt, feature enhancements, and scientific audits.

## 1. App Store & Deployment
- [ ] **Implementation of App Store Upload Guide**
    - [ ] Create `PrivacyInfo.xcprivacy` and declare data types.
    - [ ] Add visible medical disclaimer on first-run onboarding.
    - [ ] Configure Apple App Store Connect metadata (Screenshots, Nutrition Labels).
    - [ ] Set up a Demo Account for App Reviewers.

## 2. Scientific Data & Intelligence
- [ ] **Phase 3: Scientific Deep-Dive**
    - [ ] Audit and integrate meta-analysis data for core supplements.
    - [ ] Expand FAQ coverage based on common user questions about stimulant/supplement interactions.
- [ ] **Link & Title Audit**
    - [ ] Fix study title/URL mismatches in `seeding_service.dart`.
    - [ ] Audit and fix study titles in `ScienceHubViewModel`.
    - [ ] Implement `launchUrl` handling in `ScienceHubScreen`.

## 3. Optimization & Stability
- [ ] **Architectural Refactoring**
    - [ ] Refactor `lib/config/locator.dart` to group registrations by feature domain.
    - [ ] Implement typed `Failure` system in `lib/domain/errors/failure.dart` for resilient error handling.
- [ ] **Asset & Performance Polish**
    - [ ] Optimize loading states with `SkeletonLoader` widgets in Daily Stack and Insights screens.
    - [ ] Implement `HapticFeedback` for high-frequency actions (e.g., Log Dose).
- [ ] **Logging Infrastructure**
    - [ ] Replace scattered `debugPrint` calls with a centralized, structured `AppLogger`.

## 4. UI/UX Refinement
- [ ] **Stack Builder Polish**
    - [ ] Add "Edit Stack Name/Time" dialog.
    - [ ] Implementation of custom dosage input for individual stack items.
- [ ] **Insights Data Visualization**
    - [ ] Add multi-week comparison views.
    - [ ] Integrate "Scientific Nudges" based on real-time focus trends.

## 5. Testing & CI/CD
- [ ] **Testing Resilience**
    - [ ] Fix broken widget tests in `test/widget/` (dependency injection issues).
    - [ ] Add integration tests for the Stack Builder flow.
    - [ ] Verify iOS build stability in GitHub Actions.

## Archive (Completed Milestones)
- [x] Supplement Standardization (51 items)
- [x] Science Hub Infrastructure (FAQ, Research Library, Educational Content)
- [x] Stack Builder Refactor (ViewModel-based, Reordering, Overflow fixed)
- [x] Medication Safety Guard & Interactions
- [x] Local Asset Asset Implementation (Eliminated broken external link placeholders)
