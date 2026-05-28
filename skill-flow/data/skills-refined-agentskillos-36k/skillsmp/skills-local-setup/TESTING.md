# Testing & Evaluation

Testing documentation for the Local Skills Setup skill.

## Testing Summary

| Model | Tested | Result |
|-------|--------|--------|
| Claude Haiku | Yes | Runs script correctly, follows workflow |
| Claude Sonnet | Yes | Reliable execution |
| Claude Opus | Yes | Comprehensive validation |

## Evaluation Scenarios

### Scenario 1: Full Setup (all)

**Setup**: New repo with `AGENTS.md`, no existing `.claude/`, `.agent/`, or `.opencode/` directories.

**Query:** "Set up skills for all tools" or "Run skills-local-setup all"

**Expected behaviors:**
- [ ] Creates `.claude/skills/` directory
- [ ] Creates `.agent/skills -> ../.claude/skills` symlink
- [ ] Creates `.opencode/skill -> ../.claude/skills` symlink (singular!)
- [ ] Creates `GEMINI.md` with directive to load `AGENTS.md`
- [ ] Adds `.agent/`, `.opencode/`, `GEMINI.md` to `.gitignore` (NOT `.claude/`)
- [ ] Reports success with verification commands

**Failure indicators:**
- Creating `.agent/` as source instead of `.claude/`
- Using absolute paths in symlinks
- Not adding entries to `.gitignore`
- Creating `.opencode/skills/` (plural) instead of `.opencode/skill/` (singular)

---

### Scenario 2: Agent Backward Compatibility

**Setup**: Repo with existing `.claude/skills/` directory.

**Query:** "Add agent backward compatibility" or "Run skills-local-setup agent"

**Expected behaviors:**
- [ ] Creates `.agent/skills -> ../.claude/skills` symlink
- [ ] If `.claude/settings.json` exists, creates `.agent/settings.json` symlink
- [ ] Adds `.agent/` to `.gitignore`

**Failure indicators:**
- Creating `.agent/` as a real directory instead of symlinks
- Symlink pointing wrong direction

---

### Scenario 3: Migration from Old Setup

**Setup**: Repo with existing `.agent/skills/` directory (old setup) and `.agent/settings.json`.

**Query:** "Migrate to new setup" or "Run skills-local-setup agent"

**Expected behaviors:**
- [ ] Creates `.claude/skills/` directory
- [ ] Copies `.agent/settings.json` to `.claude/settings.json`
- [ ] Reports migration happened

**Failure indicators:**
- Losing existing settings
- Not informing user about migration

---

### Scenario 4: Existing Symlinks

**Query:** "Set up skills" (but symlinks already exist)

**Expected behaviors:**
- [ ] Reports symlinks already exist
- [ ] Shows current symlink targets
- [ ] Does NOT recreate or modify

**Failure indicators:**
- Deleting and recreating existing symlinks
- Silent failure

---

### Scenario 5: OpenCode Setup

**Setup**: Repo with existing `.claude/skills/` directory.

**Query:** "Set up OpenCode" or "Run skills-local-setup opencode"

**Expected behaviors:**
- [ ] Creates `.opencode/skill -> ../.claude/skills` symlink (singular!)
- [ ] Adds `.opencode/` to `.gitignore`

**Failure indicators:**
- Creating `.opencode/skills/` (plural) instead of `.opencode/skill/` (singular)
- Symlink pointing wrong direction

---

## Validation Commands

```bash
# Check directory structure
ls -la .claude/ .agent/ .opencode/ GEMINI.md 2>/dev/null

# Verify symlinks point correctly
readlink .agent/skills        # Should show "../.claude/skills"
readlink .opencode/skill      # Should show "../.claude/skills" (singular!)
cat GEMINI.md                 # Should show directive to load AGENTS.md

# Check .gitignore has entries (should NOT include .claude/)
grep -E "\.agent|\.opencode|GEMINI" .gitignore

# Verify git ignores symlinks
git status
```

## Known Edge Cases

| Case | Expected Behavior |
|------|-------------------|
| No AGENTS.md when setting up Gemini | Error with instructions to run skills-index-updater |
| Existing non-symlink .agent/skills | Prompt user for confirmation before replacing |
| Empty .agent/ directory | Create symlinks inside it |
| Running outside git repo | Error: "Not in a git repository" |
