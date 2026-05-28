# ADR 0034: App Store Compliance (Privacy & Medical Safety)

## Status
Accepted

## Context
Apple's App Store guidelines for medical and health apps (Section 1.4.1 and 5.1) require explicit medical disclaimers and detailed privacy manifest declarations for 2024+ submissions. To avoid rejection and ensure patient safety, the app needed a structured way to declare its data usage and a mandatory mechanism for users to acknowledge the "not medical advice" nature of the tool.

## Decision
We implemented a multi-layered compliance framework:
1.  **iOS Privacy Manifest**: Created `PrivacyInfo.xcprivacy` with precise declarations for User ID collection (Auth), Product Interaction (Analytics), and Crash Data. Justified the usage of accessed APIs like `UserDefaults` using the standard `CA92.1` reason.
2.  **Mandatory Onboarding Disclaimer**: Integrated a high-contrast `MedicalDisclaimerWidget` as the absolute first step of the `QuickSetupWizardScreen`.
3.  **Enforced Agreement**: Developed a logic gate (`_canProceed`) that prevents progression to the goals/stack selection until the user explicitly checks the "I understand" agreement box.
4.  **Acceptance Persistence**: Updated the `SettingsRepository` to include `setAcceptedDisclaimer`, ensuring that this friction is only applied once during the initial install.
5.  **Micro-copy Optimization**: Used ADHD-friendly formatting (bullets, bolding) to ensure the disclaimer is readable and not just a "wall of text" that get ignored.

## Consequences
- **Submission Readiness**: The app now meets the technical and legal requirements for store review.
- **Liability Mitigation**: Clear separation established between informational tracking and clinical advice.
- **Installation Friction**: Adds one mandatory step to the first-run experience, but optimized for readability to minimize drop-off.
