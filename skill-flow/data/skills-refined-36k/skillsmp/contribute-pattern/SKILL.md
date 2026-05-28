---
name: contribute-pattern
description: Share a project learning as a universal pattern to the plugin repository
argument-hint: "[path to learning file OR leave empty to select]"
model: claude-sonnet-4-5
context: fork
agent: general-purpose
allowed-tools:
  - Bash(*)
  - Read
  - Write
  - Grep
  - Glob
extended-thinking: true
---

# Pattern Contribution Command

You help developers share valuable learnings with the broader community by contributing universal patterns to the plugin repository.

**Target:** $ARGUMENTS

## Workflow

### Phase 1: Learning Selection

```bash
# Check for project learnings
echo "=== Project Learnings Available ==="
LEARNINGS_DIR="./docs/learnings"

if [ ! -d "$LEARNINGS_DIR" ]; then
  echo "No learnings directory found at $LEARNINGS_DIR"
  echo "Run /compound first to capture learnings."
  exit 0
fi

# List available learnings
find "$LEARNINGS_DIR" -name "*.md" -type f | while read file; do
  # Extract title and applicable_to from frontmatter
  TITLE=$(grep "^title:" "$file" 2>/dev/null | cut -d: -f2- | xargs)
  APPLICABLE=$(grep "^applicable_to:" "$file" 2>/dev/null | cut -d: -f2- | xargs)

  if [ "$APPLICABLE" = "universal" ]; then
    echo "✅ [UNIVERSAL] $file"
    echo "   Title: $TITLE"
  else
    echo "⚪ [PROJECT] $file"
    echo "   Title: $TITLE"
  fi
done
```

If $ARGUMENTS provided, use that file. Otherwise, prompt user to select from universal learnings.

### Phase 2: Validate Learning

Read the selected learning file and validate:

```markdown
### Validation Checklist

**Structure:**
- [ ] Has valid YAML frontmatter
- [ ] Has title, category, tags, severity, date
- [ ] Has Summary section
- [ ] Has Problem section
- [ ] Has Solution section

**Universality:**
- [ ] Does NOT reference project-specific code paths
- [ ] Does NOT contain sensitive information
- [ ] Applies to common frameworks/tools
- [ ] Solution is generalizable

**Quality:**
- [ ] Clear problem description
- [ ] Actionable solution
- [ ] Includes prevention steps
```

### Phase 3: Prepare Contribution

Transform the learning for plugin contribution:

```bash
# Generate pattern filename
CATEGORY=$(grep "^category:" "$LEARNING_FILE" | cut -d: -f2- | xargs)
TITLE_SLUG=$(grep "^title:" "$LEARNING_FILE" | cut -d: -f2- | xargs | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | cut -c1-50)
PATTERN_FILENAME="${CATEGORY}/${TITLE_SLUG}.md"

echo "=== Pattern Contribution Details ==="
echo "Source: $LEARNING_FILE"
echo "Target: docs/patterns/$PATTERN_FILENAME"
echo "Category: $CATEGORY"
```

### Phase 4: Create Pull Request

```bash
# Check if user has access to plugin repo
PLUGIN_REPO="psd401/psd-claude-coding-system"

echo "=== Checking Repository Access ==="
gh repo view "$PLUGIN_REPO" --json nameWithOwner > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "Cannot access $PLUGIN_REPO"
  echo ""
  echo "To contribute patterns, you need:"
  echo "1. Fork the repository: gh repo fork $PLUGIN_REPO"
  echo "2. Run this command again"
  exit 1
fi

# Fork if needed
FORK_EXISTS=$(gh repo list --fork --json nameWithOwner --jq '.[].nameWithOwner' | grep "psd-claude-coding-system")
if [ -z "$FORK_EXISTS" ]; then
  echo "Forking repository..."
  gh repo fork "$PLUGIN_REPO" --clone=false
fi

# Get fork URL
FORK_URL=$(gh repo list --fork --json nameWithOwner,url --jq '.[] | select(.nameWithOwner | contains("psd-claude-coding-system")) | .url')

# Clone fork to temp directory
TEMP_DIR=$(mktemp -d)
echo "Cloning fork to $TEMP_DIR"
git clone "$FORK_URL" "$TEMP_DIR/plugin"
cd "$TEMP_DIR/plugin"

# Create branch
BRANCH_NAME="pattern/contribute-${TITLE_SLUG}"
git checkout -b "$BRANCH_NAME"

# Copy pattern file
mkdir -p "plugins/psd-claude-coding-system/docs/patterns/$CATEGORY"
cp "$LEARNING_FILE" "plugins/psd-claude-coding-system/docs/patterns/$PATTERN_FILENAME"

# Update applicable_to to universal
sed -i '' 's/applicable_to: project/applicable_to: universal/' "plugins/psd-claude-coding-system/docs/patterns/$PATTERN_FILENAME"

# Commit
git add .
git commit -m "docs: Add pattern - $TITLE

Category: $CATEGORY
Source: Project learning contribution

This pattern was contributed from a project learning that
proved valuable enough to share with the community."

# Push and create PR
git push origin "$BRANCH_NAME"

gh pr create \
  --repo "$PLUGIN_REPO" \
  --base main \
  --head "$BRANCH_NAME" \
  --title "docs: Add pattern - $TITLE" \
  --body "## Pattern Contribution

### Summary
$SUMMARY

### Category
$CATEGORY

### Validation
- [x] Universal applicability verified
- [x] No project-specific references
- [x] Clear problem and solution

### Source
Contributed from project learning that proved valuable.

---
*Contributed via /contribute-pattern command*"

# Cleanup
cd -
rm -rf "$TEMP_DIR"

echo ""
echo "✅ Pattern contribution PR created!"
echo "The plugin maintainers will review and merge if appropriate."
```

## Output Format

```markdown
## 📤 Pattern Contribution

**Learning:** [Title]
**Category:** [Category]
**Status:** [PR Created / Validation Failed / No Access]

### Validation Results
- Structure: ✅ Valid
- Universality: ✅ Verified
- Quality: ✅ Acceptable

### Pull Request
- **URL:** [PR URL]
- **Status:** Open, awaiting review

### Next Steps
- Wait for maintainer review
- Address any feedback if requested
- Pattern will be available to all users after merge
```

## Contribution Guidelines

### What Makes a Good Universal Pattern

1. **Applies to Common Tools**
   - Popular frameworks (React, Django, Rails, etc.)
   - Standard libraries
   - Common development workflows

2. **Solves a Non-Obvious Problem**
   - Not easily found in documentation
   - Counter-intuitive behavior
   - Edge case that causes production issues

3. **Has Clear Prevention Steps**
   - How to detect the issue early
   - Configuration or tooling recommendations
   - Testing strategies

### What Should NOT Be Contributed

- Project-specific configurations
- Proprietary business logic
- Patterns containing sensitive information
- Issues specific to outdated library versions
- Extremely niche use cases

## Success Criteria

- ✅ Learning validated for universality
- ✅ Pattern properly formatted
- ✅ PR created successfully
- ✅ No sensitive information included

Remember: Shared knowledge benefits everyone. Quality patterns help developers avoid common pitfalls.
