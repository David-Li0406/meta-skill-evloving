# Skill Resolution Guide

## How Claude Finds Skills

Claude Code loads skills from two locations in this order:

### 1. Global Skills (~/.claude/skills/)
- **Source**: Synced from marketplace or user-installed
- **Availability**: Available in ALL projects
- **Priority**: Lower (can be overridden)
- **Use case**: General-purpose skills used across projects

### 2. Project-Level Skills (.claude/skills/)
- **Source**: Checked into project repository
- **Availability**: Only in this project
- **Priority**: Higher (overrides global if same name)
- **Use case**: Project-specific customizations

## Resolution Algorithm

```
1. Claude checks for skill in .claude/skills/ (project)
   └─ IF FOUND: Use project version

2. Claude checks for skill in ~/.claude/skills/ (global)
   └─ IF FOUND: Use global version

3. IF NOT FOUND in either:
   └─ Skill not available
```

## Common Scenarios

### Scenario 1: Using Global Skills Only
```
~/.claude/skills/
  └── julien-infra-hostinger-docker/    ← Used by all projects

project-a/
  └── (no .claude/skills/)              ← Uses global version

project-b/
  └── (no .claude/skills/)              ← Uses global version
```

**Result**: All projects use the same version from global.

### Scenario 2: Project Override
```
~/.claude/skills/
  └── julien-infra-hostinger-docker/    ← Global version

project-a/.claude/skills/
  └── julien-infra-hostinger-docker/    ← Project override

project-b/
  └── (no .claude/skills/)              ← Uses global
```

**Result**:
- project-a uses its own version
- project-b uses global version

### Scenario 3: Missing Skill
```
~/.claude/skills/
  └── (skill not synced)

project/.claude/skills/
  └── (skill not present)
```

**Result**: Skill not available, Claude will indicate it's missing.

## Troubleshooting Missing Skills

### Problem: Skill in marketplace but not available

**Step 1**: Check if skill is synced globally
```bash
ls -1 ~/.claude/skills/ | grep skill-name
```

**Step 2**: If not synced, run sync
```bash
/sync-personal-skills
```

**Step 3**: Verify sync completed
```bash
./check-loaded-skills.sh
```

### Problem: Skill works in one project but not another

**Cause**: Project-level override in one project

**Solution**:
1. Check project-level skills: `ls -1 .claude/skills/`
2. Remove project override if unintended
3. Or sync new version to global if intentional

### Problem: Outdated skill version

**Cause**: Old version in global, new version in marketplace

**Solution**:
1. Update marketplace repo
2. Re-sync: `/sync-personal-skills`
3. Verify: `/check-loaded-skills`

## Best Practices

### ✅ Do
- Keep commonly-used skills in global (~/.claude/skills/)
- Use project-level only for project-specific customizations
- Sync marketplace regularly to get updates
- Check loaded skills when debugging availability

### ❌ Don't
- Don't duplicate skills in every project
- Don't mix project-level and global unless necessary
- Don't forget to sync after adding marketplace skills
- Don't override globals without good reason

## Skill Sync Workflow

```
Marketplace/skills/
  └── julien-workflow-check-loaded-skills/
        ↓
      [/sync-personal-skills]
        ↓
~/.claude/skills/
  └── julien-workflow-check-loaded-skills/
        ↓
      [Auto-loaded by Claude]
        ↓
    Available in ALL projects
```

## Related Commands

- `/sync-personal-skills` - Sync marketplace to global
- `/check-loaded-skills` - Check what's loaded
- `ls -1 ~/.claude/skills/` - List global skills manually
- `ls -1 .claude/skills/` - List project skills manually
