# Consumer Product Domain Invariants

Extends: [[system-invariants]]
Domain: Mobile apps, web apps, consumer-facing products

---

## When to Use

Load this domain for:
- iOS/Android apps
- Web applications
- Consumer-facing products
- Karen's calorie tracker
- LineSheet Pro

---

## Domain Invariants (11-15)

### 11. User Emotion Must Map to Affordance

**Principle**: Emotional goals must become UI/UX elements

**Violation**: "Users feel X" without concrete implementation

**Examples**:
- ❌ "Users feel accomplished"
- ❌ "Users feel confident"
- ❌ "Users feel in control"
- ✅ "Accomplishment := green_checkmark + haptic_feedback + animation(0.3s) + sound(success.mp3)"
- ✅ "Confidence := preview_before_commit + undo_button(5min) + success_rate_display"
- ✅ "Control := visible_progress_indicator + cancel_button_always_available + state_shown"

**Enforcement**: Emotion must be followed by `:=` and concrete UI elements → Otherwise REJECT

---

### 12. Behavioral Friction Must Be Quantified

**Principle**: "Easy" must become measurable interaction cost

**Violation**: Ease/difficulty without numbers

**Examples**:
- ❌ "Make logging easy"
- ❌ "Simplify the workflow"
- ❌ "Quick entry"
- ✅ "Easy := max_3_taps + <10_sec_completion + voice_input_option"
- ✅ "Simple := single_screen + zero_config + auto_prefill_from_last_entry"
- ✅ "Quick := <5_sec_total + 1_tap_to_start + no_scrolling_required"

**Enforcement**: Friction words (easy, simple, quick, fast, intuitive) must specify: tap_count + time_limit + input_method → Otherwise REJECT

---

### 13. Accessibility Must Be Explicit

**Principle**: Every UI spec must declare accessibility compliance

**Violation**: Missing WCAG/platform accessibility guidelines

**Examples**:
- ❌ "Create login screen"
- ❌ "Show meal list"
- ❌ "Display dashboard"
- ✅ "Login screen: WCAG_AA + VoiceOver_labels + dynamic_type_support + 44pt_touch_targets"
- ✅ "Meal list: color_contrast≥4.5:1 + screen_reader_order + reduced_motion_fallback"
- ✅ "Dashboard: keyboard_navigable + focus_indicators + aria_labels_complete"

**Enforcement**: Every UI component must include accessibility declaration → Otherwise REJECT

---

### 14. Offline Behavior Must Be Defined

**Principle**: Network-dependent features must specify offline mode

**Violation**: Assuming always-online

**Examples**:
- ❌ "Sync meal data"
- ❌ "Save to cloud"
- ❌ "Fetch user profile"
- ✅ "Meal sync: local_first → queue_when_offline → sync_when_connected + conflict_resolution(last_write_wins)"
- ✅ "Cloud save: immediate_local_write → background_sync + retry_3x + show_sync_status"
- ✅ "Profile fetch: cache_locally + refresh_on_connect + stale_indicator_after(24h)"

**Enforcement**: Network operations must specify offline behavior → Otherwise REJECT

---

### 15. Loading States Must Be Bounded

**Principle**: Every loading state must have timeout

**Violation**: Infinite spinners, unbounded wait times

**Examples**:
- ❌ "Show loading spinner"
- ❌ "Wait for response"
- ❌ "Loading..."
- ✅ "Loading: spinner(max_5s) → timeout_error + retry_option + offline_fallback"
- ✅ "Response wait: 3s_spinner → 10s_timeout → cached_data_option"
- ✅ "Data fetch: skeleton_ui(immediate) → content(max_3s) → timeout_message + manual_refresh"

**Enforcement**: Loading states must specify: max_duration + timeout_behavior → Otherwise REJECT

---

## UI-Specific Sub-Invariants

### 15a. No Blocking Modals in Primary Flows

- Primary user journeys must not be interrupted by modals
- Confirmations must be inline or non-blocking
- Progress indicators required for operations >500ms

### 15b. Error Messages Must Be Actionable

- Error copy ≤15 words, neutral tone
- Must tell user what to do, not just what went wrong
- No technical jargon in user-facing errors

### 15c. Default State Must Be Recoverable

- Refresh/reload must not lose user work
- Auto-save or explicit save prompts required
- Recovery path documented for each state

### 15d. Touch Targets Must Be Accessible

- Minimum 44px touch targets on mobile (iOS HIG)
- Adequate spacing between interactive elements
- Keyboard navigation supported for all actions

---

## Quick Reference

| # | Invariant | Key Test |
|---|-----------|----------|
| 11 | User Emotion Must Map to Affordance | "Feel X" → ":= UI elements" |
| 12 | Behavioral Friction Must Be Quantified | "Easy" → taps + seconds |
| 13 | Accessibility Must Be Explicit | Every UI has a11y declaration |
| 14 | Offline Behavior Must Be Defined | Network ops have offline mode |
| 15 | Loading States Must Be Bounded | Spinners have timeouts |

---

*Domain: Consumer Product*
*Invariants: 11-15 (plus sub-invariants)*
*Use with: Core invariants 1-10*
