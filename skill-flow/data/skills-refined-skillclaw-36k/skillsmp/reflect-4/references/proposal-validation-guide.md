# Proposal Validation Guide

This guide explains how the reflect-critic agent validates proposals to ensure high-quality skill improvements.

## Overview

The multi-agent reflection workflow (Phase 4) uses a **generator-critic pattern**:

1. **Generator** (reflect skill): Analyzes conversation, identifies signals, drafts proposal
2. **Critic** (reflect-critic agent): Validates proposal quality, scores 0-100, recommends action
3. **Orchestrator** (reflect skill): Incorporates feedback, presents final proposal to user

This two-pass approach improves proposal quality by 15-20% according to MAR (Multi-Agent Reflexion) research.

---

## Validation Framework

The critic validates proposals against three dimensions:

### 1. 12-Factor Agent Principles (0-50 points)

Based on HumanLayer.dev research, the top 5 most relevant factors are scored:

**Factor 1: Single Responsibility**
- Each proposed change has a clear, single purpose
- Concerns are properly separated
- ❌ RED FLAG: Mixing multiple unrelated changes

**Factor 3: Configuration via Environment**
- User preferences are configurable, not hard-coded
- Behavior can be adjusted without code changes
- ❌ RED FLAG: Hard-coding preferences that should be configurable

**Factor 5: Strict Separation of Execution Stages**
- Build/run/validation phases are clearly separated
- Each phase can fail independently with clear errors
- ❌ RED FLAG: Conflating planning with execution

**Factor 8: Scale via Process Model**
- Skill can handle varying conversation sizes
- Degrades gracefully with large inputs
- ❌ RED FLAG: Fails on large conversations without fallback

**Factor 9: Disposability**
- Skill execution can be interrupted safely
- Partial results are handled gracefully
- ❌ RED FLAG: Leaves system in inconsistent state on failure

### 2. Signal-to-Proposal Alignment (0-20 points)

**Evidence Quality** (0-10 points)
- Are the signals (corrections, successes, edge cases) concrete?
- Is there clear evidence for each proposed change?
- ❌ RED FLAG: Vague signals like "user seems to prefer..."

**Signal Coverage** (0-10 points)
- Does the proposal address ALL identified signals?
- Are high-confidence signals prioritized appropriately?
- ❌ RED FLAG: Ignores external feedback (HIGH confidence signals)

### 3. Implementation Feasibility (0-20 points)

**Backward Compatibility** (0-10 points)
- Will this break existing workflows?
- Are migration steps provided if breaking?
- ❌ RED FLAG: Breaking change without migration path

**Testability** (0-10 points)
- Can the change be validated?
- Are success criteria clear?
- ❌ RED FLAG: No way to verify the improvement worked

---

## Scoring Rubric

**90-100 (Excellent)** → APPROVE
- Strong evidence, clear implementation, follows all principles
- Action: Proceed to user immediately

**70-89 (Good)** → APPROVE with suggestions
- Solid proposal with small gaps or unclear areas
- Action: Incorporate suggestions, then proceed to user

**50-69 (Needs work)** → REVISE
- Good intent but significant issues in implementation or alignment
- Action: Revise based on feedback, re-validate with critic

**0-49 (Poor)** → REJECT
- Misaligned with signals, violates principles, or infeasible
- Action: Reject proposal, consider alternative approach

---

## Common Anti-Patterns

Watch for these red flags in proposals:

### 🚩 Scope Creep
**Problem**: Proposal tries to fix too many unrelated issues

**Example**:
```
🔴 HIGH: Add accessibility labels
🔴 HIGH: Refactor state management
🔴 HIGH: Update color palette
🟡 MED: Add TypeScript support
```

**Why bad**: Mixes accessibility, architecture, design, and tooling concerns

**Fix**: Split into 4 separate proposals, each focused on one concern

---

### 🚩 Vague Evidence
**Problem**: Signals are not concrete or specific

**Example**:
```
Signals: 2 corrections
🔴 HIGH: User seems to prefer simpler components
```

**Why bad**: "seems to prefer" is not evidence - what did user actually say/do?

**Fix**:
```
Signals: 2 corrections
Evidence: User said "too complex" twice, requested simpler version
🔴 HIGH: Keep components under 200 lines (user correction)
```

---

### 🚩 Signal Mismatch
**Problem**: Proposed change doesn't address identified signals

**Example**:
```
Signals: 3 corrections about missing tests
Proposed:
🔴 HIGH: Add TypeScript type definitions
```

**Why bad**: Proposal is about types, but signals are about tests

**Fix**:
```
Signals: 3 corrections about missing tests
Proposed:
🔴 HIGH: Require tests for all new functions (3 user corrections)
```

---

### 🚩 Breaking Changes Without Migration
**Problem**: Changes existing behavior without providing migration path

**Example**:
```
🔴 HIGH: Change skill output format to JSON
```

**Why bad**: Existing workflows expect current format, will break immediately

**Fix**:
```
🔴 HIGH: Add --json flag for JSON output (default: current format)
🟡 MED: Deprecation notice for old format (remove in 3 months)
```

---

### 🚩 Hard-Coded Preferences
**Problem**: User preferences are hard-coded instead of configurable

**Example**:
```
🔴 HIGH: Always use Tailwind CSS (never allow inline styles)
```

**Why bad**: Different users may have different preferences

**Fix**:
```
🔴 HIGH: Prefer Tailwind CSS by default (configurable via ~/.claude/memories)
Implementation: Check user preferences, fallback to Tailwind if not specified
```

---

### 🚩 Untestable Changes
**Problem**: No way to verify the improvement worked

**Example**:
```
🟡 MED: Make code more readable
```

**Why bad**: "More readable" is subjective and can't be measured

**Fix**:
```
🟡 MED: Limit functions to 50 lines (readability guideline)
Success criteria: Future sessions have no "function too long" corrections
```

---

### 🚩 Premature Optimization
**Problem**: Optimizing for hypothetical future cases

**Example**:
```
Signals: 1 edge case with large file
🔴 HIGH: Add streaming support, caching, and async processing
```

**Why bad**: Over-engineering for single edge case

**Fix**:
```
Signals: 1 edge case with large file
🟡 MED: Add warning for files >10MB (suggest chunking)
Note: If happens repeatedly, revisit streaming support
```

---

## Quality Checklist

Before accepting a proposal, verify:

### Evidence
- [ ] Each HIGH item has explicit correction or external feedback
- [ ] Each MED item has 2+ occurrences or clear pattern
- [ ] LOW items are marked as optional/preference
- [ ] External feedback (tests/lint) is prioritized over conversation signals

### Implementation
- [ ] Each change is actionable (clear what to do)
- [ ] Changes don't break existing workflows (or provide migration)
- [ ] Success criteria are defined (how to verify improvement)
- [ ] Changes are scoped appropriately (not too broad/narrow)

### Principles
- [ ] Single responsibility - each change has one purpose
- [ ] Configurable - preferences aren't hard-coded
- [ ] Testable - can verify the change worked
- [ ] Backward compatible - existing workflows still work
- [ ] Handles failures gracefully - doesn't leave inconsistent state

---

## Example: Good vs Bad Proposals

### ❌ Bad Proposal

```
Skill Reflection: frontend-design

Signals: 2 corrections, 1 success

Proposed changes:
🔴 HIGH: Improve component quality
🔴 HIGH: Make code better
🟡 MED: Add features users want

Commit: "frontend-design: improvements"
```

**Why bad**:
- Vague changes ("improve", "better", "features users want")
- No evidence linking signals to changes
- Untestable (how to verify "quality" improved?)
- Unclear what to actually implement

**Critic score**: 15/100 → REJECT

---

### ✅ Good Proposal

```
Skill Reflection: frontend-design

Signals: 2 corrections, 3 external feedback (accessibility tests)

Proposed changes:
🔴 HIGH: Add aria-label to all buttons (3 test failures)
   Evidence: test_accessibility.py failed on Login, Submit, Cancel buttons
   Implementation: Check for aria-label in button generation code

🔴 HIGH: Use semantic HTML (2 user corrections)
   Evidence: User said "use <button> not <div onClick>" twice
   Implementation: Update component templates to use proper elements

🟡 MED: Prefer CSS Grid for card layouts (1 pattern)
   Evidence: User chose Grid over Flexbox for dashboard cards
   Implementation: Default to Grid for grid-like layouts, allow Flexbox override

Commit: "frontend-design: accessibility + semantic HTML"

Critic Score: 88/100 (APPROVE with suggestions)
Critic: Excellent evidence. Suggest clarifying when Grid vs Flexbox.
```

**Why good**:
- Concrete changes with clear evidence
- External feedback (tests) prioritized as HIGH
- Each change is actionable and testable
- Success criteria implicit (tests pass, no more corrections)
- Scoped appropriately (accessibility + semantics related)

**Critic score**: 88/100 → APPROVE with suggestions

---

## Using Critic Feedback

### If Score 90-100 (Excellent)
**Action**: Accept proposal as-is
- Proceed directly to user
- All validation passed

### If Score 70-89 (Good)
**Action**: Incorporate suggestions
- Read critic's suggestions carefully
- Make minor improvements
- Don't re-validate (proceed to user)

**Example**:
```
Critic: "88/100 - APPROVE with suggestions"
Suggestion: "Clarify when Grid is preferred vs Flexbox"

Updated proposal:
🟡 MED: Prefer CSS Grid for grid-like layouts (card dashboards, galleries)
   Note: Use Flexbox for linear layouts (navigation, toolbars)
```

### If Score 50-69 (Needs work)
**Action**: Revise and re-validate
- Read critic's detailed feedback
- Address major concerns
- Re-validate with critic before showing to user

**Example**:
```
Critic: "62/100 - REVISE"
Concerns:
- HIGH item lacks evidence (only 1 occurrence)
- Breaking change without migration
- Untestable improvement claim

Actions:
- Downgrade to MED (single occurrence)
- Add backward compatibility shim
- Define measurable success criteria
- Re-validate with critic
```

### If Score 0-49 (Poor)
**Action**: Reject and reconsider
- Proposal fundamentally flawed
- Consider if signals were misinterpreted
- May need to gather more data before proposing

**Example**:
```
Critic: "35/100 - REJECT"
Reason: "Proposal addresses TypeScript types, but all signals were about missing tests"

Alternative: Focus on test coverage (align with actual signals)
```

---

## Best Practices

### For High-Quality Proposals

1. **Start with evidence**: What did user actually say/do?
2. **Prioritize external feedback**: Tests > Lint > Conversation
3. **One concern per proposal**: Don't mix accessibility + architecture
4. **Make it testable**: Define success criteria
5. **Protect existing workflows**: Backward compatibility matters
6. **Be specific**: "Add aria-labels" > "Improve accessibility"
7. **Accept suggestions**: Critic feedback improves quality 15-20%

### For Using the Critic

1. **Always validate**: Don't skip Step 3B (critic validation)
2. **Read feedback carefully**: Critic explains WHY score is low
3. **Trust low scores**: 0-49 = fundamentally flawed, don't ignore
4. **Incorporate suggestions**: 70-89 means small improvements help
5. **Re-validate after major revisions**: 50-69 needs second look
6. **Track scores in metrics**: Learn which patterns score well

---

*Part of Phase 4: Multi-Agent Reflection*
*See agents/reflect-critic.md for complete critic agent definition*
