---
name: bookmark-analyzer
description: Use when analyzing Bookmark Vault codebase comprehensively from multiple dimensions simultaneously (component structure, data flow, type coverage).
context: fork
allowed-tools: Read, Grep, Glob
---

# Bookmark Analyzer

Analyzes Bookmark Vault using isolated context forks for three analysis areas simultaneously, then merges findings into a unified report.

## When to Use

- Comprehensive codebase review needed
- Analyzing multiple dimensions: architecture, data flow, type safety
- Need isolated findings per perspective (prevents cross-contamination of analysis)
- Building reports that synthesize findings across layers

## Core Pattern: Isolation → Analysis → Synthesis

```
Request: "Analyze bookmark vault comprehensively"
    ↓
FORK 1: Component Structure Analysis
├─ Tools: Glob components/, Grep for React exports
├─ Analysis: Count, hierarchy, reusability
└─ Output: Structured findings with specific metrics

FORK 2: Data Flow Analysis (runs in parallel)
├─ Tools: Grep useBookmarks, hooks/, lib/storage
├─ Analysis: Trace state, prop drilling, hook dependencies
└─ Output: Flow diagrams, path analysis, metrics

FORK 3: Type Coverage Analysis (runs in parallel)
├─ Tools: Read lib/types.ts, lib/validation.ts
├─ Analysis: Interface coverage, Zod schemas, alignment
└─ Output: Coverage score, gaps, alignment matrix

SYNTHESIZE: Merge three outputs
├─ Combine findings preserving section structure
├─ Identify cross-section implications
├─ Create unified recommendations
└─ Return final report
```

## Analysis Areas

### Fork 1: Component Structure Analysis

**Objective:** Quantify component inventory and relationships

**Tasks:**
1. Count total components by category (UI primitives, feature modules, etc.)
2. Map parent-child relationships (component tree)
3. Identify high-reuse components
4. Analyze size distribution (lines per component)

**Key Files:**
- `components/ui/` - UI primitives
- `components/bookmarks/` - Feature modules
- `components/vault/`, `components/settings/`, `components/sync/`
- `components/spaces/`, `components/theme/`, `components/auth/`

**Output Format:**
```
## Component Structure Analysis

### Inventory
- Total components: [count]
- UI primitives: [count]
- Feature modules: [count]
- [Other categories]

### Hierarchy
[Component tree showing relationships]

### Reusability
- High-reuse components: [list with usage count]
- Reuse score: [percentage]

### Size Distribution
- Components < 100 lines: [count]
- Components 100-200 lines: [count]
- Components 200+ lines: [count]

### Key Findings
[Specific observations about structure quality, issues]
```

### Fork 2: Data Flow Analysis

**Objective:** Trace how bookmark data moves through the system

**Tasks:**
1. Identify data sources: localStorage, Context, Zustand stores
2. Trace state flow: storage → hooks → components
3. Map prop drilling chains (count depth, props per component)
4. Document hook dependencies and interconnections
5. Identify refresh mechanisms and data sync patterns

**Key Files:**
- `hooks/useBookmarks.ts` - Main state hook
- `hooks/useSyncEngineUnified.ts` - Sync orchestration
- `lib/storage.ts` - localStorage access
- `stores/vault-store.ts`, `stores/settings-store.ts` - Zustand stores

**Output Format:**
```
## Data Flow Analysis

### Flow Paths
- Storage layer: [what stores data]
- State management: [useBookmarks context flow]
- UI consumption: [component data flow]

### Prop Drilling Analysis
- Max depth: [levels]
- Components with 8+ props: [list]
- Average props per component: [number]

### Hook Dependencies
- [Hook name]: Depends on [other hooks/stores]
- [Circular dependency check results]

### Data Refresh Mechanisms
- [Pattern 1]: [description]
- [Pattern 2]: [description]

### Issues Found
[Specific prop drilling bottlenecks, refresh issues]

### Key Findings
[Assessment of data flow quality, performance implications]
```

### Fork 3: Type Coverage Analysis

**Objective:** Assess TypeScript safety and validation completeness

**Tasks:**
1. Verify TypeScript configuration (strict mode enabled)
2. Count and categorize types/interfaces defined
3. Check Zod schema coverage vs. interface definitions
4. Audit function signatures for proper typing
5. Identify any `any` type usage
6. Validate component prop interfaces

**Key Files:**
- `lib/types.ts` - Core domain types
- `lib/validation.ts` - Zod schemas
- `components/**/*.tsx` - Component prop interfaces
- `hooks/**/*.ts` - Hook return types
- `tsconfig.json` - TS configuration

**Output Format:**
```
## Type Coverage Analysis

### Configuration
- TypeScript strict mode: [enabled/disabled]
- Strict flags: [list if enabled]

### Type Definitions
- Total interfaces: [count]
- Total type aliases: [count]
- Exported core types: [count with list]

### Validation Schemas
- Total Zod schemas: [count]
- Schema coverage: [percentage with details]

### Schema-Interface Alignment
| Type | Interface | Schema | Alignment |
| --- | --- | --- | --- |
| [Type name] | ✓/❌ | ✓/❌ | [Status] |

### Coverage Metrics
- Hook return types: [percentage typed]
- Component props: [percentage typed]
- Function signatures: [percentage typed]
- `any` type usage: [count, locations if found]

### Issues Found
[Missing schemas, untyped functions, alignment gaps]

### Key Findings
[Overall type safety score, gaps, recommendations]
```

## Output Format (Synthesis)

Return combined analysis as single structured report:

```markdown
# Bookmark Vault Comprehensive Analysis

## Component Structure Analysis
[Fork 1 findings]

## Data Flow Analysis
[Fork 2 findings]

## Type Coverage Analysis
[Fork 3 findings]

## Cross-Section Implications
[Observations connecting multiple areas]

## Recommendations (Prioritized)
1. [Specific, actionable recommendation]
2. [Specific, actionable recommendation]
3. [Specific, actionable recommendation]

## Overall Assessment Score
- Component Architecture: [/10]
- Data Flow: [/10]
- Type Safety: [/10]
- OVERALL: [/10]
```

## Common Issues to Watch

| Issue | Signal | Location |
|---|---|---|
| Prop drilling bottleneck | Component receives 8+ props | Check if can extract to hook |
| Missing schema | Type defined but no validation | Add Zod schema |
| Circular dependency | Hook A depends on B, B depends on A | Refactor to separate concerns |
| Type gaps | `any` found in code | Replace with explicit type |
| Untyped component | Props interface missing | Add `interface XyzProps` |
| Sync complexity | Single hook > 400 lines | Consider splitting responsibilities |

## Analysis Verification Checklist

- [ ] Fork 1: Component count verified via Glob
- [ ] Fork 1: Parent-child tree complete (spot-check 5 components)
- [ ] Fork 2: Data flow traced from storage to UI (end-to-end)
- [ ] Fork 2: Prop drilling documented with specific component paths
- [ ] Fork 3: TypeScript config verified (read tsconfig.json)
- [ ] Fork 3: Zod schemas counted and compared to interfaces
- [ ] Synthesis: All three areas represented in final report
- [ ] Recommendations: Each is actionable and specific

## Red Flags - STOP and Reconsider

These indicate analysis might be incomplete or context-forking failed:

| Red Flag | What to Do | Rationalization to Block |
|---|---|---|
| "It seems like..." without verification | Stop. Find specific file/line numbers. | "I can estimate without precise data" |
| Only 1-2 findings per area | Incomplete. Each area should have 3-5 findings minimum. | "Some areas just don't have much" |
| Generic observations ("code is clean") | Incomplete. Need specific metrics and evidence. | "Quality is obvious without details" |
| Skipping one of three areas | **CRITICAL ERROR**. All three forks must produce findings. | "Component analysis covers everything" |
| Merged findings with no section breaks | Failed synthesis. Keep areas separate, then synthesize. | "Combining saves time on writing" |
| Recommendations without evidence | Invalid. Each recommendation must reference specific finding. | "These are best practices anyway" |
| No component count or metric numbers | Incomplete Fork 1. Requires: total count, size distribution. | "Exact numbers don't matter much" |
| No prop drilling analysis or depth number | Incomplete Fork 2. Requires: depth count, examples with paths. | "Prop drilling isn't really an issue" |
| No schema-interface alignment table | Incomplete Fork 3. Requires: coverage %, specific gaps. | "Type safety is obvious from inspection" |
| Single report without three sections | Context-forking failed. Must show Fork 1, 2, 3 results separately first. | "One big report is cleaner" |
| No "Cross-Section Implications" section | Failed synthesis step. Findings must connect across forks. | "Each area stands alone" |

---

## Rationalization Blocking (Discipline Pattern)

**The core pattern you're protecting against:**

"I can combine the three analyses into one big report faster"

**Reality:** This violates the isolation principle. Fork results MUST be separated first.

**Steps to combat this:**

1. **Even if rushing**: Present Fork 1 findings first, Fork 2 second, Fork 3 third
2. **Even if fork had no major issues**: Include "Key Findings" section per fork showing isolation maintained
3. **Even if synthesis seems obvious**: Write explicit "Cross-Section Implications" - don't skip this step
4. **Even if one area seems small**: Include it with any findings found (minimum: configuration details)

**Exception:** None. Always separate, then synthesize.

---

## Success Criteria

✓ **Report includes all three analysis areas with structured section breaks**
✓ **Each area has 3+ specific findings with metrics or line references**
✓ **Fork isolation maintained**: Findings organized by Fork 1 → Fork 2 → Fork 3 → Synthesis**
✓ **Cross-section implications section present and non-empty**
✓ **Recommendations are actionable and tied to specific findings with file paths**
✓ **Overall assessment score provided with supporting evidence**
✓ **Verification checklist completed and all items checked**
✓ **No vague observations without data backing them**
✓ **No recommendations without line number or file reference**
✓ **Schema-interface alignment has actual percentages, not estimates**
