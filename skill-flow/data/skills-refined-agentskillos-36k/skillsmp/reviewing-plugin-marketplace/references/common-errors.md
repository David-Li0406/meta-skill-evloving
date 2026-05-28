# Common Marketplace Configuration Errors

Detailed error patterns encountered in real-world Claude Code plugin marketplace configurations, with solutions.

## Table of Contents

- **enabledPlugins Format Error** ⚠️ #1 CRITICAL
- Repository URL Mismatches
- Source Path Errors
- Skills Path Validation
- Settings.json Format Issues
- Understanding the `strict` Field

## enabledPlugins Format Error ⚠️ MOST COMMON ISSUE

### Error Pattern

Plugins appear to install successfully, but **don't actually load or activate**. No obvious error messages.

### Root Cause

Using **array format** instead of **object format** in `.claude/settings.json`:

**WRONG** (array format - DOES NOT WORK):
```json
{
  "enabledPlugins": [
    "example-plugin@my_marketplace"
  ]
}
```

**CORRECT** (object format - WORKS):
```json
{
  "enabledPlugins": {
    "example-plugin@my_marketplace": true,
    "another-plugin@my_marketplace": true
  }
}
```

### Impact

**CRITICAL**: This is the **#1 cause of "my plugin isn't working" issues**. Based on real testing:
- ✗ Array format: Plugins silently fail to activate
- ✓ Object format: Plugins load and work correctly

### Detection

Check user's `.claude/settings.json`:
```bash
cat .claude/settings.json | grep -A 3 enabledPlugins
```

Look for square brackets `[...]` (wrong) vs curly braces `{...}` (correct).

### Solution

**Fix the format in user's project settings.json**:

```json
{
  "extraKnownMarketplaces": {
    "your-marketplace-name": {
      "source": {
        "source": "github",
        "repo": "owner/repo"
      }
    }
  },
  "enabledPlugins": {
    "plugin-name@marketplace-name": true
  }
}
```

**For multiple plugins**:
```json
{
  "enabledPlugins": {
    "plugin-one@marketplace": true,
    "plugin-two@marketplace": true,
    "another-plugin@different-marketplace": true
  }
}
```

### Prevention

- Always show **object format** in documentation examples
- Include complete `.claude/settings.json` examples in README.md
- Test installation instructions in a clean project

## Repository URL Mismatches

### Error Pattern

```
Plugin 'skills-helper' not found in marketplace 'agentic-skills-creator'
→ Plugin may not exist in marketplace 'agentic-skills-creator'
```

### Root Cause

Repository URLs don't match across configuration files:

```
README.md:           SoftGraphy/agentic-ai-skills-creator
marketplace.json:    (no repo field, uses marketplace name)
Git remote:          taisukeoe/agentic-ai-skills-creator  ← ACTUAL
User settings:       SoftGraphy/agentic-ai-skills-creator  ← WRONG
```

Claude Code fetches from the **git remote URL in user's settings.json**, but that URL is wrong.

### Detection

Check all locations:
1. `git remote -v` - The source of truth for YOUR repository
2. `README.md` - Installation examples
3. User's project `.claude/settings.json` - The URL they're using to fetch

### Solution

**Fix all URLs to match git remote**:

```bash
# 1. Check actual remote
git remote -v
# Output: origin  git@github.com:taisukeoe/repo.git

# 2. Update README.md installation examples
sed -i '' 's/SoftGraphy/taisukeoe/g' README.md

# 3. Commit and push
git add README.md
git commit -m "fix: correct repository URLs in documentation"
git push

# 4. In user's project, update .claude/settings.json
# Change: "repo": "SoftGraphy/agentic-ai-skills-creator"
# To:     "repo": "taisukeoe/agentic-ai-skills-creator"

# 5. Refresh marketplace in user's project
/plugin marketplace remove agentic-skills-creator
/plugin marketplace add taisukeoe/agentic-ai-skills-creator
```

### Prevention

- Always verify `git remote -v` before writing documentation
- Use correct owner/username from the start
- Test installation in a separate project before publishing

## Source Path Errors

### Error Pattern: Wrong Directory

**marketplace.json**:
```json
{
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./.claude-plugin"  ← WRONG: Don't point to .claude-plugin
    }
  ]
}
```

**Correct** (Anthropic format):
```json
{
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./",  ← Correct: Point to repository root
      "skills": [
        "./skills/skill-one",
        "./skills/skill-two"
      ]
    }
  ]
}
```

### Why "./" is Correct

marketplace.json is **already in** `.claude-plugin/`, so:
- `source: "./"` means "go to repository root from .claude-plugin/"
- Skills are in `skills/` at the root
- This matches Anthropic's official format

### Verification

```bash
# From repository root, verify structure:
ls -la .claude-plugin/marketplace.json  # Should exist
ls -la skills/                          # Should exist
ls -la skills/*/SKILL.md                # Each skill should have SKILL.md
```

## Skills Path Validation

### Error Pattern

```json
{
  "skills": [
    "./skills/creating-effective-skills",  ← Exists
    "./skills/reviewing-skills",           ← Exists
    "./skills/missing-skill"               ← DOESN'T EXIST
  ]
}
```

### Impact

- Claude Code fails to load the plugin
- Confusing error messages
- Skills won't be available

### Detection

```bash
# Verify each skill path exists with SKILL.md
for skill_path in ./skills/*; do
  if [ ! -f "$skill_path/SKILL.md" ]; then
    echo "❌ Missing SKILL.md in $skill_path"
  else
    echo "✓ $skill_path"
  fi
done
```

### Solution

**Option 1: Remove invalid paths**:
```json
{
  "skills": [
    "./skills/creating-effective-skills",
    "./skills/reviewing-skills"
    // Removed missing-skill
  ]
}
```

**Option 2: Create the missing skill**:
```bash
mkdir -p skills/missing-skill
# Create SKILL.md with proper frontmatter
```

## Settings.json Format Issues

### Wrong Format (Deprecated)

**INCORRECT** (old format, doesn't work):
```json
{
  "skills": {
    "allow": ["skill-name"]
  }
}
```

### Correct Formats

#### User's Project Settings

**.claude/settings.json** (in project using your marketplace):
```json
{
  "extraKnownMarketplaces": {
    "agentic-skills-creator": {
      "source": {
        "source": "github",
        "repo": "taisukeoe/agentic-ai-skills-creator"
      }
    }
  },
  "enabledPlugins": {
    "skills-helper@agentic-skills-creator": true
  },
  "permissions": {
    "allow": [
      "Skill(creating-effective-skills)",
      "Skill(reviewing-skills)",
      "Skill(reviewing-plugin-marketplace)"
    ]
  }
}
```

**Key points**:
- `extraKnownMarketplaces` - Registers your marketplace
- `enabledPlugins` - Format: `"plugin-name@marketplace-name": true`
- `permissions.allow` - Format: `"Skill(skill-name)"`

#### Your Marketplace Repository Settings

**.claude/settings.json** (in your marketplace repository for local dev):
```json
{
  "permissions": {
    "allow": [
      "Skill(creating-effective-skills)",
      "Skill(reviewing-skills)",
      "Skill(reviewing-plugin-marketplace)"
    ]
  }
}
```

**Note**: Skills in `.claude/skills/` (via symlink to `skills/`) are auto-discovered, so you only need to pre-approve them.

## Anthropic Official Format

### Recommended Structure

Follow https://github.com/anthropics/skills:

```
your-repo/
├── .claude-plugin/
│   └── marketplace.json          ← Only this file needed
├── skills/
│   ├── skill-one/
│   │   └── SKILL.md
│   └── skill-two/
│       └── SKILL.md
└── README.md
```

**NO plugin.json needed** - marketplace.json contains everything.

### marketplace.json Template

```json
{
  "name": "your-marketplace-name",
  "owner": {
    "name": "Your Name"
  },
  "metadata": {
    "description": "Brief description",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "your-plugin-name",
      "description": "What the plugin does",
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/skill-one",
        "./skills/skill-two"
      ]
    }
  ]
}
```

## Understanding the `strict` Field

### What It Does

The `strict` field in marketplace.json controls whether plugins **must** have their own `plugin.json` file.

**`strict: true` (default)**:
- Each plugin directory MUST include `.claude-plugin/plugin.json`
- marketplace.json fields supplement the plugin's own manifest
- More rigid structure

**`strict: false`**:
- plugin.json is **optional**
- If plugin.json is missing, marketplace.json serves as the complete manifest
- More flexible structure

### Real-World Impact

**Based on actual testing**: If your plugins already have `plugin.json` files, `strict: false` **has NO EFFECT**.

**Example**: Multi-plugin marketplace testing:
```
plugins/category-a/tool-one/.claude-plugin/plugin.json  ← EXISTS
plugins/category-b/tool-two/.claude-plugin/plugin.json ← EXISTS

Result: strict: false does nothing (plugins already have plugin.json)
```

### When It Matters

**Use `strict: false` when**:
- You want to define plugins entirely in marketplace.json (no individual plugin.json files)
- Simpler plugin structure for lightweight tools
- Example from Anthropic's format

**No need for `strict: false` when**:
- Each plugin has its own `.claude-plugin/plugin.json` (multi-plugin marketplace)
- Plugin structure is already established
- **This is the common case for organizational marketplaces**

### Configuration Examples

**Scenario 1: Multi-plugin with individual plugin.json files**
```json
{
  "plugins": [
    {
      "name": "example-tool",
      "source": "./plugins/category/example-tool"
      // Each plugin dir has .claude-plugin/plugin.json
      // strict: false has NO EFFECT here
    }
  ]
}
```

**Scenario 2: Single plugin, no plugin.json (Anthropic pattern)**
```json
{
  "plugins": [
    {
      "name": "my-skills",
      "source": "./",
      "strict": false,  ← NEEDED: No plugin.json exists
      "skills": ["./skills/skill-one", "./skills/skill-two"]
    }
  ]
}
```

### Recommendation

**For organizational multi-plugin marketplaces**: Don't worry about `strict: false` - it won't affect functionality if you have plugin.json files.

**For simple skill-only marketplaces**: Use `strict: false` and skip creating individual plugin.json files (follow Anthropic pattern).

### Sources

- [Plugin marketplaces - Claude Code Docs](https://code.claude.com/docs/en/plugin-marketplaces)
- [Plugin marketplaces - Claude Docs](https://anthropic.mintlify.app/en/docs/claude-code/plugin-marketplaces)

## Checklist Before Publishing

**Critical** (breaks functionality):
- [ ] README.md shows **object format** for `enabledPlugins`: `{"plugin@marketplace": true}`
- [ ] NOT array format: `["plugin@marketplace"]` ← WRONG
- [ ] `git remote -v` matches all documentation URLs
- [ ] marketplace.json has `source: "./"`
- [ ] All skills paths exist with SKILL.md

**Testing**:
- [ ] Tested in a separate project:
  ```bash
  /plugin marketplace add your-username/your-repo
  /plugin install plugin-name@your-username/your-repo
  ```
- [ ] Verified settings.json uses correct enabledPlugins format
- [ ] Check `/plugin` for errors tab (should be empty)
- [ ] Skills actually load and work (not just install)

## Recovery from Broken Marketplace

```bash
# In user's project:
/plugin marketplace remove marketplace-name
# Fix your marketplace repository, commit, push
# Re-add marketplace:
/plugin marketplace add correct-owner/repo
# Verify:
/plugin
# Errors tab should be empty
```
