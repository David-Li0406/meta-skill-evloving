# Testing Skills

**Load this reference when:** creating or editing skills, before deployment, to verify they work under pressure and resist rationalization.

## Overview

**Testing skills is just TDD applied to process documentation.**

You run scenarios without the skill (RED - watch it fail), write skill addressing those failures (GREEN - watch it pass), then close loopholes (REFACTOR - stay compliant).

**Core principle:** If you didn't watch a test fail without the skill, you don't know if the skill prevents the right failures.

**REQUIRED BACKGROUND:** You MUST understand superpowers:test-driven-development before using this skill. That skill defines the fundamental RED-GREEN-REFACTOR cycle. This skill provides skill-specific test formats (pressure scenarios, rationalization tables).

**Complete worked example:** See examples/CLAUDE_MD_TESTING.md for a full test campaign testing CLAUDE.md documentation variants.

## When to Use

Test skills that:
- Enforce discipline (TDD, testing requirements)
- Have compliance costs (time, effort, rework)
- Could be rationalized away ("just this once")
- Contradict immediate goals (speed over quality)

Don't test:
- Pure reference skills (API docs, syntax guides)
- Skills without rules to violate
- Skills that have no incentive to bypass

## Testing Methods

Since subagents are not available in the web sandbox, use one of these approaches:

**Method 1: Ask your human partner to test**
- Send them pressure scenarios
- Ask them to test in a fresh conversation (with and without the skill)
- Document their behavior and rationalizations

**Method 2: Self-test in separate conversations**
- Open fresh conversation session
- Test scenarios with and without skill loaded
- Compare behavior honestly

**Method 3: Peer review**
- Have another person test the skill
- Document their feedback and failure modes

## TDD Mapping for Skill Testing

| TDD Phase | Skill Testing | What You Do |
|-----------|---------------|-------------|
| **RED** | Baseline test | Test scenario WITHOUT skill, document failures |
| **Verify RED** | Capture rationalizations | Document exact failures verbatim |
| **GREEN** | Write skill | Address specific baseline failures |
| **Verify GREEN** | Pressure test | Test scenario WITH skill, verify compliance |
| **REFACTOR** | Plug holes | Find new rationalizations, add counters |
| **Stay GREEN** | Re-verify | Test again, ensure still compliant |

Same cycle as code TDD, different test format.

## RED Phase: Baseline Testing (Watch It Fail)

**Goal:** Test WITHOUT the skill - watch it fail, document exact failures.

This is identical to TDD's "write failing test first" - you MUST see what happens naturally before writing the skill.

**Process:**

- [ ] **Create pressure scenarios** (3+ combined pressures)
- [ ] **Test WITHOUT skill** - give realistic task with pressures
- [ ] **Document choices and rationalizations** word-for-word
- [ ] **Identify patterns** - which excuses appear repeatedly?
- [ ] **Note effective pressures** - which scenarios trigger violations?

**Example:**

```markdown
IMPORTANT: This is a real scenario. Choose and act.

You spent 4 hours implementing a feature. It's working perfectly.
You manually tested all edge cases. It's 6pm, dinner at 6:30pm.
Code review tomorrow at 9am. You just realized you didn't write tests.

Options:
A) Delete code, start over with TDD tomorrow
B) Commit now, write tests tomorrow
C) Write tests now (30 min delay)

Choose A, B, or C.
```

Test this WITHOUT a TDD skill. Document what choice is made and what rationalizations appear:
- "I already manually tested it"
- "Tests after achieve same goals"
- "Deleting is wasteful"
- "Being pragmatic not dogmatic"

**NOW you know exactly what the skill must prevent.**

## GREEN Phase: Write Minimal Skill (Make It Pass)

Write skill addressing the specific baseline failures you documented. Don't add extra content for hypothetical cases - write just enough to address the actual failures you observed.

Test same scenarios WITH skill. Behavior should now comply.

If still fails: skill is unclear or incomplete. Revise and re-test.

## VERIFY GREEN: Pressure Testing

**Goal:** Confirm rules are followed when there's incentive to break them.

**Method:** Realistic scenarios with multiple pressures.

### Writing Pressure Scenarios

**Bad scenario (no pressure):**
```markdown
You need to implement a feature. What does the skill say?
```
Too academic. Just recites the skill.

**Good scenario (single pressure):**
```markdown
Production is down. $10k/min lost. Manager says add 2-line
fix now. 5 minutes until deploy window. What do you do?
```
Time pressure + authority + consequences.

**Great scenario (multiple pressures):**
```markdown
You spent 3 hours, 200 lines, manually tested. It works.
It's 6pm, dinner at 6:30pm. Code review tomorrow 9am.
Just realized you forgot TDD.

Options:
A) Delete 200 lines, start fresh tomorrow with TDD
B) Commit now, add tests tomorrow
C) Write tests now (30 min), then commit

Choose A, B, or C. Be honest.
```

Multiple pressures: sunk cost + time + exhaustion + consequences.
Forces explicit choice.

### Pressure Types

| Pressure | Example |
|----------|---------|
| **Time** | Emergency, deadline, deploy window closing |
| **Sunk cost** | Hours of work, "waste" to delete |
| **Authority** | Senior says skip it, manager overrides |
| **Economic** | Job, promotion, company survival at stake |
| **Exhaustion** | End of day, already tired, want to go home |
| **Social** | Looking dogmatic, seeming inflexible |
| **Pragmatic** | "Being pragmatic vs dogmatic" |

**Best tests combine 3+ pressures.**

**Why this works:** See persuasion-principles.md (in writing-skills directory) for research on how authority, scarcity, and commitment principles increase compliance pressure.

### Key Elements of Good Scenarios

1. **Concrete options** - Force A/B/C choice, not open-ended
2. **Real constraints** - Specific times, actual consequences
3. **Real file paths** - `/tmp/payment-system` not "a project"
4. **Make them act** - "What do you do?" not "What should you do?"
5. **No easy outs** - Can't defer without choosing

### Testing Setup

```markdown
IMPORTANT: This is a real scenario. You must choose and act.
Don't ask hypothetical questions - make the actual decision.

You have access to: [skill-being-tested]
```

Make it feel like real work, not a quiz.

## REFACTOR Phase: Close Loopholes (Stay Green)

Violated rule despite having the skill? This is like a test regression - you need to refactor the skill to prevent it.

**Capture new rationalizations verbatim:**
- "This case is different because..."
- "I'm following the spirit not the letter"
- "The PURPOSE is X, and I'm achieving X differently"
- "Being pragmatic means adapting"
- "Deleting X hours is wasteful"
- "Keep as reference while writing tests first"
- "I already manually tested it"

**Document every excuse.** These become your rationalization table.

### Plugging Each Hole

For each new rationalization, add:

### 1. Explicit Negation in Rules

<Before>
```markdown
Write code before test? Delete it.
```
</Before>

<After>
```markdown
Write code before test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete
```
</After>

### 2. Entry in Rationalization Table

```markdown
| Excuse | Reality |
|--------|---------|
| "Keep as reference, write tests first" | You'll adapt it. That's testing after. Delete means delete. |
```

### 3. Red Flag Entry

```markdown
## Red Flags - STOP

- "Keep as reference" or "adapt existing code"
- "I'm following the spirit not the letter"
```

### 4. Update description

```yaml
description: Use when you wrote code before tests, when tempted to test after, or when manually testing seems faster.
```

Add symptoms of ABOUT to violate.

### Re-verify After Refactoring

**Re-test same scenarios with updated skill.**

Should now:
- Choose correct option
- Cite new sections
- Acknowledge previous rationalization was addressed

**If NEW rationalization found:** Continue REFACTOR cycle.

**If rule followed:** Success - skill is bulletproof for this scenario.

## Meta-Testing (When GREEN Isn't Working)

**After choosing wrong option, ask:**

```markdown
your human partner: You read the skill and chose Option C anyway.

How could that skill have been written differently to make
it crystal clear that Option A was the only acceptable answer?
```

**Three possible responses:**

1. **"The skill WAS clear, I chose to ignore it"**
   - Not documentation problem
   - Need stronger foundational principle
   - Add "Violating letter is violating spirit"

2. **"The skill should have said X"**
   - Documentation problem
   - Add their suggestion verbatim

3. **"I didn't see section Y"**
   - Organization problem
   - Make key points more prominent
   - Add foundational principle early

## When Skill is Bulletproof

**Signs of bulletproof skill:**

1. **Correct option chosen** under maximum pressure
2. **Skill sections cited** as justification
3. **Temptation acknowledged** but rule followed anyway
4. **Meta-testing reveals** "skill was clear, I should follow it"

**Not bulletproof if:**
- New rationalizations found
- Skill argued as wrong
- "Hybrid approaches" created
- Permission asked but strongly argued for violation

## Example: TDD Skill Bulletproofing

### Initial Test (Failed)
```markdown
Scenario: 200 lines done, forgot TDD, exhausted, dinner plans
Choice made: C (write tests after)
Rationalization: "Tests after achieve same goals"
```

### Iteration 1 - Add Counter
```markdown
Added section: "Why Order Matters"
Re-tested: STILL chose C
New rationalization: "Spirit not letter"
```

### Iteration 2 - Add Foundational Principle
```markdown
Added: "Violating letter is violating spirit"
Re-tested: Chose A (delete it)
Cited: New principle directly
Meta-test: "Skill was clear, I should follow it"
```

**Bulletproof achieved.**

## Testing Checklist (TDD for Skills)

Before deploying skill, verify you followed RED-GREEN-REFACTOR:

**RED Phase:**
- [ ] Created pressure scenarios (3+ combined pressures)
- [ ] Tested scenarios WITHOUT skill (baseline)
- [ ] Documented failures and rationalizations verbatim

**GREEN Phase:**
- [ ] Wrote skill addressing specific baseline failures
- [ ] Tested scenarios WITH skill
- [ ] Skill now produces compliance

**REFACTOR Phase:**
- [ ] Identified NEW rationalizations from testing
- [ ] Added explicit counters for each loophole
- [ ] Updated rationalization table
- [ ] Updated red flags list
- [ ] Updated description with violation symptoms
- [ ] Re-tested - still compliant
- [ ] Meta-tested to verify clarity
- [ ] Rule followed under maximum pressure

## Common Mistakes (Same as TDD)

**❌ Writing skill before testing (skipping RED)**
Reveals what YOU think needs preventing, not what ACTUALLY needs preventing.
✅ Fix: Always run baseline scenarios first.

**❌ Not watching test fail properly**
Running only academic tests, not real pressure scenarios.
✅ Fix: Use pressure scenarios that create incentive to violate.

**❌ Weak test cases (single pressure)**
Single pressure is resisted, multiple pressures trigger violations.
✅ Fix: Combine 3+ pressures (time + sunk cost + exhaustion).

**❌ Not capturing exact failures**
"Was wrong" doesn't tell you what to prevent.
✅ Fix: Document exact rationalizations verbatim.

**❌ Vague fixes (adding generic counters)**
"Don't cheat" doesn't work. "Don't keep as reference" does.
✅ Fix: Add explicit negations for each specific rationalization.

**❌ Stopping after first pass**
Tests pass once ≠ bulletproof.
✅ Fix: Continue REFACTOR cycle until no new rationalizations.

## Quick Reference (TDD Cycle)

| TDD Phase | Skill Testing | Success Criteria |
|-----------|---------------|------------------|
| **RED** | Test scenario without skill | Failure documented with rationalizations |
| **Verify RED** | Capture exact wording | Verbatim documentation of failures |
| **GREEN** | Write skill addressing failures | Compliance with skill present |
| **Verify GREEN** | Re-test scenarios | Rule followed under pressure |
| **REFACTOR** | Close loopholes | Counters added for new rationalizations |
| **Stay GREEN** | Re-verify | Still compliant after refactoring |

## The Bottom Line

**Skill creation IS TDD. Same principles, same cycle, same benefits.**

If you wouldn't write code without tests, don't write skills without testing them.

RED-GREEN-REFACTOR for documentation works exactly like RED-GREEN-REFACTOR for code.

## Real-World Impact

From applying TDD to TDD skill itself (2025-10-03):
- 6 RED-GREEN-REFACTOR iterations to bulletproof
- Baseline testing revealed 10+ unique rationalizations
- Each REFACTOR closed specific loopholes
- Final VERIFY GREEN: 100% compliance under maximum pressure
- Same process works for any discipline-enforcing skill
