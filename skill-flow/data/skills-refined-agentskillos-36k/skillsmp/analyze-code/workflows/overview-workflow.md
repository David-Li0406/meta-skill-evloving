# Overview Mode Workflow

**Purpose**: Create comprehensive repository map for reference documentation (refs/overview.md)

**When to Use**: First-time codebase exploration, building project documentation, understanding high-level architecture

**Token Budget**: ~2K (vs 50K+ reading all files) = **96% savings**

---

## Command Chain (6 Steps)

### Step 1: Project Statistics
**Purpose**: Understand project scale and technology stack

```bash
node project-intel.mjs stats --json > /tmp/overview_stats.json
```

**Output Example**:
```json
{
  "totalFiles": 84,
  "filesByType": {"tsx": 45, "ts": 32, "json": 7},
  "linesOfCode": 12456,
  "topLevelDirectories": ["app", "components", "lib", "tests"]
}
```

**Tokens**: ~50 bytes (JSON output)

---

### Step 2: Directory Tree
**Purpose**: Visualize project structure

```bash
node project-intel.mjs tree --max-depth 2 --json > /tmp/overview_tree.json
```

**Output**: Nested structure showing directories and key files up to 2 levels deep

**Tokens**: ~300 bytes

---

### Step 3: Component Inventory
**Purpose**: List all UI components

```bash
node project-intel.mjs list --type component --json > /tmp/overview_components.json
```

**Filters for**: Files matching component patterns (React, Vue, etc.)

**Tokens**: ~200 bytes

---

### Step 4: Page/Route Inventory
**Purpose**: Map application routes and entry points

```bash
node project-intel.mjs list --type page --json > /tmp/overview_pages.json
```

**Filters for**: Route files (Next.js pages, React Router, etc.)

**Tokens**: ~200 bytes

---

### Step 5: Search for Key Patterns
**Purpose**: Identify important architectural elements

```bash
# Find configuration files
node project-intel.mjs search "config" --json > /tmp/overview_configs.json

# Find API routes
node project-intel.mjs search "api|route" --json > /tmp/overview_apis.json

# Find database models
node project-intel.mjs search "model|schema" --json > /tmp/overview_models.json
```

**Tokens**: ~300 bytes total

---

### Step 6: Summarize Key Directories
**Purpose**: Get high-level summaries of important directories

```bash
node project-intel.mjs summarize app --json > /tmp/overview_app.json
node project-intel.mjs summarize components --json > /tmp/overview_components_summary.json
node project-intel.mjs summarize lib --json > /tmp/overview_lib.json
```

**Tokens**: ~500 bytes total

---

## Total Token Usage

```
Command Outputs: ~1550 bytes (~400 tokens)
Template Processing: ~600 tokens
Output Generation: ~1000 tokens
──────────────────────────────────────
Total: ~2000 tokens

vs. Reading All Files: 50K+ tokens
Savings: 96%
```

---

## Processing Steps

### Parse Intel Results
```typescript
const stats = JSON.parse(readFileSync('/tmp/overview_stats.json', 'utf-8'));
const tree = JSON.parse(readFileSync('/tmp/overview_tree.json', 'utf-8'));
const components = JSON.parse(readFileSync('/tmp/overview_components.json', 'utf-8'));
const pages = JSON.parse(readFileSync('/tmp/overview_pages.json', 'utf-8'));
```

### Extract Key Insights
- **Project Type**: Identify from stats.filesByType (Next.js, React, Vue, etc.)
- **Scale**: Classify based on totalFiles (Small <50, Medium 50-200, Large 200+)
- **Entry Points**: Extract from pages inventory
- **Component Count**: Count from components inventory
- **Key Directories**: Parse from tree structure

### Fill Template Placeholders
Using **@.claude/templates/analysis/overview.md**:
- `{{project_stats}}` ← stats JSON
- `{{directory_tree}}` ← tree visualization
- `{{component_list}}` ← components array
- `{{page_list}}` ← pages/routes array
- `{{key_patterns}}` ← search results
- `{{recommendations}}` ← Generated based on patterns found

---

## Output Specification

**File**: `refs/overview.md`

**Sections**:
1. Project Overview (stats, tech stack)
2. Directory Structure (tree with explanations)
3. Component Inventory (categorized list)
4. Entry Points (pages/routes map)
5. Architecture Patterns (identified from search)
6. Recommendations (next steps for developers)

**Reference in CLAUDE.md**:
```markdown
## Reference Inventory

- **@refs/overview.md** - Complete repository map (generated YYYY-MM-DD)
```

---

## Validation Checklist

Before finalizing:
- [ ] All 6 intel commands executed successfully
- [ ] JSON outputs saved to /tmp/ for evidence
- [ ] No full file reads performed
- [ ] Template filled with all placeholders
- [ ] Token usage ≤ 2500 tokens
- [ ] Output saved to refs/overview.md
- [ ] CLAUDE.md updated with reference

---

## Example Usage

```bash
# Execute complete overview workflow
node project-intel.mjs stats --json > /tmp/overview_stats.json
node project-intel.mjs tree --max-depth 2 --json > /tmp/overview_tree.json
node project-intel.mjs list --type component --json > /tmp/overview_components.json
node project-intel.mjs list --type page --json > /tmp/overview_pages.json
node project-intel.mjs search "config" --json > /tmp/overview_configs.json
node project-intel.mjs summarize app --json > /tmp/overview_app.json

# Process results and generate refs/overview.md
# (Template processing logic executed by agent)
```

---

**Reference**: Adapted from @.claude/shared-imports/project-intel-mjs-guide.md (Optimal Workflow Pattern, lines 42-65)
