# Onboarding & Setup Flow

This document describes the initial user experience and stack configuration.

## Overview
The app features a multi-step onboarding flow to help ADHD users get started without overwhelming them with choices.

## Screens

### 1. `QuickSetupWizardScreen`
**Location**: `lib/presentation/views/quick_setup_wizard_screen.dart`

A streamlined wizard that walks users through their first supplement stack setup.

**Flow:**
1. Welcome message explaining the app's purpose.
2. Medication input (for safety checking).
3. Quick supplement selection (Popular stacks: Focus, Sleep, Energy).
4. Notification preferences.

**Key Features:**
- Progress indicator showing steps.
- "Skip" option for power users.
- Auto-saves progress locally (can resume later).

### 2. `OnboardingGoalSelectionScreen`
**Location**: `lib/presentation/views/onboarding_goal_selection_screen.dart`

Lets users select their primary health goals to personalize recommendations.

**Goals:**
- 🎯 Focus & Concentration
- 💤 Better Sleep
- ⚡ Energy & Motivation
- 😌 Anxiety Management
- 🧠 Memory & Learning

**Usage:**
Stores selections in user profile for filtering supplement library.

### 3. `OnboardingGracePeriodScreen`
**Location**: `lib/presentation/views/onboarding_grace_period_screen.dart`

Explains the "Grace Period" gamification mechanic where missing a day doesn't break the streak immediately.

**Educational Content:**
- What Grace Days are (3 automatic per month).
- How they prevent demotivation from strict streaks.
- Transparency that it's designed to be supportive, not punitive.

### 4. `OnboardingStackSetupScreen`
**Location**: `lib/presentation/views/onboarding_stack_setup_screen.dart`

The core stack builder used during onboarding (also accessible later).

**Features:**
- Drag-and-drop supplement items.
- Time-based stacks (Morning, Afternoon, Evening).
- Visual pill preview.
- Safety warnings inline.

**Data Saved:**
Creates initial `SupplementStack` entities and saves to Firebase.

## Navigation Flow
```
App Launch
  ↓
OnboardingGoalSelectionScreen
  ↓
OnboardingGracePeriodScreen (Educational)
  ↓
QuickSetupWizardScreen
  ↓
OnboardingStackSetupScreen
  ↓
Dashboard (Home)
```

## Related Features
- **Stack Builder**: Users can modify stacks later via `StackBuilderScreen`.
- **Medication Safety**: Inputs from onboarding feed into `SafetyGuard` for interaction checks.
