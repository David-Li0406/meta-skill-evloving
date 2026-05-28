# Feature Mode Workflow

**Purpose**: Deep dive into specific feature/domain for development context (refs/design.md)

**When to Use**: Understanding how a feature works, planning modifications, creating feature documentation

**Token Budget**: ~8K (vs 40K+ reading all feature files) = **80% savings**

---

## Command Chain (6 Steps)

**Input Required**: `target` parameter (feature name, e.g., "booking", "authentication", "payment")

### Step 1: Search for Feature Files
**Purpose**: Identify all files related to the target feature

```bash
node project-intel.mjs search "{target}" --json -l 10 > /tmp/feature_search.json
```

**Example** (target="booking"):
```bash
node project-intel.mjs search "booking" --json -l 10 > /tmp/feature_search.json
```

**Output**: List of files containing "booking" (ranked by relevance)

**Tokens**: ~100 bytes

---

### Step 2: Investigate Feature Entry Point
**Purpose**: Find the main entry point for the feature

```bash
node project-intel.mjs investigate "{target}" -l 3 --json > /tmp/feature_entry.json
```

**Filters**: Components, pages, main modules matching target

**Tokens**: ~500 bytes

---

### Step 3: Search for UI Components
**Purpose**: Find React/Vue components related to feature

```bash
node project-intel.mjs search "{Target}.*Component|{target}-.*\.tsx" --json > /tmp/feature_components.json
```

**Example**:
```bash
node project-intel.mjs search "Booking.*Component|booking-.*\.tsx" --json > /tmp/feature_components.json
```

**Tokens**: ~200 bytes

---

### Step 4: Analyze Symbol Exports
**Purpose**: Understand what each file exports without reading full content

```bash
# For main entry point (identified in Step 2)
node project-intel.mjs symbols {entry_file_path} --json > /tmp/feature_symbols.json

# For related components (top 3 from Step 1)
node project-intel.mjs symbols {component1_path} --json > /tmp/feature_comp1_symbols.json
node project-intel.mjs symbols {component2_path} --json > /tmp/feature_comp2_symbols.json
```

**Output**: Functions, classes, types exported from each file with line numbers

**Tokens**: ~600 bytes (200 per file)

---

### Step 5: Trace Dependencies (Upstream)
**Purpose**: Understand what the feature imports/depends on

```bash
node project-intel.mjs dependencies {entry_file_path} --direction upstream --json > /tmp/feature_deps_up.json
```

**Output**: All imports and their sources

**Tokens**: ~300 bytes

---

### Step 6: Trace Dependencies (Downstream)
**Purpose**: Understand what consumes this feature

```bash
node project-intel.mjs dependencies {entry_file_path} --direction downstream --json > /tmp/feature_deps_down.json

# Or use importers command
node project-intel.mjs importers {entry_file_path} --json > /tmp/feature_importers.json
```

**Output**: All files that import this feature

**Tokens**: ~300 bytes

---

## Optional Step 7: Debug Feature Issues
**Purpose**: If feature has known issues, get diagnostic insights

```bash
node project-intel.mjs debug {ComponentName} --json > /tmp/feature_debug.json
```

**Provides**: Common issues, dependency conflicts, circular references

**Tokens**: ~500 bytes

---

## Total Token Usage

```
Command Outputs: ~2500 bytes (~650 tokens)
Targeted File Reads: ~5000 bytes (~1250 tokens) - Read only key sections
Template Processing: ~1000 tokens
MCP Verification: ~500 tokens (if library behavior needs checking)
Output Generation: ~4000 tokens
─────────────────────────────────────────────
Total: ~8000 tokens

vs. Reading All Feature Files: 40K+ tokens
Savings: 80%
```

---

## Processing Steps

### Parse Intel Results
```typescript
const search = JSON.parse(readFileSync('/tmp/feature_search.json', 'utf-8'));
const entry = JSON.parse(readFileSync('/tmp/feature_entry.json', 'utf-8'));
const components = JSON.parse(readFileSync('/tmp/feature_components.json', 'utf-8'));
const symbols = JSON.parse(readFileSync('/tmp/feature_symbols.json', 'utf-8'));
const depsUp = JSON.parse(readFileSync('/tmp/feature_deps_up.json', 'utf-8'));
const depsDown = JSON.parse(readFileSync('/tmp/feature_deps_down.json', 'utf-8'));
```

### Build Feature Map
1. **Feature Boundary**: Extract from search results (all files related to target)
2. **Entry Point**: Identify from investigate results (main component/module)
3. **Component Hierarchy**: Build from components search + symbols
4. **Dependency Graph**: Combine upstream + downstream dependencies
5. **Data Flow**: Trace from symbols (state management, API calls, props)
6. **Integration Points**: External systems from upstream dependencies

### Targeted File Reads (After Intel)
**Read ONLY specific sections identified by intel queries**:
```bash
# Example: Read main component implementation (lines 40-120 only)
sed -n '40,120p' components/booking/CalBookingModal.tsx

# Read hook definition (lines 15-45)
sed -n '15,45p' hooks/useBooking.ts
```

**Strategy**: Read max 200 lines total across all files (vs 2000+ lines if reading full files)

---

## Fill Template Placeholders

Using **@.claude/templates/analysis/design.md**:

- `{{feature_name}}` ← target parameter
- `{{feature_boundary}}` ← File list from search
- `{{entry_point}}` ← Main file from investigate
- `{{component_hierarchy}}` ← Tree from components + symbols
- `{{dependency_graph}}` ← Mermaid diagram from deps up/down
- `{{data_flow}}` ← Traced from symbols (useState, API calls, etc.)
- `{{integration_points}}` ← External systems from upstream
- `{{key_functions}}` ← Exported functions from symbols
- `{{recommendations}}` ← Generated based on analysis

---

## Output Specification

**File**: `refs/design.md` (or `refs/{feature}-design.md` for multiple features)

**Sections**:
1. Feature Overview (purpose, scope)
2. Boundary Definition (which files belong to this feature)
3. Component Hierarchy (how components relate)
4. Dependency Graph (visual diagram)
5. Data Flow (state management, API interactions)
6. Integration Points (external systems, shared utilities)
7. Key Functions & Types (from symbols analysis)
8. Recommendations (development guidance, gotchas)

**Reference in CLAUDE.md**:
```markdown
## Reference Inventory

- **@refs/design.md** - {feature_name} feature context (generated YYYY-MM-DD)
```

---

## Validation Checklist

Before finalizing:
- [ ] Target feature specified
- [ ] All 6 intel commands executed (7 if debug used)
- [ ] JSON outputs saved to /tmp/ for evidence
- [ ] Targeted reads ≤ 200 lines total
- [ ] Dependency graph generated
- [ ] Template filled with all placeholders
- [ ] Token usage ≤ 10K tokens
- [ ] Output saved to refs/design.md
- [ ] CLAUDE.md updated with reference

---

## Example Usage (Booking Feature)

```bash
# Step 1: Search for booking-related files
node project-intel.mjs search "booking" --json -l 10 > /tmp/feature_search.json

# Step 2: Find entry point
node project-intel.mjs investigate "booking" -l 3 --json > /tmp/feature_entry.json

# Step 3: Find UI components
node project-intel.mjs search "Booking.*Component|booking-.*\.tsx" --json > /tmp/feature_components.json

# Step 4: Analyze symbols from main component
node project-intel.mjs symbols components/booking/CalBookingModal.tsx --json > /tmp/feature_symbols.json

# Step 5: Upstream dependencies
node project-intel.mjs dependencies components/booking/CalBookingModal.tsx --direction upstream --json > /tmp/feature_deps_up.json

# Step 6: Downstream consumers
node project-intel.mjs importers components/booking/CalBookingModal.tsx --json > /tmp/feature_importers.json

# Now read ONLY key sections (after intel identified them)
sed -n '20,80p' components/booking/CalBookingModal.tsx  # Main implementation
sed -n '10,35p' hooks/useBooking.ts  # Hook logic

# Process results and generate refs/design.md
# (Template processing logic executed by agent)
```

---

## CoD^Σ Trace Example

```
Goal: Understand booking feature

UserRequest("how does booking work")
  → ModeDetection(contains("how does", "booking"))
  → mode=feature, target="booking"

IntelGathering:
  Step1 → search("booking") → {CalBookingModal.tsx, useBooking.ts, BookingForm.tsx}
  Step2 → investigate("booking") → entry_point = CalBookingModal.tsx
  Step3 → symbols(CalBookingModal.tsx) → {CalBookingModal:45, useBooking:62, submitBooking:78}
  Step4 → dependencies(CalBookingModal.tsx, upstream) → {@calcom/embed-react, hooks/useBooking}
  Step5 → importers(CalBookingModal.tsx) → {PageContent.tsx, ServicesPage.tsx}

TargetedReads:
  Read CalBookingModal.tsx:45-80 → Component implementation
  Read useBooking.ts:10-35 → Hook logic
  Total: 70 lines (vs 500+ full files)

Output → refs/design.md
  FeatureBoundary: [CalBookingModal, useBooking, BookingForm]
  EntryPoint: CalBookingModal.tsx
  Dependencies: @calcom/embed-react ⇄ useBooking
  Integration: Cal.com API (external)

TokenCost: 8200 (vs 42000 reading full files) = 80% savings
```

---

**Reference**: Adapted from @.claude/shared-imports/project-intel-mjs-guide.md (Workflow 1: Understanding Existing Feature, lines 481-517)
