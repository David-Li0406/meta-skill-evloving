---
name: marketplace-manager
description: Use this skill when you need to manage the claude-code-plugins marketplace catalog, including updating plugins, syncing catalog files, and ensuring catalog integrity.
---

# Marketplace Manager

## Purpose
Automatically manages the claude-code-plugins marketplace catalog system, handling updates to `marketplace.extended.json`, syncing to `marketplace.json`, and ensuring catalog integrity.

## Trigger Keywords
- "update marketplace"
- "sync marketplace" or "sync catalog"
- "add to marketplace"
- "marketplace catalog"
- "update catalog"
- "regenerate marketplace"

## Two-Catalog System

**Critical Understanding:**
```
marketplace.extended.json (SOURCE OF TRUTH)
├── Full metadata
├── Extended fields (featured, mcpTools, etc.)
└── Edit THIS file manually

↓ npm run sync-marketplace

marketplace.json (GENERATED)
├── CLI-compatible subset
├── Sanitized fields
└── NEVER edit directly
```

## Marketplace Management Tasks

### 1. Add Plugin to Catalog

When adding a new plugin, update `marketplace.extended.json` as follows:

```json
{
  "name": "plugin-name",
  "source": "./plugins/category/plugin-name",
  "description": "Clear one-line description",
  "version": "1.0.0",
  "category": "productivity",
  "keywords": ["keyword1", "keyword2"],
  "author": {
    "name": "Author Name",
    "email": "[email protected]"
  },
  "repository": "https://github.com/user/repo",
  "featured": false  // Set to true for featured plugins
}
```

Then run:
```bash
npm run sync-marketplace
```

### 2. Update Plugin Version

To bump a plugin version:

1. Update `plugins/category/plugin-name/.claude-plugin/plugin.json`.
2. Update the corresponding entry in `marketplace.extended.json`.
3. Run `npm run sync-marketplace`.
4. Validate the sync worked:
```bash
git diff .claude-plugin/marketplace.json
```

### 3. Sync Validation

After syncing, verify the following:

```bash
# Check if marketplace.json was regenerated
git status .claude-plugin/marketplace.json

# Validate JSON syntax
jq empty .claude-plugin/marketplace.extended.json
jq empty .claude-plugin/marketplace.json

# Check specific plugin entry
jq '.plugins[] | select(.name == "plugin-name")' .claude-plugin/marketplace.json
```

### 4. Featured Plugin Management

To mark a plugin as featured, update the entry in `marketplace.extended.json`:

```json
{
  "name": "plugin-name",
  "featured": true,  // Add this field
  // ... rest of fields
}
```

Featured plugins will appear first in the marketplace.

### 5. Catalog Integrity Checks

Ensure the integrity of the catalog by performing regular checks and validations as needed.