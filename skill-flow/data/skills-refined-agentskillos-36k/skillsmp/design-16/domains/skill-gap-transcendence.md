# Skill Gap Transcendence Domain Invariants

Extends: [[system-invariants]]
Domain: Projects requiring unknown technologies or skills

---

## When to Use

Load this domain for:
- Projects with new/unfamiliar technologies
- Learning-intensive work
- Fixed-deadline demos with skill gaps
- High-stress stretch assignments
- Any project where you're not yet competent

---

## Core Philosophy

**Traditional approach**: Skill gap → Can't do it → Reject or struggle
**This system**: Skill gap → Forces explicit design → Achievable with right structure

Skill gaps are **compilation constraints**, not blockers. They force clarity about:
- Learning budgets
- Scope tradeoffs
- Support structures
- Fallback protocols

---

## Domain Invariants (37-43)

### 37. Skill Gaps Force Explicit Learning Budget

**Principle**: Unknown technologies must have learning time as first-class schedule items

**Violation**: Assuming you can "figure it out" without budgeted time

**Examples**:
- ❌ "Build Kubernetes demo by Friday"
- ❌ "Learn as you go"
- ❌ "It shouldn't take long to pick up"
- ✅ "Kubernetes demo: learning_phase(3d) + building_phase(2d) + buffer(1d) | IF learning > 50%_timeline THEN require(extension OR scope_reduction OR tech_substitution)"
- ✅ "New framework: allocate_20%_for_learning + validation_prototype_first + proceed_only_after_validation"
- ✅ "Skill gap identified: document_learning_sources + define_fallback_resources + set_pivot_criteria"

**Enforcement**: Projects with skill gaps must specify: learning_time_budget + scope_tradeoff_if_exceeded + validation_criteria → Otherwise REJECT

---

### 38. Support Structure Must Be Pre-Defined

**Principle**: Every skill gap needs explicit blocker resolution protocol

**Violation**: No plan for getting unstuck

**Examples**:
- ❌ "Ask for help if stuck"
- ❌ "Figure it out"
- ❌ "Google it"
- ✅ "Blocker protocol: primary_resource(official_docs) + fallback_1(colleague_X) + fallback_2(external_consultant) + escalation_after(4hr_stuck)"
- ✅ "Learning support: mentor_identified + office_hours(2x/week) + pair_programming_available + pivot_criteria(can't_complete_validation_in_2d)"
- ✅ "Escalation timing: 2hr_self_study → 2hr_docs → ask_team → ask_manager → request_scope_change"

**Enforcement**: Each unknown technology must have: learning_sources + escalation_timing + pivot_criteria → Otherwise REJECT

---

### 39. Demos Require Triple-Backup Protocol

**Principle**: Public demos with skill gaps need layered fallbacks

**Violation**: Single path to demo success

**Examples**:
- ❌ "Demo the new feature live"
- ❌ "It'll work on the day"
- ❌ "We'll figure it out if something goes wrong"
- ✅ "Demo protocol: primary(live_demo) + fallback_1(pre_recorded_video) + fallback_2(slides_with_screenshots) + fallback_3(alternative_simpler_demo)"
- ✅ "Confidence gate: 1_week_before → full_rehearsal → go/no-go_decision → switch_to_fallback_if_needed"
- ✅ "Demo insurance: record_working_version_immediately + update_recording_daily + slides_always_current"

**Enforcement**: Public demos must specify: primary_approach + pre_recorded_fallback + slides_fallback + confidence_check_date → Otherwise REJECT

---

### 40. Health Signals Trigger Scope Adjustment

**Principle**: Physical/mental stress is a legitimate project constraint

**Violation**: Powering through at personal cost

**Examples**:
- ❌ "Just push through"
- ❌ "It's only temporary stress"
- ❌ "I'll rest after the deadline"
- ✅ "Health triggers: sleep_disruption(2+nights) OR physical_symptoms OR anxiety_interfering → trigger_scope_reduction_protocol"
- ✅ "Adjustment protocol: document_symptoms + identify_stress_sources + propose_targeted_scope_cut + escalate_if_denied"
- ✅ "Monitoring: daily_checkin(am_I_dreading_this?) + weekly_assessment + adjustment_authority_granted"

**Enforcement**: Stretch projects must specify: health_monitoring_protocol + scope_reduction_triggers + escalation_path → Otherwise REJECT

---

### 41. Fixed Deadlines Require Tiered Scope

**Principle**: Immovable dates mean movable scope, explicitly defined

**Violation**: Fixed date + fixed scope + skill gaps

**Examples**:
- ❌ "Deliver everything by conference date"
- ❌ "We committed to all features"
- ❌ "Cut scope at the last minute"
- ✅ "Fixed deadline scope: MVP(must_ship) + stretch(if_time_permits) + optional(first_to_drop) + 50%_checkpoint_for_assessment"
- ✅ "Tiered commitment: tier_1(demo_works) + tier_2(handles_edge_cases) + tier_3(polished_UI) → manager_approves_tiers_upfront"
- ✅ "Scope flexibility: optional_features_identified + drop_order_predetermined + 'cut_optional' != 'failed_to_deliver'"

**Enforcement**: Fixed-deadline projects must specify: scope_tiers(MVP/stretch/optional) + checkpoint_dates + drop_criteria → Otherwise REJECT

---

### 42. Learning Time Is First-Class Work

**Principle**: "I'm learning" is a legitimate status, not an excuse

**Violation**: Learning treated as overhead or procrastination

**Examples**:
- ❌ "Why aren't you building yet?"
- ❌ "Learning on your own time"
- ❌ "You should know this already"
- ✅ "Learning phase: scheduled_explicitly + validation_deliverable(throwaway_prototype) + proceed_only_after_pass"
- ✅ "Status legitimacy: 'in_learning_phase' = valid_status + expected_duration_communicated + manager_aware"
- ✅ "Validation gate: build_minimal_proof → if_pass(proceed_to_real_work) → if_fail(trigger_scope_reduction)"

**Enforcement**: Unknown technologies must have: explicit_learning_schedule + validation_criteria + automatic_scope_trigger_on_validation_failure → Otherwise REJECT

---

### 43. Discovery Phase Required for Unknowns

**Principle**: New territory gets 20% of timeline for exploration before commitment

**Violation**: Committing to estimates before understanding the problem

**Examples**:
- ❌ "Estimate the project now"
- ❌ "Commit to the timeline upfront"
- ❌ "We need certainty before starting"
- ✅ "Discovery phase: 20%_of_timeline + spike/prototype_deliverable + re-estimation_required_after + scope_adjustment_expected"
- ✅ "Discovery output: minimal_prototype + unknowns_discovered_list + re-estimated_timeline + adjusted_scope_proposal"
- ✅ "Commitment model: soft_commit(before_discovery) → hard_commit(after_discovery) → scope_flexibility_preserved"

**Enforcement**: New tech/domain projects must specify: discovery_phase_allocation + prototype_requirement + re-estimation_gate → Otherwise REJECT

---

## Skill Gap Sub-Invariants

### 43a. Imposter Syndrome Mitigation

- Skill gaps are normal, not shameful
- Documentation of gaps is strength, not weakness
- Asking for help is expected, not failure
- "I don't know yet" is valid answer

### 43b. Manager Communication Protocol

- Skill gaps communicated proactively
- Tradeoffs presented as choices, not problems
- Scope cuts framed as decisions, not failures
- Learning time defended as necessary work

### 43c. Validation Before Commitment

- Never commit to timeline without validation prototype
- "I need to spike this first" is legitimate
- Re-estimation after discovery is planned, not reactive
- Early failures are cheaper than late failures

### 43d. Psychological Safety Preservation

- Projects shouldn't require heroics
- Sustainable pace over crunch
- Health signals taken seriously
- Failure modes planned for, not punished

---

## Quick Reference

| # | Invariant | Key Test |
|---|-----------|----------|
| 37 | Skill Gaps Force Explicit Learning Budget | Learning time budgeted, not assumed |
| 38 | Support Structure Must Be Pre-Defined | Blocker resolution protocol exists |
| 39 | Demos Require Triple-Backup | Three fallback paths defined |
| 40 | Health Signals Trigger Scope Adjustment | Stress → automatic scope reduction |
| 41 | Fixed Deadlines Require Tiered Scope | MVP/stretch/optional defined upfront |
| 42 | Learning Time Is First-Class Work | Learning scheduled, not overhead |
| 43 | Discovery Phase Required for Unknowns | 20% for exploration + re-estimation |

---

## The Power This Gives You

1. **Learning is billable work** — not something you hide
2. **Scope cuts are documented requirements** — not failures
3. **"I'm stuck" has a protocol** — not panic
4. **Health is a constraint** — not weakness
5. **Demos have safety nets** — not prayers
6. **Estimates can change** — after discovery
7. **Manager approved the structure** — you're protected

---

*Domain: Skill Gap Transcendence*
*Invariants: 37-43 (plus sub-invariants)*
*Use with: Core invariants 1-10*
*Often combined with: consumer-product.md, integration.md*
*Philosophy: Skill gaps are compilation constraints, not blockers*
