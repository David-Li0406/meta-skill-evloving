# ADR-002: Flutter 16KB Page Alignment

**Status**: Accepted
**Date**: 2026-01-19
**Context**:
Android 15 introduces a requirement for 16KB page size compatibility. Apps that only support 4KB pages will fail to run or be rejected by the Play Store.

**Decision**:
We utilize Flutter version 3.38.7 (or later) which includes native support for 16KB memory page alignment.
- **Build Artifact**: We generate Android App Bundles (AAB) which handle the split ABIs automatically.
- **Verification**: We must verify the alignment using specific Android SDK tools if targeting devices directly, but the AAB workflow handles this for the Store.

**Consequences**:
- **Positive**: Future-proofs the app for 2026+ Android devices; prevents Play Store rejection.
- **Negative**: Slightly larger binary size due to alignment padding (negligible).
