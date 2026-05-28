---
name: task-refinement
description: Use when refining Tasks into actionable plans - SRE-style review ensuring corner cases handled, junior engineer can execute without questions
---

# Task Refinement

## Overview

Review Task plans with Google Fellow SRE perspective to ensure junior engineer can execute without questions. Catch edge cases, verify granularity, strengthen criteria, prevent production issues before implementation.

**Core principle:** If a junior engineer would need to ask a question, the Task is incomplete.

**Announce at start:** "I'm using gambit:task-refinement to review this plan with Google Fellow-level scrutiny."

## Rigidity Level

LOW FREEDOM - Follow the 8-category checklist exactly. Apply all categories to every Task. No skipping red flag checks. Always verify no placeholder text after updates. Reject plans with critical gaps.

## Quick Reference

| Category | Key Questions | Auto-Reject If |
|----------|---------------|----------------|
| 1. Granularity | Tasks 4-8 hours? | Any task > 16h without breakdown |
| 2. Implementability | Junior can execute without questions? | Vague language, missing details |
| 3. Success Criteria | 3+ measurable criteria per task? | Can't verify ("works well") |
| 4. Dependencies | Correct blocking relationships? | Circular dependencies |
| 5. Safety Standards | Anti-patterns specified? | No anti-patterns section |
| 6. Edge Cases | Empty? Unicode? Concurrency? Failures? | No edge case consideration |
| 7. Red Flags | Placeholder text? Vague instructions? | "[detailed above]", "TODO" |
| 8. Test Meaningfulness | Tests catch real bugs? | Only verify syntax/existence |

**Perspective:** Google Fellow SRE with 20+ years experience reviewing junior engineer designs.

**Time:** Don't rush - catching one gap pre-implementation saves hours of rework.

## When to Use

- Reviewing epic/feature plans before implementation
- Need to ensure junior engineer can execute without questions
- Want to catch edge cases and failure modes upfront
- After `gambit:brainstorm` creates initial design
- Before `gambit:execute-plan` starts implementation

**Don't use for:**
- Task already being implemented (too late)
- Just need to understand existing code (use Explore agent)
- Debugging issues (use `gambit:debugging`)
- Creating plan from scratch (use `gambit:brainstorm`)

## The 8-Category Checklist

### 1. Task Granularity

**Check:**
- [ ] No task > 8 hours (subtasks)?
- [ ] Large tasks broken into 4-8 hour subtasks?
- [ ] Each subtask independently completable?
- [ ] Each subtask has clear deliverable?

**If task > 16 hours:**

```
TaskCreate
  subject: "Subtask 1: [Specific Component]"
  description: "[Complete subtask design]"
  activeForm: "[Active form]"
```

Then link via `addBlockedBy`:

```
TaskUpdate
  taskId: "[subtask-id]"
  addBlockedBy: ["[earlier-subtask-id]"]
```

---

### 2. Implementability (Junior Engineer Test)

**Check:**
- [ ] Can junior engineer implement without asking questions?
- [ ] Function signatures/behaviors described, not just "implement X"?
- [ ] Test scenarios described (what they verify, not just names)?
- [ ] "Done" clearly defined with verifiable criteria?
- [ ] All file paths specified or marked "TBD: new file"?

**Red flags:**
- "Implement properly" (how?)
- "Add support" (for what exactly?)
- "Make it work" (what does working mean?)
- File paths missing or ambiguous

---

### 3. Success Criteria Quality

**Check:**
- [ ] Each task has 3+ specific, measurable success criteria?
- [ ] All criteria testable/verifiable (not subjective)?
- [ ] Includes automated verification (tests pass, lint clean)?
- [ ] No vague criteria like "works well" or "is implemented"?

**Good criteria examples:**
- ✅ "5+ unit tests pass (valid input, invalid input, edge cases)"
- ✅ "Lint clean with no warnings"
- ✅ "Performance: < 100ms for 1000 records"
- ✅ "Error returns proper message, not panic"

**Bad criteria examples:**
- ❌ "Code is good quality"
- ❌ "Works correctly"
- ❌ "Is implemented"

---

### 4. Dependency Structure

**Check:**
- [ ] Blocking dependencies correct (earlier work blocks later)?
- [ ] No circular dependencies?
- [ ] Dependency graph makes logical sense?

**Verify with TaskList:**

```
TaskList
```

Check that `blockedBy` relationships are correct.

---

### 5. Safety & Quality Standards

**Check:**
- [ ] Anti-patterns include common pitfalls?
- [ ] Anti-patterns include TODO prohibition (or must have issue #)?
- [ ] Anti-patterns include stub implementation prohibition?
- [ ] Error handling requirements specified?
- [ ] Test requirements specific?

**Minimum anti-patterns:**
- ❌ No panic/unwrap/expect in production code
- ❌ No TODOs without task references
- ❌ No stub implementations (unimplemented!, todo!)
- ❌ No swallowed errors (must handle or propagate)

---

### 6. Edge Cases & Failure Modes (Fellow SRE Perspective)

**Ask for each task:**
- [ ] What happens with malformed input?
- [ ] What happens with empty/nil/zero values?
- [ ] What happens under high load/concurrency?
- [ ] What happens when dependencies fail?
- [ ] What happens with Unicode, special characters, large inputs?
- [ ] Are these edge cases addressed in the plan?

**Add to Key Considerations section:**

```markdown
## Key Considerations

**Edge Case: Empty Input**
- What happens when input is empty string?
- MUST validate input length before processing

**Edge Case: Unicode Handling**
- What if string contains RTL or surrogate pairs?
- Use proper Unicode-aware string methods

**Performance Concern: Large Inputs**
- What if input is 10MB?
- Add size limits, streaming if needed
```

---

### 7. Red Flags (AUTO-REJECT)

**Check for these - if found, REJECT plan:**

- ❌ Any task > 16 hours without subtask breakdown
- ❌ Vague language: "implement properly", "add support", "make it work"
- ❌ Success criteria that can't be verified: "code is good", "works well"
- ❌ Missing test specifications
- ❌ "We'll handle this later" or "TODO" in the plan itself
- ❌ No anti-patterns section
- ❌ Implementation checklist with fewer than 3 items per task
- ❌ Missing error handling considerations
- ❌ **CRITICAL: Placeholder text** - "[detailed above]", "[as specified]", "[complete steps here]"

---

### 8. Test Meaningfulness (Fellow SRE Perspective)

**Tests must catch real bugs, not inflate coverage.**

**Ask for each test specification:**
- [ ] What specific bug would this test catch?
- [ ] Could production code break while this test passes?
- [ ] Does this test exercise a real user scenario?
- [ ] Is the assertion meaningful? (`result == expected` vs `result != nil`)

**Red flags (AUTO-REJECT):**
- ❌ Tests that only verify syntax/existence ("struct has fields")
- ❌ Tautological tests (pass by definition: `expect(builder.build() != nil)`)
- ❌ Tests that duplicate implementation (testing 1+1==2)
- ❌ Tests without meaningful assertions
- ❌ Tests that verify mocks instead of production code
- ❌ Generic test names ("test_basic", "test_it_works")

**Good test specifications:**
- ✅ "test_empty_payload_returns_validation_error" - catches missing validation
- ✅ "test_concurrent_writes_dont_corrupt_data" - catches race condition
- ✅ "test_malformed_json_returns_400_not_500" - catches error handling bug
- ✅ "test_unicode_name_preserved_after_roundtrip" - catches encoding bugs

**Bad test specifications:**
- ❌ "test_user_model_exists" - tautological, compiler catches this
- ❌ "test_basic_functionality" - vague, what bug does it catch?
- ❌ "test_encode_decode" - only happy path, no edge cases

---

## Review Process

### For Each Task:

**Step 1: Read the Task**

```
TaskGet
  taskId: "[task-id]"
```

**Step 2: Apply all 8 checklist categories**

Go through each category systematically.

**Step 3: Document findings**

Take notes:
- What's done well
- What's missing
- What's vague or ambiguous
- Hidden failure modes not addressed
- Better approaches

**Step 4: Update the Task**

```
TaskUpdate
  taskId: "[task-id]"
  description: |
    ## Goal
    [Original goal, preserved]

    ## Success Criteria
    - [ ] Existing criteria
    - [ ] NEW: Added missing measurable criteria

    ## Implementation Checklist
    [Complete checklist with file paths]

    ## Key Considerations (ADDED BY SRE REVIEW)

    **Edge Case: Empty Input**
    - What happens when input is empty string?
    - MUST validate input length before processing

    **Edge Case: Unicode Handling**
    - Use proper Unicode-aware string methods

    **Performance Concern**
    - Add size limits for large inputs

    ## Anti-patterns
    [Original anti-patterns]
    - ❌ NEW: Specific anti-pattern for this task's risks
```

**Step 5: Verify no placeholder text (MANDATORY)**

After updating, read back with `TaskGet` and verify:
- ✅ All sections contain actual content
- ✅ No placeholder text like "[detailed above]", "[as specified]"
- ✅ Implementation steps fully written
- ❌ If ANY placeholder text found: rewrite with actual content

---

## Breaking Down Large Tasks

If task > 16 hours, create subtasks:

```
# Parent task becomes coordinator
TaskUpdate
  taskId: "[parent-id]"
  description: |
    ## Goal
    Coordinate implementation of [feature]. Broken into N subtasks.

    ## Success Criteria
    - [ ] All N child subtasks completed
    - [ ] Integration tests pass
    - [ ] [High-level criteria]

# Create subtasks
TaskCreate
  subject: "Subtask 1: [Specific Component]"
  description: "[Complete subtask design - 4-8 hours of work]"

TaskCreate
  subject: "Subtask 2: [Another Component]"
  description: "[Complete subtask design]"

# Link dependencies
TaskUpdate
  taskId: "[subtask-2-id]"
  addBlockedBy: ["[subtask-1-id]"]
```

---

## Output Format

After reviewing all tasks:

```markdown
## Plan Review Results

### Overall Assessment
[APPROVE ✅ / NEEDS REVISION ⚠️ / REJECT ❌]

### Task-by-Task Review

#### [Task Name] ([task-id])
**Status**: [✅ Ready / ⚠️ Needs Improvements / ❌ Needs Revision]

**Strengths**:
- [What's done well]

**Critical Issues** (must fix):
- [Blocking problems]

**Improvements Made**:
- [Specific improvements added]

**Edge Cases Added**:
- [Failure modes now addressed]

---

[Repeat for each task]

### Summary of Changes

**Tasks Updated**:
- [task-id] - Added edge case handling
- [task-id] - Broke into 3 subtasks
- [task-id] - Strengthened success criteria

### Recommendations

[If APPROVE]:
✅ Plan is solid and ready for implementation.

[If NEEDS REVISION]:
⚠️ Plan needs improvements:
- [List major items]

[If REJECT]:
❌ Plan has fundamental issues:
- [Critical problems]
```

---

## Critical Rules

### Rules That Have No Exceptions

1. **Apply all 8 categories to every task** → No skipping any category
2. **Reject plans with placeholder text** → "[detailed above]" = instant reject
3. **Verify no placeholder after updates** → Read back with TaskGet
4. **Break tasks > 16 hours** → Create subtasks
5. **Strengthen vague criteria** → "Works correctly" → measurable commands
6. **Add edge cases to every task** → Empty? Unicode? Concurrency?
7. **Never skip Category 6** → Edge case analysis prevents production issues
8. **Reject tautological tests** → Tests must catch bugs

### Common Excuses

All of these mean: **STOP. Apply the full process.**

| Excuse | Reality |
|--------|---------|
| "Task looks straightforward" | Edge cases hide in "straightforward" tasks |
| "Has 3 criteria, meets minimum" | Criteria must be measurable, not just 3+ items |
| "Placeholder text is just formatting" | Placeholders = incomplete specification |
| "Can handle edge cases during implementation" | Must specify upfront |
| "Junior will figure it out" | Junior should NOT need to figure out |
| "Too detailed, feels like micromanaging" | Detail prevents questions and rework |
| "Taking too long to review" | One gap caught saves hours of rework |
| "Tests are specified, don't need review" | Test quality matters more than quantity |

---

## Examples

### Bad: Skip Edge Case Analysis

```
Task: "Implement VIN scanner"

Review:
1. Granularity: ✅ 6-8 hours
2. Implementability: ✅
3. Success Criteria: ✅
4. Dependencies: ✅
5. Safety Standards: ✅
6. Edge Cases: [SKIPPED - "looks straightforward"]
7. Red Flags: ✅
8. Tests: ✅

Conclusion: "Task looks good, approve ✅"

# Production issues:
# - VIN scanner matches random 17-char strings (no checksum validation)
# - Lowercase VINs not handled
# - Catastrophic regex backtracking (DoS vulnerability)
```

**Why it fails:**
- Skipped edge case analysis
- Missed checksum validation
- Missed case handling
- Missed performance concerns

### Good: Full Edge Case Analysis

```
Task: "Implement VIN scanner"

Category 6 (Edge Cases):
- Malformed input? VIN has checksum - must validate
- Empty/nil? What if empty string passed?
- Unicode/special? VIN is alphanumeric only, but lowercase?
- Large inputs? Regex patterns can cause backtracking

Findings:
❌ VIN checksum validation not mentioned
❌ Case normalization not mentioned
❌ Regex backtracking risk not mentioned

Update Task with Key Considerations:

## Key Considerations (ADDED BY SRE REVIEW)

**VIN Checksum**
- ISO 3779 requires transliteration and weighted sum
- MUST validate checksum, not just pattern

**Case Normalization**
- VINs can appear lowercase
- MUST normalize to uppercase before validation

**Regex Backtracking Risk**
- Test with pathological inputs (10000 'X's)
- Use bounded repetition
```

### Bad: Accept Vague Success Criteria

```
Task: "Implement data encryption"

## Success Criteria
- [ ] Encryption is implemented correctly
- [ ] Code is good quality
- [ ] Tests work properly

Review: "Has 3 success criteria ✅"

# Junior engineer:
# "How do I know if encryption is 'correct'?"
# "What makes code 'good quality'?"
# Uses ECB mode (insecure)
# Complete rewrite required
```

### Good: Measurable Success Criteria

```
## Success Criteria

**Encryption Implementation**:
- [ ] Uses AES-256-GCM mode (verified in code review)
- [ ] Unique IV generated per encryption (crypto_random)
- [ ] Authentication tag verified on decryption

**Code Quality** (automated):
- [ ] Lint clean with no warnings
- [ ] No panic/unwrap in production code
- [ ] No TODOs without task references

**Tests**:
- [ ] test_encrypt_decrypt_roundtrip (happy path)
- [ ] test_wrong_key_fails_auth (security)
- [ ] test_empty_plaintext (edge case)
- [ ] test_large_plaintext_10mb (performance)
- [ ] test_unicode_plaintext (data handling)
```

---

## Verification Checklist

Before completing SRE review:

**Per task reviewed:**
- [ ] Applied all 8 categories
- [ ] Checked for placeholder text
- [ ] Updated task with missing information
- [ ] Verified updated task (no placeholders remain)
- [ ] Broke down any task > 16 hours
- [ ] Strengthened vague success criteria
- [ ] Added edge case analysis
- [ ] Verified test specifications meaningful

**Overall plan:**
- [ ] Reviewed ALL tasks (no exceptions)
- [ ] Documented findings for each
- [ ] Created summary of changes
- [ ] Provided clear recommendation

**Can't check all boxes?** Return to review process.

---

## Integration

**This skill is used after:**
- `gambit:brainstorm` (creates initial design)
- `gambit:write-plan` (creates Tasks)

**This skill is used before:**
- `gambit:execute-plan` (implements Tasks)

**Workflow:**
```
gambit:brainstorm → gambit:write-plan → gambit:task-refinement → gambit:execute-plan
                                               ↓
                                        (if gaps: revise)
```

**Time expectations:**
- Small epic (3-5 tasks): 15-20 minutes
- Medium epic (6-10 tasks): 25-40 minutes
- Large epic (10+ tasks): 45-60 minutes

**Don't rush:** Catching one critical gap pre-implementation saves hours of rework.

---

## Resources

**Review patterns:**
- Task too large (> 16h) → Break into 4-8h subtasks
- Vague criteria ("works correctly") → Measurable commands/checks
- Missing edge cases → Add to Key Considerations
- Placeholder text → Rewrite with actual content
- Tautological tests → Strengthen to catch specific bugs

**When stuck:**
- Unsure if task too large → Ask: Can junior complete in one day?
- Unsure if criteria measurable → Ask: Can I verify with command/code review?
- Unsure if edge case matters → Ask: Could this fail in production?
- Unsure if placeholder → Ask: Does this reference other content instead of providing it?
- Unsure if test meaningful → Ask: What specific bug does this prevent?

**Key principle:** Junior engineer should be able to execute task without asking questions. If they would need to ask, specification is incomplete.
