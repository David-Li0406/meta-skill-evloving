# Testing & evaluation

Testing documentation for the skill index updater.

## Testing summary

| Model | Tested | Result |
|-------|--------|--------|
| Claude Haiku | - | - |
| Claude Sonnet | - | - |
| Claude Opus | - | - |

## Evaluation scenarios

### Scenario 1: Update from home directory

**Query:** "Update the skill index" (while in `~/`)

**Expected behaviors:**
- [ ] Runs `python3 ~/.claude/skills/skills-index-updater/scripts/update_skill_index.py`
- [ ] Updates `~/.kiro/steering/global.md` with global skills
- [ ] Skips local skills (displays message: "working from home directory")
- [ ] Does NOT prompt for any user input

**Failure indicators:**
- Prompting for global/local choice
- Trying to update AGENTS.md when in ~/
- Creating AGENTS.md in home directory

---

### Scenario 2: Update from a repository

**Query:** "Update skill index" (while in a git repo that's not ~/`)

**Expected behaviors:**
- [ ] Updates `~/.kiro/steering/global.md` with global skills
- [ ] Updates `AGENTS.md` in the repo with local skills
- [ ] If AGENTS.md doesn't exist, prompts to create it
- [ ] Reports skill counts for both global and local

**Failure indicators:**
- Only updating one of the two files
- Mixing global and local skills in the same file

---

### Scenario 3: Dry run preview

**Query:** "Preview what the skill index update would do"

**Expected behaviors:**
- [ ] Uses `--dry-run` flag
- [ ] Shows what would be written to both global.md and AGENTS.md
- [ ] Does NOT modify any files
- [ ] Clearly labels output as "DRY RUN"

**Failure indicators:**
- Making changes during dry run
- Not showing both global and local outputs

---

### Scenario 4: Missing index section

**Query:** "Update skill index" (but target file lacks the index section)

**Expected behaviors:**
- [ ] Script reports error: "## Available Skills Index header not found"
- [ ] Suggests adding the section marker
- [ ] Does NOT crash or corrupt file
- [ ] Continues processing other files if one fails

**Failure indicators:**
- Appending index to wrong location
- Silent failure
- Corrupting existing file content

---

### Scenario 5: Outside a repository

**Query:** "Update skill index" (from a directory that's not a git repo and not ~/)

**Expected behaviors:**
- [ ] Updates global skills in `~/.kiro/steering/global.md`
- [ ] Skips local skills (displays message: "not in a git repository")
- [ ] Completes successfully

**Failure indicators:**
- Failing entirely because not in a repo
- Creating AGENTS.md in a non-repo directory

---

## Validation commands

```bash
# Dry run to preview all changes
python3 ~/.claude/skills/skills-index-updater/scripts/update_skill_index.py --dry-run

# Check global.md was updated
grep -A 5 "## Available Skills Index" ~/.kiro/steering/global.md

# Check AGENTS.md was updated (when in a repo)
grep -A 5 "## Available Skills Index" AGENTS.md

# Count skills found during run
python3 ~/.claude/skills/skills-index-updater/scripts/update_skill_index.py 2>&1 | grep "Found"

# Verify no interactive prompts (except for AGENTS.md creation)
echo "" | python3 ~/.claude/skills/skills-index-updater/scripts/update_skill_index.py --dry-run
```

## Known edge cases

| Case | Expected behavior |
|------|-------------------|
| Skill folder without SKILL.md | Warning printed, skill skipped |
| Invalid YAML in frontmatter | Warning printed, skill skipped |
| Missing name or description | Warning printed, skill skipped |
| Hidden folders (starting with .) | Automatically excluded |
| global.md doesn't exist | Warning printed, global update skipped |
| AGENTS.md doesn't exist | Prompt to create (or use --init) |
| Running from ~/ | Only updates global skills |
| No local skills in repo | Reports 0 local skills, still updates AGENTS.md |
