---
name: kata-update-and-changelog
description: Use this skill when checking for updates to Kata, installing the latest version if available, and displaying changelog entries for recent changes.
---

# Body of the merged SKILL.md

<kata_path>
**IMPORTANT:** Before reading any Kata file (templates, references, workflows), resolve the base path:

```bash
KATA_BASE=$(if [ -n "$CLAUDE_PLUGIN_ROOT" ]; then echo "$CLAUDE_PLUGIN_ROOT/kata"; elif [ -d ~/.claude/kata ]; then echo ~/.claude/kata; else echo ./.claude/kata; fi) && echo $KATA_BASE
```

Use the output as `$KATA_BASE` for all file paths below. For example:
- `$KATA_BASE/templates/summary.md` instead of `~/.claude/kata/templates/summary.md`
</kata_path>

<objective>
Check for Kata updates, install if available, and display what changed since the installed version.
</objective>

<process>

<step name="get_installed_version">
Read installed version from VERSION file:

```bash
if [ -n "$CLAUDE_PLUGIN_ROOT" ]; then
  cat "$CLAUDE_PLUGIN_ROOT/kata/VERSION" 2>/dev/null
elif [ -f ~/.claude/kata/VERSION ]; then
  cat ~/.claude/kata/VERSION
elif [ -f ./.claude/kata/VERSION ]; then
  cat ./.claude/kata/VERSION
fi
```

**If VERSION file missing:**
```
## Kata Update

**Installed version:** Unknown

Your installation doesn't include version tracking.

Running fresh install...
```
</step>

<step name="check_latest_version">
Check npm for the latest version:

```bash
npm view @gannonh/kata version 2>/dev/null
```

**If npm check fails:**
```
Couldn't check for updates (offline or npm unavailable).

To update manually: `npx @gannonh/kata --global`
```

STOP here if npm unavailable.
</step>

<step name="compare_versions">
Compare installed vs latest:

**If installed == latest:**
```
## Kata Update

**Installed:** X.Y.Z
**Latest:** X.Y.Z

You're already on the latest version.
```

STOP here if already up to date.

**If installed > latest:**
```
## Kata Update

**Installed:** X.Y.Z
**Latest:** A.B.C

You're ahead of the latest release (development version?).
```

STOP here if ahead.
</step>

<step name="show_changes_and_confirm">
**If update available**, fetch and show what's new BEFORE updating:

1. Fetch latest CHANGELOG.md from GitHub using WebFetch tool:
   - URL: `https://raw.githubusercontent.com/gannonh/kata/refs/heads/main/CHANGELOG.md`
   - Prompt: "Extract all version entries with their dates and changes. Return in Keep-a-Changelog format."

**If fetch fails:**
Fall back to local changelog:
```bash
cat $KATA_BASE/CHANGELOG.md 2>/dev/null
```

2. Extract entries between installed and latest versions.
3. Display preview and ask for confirmation:

```
## Kata Update Available

**Installed:** 1.5.10
**Latest:** 1.5.15

### What's New
────────────────────────────────────────────────────────────

## [1.5.15] - 2026-01-20

### Added
- Feature X

## [1.5.14] - 2026-01-18

### Fixed
- Bug fix Y

────────────────────────────────────────────────────────────

⚠️  **Note:** The installer performs a clean install of Kata folders:
- `~/.claude/commands/kata/` will be wiped and replaced
- `~/.claude/kata/` will be wiped and replaced
- `~/.claude/agents/kata-*` files will be replaced

Your custom files in other locations are preserved:
- Custom commands in `~/.claude/commands/your-stuff/` ✓
- Custom agents not prefixed with `kata-` ✓
- Custom hooks ✓
- Your CLAUDE.md files ✓

If you've modified any Kata files directly, back them up first.
```

Use AskUserQuestion:
- Question: "Proceed with update?"
- Options:
  - "Yes, update now"
  - "No, cancel"

**If user cancels:** STOP here.
</step>

<step name="run_update">
First, check if running from within the kata source directory:

```bash
grep -q '"name": "@gannonh/kata"' package.json 2>/dev/null && echo "KATA_SOURCE_DIR"
```

**If output is "KATA_SOURCE_DIR":**
```
Cannot run update from within the Kata source directory.
npm resolves @gannonh/kata locally instead of fetching from registry.

**Solutions:**
1. Run `/kata:update` from a different directory
2. Run `cd ~ && npx @gannonh/kata --global` manually
3. Run `npm install -g @gannonh/kata` for global install
```

STOP here if in kata source directory.

Otherwise, run the update:

```bash
npx @gannonh/kata --global
```

Capture output. If install fails, show error and STOP.

Clear the update cache so statusline indicator disappears:

```bash
rm -f ~/.claude/cache/kata-update-check.json
```
</step>

<step name="display_result">
Format completion message (changelog was already shown in confirmation step):

```
╔═══════════════════════════════════════════════════════════╗
║  Kata Updated: v1.5.10 → v1.5.15                           ║
╚═══════════════════════════════════════════════════════════╝

⚠️  Restart Claude Code to pick up the new commands.

[View full changelog](https://github.com/gannonh/kata/blob/main/CHANGELOG.md)
```
</step>

</process>

<success_criteria>
- [ ] Installed version read correctly
- [ ] Latest version checked via npm
- [ ] Update skipped if already current
- [ ] Changelog fetched and displayed BEFORE update
- [ ] Clean install warning shown
- [ ] User confirmation obtained
- [ ] Update executed successfully
- [ ] Restart reminder shown
</success_criteria>