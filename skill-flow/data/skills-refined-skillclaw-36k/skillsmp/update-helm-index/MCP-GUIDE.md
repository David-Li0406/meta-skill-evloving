# MCP Tool Usage Guide

This guide explains how to use serena, context7, and sequential thinking MCP tools in the Helm index update workflow.

---

## Tool Selection Decision Tree

```
Start
  │
  ├─ Need to analyze codebase?
  │   └─ YES → Use serena
  │
  ├─ Need to query latest docs?
  │   └─ YES → Use context7
  │
  ├─ Encountering complex issues?
  │   └─ YES → Use sequential thinking
  │
  └─ Simple task → Use scripts directly
```

---

## serena - Semantic Codebase Analysis

serena provides powerful codebase search and analysis for understanding Chart structure and finding files.

### 1. List Directory Contents

**Scenario**: Check which Charts are available

```bash
# List charts/ directory (non-recursive)
mcp__serena__list_dir --relative_path "charts" --recursive false
```

**Output Example**:
```json
{
  "directories": ["subconverter", "booklore", "claude-relay-service"],
  "files": []
}
```

---

### 2. Find Chart.yaml Versions

**Scenario**: Check which Charts have version updates

```bash
# Find all Chart.yaml files
mcp__serena__find_file --file_mask "Chart.yaml" --relative_path "charts"

# Get symbol overview
mcp__serena__get_symbols_overview --relative_path "charts/subconverter/Chart.yaml"
```

---

### 3. Search .tgz Files

**Scenario**: Check existing packaged files

```bash
# Search all .tgz files
mcp__serena__search_for_pattern \
  --substring_pattern "\.tgz$" \
  --relative_path "." \
  --restrict_search_to_code_files false
```

**Output Example**:
```json
{
  "./subconverter-1.0.0.tgz": ["subconverter-1.0.0.tgz"],
  "./booklore-0.0.1.tgz": ["booklore-0.0.1.tgz"]
}
```

---

### 4. Verify Chart Structure

**Scenario**: Ensure Chart directory structure is correct

```bash
# Find all files in specific Chart
mcp__serena__find_file --file_mask "*" --relative_path "charts/subconverter"
```

---

## context7 - Latest Documentation

context7 provides up-to-date library documentation and examples for correct Helm commands and best practices.

### 1. Resolve Helm Library ID

**First, get Helm's library ID**:

```bash
mcp__plugin_context7_context7__resolve-library-id \
  --libraryName "helm" \
  --query "helm package command"
```

**Possible Output**:
- `/helm/helm`
- `/helm/helm/docs`

---

### 2. Query Helm Documentation

**Scenario**: Understand how to package Charts

```bash
mcp__plugin_context7_context7__query-docs \
  --libraryId "/helm/helm" \
  --query "How to package a chart and create a .tgz file?"
```

**Scenario**: Understand how to update repository index

```bash
mcp__plugin_context7_context7__query-docs \
  --libraryId "/helm/helm" \
  --query "How to update helm repository index.yaml?"
```

**Scenario**: Understand index file format

```bash
mcp__plugin_context7_context7__query-docs \
  --libraryId "/helm/helm" \
  --query "index.yaml file format and structure"
```

---

### 3. Query Best Practices

**Scenario**: Understand Chart versioning

```bash
mcp__plugin_context7_context7__query-docs \
  --libraryId "/helm/helm" \
  --query "Helm chart versioning best practices"
```

**Scenario**: Understand digest verification

```bash
mcp__plugin_context7_context7__query-docs \
  --libraryId "/helm/helm" \
  --query "How to verify chart package integrity with digest?"
```

---

## sequential thinking - Complex Decisions

sequential thinking handles complex problems, diagnoses errors, and plans strategies.

### 1. Plan Multi-Chart Update Strategy

**Scenario**: Need to update multiple Charts simultaneously

```markdown
Use sequential thinking to plan:
1. Analyze which Charts need updates
2. Determine update order (dependencies)
3. Plan verification steps
4. Prepare rollback strategy
```

**Actual Usage**:
```bash
mcp__sequential-thinking__sequentialthinking \
  --thought "Need to update 3 Charts: subconverter, booklore, claude-relay-service. Check dependencies between them." \
  --nextThoughtNeeded true \
  --thoughtNumber 1 \
  --totalThoughts 5
```

---

### 2. Diagnose Index Update Failures

**Scenario**: helm repo index command failed

```markdown
Use sequential thinking to analyze:
1. Check error messages
2. Analyze possible causes (permissions, YAML syntax, disk space)
3. Develop debugging steps
4. Verify fix
```

**Actual Usage**:
```bash
mcp__sequential-thinking__sequentialthinking \
  --thought "helm repo index failed with error: 'Error: no such file or directory'. Check current directory and .tgz file existence." \
  --nextThoughtNeeded true \
  --thoughtNumber 1 \
  --totalThoughts 4
```

---

### 3. Analyze Version Conflicts

**Scenario**: Chart version conflicts with existing packages

```markdown
Use sequential thinking to resolve:
1. Identify conflicting version numbers
2. Check if old versions can be overwritten
3. Decide to keep or delete old packages
4. Update index
```

---

## Remote Index Comparison

Compare local and published index.yaml to detect issues before publishing.

### Fetch Remote Index

```bash
# Download remote index.yaml
curl -s https://helm-chart.anubis.cafe/index.yaml -o /tmp/remote-index.yaml

# Check if remote is accessible
curl -s -o /dev/null -w "%{http_code}" https://helm-chart.anubis.cafe/index.yaml
# Should return: 200
```

### Compare Versions

```bash
# Compare local and remote indexes
diff -u index.yaml /tmp/remote-index.yaml

# Check specific chart versions
yq '.charts.booklore[].version' /tmp/remote-index.yaml
yq '.charts.booklore[].version' index.yaml
```

### Detect Conflicts

```bash
# Find versions only in remote
comm -23 <(yq '.charts[].[] | select(.name == "booklore") | .version' /tmp/remote-index.yaml | sort -u) \
          <(yq '.charts[].[] | select(.name == "booklore") | .version' index.yaml | sort -u)

# Find versions only in local
comm -13 <(yq '.charts[].[] | select(.name == "booklore") | .version' /tmp/remote-index.yaml | sort -u) \
          <(yq '.charts[].[] | select(.name == "booklore") | .version' index.yaml | sort -u)
```

---

## Integrated Workflow Example

### Complete MCP-Driven Update Process

```bash
# 1. Use serena to analyze codebase
mcp__serena__list_dir --relative_path "charts" --recursive false

# 2. Use serena to find version changes
mcp__serena__search_for_pattern \
  --substring_pattern "version:" \
  --relative_path "charts" \
  --restrict_search_to_code_files false

# 3. Fetch and compare with remote index
curl -s https://helm-chart.anubis.cafe/index.yaml -o /tmp/remote-index.yaml
diff -u index.yaml /tmp/remote-index.yaml || echo "Differences detected"

# 4. Use context7 to confirm correct commands
mcp__plugin_context7_context7__query-docs \
  --libraryId "/helm/helm" \
  --query "helm package command"

# 5. Execute packaging
helm package charts/*

# 6. Use context7 to confirm index command
mcp__plugin_context7_context7__query-docs \
  --libraryId "/helm/helm" \
  --query "update helm repository index"

# 7. Execute index update
helm repo index . --url https://helm-chart.anubis.cafe

# 8. Verify against remote
diff -u index.yaml /tmp/remote-index.yaml

# 9. If issues arise, use sequential thinking to diagnose
mcp__sequential-thinking__sequentialthinking \
  --thought "Verification step found issues, need to diagnose..." \
  --nextThoughtNeeded true \
  --thoughtNumber 1 \
  --totalThoughts 3
```

---

## Best Practices

### When to Use serena

- ✅ Need to understand codebase structure
- ✅ Find specific files or symbols
- ✅ Search for pattern matches
- ✅ Analyze Chart dependencies

### When to Use context7

- ✅ Uncertain about correct command syntax
- ✅ Need to understand best practices
- ✅ Query API documentation
- ✅ Get latest example code

### When to Use sequential thinking

- ✅ Encountering complex errors
- ✅ Need multi-step decision making
- ✅ Planning complex workflows
- ✅ Diagnosing system issues

### When to Check Remote Index

- ✅ Before publishing new versions
- ✅ Detecting version conflicts
- ✅ Verifying sync status
- ✅ Debugging published issues

### When to Use Scripts Directly

- ✅ Environment is known and stable
- ✅ Executing routine tasks
- ✅ Scripts already include required logic
- ✅ Need quick completion

---

## Troubleshooting

### Issue: serena Cannot Find Files

**Cause**: Incorrect path or file doesn't exist

**Solution**:
1. Use `mcp__serena__list_dir` to confirm directory structure
2. Check if relative path is correct
3. Verify files are not gitignored

---

### Issue: context7 Returns Empty Results

**Cause**: Incorrect libraryId or query doesn't match

**Solution**:
1. Use `resolve-library-id` first to get correct ID
2. Simplify query statement
3. Try different keywords

---

### Issue: sequential thinking Chain Too Long

**Cause**: Problem is too complex

**Solution**:
1. Break problem into smaller sub-problems
2. Use sequential thinking on each sub-problem separately
3. Synthesize results at the end

---

### Issue: Remote Index Not Accessible

**Cause**: Network issues or URL is wrong

**Solution**:
1. Check connectivity: `curl -I https://helm-chart.anubis.cafe/index.yaml`
2. Verify URL is correct
3. Check if remote repository is down

---

## Summary

- **serena**: Swiss army knife for codebase analysis
- **context7**: Treasure trove of latest documentation
- **sequential thinking**: Expert problem solver
- **Remote Index Check**: Guardian against version conflicts

Together, these tools build a powerful, intelligent, and reliable Helm index update workflow.
