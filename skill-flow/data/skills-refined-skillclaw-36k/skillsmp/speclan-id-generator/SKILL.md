---
name: SPECLAN ID Generator
description: This skill should be used when generating IDs for SPECLAN entities, creating new specs, or needing collision-free unique identifiers. Use when user asks to "create a spec", "generate ID", "new feature ID", "unique requirement ID", or when commands need to assign IDs to new entities.
version: 0.1.0
context: fork
---

# SPECLAN ID Generator

Generate unique, collision-free random IDs for SPECLAN entities with automatic retry and comprehensive collision detection.

## Why Use This Skill

- **Collision-free:** Automatically checks existing IDs and retries if collision detected
- **Entity-aware:** Correct format for each entity type (goals: 3-digit, others: 4-digit)
- **Comprehensive detection:** Checks both filenames AND frontmatter
- **Reusable:** Single script usable by all commands and agents

## Entity ID Formats

| Entity Type | Prefix | Digits | Range | Example |
|-------------|--------|--------|-------|---------|
| goal | G- | 3 | 100-999 | G-142 |
| feature | F- | 4 | 1000-9999 | F-1847 |
| requirement | R- | 4 | 1000-9999 | R-3928 |
| change-request | CR- | 4 | 1000-9999 | CR-7291 |
| scenario | S- | 4 | 1000-9999 | S-4521 |
| acceptance-criterion | AC- | 4 | 1000-9999 | AC-2847 |
| test | T- | 4 | 1000-9999 | T-1029 |

**ID-Based Ordering:** IDs determine artifact priority numerically. Lower IDs = higher priority. When generating IDs for artifacts that should have specific priority relative to existing ones, consider the ID range carefully.

## Usage

### Script Location

```
${PLUGIN_ROOT}/skills/speclan-id-generator/scripts/generate-id.sh
```

### Command Line

```bash
./generate-id.sh <entity-type> [count] [speclan-dir]
```

**Arguments:**
- `entity-type` - Required. One of: `goal`, `feature`, `requirement`, `change-request`, `scenario`, `acceptance-criterion`, `test`
- `count` - Optional. Number of IDs to generate (default: 1)
- `speclan-dir` - Optional. Path to speclan directory (defaults to `./speclan`)

**Output:**
- Success: Prints unique ID(s) to stdout, one per line
- Failure: Prints error to stderr, exits with code 1

### Examples

```bash
# Generate a single feature ID
./generate-id.sh feature
# Output: F-1847

# Generate 5 requirement IDs at once
./generate-id.sh requirement 5
# Output:
# R-3928
# R-4521
# R-7832
# R-1293
# R-5647

# Generate 3 feature IDs with custom speclan path
./generate-id.sh feature 3 /path/to/project/speclan
# Output:
# F-1142
# F-2893
# F-5467

# Generate a change request ID
./generate-id.sh change-request
# Output: CR-7291
```

### In Commands/Agents

```bash
# Capture single ID
FEATURE_ID=$(./skills/speclan-id-generator/scripts/generate-id.sh feature speclan)
echo "Created feature: $FEATURE_ID"

# Generate multiple IDs at once (more efficient than multiple calls)
REQ_IDS=$(./generate-id.sh requirement 5 speclan)
echo "Created requirements:"
echo "$REQ_IDS"

# Parse multiple IDs into array
mapfile -t REQ_ARRAY <<< "$(./generate-id.sh requirement 3 speclan)"
echo "First: ${REQ_ARRAY[0]}, Second: ${REQ_ARRAY[1]}, Third: ${REQ_ARRAY[2]}"

# Or use read for bash 3.x compatibility
IFS=$'\n' read -d '' -r -a REQ_ARRAY <<< "$(./generate-id.sh requirement 3 speclan)" || true
```

### Session-Aware Collision Detection

When generating multiple IDs in a single call, the script tracks generated IDs within the session to ensure no duplicates, even before they're written to disk. This is more efficient than making multiple separate calls.

## Algorithm

The script implements a robust ID generation algorithm:

```
1. Parse entity type to get prefix, digit count, and range
2. For up to 100 attempts:
   a. Generate random number in range
   b. Format as ID (e.g., F-2934)
   c. Check for collisions:
      - Search filenames: find speclan -name "F-2934-*"
      - Search frontmatter: grep "^id: F-2934$"
   d. If no collision, return ID
3. If all attempts fail, exit with error
```

## Collision Detection

The script checks two locations for collisions:

### 1. Filename/Directory Collision

Searches for files or directories matching the ID pattern:
```bash
find "$speclan_dir" -name "${id}-*" -o -name "${id}.md"
```

This catches both directory-based and flat file entities:
- `F-2934-my-feature/` (feature directory)
- `R-4521-requirement/` (requirement directory)
- `G-142-goal.md` (flat goal file)
- `CR-1234-change.md` (flat change request file)

### 2. Frontmatter Collision

Searches for ID in YAML frontmatter:
```bash
grep -r "^id: ${id}$" "$speclan_dir"
```

This catches:
- Files that were renamed but kept the original ID
- IDs referenced but not yet written to files

## Inline Algorithm (For Commands)

If the script is not available, commands can use this inline algorithm:

```bash
# Generate unique Feature ID (4-digit)
generate_feature_id() {
  local speclan_dir="${1:-speclan}"
  local max_attempts=100

  for attempt in $(seq 1 $max_attempts); do
    # Generate random 4-digit number (1000-9999)
    local num=$((RANDOM % 9000 + 1000))
    local id="F-${num}"

    # Check for collisions
    if [ ! -d "$speclan_dir" ]; then
      echo "$id"
      return 0
    fi

    # Check filenames and frontmatter
    if ! find "$speclan_dir" -name "${id}-*" 2>/dev/null | grep -q . && \
       ! grep -r "^id: ${id}$" "$speclan_dir" 2>/dev/null | grep -q .; then
      echo "$id"
      return 0
    fi
  done

  echo "ERROR: Could not generate unique ID" >&2
  return 1
}

# Generate unique Requirement ID (4-digit)
generate_requirement_id() {
  local speclan_dir="${1:-speclan}"
  local max_attempts=100

  for attempt in $(seq 1 $max_attempts); do
    # Generate random 4-digit number (1000-9999)
    local num=$((RANDOM % 9000 + 1000))
    local id="R-${num}"

    if [ ! -d "$speclan_dir" ]; then
      echo "$id"
      return 0
    fi

    if ! find "$speclan_dir" -name "${id}-*" 2>/dev/null | grep -q . && \
       ! grep -r "^id: ${id}$" "$speclan_dir" 2>/dev/null | grep -q .; then
      echo "$id"
      return 0
    fi
  done

  echo "ERROR: Could not generate unique ID" >&2
  return 1
}

# Usage
FEATURE_ID=$(generate_feature_id speclan)
REQ_ID=$(generate_requirement_id speclan)
```

## Error Handling

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success - ID printed to stdout |
| 1 | Error - message printed to stderr |

**Common errors:**
- Invalid entity type
- Could not generate unique ID after 100 attempts (ID space exhausted)
- Missing required arguments

## Integration

### With `infer-from-codebase` Command

The command should use this skill for all ID generation:

```markdown
##### 3.4.4 Generate IDs

Use the `speclan-id-generator` skill:

\`\`\`bash
FEATURE_ID=$(./skills/speclan-id-generator/scripts/generate-id.sh feature speclan)
REQ_ID=$(./skills/speclan-id-generator/scripts/generate-id.sh requirement speclan)
\`\`\`
```

### With Agents

Agents should reference the inline algorithm from this skill when they need to suggest ID generation code.
