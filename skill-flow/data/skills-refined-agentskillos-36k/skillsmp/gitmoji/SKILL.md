---
name: Gitmoji
description: This skill should be used when the user asks to "use gitmoji", "add gitmoji to commit", "select gitmoji", "find appropriate emoji for commit", or when creating commit messages that should include gitmojis. Provides semantic matching of commit messages to appropriate gitmoji emojis from the official gitmoji database.
version: 0.1.0
---

# Gitmoji Skill

Semantic gitmoji selection for commit messages. Reads gitmoji index, analyzes commit message, selects appropriate emoji prefix. Augments `/commit` workflow.

## When to Use

**Use when:** User requests gitmoji • Integrated into `/commit` skill • Projects using gitmoji conventions • CLAUDE.md specifies gitmoji usage

## Execution Protocol

### 1. Read Gitmoji Indices
**Official index**: Read `skills/gitmoji/cache/gitmojis.txt` (~75 entries, format: `emoji - name - description`)
**Custom index**: Read `skills/gitmoji/custom-gitmojis.md` (project-specific gitmojis)

If index missing, run: `skills/gitmoji/scripts/update-gitmoji-index.sh`

### 2. Analyze Commit Message
Understand semantic meaning:
- **Type**: bug fix • feature • docs • refactor • performance • config • test • deps
- **Scope**: code structure • dependencies • security • CI • architecture
- **Impact**: critical hotfix • breaking change • minor update • WIP

### 3. Select Gitmoji
**Matching criteria:**
- Primary: Direct semantic alignment (fix bug → 🐛, add feature → ✨, improve perf → ⚡️)
- Secondary: Urgency (critical → 🚑️ vs regular 🐛), scope (docs → 📝), special cases (initial → 🎉)

**Selection rules:**
- Most specific gitmoji matching primary intent
- Multiple matches → prefer most significant aspect
- Avoid generic when specific available
- Consider project conventions

**Lookup order:**
1. Official index (`cache/gitmojis.txt`) first
2. Custom index (`custom-gitmojis.md`) if no match
3. Use custom if better semantic match

### 4. Return Format
Return emoji character only (not name/code): `🐛` ✓ • `:bug:` ✗ • `"bug"` ✗

**Commit format**: `emoji commit message` (example: `🐛 Fix null pointer exception in user authentication`)

## Integration

**Methods:**
- **CLAUDE.md**: Always-use instruction
- **Custom /commit skill**: Gitmoji selection step
- **On-demand**: User explicit request

**Scope boundary**: This skill does NOT analyze git diffs - caller's responsibility. Focuses on semantic matching message→gitmoji only.

## Index Maintenance

**Update script**: `skills/gitmoji/scripts/update-gitmoji-index.sh`
**Requirements**: curl • jq • internet connection to gitmoji.dev
**Run when**: New gitmojis released • Initial setup • Periodic refresh (monthly)

## Critical Rules

**Do:**
- Read entire index (small, efficient)
- Semantic matching (not keyword matching)
- Return emoji character in commit message
- Prioritize primary intent

**Don't:**
- Search/grep index (read entirely)
- Use codes (`:bug:`) instead of emoji (🐛)
- Add multiple gitmojis per commit
- Skip selection (make best judgment)

## Resources

**Files:**
- `cache/gitmojis.txt` - Official gitmoji index (75 entries)
- `custom-gitmojis.md` - Project-specific gitmojis
- `scripts/update-gitmoji-index.sh` - Index updater

**Limitations**: Internet for initial download • Manual updates • jq dependency • One gitmoji per commit • No git diff analysis
