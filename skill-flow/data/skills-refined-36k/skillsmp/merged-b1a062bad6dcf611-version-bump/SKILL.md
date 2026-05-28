---
name: version-bump
description: Use this skill to bump a plugin version in either the plugin.json or marketplace.json file using semantic versioning when changes warrant a version update.
---

# Version Bump

Bump a plugin version in either `plugins/PLUGIN_NAME/.claude-plugin/plugin.json` or `.claude-plugin/marketplace.json` following semantic versioning.

## Inference Rules

Infer bump type from context:
- **Major** (X.0.0): Breaking changes, renames, restructuring
- **Minor** (x.Y.0): New features, new skills
- **Patch** (x.y.Z): Bug fixes, doc updates, grammar fixes

## Commands

### For plugin.json

```bash
# Bump patch (e.g., 1.2.3 → 1.2.4)
jq '.version |= (split(".") | .[2] = ((.[2] | tonumber) + 1 | tostring) | join("."))' plugins/PLUGIN_NAME/.claude-plugin/plugin.json > /tmp/claude/plugin.json && mv /tmp/claude/plugin.json plugins/PLUGIN_NAME/.claude-plugin/plugin.json

# Bump minor (e.g., 1.2.3 → 1.3.0)
jq '.version |= (split(".") | .[1] = ((.[1] | tonumber) + 1 | tostring) | .[2] = "0" | join("."))' plugins/PLUGIN_NAME/.claude-plugin/plugin.json > /tmp/claude/plugin.json && mv /tmp/claude/plugin.json plugins/PLUGIN_NAME/.claude-plugin/plugin.json

# Bump major (e.g., 1.2.3 → 2.0.0)
jq '.version |= (split(".") | .[0] = ((.[0] | tonumber) + 1 | tostring) | .[1] = "0" | .[2] = "0" | join("."))' plugins/PLUGIN_NAME/.claude-plugin/plugin.json > /tmp/claude/plugin.json && mv /tmp/claude/plugin.json plugins/PLUGIN_NAME/.claude-plugin/plugin.json
```

### For marketplace.json

```bash
# Bump patch (e.g., 1.2.3 → 1.2.4)
jq '(.plugins[] | select(.name == "PLUGIN_NAME") | .version) |= (split(".") | .[2] = ((.[2] | tonumber) + 1 | tostring) | join("."))' .claude-plugin/marketplace.json > /tmp/claude/marketplace.json && mv /tmp/claude/marketplace.json .claude-plugin/marketplace.json

# Bump minor (e.g., 1.2.3 → 1.3.0)
jq '(.plugins[] | select(.name == "PLUGIN_NAME") | .version) |= (split(".") | .[1] = ((.[1] | tonumber) + 1 | tostring) | .[2] = "0" | join("."))' .claude-plugin/marketplace.json > /tmp/claude/marketplace.json && mv /tmp/claude/marketplace.json .claude-plugin/marketplace.json

# Bump major (e.g., 1.2.3 → 2.0.0)
jq '(.plugins[] | select(.name == "PLUGIN_NAME") | .version) |= (split(".") | .[0] = ((.[0] | tonumber) + 1 | tostring) | .[1] = "0" | .[2] = "0" | join("."))' .claude-plugin/marketplace.json > /tmp/claude/marketplace.json && mv /tmp/claude/marketplace.json .claude-plugin/marketplace.json
```

Replace `PLUGIN_NAME` with the actual plugin name.

## Workflow

1. Get current version first:
   - For `plugin.json`:
     ```bash
     jq '.version' plugins/PLUGIN_NAME/.claude-plugin/plugin.json
     ```
   - For `marketplace.json`:
     ```bash
     jq '.plugins[] | select(.name == "PLUGIN_NAME") | .version' .claude-plugin/marketplace.json
     ```
2. Run the appropriate bump command.
3. Confirm new version to user.

## References

- [Plugins](https://code.claude.com/docs/en/plugins)
- [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)