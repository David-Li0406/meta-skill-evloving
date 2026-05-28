---
title: Command Quality Review Framework
description: Comprehensive quality review framework with automated validation, manual checklists, scoring rubrics, and approval criteria for command creation
keywords: quality review, validation, commands, scoring, checklists, frontmatter, preflight checks, context gathering, task instructions, tool restrictions
skill: creating-commands
---

# Command Quality Review

Comprehensive quality review framework for command creation. Use this before deploying any command.

## Overview

This review process ensures commands meet production standards through systematic validation, scoring, and testing. The review is organized into **6 scoring categories**, each containing specific checklist items. Scores are determined by the percentage of checks passed within each category.

**Target**: All categories ≥4/5 for approval.

---

## Review Workflow

Follow these 4 steps for every command review:

### Step 1: Automated Pre-Flight Gate

**Purpose**: Catch structural and syntactic errors before manual review.

**RECOMMENDED**: During command development, use `--minimal` mode for rapid iteration:

```bash
python3 scripts/validate_command.py /path/to/command.md --minimal
```

Use this mode **early and often** while drafting your command. Fix issues incrementally.

**For final review before deployment**, run full validation:

```bash
python3 scripts/validate_command.py /path/to/command.md
```

**Desired outcome**: 100% pass rate (17/17 checks).

**The --minimal flag shows:**
- One-line score summary with key metrics
- Only failures and warnings (no passing checks)
- Actionable recommendations based on metrics
- Perfect for rapid iteration during command development

**Understanding Errors vs Warnings:**
- **Errors** (✗ red): Block validation, must be fixed to pass
- **Warnings** (⚠ yellow): Review manually, not blocking, may be acceptable
- **Info** (ℹ cyan): Informational metrics, always pass

**Context Matters:**
The validation script performs pattern-based analysis and may flag content that is contextually appropriate:
- **Bad examples**: "You should do X" in anti-pattern examples
- **Technical terms**: "current branch", "latest commit" (not time-sensitive in git context)
- **Quoted content**: Examples showing incorrect usage patterns
- **Documentation**: References to user actions in context sections

**Always apply judgment** when reviewing flagged items. Ask yourself:
- Is this in an example block showing what NOT to do?
- Is this technical terminology (like "current branch") rather than time reference?
- Is this describing expected behavior vs prescriptive instruction?

**Common false positives:**
- Line count >200: May warrant converting to skill
- No bash commands: Commands without preflight checks (acceptable for some commands)
- Time-sensitive content: Often flags "current branch", "latest commit" - review context
- Person usage: May flag "you" in anti-pattern examples or documentation blocks

### Step 2: Manual Quality Review

**Purpose**: Deep assessment of command quality, usability, and completeness.

**IMPORTANT**: This review requires contextual interpretation. The automated script performs pattern-based analysis and may flag content that is contextually appropriate (e.g., anti-pattern examples, technical terms like "current branch", quoted incorrect usage). Always apply judgment when reviewing flagged items.

For each of the 6 categories in "Scoring Categories" below:

1. **Review all checklist items** - Read each item carefully
2. **Mark as pass (✓) or fail (✗)** - Some items reference Step 1 automated results, most require manual judgment
3. **Apply contextual analysis** - Understand WHY something was flagged before marking as fail
4. **Calculate percentage** - (items passed / total items) × 100
5. **Assign score** - Use rubric below based on percentage
6. **Document issues** - Note specific problems for any failed items

**Scoring Rubric (applies to all 6 categories):**

- **5 (Excellent)**: 90-100% of checks pass
- **4 (Good)**: 75-89% of checks pass
- **3 (Acceptable)**: 60-74% of checks pass
- **2 (Needs Work)**: 40-59% of checks pass
- **1 (Poor)**: <40% of checks pass

**Target**: All categories score ≥4/5 for approval.

### Step 3: Test the Command

**IMPORTANT**: Commands may have side effects. Test with extreme caution.

**Safety assessment:**
1. Review `allowed-tools` frontmatter
2. Check for destructive operations (git commit, file writes, API calls)
3. Identify potential risks

**Safe testing patterns:**
- Commands with `Read, Grep, Glob` only → Safe to test
- Commands with `Edit, Write` → Test in isolated directory
- Commands with `Bash(git:*)` → Test in isolated git repo
- Commands with external APIs → Do NOT test without user approval

**Testing workflow (when safe):**
```bash
# Structure check
cat /path/to/command.md | head -30

# Invoke command (only if safe!)
/command-name [test-args]

# Observe:
# - Loads correctly?
# - Preflight checks work?
# - Context gathering succeeds?
# - Task execution follows instructions?
# - Success criteria verifiable?
```

**When NOT to functionally test:**
- Destructive operations (delete, force push, production changes)
- External API calls
- Commands requiring specific environment state
- Uncertain about safety

→ Structure validation only in these cases

### Step 4: Apply Recommendation Logic

Based on scores from Step 2:

- **APPROVE** - All scores ≥4, ready for deployment
- **NEEDS_REVISION** - Any score <4, requires improvements
- **CONSIDER_DIFFERENT_TYPE** - Artifact Type score ≤2, might be better as skill/subagent

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

### Category 1: Frontmatter & Tool Restrictions

The YAML frontmatter determines command behavior and safety boundaries. Quality here directly impacts security and usability.

#### Checklist Items

**Required Fields** (from automated validation)
- [ ] `allowed-tools` field present
- [ ] `argument-hint` field present
- [ ] `description` field present
- [ ] `model` field present
- [ ] YAML syntax valid

**allowed-tools (Security Critical)**
- [ ] Tools are explicitly listed (no wildcards at top level)
- [ ] Bash commands are specific (NOT bare `Bash`)
- [ ] Pattern: `Bash(command:*)` for specific commands
- [ ] Only necessary tools included (minimal surface area)
- [ ] Destructive operations justified in description
- [ ] Read-only tools preferred when possible

**argument-hint (Usability)**
- [ ] Arguments clearly indicated
- [ ] Uses `<required>` for required args
- [ ] Uses `[optional]` for optional args
- [ ] Multiple modes separated with `|`
- [ ] Brief and clear (≤50 chars)

**description (Discovery)**
- [ ] Under 100 characters (~10 words target)
- [ ] Clear and concise
- [ ] Action-oriented
- [ ] Third person perspective
- [ ] No implementation details

**model (Performance)**
- [ ] Appropriate for task complexity
- [ ] `haiku` for simple tasks (<5 steps, fast execution)
- [ ] `sonnet` for most tasks (default)

**Total checks**: 20

**Score**: _____ /5 (based on % passed)

**Issues identified**:

---

### Category 2: Preflight Checks

Preflight checks validate that the command can execute successfully. Missing checks lead to runtime failures.

#### Checklist Items

**Check Coverage**
- [ ] File existence checks where needed
- [ ] Git repository validation if using git
- [ ] Dependency checks for required tools
- [ ] State validation checks where applicable
- [ ] Argument validation if command takes args

**Check Implementation**
- [ ] Uses !`command` syntax correctly
- [ ] Commands are safe (no side effects)
- [ ] Error cases handled (command || echo "fallback")
- [ ] Output is meaningful
- [ ] Checks fail fast (stop if prerequisites missing)

**Edge Cases**
- [ ] Handles missing files gracefully
- [ ] Handles non-git repositories
- [ ] Handles missing dependencies
- [ ] Clear error messages when checks fail

**Bash Command Metrics** (from automated validation)
- [ ] Has at least some bash commands (>0)
- [ ] Bash commands are validation-focused
- [ ] Not using bash for complex logic (that should be in scripts)

**Total checks**: 17

**Score**: _____ /5 (based on % passed)

**Issues identified**:

---

### Category 3: Context Gathering

Context gathering provides information Claude needs to execute effectively. Insufficient context leads to poor decisions.

#### Checklist Items

**Context Adequacy**
- [ ] Sufficient context for task
- [ ] No unnecessary context (efficient)
- [ ] Git context when modifying code
- [ ] Project context when analyzing structure
- [ ] File contents included where needed (@path/to/file)

**Context Implementation**
- [ ] Uses !`command` for dynamic context
- [ ] Uses @path/to/file for static file includes
- [ ] Uses @skill-name for skill references
- [ ] Context commands are safe (read-only)
- [ ] Context is gathered early (before task execution)

**Context Organization**
- [ ] Logically grouped
- [ ] Clear labels for each context item
- [ ] No duplication
- [ ] Progressive disclosure (load what's needed when needed)

**File & Skill References** (from automated validation)
- [ ] @file references exist
- [ ] @skill references are valid skill names
- [ ] Skills referenced are appropriate for task

**Total checks**: 16

**Score**: _____ /5 (based on % passed)

**Issues identified**:

---

### Category 4: Task Instructions & Prompt Quality

Task instructions are the core prompt directing Claude's behavior. Quality here determines execution success.

#### Checklist Items

**Instruction Clarity**
- [ ] Clear, numbered steps
- [ ] Each step has concrete action
- [ ] Steps are sequential and logical
- [ ] No ambiguous language
- [ ] Explicit about what to do (not what not to do)

**Skill & Subagent Integration**
- [ ] Uses Skill(command="name") for explicit skill execution
- [ ] References skills appropriately
- [ ] Delegates to subagents where appropriate
- [ ] Specifies subagent thoroughness levels
- [ ] Clear handoff between steps

**Tool Usage Patterns**
- [ ] Uses correct tool invocation syntax
- [ ] Tool calls have all required parameters
- [ ] Tool sequence is logical
- [ ] Verification steps after tool calls
- [ ] Error handling specified

**Prompt Engineering** (crafting-agentic-prompts principles)
- [ ] Uses directive language (not suggestive)
- [ ] Positive framing (what TO do, not what NOT to do)
- [ ] Provides context for WHY behaviors matter
- [ ] Examples align with desired outcomes
- [ ] Assumes Claude's intelligence (no over-explanation)

**Writing Style**
- [ ] Imperative form throughout
- [ ] No first/second person ("you", "I", "we")
- [ ] Concise and direct
- [ ] No time-sensitive information
- [ ] No platform-specific paths

**Integration Metrics** (from automated validation)
- [ ] Skill() invocations are appropriate
- [ ] Task() invocations specify correct subagent types
- [ ] Tool references match allowed-tools

**Total checks**: 26

**Score**: _____ /5 (based on % passed)

**Issues identified**:

---

### Category 5: Success Criteria

Success criteria define when the command has completed correctly. Missing criteria make verification impossible.

#### Checklist Items

**Criteria Clarity**
- [ ] Clear completion conditions
- [ ] Measurable outcomes
- [ ] Verifiable by user or automation
- [ ] Specific (not vague)
- [ ] Complete (covers all task aspects)

**Verification Methods**
- [ ] Commands to verify success
- [ ] Expected output described
- [ ] Files to check listed
- [ ] State changes specified
- [ ] Error conditions documented

**User Communication**
- [ ] Clear success message format
- [ ] Failure scenarios documented
- [ ] Next steps indicated
- [ ] Output locations specified

**Total checks**: 14

**Score**: _____ /5 (based on % passed)

**Issues identified**:

---

### Category 6: Command Metrics & Artifact Type

Validate that the command is the appropriate artifact type and has good structural metrics.

#### Checklist Items

**Line Count & Complexity**
- [ ] ≤200 lines (from automated validation)
- [ ] Single-file appropriate
- [ ] Complexity warrants command (not too simple)
- [ ] Not complex enough to be skill (no multiple resource files needed)

**Command Metrics** (from automated validation)
- [ ] Appropriate bash command count
- [ ] File references used where needed
- [ ] Skill references appropriate
- [ ] Tool invocations match task complexity

**Artifact Type Validation**
- [ ] Command is the right artifact type (not skill/subagent)
- [ ] Explicit invocation appropriate (not proactive)
- [ ] Single workflow (not multiple independent workflows)
- [ ] No need for bundled resources (scripts, references, templates)
- [ ] Fits command pattern (quick, repeatable, manual trigger)

**Alternative Artifact Types** (flag if true)
- [ ] Would NOT be better as skill (>200 lines, needs resources)
- [ ] Would NOT be better as subagent (autonomous sub-tasks)
- [ ] Scope is appropriate (not too broad or narrow)

**Total checks**: 14

**Score**: _____ /5 (based on % passed)

**Issues identified**:

---

## Additional Validation Checks

These are yes/no gates that must pass regardless of category scores.

### Security Considerations
- [ ] No hardcoded credentials
- [ ] No destructive operations without clear warnings
- [ ] Tool restrictions appropriate for task
- [ ] Input validation where needed
- [ ] Safe file handling practices

### Artifact Type Validation
- [ ] Command is appropriate artifact type
- [ ] Not better suited as skill (complexity, resources)
- [ ] Not better suited as subagent (autonomous, separate domain)
- [ ] Manual invocation makes sense (not proactive)

### Final Verification
- [ ] All @file references are valid
- [ ] All @skill references are valid skills
- [ ] All tool invocations match allowed-tools
- [ ] YAML syntax valid
- [ ] No critical typos in instructions

---

## Score Summary

Complete after scoring all categories:

| Category | Score | Status |
|----------|-------|--------|
| 1. Frontmatter & Tool Restrictions | ___/5 | ___ |
| 2. Preflight Checks | ___/5 | ___ |
| 3. Context Gathering | ___/5 | ___ |
| 4. Task Instructions & Prompt Quality | ___/5 | ___ |
| 5. Success Criteria | ___/5 | ___ |
| 6. Command Metrics & Artifact Type | ___/5 | ___ |
| **Average** | **___/5** | ___ |

**Status codes**: ✓ Pass (≥4) | ⚠ Review (3) | ✗ Fail (<3)

---

## Final Recommendation

Based on scores and validation checks:

**[ ] APPROVE** - All scores ≥4, all validation checks pass
- Command is ready for deployment
- Test carefully if command has side effects
- Document any safety considerations for users

**[ ] NEEDS_REVISION** - Any score <4 or validation checks fail
- Address all issues documented in category reviews
- Re-run quality review after improvements
- Focus on categories with scores <4

**[ ] CONSIDER_DIFFERENT_TYPE** - Artifact Type validation concerns
- Consider if command would be better as skill or subagent
- Skills: Complex workflow (>200 lines), needs bundled resources
- Subagents: Autonomous sub-tasks, separate domain, proactive triggers

---

## Common Anti-Patterns

Watch for these frequent mistakes:

**Frontmatter Issues**
- ✗ Bare `Bash` without restrictions (security risk)
- ✗ Description too long or vague
- ✗ Unnecessary tools in allowed-tools
- ✗ Wrong model for task (opus when sonnet suffices)

**Preflight Check Issues**
- ✗ No preflight checks at all
- ✗ Checks have side effects
- ✗ Missing critical prerequisite checks
- ✗ Poor error messages when checks fail

**Context Gathering Issues**
- ✗ Too much context (inefficient)
- ✗ Too little context (poor decisions)
- ✗ Context gathered too late
- ✗ Unsafe context commands

**Task Instruction Issues**
- ✗ Vague instructions ("do the thing")
- ✗ Second person language ("you should...")
- ✗ No skill/subagent delegation
- ✗ Missing verification steps
- ✗ Ambiguous tool invocations

**Success Criteria Issues**
- ✗ No success criteria
- ✗ Unverifiable criteria
- ✗ Vague completion conditions
- ✗ Missing failure scenarios

**Artifact Type Issues**
- ✗ Command is >200 lines (should be skill)
- ✗ Command needs multiple resource files (should be skill)
- ✗ Command is proactive (should be subagent)
- ✗ Command does autonomous sub-tasks (should be subagent)

---

## Quality Standards Summary

A production-ready command must be:

1. **Safe** - Restrictive tool permissions, validated prerequisites
2. **Clear** - Explicit instructions, well-organized structure
3. **Concise** - Single-file, ≤200 lines, focused workflow
4. **Complete** - Preflight checks, context, instructions, success criteria
5. **Correct** - Valid references, proper tool invocations, tested
6. **Contextual** - Sufficient context for Claude to succeed
7. **Appropriate** - Right artifact type for the task

**Minimum standard**: All categories score 4+/5, all validation checks pass.

---

## Using the Validation Script

### Quick Iteration Mode

During development, use `--minimal` for fast feedback:

```bash
python3 scripts/validate_command.py /path/to/command.md --minimal
```

**Output shows:**
- One-line score with percentage
- Key metrics (lines, bash cmds, @references, Skill/Task invocations)
- Only errors and warnings (no passing checks)
- Actionable recommendations

**Example minimal output:**
```
quick-commit: 18/20 (90%) | 1 errors, 1 warnings | ✗ FAIL
Metrics: 156 lines | 5 bash cmds | 2 @files | 3 @skills | 1 Skill() | 0 Task()

Errors:
  ✗ allowed-tools restrictive: Replace 'Bash' with specific commands

Warnings:
  ⚠ line count (warning)

Recommendations:
  • Add preflight checks with !`command` syntax
```

### Full Validation Mode

For final review before deployment:

```bash
python3 scripts/validate_command.py /path/to/command.md
```

Shows:
- Detailed category-by-category checks
- All passing/failing checks with context
- Full error descriptions with fixes
- Complete metrics summary
- Comprehensive recommendations

---

## Automated Checks Reference

The validation script (`scripts/validate_command.py`) performs 17 automated checks:

**Category 1: File Structure** (2 checks)
1. Command file exists
2. Command file readable

**Category 2: Frontmatter Structure** (2 checks)
3. Valid YAML frontmatter
4. Required fields present

**Category 3: Frontmatter Content** (4 checks)
5. Description length ≤100 chars
6. Model value valid (sonnet/haiku/opus)
7. allowed-tools is restrictive
8. Description uses third person

**Category 4: Required Sections** (4 checks)
9. Preflight Checks section present
10. Context section present
11. Task Instructions section present
12. Success Criteria section present

**Category 5: Command Metrics** (2 checks)
13. Line count ≤200 (warning if exceeded)
14. Has bash commands (warning if 0)

*Note: File refs, skill refs, Skill() calls, and Task() calls are reported as informational metrics, not validation checks.*

**Category 6: Writing Style** (3 checks)
15. Uses imperative form (no you/I/we)
16. No time-sensitive content (warning only)
17. No Windows-style paths

All checks must pass (score 17/17) for approval, except warnings which are advisory.
