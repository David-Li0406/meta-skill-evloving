---
name: yazi-plugin-migration
description: Migrate an existing yazi plugin (non-submodule) to a git submodule by forking
---

# Yazi Plugin Migration

Migrate a yazi plugin from local files to a git submodule, preserving local modifications.

## Prerequisites

- The plugin must exist at `yazi/plugins/<plugin-name>.yazi/`
- The plugin must NOT already be a git submodule
- User must have `gh` CLI authenticated with access to `studio-boxcat` org

## Arguments

`$ARGUMENTS` should be the plugin name (e.g., `close-and-restore-tab` for `close-and-restore-tab.yazi`)

## Instructions

### Step 1: Validate the plugin exists and is not a submodule

```bash
# Check plugin directory exists
ls -la yazi/plugins/<plugin-name>.yazi/

# Verify it's not already a submodule
git submodule status | grep <plugin-name> || echo "Not a submodule (good)"
```

### Step 2: Find the original repository

Check the plugin's README.md for upstream source:
```bash
cat yazi/plugins/<plugin-name>.yazi/README.md
```

Common locations:
- `https://github.com/yazi-rs/plugins` (official plugins monorepo)
- `https://github.com/<author>/<plugin-name>.yazi`

### Step 3: Compare local vs upstream and create patch

Fetch the upstream main.lua via raw GitHub URL and compare with local version:
```bash
# Fetch upstream (try main branch first, then master)
curl -sf https://raw.githubusercontent.com/<author>/<plugin-name>.yazi/main/main.lua > /tmp/upstream-main.lua \
  || curl -sf https://raw.githubusercontent.com/<author>/<plugin-name>.yazi/master/main.lua > /tmp/upstream-main.lua

# Create unified diff patch (upstream -> local direction, with correct paths for git apply)
diff -u /tmp/upstream-main.lua yazi/plugins/<plugin-name>.yazi/main.lua \
  | sed 's|/tmp/upstream-main.lua|a/main.lua|; s|yazi/plugins/<plugin-name>.yazi/main.lua|b/main.lua|' \
  > /tmp/<plugin-name>-local.patch
```

If the patch is empty, there are no local modifications - skip Step 6.

### Step 4: Fork the repository to studio-boxcat org

```bash
gh repo fork <author>/<plugin-name>.yazi --org studio-boxcat --clone=false
```

If the fork already exists, this step will skip automatically.

### Step 5: Remove existing plugin files from git and add as submodule

**Important**: Use `git rm` (not `rm`) since files are tracked in git index.

```bash
git rm -rf yazi/plugins/<plugin-name>.yazi
git submodule add https://github.com/studio-boxcat/<plugin-name>.yazi.git yazi/plugins/<plugin-name>.yazi
```

### Step 6: Apply the patch and push to fork

**Important**: Use `git -C <path>` to avoid shell directory state issues.

```bash
# Apply patch
git -C yazi/plugins/<plugin-name>.yazi apply /tmp/<plugin-name>-local.patch

# Commit and push
git -C yazi/plugins/<plugin-name>.yazi add -A
git -C yazi/plugins/<plugin-name>.yazi commit -m "Apply local modifications"
git -C yazi/plugins/<plugin-name>.yazi push origin main
```

### Step 7: Commit submodule reference in main repo

```bash
git add yazi/plugins/<plugin-name>.yazi .gitmodules
git commit -m "yazi: migrate <plugin-name> plugin to submodule"
```

## Monorepo Plugins (yazi-rs/plugins)

For plugins from the official monorepo, you have two options:

**Option A**: Fork entire monorepo and use specific subdirectory
```bash
gh repo fork yazi-rs/plugins --org studio-boxcat --clone=false
git submodule add https://github.com/studio-boxcat/plugins.git yazi/plugins/yazi-rs-plugins
# Configure yazi to use the specific plugin path
```

**Option B**: Use git subtree to extract just the plugin (more complex)

## Notes

- Clean up the temporary patch file after successful migration
- The `.gitmodules` file will be created/updated automatically by `git submodule add`
- Always use `git -C <path>` instead of `cd` to avoid shell state issues
- Step 3 only patches `main.lua` - for plugins with multiple modified files, repeat the diff/sed for each file or create patches manually
