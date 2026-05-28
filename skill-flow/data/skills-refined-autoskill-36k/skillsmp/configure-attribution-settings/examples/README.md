# Attribution Configuration Examples

This directory contains example configurations for common attribution scenarios.

## Examples

### name-change.json
Changing Claude's name while keeping model version.

**Scenario:** User says "Change Claude's name to Big Dawg"

**Changes:**
- Commit: `Co-Authored-By: Big Dawg Sonnet 4.5 <noreply@anthropic.com>`
- PR: Unchanged (default)

**Use this when:** Customizing the AI assistant's name in git attribution

---

### remove-model.json
Removing model information from attribution.

**Scenario:** User says "Remove the model from Co-Authored-By"

**Changes:**
- Commit: `Co-Authored-By: Big Dawg <noreply@anthropic.com>` (no model version)
- PR: Unchanged (default)

**Use this when:** User wants simpler attribution without model version

---

### custom-pr.json
Customizing PR description attribution.

**Scenario:** User says "Change the PR attribution to say it's generated with style and update Claude's name to match"

**Changes:**
- Commit: `Co-Authored-By: Big Dawg <noreply@anthropic.com>`
- PR: `🤖 Generated with ✨ Style ✨ and [Big Dawg](https://claude.com/claude-code)`

**Use this when:** User wants personalized PR attribution messaging

---

### remove-all.json
Completely removing all attribution.

**Scenario:** User says "Remove co-authored by" and confirms they want to remove PR attribution too

**Changes:**
- Commit: `""` (empty - no attribution)
- PR: `""` (empty - no attribution)

**Use this when:** User wants no AI attribution in commits or PRs

---

### partial-update.json
Updating only one field while preserving others.

**Scenario:** User says "Change Claude's name to Big Dawg in the Co-Authored-By"

**Changes:**
- Commit: `Co-Authored-By: Big Dawg Sonnet 4.5 <noreply@anthropic.com>`
- PR: Unchanged (preserved from existing settings)
- model: Unchanged (preserved from existing settings)

**Use this when:** Demonstrating preservation of unrelated settings

---

## Important Notes

### Other Settings Preserved

All examples include other settings (`statusLine`, `model`, etc.) to demonstrate the critical principle of **preserving unrelated configuration** when updating attribution.

When modifying attribution:
- ✅ Only update `attribution.commit` and/or `attribution.pr`
- ✅ Preserve all other keys in settings.local.json
- ✅ When updating only commit, preserve PR
- ✅ When updating only PR, preserve commit

### Usage

These examples show complete `.claude/settings.local.json` files. Extract the `attribution` object to understand what changes, but always merge into existing settings rather than replacing the entire file.
