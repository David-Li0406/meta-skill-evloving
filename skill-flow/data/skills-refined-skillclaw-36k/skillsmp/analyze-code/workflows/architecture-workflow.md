# Architecture Mode Workflow

**Purpose**: Analyze system layers, boundaries, and architectural patterns

**When to Use**: Evaluating architecture decisions, finding violations, planning major refactoring

**Token Budget**: ~5K (vs 30K+ reading full system) = **83% savings**

---

## Command Chain (5 Steps)

### Step 1: Import Graph Mapping
**Purpose**: Build complete import/dependency graph

```bash
node project-intel.mjs map-imports --json > /tmp/arch_import_map.json
```

**Output**: Complete graph of all imports across the project

**Tokens**: ~1000 bytes

---

### Step 2: Trace Call Paths
**Purpose**: Identify critical execution paths

```bash
# Find entry points first
node project-intel.mjs list --type page --json > /tmp/arch_entries.json

# Trace from main entry
node project-intel.mjs trace {main_entry_file} --max-depth 3 --json > /tmp/arch_trace.json
```

**Output**: Call graph showing function invocation paths

**Tokens**: ~800 bytes

---

### Step 3: Find Circular Dependencies
**Purpose**: Detect architectural violations

```bash
# Circular dependency detection is part of map-imports output
# Filter from arch_import_map.json for cycles

# Alternative: Check specific suspicious paths
node project-intel.mjs dependencies {file1} --direction both --json > /tmp/arch_bidirectional.json
```

**Output**: Cycles in dependency graph (A → B → C → A)

**Tokens**: ~300 bytes

---

### Step 4: Calculate Metrics
**Purpose**: Quantify code quality and complexity

```bash
node project-intel.mjs metrics --json > /tmp/arch_metrics.json
```

**Output**:
- Cyclomatic complexity by file
- Coupling metrics (afferent/efferent)
- Dead code detection
- Code coverage stats

**Tokens**: ~500 bytes

---

### Step 5: Analyze Patterns
**Purpose**: Identify architectural patterns and anti-patterns

```bash
# Search for common patterns
node project-intel.mjs search "context|provider" --json > /tmp/arch_patterns_context.json
node project-intel.mjs search "hook|use[A-Z]" --json > /tmp/arch_patterns_hooks.json
node project-intel.mjs search "\.test\.|spec\." --json > /tmp/arch_patterns_tests.json

# Check for anti-patterns
node project-intel.mjs search "any|TODO|FIXME" --json > /tmp/arch_antipatterns.json
```

**Tokens**: ~400 bytes total

---

## Total Token Usage

```
Command Outputs: ~3000 bytes (~750 tokens)
Targeted File Reads: ~2000 bytes (~500 tokens) - Sample architectural files
Analysis & Processing: ~2000 tokens
MCP Verification: ~500 tokens (architectural best practices)
Output Generation: ~1500 tokens
─────────────────────────────────────────────
Total: ~5000 tokens

vs. Reading Full System: 30K+ tokens
Savings: 83%
```

---

## Processing Steps

### Parse Intel Results
```typescript
const importMap = JSON.parse(readFileSync('/tmp/arch_import_map.json', 'utf-8'));
const trace = JSON.parse(readFileSync('/tmp/arch_trace.json', 'utf-8'));
const metrics = JSON.parse(readFileSync('/tmp/arch_metrics.json', 'utf-8'));
const patterns = {
  context: JSON.parse(readFileSync('/tmp/arch_patterns_context.json', 'utf-8')),
  hooks: JSON.parse(readFileSync('/tmp/arch_patterns_hooks.json', 'utf-8')),
  tests: JSON.parse(readFileSync('/tmp/arch_patterns_tests.json', 'utf-8'))
};
```

### Architectural Analysis

#### 1. Layer Detection
**Identify layers from directory structure and imports**:
- Presentation Layer: components/, pages/, app/
- Business Logic: services/, hooks/, lib/
- Data Layer: models/, database/, api/
- Infrastructure: config/, middleware/, utils/

**Validation**: Ensure dependencies flow top-down (presentation → business → data)

#### 2. Boundary Violations
**Check for violations**:
- ❌ Data layer importing from presentation
- ❌ Circular dependencies between layers
- ❌ Business logic in presentation components

**Extract from**: Import map analysis

#### 3. Pattern Identification
**Architectural Patterns Found**:
- State Management: Context API, Redux, Zustand (from context search)
- Composition: Custom hooks pattern (from hooks search)
- Testing: Test coverage and strategy (from test search)

#### 4. Quality Metrics
**From metrics.json**:
- Average cyclomatic complexity
- Highest complexity files (refactoring candidates)
- Coupling ratios (highly coupled modules)
- Dead code percentage

#### 5. Circular Dependencies
**Extract cycles from import map**:
```typescript
// Pseudo-code for cycle detection
const cycles = importMap.filter(edge =>
  edge.source === edge.target ||
  hasCycle(edge.source, importMap)
);
```

---

## MCP Verification (Optional)

**Query Ref MCP for architectural best practices**:

```typescript
// Verify React patterns
ref_search_documentation("React architectural patterns context provider")

// Verify Next.js routing best practices
ref_search_documentation("Next.js App Router layout patterns")

// Verify testing strategies
ref_search_documentation("Vitest testing patterns React components")
```

**Purpose**: Validate that identified patterns follow official recommendations

---

## Fill Template Placeholders

Using **@.claude/templates/analysis/architecture.md**:

- `{{layers}}` ← Detected layers with file counts
- `{{layer_diagram}}` ← Mermaid diagram showing layers
- `{{boundaries}}` ← Layer boundaries and rules
- `{{violations}}` ← Boundary violations found (with file:line)
- `{{circular_deps}}` ← List of cycles
- `{{patterns}}` ← Identified patterns (state management, composition, etc.)
- `{{metrics_summary}}` ← Key metrics (complexity, coupling, dead code)
- `{{recommendations}}` ← Refactoring suggestions based on violations

---

## Output Specification

**File**: `report.md` (or `refs/architecture-analysis.md`)

**Sections**:
1. Architecture Overview (layers, boundaries)
2. Layer Diagram (visual representation)
3. Boundary Rules (enforced conventions)
4. Violations Found (with severity ratings)
5. Circular Dependencies (if any)
6. Architectural Patterns (identified)
7. Quality Metrics (complexity, coupling, dead code)
8. Recommendations (prioritized fixes)

**Reference in CLAUDE.md**:
```markdown
## Reference Inventory

- **@report.md** - Architecture analysis (generated YYYY-MM-DD)
```

---

## Validation Checklist

Before finalizing:
- [ ] All 5 intel commands executed
- [ ] Import map generated
- [ ] Circular dependencies identified (or confirmed none)
- [ ] Layer boundaries defined
- [ ] Violations documented with file:line
- [ ] Metrics calculated
- [ ] Patterns identified
- [ ] Template filled with all placeholders
- [ ] Token usage ≤ 6K tokens
- [ ] Output saved to report.md

---

## Example Usage

```bash
# Step 1: Build import graph
node project-intel.mjs map-imports --json > /tmp/arch_import_map.json

# Step 2: Trace from main entry
node project-intel.mjs list --type page --json > /tmp/arch_entries.json
node project-intel.mjs trace app/[lang]/page.tsx --max-depth 3 --json > /tmp/arch_trace.json

# Step 3: Calculate metrics
node project-intel.mjs metrics --json > /tmp/arch_metrics.json

# Step 4: Search for patterns
node project-intel.mjs search "context|provider" --json > /tmp/arch_patterns_context.json
node project-intel.mjs search "hook|use[A-Z]" --json > /tmp/arch_patterns_hooks.json

# Step 5: Check for anti-patterns
node project-intel.mjs search "any|TODO|FIXME" --json > /tmp/arch_antipatterns.json

# Process results and generate report.md
# (Template processing logic executed by agent)
```

---

## CoD^Σ Trace Example

```
Goal: Review architecture for circular dependencies

UserRequest("review architecture")
  → ModeDetection(contains("architecture"))
  → mode=architecture

IntelGathering:
  Step1 → map-imports() → {498 import edges}
  Step2 → trace(app/[lang]/page.tsx) → {depth-3 call graph}
  Step3 → metrics() → {avg_complexity: 4.2, max_complexity: 15@utils/validation.ts:42}
  Step4 → search("context|provider") → {3 Context providers found}
  Step5 → search("any|TODO") → {12 any types, 8 TODOs}

CycleDetection:
  ImportMap → CycleAnalysis
    → Found: components/A.tsx → lib/B.ts → components/C.tsx → components/A.tsx
    → Severity: HIGH (violates layer boundary)

LayerAnalysis:
  Presentation: {app/, components/} (45 files)
  Business: {hooks/, lib/services/} (32 files)
  Data: {lib/supabase/} (8 files)

  Violations:
    ❌ lib/supabase/client.ts → components/auth/LoginForm.tsx (data → presentation)
    ❌ components/A.tsx ⇄ components/C.tsx (circular in same layer)

Output → report.md
  Layers: 3 detected (Presentation, Business, Data)
  Violations: 2 found (1 cross-layer, 1 circular)
  Metrics: avg_complexity=4.2 (acceptable), max=15 (refactor candidate)
  Patterns: Context API (state), Custom Hooks (composition)

TokenCost: 5100 (vs 31000 reading all files) = 83% savings
```

---

**Reference**: Adapted from @.claude/shared-imports/project-intel-mjs-guide.md (Architecture Analysis patterns, lines 530-583)
