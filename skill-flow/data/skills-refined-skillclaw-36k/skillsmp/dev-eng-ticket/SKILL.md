---
name: dev-eng-ticket
description: Orchestrate development work for an engineering ticket, with paths for new work or existing PR follow-up.
argument-hint: "[TCK-XXXXX | RFC-XXXX | empty]"
---

orientation: "You are an autonomous senior engineer tasked with implementing a critical engineering ticket. You will follow a logical decision tree to either start the ticket from scratch or follow up on existing work. Your task is scoped purely to working on the ticket. Your code will be reviewed by an independent third party, so please work diligently and to the highest possible standard."

note: "Module-specific documentation and invariants live in AGENTS.md files colocated with the code you are editing. Always read the root README.md to identify the relevant modules and their corresponding AGENTS.md files before making changes. Update AGENTS.md when module invariants or public behavior changes."

title: Dev Engineering Ticket Workflow
protocol:
  id: DEV-ENG-TICKET
  version: 2.0.0
  type: executable_specification
  inputs[1]:
    - TICKET_ID_OPTIONAL
  outputs[2]:
    - WorktreePath
    - PR_URL

variables:
  TICKET_ID_OPTIONAL: "$1"

references[2]:
  - path: references/dev-eng-ticket-workflow.md
    purpose: "Primary decision tree for new ticket vs existing PR follow-up."
  - path: references/commands.md
    purpose: "Command reference with flags and examples."

decision_tree:
  entrypoint: WORKFLOW
  nodes[1]:
    - id: WORKFLOW
      action: invoke_reference
      reference: references/dev-eng-ticket-workflow.md

## Required Reading (Mandatory)

The following documents define the core principles and security posture of APM2:

*   **[Agent-Native Software: Industry Textbook](/documents/skills/agent-native-software/SKILL.md)**: First principles of stochastic cognition, context limits, and tool-loops.
*   **[Security Documentation](/documents/security/AGENTS.md)**: Security philosophy, policy, and required reading for all agents.

## Required Reading (APM2 Rust Textbook)

Engineering tickets in APM2 MUST adhere to the **[APM2 Rust Textbook](/documents/skills/rust-textbook/)**. This textbook defines the normative contracts, invariants, and hazards that govern our implementation quality.

### Foundational Chapters (Mandatory)

The following chapters represent the baseline requirement for any development work in this repository:

*   **[07 — Errors, Panics, Diagnostics](/documents/skills/rust-textbook/07_errors_panics_diagnostics.md)**: Structured error handling and panic safety.
*   **[12 — API Design](/documents/skills/rust-textbook/12_api_design_stdlib_quality.md)**: Contract-first, misuse-resistant interfaces.
*   **[13 — Collections and Allocation](/documents/skills/rust-textbook/13_collections_allocation_models.md)**: Memory DoS prevention and address stability.
*   **[15 — Paths and Filesystem](/documents/skills/rust-textbook/15_paths_filesystem_os.md)**: Sanitization and atomic write protocols.
*   **[16 — I/O and Protocol Boundaries](/documents/skills/rust-textbook/16_io_protocol_boundaries.md)**: Framing, bounded reads, and strict Serde.
*   **[19 — Security-Adjacent Rust](/documents/skills/rust-textbook/19_security_adjacent_rust.md)**: Resource exhaustion and integrity failures.
*   **[24 — Hazard Catalog](/documents/skills/rust-textbook/24_hazard_catalog_checklists.md)**: **CRITICAL** quick-scan checklist for all changes.
*   **[26 — APM2 Safe Patterns](/documents/skills/rust-textbook/26_apm2_safe_patterns_and_anti_patterns.md)**: Project-specific idioms and lessons learned.

### PR Review Readiness Checklist

Before submitting a PR, verify your changes against the following specific contracts from the textbook:

1.  **Bounded Reads:** All reads checked against `max` before allocation ([RSK-1601], [CTR-1603]).
2.  **Atomic Writes:** State updates use `NamedTempFile` + `persist` ([CTR-1502], [CTR-2607]).
3.  **Path Safety:** `ParentDir` (`..`) rejected; `symlink_metadata` used if sensitive ([CTR-1503], [CTR-2609]).
4.  **Negative Tests:** Oversize input fails; traversal fails; forbidden actions denied ([INV-1701], [RSK-0701]).
5.  **Miri Validation:** If `unsafe` is used, `// SAFETY:` comment is present and Miri passes ([CTR-0902], [RSK-1701]).
6.  **Textbook Alignment:** Check your changes against the [Hazard Catalog](/documents/skills/rust-textbook/24_hazard_catalog_checklists.md).
7.  **Serialization Safety:** Serde operations in crypto contexts propagate errors ([CTR-1908]).
8.  **Builder Completeness:** Builder validates ALL inputs, not just IDs ([CTR-1205], [CTR-2603]).
9.  **Chain Integrity:** Hash chains commit to all related events ([CTR-2616]).
10. **Bounded Stores:** In-memory stores have `max_entries` limit with O(1) eviction ([CTR-1303]).
11. **Ledger Serde:** Audit/ledger types use `#[serde(deny_unknown_fields)]` ([CTR-1604]).
12. **Fail-Closed Flags:** Security feature flags default to disabled ([CTR-2003]).
13. **Cancellation Safety:** Idempotency markers set AFTER side effects complete ([CTR-1104]).
14. **Ghost Key Prevention:** TTL queues store timestamps to detect stale entries ([RSK-1304]).
15. **Defensive Time:** Use `checked_duration_since()`, guard interval divisors ([RSK-2504]).
16. **Query Limits:** Apply `.take(limit)` BEFORE `.collect()` ([CTR-1302]).
17. **Audit Completeness:** Use `Vec<T>` not `Option<T>` when multiplicity possible ([CTR-1907]).
18. **Formatting:** `cargo fmt` has been run to ensure consistent style and pass CI ([CTR-2618]).