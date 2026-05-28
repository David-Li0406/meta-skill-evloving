# Daily Stack & Logging System

This document covers the safety mechanisms that prevent harmful supplement-medication interactions and identifies substances to avoid.

## 1. Avoid List (Supplement Status)
The app categorizes supplements into three delivery statuses:
- **Beneficial**: Recommended and safe for general ADHD support.
- **Avoid**: Specifically flagged as harmful or ineffective (e.g., Red Dye 40, HFCS).
- **Neutral**: Supporting items with no significant ADHD impact.

**Safety Enforcement:**
- **Library Toggles**: Users can switch between "Recommended" and "Avoid List" views.
- **Visual Warnings**: Avoided items feature red accents and warning icons.
- **Detail Lock**: The "Add to Stack" functionality is completely disabled for `avoid` items, replaced by a "Risk Profile" card.

## Overview
The "Daily Stack" is the heart of the app. Users build routines (Morning, Evening) with supplements, and the app tracks their adherence over time.

## Components

### 1. `DailyStackViewModel` (Presentation Layer)
**Location**: `lib/presentation/view_models/daily_stack_view_model.dart`

Manages the user's daily routine and intake logging.

**State:**
- `_stacks`: List of `SupplementStack` (Morning, Evening, etc.).
- `_todayLog`: `DailyLog` object for today's date.
- `_streakCount`: Consecutive days of completion.

**Key Methods:**
- `initialize()`: Loads stacks, today's log, and streak count in parallel.
- `markSupplementTaken(String supplementId)`: Logs intake.
- `markSupplementSkipped(String supplementId, {String? reason})`: Logs a skip.
- `toggleSupplement(String supplementId)`: Toggle taken/untaken.
- `isSupplementTaken(String supplementId)`: Check status.
- `saveSymptomRatings(Map<String, int> ratings)`: Save mood/focus/energy ratings.
- `_getLogicalToday()`: Implementation of the **4 AM Rollover Rule**. Treats time before 4 AM as the previous calendar day to accommodate late-night users.

**Dashboard Logic:**
- **Dynamic Filtering**: Supplements marked as "Taken" are automatically hidden from the Today view to maintain a focused task list.
- **Feedback Loop**: Mark as taken triggers a system "tick" sound, haptic feedback, and a streak confirmation message.

**Computed Getters:**
- `todayProgress`: Double from 0.0 to 1.0.
- `progressText`: e.g., "2 of 3 stacks completed".

### 2. `HistoryLogViewModel` (Presentation Layer)
**Location**: `lib/presentation/view_models/history_log_view_model.dart`

Manages historical log viewing and filtering.

**State:**
- `_logs`: List of `DailyLog` for the past N days.
- `_selectedFilter`: `All`, `Taken`, `Missed`, `Dismissed`.

**Key Methods:**
- `initialize({int days = 30})`: Load recent history.
- `loadDateRange(DateTime start, DateTime end)`: Custom range.
- `setFilter(String filter)`: Filter entries.
- `getFilteredEntries(DailyLog log)`: Apply filter to a specific day's log.

**Computed Getters:**
- `groupedLogs`: Groups by "Today", "Yesterday", "This Week".
- `stats`: `{'total': N, 'taken': N, 'missed': N, 'completionRate': N}`.

### 3. `LibraryViewModel` (Presentation Layer)
**Location**: `lib/presentation/view_models/library_view_model.dart`

Manages the supplement discovery/search library.

**Key Methods:**
- `initialize()`: Load all supplements.
- `search(String query)`: Remote search (User-aware).
- `filterByCategory(String? category)`: Local filter.
- `createCustomSupplement(...)`: Add a private user supplement.
- `deleteCustomSupplement(...)`: Remove a private user supplement.
- `clearFilters()`: Reset.
- `getSupplement(String id)`: Fetch by ID.

**Computed Getters:**
- `categories`: Unique list of supplement categories.

## Data Entities
- `SupplementStack`: `{ id, name, userId, items: [...], time, isActive }`.
- `DailyLog`: `{ id, userId, date, entries: [...], symptomRatings, createdAt }`.
- `LogEntry`: `{ supplementId, takenAt, taken, skippedReason }`.
- `Supplement`: `{ id, name, category, benefits, dosage, amazonAsin, ... }`.

## Repositories (Domain Ports)
- `StackRepository`: CRUD for user stacks.
- `LogRepository`: Stores daily logs, streak calculation.
- `SupplementRepository`: Fetches supplement catalog (Global + User-specific).
- **Custom Supplements**: Stored per-user in Firestore (`/users/{uid}/custom_supplements`).

## Firebase Implementations (Infrastructure)
- `FirebaseStackRepository`
- `FirebaseLogRepository`
- `FirebaseSupplementRepository`

> **Note**: These require a configured Firebase project. See `firebase_options.dart`.
