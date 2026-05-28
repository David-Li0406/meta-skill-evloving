# ADR-001: Safety-First Supplement Architecture

**Status**: Accepted
**Date**: 2026-01-19
**Context**:
Building an ADHD supplement app requires strict safety controls. Users may be on prescription medication (Stimulants/Non-Stimulants). Recommending supplements without cross-referencing interactions poses a significant health risk and legal liability.

**Decision**:
We implement a "Safety-First" architecture where:
1.  **Middleware Intercept**: Any "Add to Stack" action is intercepted by `SafetyViewModel`.
2.  **Interaction Matrix**: A local interaction database checks `Supplement` vs `UserMedication`.
3.  **Hard Stops**: High-risk interactions (e.g., Vitamin C + Vyvanse < 2hrs) trigger blocking modals, not just toast warnings.
4.  **Audit Logs**: All overrides are logged in `SafetyOverride` entity for liability tracking.

**Consequences**:
- **Positive**: Prevents dangerous combinations; builds Clinical Trust.
- **Negative**: Adds friction to the "Onboarding" and "Add Stack" flows.
- **Mitigation**: Use "Educational" friction (explaining WHY it's blocked) rather than "Bureaucratic" friction.
