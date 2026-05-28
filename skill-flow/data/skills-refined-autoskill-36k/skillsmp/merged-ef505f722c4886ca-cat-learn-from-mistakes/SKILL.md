---
name: cat:learn-from-mistakes
description: Analyze mistakes with conversation length as potential cause (CAT-specific)
---

# Learn From Mistakes (CAT-Specific)

## Purpose

Analyze mistakes using 5-whys with CAT-specific consideration of conversation length and context degradation. Integrates token tracking to identify context-related failures and recommend preventive measures including earlier decomposition.

## When to Use

- Any mistake during CAT orchestration
- Subagent produces incorrect/incomplete results
- Task requires rework or correction
- Build/test/logical errors
- Repeated attempts at the same operation
- Quality degradation over time

## Workflow

### 1. Verify Event Sequence (MANDATORY)

**CRITICAL: Do NOT rely on memory for root cause analysis.**

Verify actual event sequence using get-history:

```bash
/cat:get-history
# Look for: When stated? Action order? User corrections? Actual trigger?
```

**Anti-Pattern (M037):** Root cause analysis based on memory without get-history verification. Memory is unreliable for causation, timing, attribution.

**If get-history unavailable:** Document analysis based on current context only, may be incomplete.

### 2. Document the Mistake

```yaml
mistake:
  timestamp: 2026-01-10T16:30:00Z
  type: incorrect_implementation
  description: |
    Subagent implemented parser with wrong precedence rules.
    Expressions like "a + b * c" parsed as "(a + b) * c" instead of "a + (b * c)".
  impact: |
    All tests using operator precedence failing. Required complete rewrite.
```

### 3. Gather Context Metrics

**CAT-specific: Always collect token data**

```bash
SESSION_ID="${SUBAGENT_SESSION}"
SESSION_FILE="/home/node/.config/claude/projects/-workspace/${SESSION_ID}.jsonl"

TOKENS_AT_ERROR=$(jq -s 'map(select(.type == "assistant")) |
  map(.message.usage | .input_tokens + .output_tokens) | add' "${SESSION_FILE}")
COMPACTIONS=$(jq -s '[.[] | select(.type == "summary")] | length' "${SESSION_FILE}")
MESSAGE_COUNT=$(jq -s '[.[] | select(.type == "assistant")] | length' "${SESSION_FILE}")
SESSION_DURATION=$(calculate_duration "${SESSION_FILE}")
```

### 4. Perform Root Cause Analysis

**A/B TEST IN PROGRESS** - See [RCA-AB-TEST.md](RCA-AB-TEST.md) for full specification.

**Method Assignment Rule:** Use mistake ID modulo 3:
- IDs ending in 6,9,2,5,8 (mod 3 = 0) → Method A (5-Whys)
- IDs ending in 7,0,3 (mod 3 = 1) → Method B (Taxonomy)
- IDs ending in 8,1,4 (mod 3 = 2) → Method C (Causal Barrier)

---

#### Method A: 5-Whys (Control)

Ask "why" iteratively until reaching fundamental cause (typically 5 levels):

```yaml
five_whys:
  - why: "Why did this happen?"
    answer: "Immediate cause of the mistake"
  - why: "Why [previous answer]?"
    answer: "Deeper contributing factor"
  - why: "Why [previous answer]?"
    answer: "Organizational or process factor"
  - why: "Why [previous answer]?"
    answer: "Systemic or environmental factor"
  - why: "Why [previous answer]?"
    answer: "Root cause - fundamental issue"

root_cause: "The fundamental issue identified at deepest 'why'"
category: "Select from category reference"
rca_method: "A"
```

**Example:**

```yaml
five_whys:
  - why: "Why was precedence implemented incorrectly?"
    answer: "Subagent confused multiplication and addition handling"
  - why: "Why was the subagent confused?"
    answer: "Earlier context about precedence rules was not referenced"
  - why: "Why wasn't earlier context referenced?"
    answer: "Session had 95K tokens, approaching context limit"
  - why: "Why were there 95K tokens in the session?"
    answer: "Task scope was too large for single context window"
  - why: "Why wasn't the task decomposed earlier?"
    answer: "Token monitoring wasn't triggering at 40% threshold"

root_cause: "Task exceeded safe context bounds without decomposition"
category: "context_degradation"
rca_method: "A"
```

**Check against common root cause patterns:**
- Assumption without verification?
- Completion bias (rationalized ignoring rules)?
- Memory reliance (didn't re-verify)?
- Environment state mismatch?
- Documentation ignored (rule existed)?

---

#### Method B: Modular Error Taxonomy

Based on [AgentErrorTaxonomy](https://arxiv.org/abs/2509.25370) (24% accuracy improvement).

```yaml
taxonomy_analysis:
  # Step 1: Classify into module
  module: MEMORY | PLANNING | ACTION | REFLECTION | SYSTEM
  module_definitions:
    MEMORY: "Failed to retain/recall earlier context"
    PLANNING: "Poor task decomposition or sequencing"
    ACTION: "Incorrect tool use or execution"
    REFLECTION: "Failed to detect/correct own error"
    SYSTEM: "Environment, tooling, or integration failure"

  # Step 2: Identify failure mode within module
  failure_mode: "What specific capability failed?"
  failure_type: FALSE_POSITIVE | FALSE_NEGATIVE
    # FALSE_POSITIVE = did something wrong
    # FALSE_NEGATIVE = missed something

  # Step 3: Check for cascading
  cascading:
    caused_downstream: true | false
    is_symptom_of: null | "earlier failure description"

  # Step 4: Corrective feedback
  corrective_feedback: "What specific guidance would have prevented this?"
  intervention_point: "At what step should intervention have occurred?"

root_cause: "..."
category: "..."
rca_method: "B"
```

---

#### Method C: Causal Barrier Analysis

Based on [causal reasoning research](https://www.infoq.com/articles/causal-reasoning-observability/).

```yaml
causal_barrier_analysis:
  # Step 1: List ALL candidate causes
  candidates:
    - cause: "Knowledge gap - didn't know correct approach"
      expected_symptoms: ["asked questions", "explored alternatives"]
      observed: false
      likelihood: LOW

    - cause: "Compliance failure - knew rule, didn't follow"
      expected_symptoms: ["rule exists in docs", "no confusion expressed"]
      observed: true
      likelihood: HIGH

    - cause: "Tool limitation - tool couldn't do what was needed"
      expected_symptoms: ["error messages", "tried alternatives"]
      observed: false
      likelihood: LOW

  # Step 2: Select most likely cause
  selected_cause: "Compliance failure"
  confidence: HIGH | MEDIUM | LOW
  evidence: "Rule documented in X, no exploration attempts observed"

  # Step 3: Verify cause vs symptom
  verification:
    question: "If we fixed this, would the problem definitely not recur?"
    answer: "Yes, if enforcement hook blocks the incorrect behavior"
    is_root_cause: true  # If uncertain, this may be a symptom

  # Step 4: Barrier analysis
  barriers:
    - barrier: "Documentation in CLAUDE.md"
      existed: true
      why_failed: "Agent did not read/follow it"

    - barrier: "PreToolUse hook"
      existed: false
      should_exist: true
      strength_if_added: "Would block incorrect behavior"

  minimum_effective_barrier: "hook (level 2)"

root_cause: "..."
category: "..."
rca_method: "C"
```

---

**Record the method used** in the final JSON entry:

```json
{
  "rca_method": "A|B|C",
  "rca_method_name": "5-whys|taxonomy|causal-barrier"
}
```

### 5. Check for Context Degradation Patterns

**CAT-specific analysis checklist:**

Reference: agent-architecture.md § Context Limit Constants

```yaml
context_degradation_analysis:
  tokens_at_error: 95000
  threshold_exceeded: true
  threshold_exceeded_by: 15000
  compaction_events: 2
  errors_after_compaction: true
  session_duration: 4.5 hours
  messages_before_error: 127
  early_session_quality: high
  late_session_quality: degraded
  quality_degradation_detected: true
  context_related: LIKELY
  confidence: 0.85
```

### 6. Identify Prevention Level

**Choose the strongest prevention level that addresses the root cause:**

```yaml
prevention_hierarchy:
  - level: 1
    type: code_fix
    description: "Make incorrect behavior impossible in code"
    examples: ["compile-time check", "type system enforcement", "API design"]
  - level: 2
    type: hook
    description: "Automated enforcement via PreToolUse/PostToolUse hooks"
    examples: ["block dangerous commands", "require confirmation", "validate state"]
  - level: 3
    type: validation
    description: "Automated checks that catch mistakes early"
    examples: ["build verification", "lint rules", "test assertions"]
  - level: 4
    type: config
    description: "Configuration or threshold changes"
    examples: ["lower context threshold", "adjust timeouts", "change defaults"]
    cat_specific: true
  - level: 5
    type: skill
    description: "Update skill documentation with explicit guidance"
    examples: ["add anti-pattern section", "add checklist item", "clarify steps"]
  - level: 6
    type: process
    description: "Change workflow steps or ordering"
    examples: ["add mandatory checkpoint", "reorder operations", "add verification"]
  - level: 7
    type: documentation
    description: "Document to prevent future occurrence"
    examples: ["add to CLAUDE.md", "update style guide", "add comments"]
    note: "Weakest prevention - escalate if documentation already exists"
```

**Key principle:** Lower level = stronger prevention. Always prefer level 1-3 over level 5-7.

### 7. Evaluate Prevention Quality

**BEFORE implementing, verify the prevention is robust:**

```yaml
prevention_quality_check:
  verification_type:
    positive: "Check for PRESENCE of correct behavior"  # ✅ Preferred
    negative: "Check for ABSENCE of specific failure"   # ❌ Fragile

  # Ask: Am I checking for what I WANT, or what I DON'T want?
  # Example:
  #   ❌ grep "Initial implementation -"  (catches ONE placeholder pattern)
  #   ✅ grep "^- \`[a-f0-9]{7,}\`"        (checks for correct commit format)

  generality:
    question: "If the failure mode varies slightly, will this still catch it?"
    examples:
      - "What if placeholder text changes from 'Initial' to 'First'?"
      - "What if someone uses 'TBD' or 'TODO' instead?"
      - "What if the format is subtly wrong in a different way?"
    # If answer is NO → prevention is too specific → redesign

  inversion:
    question: "Can I invert this check to verify correctness instead?"
    pattern: |
      Instead of: "Fail if BAD_PATTERN exists"
      Try:        "Fail if GOOD_PATTERN is missing"
    # Positive verification catches ALL failures, not just anticipated ones

  fragility_assessment:
    low:    "Checks for correct format/behavior (positive verification)"
    medium: "Checks for category of errors (e.g., any TODO-like text)"
    high:   "Checks for exact observed failure (specific string match)"
```

**Decision gate:** If fragility is HIGH, redesign the prevention before implementing.

### 8. Check If Prevention Already Exists (MANDATORY)

**CRITICAL: If prevention already exists, it FAILED and MUST be replaced with stronger prevention.**

Before implementing prevention, check if it already exists:

```yaml
existing_prevention_check:
  question: "Does documentation/process already cover this?"
  check_locations:
    - Workflow files (work.md, etc.)
    - CLAUDE.md / project instructions
    - Skill documentation
    - Existing hooks

  if_exists:
    conclusion: "Existing prevention FAILED - it was ineffective"
    action: "MUST escalate to higher prevention level"
    rationale: |
      If prevention exists and the mistake still occurred, that prevention
      is NOT WORKING. Pointing to it again changes nothing. The mistake
      WILL recur unless you implement STRONGER prevention.
```

**Key insight:** Existing prevention that didn't prevent the mistake is NOT prevention - it's failed prevention. You must escalate to a level that will actually work.

**Escalation hierarchy (when current level failed):**

| Failed Level | Escalate To | Example |
|--------------|-------------|---------|
| Documentation | Hook/Validation | Add pre-commit hook that blocks incorrect behavior |
| Process | Code fix | Make incorrect path impossible in code |
| Threshold | Lower threshold + hook | Add monitoring that forces action |
| Validation | Code fix | Compile-time or runtime enforcement |

**Example - Documentation failed:**

```yaml
# Situation: Workflow says "MANDATORY: Execute different task when locked"
# Agent ignored it and tried to delete the lock

# ❌ WRONG: Record prevention as "documentation" pointing to same workflow
prevention_type: documentation
prevention_path: "work.md"  # Already says MANDATORY - and it FAILED!

# ✅ CORRECT: Escalate to hook that enforces the behavior
prevention_type: hook
prevention_path: "${CLAUDE_PROJECT_DIR}/.claude/hooks/enforce-lock-protocol.sh"
action: |
  Create hook that detects lock investigation patterns and blocks them.
  Or: Modify task-lock.sh to output ONLY "find another task" guidance,
  removing any information that could be used to bypass the lock.
```

**The prevention step MUST take NEW action.** Recording a mistake without implementing NEW prevention (beyond what already existed) is not learning - it's just logging. The same mistake WILL recur.

**BLOCKING CRITERIA (A002) - Documentation-level prevention NOT ALLOWED when:**

| Condition | Why Blocked | Required Action |
|-----------|-------------|-----------------|
| Similar documentation already exists | Documentation already failed | Escalate to hook or code_fix |
| Mistake category is `protocol_violation` | Protocol was documented but violated | Escalate to hook enforcement |
| This is a recurrence (`recurrence_of` is set) | Previous prevention failed | Escalate to stronger level |
| prevention_type would be `documentation` (level 7) | Weakest level, often ineffective | Consider hook (level 2) or validation (level 3) |

**Self-check before recording prevention_type: documentation:**

```yaml
documentation_prevention_blocked_if:
  - Similar instruction already exists in workflow/skill docs
  - The mistake was ignoring existing documentation
  - Category is protocol_violation (protocols ARE documentation)
  - This is a recurrence of a previous mistake

# If ANY of the above is true:
action: "STOP. Escalate to hook, validation, or code_fix instead."
```

**Verification questions:**
1. "Did prevention for this already exist?" → If YES, it failed and must be escalated
2. "What NEW mechanism will prevent this tomorrow?" → Must be different from what failed today
3. "Is this prevention stronger than what failed?" → Must be higher in the hierarchy
4. "Am I choosing documentation because it's easy?" → If YES, find a stronger approach (A002)

**If you cannot identify NEW prevention stronger than what already exists, you have NOT learned.**

### 9. Implement Prevention

**MANDATORY: Take concrete action. Prevention without action changes nothing.**

The prevention step must result in a modified file - code, hook, configuration, or documentation. If you finish this step without editing a file, you have not implemented prevention.

**Language requirements for documentation/prompt changes:**

When prevention involves updating documentation, prompts,