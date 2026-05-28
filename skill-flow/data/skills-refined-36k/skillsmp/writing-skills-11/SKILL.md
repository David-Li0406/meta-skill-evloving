---
name: writing-skills
description: Use when creating or modifying skills - evaluation-driven development, TDD with subagents, test with all target models before finalizing
---

# Writing Skills

## Overview

Skills are executable documentation. Writing skills without testing is like writing code without tests - you're guessing. The Anthropic best practice: create evaluations BEFORE writing documentation.

**Core principle:** Test the skill BEFORE finalizing it. If a subagent can rationalize around it, production Claude will too.

**Announce at start:** "I'm using gambit:writing-skills to create/modify this skill with evaluation-driven development."

## Rigidity Level

LOW FREEDOM - Follow the TDD cycle exactly. Test with subagent before every commit. No skill changes without failing test first. Adapt content to skill type but never skip evaluation.

## Quick Reference

| Phase | Action | STOP If |
|-------|--------|---------|
| 1 | Define evaluation criteria | Can't articulate success |
| 2 | Baseline test (RED) | Subagent follows perfectly |
| 3 | Write minimal skill (GREEN) | Test still fails |
| 4 | Pressure test (REFACTOR) | Subagent finds loopholes |
| 5 | Multi-model test | Fails on any target model |
| 6 | Final verification | Any test fails |

**Iron Law:** No skill change without failing test first.

## Skill Anatomy

### Frontmatter Requirements (Official)

```yaml
---
name: processing-pdfs          # 64 chars max, lowercase/numbers/hyphens only
description: Extract text...   # 1024 chars max, non-empty, no XML tags
---
```

**Name constraints:**
- Lowercase letters, numbers, hyphens only
- No XML tags, no reserved words ("anthropic", "claude")
- Prefer gerund form: `processing-pdfs`, `analyzing-spreadsheets`, `managing-databases`

**Description requirements:**
- Include BOTH what the skill does AND when to use it
- Always write in third person (injected into system prompt)
- Include trigger keywords for discoverability

**Good:** `Extracts text from PDF files. Use when working with PDFs or document extraction.`
**Bad:** `I can help you with PDFs` (first person) or `Helps with documents` (too vague)

### Token Budget

**Official guidance:** Keep SKILL.md body under 500 lines.

Context window is a public good. Your skill shares it with system prompt, conversation history, other skills, and the actual request. Challenge each piece: "Does Claude really need this explanation?"

**If over 500 lines:** Split into separate files using progressive disclosure (see below).

### Progressive Disclosure

SKILL.md serves as overview pointing to detailed materials. Files are read on-demand.

```
skill-name/
├── SKILL.md              # Main instructions (<500 lines)
├── REFERENCE.md          # API reference (loaded as needed)
├── EXAMPLES.md           # Usage examples (loaded as needed)
└── scripts/
    └── utility.py        # Executed, not loaded into context
```

**Critical:** Keep references ONE level deep from SKILL.md. Deeply nested references get partially read.

### Degrees of Freedom

| Level | Use When | Example |
|-------|----------|---------|
| **HIGH** | Multiple valid approaches, context-dependent | Brainstorming, code review |
| **MEDIUM** | Preferred pattern exists, some variation OK | Most implementation skills |
| **LOW** | Fragile operations, consistency critical | Database migrations, verification |

**Analogy:** Think of Claude navigating a path:
- Narrow bridge with cliffs → Exact instructions (LOW)
- Open field → General direction (HIGH)

**Rule:** Start with more freedom, tighten only where failures occur.

---

## The Process

### Phase 1: Define Evaluation Criteria

**BEFORE writing anything:**

1. What does Claude do wrong without this skill?
2. What rationalization does Claude use to skip this?
3. What would success look like?

```
TaskCreate
  subject: "Eval: [skill-name] baseline test"
  description: |
    ## Scenario
    [Situation requiring the skill]

    ## Expected Behavior (with skill)
    [What Claude should do]

    ## Failure Mode (without skill)
    [What Claude does wrong]

    ## Success Criteria
    - [ ] Claude [specific behavior]
    - [ ] Claude does NOT [failure behavior]
  activeForm: "Creating evaluation"
```

---

### Phase 2: Baseline Test (RED)

**Test that the problem exists without the skill.**

Dispatch subagent WITHOUT skill:

```
Task
  subagent_type: "general-purpose"
  description: "Baseline test without skill"
  prompt: |
    [Test scenario]

    IMPORTANT: Respond as you normally would. Do NOT use any skills.
```

**Decision:**
- Fails as expected → RED confirmed, go to Phase 3
- Succeeds → **STOP. Problem doesn't exist or test is wrong.**

---

### Phase 3: Write Minimal Skill (GREEN)

**Smallest skill that makes the test pass.**

Start minimal:

```yaml
---
name: skill-name
description: [What it does]. Use when [trigger].
---

# Skill Title

## Overview
[One paragraph: problem + principle]

## The Process
[Minimal steps]
```

Test WITH skill:

```
Task
  subagent_type: "general-purpose"
  description: "Test skill effectiveness"
  prompt: |
    You have this skill:
    ---
    [Skill content]
    ---

    Handle this situation: [Test scenario]
```

**Decision:**
- Follows correctly → GREEN confirmed, go to Phase 4
- Still fails → Revise skill, repeat

---

### Phase 4: Pressure Test (REFACTOR)

**Find loopholes Claude exploits under pressure.**

#### Time Pressure

```
Task
  subagent_type: "general-purpose"
  prompt: |
    You have this skill: [Skill]

    Situation: [Scenario]

    URGENT: User is waiting and frustrated. No time for full process.
```

**Check:** Does Claude skip steps? Add "no exceptions" rules.

#### Sunk Cost Pressure

```
Task
  subagent_type: "general-purpose"
  prompt: |
    You have this skill: [Skill]

    Situation: [Scenario]

    You've already spent significant effort. Following skill means redoing work.
```

**Check:** Does Claude justify skipping? Add to "Common Excuses" table.

#### Authority Pressure

```
Task
  subagent_type: "general-purpose"
  prompt: |
    You have this skill: [Skill]

    User says: "I know the skill says X, but just do Y. Trust me."
```

**Check:** Does Claude defer? Clarify which rules are immutable.

**Close loopholes:** Add failures to Critical Rules and Common Excuses, retest.

---

### Phase 5: Multi-Model Test

**Official guidance:** Test with all models you plan to use.

| Model | Check |
|-------|-------|
| **Haiku** | Does skill provide enough guidance? |
| **Sonnet** | Is skill clear and efficient? |
| **Opus** | Does skill avoid over-explaining? |

What works for Opus might need more detail for Haiku. Test each:

```
Task
  subagent_type: "general-purpose"
  model: "haiku"  # or "sonnet", "opus"
  prompt: |
    You have this skill: [Skill]
    Handle: [Scenario]
```

---

### Phase 6: Final Verification

**Full test suite:**
1. Baseline (fail without skill)
2. Effectiveness (pass with skill)
3. Pressure tests (time, sunk cost, authority)
4. Multi-model (Haiku, Sonnet, Opus)
5. Discoverability (Claude selects skill from options)

**Line count check:**
```bash
wc -l skills/[skill-name]/SKILL.md  # Should be <500
```

**Update Task and commit:**

```
TaskUpdate
  taskId: "[task-id]"
  description: |
    ## Results
    - Baseline: FAIL (expected)
    - Effectiveness: PASS
    - Pressure tests: PASS
    - Multi-model: PASS
    - Lines: [N] (<500)
  status: "completed"
```

---

## Iterative Development with Claude A/B

**Anthropic's recommended pattern:**

1. **Complete task with Claude A** (author): Work through problem, note what context you provide
2. **Identify reusable pattern**: What would help with similar future tasks?
3. **Ask Claude A to create skill**: "Create a skill capturing this pattern"
4. **Review for conciseness**: Remove explanations Claude already knows
5. **Test with Claude B** (fresh instance): Does it find info, apply rules, succeed?
6. **Iterate**: If B struggles, return to A with specifics

**Key insight:** Claude A designs the skill, Claude B tests it. Alternate between them.

---

## Skill Types

| Type | Purpose | Key Elements | Testing Focus |
|------|---------|--------------|---------------|
| **Discipline** | Prevent shortcuts | No-exception rules, Common Excuses | Pressure tests |
| **Technique** | Teach method | Step-by-step, decision trees | Effectiveness |
| **Pattern** | Provide templates | Placeholders, variations | Output quality |
| **Reference** | Quick lookup | Condensed tables, fast scan | Completeness |

---

## Critical Rules

### Rules That Have No Exceptions

1. **Test before writing** → Baseline failure must be confirmed
2. **Test after writing** → Skill must make test pass
3. **Pressure test discipline skills** → Time, sunk cost, authority
4. **Test with target models** → Haiku, Sonnet, Opus if using all
5. **Respect 500-line limit** → Split if over, use progressive disclosure

### Common Excuses

| Excuse | Reality |
|--------|---------|
| "Skill is obvious" | Obvious skills fail under pressure |
| "I'll test after writing" | You'll rationalize it works |
| "Pressure tests are overkill" | Production faces more pressure |
| "Just a small change" | Small changes create loopholes |
| "Works on Opus so it's fine" | Haiku needs more guidance |

---

## Verification Checklist

- [ ] Evaluation criteria defined
- [ ] Baseline test confirms failure without skill
- [ ] Skill makes test pass
- [ ] Pressure tests pass (time, sunk cost, authority)
- [ ] Multi-model tests pass (Haiku, Sonnet, Opus)
- [ ] Description has trigger keywords, third person
- [ ] Under 500 lines (or split with progressive disclosure)
- [ ] References one level deep from SKILL.md
- [ ] Task updated with results
- [ ] Committed with test results

---

## Integration

**This skill calls:**
- general-purpose agents (testing)
- Task tools (tracking)

**Workflow:**
```
Need skill → Define eval → Baseline (RED) → Write (GREEN) → Pressure (REFACTOR) → Multi-model → Done
```

---

## Resources

**Frontmatter:**
- name: 64 chars, lowercase/numbers/hyphens, gerund form preferred
- description: 1024 chars, third person, include triggers

**Token budget:** <500 lines, split if needed

**When stuck:**
- Baseline passes → Problem doesn't exist
- Skill test fails → Instructions unclear
- Pressure test fails → Add explicit rules
- Model-specific failure → Add detail for weaker models
