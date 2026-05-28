---
name: eventarc-validation
description: Validates CloudEvents published to Eventarc for strict CloudEvents v1.0 compliance (e.g., datacontenttype correctness). Prevents routing failures.
---

# Eventarc Validation

## When to use this skill

- When defining new custom events.
- When debugging "silent failures" where events are not triggering functions.
- When writing code that publishes to Eventarc.

## How to use it

1. **Validate CloudEvents Attributes**:
   - Ensure `type` follows the `com.boklo.transaction.*` format.
   - Verify `source` identifies the producing service (e.g., `//firestore.googleapis.com/...`).
   - Check that `datacontenttype` is explicitly `application/json` (often missed, causing routing failures).
2. **Check Payload Structure**:
   - Ensure the `data` attribute contains a valid JSON object matching the expected schema.
3. **Verify Routing Config**:
   - Confirm that the `eventarc_trigger` definition in `firebase.json` or Terraform matches the emitted event attributes exactly.
4. **Log & Trace**:
   - Recommend logging the full CloudEvent object before publishing during debugging to ensure all fields are populated correctly.
