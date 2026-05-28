# Meta Skill Template

Template for creating meta skills that operate on the skill system itself.

## When to Use This Template

Use this template when creating a skill that:
- Creates or modifies skills
- Analyzes the skill system
- Automates skill maintenance
- Performs system-level operations on skills

**Examples:** skill-creator, skill-updater, skill-analyzer

## Template Structure

```markdown
---
name: meta-skill-name
description: |
  Operate on skill system for [purpose]. Use when [meta-operation 1], [meta-operation 2], or [meta-operation 3]. Invoke when seeing "[system issue pattern]", "[skill problem indicator]", "[maintenance need]", or discussing [skill system operations], [skill enhancement], or [system maintenance]. Handles [system-level responsibility] following V3 patterns. Keywords: [skill-operation], [system-verb], [meta-tool], [skill-system], [maintenance-type]
tags: [meta, [operation-type], [system-area]]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(find:*)
  - Bash(grep:*)
  - Bash(git:*)
---

# Meta Skill Name

Skill system operation: [What this changes] (<duration>).

## Purpose

[What this meta-skill does to the skill system and why]

**Impact:** [What changes in the skill system]

**Philosophy:** [Meta-operation principle]

## When to Use This Skill

**Trigger phrases:**
- "[meta-operation phrase 1]"
- "[meta-operation phrase 2]"
- "[meta-operation phrase 3]"

**Use when:**
- [Meta-operation pattern 1]
- [Meta-operation pattern 2]
- [Meta-operation pattern 3]

## Workflow

### 1. Analyze System State

[Understand current skill system state]

**Questions to answer:**
- What skills currently exist?
- What patterns are in use?
- What needs to change?
- What's the impact?

**Analysis pattern:**
```bash
# Scan skill system
find agent-skills -name "SKILL.md"

# Analyze each skill
grep -r "pattern" agent-skills/
```

### 2. Design Change

[Plan modifications to skill system]

**A. Define Scope**
- [What will change]
- [What won't change]
- [Safety boundaries]

**B. Plan Artifacts**
```[language]
# What files to create/modify
# What structure to use
# What patterns to apply
```

**C. Identify Dependencies**
- [Dependency 1]
- [Dependency 2]

### 3. Generate Artifacts

[Create or modify skill artifacts]

**A. [Artifact type 1]**
```[language]
# Generation code
```

**B. [Artifact type 2]**
```[language]
# Generation code
```

### 4. Integrate with System

[Add to skill system, update metadata]

**A. Update skill-rules.json**
```[language]
# Add auto-activation rules
```

**B. Update CLAUDE.md**
```[language]
# Document new skill
```

**C. Test Integration**
```[language]
# Verify system still works
```

### 5. Verify System Integrity

[Ensure skill system remains functional]

**Checks:**
- [ ] All existing skills still work
- [ ] New artifacts follow V3 patterns
- [ ] Auto-activation works
- [ ] Documentation updated
- [ ] No broken references

**Validation:**
```[language]
# System integrity checks
```

## Safety Guardrails

### Before Meta-Operations

**Check:**
- [ ] Understand full impact
- [ ] Have rollback plan
- [ ] Test in isolated context
- [ ] Get user confirmation if significant

### During Meta-Operations

**Ensure:**
- [ ] Don't break existing skills
- [ ] Follow V3 patterns
- [ ] Maintain progressive disclosure
- [ ] Preserve integration points

### After Meta-Operations

**Verify:**
- [ ] System integrity maintained
- [ ] All skills loadable
- [ ] Auto-activation works
- [ ] Documentation complete

## System Knowledge

### Skill System Structure

```
.claude/skills/
├── skill-name/
│   ├── SKILL.md (<500 lines)
│   └── resources/
│       ├── examples/
│       ├── patterns/
│       └── reference/
├── skill-rules.json
└── ...

CLAUDE.md (references skills)
```

### Required Files

**SKILL.md frontmatter:**
```yaml
---
name: skill-name
description: One-line with MUST BE USED. Use when [patterns].
allowed-tools:
  - Tool patterns
---
```

**skill-rules.json entry:**
```json
{
  "skill-name": {
    "triggers": ["phrase1", "phrase2"],
    "intents": ["Intent pattern"],
    "examples": ["User: 'example'"]
  }
}
```

**CLAUDE.md sections:**
```markdown
### Natural Language → Skills
- **"trigger"** → skill-name skill
  - What it does
  - **Total: <time>**
```

### V3 Patterns to Enforce

1. **Progressive disclosure:** Main SKILL.md <500 lines
2. **Auto-activation:** Entry in skill-rules.json
3. **Natural language:** Trigger phrases documented
4. **Fast execution:** Time budgets met
5. **Integration:** Beads/Serena/Git patterns

## Integration Points

### With File System

[How meta-skill modifies files]

**Pattern:**
```[language]
# Read existing files
# Generate new content
# Write/Edit files
# Verify structure
```

### With Git

[How meta-skill tracks changes]

**Pattern:**
```bash
# Stage skill files
git add .claude/skills/skill-name/
git add .claude/skills/skill-rules.json
git add CLAUDE.md

# Commit with Feature-Key
git commit -m "feat: Add skill-name skill

Feature-Key: [CURRENT_FEATURE]
Agent: claude-code
Role: skill-creator"
```

### With Skill System

[How meta-skill integrates new artifacts]

**Pattern:**
```[language]
# Update skill registry (skill-rules.json)
# Update documentation (CLAUDE.md)
# Test auto-activation
# Verify existing skills unaffected
```

## Decision Framework

### When to Create vs Modify

**Create new skill when:**
- [ ] Automating new workflow
- [ ] Adding new domain expertise
- [ ] New meta-operation

**Modify existing skill when:**
- [ ] Fixing bug in skill
- [ ] Updating to new pattern
- [ ] Adding missing section

**Use meta-skill when:**
- [ ] System-level change (affects multiple skills)
- [ ] Pattern enforcement across skills
- [ ] Automated skill generation

### Scope Boundaries

**In scope:**
- Creating skill files
- Updating skill metadata
- Enforcing patterns
- Documentation generation

**Out of scope:**
- Modifying skill behavior directly (user does this)
- Changing V3 philosophy (that's a design decision)
- Breaking existing skills
- Ignoring user preferences

## Best Practices

### Do

✅ Analyze full impact before changes
✅ Maintain system integrity
✅ Follow V3 patterns strictly
✅ Test integration thoroughly
✅ Document all changes
✅ Get user confirmation for significant changes
✅ Provide rollback information
✅ Verify existing skills unaffected

### Don't

❌ Break existing skills
❌ Skip safety checks
❌ Ignore V3 patterns
❌ Make assumptions about impact
❌ Forget to update documentation
❌ Skip integration testing
❌ Leave system in inconsistent state

## What This Skill Does

✅ [Meta-operation 1]
✅ [Meta-operation 2]
✅ [Meta-operation 3]
✅ [Meta-operation 4]

## What This Skill DOESN'T Do

❌ [Non-meta-operation 1]
❌ [Non-meta-operation 2]
❌ [Non-meta-operation 3]

## Examples

### Example 1: [Simple Meta-Operation]

```
User: "[meta-operation request]"

AI analyzes:
- [Current state]
- [Desired state]
- [Impact assessment]

AI executes:
1. [Meta-operation step 1]
2. [Meta-operation step 2]
3. [Verify system integrity]

Result:
✅ [Skill system change]
✅ [All existing skills still work]
✅ [Documentation updated]
```

### Example 2: [Complex Meta-Operation]

```
User: "[complex meta-operation request]"

AI analyzes:
- [Multiple skills affected]
- [Pattern changes needed]
- [Risk assessment]

AI asks: "This will affect [N] skills. Proceed?"
User: "Yes"

AI executes:
1. [Backup current state]
2. [Apply changes]
3. [Test each affected skill]
4. [Update documentation]

Result:
✅ [System-wide change applied]
✅ [All skills tested and working]
⚠️ [Rollback instructions provided]
```

### Example 3: [Safety Guardrail Triggered]

```
User: "[risky meta-operation]"

AI analyzes:
- [High impact change]
- [Potential to break skills]
- [No clear rollback]

AI responds:
"⚠️ This operation is risky:
- Could break [N] skills
- No automatic rollback
- Requires manual testing

Recommend: [Alternative safer approach]

Proceed anyway? (yes/no)"

User: "no, use alternative"

AI: [Executes safer approach]
```

## Troubleshooting

### System Integrity Issues

**Symptom:** Existing skills stop working after meta-operation

**Diagnosis:**
```[language]
# Check each skill loads
# Check skill-rules.json valid
# Check CLAUDE.md references correct
```

**Fix:**
```[language]
# Rollback to previous state
# Re-apply changes carefully
# Test incrementally
```

### Pattern Violations

**Symptom:** Generated skill doesn't follow V3 patterns

**Diagnosis:**
```[language]
# Check main SKILL.md line count
# Check progressive disclosure structure
# Check trigger phrases
# Check integration points
```

**Fix:**
```[language]
# Regenerate with correct patterns
# Extract to resources/
# Add missing sections
```

## Related Skills

- **[other-meta-skill]**: [How they interact]
- **[workflow-skill]**: [What this meta-skill creates]
- **[specialist-skill]**: [What this meta-skill maintains]

## Resources

**Reference materials:**
- `resources/v3-philosophy.md` - Patterns to enforce
- `resources/skill-types.md` - Types to generate
- `resources/examples/` - Templates to use

**System files:**
- `.claude/skills/skill-rules.json` - Auto-activation registry
- `CLAUDE.md` - Skill documentation
- `.claude/skills/*/SKILL.md` - Existing skills

---

**Last Updated:** [Date]
**Skill Type:** Meta
**Impact:** Skill system itself
**Average Duration:** Variable
**Related Docs:**
- docs/DX_PARITY_V3/SKILL_ACTIVATION_SYSTEM_SPEC.md
- CLAUDE.md (V3 DX Workflow)
```

## Meta Skill Checklist

When creating a meta skill, ensure:

- [ ] System state analysis comprehensive
- [ ] Impact assessment documented
- [ ] Safety guardrails in place
- [ ] Rollback plan available
- [ ] System integrity checks implemented
- [ ] Pattern enforcement consistent
- [ ] All artifacts follow V3
- [ ] Documentation updated
- [ ] Integration tested
- [ ] User confirmation for significant changes
- [ ] Existing skills verified unaffected

## Common Meta Patterns

### Generate-Integrate-Verify Pattern

```
1. Analyze what to generate
2. Generate artifacts using templates
3. Integrate into skill system
4. Verify system integrity
5. Document changes
```

**Use for:** skill-creator, new artifact generators

### Scan-Transform-Apply Pattern

```
1. Scan existing skills
2. Identify transformation needed
3. Apply transformation to each
4. Test each after transformation
5. Update documentation
```

**Use for:** skill-updater, pattern enforcement

### Analyze-Report-Suggest Pattern

```
1. Analyze skill system state
2. Generate reports/metrics
3. Suggest improvements
4. (Optional) Apply improvements with user approval
```

**Use for:** skill-analyzer, system monitoring

## Safety Considerations

### High-Risk Operations

**Creating new skills:**
- Risk: Low (additive, doesn't break existing)
- Guardrail: Follow templates, test auto-activation

**Modifying existing skills:**
- Risk: Medium (could break workflows)
- Guardrail: Get user confirmation, provide rollback

**System-wide changes:**
- Risk: High (affects all skills)
- Guardrail: Test thoroughly, incremental rollout

### Rollback Strategy

**For file changes:**
```bash
# Before meta-operation
git stash push -m "Before meta-skill operation"

# After meta-operation (if needed)
git stash pop
```

**For skill-rules.json:**
```bash
# Keep backup
cp .claude/skills/skill-rules.json .claude/skills/skill-rules.json.backup

# Restore if needed
cp .claude/skills/skill-rules.json.backup .claude/skills/skill-rules.json
```

## Real Examples

### skill-creator (this skill!)

**Meta-operation:** Create new skills
**Pattern:** Generate-Integrate-Verify
**Impact:** Adds new skills to system
**Safety:** Low risk (additive only)
**Duration:** <5 minutes

### skill-updater (future)

**Meta-operation:** Update existing skills to new patterns
**Pattern:** Scan-Transform-Apply
**Impact:** Modifies existing skills
**Safety:** Medium risk (changes behavior)
**Duration:** Variable

### skill-analyzer (future)

**Meta-operation:** Analyze skill usage and effectiveness
**Pattern:** Analyze-Report-Suggest
**Impact:** Read-only, no changes
**Safety:** Low risk (reporting only)
**Duration:** <1 minute

---

**Related:**
- resources/skill-types.md - Skill type details
- resources/v3-philosophy.md - Patterns to enforce
- skill-creator/SKILL.md - Example meta-skill
