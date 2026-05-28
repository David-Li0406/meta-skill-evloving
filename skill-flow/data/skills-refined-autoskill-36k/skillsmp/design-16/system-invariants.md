# System Invariants v1.0

Last Updated: 2026-01-19
Purpose: Non-negotiable principles enforced by PRP compiler

---

## Core Philosophy

- Invariants come from pain, not theory
- Violations are **REJECTED**, not fixed
- Spec Delta feeds back into invariants
- Every invariant must have enforcement mechanism

This is a **compiler for human intent**. Specs are programs. Invariants are the type system.

---

## Structure

```
system-invariants.md          ← You are here (Universal Core)
├── domains/
│   ├── consumer-product.md   ← Mobile apps, web apps, consumer-facing
│   ├── physical-construction.md ← Buildings, infrastructure
│   ├── data-architecture.md  ← Pipelines, warehouses, analytics
│   ├── integration.md        ← APIs, webhooks, third-party services
│   ├── remote-management.md  ← Projects managed from distance
│   └── skill-gap-transcendence.md ← Unknown tech, learning-intensive projects
└── enforcement/
    ├── validator.sh          ← Automated invariant checking
    └── violation-messages.md ← Human-readable error templates
```

---

## UNIVERSAL INVARIANTS (Apply to All Domains)

### 1. Ambiguity is Invalid

**Principle**: Every term must have operational definition

**Violation**: Subjective terms without objective criteria

**Examples**:
- ❌ "Process data properly"
- ❌ "Make it user-friendly"
- ❌ "Build with quality materials"
- ✅ "Validate data against schema v2.1, reject if malformed, log to error_queue"
- ✅ "3-tap maximum, <10 sec completion, voice input fallback"
- ✅ "M25 concrete, 28-day cure, compression test ≥25 N/mm²"

**Enforcement**: Regex flags "properly", "easily", "good", "quality", "intuitive" without objective criteria → REJECT

---

### 2. State Must Be Explicit

**Principle**: Every state transition must be documented

**Violation**: Implicit state changes, hidden side effects

**Examples**:
- ❌ "Update user preferences"
- ❌ "Start construction"
- ❌ "Sync data"
- ✅ "user.preferences := {theme: dark} → trigger cache_invalidation → notify_ui"
- ✅ "foundation.state := CURING (28 days) → block column_work → enable inspection_gate"
- ✅ "meal.state := LOGGED → increment daily_total → queue cloudkit_sync if online"

**Enforcement**: Every verb must have: before-state → action → after-state. Missing state declaration → REJECT

---

### 3. Emotional Intent Must Compile

**Principle**: Feelings must map to enforceable mechanisms

**Violation**: Emotion words without implementation spec

**Examples**:
- ❌ "Users should feel confident"
- ❌ "Design should feel premium"
- ❌ "Construction should feel solid"
- ✅ "User confidence := display success_rate (90%+) + show undo_option + provide preview"
- ✅ "Premium feel := haptic_feedback + 60fps_animation + material_shadows"
- ✅ "Structural confidence := engineer_signoff + compression_test_pass + 10yr_warranty"

**Enforcement**: Emotion words (feel, should, comfortable, confident) must be followed by `:=` and concrete mechanism → Otherwise REJECT

---

### 4. No Irreversible Actions Without Recovery

**Principle**: Every destructive action must have escape hatch

**Violation**: Delete/destroy without undo/backup/recovery

**Examples**:
- ❌ "Delete user account"
- ❌ "Pour concrete"
- ❌ "Drop production table"
- ✅ "Delete user account → soft_delete (30-day retention) → hard_delete_after_30d"
- ✅ "Pour concrete → require engineer_approval + test_batch_first + allow 24h for issues"
- ✅ "Drop table → backup_to_s3 + require manual_confirmation + 7-day restore_window"

**Enforcement**: Destructive verbs (delete, drop, remove, destroy, demolish) must specify: recovery mechanism + time window → Otherwise REJECT

---

### 5. Execution Must Fail Loudly

**Principle**: Errors must be observable and actionable

**Violation**: Silent failures, swallowed exceptions, unclear errors

**Examples**:
- ❌ "Handle errors gracefully"
- ❌ "Try to continue if possible"
- ❌ "Log error and move on"
- ✅ "ValidationError → block execution + display specific_failure + require human_decision"
- ✅ "Concrete_slump_test_fail → stop_pour + alert_engineer + document_in_log"
- ✅ "API_timeout → retry 3x + circuit_breaker_open + alert_oncall"

**Enforcement**: Every error path must specify: detection + alerting + blocking behavior. "Gracefully" or "silently" → REJECT

---

### 6. Scope Must Be Bounded

**Principle**: No unbounded operations on files/data/structures

**Violation**: "All", "everything", unlimited iteration

**Examples**:
- ❌ "Process all user records"
- ❌ "Load entire dataset"
- ❌ "Build using all available materials"
- ✅ "Process users in batches of 1000, max 100K records, timeout 5min per batch"
- ✅ "Load last 30 days of data, max 10GB, paginate at 1000 rows"
- ✅ "Use approved_materials_list (15 items), validate availability before spec"

**Enforcement**: Keywords "all", "everything", "entire" must specify: max_count OR max_size OR max_time OR pagination → Otherwise REJECT

---

### 7. Validation Must Be Executable

**Principle**: Success criteria must be measurable by code or process

**Violation**: Subjective validation, human-only checks

**Examples**:
- ❌ "Ensure quality is good"
- ❌ "Verify it looks right"
- ❌ "Confirm structure is sound"
- ✅ "Quality := unit_tests_pass (100%) + coverage ≥80% + lint_score ≥9.0"
- ✅ "Visual correctness := screenshot_diff <2% + accessibility_score ≥90"
- ✅ "Structural soundness := compression_test ≥25 N/mm² + ultrasonic_test_pass"

**Enforcement**: Validation criteria must include: metric + threshold + measurement_method. Subjective terms without metrics → REJECT

---

### 8. Cost Boundaries Must Be Explicit

**Principle**: Every resource consumption must have upper limit

**Violation**: Unbounded API calls, storage, compute, money

**Examples**:
- ❌ "Fetch data from API"
- ❌ "Store user uploads"
- ❌ "Order materials as needed"
- ✅ "API calls: max 1000/day, $10 budget, circuit_breaker at 5 consecutive failures"
- ✅ "Storage: 100MB per user, 10GB total, archive after 90 days"
- ✅ "Materials: ₹15L budget, 10% contingency, approval required >₹50K"

**Enforcement**: External calls, storage, purchases must specify: limit + budget + circuit_breaker → Otherwise REJECT

---

### 9. Blast Radius Must Be Declared

**Principle**: Every operation must state what it affects

**Violation**: Unknown or unspecified impact scope

**Examples**:
- ❌ "Update configuration"
- ❌ "Modify foundation"
- ❌ "Change database schema"
- ✅ "Update config → affects: single_service + restart_required + no_user_impact"
- ✅ "Foundation change → affects: entire_structure + 8-week_delay + ₹2L_rework_cost"
- ✅ "Schema change → affects: 3_services + migration_required + 2hr_downtime"

**Enforcement**: Write operations must declare: affected_scope + dependencies + recovery_cost → Otherwise REJECT

---

### 10. Degradation Path Must Exist

**Principle**: External dependencies must have fallback

**Violation**: Hard dependency without graceful failure

**Examples**:
- ❌ "Fetch weather from API"
- ❌ "Use contractor's materials"
- ❌ "Sync to cloud storage"
- ✅ "Weather API (timeout: 2s) → fallback: cached_last_known → fallback: manual_entry"
- ✅ "Contractor materials → fallback: approved_alternative_list → fallback: client_approval_required"
- ✅ "Cloud sync → fallback: local_queue → fallback: manual_export_csv"

**Enforcement**: External dependencies must specify: primary + fallback1 + fallback2 OR explicit_fail → Otherwise REJECT

---

### 11. Accessibility is Non-Negotiable

**Principle**: All user interfaces must be usable by everyone

**Violation**: UI without accessibility considerations, inaccessible interactions

**Examples**:
- ❌ "Add a button to submit"
- ❌ "Show error in red"
- ❌ "Click to expand details"
- ✅ "Submit button: keyboard_focusable + aria_label + min_touch_target_44px"
- ✅ "Error display: red_text + icon_indicator + aria_live_announce + contrast_ratio_4.5:1"
- ✅ "Expandable section: keyboard_enter_to_toggle + aria_expanded_state + screen_reader_announce"

**Standards**:
- WCAG 2.1 AA as baseline
- Keyboard navigation for all interactions
- Screen reader compatibility (semantic HTML, ARIA labels)
- Color contrast ratio ≥ 4.5:1 for text
- Touch targets ≥ 44x44px on mobile
- No information conveyed by color alone

**Enforcement**: UI components must specify: keyboard_access + screen_reader_support + contrast_compliance. UI without accessibility declaration → REJECT

---

## How Invariants Are Used

| Artifact | Invariant Role |
|----------|----------------|
| Specs | Must not violate any invariant |
| PRPs | Compiler rejects if invariant violated |
| Probes | Can surface invariant violations early |
| Spec Delta | Violations become new invariants |

### Enforcement Layers

```
Layer 1: Static Analysis (Pre-PRP)
  - Parse spec for invariant violations
  - Reject with specific violation message
  - No PRP generation on failure

Layer 2: Execution Probe (Pre-Implementation)
  - Test invariant assumptions in real environment
  - Surface violations early
  - Update spec before full implementation

Layer 3: Runtime Validation (During Implementation)
  - Generated code includes invariant checks
  - Fail loudly on violation
  - Log violation for Spec Delta

Layer 4: Spec Delta (Post-Mortem)
  - Capture new invariant from failure
  - Add to appropriate domain file
  - Validate against historical specs
```

---

## Domain Selection

Choose domains based on project type:

| Project Type | Load These Domains |
|--------------|-------------------|
| Mobile/web app | consumer-product.md |
| iOS calorie tracker | consumer-product.md |
| Data pipeline | data-architecture.md |
| API integration | integration.md |
| House construction | physical-construction.md + remote-management.md |
| LineSheet Pro | consumer-product.md + data-architecture.md + integration.md |
| New tech demo | skill-gap-transcendence.md |
| Stretch assignment | skill-gap-transcendence.md + relevant domain |
| Conference presentation | skill-gap-transcendence.md (invariant 39) |
| Learning-intensive project | skill-gap-transcendence.md |

Multiple domains can be combined. All specs must pass core invariants (1-10) plus selected domain invariants.

---

## Adding New Invariants

New invariants come from Spec Deltas only. Process:

1. Execution failure occurs
2. Spec Delta identifies root cause
3. If cause is a class of problem (not one-off), propose invariant
4. Add to appropriate domain file with:
   - Pain source (incident/failure that triggered it)
   - Violation example
   - Valid example
   - Enforcement mechanism
5. Update validator.sh to enforce

**Never add invariants from theory — only from pain.**

---

## Quick Reference

| # | Invariant | Key Test |
|---|-----------|----------|
| 1 | Ambiguity is Invalid | No "properly", "easily", "quality" without definition |
| 2 | State Must Be Explicit | Every verb has before→action→after |
| 3 | Emotional Intent Must Compile | "Feel X" becomes ":= concrete mechanism" |
| 4 | No Irreversible Without Recovery | Destructive verbs have undo/backup |
| 5 | Execution Must Fail Loudly | No "gracefully" or "silently" |
| 6 | Scope Must Be Bounded | No "all" without limits |
| 7 | Validation Must Be Executable | Metrics + thresholds, not "looks good" |
| 8 | Cost Boundaries Must Be Explicit | Limits on API/storage/money |
| 9 | Blast Radius Must Be Declared | Write ops declare affected scope |
| 10 | Degradation Path Must Exist | External deps have fallbacks |
| 11 | Accessibility is Non-Negotiable | WCAG 2.1 AA, keyboard nav, screen readers |

---

*Last updated: 2026-01-20*
*Core invariants: 11*
*Domain invariants: See domain files*
