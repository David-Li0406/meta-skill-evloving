# Apple App Store Upload Guide (2026)

Uploading to the Apple App Store is a more "locked-down" process than Android. In 2026, Apple has introduced stricter Privacy Manifests and Accessibility Nutrition Labels that you must complete, especially for a health-oriented app like yours.

Here is the professional workflow to get your ADHD app from Antigravity to an iPhone.

## 1. The Membership Requirement
Unlike Android’s one-time fee, Apple requires a yearly subscription ($99 USD).

- **Action**: Enroll in the Apple Developer Program.
- **2026 Requirement**: Ensure you have Xcode 17 (or the current stable version for 2026) installed on a Mac. Apple now mandates that all new submissions use the latest SDKs to ensure compatibility with modern privacy features.

## 2. Prepare the "Privacy Manifest" (Critical for 2026)
As of 2026, Apple "technically enforces" privacy declarations. If your code accesses certain data without a Privacy Manifest file, your upload will be rejected immediately.

1. In Xcode, right-click your `Runner` folder and select **New File**.
2. Choose **App Privacy File** (named `PrivacyInfo.xcprivacy`).
3. **For your ADHD App**: You must declare why you are tracking "Health" data (supplements) and "Identifiers" (if using Firebase for user stacks).
    - *Example*: Define `NSPrivacyAccessedAPITypes` for any health-related APIs you use.

## 3. The Flutter Build Process
Once your code is ready in Antigravity, you need to generate the "IPA" (the iOS equivalent of an APK/AAB).

1. **Update Versioning**: In `pubspec.yaml`, increment your version (e.g., `1.0.1+2`).
2. **Run Build Command**: In your terminal, run:
   ```bash
   flutter build ipa --release
   ```
3. **Open Xcode**: Open the `ios/Runner.xcworkspace` file.
4. **Archive**: Go to **Product > Archive**. This bundles your app for distribution.
5. **Distribute**: In the "Organizer" window that pops up, click **Distribute App** and select **App Store Connect**.

## 4. App Store Connect Setup
While your app is "Processing" in Apple's cloud, you must fill out the storefront details:
- **Screenshots**: Apple is strict. You need sets for 6.7" (Pro Max) and 5.5" (older Plus models). Use your Google Stitch designs as a template for these.
- **Review Guidelines (Health)**: Because you offer supplement information, you must specify that the app is informational only.
    - *Tip*: In the "App Review Information" notes, explicitly state: "This app provides educational content on supplements. It does not provide medical diagnoses or prescriptions."
- **Age Rating**: Mark it appropriately. Since it involves health and "unrestricted web access" (if your referral links open a browser), it will likely be 12+ or 17+.

## 5. The "Privacy Nutrition Label"
You must answer a series of questions in App Store Connect about the data you collect.

- **Data Linked to User**: If users save their supplement stacks to an account, this is "Linked Data."
- **Tracking**: If you use your affiliate links to track purchases across other sites, you must declare this under **Tracking**.

## Strategy for a Smooth Review
Apple's human reviewers are very cautious about "Medical Advice." To avoid a rejection:
1. **Include a visible disclaimer** on the first screen (onboarding).
2. **Provide a Demo Account**: In the review notes, give them a login so they can see all the supplement information without having to pay or sign up personally.
