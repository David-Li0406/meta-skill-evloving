# Update Helm Index - Detailed Workflow

This document provides detailed execution steps, MCP tool integration, scenarios, and best practices for updating Helm Chart repository index.

---

## Use Automation Scripts

This skill provides automation scripts to simplify the workflow:

### 1. Environment Check Script
```bash
bash .claude/skills/update-helm-index/scripts/check-env.sh
```

Verifies all prerequisites, including Helm version, Git configuration, directory permissions, etc.

### 2. One-Click Update Script
```bash
# Preview mode (recommended for first use)
bash .claude/skills/update-helm-index/scripts/update-index.sh --dry-run

# Execute update
bash .claude/skills/update-helm-index/scripts/update-index.sh

# Auto-push to remote
bash .claude/skills/update-helm-index/scripts/update-index.sh --auto-push
```

Automates the complete workflow: packaging, index update, verification, and Git commit.

### 3. Health Check Script
```bash
bash .claude/skills/update-helm-index/scripts/health-check.sh
```

Periodically verify repository integrity, check digest, YAML syntax, etc.

See [scripts/README.md](scripts/README.md) for detailed script documentation.

---

## MCP-Driven Workflow

Example of a complete workflow enhanced with MCP tools:

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

# 9. Verify results
bash scripts/health-check.sh
```

---

## Complete Execution Flow

### Step 1: Verify Environment

**Quick check with script:**
```bash
bash .claude/skills/update-helm-index/scripts/check-env.sh
```

**MCP Tool Recommendations:**

Use serena to verify codebase structure:
```bash
# List charts directory
mcp__serena__list_dir --relative_path "charts" --recursive false
```

Use context7 to query latest Helm version requirements:
```bash
mcp__plugin_context7_context7__query-docs \
  --libraryId "/helm/helm" \
  --query "minimum helm version required"
```

**Manual Check Items:**
- ✅ Helm >= 3.0.0
- ✅ Git user info configured
- ✅ Directory write permissions
- ✅ Existing .tgz file status

---

### Step 2: Analyze Chart State

**Check existing .tgz package files:**

```bash
ls -lh *.tgz
```

**Expected Output:**
```
-rw-r--r-- 1 user user 15K Jan 10 10:30 subconverter-1.0.0.tgz
-rw-r--r-- 1 user user 12K Jan  8 15:20 claude-relay-service-0.1.0.tgz
```

**MCP Tool Recommendations:**

Use serena to find all Chart.yaml files and analyze versions:
```bash
# Find all Chart.yaml
mcp__serena__find_file --file_mask "Chart.yaml" --relative_path "charts"

# Search for existing .tgz files
mcp__serena__search_for_pattern \
  --substring_pattern "\.tgz$" \
  --relative_path "." \
  --restrict_search_to_code_files false
```

Use sequential thinking to plan update strategy (multi-chart scenario):
```bash
mcp__sequential-thinking__sequentialthinking \
  --thought "Found 3 Charts needing updates. Analyze dependencies between them to determine update order." \
  --nextThoughtNeeded true \
  --thoughtNumber 1 \
  --totalThoughts 3
```

**Verification Points:**
- ✅ Confirm new version packages exist
- ✅ Check file size and modification time
- ✅ Identify old version packages to delete

---

### Step 3: Check Remote Index (NEW)

**Before publishing, compare with remote repository:**

```bash
# Fetch remote index.yaml
curl -s https://helm-chart.anubis.cafe/index.yaml -o /tmp/remote-index.yaml

# Check if remote is accessible
curl -s -o /dev/null -w "%{http_code}" https://helm-chart.anubis.cafe/index.yaml
# Should return: 200

# Compare local and remote
diff -u index.yaml /tmp/remote-index.yaml

# Check specific chart versions in remote
yq '.charts.booklore[].version' /tmp/remote-index.yaml
```

**Why Check Remote Index:**
- Detect version conflicts before publishing
- Verify sync status
- Identify orphaned entries
- Avoid duplicate version issues

**MCP Tool Recommendations:**

Use sequential thinking to analyze version conflicts:
```bash
mcp__sequential-thinking__sequentialthinking \
  --thought "Remote index has booklore-0.2.2 but local only has 0.0.1. This indicates version rollback or missing package files." \
  --nextThoughtNeeded true \
  --thoughtNumber 1 \
  --totalThoughts 3
```

---

### Step 4: Package Charts

If Chart source has updates (Chart.yaml, templates, values, etc.), package first:

```bash
# Package all Charts
helm package charts/*

# Or package specific Charts
helm package charts/subconverter
helm package charts/claude-relay-service
```

**MCP Tool Recommendations:**

Use context7 to query packaging best practices:
```bash
mcp__plugin_context7_context7__query-docs \
  --libraryId "/helm/helm" \
  --query "helm package command best practices and validation"
```

Use serena to verify Chart structure:
```bash
# Get Chart structure overview
mcp__serena__get_symbols_overview --relative_path "charts/subconverter/Chart.yaml"
```

**Purpose:**
- Package Chart directory into .tgz file
- Automatically verify Chart structure
- Generate publishable compressed package

**Expected Output:**
```
Successfully packaged chart and saved it to:
subconverter-1.0.0.tgz
```

**Verify packaging result:**
```bash
# Verify package format
helm lint subconverter-1.0.0.tgz

# View package contents
tar -tzf subconverter-1.0.0.tgz | head -20
```

---

### Step 5: Regenerate Helm Repository Index

Use Helm CLI to regenerate index.yaml:

```bash
helm repo index . --url https://helm-chart.anubis.cafe
```

**MCP Tool Recommendations:**

Use context7 to understand index file format:
```bash
mcp__plugin_context7_context7__query-docs \
  --libraryId "/helm/helm" \
  --query "index.yaml file format and digest calculation"
```

Use serena to search for old index files:
```bash
mcp__serena__search_for_pattern \
  --substring_pattern "^index:" \
  --relative_path "." \
  --restrict_search_to_code_files false
```

**Purpose:**
- Scan all .tgz files in directory
- Automatically calculate SHA256 digest for each package
- Update all chart entries in index.yaml
- Ensure index.yaml matches actual .tgz files

**Parameter Description:**
- `.` - Current directory (Helm repository root)
- `--url` - Public access URL of Helm repository
  - This project uses: `https://helm-chart.anubis.cafe`
  - Adjust according to actual deployment environment

**Expected Output:**
```
Index file created successfully
```

---

### Step 6: Verify Index Update

Check if index.yaml is correctly updated:

```bash
# View specific chart index
grep -A 20 "subconverter:" index.yaml
```

**Expected Output:**
```yaml
subconverter:
  - name: subconverter
    created: 2025-01-10T10:30:00Z
    description: A subscription converter
    digest: a1b2c3d4e5f6...
    home: https://github.com/example/subconverter
    icon: https://example.com/icon.png
    urls:
      - https://helm-chart.anubis.cafe/subconverter-1.0.0.tgz
    version: 1.0.0
    annotations:
      artifacthub.io/changes: |
        - Update to v1.0.0
        - Fix bug in ...
```

**MCP Tool Recommendations:**

Use serena to verify index file:
```bash
# Read index.yaml structure
mcp__serena__get_symbols_overview --relative_path "index.yaml"
```

Use sequential thinking to diagnose verification issues:
```bash
mcp__sequential-thinking__sequentialthinking \
  --thought "Verification found digest mismatch. Analyze possible causes: .tgz file corrupted or index generation error." \
  --nextThoughtNeeded true \
  --thoughtNumber 1 \
  --totalThoughts 3
```

**Verify Against Remote:**
```bash
# Compare new local index with remote
diff -u /tmp/remote-index.yaml index.yaml

# Check if new version appears
yq '.charts.subconverter[].version' index.yaml
```

**Verification Checklist:**
- [ ] Version number correctly updated
- [ ] URL points to correct .tgz file
- [ ] Timestamp is current
- [ ] Digest value recalculated
- [ ] Description and metadata correct

**Use health check script:**
```bash
bash .claude/skills/update-helm-index/scripts/health-check.sh
```

---

### Step 7: Git Commit Update

Commit updated files to Git:

```bash
# Add updated files
git add *.tgz index.yaml

# Check status
git status

# Commit changes
git commit -m "chore: update subconverter to v1.0.0 and refresh Helm index

- Update subconverter Chart from 0.2.0 to 1.0.0
- Add new feature: support multiple subscriptions
- Fix: fix config file parsing error
- Regenerate index.yaml to reflect latest .tgz packages"
```

**MCP Tool Recommendations:**

Use serena to find files referencing Chart (if documentation needs update):
```bash
# Find files referencing old version
mcp__serena__search_for_pattern \
  --substring_pattern "0.2.0" \
  --relative_path "." \
  --restrict_search_to_code_files false
```

**Commit files include:**
- New .tgz package files
- Updated index.yaml
- Possibly other modified .tgz files

**Commit message template:**
```
chore: update [chart-name] to v[version] and refresh Helm index

- Update [chart-name] Chart from [old-version] to [new-version]
- [Main change description]
- Regenerate index.yaml to reflect latest .tgz packages
```

---

### Step 8: Push to Remote Repository (Optional)

```bash
git push
```

**⚠️ Note:** Be cautious with this step, confirm everything is correct before pushing.

---

## Common Scenarios

### Scenario 1: Publish New Chart Version

**Situation:** Developed new version features, need to publish

**Workflow:**

1. Update version number in `charts/subconverter/Chart.yaml`
   ```yaml
   version: 1.0.0  # Update from 0.2.0
   ```
2. Update Chart templates, values, and other files

3. **Check remote index first:**
   ```bash
   curl -s https://helm-chart.anubis.cafe/index.yaml -o /tmp/remote-index.yaml
   yq '.charts.subconverter[].version' /tmp/remote-index.yaml
   ```

4. **Use MCP tools to verify:**
   ```bash
   # Use serena to find all files needing update
   mcp__serena__find_referencing_symbols \
     --name_path "Chart.yaml/version" \
     --relative_path "charts/subconverter"
   ```

5. Package new version:
   ```bash
   helm package charts/subconverter
   ```

6. Run complete workflow to update index

7. Push to Git repository

**Verify:**
```bash
helm search repo anubis/subconverter --versions
```

---

### Scenario 2: Index Out of Sync

**Situation:** Periodic maintenance, check if index is current

**Workflow:**

1. **Fetch and compare with remote:**
   ```bash
   curl -s https://helm-chart.anubis.cafe/index.yaml -o /tmp/remote-index.yaml
   diff -u index.yaml /tmp/remote-index.yaml
   ```

2. **Use serena to analyze index status:**
   ```bash
   # Search for .tgz files
   mcp__serena__search_for_pattern \
     --substring_pattern "\.tgz$" \
     --relative_path "." \
     --restrict_search_to_code_files false

   # Read index.yaml
   mcp__serena__get_symbols_overview --relative_path "index.yaml"
   ```

3. **Use sequential thinking to compare versions:**
   ```bash
   mcp__sequential-thinking__sequentialthinking \
     --thought "Comparing .tgz file list and versions in index.yaml. Found booklore-0.2.2.tgz exists but not recorded in index." \
     --nextThoughtNeeded true \
     --thoughtNumber 1 \
     --totalThoughts 2
   ```

4. If mismatch found, run this skill's complete workflow

5. Verify update results

---

### Scenario 3: Multi-Chart Update

**Situation:** Update multiple Charts simultaneously

**Workflow:**

1. **Fetch remote index to check current state:**
   ```bash
   curl -s https://helm-chart.anubis.cafe/index.yaml -o /tmp/remote-index.yaml
   ```

2. **Use sequential thinking to plan update strategy:**
   ```bash
   mcp__sequential-thinking__sequentialthinking \
     --thought "Need to update 3 Charts. Analyze dependencies to determine order: 1) Charts with no dependencies, 2) Charts that are depended upon." \
     --nextThoughtNeeded true \
     --thoughtNumber 1 \
     --totalThoughts 4
   ```

3. **Use serena to find all Charts needing update:**
   ```bash
   mcp__serena__list_dir --relative_path "charts" --recursive false
   ```

4. Update each Chart's `Chart.yaml` and related files

5. Package all updated Charts:
   ```bash
   helm package charts/*
   ```

6. Run complete workflow to update all indexes:
   ```bash
   helm repo index . --url https://helm-chart.anubis.cafe
   ```

7. Commit all changes at once:
   ```bash
   git add *.tgz index.yaml
   git commit -m "chore: batch update Charts and refresh index

   - Update subconverter to 1.0.0
   - Update claude-relay-service to 1.1.0
   - Regenerate index.yaml"
   ```

8. **Verify against remote before pushing:**
   ```bash
   diff -u /tmp/remote-index.yaml index.yaml
   ```

---

### Scenario 4: Delete Old Versions

**Situation:** Clean up unsupported old versions

**Workflow:**

1. **Check remote index first:**
   ```bash
   yq '.charts.subconverter[].version' /tmp/remote-index.yaml
   ```

2. **Use serena to identify old versions:**
   ```bash
   mcp__serena__search_for_pattern \
     --substring_pattern "0.2.0\.tgz" \
     --relative_path "." \
     --restrict_search_to_code_files false
   ```

3. Delete old .tgz packages:
   ```bash
   rm subconverter-0.2.0.tgz
   ```

4. Delete old index.yaml:
   ```bash
   rm index.yaml
   ```

5. Regenerate index (only includes existing .tgz):
   ```bash
   helm repo index . --url https://helm-chart.anubis.cafe
   ```

6. Commit changes:
   ```bash
   git add index.yaml
   git commit -m "chore: remove subconverter v0.2.0, keep only latest version"
   ```

---

### Scenario 5: Fix Index URL

**Situation:** Repository URL changed or configuration error

**Workflow:**

1. **Use context7 to query correct index format:**
   ```bash
   mcp__plugin_context7_context7__query-docs \
     --libraryId "/helm/helm" \
     --query "helm repo index URL format"
   ```

2. Delete old index.yaml:
   ```bash
   rm index.yaml
   ```

3. Regenerate with correct URL:
   ```bash
   helm repo index . --url https://helm-chart.anubis.cafe
   ```

4. **Use serena to verify URL:**
   ```bash
   mcp__serena__search_for_pattern \
     --substring_pattern "https://helm-chart.anubis.cafe" \
     --relative_path "index.yaml" \
     --restrict_search_to_code_files false
   ```

5. Commit changes

---

## Multi-Environment Handling

### Development Environment

```bash
# Use development environment URL
helm repo index . --url http://localhost:8080
```

### Production Environment

```bash
# Use production environment URL
helm repo index . --url https://helm-chart.anubis.cafe
```

### Test Environment

```bash
# Use test environment URL
helm repo index . --url https://test-helm.example.com
```

---

## Batch Operation Tips

### Package All Charts

```bash
# Method 1: Package all Charts under charts directory
helm package charts/*

# Method 2: Find all Chart directories and package
find charts -name "Chart.yaml" -exec dirname {} \; | xargs -I {} helm package {}
```

**MCP Enhanced:**
```bash
# Use serena to find all Charts
mcp__serena__find_file --file_mask "Chart.yaml" --relative_path "charts"
```

### Verify All Packages

```bash
# Verify all .tgz packages
for file in *.tgz; do
  echo "Validating $file..."
  helm lint "$file"
done
```

### View Index Summary

```bash
# View all Charts in index
grep "^  [a-z-]*:$" index.yaml | sed 's/://g'

# View version count for each Chart
grep "^  [a-z-]*:$" -A 100 index.yaml | grep "version:" | wc -l
```

---

## Performance Optimization

### Large Repository Optimization

For repositories with many Charts:

```bash
# Only update changed packages
helm repo index . --url https://helm-chart.anubis.cafe --merge index.yaml
```

**Parameter Description:**
- `--merge`: Merge into existing index instead of complete rewrite
- Pros: Faster, less computation
- Cons: May retain entries for deleted packages

**Use context7 to understand merge option:**
```bash
mcp__plugin_context7_context7__query-docs \
  --libraryId "/helm/helm" \
  --query "helm repo index merge option"
```

### Parallel Packaging

```bash
# Use GNU parallel for parallel packaging
ls charts/* | parallel -j 4 helm package
```

---

## Automation Recommendations

### CI/CD Integration

Automate index updates in CI/CD workflow:

```yaml
# .github/workflows/release-chart.yml
name: Release Helm Chart

on:
  push:
    paths:
      - 'charts/**/Chart.yaml'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Helm
        uses: azure/setup-helm@v3

      - name: Fetch Remote Index
        run: |
          curl -s https://helm-chart.anubis.cafe/index.yaml -o /tmp/remote-index.yaml

      - name: Package Chart
        run: |
          helm package charts/*

      - name: Update Index
        run: |
          helm repo index . --url https://helm-chart.anubis.cafe

      - name: Verify Against Remote
        run: |
          diff -u /tmp/remote-index.yaml index.yaml || true

      - name: Commit Changes
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add *.tgz index.yaml
          git commit -m "chore: auto-update Helm index"
          git push
```

**Use MCP tools to enhance CI/CD:**
- Use serena to analyze changes when PR is created
- Use sequential thinking to diagnose issues when build fails
- Use context7 to periodically update best practices

---

## Error Handling

### Use sequential thinking to Diagnose Issues

When encountering errors, use sequential thinking for systematic analysis:

```bash
mcp__sequential-thinking__sequentialthinking \
  --thought "helm repo index command failed with error code 1. Analyze possible causes: 1) .tgz file corrupted, 2) disk space insufficient, 3) permission issues." \
  --nextThoughtNeeded true \
  --thoughtNumber 1 \
  --totalThoughts 5
```

### Common Errors and Solutions

**Error: "no such file or directory"**
- Use serena to verify file existence:
  ```bash
  mcp__serena__search_for_pattern \
    --substring_pattern "\.tgz$" \
    --relative_path "." \
    --restrict_search_to_code_files false
  ```

**Error: "invalid YAML"**
- Use context7 to query YAML format requirements:
  ```bash
  mcp__plugin_context7_context7__query-docs \
    --libraryId "/helm/helm" \
    --query "index.yaml YAML format validation"
  ```

**Error: "version conflict with remote"**
- Check remote index before publishing:
  ```bash
  curl -s https://helm-chart.anubis.cafe/index.yaml -o /tmp/remote-index.yaml
  yq '.charts[].[] | select(.name == "booklore") | .version' /tmp/remote-index.yaml
  ```

---

## Reference Documentation

- [Helm Repository Best Practices](https://helm.sh/docs/topics/chart_repository/)
- [Helm Index File Format](https://helm.sh/docs/topics/charts/#the-index-file)
- [Artifact Hub Integration](https://artifacthub.io/docs/topics/repositories/#helm-charts)
- [MCP-GUIDE.md](MCP-GUIDE.md) - Detailed MCP tool usage guide
- [troubleshooting.md](troubleshooting.md) - Troubleshooting guide
