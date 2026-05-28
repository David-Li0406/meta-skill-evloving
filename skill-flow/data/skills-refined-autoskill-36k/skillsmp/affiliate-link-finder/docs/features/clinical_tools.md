# Clinical Tools & Medical Features

This document covers features designed to bridge the gap between the app and clinical care.

## Overview
These tools help users communicate with their healthcare providers and manage ADHD medication-related challenges.

## Screens

### 1. `DoctorExportScreen`
**Location**: `lib/presentation/views/doctor_export_screen.dart`

Generates a professional report for doctor appointments.

**Report Contents:**
- Supplement intake history (past 30 days).
- Symptom ratings over time (charts).
- Medication list.
- Notes and observations.

**Export Formats:**
- 📄 PDF (formatted, print-ready).
- 📧 Email (send directly to doctor).

**Use Case:**
"My doctor asked what supplements I'm taking and how they affect my focus. I showed them this report and it helped my prescription adjustment."

**Current State:**
UI implemented. PDF generation requires `pdf` package integration.

### 2. `VisualPillMatcherScreen`
**Location**: `lib/presentation/views/visual_pill_matcher_screen.dart`

A visual guide to identify pills by shape, color, and imprint.

**How It Works:**
1. User selects pill characteristics (Round, White, "A 10").
2. App shows matching images from database.
3. User confirms match.
4. Pill is added to their medication list.

**Safety:**
Always includes disclaimer: "This is not a substitute for pharmacist verification. If unsure, consult your pharmacist."

**Data Source:**
Pill images from FDA's Pill Identifier database (requires API integration).

### 3. `LateDoseTriageScreen`
**Location**: `lib/presentation/views/late_dose_triage_screen.dart`

Decision tree for "It's 4pm and I forgot my morning stimulant. Should I take it now?"

**Triage Logic:**
- **If before 2pm**: "Yes, take it now."
- **If 2-4pm**: "Take half dose OR skip and take tomorrow."
- **If after 4pm**: "Skip. Taking stimulants late may disrupt sleep."

**Customization:**
User can set their typical bedtime to adjust the thresholds.

**Disclaimer:**
Always includes: "This is general guidance. Always follow your doctor's instructions."

## Medical Safety Context
These features are designed to **supplement**, not replace, medical advice. All clinical screens include:
- Prominent disclaimers.
- Links to "Contact your doctor" or "Call your pharmacist."
- Clear indication that the app is "FDA: Medical Reference, not Medical Device."

## Related Features
See also: [Safety & Interactions](safety_and_interactions.md) for medication interaction checking.
