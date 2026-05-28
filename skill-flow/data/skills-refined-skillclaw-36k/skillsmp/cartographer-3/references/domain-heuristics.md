# Domain Detection Heuristics

This reference defines how to identify domains within a codebase by directory patterns, file conventions, and structural signals. Also includes confidence scoring algorithms for project types, domains, and drift detection.

## Core Principles

1. **Observe, don't assume**: Detect domains from actual structure, not framework expectations
2. **Structural boundaries**: Look for directories with distinct conventions or purposes
3. **One clear purpose**: If a domain description needs "and", consider splitting
4. **Evidence-based**: Every domain should have supporting file pattern evidence
5. **Import-aware**: When available, use import relationships to validate domain boundaries

---

## Confidence Levels

| Level | Score Range | Action |
|-------|-------------|--------|
| HIGH | >= 0.8 | Auto-proceed |
| MEDIUM | 0.5 - 0.8 | Auto-proceed with note |
| LOW | < 0.5 | Prompt for confirmation |

---

## Domain Detection Signals

### Directory Name Patterns

**HIGH confidence signals (common conventions):**

| Pattern | Likely Domain |
|---------|---------------|
| `src/components/` | UI Components |
| `src/pages/`, `app/` | Pages/Routes |
| `src/hooks/` | Custom Hooks |
| `src/utils/`, `src/helpers/` | Utilities |
| `src/services/` | Services |
| `src/controllers/` | Controllers |
| `src/routes/`, `src/api/` | Routes/API |
| `src/models/`, `src/entities/` | Models |
| `src/redux/`, `src/store/` | State Management |
| `src/middleware/` | Middleware |
| `src/types/`, `src/interfaces/` | Types |
| `lib/`, `libs/` | Libraries |
| `pkg/`, `internal/` | Packages (Go) |

**MEDIUM confidence signals (less common):**

| Pattern | Likely Domain |
|---------|---------------|
| `src/features/` | Feature Modules |
| `src/modules/` | Modules |
| `src/domain/` | Domain Logic |
| `src/infrastructure/` | Infrastructure |
| `src/shared/` | Shared Code |
| `src/core/` | Core Logic |

---

## Domain Confidence Scoring

### Scoring Factors

| Factor | Points | Description |
|--------|--------|-------------|
| Directory name matches known pattern | +0.30 | See "Directory Name Patterns" above |
| Consistent file naming convention | +0.20 | >80% of files follow pattern |
| Has index/barrel file | +0.10 | Clear entry point |
| File count > 5 | +0.10 | Substantial content |
| Clear import patterns | +0.20 | Referenced consistently elsewhere |
| Has local config file | +0.10 | Domain-specific config |
| Conflicting conventions | -0.20 | Mixed naming patterns |
| Very few files (<3) | -0.10 | May not warrant domain |
| No clear naming pattern | -0.20 | Hard to characterize |

### Import Graph Scoring (when `--deep` analysis enabled)

| Factor | Points | Description |
|--------|--------|-------------|
| Low external coupling (<20%) | +0.15 | Self-contained domain |
| Clear dependency direction | +0.10 | Imports flow one way |
| No bidirectional coupling | +0.10 | Clean boundaries |
| High internal cohesion | +0.15 | Files within domain import each other |
| Heavy external coupling (>50%) | -0.20 | May need to split or merge |
| Bidirectional coupling | -0.15 | Tangled boundaries |
| Layering violations | -0.10 | Skips architectural layers |

### Example

```
Domain: src/hooks/
+ Known pattern "hooks"                    → +0.30
+ All files use "use*.ts" convention       → +0.20
+ Has index.ts barrel export               → +0.10
+ Contains 12 files                        → +0.10
+ Imported from 15+ other files            → +0.20
────────────────────────────────────────────
Total: 0.90 → HIGH confidence
```

---

## Project Type Scoring

### Signal Weights

**Primary signals (HIGH weight: 0.3-0.4):**
- Config file explicitly indicates type
- Framework-specific entry point exists
- Multiple corroborating signals

**Secondary signals (MEDIUM weight: 0.15-0.25):**
- Directory patterns match type
- Dependencies suggest type
- Build configuration aligns

**Disqualifying signals (negative: -0.2 to -0.3):**
- Conflicting primary signals
- Missing expected artifacts

For detailed project type signals, see `references/project-types.md`.

---

## Granularity Rules

### When to Split

Split a directory into sub-domains when:

1. **Different conventions**: Sub-directories use different file patterns
2. **Different purposes**: Sub-directories serve distinct functions
3. **Scale**: Combined domain would have >50 files and distinct sub-areas
4. **Compound description**: Domain purpose needs "and" to describe

### When to Combine

Keep as single domain when:

1. **Consistent conventions**: All files follow same pattern
2. **Tight coupling**: Heavy cross-imports within directory
3. **Small scale**: Combined would be <30 files
4. **Single purpose**: One sentence describes all content

---

## Import Graph Analysis

Import analysis is an **optional supplement** to directory-based detection, enabled via `--deep` flag or interview question. It analyzes actual `import`/`from` statements to validate and refine domain boundaries.

### When Import Analysis Helps

| Scenario | How Import Analysis Helps |
|----------|---------------------------|
| Unclear directory structure | Reveals de facto boundaries from usage |
| Layered architecture | Detects violations (controllers importing DAOs) |
| Large codebase | Finds hidden coupling not obvious from names |
| Refactoring assessment | Shows which domains are tangled |
| Legacy code | Maps actual dependencies vs intended structure |

### What Import Analysis Detects

**Coupling patterns:**
- Strong coupling (>50% cross-imports) → Consider merging domains
- Bidirectional coupling → Tangled boundaries, needs refactoring
- Fan-in hubs → Central utilities that many domains depend on
- Fan-out concerns → Domains with too many responsibilities

**Layering violations:**
- Controllers importing DAOs directly (skipping providers)
- Reverse direction imports (providers importing routes)
- Cross-layer shortcuts

**Domain boundary issues:**
- Split candidates: Directory has distinct clusters
- Merge candidates: Two directories that are effectively one unit
- Missing domains: Heavily-imported areas not tracked

### Limitations

Import analysis cannot detect:
- Runtime dependencies (dynamic imports, dependency injection)
- Implicit coupling through shared state
- Architectural intent (only observes actual usage)

Use import analysis to **supplement**, not replace, developer knowledge about the codebase.

---

## Special Cases

### Monorepos

Treat each package as a namespace:
```
packages/
├── app-a/src/components/    → domain: "app_a_components"
└── shared/src/utils/        → domain: "shared_utils"
```

### Feature-Based Organization

Options:
1. Create domain per feature: `feature_auth`, `feature_dashboard`
2. Create cross-cutting domains: `components`, `hooks`, `apis`

**Recommendation**: Feature domains when features are self-contained.

### Legacy/Mixed Codebases

1. Document dominant pattern as primary domains
2. Note inconsistencies in observations
3. Create `legacy` domain for unstructured code

---

## Drift Detection Scoring

### Staleness Calculation

```
staleness = (age_factor × 0.4) + (change_factor × 0.6)

age_factor = min(1.0, days_since_update / 90)
change_factor = min(1.0, file_changes / 100)
```

### Drift Indicators

| Indicator | Severity | Score Impact |
|-----------|----------|--------------|
| Path doesn't exist | CRITICAL | -1.0 (invalid) |
| File count mismatch >50% | HIGH | -0.4 |
| File count mismatch >20% | MEDIUM | -0.2 |
| New untracked directories | LOW | -0.1 per dir |
| Pattern no longer matches | MEDIUM | -0.3 |

### Rechart Triggers

| Staleness | Action |
|-----------|--------|
| < 0.3 | No action needed |
| 0.3 - 0.6 | Suggest `/cartographer:rechart` |
| > 0.6 | Strongly recommend rechart |
| Critical drift | Block navigator commands |

---

## User Prompts for Low Confidence

Prompt user when:
1. Project type confidence < 0.5
2. >30% of domains have LOW confidence
3. Critical domain has LOW confidence
4. Conflicting signals detected

### Prompt Format

```markdown
## Confirmation Needed

I detected the following with low confidence:

**Project Type**: `backend_api` (confidence: 0.45)
- Found Express dependency
- But also found React components
- Unclear if this is fullstack or separate frontend

**Options:**
1. Confirm as `backend_api`
2. Change to `fullstack`
3. Change to `monorepo`
4. Let me provide more context
```

---

## Domain Naming Conventions

Use snake_case for domain identifiers:
- `user_management`
- `api_routes`
- `redux_slices`
- `common_components`

**Rules:**
1. Be descriptive: `auth_middleware` not `middleware1`
2. Include context in monorepos: `grow_pages` not just `pages`
3. Reflect purpose: `rtk_query_apis` not `api_files`
4. Avoid redundancy: `hooks` not `custom_hooks_directory`
