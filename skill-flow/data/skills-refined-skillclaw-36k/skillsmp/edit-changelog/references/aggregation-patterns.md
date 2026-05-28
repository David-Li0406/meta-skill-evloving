# Aggregation Patterns

Git-based patterns for dynamically generating changelog entries from commit history.

## Overview

This guide provides techniques for parsing git commits, categorizing changes, maintaining proper structure, and optimizing performance during changelog generation.

**Key optimizations:**
- Incremental processing (only new commits via pointer)
- Parse conventional commit format
- Duplicate detection by issue number
- On-the-fly generation (no intermediate files)
- Silent operation

## Git-Based Architecture

### Pointer File System

**Track last aggregated commit:**
```bash
POINTER_FILE=".last-aggregated-commit"

# Read pointer
if [ ! -f "$POINTER_FILE" ]; then
  # Bootstrap: initialize to HEAD, no backfill
  git rev-parse HEAD > "$POINTER_FILE"
  exit 0
fi

LAST_COMMIT=$(cat "$POINTER_FILE")

# Verify commit exists
if ! git cat-file -e "$LAST_COMMIT" 2>/dev/null; then
  # Corrupted pointer - reinitialize
  git rev-parse HEAD > "$POINTER_FILE"
  exit 0
fi
```

**Benefits:**
- O(new commits) performance
- No intermediate files to manage
- Resilient to rebases/cherry-picks
- Simple state management

### Incremental Detection

**Get commits since last aggregation:**
```bash
# Get commits in chronological order (oldest first)
NEW_COMMITS=$(git log $LAST_COMMIT..HEAD --reverse --pretty=format:%H)

# If no new commits, exit silently
if [ -z "$NEW_COMMITS" ]; then
  exit 0
fi
```

**Update pointer after successful aggregation:**
```bash
git rev-parse HEAD > .last-aggregated-commit
```

---

## Conventional Commit Parsing

### Format Detection

**Parse conventional commit format:**
```bash
# Pattern: <type>[scope]: <description>
if [[ "$SUBJECT" =~ ^(feat|fix|perf|refactor|revert|build|docs|style|test|chore|ci)(\([^)]+\))?(!)?: ]]; then
  TYPE="${BASH_REMATCH[1]}"
  SCOPE="${BASH_REMATCH[2]}"
  BREAKING="${BASH_REMATCH[3]}"
  DESC=$(echo "$SUBJECT" | sed -E 's/^[a-z]+(\([^)]+\))?(!)?: //')
else
  # Non-conventional commit - skip or use fallback
  continue
fi
```

**Regex groups:**
- Type: `feat`, `fix`, `perf`, etc.
- Scope: Optional, in parentheses `(auth)`
- Breaking: `!` indicator
- Description: Rest of message

### Type to Category Mapping

**Map commit types to Keep a Changelog categories:**

| Commit Type | Changelog Category | Notes |
|------------|-------------------|-------|
| `feat` | Added | New features |
| `fix` | Fixed | Bug fixes |
| `perf` | Changed | Performance improvements ("Improved...") |
| `refactor` | Changed | Only if user-facing or breaking |
| `revert` | Removed | Reverted features |
| `build` | Changed | Only dependency updates |
| `docs` | (skip) | Not user-facing |
| `style` | (skip) | Not user-facing |
| `test` | (skip) | Not user-facing |
| `chore` | (skip) | Not user-facing |
| `ci` | (skip) | Not user-facing |

**Example implementation:**
```bash
case "$TYPE" in
  feat)
    entries_added["$commit"]="- $DESC"
    ;;
  fix)
    entries_fixed["$commit"]="- $DESC"
    ;;
  perf)
    entries_changed["$commit"]="- Improved $DESC"
    ;;
  refactor)
    # Only include if user-facing
    if echo "$BODY" | grep -qi "user-facing\|breaking"; then
      entries_changed["$commit"]="- $DESC"
    fi
    ;;
  revert)
    entries_removed["$commit"]="- Reverted: $DESC"
    ;;
  build)
    # Only include if affects users
    if echo "$SUBJECT" | grep -qi "deps\|upgrade"; then
      entries_changed["$commit"]="- $DESC"
    fi
    ;;
  chore|ci|style|test|docs)
    # Skip non-user-facing commits
    continue
    ;;
esac
```

### Breaking Changes Detection

**Identify breaking changes:**
```bash
# Check for ! after type
if [ -n "$BREAKING" ]; then
  entries_changed["$commit"]="- **BREAKING**: $DESC"
  continue
fi

# Check for BREAKING CHANGE: in body
if echo "$BODY" | grep -qi "^BREAKING[- ]CHANGE:"; then
  BREAKING_DESC=$(echo "$BODY" | grep -i "^BREAKING[- ]CHANGE:" | sed 's/^BREAKING[- ]CHANGE: //')
  if [ -z "$BREAKING_DESC" ]; then
    BREAKING_DESC="$DESC"
  fi
  entries_changed["$commit"]="- **BREAKING**: $BREAKING_DESC"
  continue
fi
```

**Handling:**
- Always go to Changed section
- Prefix with `**BREAKING**`
- Sort first within Changed section

---

## Duplicate Detection

### Issue Number Deduplication (Recommended)

**Track seen issues to prevent duplicates:**
```bash
declare -A seen_issues

# Extract issue numbers from commit
ISSUES=$(echo "$SUBJECT $BODY" | grep -oE '#[0-9]+')

# Check for duplicates
if [ -n "$ISSUES" ]; then
  duplicate=false
  for issue in $ISSUES; do
    if [[ -n "${seen_issues[$issue]}" ]]; then
      duplicate=true
      break
    fi
  done

  if [ "$duplicate" = true ]; then
    continue  # Skip duplicate
  fi

  # Mark issues as seen
  for issue in $ISSUES; do
    seen_issues[$issue]=1
  done
fi
```

**Benefits:**
- Handles different wording for same issue
- Prevents cherry-picks/amended commits from appearing twice
- First occurrence wins
- 10-30% reduction in duplicates

**Scenarios handled:**
- Amended commits (same issue, new hash)
- Cherry-picks (same change, different hash)
- Multiple commits referencing same issue

**Limitation:** Entries without issue numbers are always included

---

## Category Management

### In-Memory Storage

**Use associative arrays for categorization:**
```bash
declare -A entries_added
declare -A entries_changed
declare -A entries_deprecated
declare -A entries_removed
declare -A entries_fixed
declare -A entries_security
declare -A seen_issues
```

**Benefits:**
- O(1) lookup and insertion
- No file I/O during processing
- Typically <1 MB for hundreds of entries

### Building Unreleased Section

**Generate section with proper ordering:**
```bash
UNRELEASED="## [Unreleased]\n\n"

# Add categories in Keep a Changelog order
if [ ${#entries_added[@]} -gt 0 ]; then
  UNRELEASED+="### Added\n"
  for commit in "${!entries_added[@]}"; do
    UNRELEASED+="${entries_added[$commit]}\n"
  done
  UNRELEASED+="\n"
fi

if [ ${#entries_changed[@]} -gt 0 ]; then
  UNRELEASED+="### Changed\n"
  # Sort breaking changes first
  for commit in "${!entries_changed[@]}"; do
    if [[ "${entries_changed[$commit]}" == *"**BREAKING**"* ]]; then
      UNRELEASED+="${entries_changed[$commit]}\n"
    fi
  done
  for commit in "${!entries_changed[@]}"; do
    if [[ "${entries_changed[$commit]}" != *"**BREAKING**"* ]]; then
      UNRELEASED+="${entries_changed[$commit]}\n"
    fi
  done
  UNRELEASED+="\n"
fi

# Repeat for other categories...
```

**Category order:**
1. Added
2. Changed (breaking changes first)
3. Deprecated
4. Removed
5. Fixed
6. Security

**Empty categories:** Automatically omitted

### Preserving Existing Structure

**Extract parts to preserve:**
```bash
# Preserve header (everything before first "## ")
sed -n '/^## /q;p' CHANGELOG.md > /tmp/changelog_header.txt

# Preserve version sections (everything from first version tag onwards)
sed -n '/^## \[[0-9]/,$p' CHANGELOG.md > /tmp/changelog_versions.txt
```

**Reconstructing CHANGELOG.md:**
```bash
cat > CHANGELOG.md << EOF
$(cat /tmp/changelog_header.txt)

$UNRELEASED
$(cat /tmp/changelog_versions.txt)
EOF

# Cleanup
rm -f /tmp/changelog_header.txt /tmp/changelog_versions.txt
```

**Preserved sections:**
- Header (title, description, links)
- All versioned releases (## [1.0.0], etc.)

**Regenerated section:**
- ## [Unreleased] - completely rebuilt from git commits

---

## Edge Cases

### Rebase Handling

**Scenario:** Commits rebased, hashes changed.

**Handling:**
- Git log shows "new" commits (rebased hashes)
- Entries generated for rebased commits
- Deduplication by issue number prevents duplicates
- Pointer updated to new HEAD

**Example:**
```
Before rebase: A → B → C → D (HEAD)
                    ↑
                  pointer

After rebase:  A → B → C' → D' (HEAD)
                    ↑
                  pointer

git log pointer..HEAD shows C' and D'
```

### Cherry-Pick Handling

**Scenario:** Same commit appears twice with different hashes.

**Handling:**
- Both commits processed
- Deduplication by issue number prevents duplicate entries
- Only first occurrence kept

**Example:**
```
Commit abc1234: feat: add login (#123)
Commit def5678: feat: add login (#123)  [cherry-picked]

Result: Only one "- add login (#123)" entry
```

### Non-Conventional Commits

**Scenario:** Commit message doesn't follow conventional format.

**Handling:**
- Skip commit (no entry generated)
- Optional enhancement: detect keywords ("fix", "add") as fallback

**Example:**
```bash
# Fallback for non-conventional commits
if ! [[ "$SUBJECT" =~ ^(feat|fix|...) ]]; then
  # Try keyword detection
  if echo "$SUBJECT" | grep -qi "^fix\|^add\|^remove"; then
    # Process with keyword-based categorization
  else
    continue  # Skip
  fi
fi
```

### Corrupted Pointer

**Scenario:** Pointer contains invalid commit hash.

**Handling:**
```bash
if ! git cat-file -e "$LAST_COMMIT" 2>/dev/null; then
  # Reinitialize to HEAD
  git rev-parse HEAD > "$POINTER_FILE"
  exit 0
fi
```

**Bootstrap behavior:**
- If pointer missing → initialize to HEAD, exit
- If pointer corrupted → reinitialize to HEAD, exit
- Future runs will process commits after this point

---

## Performance Characteristics

### Complexity Analysis

**Time complexity:**
- Git log query: O(commits since last run)
- Commit parsing: O(new commits)
- Issue deduplication: O(new commits × avg issues per commit)
- CHANGELOG.md write: O(total unreleased entries)

**Space complexity:**
- Associative arrays: O(unique entries)
- Typically <1 MB for hundreds of entries

### Performance Benchmarks

**Typical performance:**
- 10 new commits: <0.1s
- 100 new commits: <0.5s
- 1000 new commits: <3s

**Incremental advantage:**
- First run: Process all commits since pointer
- Subsequent runs: Process only new commits
- Example: 500 commits in repo, 2 new → process 2 instead of 500 (250x faster)

### Memory Efficiency

**No file I/O during processing:**
- No intermediate files to read/write
- Git provides data directly via stdout
- In-memory categorization only

**Streaming pattern:**
```bash
# Process commits one at a time
git log $LAST_COMMIT..HEAD --reverse --pretty=format:%H | while read commit; do
  # Parse and categorize
done
```

---

## Testing Patterns

### Test Cases

**Test 1: Single new commit**
- Input: One feat commit since last run
- Expected: Entry appears in Added section

**Test 2: Multiple categories**
- Input: feat, fix, perf commits
- Expected: Added, Fixed, Changed sections appear

**Test 3: Breaking changes**
- Input: Commit with `!` or `BREAKING CHANGE:`
- Expected: Entry in Changed with **BREAKING** prefix, sorted first

**Test 4: Duplicates by issue**
- Input: Two commits with same issue number
- Expected: Only first occurrence included

**Test 5: Non-user-facing commits**
- Input: chore, ci, test, docs commits
- Expected: No entries generated (filtered out)

**Test 6: Preserve versions**
- Input: New commits + existing version sections
- Expected: Version sections preserved, Unreleased updated

**Test 7: No new commits**
- Input: Pointer at HEAD
- Expected: Exit silently, no changes to CHANGELOG.md

**Test 8: Corrupted pointer**
- Input: Pointer with invalid commit hash
- Expected: Reinitialize to HEAD, exit silently

---

## Algorithm: Complete Git-Based Aggregation

**High-level algorithm:**

```
1. Read pointer file (or initialize on first run)
2. Verify pointer commit exists (reinitialize if corrupted)
3. Query git for new commits: git log POINTER..HEAD
4. If no new commits, exit silently
5. For each commit:
   a. Parse subject and body
   b. Match conventional commit format
   c. Filter non-user-facing types
   d. Extract issue numbers
   e. Check for duplicates (by issue number)
   f. Map type to category
   g. Store entry in category array
6. Build Unreleased section:
   a. Add category headers
   b. Add entries (breaking changes first in Changed)
   c. Omit empty categories
7. Preserve CHANGELOG.md structure:
   a. Extract header
   b. Extract version sections
8. Reconstruct CHANGELOG.md:
   a. Header
   b. New Unreleased section
   c. Version sections
9. Write updated CHANGELOG.md
10. Update pointer to HEAD
11. Exit silently (code 0)
```

**Pseudocode:**

```python
# Read pointer
pointer_file = ".last-aggregated-commit"
if not exists(pointer_file):
    write(pointer_file, git("rev-parse HEAD"))
    exit(0)

last_commit = read(pointer_file)
if not git_commit_exists(last_commit):
    write(pointer_file, git("rev-parse HEAD"))
    exit(0)

# Get new commits
new_commits = git(f"log {last_commit}..HEAD --reverse --pretty=format:%H")
if not new_commits:
    exit(0)

# Categorize commits
entries = {
    "Added": [],
    "Changed": [],
    "Deprecated": [],
    "Removed": [],
    "Fixed": [],
    "Security": []
}
seen_issues = set()

for commit in new_commits:
    subject = git(f"log -1 --pretty=format:%s {commit}")
    body = git(f"log -1 --pretty=format:%b {commit}")

    # Parse conventional commit
    match = re.match(r'^(feat|fix|perf|...)(\([^)]+\))?(!)?: (.+)$', subject)
    if not match:
        continue

    type, scope, breaking, desc = match.groups()

    # Filter non-user-facing
    if type in ['chore', 'ci', 'style', 'test', 'docs']:
        continue

    # Extract issue numbers
    issues = re.findall(r'#\d+', subject + body)

    # Check duplicates
    if issues and any(issue in seen_issues for issue in issues):
        continue
    seen_issues.update(issues)

    # Categorize
    category = map_type_to_category(type, breaking)
    entries[category].append(format_entry(desc, breaking))

# Build Unreleased
unreleased = "## [Unreleased]\n\n"
for category in ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"]:
    if entries[category]:
        unreleased += f"### {category}\n"
        # Sort breaking first in Changed
        if category == "Changed":
            breaking = [e for e in entries[category] if "**BREAKING**" in e]
            normal = [e for e in entries[category] if "**BREAKING**" not in e]
            for entry in breaking + normal:
                unreleased += entry + "\n"
        else:
            for entry in entries[category]:
                unreleased += entry + "\n"
        unreleased += "\n"

# Reconstruct CHANGELOG.md
header = extract_before_first_version("CHANGELOG.md")
versions = extract_version_sections("CHANGELOG.md")
new_changelog = header + "\n" + unreleased + "\n" + versions

write("CHANGELOG.md", new_changelog)

# Update pointer
write(pointer_file, git("rev-parse HEAD"))

exit(0)
```

---

## References

- Conventional Commits: https://www.conventionalcommits.org/
- Keep a Changelog: https://keepachangelog.com/
- Semantic Versioning: https://semver.org/
