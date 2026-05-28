---
name: release-prep
description: Prepare release documentation including CHANGELOG entry, announcement text, and validation. Run before tagging a new release.
---

# Release Prep Skill

This skill automates release preparation for MassGen, generating CHANGELOG entries, announcement text, and validating documentation.

## When to Use

Run this skill when preparing a new release:
- After merging the release PR to main
- Before creating the git tag

## Usage

```
/release-prep v0.1.34
```

## What This Skill Does

### 1. Gather Changes

Read commits and PRs since the last tag:

```bash
# Get last tag
git describe --tags --abbrev=0

# Get commits since last tag
git log v0.1.33..HEAD --oneline

# Get merged PRs (if using GitHub)
gh pr list --base main --state merged --search "merged:>2024-01-01"
```

### 2. Archive Previous Announcement

If `docs/announcements/current-release.md` exists:

```bash
# Extract version from current-release.md
VERSION=$(grep -m1 "^# MassGen v" docs/announcements/current-release.md | sed 's/# MassGen v\([^ ]*\).*/\1/')

# Archive it
mv docs/announcements/current-release.md docs/announcements/archive/v${VERSION}.md
```

### 3. Generate CHANGELOG Entry

**Update the Recent Releases section** at the top of `CHANGELOG.md`:
- Add the new release summary at the top
- Keep only the **3 newest releases** in this section
- Remove older entries (they remain in the detailed changelog below)

Create a structured entry following Keep a Changelog format:

```markdown
## [0.1.34] - YYYY-MM-DD

### Added
- **Feature Name**: Description
  - Implementation details

### Changed
- **Modified Feature**: What changed

### Fixed
- **Bug #123**: Description of fix

### Documentations, Configurations and Resources
- **Feature Guide**: New `docs/source/user_guide/feature.rst` for feature usage
- **Design Document**: New `docs/dev_notes/feature_design.md` for implementation details
- **Updated Docs**: Updated `docs/source/reference/cli.rst` with new commands
- **Skills**: New `massgen/skills/skill-name/SKILL.md` for automation
```

**Documentation section rules:**
- Reference specific file paths (`.rst`, `.md`, `.yaml` files)
- Use "New" for newly added files, "Updated" for modified files
- Run `git diff <last-tag>..HEAD --name-only -- "*.md" "*.rst" "*.yaml"` to find changed docs

**Categorization rules:**
- `feat:` commits → Added
- `fix:` commits → Fixed
- `docs:` commits → Documentation
- `refactor:`, `perf:` commits → Changed
- Breaking changes → highlight with ⚠️

**Contributors:**
- Run `git shortlog -sn <last-tag>..HEAD` to find all contributors
- List contributors by commit count in the Technical Details section

### 4. Generate Announcement

Create `docs/announcements/current-release.md`:

```markdown
# MassGen vX.X.X Release Announcement

## Release Summary

We're excited to release MassGen vX.X.X, adding [MAIN FEATURE]! 🚀

[2-3 sentences describing the key changes]

## Install

\`\`\`bash
pip install massgen==X.X.X
\`\`\`

## Links

- **Release notes:** https://github.com/massgen/MassGen/releases/tag/vX.X.X
- **X post:** [TO BE ADDED AFTER POSTING]
- **LinkedIn post:** [TO BE ADDED AFTER POSTING]
```

### 5. Validate Documentation

Check that required documentation exists:

```bash
# Check for user guide updates (if new features)
ls docs/source/user_guide/

# Check capabilities.py updated (if new models)
git diff v0.1.33..HEAD -- massgen/backend/capabilities.py

# Check token_manager.py (if pricing changes)
git diff v0.1.33..HEAD -- massgen/token_manager/token_manager.py

# Check for case study
ls docs/source/examples/case_studies/
```

### 6. Character Count Check

Verify announcement fits LinkedIn's ~3000 char limit:

```bash
# Count characters
cat docs/announcements/current-release.md docs/announcements/feature-highlights.md | wc -m

# Should be < 3000
```

### 7. Suggest Screenshot/Media

Based on the changes in this release, suggest what screenshot or GIF to capture:

**Feature-to-Screenshot Mapping:**

| Change Type | Screenshot Suggestion |
|-------------|----------------------|
| New backend/model support | Terminal showing agent using new model with successful response |
| Multi-agent coordination | Multiple agents working in parallel with colored output |
| Voting/consensus | Voting phase with agent decisions and final selection |
| MCP tools | Tool execution with visible results (file ops, search, etc.) |
| Context compression | Log output showing compression stats and message counts |
| Memory/persistence | Agent recalling context from previous session |
| Web UI changes | Dashboard with agent activity or new UI feature |
| Cost tracking | Summary showing token usage and costs per agent |
| Error handling | Agent gracefully recovering from failure |
| Performance improvements | Before/after timing or throughput comparison |
| New config options | YAML config snippet with new options highlighted |

**Analysis approach:**

1. Look at the main features from commits
2. Identify the most visually compelling change
3. Suggest specific command to run that demonstrates the feature
4. Note if a GIF (via VHS) would be better than a static screenshot

**Example output:**

```
### 📸 Suggested Screenshot for v0.1.34

Based on this release's changes, recommend capturing:

**Primary:** GPT-5 model support
- Run: `massgen --config massgen/configs/providers/openai/gpt5_demo.yaml "Explain quantum computing"`
- Capture: Terminal showing GPT-5 model name in agent output with response

**Alternative:** Context compression improvements
- Run: `massgen --automation --config [long-context-config] "question" | grep compression`
- Capture: Log output showing reduced token counts

**Media type:** Static screenshot is fine (no complex animation needed)
```

### 8. Output Summary

Print a checklist:

```
## Release Prep Summary for v0.1.34

✅ Archived previous announcement → archive/v0.1.33.md
✅ Generated CHANGELOG entry draft
✅ Created current-release.md
✅ Character count: 2847/3000

### Manual Steps Remaining:
1. Review and edit CHANGELOG.md entry
2. Review announcement text in current-release.md
3. Capture suggested screenshot (see below)
4. Commit changes
5. Create tag: git tag v0.1.34 && git push origin v0.1.34
6. Publish GitHub Release (triggers PyPI publish)
7. Post to LinkedIn/X with screenshot, update links in current-release.md

### 📸 Screenshot Suggestion:
[Feature-specific suggestion based on changes]

### Validation Warnings:
⚠️ No case study found for this release
⚠️ capabilities.py was modified - verify docs updated
```

## Reference Files

- **Announcement directory:** `docs/announcements/`
- **Feature highlights:** `docs/announcements/feature-highlights.md`
- **Current release:** `docs/announcements/current-release.md`
- **Release checklist:** `docs/dev_notes/release_checklist.md`
- **CHANGELOG:** `CHANGELOG.md`

## Tips

- Run this skill on the main branch after merging the release PR
- The generated CHANGELOG entry is a draft - review and edit before committing
- Update feature-highlights.md if this release adds major new capabilities
- After posting to social media, update the links in current-release.md
