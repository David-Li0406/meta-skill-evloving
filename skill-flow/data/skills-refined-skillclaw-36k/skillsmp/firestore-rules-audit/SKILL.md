---
name: firestore-rules-audit
description: Audits Firestore security rules to ensure ownership enforcement, immutability, and backend-only authority.
---

# Firestore Rules Audit

## When to use this skill

- When modifying `firestore.rules`.
- When adding new collections or documents.
- Periodic security reviews.

## How to use it

1. **Enforce Backend Authority**:
   - **Ledger/Balance**: Ensure these collections are `read: if request.auth != null; write: if false;` (or strictly limited to specific service accounts if not using the Admin SDK). The Client MUST NEVER be able to write to these.
2. **Enforce Ownership**:
   - For user-specific data (e.g., profiles, private notifications), ensure `allow read: if request.auth.uid == resource.data.userId;`.
3. **Check Immutability**:
   - For transaction logs, ensure that once written, fields cannot be changed. (e.g., `allow update: if false;` or strict field-level validation).
4. **Deny Default**:
   - Ensure the rules start or end with a catch-all deny for undefined collections.
5. **Validate Types**:
   - Ensure rules enforce data types (e.g., `request.resource.data.amount is int`) to prevent data corruption.
