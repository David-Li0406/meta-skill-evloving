# Symptom Tracking & Insights

This document covers the mood/symptom logging and data analysis features.

## Overview
Users can track their ADHD symptoms (focus, mood, energy) daily to correlate with supplement intake.

## Components

### 1. `DailySymptomCheckinScreen`
**Location**: `lib/presentation/views/daily_symptom_checkin_screen.dart`

**ViewModel**: `SymptomCheckInViewModel`

A daily check-in screen where users rate their symptoms on a 1-10 scale.

**Symptoms Tracked:**
- 🧠 Focus & Concentration
- 😊 Mood
- ⚡ Energy Levels
- 😴 Sleep Quality (previous night)

**UI:**
- Custom sliders for each symptom.
- Optional notes field for context ("Had coffee at 3pm").
- Quick submit with haptic feedback.

**Data Storage:**
Saved as part of `DailyLog` entity with `symptomRatings` map.

### 2. `NightlyReflectionScreen`
**Location**: `lib/presentation/views/nightly_reflection_screen.dart`

An evening prompt to log the day's experience.

**Features:**
- "How was your day?" free-form text.
- Quick rating of stack effectiveness.
- Option to mark specific supplements as "Felt beneficial" or "No effect".

**Purpose:**
Feeds into long-term insights and helps users identify what's actually working.

### 3. `InsightsScreen`
**Location**: `lib/presentation/views/insights_screen.dart`

Displays data visualizations and trend analysis.

**Charts:**
- **Focus vs Intake**: Line chart showing focus score over time with supplement adherence overlay.
- **Correlation Matrix**: Which supplements correlate with better symptom scores.
- **Weekly Averages**: Compare this week to last week.

**Current State:**
UI is implemented with mock data. Real chart logic requires integration with a charting library (e.g., `fl_chart`).

### 4. `WeeklyReviewScreen`
**Location**: `lib/presentation/views/weekly_review_screen.dart`

A Sunday summary of the past week's performance.

**Metrics:**
- Total supplements taken vs skipped.
- Average symptom scores.
- Streak status.
- Motivational message based on progress.

**Gamification:**
Unlocks badges/achievements if certain milestones are hit.

## Data Flow
```
User rates symptoms
  ↓
SymptomCheckInViewModel.saveRatings()
  ↓
Saved to DailyLog.symptomRatings
  ↓
Aggregated for InsightsScreen charts
```

## Related ViewModels
- `SymptomCheckInViewModel`: Manages daily check-in state.
- (Future) `InsightsViewModel`: Will calculate correlations and trends.
