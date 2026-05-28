---
name: claude-code-updates
description: Analyze Claude Code releases and recommend plugin improvements
argument-hint: "[optional: version-range e.g. \"2.1.0-2.1.15\"]"
model: claude-opus-4-5-20251101
context: fork
agent: Explore
allowed-tools:
  - WebFetch
  - WebSearch
  - Read
  - Grep
  - Glob
extended-thinking: true
---

# Claude Code Updates Analyzer

Analyze recent Claude Code releases and identify improvements for this plugin.

**Version Range:** $ARGUMENTS (or latest if empty)

## Workflow

### Phase 1: Gather Current Plugin State

```bash
# Get current plugin version
PLUGIN_DIR="$(dirname "$(dirname "$0")")"
echo "=== Current Plugin State ==="
cat "$PLUGIN_DIR/.claude-plugin/plugin.json" 2>/dev/null || echo "Plugin JSON not found"

# Count current structure
echo -e "\n=== Structure Counts ==="
echo "Commands: $(find "$PLUGIN_DIR/commands" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')"
echo "Skills: $(find "$PLUGIN_DIR/skills" -type d -mindepth 1 2>/dev/null | wc -l | tr -d ' ')"
echo "Agents: $(find "$PLUGIN_DIR/agents" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')"

# Sample frontmatter patterns
echo -e "\n=== Frontmatter Patterns ==="
head -10 "$PLUGIN_DIR/commands/work.md" 2>/dev/null | grep -E "^[a-z-]+:" || true
```

### Phase 2: Fetch Claude Code Changelog

Use WebFetch to retrieve the Claude Code changelog:

**Primary Source:** https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md

**Fallback Sources:**
- https://docs.anthropic.com/claude-code/changelog
- https://www.anthropic.com/news (filter for Claude Code)

**Focus Areas for Analysis:**
1. **Skills/Commands Architecture**
   - New frontmatter fields
   - Skills directory structure changes
   - Command deprecations
   - `context: fork` and `agent` field support

2. **Hooks System**
   - New hook events
   - Per-skill hooks in frontmatter
   - Hook parameter changes

3. **Tool Permissions**
   - `allowed-tools` syntax changes
   - New tools available
   - Permission model updates

4. **Model Updates**
   - New model IDs available
   - Model deprecations
   - Extended thinking changes

5. **Breaking Changes**
   - API changes
   - Configuration format changes
   - Plugin structure requirements

### Phase 3: Analyze Plugin Compatibility

For each relevant change found:

1. **Check if plugin implements the feature**
   ```bash
   # Example: Check for context: fork usage
   grep -r "context: fork" "$PLUGIN_DIR" || echo "Not using context: fork"

   # Check for new frontmatter fields
   grep -r "agent:" "$PLUGIN_DIR/commands" || echo "Not using agent field"
   ```

2. **Identify gaps between Claude Code features and plugin**

3. **Assess migration effort**
   - Trivial: Single-line changes
   - Medium: Multiple files, same pattern
   - Complex: Architecture changes

### Phase 4: Generate Improvement Report

## Output Format

Produce a structured report with the following sections:

```markdown
# Claude Code Updates Analysis

**Plugin Version:** [current]
**Claude Code Version Analyzed:** [from changelog]
**Analysis Date:** [today]

## Release Summary

| Version | Release Date | Relevant Changes |
|---------|--------------|------------------|
| X.Y.Z   | YYYY-MM-DD   | Brief description |

## Required Actions (Breaking Changes)

| Priority | Change | Files Affected | Complexity | Migration Steps |
|----------|--------|----------------|------------|-----------------|
| CRITICAL | ...    | N files        | Trivial/Medium/Complex | Steps |

## Recommended Improvements (New Features)

### 1. [Feature Name]
- **Claude Code Version:** X.Y.Z
- **Benefit:** Why adopt this
- **Files to Modify:** List
- **Implementation Notes:** How to adopt

### 2. [Feature Name]
...

## Deprecation Warnings

| Deprecated | Replacement | Deadline | Action Required |
|------------|-------------|----------|-----------------|
| feature    | new_feature | version  | What to do |

## Plugin Health Score

- Commands using latest patterns: X/Y (Z%)
- Agents with all recommended fields: X/Y (Z%)
- Skills using new features: X/Y (Z%)
- Hooks coverage: X/Y events

## Recommended Next Steps

1. [Highest priority action]
2. [Second priority]
3. [Third priority]
```

## Success Criteria

- Fetched and analyzed Claude Code changelog
- Identified all breaking changes affecting plugin
- Listed actionable improvements with complexity ratings
- Produced structured report for decision-making

## Notes

- This skill is **manual-only** - run when planning plugin updates
- WebSearch used as fallback if changelog URL changes
- Focus on actionable insights, not comprehensive history
- Recommend batching related changes for efficiency
