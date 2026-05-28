---
name: architecture-guard
description: Enforces Boklo Wallet’s backend-authoritative, event-driven FinTech architecture. Rejects any suggestion that violates the Source of Truth.
---

# Architecture Guard

## When to use this skill

- When proposing major architectural changes.
- When designing new features that involve financial transactions.
- When a user request seems to conflict with the Backend-Authoritative principle.
- To verify if a proposed solution respects the Single Source of Truth rules.

## How to use it

1. **Analyze the Proposal**: Review the proposed code or design against the `SOURCE_OF_TRUTH.md` and core Boklo Wallet rules.
2. **Check for Violations**:
   - Does the client write to the ledger/balance? (VIOLATION)
   - Is logic placed in the Eventarc router instead of a consumer? (VIOLATION)
   - Is the frontend calculating financial states? (VIOLATION)
3. **Enforce Rules**:
   - If a violation is found, **REJECT** the proposal immediately.
   - Cite the specific rule from `SOURCE_OF_TRUTH.md` that was violated.
   - Provide a compliant alternative (e.g., "Instead of updating the balance locally, emit a `transaction.created` event and listen for the backend response").
4. **Guard the boundaries**: Ensure that the boundary between Client (Observer) and Backend (Authority) is distinct and rigid.
