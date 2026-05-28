---
title: Subagent Quality Review Framework
description: Comprehensive quality review framework with automated validation, manual checklists, scoring rubrics, and approval criteria for subagent creation
keywords: quality review, validation, subagents, scoring, checklists, frontmatter, prompt conciseness, tool selection, skill integration, color coding
skill: creating-subagents
---

# Subagent Quality Review

Comprehensive quality review framework for subagent creation. Use this before deploying any subagent.

## Overview

This review process ensures subagents meet production standards through systematic validation, scoring, and testing. The review is organized into **6 scoring categories**, each containing specific checklist items. Scores are determined by the percentage of checks passed within each category.

**Target**: All categories ≥4/5 for approval.

---

## Review Workflow

Follow these 4 steps for every subagent review:

### Step 1: Automated Pre-Flight Gate

**Purpose**: Catch structural and syntactic errors before manual review.

Execute the comprehensive validation script:

```bash
python3 scripts/validate_subagent.py /path/to/subagent.md
```

**For quick iteration during development:**

```bash
python3 scripts/validate_subagent.py /path/to/subagent.md --minimal
```

**Desired outcome**: 100% pass rate (15/15 checks, errors only - warnings are advisory).

**The --minimal flag shows:**
- One-line score summary with key metrics (word count, tools, skill refs)
- Only failures and warnings (no passing checks)
- Actionable recommendations based on metrics
- Perfect for rapid iteration during subagent development

**Understanding Errors vs Warnings:**
- **Errors** (✗ red): Block validation, must be fixed to pass
- **Warnings** (⚠ yellow): Review manually, not blocking, may be acceptable
- **Info** (ℹ cyan): Informational metrics, always pass

**Warnings you may see:**
- Word count outside 50-200: May be acceptable if prompt is clear/complete
- No skill references: Acceptable for simple orchestration subagents
- Directive language: May flag non-standard openings - review for clarity
- Time-sensitive content: May flag technical terms - review context

### Step 2: Manual Quality Review

**Purpose**: Deep assessment of subagent quality, usability, and completeness.

For each of the 6 categories in "Scoring Categories" below:

1. **Review all checklist items** - Read each item carefully
2. **Mark as pass (✓) or fail (✗)** - Some items reference Step 1 automated results, most require manual judgment
3. **Calculate percentage** - (items passed / total items) × 100
4. **Assign score** - Use rubric below based on percentage
5. **Document issues** - Note specific problems for any failed items

**Scoring Rubric (applies to all 6 categories):**

- **5 (Excellent)**: 90-100% of checks pass
- **4 (Good)**: 75-89% of checks pass
- **3 (Acceptable)**: 60-74% of checks pass
- **2 (Needs Work)**: 40-59% of checks pass
- **1 (Poor)**: <40% of checks pass

**Target**: All categories score ≥4/5 for approval.

### Step 3: Test the Subagent

**IMPORTANT**: Subagents are generally safe to test (read-only operations, isolated context).

**Testing workflow:**
```bash
# Structure check
cat /path/to/subagent.md | head -30

# Invoke subagent (usually safe!)
# Option 1: Explicit invocation
"Use the [subagent-name] subagent to [task description]"

# Option 2: Test proactive triggering (if description includes proactive patterns)
[Say something that should trigger the subagent]

# Observe:
# - Loads correctly?
# - Understands its role?
# - Has appropriate tool access?
# - References skills correctly?
# - Produces expected results?
```

**When to be cautious:**
- Subagents with Write/Edit tools (test in isolated directory)
- Subagents with Bash tools (review what bash commands it might run)
- Subagents with external API access

**Most subagents are safe**: Research, analysis, code reading, test running (read-only) subagents can be freely tested.

### Step 4: Apply Recommendation Logic

Based on scores from Step 2:

- **APPROVE** - All scores ≥4, ready for deployment
- **NEEDS_REVISION** - Any score <4, requires improvements
- **CONSIDER_DIFFERENT_TYPE** - Artifact Type score ≤2, might be better as skill/command

Document all issues with:
- Category affected
- Severity: critical (1-2), major (3), minor (4)
- Specific problem description
- Actionable improvement suggestion

---

## Scoring Categories

**How to use these checklists:**

Each category below contains checklist items for manual review. Some items were already validated by the automated script in Step 1 (syntax, structure, required fields) - mark these as ✓ if Step 1 passed. Other items require manual judgment (quality, clarity, appropriateness) - carefully assess these during review.

**Review each category:**
1. Go through all checklist items
2. Mark ✓ (pass) or ✗ (fail) for each
3. Calculate: (items passed / total items) × 100
4. Assign score 1-5 using rubric from Step 2
5. Document issues in "Issues identified" section

---

### Category 1: Frontmatter & Discovery

The YAML frontmatter determines when Claude invokes the subagent and what capabilities it has. Quality here directly impacts discoverability and safety.

#### Checklist Items

**Required Fields** (from automated validation)
- [ ] `name` field present
- [ ] `description` field present
- [ ] `tools` field present
- [ ] `model` field present
- [ ] `color` field present
- [ ] YAML syntax valid

**Name Quality**
- [ ] Name is 64 characters or less
- [ ] Name is descriptive and clear
- [ ] Name reflects agent's purpose
- [ ] Name follows kebab-case convention
- [ ] Name avoids generic terms like "helper", "manager", "handler"

**Description Quality**
- [ ] Description written in third person
- [ ] Description includes WHAT the subagent does
- [ ] Description includes WHEN to use it (proactive triggers)
- [ ] Description is clear and specific
- [ ] Description under 500 characters
- [ ] No first person ("I can...") or second person ("You should...")

**Model Selection**
- [ ] Appropriate for task complexity
- [ ] `inherit` used when parent model sufficient
- [ ] `haiku` for simple, fast tasks
- [ ] `sonnet` for most tasks
- [ ] `opus` only if truly needed

**Color Coding** (see references/color-codes.md)
- [ ] Color field is valid (purple/blue/green/yellow/orange/red/cyan/magenta/white)
- [ ] Color matches primary purpose
- [ ] Color choice documented if non-obvious

**Total checks**: 22

**Score**: _____ /5 (based on % passed)

**Issues identified**:

---

### Category 2: Prompt Conciseness & Quality

Subagent prompts should be short, directive, and focused. Verbose prompts waste tokens and reduce effectiveness.

#### Checklist Items

**Prompt Length** (from automated validation)
- [ ] Word count is in reasonable range (50-200 target)
- [ ] If <50 words: prompt is clear despite brevity
- [ ] If >200 words: excess justified OR should be moved to skill

**Directive Language**
- [ ] Prompt starts with imperative/directive statements
- [ ] Uses active voice
- [ ] Clear, actionable instructions
- [ ] No lengthy explanations
- [ ] No pedagogical scaffolding

**Conciseness**
- [ ] Every sentence adds value
- [ ] No redundant instructions
- [ ] No over-explanation of concepts Claude knows
- [ ] Focused on orchestration, not education
- [ ] Gets to the point quickly

**Structure**
- [ ] Logical flow
- [ ] Prioritized instructions (most important first)
- [ ] Clear constraints if needed
- [ ] Verification steps if applicable
- [ ] Skill references clearly indicated

**Writing Style**
- [ ] Uses imperative form (no "you", "I", "we")
- [ ] No time-sensitive information
- [ ] No platform-specific paths
- [ ] Consistent terminology
- [ ] Professional tone

**Total checks**: 18

**Score**: _____ /5 (based on % passed)

**Issues identified**:

---

### Category 3: Tool Selection

Tool access determines what the subagent can do. Minimal necessary tools enhance safety and clarity.

#### Checklist Items

**Tool Count** (from automated validation)
- [ ] Tool count is reasonable for the task
- [ ] Not granting all tools by default

**Tool Justification**
- [ ] Every tool is necessary for the task
- [ ] No unnecessary tools granted
- [ ] Read-only tools preferred when possible
- [ ] Write/Edit tools justified if included
- [ ] Bash tools justified if included

**Tool Patterns**
- [ ] Read-only research: Read, Grep, Glob appropriate
- [ ] Code modification: Read, Edit, Grep, Glob, Bash appropriate
- [ ] Testing: Bash, Read, Grep appropriate
- [ ] Documentation: Read, Write, Grep, Glob appropriate

**Safety Considerations**
- [ ] Destructive operations require clear justification
- [ ] Tool access matches description
- [ ] No overly permissive access
- [ ] Tools enable the task without excess

**Tool List Format**
- [ ] Tools specified correctly (comma or space separated)
- [ ] Tool names are valid Claude Code tools
- [ ] No typos in tool names

**Total checks**: 15

**Score**: _____ /5 (based on % passed)

**Issues identified**:

---

### Category 4: Skill Integration

Subagents should leverage skills for complex knowledge instead of embedding instructions in prompts.

#### Checklist Items

**Skill References** (from automated validation)
- [ ] Skill references counted
- [ ] Complex prompts (>100 words) reference skills appropriately

**Skill Usage Patterns**
- [ ] Skills invoked with Skill(command='...')
- [ ] Skill invocations are valid (skills exist)
- [ ] Skills used for procedural knowledge
- [ ] Skills used for reference material
- [ ] Skills used for complex workflows

**Knowledge Organization**
- [ ] Subagent orchestrates, skills educate
- [ ] No duplication between prompt and skills
- [ ] Prompt stays lean by delegating to skills
- [ ] Clear boundaries between subagent role and skill role

**Integration Quality**
- [ ] Skill invocations are clear
- [ ] Multiple skill invocations organized logically
- [ ] Skills invoked at appropriate points
- [ ] Skill context sufficient for task

**Skill Creation Decision**
- [ ] If prompt >200 words with procedures: skill should be created
- [ ] If prompt includes reference material: should be in skill
- [ ] If prompt includes templates: should be in skill assets
- [ ] Simple orchestration doesn't need skills

**Total checks**: 16

**Score**: _____ /5 (based on % passed)

**Issues identified**:

---

### Category 5: Invocation Patterns & Proactivity

Description should clearly indicate when the subagent should be invoked, enabling both explicit and proactive usage.

#### Checklist Items

**Proactive Triggers** (from automated validation)
- [ ] Description includes invocation patterns

**Trigger Clarity**
- [ ] Clear when to invoke explicitly
- [ ] Clear when to invoke proactively
- [ ] Specific keywords or scenarios mentioned
- [ ] Triggers are unambiguous
- [ ] Multiple trigger scenarios if applicable

**Proactive Pattern Quality**
- [ ] "Use proactively when..." or similar language
- [ ] Specific conditions for proactive invocation
- [ ] Not too broad (avoid triggering incorrectly)
- [ ] Not too narrow (allow reasonable invocations)

**Invocation Examples**
- [ ] Easy to understand when agent applies
- [ ] Examples match description
- [ ] Both explicit and proactive patterns clear
- [ ] No confusion with other agents

**Total checks**: 13

**Score**: _____ /5 (based on % passed)

**Issues identified**:

---

### Category 6: Artifact Type Validation

Validate that a subagent is the appropriate artifact type for this task.

#### Checklist Items

**Subagent Appropriateness**
- [ ] Task requires separate context (not just main thread)
- [ ] Task is recurring (not one-off)
- [ ] Task has clear scope and boundaries
- [ ] Task benefits from specialized role
- [ ] Task is autonomous (not heavily interactive)

**Not Better as Skill**
- [ ] Task doesn't need bundled resources (scripts, references, templates)
- [ ] Task is about orchestration, not education
- [ ] Task doesn't require >1000 words of procedural knowledge
- [ ] Prompt stays concise (≤200 words is achievable)

**Not Better as Command**
- [ ] Task is NOT explicitly invoked every time (allows proactive)
- [ ] Task doesn't fit "manual trigger" pattern
- [ ] Task benefits from autonomous context

**Scope Validation**
- [ ] Single responsibility
- [ ] Clear domain boundaries
- [ ] No scope creep
- [ ] Purpose is distinct from other agents

**Alternative Recommendations**
- [ ] If needs resources: consider skill
- [ ] If always manual: consider command
- [ ] If too broad: split into multiple agents
- [ ] If too narrow: use main thread

**Total checks**: 16

**Score**: _____ /5 (based on % passed)

**Issues identified**:

---

## Additional Validation Checks

These are yes/no gates that must pass regardless of category scores.

### Security Considerations
- [ ] Tool access is minimal for the task
- [ ] No destructive operations without clear justification
- [ ] Safe to test in normal development environment
- [ ] Input validation appropriate for tools used

### Completeness
- [ ] All Skill() invocations reference existing skills
- [ ] Color code is appropriate for purpose (see references/color-codes.md)
- [ ] Model selection justified

### Final Verification
- [ ] YAML syntax valid
- [ ] No critical typos in prompt
- [ ] Prompt is understandable
- [ ] Clear what the subagent does

---

## Score Summary

Complete after scoring all categories:

| Category | Score | Status |
|----------|-------|--------|
| 1. Frontmatter & Discovery | ___/5 | ___ |
| 2. Prompt Conciseness & Quality | ___/5 | ___ |
| 3. Tool Selection | ___/5 | ___ |
| 4. Skill Integration | ___/5 | ___ |
| 5. Invocation Patterns & Proactivity | ___/5 | ___ |
| 6. Artifact Type Validation | ___/5 | ___ |
| **Average** | **___/5** | ___ |

**Status codes**: ✓ Pass (≥4) | ⚠ Review (3) | ✗ Fail (<3)

---

## Final Recommendation

Based on scores and validation checks:

**[ ] APPROVE** - All scores ≥4, all validation checks pass
- Subagent is ready for deployment
- Test in development environment first
- Document any special considerations

**[ ] NEEDS_REVISION** - Any score <4 or validation checks fail
- Address all issues documented in category reviews
- Re-run quality review after improvements
- Focus on categories with scores <4

**[ ] CONSIDER_DIFFERENT_TYPE** - Artifact Type validation concerns
- Consider if subagent would be better as skill or command
- Skills: Needs bundled resources, >200 words of knowledge
- Commands: Always manually invoked, explicit workflow
- Main thread: One-off tasks, no need for separate context

---

## Common Anti-Patterns

Watch for these frequent mistakes:

**Frontmatter Issues**
- ✗ Vague description without invocation patterns
- ✗ Description in first/second person
- ✗ Missing or invalid color field
- ✗ Wrong model selection for task complexity

**Prompt Issues**
- ✗ Verbose prompts (>200 words with procedures)
- ✗ Educational content (explaining concepts)
- ✗ Second person language ("you should...")
- ✗ Embedding reference material in prompt
- ✗ Missing skill references for complex tasks

**Tool Selection Issues**
- ✗ Granting all tools by default
- ✗ Unnecessary tools included
- ✗ Missing tools needed for task
- ✗ Overly permissive access

**Skill Integration Issues**
- ✗ Duplicating skill content in prompt
- ✗ Not invoking skills for complex knowledge
- ✗ Invalid skill invocations
- ✗ Poor delegation boundaries

**Invocation Pattern Issues**
- ✗ No proactive trigger patterns
- ✗ Unclear when to use agent
- ✗ Too broad (triggers on everything)
- ✗ Too narrow (never triggers)

**Artifact Type Issues**
- ✗ Should be skill (needs resources, >200 words)
- ✗ Should be command (always manual invocation)
- ✗ Too broad (multiple responsibilities)
- ✗ Too narrow (no need for separate context)

---

## Quality Standards Summary

A production-ready subagent must be:

1. **Discoverable** - Clear description with proactive triggers
2. **Concise** - 50-200 words, directive language, no bloat
3. **Safe** - Minimal necessary tools, clear boundaries
4. **Integrated** - Leverages skills for complex knowledge
5. **Focused** - Single responsibility, clear domain
6. **Testable** - Can be tested safely in development
7. **Appropriate** - Right artifact type for the task

**Minimum standard**: All categories score 4+/5, all validation checks pass.

---

## Using the Validation Script

### Quick Iteration Mode

During development, use `--minimal` for fast feedback:

```bash
python3 scripts/validate_subagent.py /path/to/subagent.md --minimal
```

**Output shows:**
- One-line score with percentage
- Key metrics (word count, tool count, skill references)
- Only errors and warnings (no passing checks)
- Actionable recommendations

**Example minimal output:**
```
doc-writer: 15/15 (100%) | 0 errors, 1 warnings | ✓ PASS
Metrics: 85 words (target: 50-200) | 4 tools | 2 skill refs

Warnings:
  ⚠ skill integration (warning)

Recommendations:
```

### Full Validation Mode

For final review before deployment:

```bash
python3 scripts/validate_subagent.py /path/to/subagent.md
```

Shows:
- Detailed category-by-category checks
- All passing/failing checks with context
- Full error descriptions with fixes
- Complete metrics summary
- Comprehensive recommendations

---

## Automated Checks Reference

The validation script (`scripts/validate_subagent.py`) performs 15 automated checks:

**Category 1: File Structure** (2 checks)
1. Subagent file exists
2. Subagent file readable

**Category 2: Frontmatter Structure** (2 checks)
3. Valid YAML frontmatter
4. Required fields present (name, description, tools, model, color)

**Category 3: Frontmatter Content** (5 checks)
5. Name length ≤64 chars
6. Model value valid (inherit/sonnet/haiku/opus)
7. Color value valid (purple/blue/green/yellow/orange/red/cyan/magenta/white)
8. Description uses third person
9. Description includes invocation patterns

**Category 4: Prompt Quality** (3 checks)
10. Word count in reasonable range (50-200 target, warnings if outside)
11. Prompt uses directive language (warning if unclear)
12. Skill integration appropriate (warning if >100 words with no skill refs)

**Category 5: Writing Style** (3 checks)
13. Uses imperative form (no you/I/we)
14. No time-sensitive content (warning only)
15. No Windows-style paths

**Metrics reported** (informational, not validation checks):
- Word count (body content, excluding frontmatter)
- Tool count (number of tools granted)
- Skill() invocations
- Line count

All checks must pass for approval, except warnings which are advisory.

---

## Color Code Quick Reference

When reviewing color selection, reference this table:

| Color   | Purpose               | Use For                                     |
|---------|-----------------------|---------------------------------------------|
| purple  | Review/Audit          | Code review, security audit, QA validation  |
| blue    | Implementation        | Feature building, API development, coding   |
| green   | Testing               | Test running, validation, verification      |
| yellow  | Documentation         | Doc writing, API docs, tutorials            |
| orange  | Maintenance           | Refactoring, formatting, dependency updates |
| red     | Debugging             | Error analysis, troubleshooting, debugging  |
| cyan    | Research              | Codebase exploration, analysis, research    |
| magenta | Deployment            | Deployment, CI/CD, release management       |
| white   | General               | Multi-purpose, orchestration, coordination  |

See `references/color-codes.md` for complete details.
