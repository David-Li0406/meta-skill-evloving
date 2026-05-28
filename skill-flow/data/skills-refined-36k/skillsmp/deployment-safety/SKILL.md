---
name: deployment-safety
description: Enforces safe production deployment and rollback rules for a FinTech system.
---

# Deployment Safety

## When to use this skill

- Before running `firebase deploy`.
- When preparing a release candidate.
- When writing deployment scripts / CI pipelines.

## How to use it

1. **Pre-Flight Checks**:
   - Have all rules been audited (`firestore-rules-audit`)?
   - Have all functions been locally emulated and tested?
   - Are there any breaking schema changes?
2. **Rolling Strategy**:
   - Deploy Rules & Indexes first.
   - Deploy Functions.
   - Deploy Front-end (if applicable / hosting).
3. **Safe Function Updates**:
   - When updating a function that handles events, ensure the new version is compatible with existing in-flight events.
   - Avoid renaming functions—Eventarc triggers might break. Create new, deprecate old.
4. **Rollback Plan**:
   - Ensure we have the previous version's artifacts or git commit hash ready.
   - If a bad deployment occurs, know the sequence to revert (revert code, redeploy).
