# Feed Config Validation

Zod schema validation and error handling for feed-create.

## Validation Gates

Before saving a feed config, it must pass:

1. **Schema validation** - zod validates structure
2. **ID uniqueness** - no duplicate feed IDs
3. **Source reachability** - URL returns 200
4. **Profile existence** - referenced style profiles exist
5. **Template resolution** - `extends` references valid templates

## Zod Schema Validation

```typescript
import { validateFeedConfig } from "~/Developer/utils/epub/schemas/schema.ts";

const result = validateFeedConfig(data);
if (!result.success) {
  // Handle errors
  result.error.issues.forEach(issue => {
    console.error(`${issue.path.join('.')}: ${issue.message}`);
  });
}
```

## Common Validation Errors

### Missing Required Fields

**Error:**
```
feeds.0.id: Required
feeds.0.source: Required
```

**Fix:**
Every feed must have `id` and `source` (or `sources`).

```yaml
feeds:
  - id: my-feed  # Add this
    source: https://example.com/feed.xml  # Add this
```

### Invalid Version

**Error:**
```
version: Expected number, received string
```

**Fix:**
Version must be a number, not a string.

```yaml
version: 1  # Not "1"
```

### Invalid Feature Toggle

**Error:**
```
style.features.syntax_highlighting: Invalid enum value. Expected 'on' | 'off' | 'auto'
```

**Fix:**
Features must be one of the tri-state values.

```yaml
style:
  features:
    syntax_highlighting: auto  # Not "yes" or true
```

### Invalid Style Profile Reference

**Error:**
```
style.profile: Style profile 'custom' not found
```

**Fix:**
Define the profile in `style_profiles` or use built-in.

```yaml
style_profiles:
  custom:
    description: My custom style
    # ... rest of profile

feeds:
  - id: feed
    style: custom  # Now valid
```

## ID Uniqueness Check

```bash
#!/bin/bash
# Check for duplicate feed IDs

FEED_ID="$1"
FEEDS_DIR="$HOME/.epub/feeds"

if [ -f "$FEEDS_DIR/$FEED_ID.yaml" ]; then
  echo "Error: Feed ID '$FEED_ID' already exists"
  exit 1
fi
```

**Fix:**
Choose a different ID or remove the existing feed.

## Source Reachability Check

```bash
#!/bin/bash
# Verify source URL returns 200

URL="$1"
STATUS=$(curl -fsL -o /dev/null -w "%{http_code}" "$URL")

if [ "$STATUS" != "200" ]; then
  echo "Warning: Source URL returned $STATUS"
  exit 1
fi
```

**Warnings:**
- 404: URL not found
- 403: Access denied (may need auth)
- 500: Server error (retry later)
- Timeout: Network issue

**Fixes:**
- Check URL spelling
- Verify feed is public
- Try alternate feed formats (RSS vs Atom)

## Template Resolution

When using `extends`:

```yaml
feeds:
  - id: my-feed
    extends: [reddit_digest]  # Must exist
```

**Check:**
1. Template defined in same file under `templates:`
2. Template exists in skill assets (`~/.claude/skills/feed-create/assets/templates/`)
3. No circular references

**Error:**
```
Template 'reddit_digest' referenced but not defined
```

**Fix:**
Define the template or remove `extends`.

## Style Profile Check

```yaml
feeds:
  - id: feed
    style: technical  # Profile must exist
```

**Built-in profiles:**
- narrative
- technical
- minimal

**Custom profiles:**
Must be defined in `style_profiles:` section.

**Error:**
```
Style profile 'custom' not found
```

**Fix:**
```yaml
style_profiles:
  custom:
    description: My style
    base_css: styles/base.css
    # ...

feeds:
  - id: feed
    style: custom
```

## Validation Script

```bash
#!/bin/bash
# Full validation pipeline

YAML_FILE="$1"

echo "Validating $YAML_FILE..."

# 1. Schema validation
if ! ~/.claude/skills/feed-create/scripts/validate-config.sh "$YAML_FILE"; then
  echo "❌ Schema validation failed"
  exit 1
fi
echo "✓ Schema valid"

# 2. Extract feed ID
FEED_ID=$(yq '.feeds[0].id' "$YAML_FILE")

# 3. Check ID uniqueness
if [ -f "$HOME/.epub/feeds/$FEED_ID.yaml" ]; then
  echo "❌ Feed ID already exists: $FEED_ID"
  exit 1
fi
echo "✓ ID unique"

# 4. Check source reachability
SOURCE=$(yq '.feeds[0].source' "$YAML_FILE")
if [[ "$SOURCE" =~ ^http ]]; then
  if ! curl -fsL -o /dev/null "$SOURCE"; then
    echo "⚠ Warning: Source URL not reachable"
  else
    echo "✓ Source reachable"
  fi
fi

echo "✓ All validation gates passed"
```

## Error Severity

| Severity | Action | Examples |
|----------|--------|----------|
| **error** | Block save | Invalid YAML, missing required fields |
| **warning** | Allow with confirmation | Unreachable URL, unknown profile |
| **info** | Proceed | Unused fields, defaults applied |

## Validation Flow

```
Generate config
    ↓
Schema validation
    ↓ (fail) → Show errors → Fix → Retry
    ↓ (pass)
ID uniqueness check
    ↓ (fail) → Suggest alternative ID
    ↓ (pass)
Source reachability
    ↓ (warn) → Confirm or fix URL
    ↓ (pass)
Template resolution
    ↓ (fail) → Show missing templates
    ↓ (pass)
Style profile check
    ↓ (fail) → Show available profiles
    ↓ (pass)
Preview config
    ↓
User confirms
    ↓
Save to ~/.epub/feeds/
```

## Recovery Strategies

### Invalid Schema

1. Show specific error path
2. Suggest valid values
3. Offer to regenerate with template

### Duplicate ID

1. List existing feed with same ID
2. Suggest alternatives (add -2, change slug)
3. Offer to overwrite (after confirmation)

### Unreachable Source

1. Check URL spelling
2. Probe alternate paths (/feed.xml, /rss, /atom)
3. Suggest manual URL entry
4. Offer to skip reachability check

### Missing Profile

1. List available built-in profiles
2. Suggest closest match (based on content)
3. Offer to create custom profile
4. Fall back to narrative

## Validation Testing

```bash
# Test valid config
feed-create validate examples/reddit-soccer.yaml
# Expected: ✓ All validation gates passed

# Test invalid config (missing id)
feed-create validate examples/invalid.yaml
# Expected: ❌ feeds.0.id: Required

# Test duplicate ID
feed-create validate examples/duplicate.yaml
# Expected: ❌ Feed ID already exists

# Test unreachable source
feed-create validate examples/404-source.yaml
# Expected: ⚠ Warning: Source URL not reachable
```

## Manual Validation Checklist

- [ ] `version: 1` is present
- [ ] At least one feed in `feeds:` array
- [ ] Each feed has `id` field
- [ ] Each feed has `source` or `sources`
- [ ] Referenced templates are defined
- [ ] Referenced profiles are defined or built-in
- [ ] Feature toggles use on/off/auto
- [ ] URLs are well-formed
- [ ] File paths exist
- [ ] No circular template inheritance

## Validation Output Formats

### JSON (for agents)

```json
{
  "valid": false,
  "errors": [
    {
      "path": "feeds.0.id",
      "message": "Required",
      "code": "invalid_type"
    }
  ],
  "warnings": [
    {
      "path": "feeds.0.source",
      "message": "URL not reachable",
      "code": "network_error"
    }
  ]
}
```

### Human-readable

```
❌ Validation failed

Errors:
  • feeds.0.id: Required
  • feeds.0.source: Required

Warnings:
  • style.profile: Profile 'custom' not found (using narrative)

Fix errors and run validation again.
```

## Stable Error Codes

For programmatic handling:

| Code | Meaning | Fix |
|------|---------|-----|
| `invalid_type` | Wrong type (string vs number) | Use correct type |
| `required` | Missing required field | Add field |
| `invalid_enum` | Invalid enum value | Use allowed value |
| `network_error` | URL not reachable | Check URL |
| `duplicate_id` | ID already exists | Choose new ID |
| `missing_reference` | Template/profile not found | Define or use built-in |
| `circular_dependency` | Template inheritance loop | Remove circular extends |
