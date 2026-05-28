# Evolution Log

> **Convention**: Reverse chronological order (newest on top, oldest at bottom). Prepend new entries.

---

## 2025-12-04: Expand Path Patterns for Script Portability

**Trigger**: Multi-agent audit found hardcoded paths across all skills/scripts.

### Problem

Path-patterns.md only covered markdown-specific patterns. Scripts had transgressions:

- `/Users/terryli/.claude/skills` (user-specific path)
- `/tmp/jscpd-report` (hardcoded temp directory)
- `~/.local/bin/graph-easy` (hardcoded binary location)

### Solution

1. Added 3 new unsafe patterns to `path-patterns.md`:
   - **Pattern 4**: Hardcoded user-specific paths (`/Users/<user>`, `/home/<user>`)
   - **Pattern 5**: Hardcoded temp directories (`/tmp`)
   - **Pattern 6**: Hardcoded binary locations (`~/.local/bin/tool`)

2. Expanded Validation Checklist with script-specific checks

3. Updated Skill Quality Checklist with inline examples:
   - Use `$HOME` not `/Users/<user>`
   - Use `tempfile.TemporaryDirectory` not `/tmp`
   - Use `command -v` not hardcoded paths

### Key Insight

Portability requires discipline in BOTH markdown AND scripts. Multi-agent parallel audit is effective for finding distributed issues across a codebase.

---

## 2025-12-04: Add Path Patterns Reference

**Trigger**: `/itp:setup` command failed due to unsupported `$(dirname "$0")` pattern in markdown.

### Problem

Command markdown files used `$(dirname "$0")` to resolve script paths, but `$0` is not set in the context where Claude reads markdown files. This is a known Claude Code bug ([#9354](https://github.com/anthropics/claude-code/issues/9354)).

### Solution

1. Created `references/path-patterns.md` documenting:
   - **Safe patterns**: Explicit fallback paths, relative links, `${BASH_SOURCE[0]}` in scripts
   - **Unsafe patterns**: `$(dirname "$0")` in markdown, bare `${CLAUDE_PLUGIN_ROOT}` without fallback
   - **Related GitHub issues**: #9354, #11278
   - **Migration guide**: How to find and fix unsafe patterns

2. Added to Skill Quality Checklist:
   - "No unsafe path patterns in markdown"

3. Added to Reference Documentation list

### Key Insight

Environment variables and bash context (`$0`, `$SCRIPT_DIR`) behave differently in actual scripts vs. markdown documentation that Claude reads. Always use explicit fallback paths for marketplace plugins.

---

## 2025-12-04: Add Continuous Improvement Section

**Trigger**: User identified gap—skill had mechanics for self-evolution but no proactive trigger.

### Problem

Skill-architecture taught HOW to make skills self-evolving (Template D, Post-Change Checklist, evolution-log) but didn't instruct Claude to ACTIVELY WATCH for improvement opportunities during normal usage.

### Solution

Added "Continuous Improvement (Proactive Self-Evolution)" section with:

- **6 improvement signals** to watch for (friction, edge cases, better patterns, confusion, tool evolution, repeated steps)
- **Immediate Update Protocol** (pause → fix → log → resume)
- **What NOT to update** (guard rails)
- **Self-Reflection Trigger** (post-task question)

### Key Insight

The distinction between reactive (what to do after changes) and proactive (actively seeking improvements) is critical. Skills should be vigilant observers, not passive recipients.

---

## 2024-12-04: Adversarial Audit Round 3 (Multi-Agent)

**Trigger**: User spawned 5 parallel sub-agents for comprehensive audit.

### Agents Deployed

| Agent             | Perspective              | Severity Found |
| ----------------- | ------------------------ | -------------- |
| Structural        | Skill Anatomy compliance | NONE           |
| Template-Tutorial | Alignment check          | MEDIUM         |
| References        | Link integrity           | LOW            |
| Description       | YAML triggers            | MEDIUM         |
| Checklist         | Self-compliance          | CRITICAL       |

### Critical Fix

**Issue**: skill-architecture not registered in `~/.claude/CLAUDE.md`
**Impact**: Violates its own teaching (Template A step 10, Tutorial Step 6)
**Fix**: Added "Global Skills" section to `~/.claude/CLAUDE.md`

### Medium Fixes

1. **YAML description** - Added specific trigger keywords: "YAML frontmatter", "validate skill", "TodoWrite templates", "bundled resources", "progressive disclosure", "allowed-tools"

2. **Orphaned file** - Added `workflow-patterns.md` to Reference Documentation

3. **Template ordering** - Swapped steps 4↔5 in Template A to match tutorial advice ("resources first, then SKILL.md")

### Low Fix

**Orphaned file**: `workflow-patterns.md` existed but wasn't referenced. Added to Reference Documentation section.

### Key Insight

Multi-agent parallel audit with different perspectives finds issues single-pass review misses. Critical issue (not registered in CLAUDE.md) was ironic - the skill teaches the very thing it violated.

---

## 2024-12-04: Adversarial Audit Round 2

**Trigger**: User requested second adversarial review to find remaining flaws.

### Flaws Found

| #   | Flaw                                                 | Location      |
| --- | ---------------------------------------------------- | ------------- |
| 1   | Skill Anatomy incomplete - missing evolution-log.md  | Lines 213-219 |
| 2   | Template D assumes config-reference.md always needed | Line 66       |
| 3   | Templates don't reference detailed tutorial          | Lines 18-83   |
| 4   | "6 Steps" title misleading vs 11-step Template A     | Line 124      |

### Changes Made

1. **Skill Anatomy updated** - Added `references/evolution-log.md` as recommended structure
2. **Template D step 5** - Changed to "(if skill manages external config)"
3. **Added cross-reference** - Templates section now links to tutorial
4. **Renamed section** - "6 Steps" → "Detailed Tutorial" with note to use templates

### Key Insight

Adversarial self-review catches inconsistencies that initial implementation misses. Two passes are better than one.

---

## 2024-12-04: TodoWrite-First Pattern + Self-Alignment

**Trigger**: User identified skill-architecture didn't follow its own standards.

### Changes Made

1. **Added TodoWrite Task Templates section** (FIRST section after frontmatter)
   - Template A: Create New Skill (11 steps)
   - Template B: Update Existing Skill
   - Template C: Add Resources to Skill
   - Template D: Convert to Self-Evolving Skill
   - Template E: Troubleshoot Skill Not Triggering
   - Skill Quality Checklist

2. **Added Post-Change Checklist (Self-Maintenance)**
   - skill-architecture now maintains itself like other skills

3. **Updated Step 4: Edit the Skill**
   - Added requirements for TodoWrite Task Templates
   - Added requirements for Post-Change Checklist

4. **Updated Step 6: Register and Iterate**
   - Added "Register skill in project CLAUDE.md"
   - Added "Verify against Skill Quality Checklist"

5. **Created this evolution-log.md**
   - skill-architecture is now self-documenting

### Flaws Fixed

| Flaw                              | Resolution                                                         |
| --------------------------------- | ------------------------------------------------------------------ |
| 6 Steps vs Template A misaligned  | Updated 6 Steps to include registration and checklist verification |
| No Post-Change Checklist for self | Added Self-Maintenance section                                     |
| Not self-evolving                 | Created evolution-log.md                                           |
| Step 4 incomplete                 | Added TodoWrite templates + Checklist requirements                 |

### Key Insight

The meta-skill that teaches skill creation must itself be an exemplar. Any pattern it teaches (TodoWrite templates, Post-Change Checklist, evolution tracking) must be present in itself.
