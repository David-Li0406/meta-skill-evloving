# Workflow Examples

## Table of Contents

- [Creating a Skill](#creating-a-skill)
- [Creating a User-Triggered Skill (Legacy Command Pattern)](#creating-a-user-triggered-skill-legacy-command-pattern)
- [Creating a Hook](#creating-a-hook)
- [Auditing a Component](#auditing-a-component)
- [Full Workflow Example](#full-workflow-example)
- [User-Triggered Skill Example](#user-triggered-skill-example)

## Creating a Skill

```bash
/skills-architect create skill api-review
```

**Dynamic Context**:
Project structure: !`find .claude/skills -name "*.md" | head -10`
Current skills: !`ls -la .claude/skills/ 2>/dev/null || echo "No skills directory"`

**Workflow**:
1. ✅ Load skills-knowledge
2. ✅ Gather requirements (purpose, triggers, examples)
3. ✅ Create directory structure
4. ✅ Generate SKILL.md with progressive disclosure
5. ✅ Add mandatory URL sections
6. ✅ Validate compliance
7. ✅ Test auto-discovery

## Creating a User-Triggered Skill (Legacy Command Pattern)

```bash
/skills-architect create skill deploy-app --disable-model-invocation
```

**Dynamic Context**:
Working directory: !`pwd`
Git branch: !`git branch --show-current 2>/dev/null || echo "Not a git repo"`
Recent commits: !`git log -3 --oneline 2>/dev/null || echo "No git history"`

**Workflow**:
1. ✅ Load skills-knowledge
2. ✅ Gather requirements (deployment target, validation)
3. ✅ Create skill with disable-model-invocation: true
4. ✅ Use skills for all workflows (no commands)
5. ✅ Add progressive disclosure
6. ✅ Validate workflow
7. ✅ Test invocation

## Creating a Hook

```bash
/hooks-architect create hook validation-hook
```

**Dynamic Context**:
Current hooks: !`ls -la hooks/ 2>/dev/null || echo "No hooks directory"`
Plugin manifest: !`cat .claude-plugin/plugin.json 2>/dev/null || echo "No plugin manifest"`

**Workflow**:
1. ✅ Load hooks-knowledge
2. ✅ Identify event type (PreToolUse, Stop, etc.)
3. ✅ Determine validation requirements
4. ✅ Create hook configuration
5. ✅ Implement validation logic
6. ✅ Add security checks
7. ✅ Test event triggering

## Auditing a Component

```bash
/toolkit-architect audit skill my-skill
```

**Dynamic Context**:
Skill files: !`find .claude/skills/my-skill -type f 2>/dev/null || echo "Skill not found"`
File size: !`du -sh .claude/skills/my-skill 2>/dev/null || echo "N/A"`
Last modified: !`stat -f "%Sm" -t "%Y-%m-%d %H:%M" .claude/skills/my-skill 2>/dev/null || echo "N/A"`

**Workflow**:
1. ✅ Load relevant knowledge base
2. ✅ Analyze structure
3. ✅ Check progressive disclosure
4. ✅ Validate URL sections
5. ✅ Review trigger quality
6. ✅ Generate audit report
7. ✅ Provide improvement recommendations

## Full Workflow Example

```bash
# 1. Create new skill
/skills-architect create skill api-conventions

# 2. Review created structure
!`find .claude/skills/api-conventions -type f`

# 3. Audit quality
/toolkit-architect audit skill api-conventions

# 4. Test auto-discovery
# Invoke with natural language about API conventions

# 5. Refine if needed
/toolkit-architect refine skill api-conventions
```

## User-Triggered Skill Example

```bash
# 1. Create deploy skill
/skills-architect create skill deploy-app --disable-model-invocation

# 2. Check structure
!`find .claude/skills/deploy-app -type f`

# 3. Test invocation
/deploy-app staging

# 4. Audit compliance
/toolkit-architect audit skill deploy-app
```
