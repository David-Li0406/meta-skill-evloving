---
name: Skill Builder
description: Transforms AI pain points into working skills. Use when creating new skills from identified patterns.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Skill Builder Skill

## Purpose

Transform AI pain points into working skills. This skill is the second stage of the self-improvement loop, converting identified error patterns into automated solutions.

## Auto-Activation Triggers

This skill activates when:
- AI Error Learner escalates a pain point (3+ occurrences)
- User requests "create a skill for [problem]"
- High-priority pain point needs resolution
- Manual invocation with pain point ID

## CRITICAL: Quality Standards

**Every skill must be complete, testable, and maintainable.**

### Required Skill Components

```
YAML Frontmatter    → name, description, allowed-tools
Purpose Section     → Clear explanation of what and why
Triggers Section    → Specific, observable conditions
Workflow Section    → Complete, sequential steps
Edge Cases Section  → Known exceptions and handling
Error Handling      → Recovery from failures
Metadata Section    → Version, date, category
```

## Skill Creation Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    SKILL BUILDER FLOW                    │
│                                                          │
│  Pain Point     Investigation     Design      Create     │
│  ┌────────┐     ┌──────────┐    ┌───────┐   ┌───────┐  │
│  │ Select │────▶│  Deep    │───▶│Trigger│──▶│ Write │  │
│  │  Pain  │     │  Dive    │    │ & Flow│   │ Skill │  │
│  │  Point │     │          │    │       │   │  File │  │
│  └────────┘     └──────────┘    └───────┘   └───────┘  │
│                                                    │     │
│                                              ┌─────▼───┐ │
│                                              │ Verify  │ │
│                                              │   &     │ │
│                                              │ Update  │ │
│                                              └─────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Core Workflow

### Step 1: Select Pain Point

Choose pain point to address:

**By ID:**
```bash
grep -A 20 "AI-PAIN-0012" .claude/pain-points/ai-pain-points.md
```

**By highest occurrence:**
```bash
python3 -c "
import json
data = json.load(open('.claude/pain-points/ai-error-history.json'))
sorted_errors = sorted(data.get('errors', {}).items(), key=lambda x: x[1].get('count', 0), reverse=True)
for fp, info in sorted_errors[:5]:
    print(f\"{info.get('count', 0):3d} | {fp} | {info.get('pain_point_id', 'N/A')}\")
"
```

### Step 2: Deep Investigation

Thoroughly understand the problem:

1. **Reproduce the error context**
   - What actions trigger it?
   - What environment conditions exist?
   - What files/tools are involved?

2. **Analyze root cause**
   - Is it a knowledge gap? (needs documentation)
   - Is it a process gap? (needs workflow)
   - Is it a tool gap? (needs automation)

3. **Review existing solutions**
   - Do similar skills exist?
   - Are there related patterns in memory?
   - What approaches have been tried?

### Step 3: Design Skill Triggers

Define specific, observable triggers:

**Good Triggers:**
- "When user runs `pytest` and tests fail with import errors"
- "When creating files in `/scripts/` directory"
- "When git push is rejected due to hooks"

**Bad Triggers:**
- "When something goes wrong" (too vague)
- "When user is frustrated" (not observable)
- "When appropriate" (undefined)

### Step 4: Design Workflow

Create complete, sequential steps:

1. **Each step should be atomic** - one clear action
2. **Include decision points** - what to check before proceeding
3. **Show concrete commands** - exact syntax to use
4. **Handle branches** - what if step fails?

### Step 5: Create Skill File

Write the complete skill using this template:

```markdown
---
name: [Skill Name]
description: [One-line description]. Use when [trigger condition].
allowed-tools: [Required tools]
---

# [Skill Name] Skill

## Purpose
[Clear explanation of what this skill does and why it exists]

## Auto-Activation Triggers
This skill activates when:
- [Observable trigger 1]
- [Observable trigger 2]
- [User phrase triggers]

## CRITICAL: [Key Protocol]
[Most important behavioral requirement]

## Core Workflow

### Step 1: [First Step]
[Detailed instructions with commands]

### Step 2: [Second Step]
[Detailed instructions with commands]

[Continue for all steps...]

## Edge Cases

### [Edge Case Name]
**Condition**: [When this occurs]
**Handling**: [What to do]

## Error Handling

### If [Failure Mode]
1. [Recovery step 1]
2. [Recovery step 2]
3. [Fallback behavior]

## Skill Metadata

**Version:** 1.0.0
**Created:** YYYY-MM-DD
**Category:** [Category]
**Origin:** AI-PAIN-NNNN
```

### Step 6: Update Documentation

After creating skill:

1. **Update CLAUDE.md** (if skill is frequently used)
   ```markdown
   **[SKILL-NNNNN]** [Brief description]
   > TRIGGER: [When to use]
   ```

2. **Update skill metrics**
   ```json
   {
     "skills": {
       "new-skill-name": {
         "invocations": 0,
         "successes": 0,
         "failures": 0,
         "origin": "AI-PAIN-NNNN",
         "created": "YYYY-MM-DD"
       }
     }
   }
   ```

3. **Update error history**
   - Mark pain point as resolved
   - Link to new skill

4. **Log in episodic memory**
   ```markdown
   ### New Skill Created
   - Skill: [skill-name]
   - Origin: AI-PAIN-NNNN
   - Purpose: [brief description]
   ```

### Step 7: Verify Integration

Confirm skill is properly integrated:

```bash
# Check skill file exists and has valid frontmatter
head -10 .claude/skills/new-skill-name/SKILL.md

# Verify YAML is valid
python3 -c "import yaml; yaml.safe_load(open('.claude/skills/new-skill-name/SKILL.md').read().split('---')[1])"

# Check metrics file updated
cat .claude/skills/skill-metrics.json | python3 -m json.tool
```

## Edge Cases

### Pain Point Has No Clear Solution
**Condition**: Investigation doesn't reveal automated solution
**Handling**: Create documentation pattern instead of skill, mark pain point as "documented"

### Similar Skill Already Exists
**Condition**: Existing skill covers 80%+ of use case
**Handling**: Extend existing skill rather than create new one

### Solution Requires External Changes
**Condition**: Fix requires config/environment changes, not automation
**Handling**: Document in quick-reference, create setup skill if applicable

### Skill Would Be Too Complex
**Condition**: Solution requires >400 lines or multiple sub-skills
**Handling**: Break into smaller skills with clear dependencies

## Integration Points

### With AI Error Learner
- Receives prioritized pain points
- Gets context from error history
- Reports completion status

### With Skill Improver
- New skills start at version 1.0.0
- Skill improver monitors effectiveness
- Triggers improvements if skill fails

### With Memory System
- Logs skill creation in episodic memory
- May discover related patterns in procedural memory
- Updates quick-reference for common skills

## Output Examples

### Example 1: Creating Permission Fix Skill

**Trigger**: AI-PAIN-0012 escalated (script permission errors)
**Response**:
```markdown
## Skill Creation: Permission Fixer

### Pain Point Analysis
**ID**: AI-PAIN-0012
**Fingerprint**: `BASH-PERMISSION_DENIED-scripts/`
**Occurrences**: 5

### Root Cause
Scripts created by Write tool have 644 permissions by default.
Execution requires 755.

### Skill Design

**Triggers:**
- When creating files in `/scripts/` directory
- When bash command fails with "Permission denied"
- User says "make it executable"

**Workflow:**
1. Detect script creation context
2. Check current permissions
3. Apply chmod +x if needed
4. Verify execution works

### Created: `.claude/skills/permission-fixer/SKILL.md`

[Full skill content...]

### Updates Made
- Added to skill-metrics.json
- Marked AI-PAIN-0012 as resolved
- Logged in episodic memory
```

## Error Handling

### If Skill Write Fails
1. Save content to temp file
2. Report failure with content
3. Suggest manual creation

### If YAML Frontmatter Invalid
1. Validate before writing
2. Use template defaults if needed
3. Log validation warnings

### If Pain Point Not Found
1. Search for similar entries
2. Offer to create new pain point
3. Proceed with available context

## Skill Metadata

**Version:** 1.0.0
**Created:** 2026-01-16
**Category:** Self-Improvement
**Integration:** AI Error Learner, Skill Improver, Memory System
**Maintenance:** On-demand (triggered by pain point escalation)
