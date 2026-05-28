# Invariant Violation Messages

This document defines the error messages, detection patterns, and fix examples for each invariant in the system.

---

## Universal Invariants

### Invariant #1: Ambiguity is Invalid

**Principle:** Every term must have operational definition

**Trigger Words:**
- properly, easily, good, quality, intuitive
- efficiently, effectively, appropriately
- better, improved, optimized
- user-friendly, seamless

**Detection Pattern:**
```bash
# Violation if line contains trigger word WITHOUT explicit definition
# (no := or → or = followed by concrete criteria)
```

**Violation Message:**
```
❌ VIOLATION: Invariant #1 (Ambiguity is Invalid)
   Line {line}: "{text}"
   
Problem: Ambiguous term '{trigger_word}' without operational definition

Why This Matters:
- AI agents will hallucinate implementation
- Humans will interpret differently
- Impossible to validate completion

Fix: Replace with objective criteria
     Format: term := metric + threshold + measurement

Examples:
❌ "Process data properly"
✓ "Process data: validate against schema v2.1 + reject if malformed + log to error_queue"

❌ "Make it user-friendly"
✓ "User-friendly := 3 taps maximum + <10 sec completion + voice input fallback"

❌ "Use quality materials"
✓ "Quality materials: M25 concrete + compression test ≥25 N/mm² + 28-day cure"
```

---

### Invariant #2: State Must Be Explicit

**Principle:** Every state transition must be documented

**Trigger Words:**
- update, change, modify, sync, alter
- set, transform, migrate

**Detection Pattern:**
```bash
# Violation if state change verb appears WITHOUT explicit transition (→)
```

**Violation Message:**
```
❌ VIOLATION: Invariant #2 (State Must Be Explicit)
   Line {line}: "{text}"

Problem: State change without explicit before/after states

Why This Matters:
- Hidden side effects cause debugging nightmares
- AI can't reason about consequences
- Impossible to track system behavior

Fix: Use explicit state transition format
     Format: before_state → action → after_state

Examples:
❌ "Update user preferences"
✓ "user.preferences={} → set_theme(dark) → user.preferences={theme:dark} → cache_invalidate"

❌ "Sync data to cloud"
✓ "local_state=dirty → sync_to_cloud() → local_state=synced + cloud_state=updated"

❌ "Start construction phase"
✓ "foundation.state=COMPLETE → begin_columns → columns.state=IN_PROGRESS + foundation.locked=true"
```

---

### Invariant #3: Emotional Intent Must Compile

**Principle:** Feelings must map to enforceable mechanisms

**Trigger Words:**
- feel, should, comfortable, confident
- happy, satisfied, pleased
- trust, believe, expect

**Detection Pattern:**
```bash
# Violation if emotion word appears WITHOUT compilation mechanism (:=)
```

**Violation Message:**
```
❌ VIOLATION: Invariant #3 (Emotional Intent Must Compile)
   Line {line}: "{text}"

Problem: Emotional goal without concrete implementation

Why This Matters:
- "Should feel X" is unimplementable
- No way to validate success
- AI will generate generic solutions

Fix: Map emotion to concrete mechanism
     Format: emotion := specific_implementation

Examples:
❌ "Users should feel confident"
✓ "User confidence := show_success_rate(90%+) + undo_button + preview_before_commit"

❌ "Design should feel premium"
✓ "Premium feel := haptic_feedback + 60fps_animation + material_shadows + subtle_transitions"

❌ "Construction should feel solid"
✓ "Structural confidence := engineer_signoff + compression_test_pass + 10yr_warranty + visual_inspection"
```

---

### Invariant #4: No Irreversible Actions Without Recovery

**Principle:** Every destructive action must have escape hatch

**Trigger Words:**
- delete, drop, remove, destroy
- demolish, erase, purge, wipe

**Detection Pattern:**
```bash
# Violation if destructive verb WITHOUT recovery terms
# (recovery, undo, backup, restore, retention, soft-delete, rollback)
```

**Violation Message:**
```
❌ VIOLATION: Invariant #4 (No Irreversible Actions Without Recovery)
   Line {line}: "{text}"

Problem: Destructive action without recovery mechanism

Why This Matters:
- Mistakes happen in production
- Irreversible = catastrophic loss
- No way to fix accidental deletions

Fix: Specify recovery mechanism with time window

Examples:
❌ "Delete user account"
✓ "Delete user account → soft_delete(30-day retention) → hard_delete_after_30d"

❌ "Pour concrete"
✓ "Pour concrete → test_batch_first + engineer_approval + 24hr_issue_window"

❌ "Drop production table"
✓ "Drop table → backup_to_s3 + manual_confirmation + 7-day_restore_window"
```

---

### Invariant #5: Execution Must Fail Loudly

**Principle:** Errors must be observable and actionable

**Trigger Words:**
- gracefully, silently
- try to continue, handle quietly
- suppress error

**Detection Pattern:**
```bash
# Violation if silent failure pattern detected
```

**Violation Message:**
```
❌ VIOLATION: Invariant #5 (Execution Must Fail Loudly)
   Line {line}: "{text}"

Problem: Silent or graceful failure mode

Why This Matters:
- Silent failures hide problems
- Errors compound over time
- Impossible to debug production issues

Fix: Specify loud failure behavior
     Format: error_detection + alerting + blocking_behavior

Examples:
❌ "Handle errors gracefully"
✓ "ValidationError → block_execution + display_specific_failure + require_human_decision"

❌ "Try to continue if possible"
✓ "API_failure → stop_immediately + alert_oncall + log_full_context + return_error_to_user"

❌ "Silently skip invalid records"
✓ "Invalid_record → halt_batch + alert_data_team + log_to_error_queue + manual_review_required"
```

---

### Invariant #6: File Scope Must Be Bounded

**Principle:** No unbounded operations on files/data/structures

**Trigger Words:**
- all, everything, entire, every
- complete, total, whole

**Detection Pattern:**
```bash
# Violation if unbounded term WITHOUT bounds specification
# (max, limit, bounded, paginated, first N, top N, last N)
```

**Violation Message:**
```
❌ VIOLATION: Invariant #6 (File Scope Must Be Bounded)
   Line {line}: "{text}"

Problem: Unbounded operation detected

Why This Matters:
- "All" can mean millions of records
- Out of memory errors
- Infinite loops
- Timeouts and system crashes

Fix: Specify bounds
     Format: max_count OR max_size OR max_time OR pagination

Examples:
❌ "Process all user records"
✓ "Process users: batch_size=1000 + max_100K_records + timeout_5min_per_batch"

❌ "Load entire dataset"
✓ "Load data: last_30_days + max_10GB + paginate_at_1000_rows"

❌ "Build using all available materials"
✓ "Materials: approved_list(15 items) + validate_availability + budget_cap_₹15L"
```

---

### Invariant #7: Validation Must Be Executable

**Principle:** Success criteria must be measurable by code or process

**Trigger Words:**
- ensure, verify, confirm, check
- validate, guarantee

**Detection Pattern:**
```bash
# Violation if validation verb WITHOUT executable criteria
# (no metrics, thresholds, test methods, measurements)
```

**Violation Message:**
```
❌ VIOLATION: Invariant #7 (Validation Must Be Executable)
   Line {line}: "{text}"

Problem: Non-executable validation criteria

Why This Matters:
- Subjective validation = inconsistent results
- No way to automate testing
- Can't verify completion

Fix: Specify executable validation
     Format: metric + threshold + measurement_method

Examples:
❌ "Ensure quality is good"
✓ "Quality := unit_tests_pass(100%) + coverage≥80% + lint_score≥9.0"

❌ "Verify it looks right"
✓ "Visual correctness := screenshot_diff<2% + accessibility_score≥90 + manual_review"

❌ "Confirm structure is sound"
✓ "Structural soundness := compression_test≥25N/mm² + ultrasonic_test_pass + engineer_signoff"
```

---

### Invariant #8: Cost Boundaries Must Be Explicit

**Principle:** Every resource consumption must have upper limit

**Detection Pattern:**
```bash
# Warning if API calls or storage detected WITHOUT cost boundaries
# (max requests, rate limit, budget, storage limit)
```

**Violation Message:**
```
⚠️  WARNING: Cost Boundaries Should Be Explicit
    {context}

Problem: Resource consumption without limits

Why This Matters:
- Unbounded API calls = budget explosion
- Runaway storage = surprise bills
- No circuit breakers = cascading failures

Fix: Specify cost boundaries
     Format: max_requests + budget + circuit_breaker

Examples:
❌ "Fetch data from API"
✓ "API calls: max_1000/day + $10_budget + circuit_breaker_at_5_failures"

❌ "Store user uploads"
✓ "Storage: 100MB_per_user + 10GB_total + archive_after_90days"

❌ "Order materials as needed"
✓ "Materials: ₹15L_budget + 10%_contingency + approval_required_>₹50K"
```

---

### Invariant #9: Blast Radius Must Be Declared

**Principle:** Every operation must state what it affects

**Detection Pattern:**
```bash
# Warning if write operation WITHOUT blast radius declaration
# (affects, impacts, scope, radius, consequences)
```

**Violation Message:**
```
⚠️  WARNING: Blast Radius Should Be Declared
    Line {line}: Write operation detected

Problem: Unknown impact scope

Why This Matters:
- Changes can cascade unexpectedly
- No way to assess risk
- Impossible to plan rollbacks

Fix: Declare blast radius
     Format: affected_scope + dependencies + recovery_cost

Examples:
❌ "Update configuration"
✓ "Update config → affects:single_service + restart_required + no_user_impact"

❌ "Modify foundation"
✓ "Foundation change → affects:entire_structure + 8wk_delay + ₹2L_rework_cost"

❌ "Change database schema"
✓ "Schema change → affects:3_services + migration_required + 2hr_downtime"
```

---

### Invariant #10: Degradation Path Must Exist

**Principle:** External dependencies must have fallback

**Detection Pattern:**
```bash
# Warning if external dependency WITHOUT fallback
# (fallback, backup, alternative, degraded, cached, timeout)
```

**Violation Message:**
```
⚠️  WARNING: Degradation Path Should Be Explicit
    Line {line}: External dependency detected

Problem: Hard dependency without graceful failure

Why This Matters:
- External services fail
- Network issues happen
- No fallback = complete system failure

Fix: Specify degradation path
     Format: primary + fallback1 + fallback2 OR explicit_fail

Examples:
❌ "Fetch weather from API"
✓ "Weather: API(timeout:2s) → fallback:cached_last_known → fallback:manual_entry"

❌ "Use contractor's materials"
✓ "Materials: contractor_supplied → fallback:approved_alternatives → fallback:client_approval"

❌ "Sync to cloud storage"
✓ "Cloud sync: primary_upload → fallback:local_queue → fallback:manual_export_csv"
```

---

## Domain-Specific Invariants

### Consumer Product Domain

#### Invariant #11: User Emotion Must Map to Affordance

**Detection Pattern:**
```bash
# Warning if user emotion mentioned WITHOUT UI affordance
```

**Violation Message:**
```
⚠️  WARNING: User Emotion Without UI Mapping

Problem: Emotional goal without concrete UI implementation

Fix: Map emotion to UI elements
     Format: emotion := visual + interaction + feedback

Examples:
❌ "Users feel accomplished"
✓ "Accomplishment := green_checkmark + haptic_feedback + animation(0.3s)"

❌ "Users feel confident"
✓ "Confidence := preview_before_action + undo_button(5min) + success_rate_display"
```

#### Invariant #12: Behavioral Friction Must Be Quantified

**Detection Pattern:**
```bash
# Warning if ease/friction mentioned WITHOUT quantification
# (tap count, time, steps)
```

**Violation Message:**
```
⚠️  WARNING: Friction Not Quantified

Problem: "Easy" without measurable interaction cost

Fix: Quantify friction
     Format: tap_count + time_limit + input_method

Examples:
❌ "Make logging easy"
✓ "Easy := max_3_taps + <10_sec_completion + voice_input_option"

❌ "Simplify the workflow"
✓ "Simple := single_screen + zero_config + auto_prefill"
```

#### Invariant #13: Accessibility Must Be Explicit

**Detection Pattern:**
```bash
# Warning if UI elements WITHOUT accessibility declaration
```

**Violation Message:**
```
⚠️  WARNING: Accessibility Not Declared

Problem: UI without accessibility compliance

Fix: Declare accessibility standards
     Format: WCAG_level + platform_support + specific_requirements

Examples:
❌ "Create login screen"
✓ "Login: WCAG_AA + VoiceOver_labels + dynamic_type + 44pt_touch_targets"

❌ "Show meal list"
✓ "Meal list: color_contrast≥4.5:1 + screen_reader_order + reduced_motion_fallback"
```

#### Invariant #14: Offline Behavior Must Be Defined

**Detection Pattern:**
```bash
# Warning if network operations WITHOUT offline behavior
```

**Violation Message:**
```
⚠️  WARNING: Offline Behavior Not Defined

Problem: Network-dependent feature assumes always-online

Why This Matters:
- Mobile users lose connectivity
- Airplane mode, tunnels, poor coverage
- Data loss if not handled

Fix: Define offline strategy
     Format: local_first + queue_when_offline + sync_strategy + conflict_resolution

Examples:
❌ "Sync meal data"
✓ "Meal sync: local_first → queue_when_offline → sync_when_connected + conflict(last_write_wins)"

❌ "Save to cloud"
✓ "Cloud save: immediate_local_write → background_sync + retry_3x + show_sync_status"
```

#### Invariant #15: Loading States Must Be Bounded

**Detection Pattern:**
```bash
# Warning if loading states WITHOUT timeout bounds
```

**Violation Message:**
```
⚠️  WARNING: Loading States Unbounded

Problem: Loading/spinner without timeout limit

Why This Matters:
- Infinite spinners frustrate users
- No way to recover from stuck states
- Users abandon app

Fix: Bound all loading states
     Format: max_duration + timeout_behavior + recovery_option

Examples:
❌ "Show loading spinner"
✓ "Loading: spinner(max_5s) → timeout_error + retry_option + offline_fallback"

❌ "Wait for response"
✓ "Response wait: 3s_spinner → 10s_timeout → cached_data_option"

❌ "Loading..."
✓ "Data fetch: skeleton_ui(immediate) → content(max_3s) → timeout_message + manual_refresh"
```

---

### Physical Construction Domain

#### Invariant #16: Material Properties Must Be Climate-Validated

**Detection Pattern:**
```bash
# Warning if materials specified WITHOUT climate validation
```

**Violation Message:**
```
⚠️  WARNING: Materials Not Climate-Validated

Problem: Materials without environmental validation

Fix: Validate for local climate
     Format: material + climate_properties + test_validation

Examples:
❌ "Use exterior paint"
✓ "Paint: heat_resistant(≤50°C) + humidity_resistant(≤95%) + salt_resistant → Asian_Paints_WeatherProof"

❌ "Install wooden doors"
✓ "Doors: teak + termite_treatment + monsoon_seal + UV_coating + coastal_experience_verified"
```

#### Invariant #17: Vendor Capabilities Must Be Validated

**Detection Pattern:**
```bash
# Warning if contractor/vendor WITHOUT capability validation
```

**Violation Message:**
```
⚠️  WARNING: Vendor Capabilities Not Validated

Problem: Contractor specified without capability verification

Why This Matters:
- Unqualified work leads to failures
- Rework costs time and money
- No recourse without documentation

Fix: Validate vendor capabilities
     Format: certification + past_projects + insurance + references

Examples:
❌ "Install waterproofing system"
✓ "Waterproofing: contractor_certification(Fosroc) + past_coastal_projects(3+) + warranty_10yr + insurance"

❌ "Lay Italian marble"
✓ "Marble: contractor_marble_experience(5yr+) + reference_projects(2) + insurance_coverage"
```

#### Invariant #18: Temporal Constraints Must Account for Climate

**Detection Pattern:**
```bash
# Warning if schedule WITHOUT climate/season consideration
```

**Violation Message:**
```
⚠️  WARNING: Schedule Ignores Climate

Problem: Construction schedule without weather consideration

Why This Matters:
- Monsoon stops work for months
- Concrete needs dry curing time
- Material delivery affected by season

Fix: Include climate in scheduling
     Format: season_constraints + weather_buffers + monsoon_plan

Examples:
❌ "Start construction in June"
✓ "Start: post-monsoon(Oct-Nov) + pre-summer(before_March) → window: Oct15-Feb28"

❌ "Complete in 6 months"
✓ "Duration: 6mo_base + 2mo_monsoon_buffer + 1mo_material_delay = 9mo_total"

❌ "Foundation by December"
✓ "Foundation: complete_before_monsoon(May) + 28-day_cure_buffer + inspection_gate"
```

#### Invariant #19: Inspection Gates Must Be Explicit

**Detection Pattern:**
```bash
# Warning if construction phases WITHOUT inspection gates
```

**Violation Message:**
```
⚠️  WARNING: No Inspection Gates Specified

Problem: Construction phases without validation checkpoints

Fix: Define inspection protocol
     Format: who_inspects + test_criteria + pass/fail_actions

Examples:
❌ "Complete foundation"
✓ "Foundation: structural_engineer_signoff + compression_test(≥25N/mm²) + photo_docs → PASS:proceed | FAIL:remediate"

❌ "Waterproofing done"
✓ "Waterproofing: independent_inspector + water_test(24hr) + warranty_activation → FAIL:redo_at_contractor_cost"
```

#### Invariant #20: Material Failure Modes Must Be Documented

**Detection Pattern:**
```bash
# Warning if critical materials WITHOUT failure mode documentation
```

**Violation Message:**
```
⚠️  WARNING: Material Failure Modes Not Documented

Problem: Critical materials without failure analysis

Why This Matters:
- Unknown failure = unknown risk
- Recovery costs unknown until too late
- No early warning system

Fix: Document failure modes
     Format: failure_mode + detection_method + recovery_cost

Examples:
❌ "Use M25 concrete for foundation"
✓ "M25 concrete: failure_mode(insufficient_strength) → detection(compression_test) → recovery(demolish+repour, ₹8L, +8wk)"

❌ "Install marble flooring"
✓ "Marble: failure_mode(cracking) → detection(visual) → recovery(replace_section, ₹2L, +2wk)"

❌ "Apply waterproof coating"
✓ "Waterproofing: failure_mode(leakage) → detection(monsoon_test) → recovery(reapply, ₹50K, +1wk)"
```

#### Invariant #21: Supply Chain Must Be Stress-Tested

**Detection Pattern:**
```bash
# Warning if specialty materials WITHOUT supply chain fallbacks
```

**Violation Message:**
```
⚠️  WARNING: Supply Chain Not Stress-Tested

Problem: Specialty materials without sourcing validation

Why This Matters:
- Import delays halt construction
- Single supplier = single point of failure
- Storage needs often overlooked

Fix: Validate supply chain
     Format: lead_time + risks + fallbacks + storage

Examples:
❌ "Use Italian marble"
✓ "Italian marble: lead_time(8wk) + monsoon_shipping_risk + storage(dry_warehouse) → fallback: Rajasthani_marble(2wk)"

❌ "Install imported fixtures"
✓ "Fixtures: local_availability_verified + 2_supplier_quotes + 4wk_delivery → fallback: alternative_equivalent"

❌ "Source specialty lumber"
✓ "Teak doors: supplier_confirmed + advance_booking(12wk) + storage_at_site → fallback: local_hardwood"
```

---

### Data Architecture Domain

#### Invariant #22: Schema Evolution Must Be Explicit

**Detection Pattern:**
```bash
# Violation if schema change WITHOUT migration path
```

**Violation Message:**
```
❌ VIOLATION: Invariant #22 (Schema Evolution Must Be Explicit)

Problem: Schema change without migration strategy

Why This Matters:
- Data loss during migration
- Incompatible versions in production
- Rollback impossible without plan

Fix: Specify migration path
     Format: migration_approach + validation + rollback_plan

Examples:
❌ "Add user_preferences column"
✓ "Add user_preferences JSONB: default={} + backfill_strategy(lazy_on_read) + index_after_50%_backfill"

❌ "Change data type to JSON"
✓ "Change to JSON: migrate_script.sql + validation_query + rollback_plan + zero_downtime(blue_green)"

❌ "Remove deprecated field"
✓ "Remove deprecated_field: null_for_6mo → drop_after_verification + downstream_impact(none)"
```

#### Invariant #23: Data Lineage Must Be Traceable

**Detection Pattern:**
```bash
# Warning if derived values WITHOUT source lineage
```

**Violation Message:**
```
⚠️  WARNING: Data Lineage Not Traceable

Problem: Calculated field without source documentation

Why This Matters:
- Can't debug incorrect values
- Can't audit data quality
- Can't reproduce calculations

Fix: Document lineage
     Format: source_tables + transformation_logic + time_window

Examples:
❌ "Display calculated_score"
✓ "calculated_score = sum(item_scores) FROM items WHERE user_id=X AND created_at > now()-30d"

❌ "Show aggregated metrics"
✓ "monthly_active_users = COUNT(DISTINCT user_id) FROM events WHERE event_date BETWEEN start_of_month AND end_of_month"
```

#### Invariant #24: Aggregation Scope Must Be Bounded

**Detection Pattern:**
```bash
# Warning if aggregation WITHOUT cardinality bounds
```

**Violation Message:**
```
⚠️  WARNING: Aggregation Scope Unbounded

Problem: Aggregation without cardinality limits

Why This Matters:
- Unbounded GROUP BY = OOM errors
- Query timeouts in production
- Cost explosion on cloud

Fix: Bound aggregations
     Format: time_bound + row_limit + timeout

Examples:
❌ "Show all user events"
✓ "User events: last_1000 + paginated(50_per_page) + index_on(user_id, timestamp)"

❌ "Aggregate by user"
✓ "Aggregate by user: WHERE created_at > now()-90d + max_10M_rows + timeout_5min"

❌ "Join all tables"
✓ "Join: max_cardinality(1M_rows) + partition_by(date) + fallback(sample_10%)"
```

#### Invariant #25: Temporal Semantics Must Be Explicit

**Detection Pattern:**
```bash
# Warning if time-based query WITHOUT timezone/granularity
```

**Violation Message:**
```
⚠️  WARNING: Temporal Semantics Implicit

Problem: Time-based query without timezone specification

Why This Matters:
- "Daily" means different things in different timezones
- Deduplication fails without clear boundaries
- Reports show inconsistent numbers

Fix: Specify temporal semantics
     Format: timezone + boundary_definition + deduplication

Examples:
❌ "Show daily active users"
✓ "Daily active users: UTC_day_boundaries + dedupe_by(user_id) + created_at_index"

❌ "Calculate retention"
✓ "7-day retention: cohort_day_0(UTC) → active_on_day_7(UTC) → percentage_calculation"

❌ "Get recent orders"
✓ "Recent orders: last_24h(user_local_timezone) + display_in(user_timezone) + store_in(UTC)"
```

#### Invariant #26: PII Must Be Declared and Protected

**Detection Pattern:**
```bash
# Violation if personal data WITHOUT protection declaration
```

**Violation Message:**
```
❌ VIOLATION: Invariant #26 (PII Must Be Declared and Protected)

Problem: Personal data without protection measures

Why This Matters:
- Legal liability (GDPR, CCPA)
- Data breach exposure
- Audit failures

Fix: Declare and protect PII
     Format: PII_tag + encryption + access_control + retention_policy

Examples:
❌ "Store user email"
✓ "user_email: PII + encrypted_at_rest(AES256) + access_control(admin_only) + audit_log"

❌ "Log user activity"
✓ "user_activity: PII_anonymized + user_id_hashed + ip_truncated + no_full_payload"

❌ "Track user location"
✓ "user_location: PII + precision_reduced(city_level) + retention(30d) + consent_required"
```

---

### Integration Domain

#### Invariant #27: API Versioning Must Be Explicit

**Detection Pattern:**
```bash
# Warning if API WITHOUT versioning strategy
```

**Violation Message:**
```
⚠️  WARNING: API Versioning Not Explicit

Problem: API endpoint without version strategy

Why This Matters:
- Breaking changes break clients
- No deprecation path
- Migration chaos

Fix: Declare versioning strategy
     Format: version + backwards_compatibility + deprecation_timeline

Examples:
❌ "Create user endpoint"
✓ "POST /v2/users: version_header(X-API-Version) + sunset_date(v1: 2025-06-01) + migration_guide_url"

❌ "Update API response format"
✓ "Response format change: v2_only + v1_unchanged + 90_day_deprecation_notice + changelog_entry"
```

#### Invariant #28: Rate Limits Must Be Declared

**Detection Pattern:**
```bash
# Violation if external API WITHOUT rate handling
```

**Violation Message:**
```
❌ VIOLATION: Invariant #28 (Rate Limits Must Be Declared)

Problem: External API call without rate limit handling

Why This Matters:
- 429 errors crash your app
- No backoff = blocked by provider
- Costs spiral without limits

Fix: Declare rate handling
     Format: rate_limit + backoff_strategy + failure_handling

Examples:
❌ "Call external API"
✓ "External API: 100_req/min + exponential_backoff(1s,2s,4s,max_30s) + circuit_breaker(5_failures) + fallback(cached_data)"

❌ "Fetch data from service"
✓ "Data fetch: rate_limit_aware + 429_handling(retry_after_header) + queue_overflow(drop_oldest)"

❌ "Send webhook notifications"
✓ "Webhooks: batch_max_100 + retry_3x_with_backoff + dead_letter_queue + manual_retry_ui"
```

#### Invariant #29: Idempotency Must Be Guaranteed

**Detection Pattern:**
```bash
# Warning if mutating operation WITHOUT idempotency mechanism
```

**Violation Message:**
```
⚠️  WARNING: Idempotency Not Guaranteed

Problem: Retryable operation may produce duplicates

Why This Matters:
- Network retries create duplicates
- Double charges, double orders
- Data corruption

Fix: Guarantee idempotency
     Format: idempotency_mechanism + dedup_strategy + retry_behavior

Examples:
❌ "Create order on submit"
✓ "Create order: idempotency_key(client_generated_uuid) + dedup_window(24h) + same_response_on_retry"

❌ "Send confirmation email"
✓ "Confirmation email: idempotency_key(order_id+email_type) + sent_flag_check + no_duplicate_sends"

❌ "Charge payment"
✓ "Payment charge: idempotency_key(order_id) + stripe_idempotency_header + verify_before_retry"
```

#### Invariant #30: Timeout Budgets Must Be Allocated

**Detection Pattern:**
```bash
# Warning if request chain WITHOUT timeout budget
```

**Violation Message:**
```
⚠️  WARNING: Timeout Budget Not Allocated

Problem: Request chain without timeout distribution

Why This Matters:
- Cascading timeouts
- Stuck requests hold resources
- User waits forever

Fix: Allocate timeout budget
     Format: total_budget + per_hop_allocation + timeout_behavior

Examples:
❌ "Call service A then B then C"
✓ "Chain A→B→C: total_budget(5s) → A(2s) → B(2s) → C(1s) + fail_fast_on_timeout + partial_response_ok"

❌ "Wait for external response"
✓ "External response: timeout(3s) + cancel_on_timeout + return_cached_or_error"

❌ "Aggregate from multiple sources"
✓ "Multi-source: parallel_fetch + per_source_timeout(2s) + return_available_on_any_timeout"
```

---

### Remote Management Domain

#### Invariant #31: Inspection Must Be Independent

**Detection Pattern:**
```bash
# Violation if remote project WITHOUT independent verification
```

**Violation Message:**
```
❌ VIOLATION: Invariant #31 (Inspection Must Be Independent)

Problem: Remote project relying solely on executor for status

Why This Matters:
- Contractor won't report own mistakes
- Problems hidden until too late
- No objective verification

Fix: Establish independent inspection
     Format: independent_verification_source + frequency + reporting_format

Examples:
❌ "Contractor will send photos"
✓ "Independent inspector: monthly_site_visit + photo_documentation + video_call_walkthrough + written_report"

❌ "Trust the site supervisor"
✓ "Dual verification: contractor_photos + independent_photos + discrepancy_review"

❌ "They'll let us know if there are issues"
✓ "Third-party QC: structural_engineer(quarterly) + waterproofing_specialist(at_milestone) + surprise_visits(random)"
```

#### Invariant #32: Communication Protocol Must Be Explicit

**Detection Pattern:**
```bash
# Warning if stakeholders WITHOUT communication protocol
```

**Violation Message:**
```
⚠️  WARNING: Communication Protocol Not Explicit

Problem: Ad-hoc communication with stakeholders

Why This Matters:
- Messages lost in wrong channels
- No escalation when stuck
- Response time unpredictable

Fix: Define communication protocol
     Format: primary_channel + backup_channel + response_SLA + escalation_path

Examples:
❌ "Stay in touch with contractor"
✓ "Contractor: WhatsApp_daily_photo(6PM_IST) + weekly_video_call(Saturday_10AM_IST) + email_for_decisions"

❌ "Regular updates"
✓ "Architect: bi-weekly_review + milestone_signoff_required + 48hr_response_SLA"

❌ "Call if there are problems"
✓ "Escalation: issue_in_chat → no_response_24hr → phone_call → no_response_48hr → site_visit_triggered"
```

#### Invariant #33: Payment Must Be Milestone-Gated

**Detection Pattern:**
```bash
# Violation if payment WITHOUT milestone gate
```

**Violation Message:**
```
❌ VIOLATION: Invariant #33 (Payment Must Be Milestone-Gated)

Problem: Payment not tied to verified deliverables

Why This Matters:
- Money released before work verified
- No leverage for quality issues
- Contractor disappears with advance

Fix: Gate payments to milestones
     Format: trigger_condition + verification_method + approval_required

Examples:
❌ "Pay monthly"
✓ "Foundation payment: 30% on completion + independent_inspection_pass + compression_test_report + photo_documentation"

❌ "Release funds as needed"
✓ "Material advance: 50% on PO + 50% on delivery_verification(photo+receipt) + quality_check_passed"

❌ "Pay on contractor's request"
✓ "Milestone release: checklist_complete + inspector_signoff + owner_approval_in_writing → payment_within_48hr"
```

#### Invariant #34: Decision Authority Must Be Delegated Explicitly

**Detection Pattern:**
```bash
# Warning if decision-making WITHOUT authority delegation
```

**Violation Message:**
```
⚠️  WARNING: Decision Authority Not Delegated

Problem: Unclear who can decide what

Why This Matters:
- Work stops waiting for owner
- Or wrong decisions made without approval
- No accountability

Fix: Delegate authority explicitly
     Format: authority_level + threshold + documentation_requirement

Examples:
❌ "Check with me for changes"
✓ "On-site authority: changes <₹10K + no_structural_impact + reversible → proceed_and_inform"

❌ "Use your judgment"
✓ "Owner required: changes >₹10K OR structural OR permanent → stop_work + await_approval(max_48hr)"

❌ "Handle minor issues"
✓ "Emergency protocol: safety_risk → immediate_action_allowed + document_thoroughly + inform_within_2hr"
```

#### Invariant #35: Documentation Must Be Timestamped and Immutable

**Detection Pattern:**
```bash
# Warning if documentation WITHOUT timestamp/immutability
```

**Violation Message:**
```
⚠️  WARNING: Documentation Not Timestamped/Immutable

Problem: Records can be altered, dates unclear

Why This Matters:
- Disputes become he-said-she-said
- Can't prove when issues occurred
- Evidence tampering possible

Fix: Ensure timestamped, immutable records
     Format: timestamp_source + immutability_mechanism + storage_location

Examples:
❌ "Keep records of progress"
✓ "Photos: GPS_tagged + timestamp_verified + uploaded_to_shared_drive_daily + no_deletion_allowed"

❌ "Document issues"
✓ "Decisions: email_thread(immutable) + decision_log(append_only) + version_history_preserved"

❌ "Take photos"
✓ "Issues: logged_in_tracker + timestamp_auto + status_changes_tracked + resolution_documented"
```

#### Invariant #36: Contingency Must Account for Physical Distance

**Detection Pattern:**
```bash
# Warning if contingency WITHOUT local agent
```

**Violation Message:**
```
⚠️  WARNING: Contingency Ignores Physical Distance

Problem: Fallback plan requires owner presence

Why This Matters:
- Can't fly out for every emergency
- 24+ hour travel time
- Visa/scheduling constraints

Fix: Plan contingencies that work remotely
     Format: local_agent + authority_scope + financial_access + dispute_resolution

Examples:
❌ "I'll fly out if needed"
✓ "Emergency contact: local_trusted_person(Dad) + authority_to_act + ₹2L_emergency_fund_access"

❌ "Handle emergencies as they come"
✓ "Contractor failure: backup_contractor_identified + contract_termination_clause + material_ownership_clear"

❌ "We'll figure it out"
✓ "Quality dispute: independent_arbitrator_named + dispute_resolution_process + escrow_for_contested_amounts"
```

---

### Skill Gap Transcendence Domain

#### Invariant #37: Skill Gaps Force Explicit Learning Budget

**Detection Pattern:**
```bash
# Violation if new technology WITHOUT learning budget
```

**Violation Message:**
```
❌ VIOLATION: Invariant #37 (Skill Gaps Force Explicit Learning Budget)

Problem: New technology without learning time budgeted

Why This Matters:
- Unknown unknowns cause project failure
- Learning time not budgeted = timeline slip
- No fallback plan when learning takes longer

Fix: Budget learning time explicitly
     Format: learning_time_budget + scope_tradeoff_if_exceeded + validation_criteria

Examples:
❌ "Build React dashboard"
✓ "React dashboard:
    REQUIRED: React_hooks(5/5) + state_management(5/5)
    CURRENT: React(0/5) + state(0/5)
    LEARNING: 40hrs + 20hrs = 60hrs
    RISK: High (learning > 50% of timeline)
    DECISION: Pivot to Python_Flask (known stack)"

❌ "Learn Kubernetes by Friday"
✓ "Kubernetes learning: 20hr_budget + validation(deploy_hello_world) + IF_fails(use_docker_compose_fallback)"
```

#### Invariant #38: Support Structure Must Be Pre-Defined

**Detection Pattern:**
```bash
# Warning if skill gap WITHOUT support structure
```

**Violation Message:**
```
⚠️  WARNING: Support Structure Not Defined

Problem: Skill gap without plan for getting unstuck

Why This Matters:
- Stuck for hours without asking for help
- No escalation = silent failure
- "Should have asked" blame after the fact

Fix: Pre-define support structure
     Format: primary_resource + escalation_timing + pivot_criteria

Examples:
❌ "Ask for help if stuck"
✓ "Blocker protocol: 2hr_self_study → 2hr_docs → ask_team → ask_manager → request_scope_change"

❌ "Figure it out"
✓ "Learning support: mentor_identified(Sarah) + office_hours(Tue/Thu) + pivot_criteria(can't_validate_in_2d)"
```

#### Invariant #39: Demos Require Triple-Backup Protocol

**Detection Pattern:**
```bash
# Violation if demo WITHOUT fallback protocol
```

**Violation Message:**
```
❌ VIOLATION: Invariant #39 (Demos Require Triple-Backup Protocol)

Problem: Public demo with single path to success

Why This Matters:
- Live demos fail at worst moments
- No recovery = public embarrassment
- Stress compounds skill gap problems

Fix: Define triple-backup protocol
     Format: primary + fallback_1(pre-recorded) + fallback_2(slides) + confidence_check_date

Examples:
❌ "Demo the new feature live"
✓ "Demo protocol:
    PRIMARY: live_demo
    FALLBACK_1: pre_recorded_video(record_when_working)
    FALLBACK_2: slides_with_screenshots
    FALLBACK_3: alternative_simpler_demo
    CONFIDENCE_GATE: 1_week_before → rehearsal → go/no-go"

❌ "It'll work on the day"
✓ "Demo insurance: record_working_version_daily + slides_always_current + backup_laptop_ready"
```

#### Invariant #40: Health Signals Trigger Scope Adjustment

**Detection Pattern:**
```bash
# Warning if high-pressure project WITHOUT health protocol
```

**Violation Message:**
```
⚠️  WARNING: Health Signals Not Monitored

Problem: High-pressure project without health safeguards

Why This Matters:
- Stress affects learning ability
- Burnout makes everything harder
- Health cost outlasts project

Fix: Define health signal protocol
     Format: health_triggers + adjustment_protocol + escalation_path

Examples:
❌ "Just push through"
✓ "Health triggers: sleep_disruption(2+nights) OR physical_symptoms OR anxiety_interfering → trigger_scope_reduction"

❌ "It's only temporary stress"
✓ "Adjustment protocol: document_symptoms + identify_stress_sources + propose_targeted_scope_cut + escalate_if_denied"

❌ "I'll rest after the deadline"
✓ "Monitoring: daily_checkin(am_I_dreading_this?) + weekly_assessment + sustainable_pace_non_negotiable"
```

#### Invariant #41: Fixed Deadlines Require Tiered Scope

**Detection Pattern:**
```bash
# Warning if fixed deadline WITHOUT scope tiers
```

**Violation Message:**
```
⚠️  WARNING: Fixed Deadline Without Tiered Scope

Problem: Immovable date with fixed scope

Why This Matters:
- Something has to give
- Last-minute cuts look like failure
- No proactive decision-making

Fix: Define tiered scope upfront
     Format: MVP(must_ship) + stretch(if_time) + optional(first_to_drop) + checkpoint

Examples:
❌ "Complete for Immersion Day (May 15)"
✓ "Immersion Day (May 15, FIXED):
    MVP: basic_search_working
    STRETCH: dashboard_if_time
    CAN_DROP: observability_module
    DECISION_GATE: May_1 (assess + adjust)"

❌ "Deliver everything by conference"
✓ "Conference demo: tier_1(core_demo_works) + tier_2(handles_questions) + tier_3(polished_UI) → checkpoint_2wk_before"
```

#### Invariant #42: Learning Time Is First-Class Work

**Detection Pattern:**
```bash
# Warning if learning NOT scheduled as explicit work
```

**Violation Message:**
```
⚠️  WARNING: Learning Time Not Scheduled

Problem: Learning treated as overhead, not real work

Why This Matters:
- "Why aren't you building yet?" pressure
- Learning happens in stolen moments
- No validation of understanding

Fix: Schedule learning as first-class work
     Format: scheduled_explicitly + validation_deliverable + proceed_only_after_pass

Examples:
❌ "Learn on your own time"
✓ "Learning phase: Mon-Wed(scheduled) + validation(build_throwaway_prototype) + proceed_only_after_pass"

❌ "You should know this already"
✓ "Learning status: 'in_learning_phase' = valid_status + expected_duration(3d) + manager_aware"

❌ "Figure it out while building"
✓ "Validation gate: build_minimal_proof → if_pass(proceed) → if_fail(trigger_scope_reduction)"
```

#### Invariant #43: Discovery Phase Required for Unknowns

**Detection Pattern:**
```bash
# Warning if unknown territory WITHOUT discovery phase
```

**Violation Message:**
```
⚠️  WARNING: Discovery Phase Not Allocated

Problem: Commitment before exploration

Why This Matters:
- Estimates without understanding = wrong
- Unknown unknowns discovered too late
- No room to adjust

Fix: Allocate discovery phase
     Format: discovery_allocation(20%_of_timeline) + prototype_requirement + re-estimation_gate

Examples:
❌ "Estimate the project now"
✓ "Discovery phase: 20%_of_timeline + spike_deliverable + re-estimation_after + scope_adjustment_expected"

❌ "Commit to the timeline upfront"
✓ "Commitment model: soft_commit(before_discovery) → hard_commit(after_discovery) → flexibility_preserved"

❌ "We need certainty before starting"
✓ "Discovery output: minimal_prototype + unknowns_list + revised_timeline + adjusted_scope_proposal"
```

---

## How to Use These Messages

### For Spec Authors

When the validator reports a violation:

1. **Read the "Why This Matters" section** - Understand the impact
2. **Look at the "Fix" format** - See what structure is needed
3. **Review the examples** - See correct vs incorrect patterns
4. **Apply the fix** - Rewrite the offending line
5. **Re-run validator** - Confirm violation is resolved

### For Validator Maintainers

When adding new invariants:

1. Define clear **trigger patterns** (words, phrases)
2. Write **detection logic** (what to grep for)
3. Create **helpful error message** (problem + why + fix)
4. Provide **concrete examples** (❌ bad, ✓ good)
5. Test against **real specs** (both pass and fail cases)

---

## Violation Severity Levels

### ❌ VIOLATION (Exit Code 1 - Blocks Compilation)

These violations make the spec uncompilable:
- Ambiguity without definition
- State changes without transitions
- Emotional intent without mechanism
- Destructive actions without recovery
- Silent failure modes
- Unbounded operations
- Non-executable validation
- Skill gaps without declaration

**Action Required:** Fix before proceeding

### ⚠️ WARNING (Exit Code 0 - Compilation Proceeds)

These are strong recommendations but not blocking:
- Cost boundaries missing
- Blast radius undeclared
- Degradation paths missing
- Domain-specific guidance

**Action Recommended:** Address before production

---

## Version History

**v1.0.0** (2026-01-20)
- Initial violation message definitions
- Core 10 universal invariants
- Domain-specific invariants (consumer, construction, capability)
- Severity levels defined

---

## Contributing

When adding new invariants:

1. Add detection pattern to `validator.sh`
2. Add violation message to this file
3. Include clear examples
4. Test against real specs
5. Document severity level

---

## See Also

- `validator.sh` - The enforcement script
- `system-invariants.md` - Complete invariant definitions
- `domains/` - Domain-specific invariant files
