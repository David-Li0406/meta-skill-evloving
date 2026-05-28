---
name: incident-analysis
description: Performs root-cause analysis of failed transfers, missing events, or notification issues using system-level reasoning.
---

# Incident Analysis

## When to use this skill

- When investigating a production or dev incident (e.g., "Transfer stuck in PENDING").
- When users report "Balance didn't update".
- When analyzing logs for error patterns.

## How to use it

1. **Trace the Event Chain**:
   - Start from the creation of the transaction.
   - Did the `transaction.created` event fire?
   - Did Eventarc deliver it to the `onTransactionCreated` function?
   - Did the function execute successfully?
   - Did the `transaction.completed` event fire?
2. **Check for Broken Links**:
   - Identify which step in the chain failed.
   - Use `functions.get_logs` or grep searching to find specific transaction IDs.
3. **Verify Data Consistency**:
   - Compare the Ledger sum vs. the aggregated Balance.
   - Check if a "compensation transaction" failed (reversal).
4. **Hypothesize & Verify**:
   - Formulate a hypothesis (e.g., "Timeout during 3rd party API call").
   - Find evidence in logs to confirm or deny.
