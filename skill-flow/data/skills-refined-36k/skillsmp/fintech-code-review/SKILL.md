---
name: fintech-code-review
description: Reviews backend and Flutter code with FinTech-grade rigor; financial correctness, idempotency, security, and race-condition safety.
---

# FinTech Code Review

## When to use this skill

- Before finalizing any pull request or code block related to transactions, ledgers, or balances.
- When implementing Cloud Functions that handle money.
- When writing Firestore transactions.
- When reviewing Flutter code that displays sensitive financial data.

## How to use it

1. **Review for Financial Correctness**:
   - Ensure all monetary values are handled as integers (e.g., cents/micros) to avoid floating-point errors.
   - Verify that positive/negative signs are strictly enforced (e.g., debits are negative, credits are positive).
2. **Check for Idempotency**:
   - Verify that all transfer/transaction functions use an `eventId` or `idempotencyKey` to prevent double-spending.
   - Ensure Firestore writes are idempotent.
3. **Analyze Concurrency & Safety**:
   - Confirm that all ledger updates happen within a Firestore Transaction.
   - Check for race conditions where two processes might read old balances simultaneously.
4. **Security Audit**:
   - Ensure service accounts are used for backend operations.
   - Verify that the client cannot spoof transaction results.
