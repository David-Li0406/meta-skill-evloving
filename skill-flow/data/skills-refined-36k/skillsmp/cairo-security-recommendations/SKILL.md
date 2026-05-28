---
name: cairo-security-recommendations
description: Summarize Starknet smart contract security recommendations and common Cairo pitfalls; use when a request involves best practices, safety checks, or audit guidance.
---

# Cairo Security Recommendations

## Overview
Provide best practice guidance for safe Starknet contract development.

## Quick Use
- Read `references/security-recommendations.md` before answering.
- Prioritize access control, input validation, and event logging.
- Call out Cairo-specific pitfalls like operator precedence and underflows.

## Response Checklist
- Require access control on privileged actions and upgrades.
- Validate external inputs, especially L1 handler senders.
- Avoid unbounded loops and large storage writes.
- Emit events for sensitive state changes.

## Example Requests
- "What are common security pitfalls in Cairo contracts?"
- "What should I validate in an L1 handler?"
- "What are general best practices for Starknet contracts?"
