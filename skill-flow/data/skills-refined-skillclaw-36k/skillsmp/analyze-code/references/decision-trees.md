# Analysis Type Decision Trees

**Purpose**: Guides for different analysis scenarios using intelligence-first approach.

---

## Mode Selection Tree (Primary)

**Use When**: analyze-code skill is invoked to determine which analysis mode to use

**Decision Process**:
```
User Request → Context Analysis
    ↓
┌─ Contains "codebase", "structure", "overview", "new to this project"?
│   → MODE: overview
│   → OUTPUT: refs/overview.md
│   → TOKEN BUDGET: ~2K (96% savings)
│
├─ Contains "how does [X] work", "[feature] explanation", specific component/feature name?
│   → MODE: feature (target=[X])
│   → OUTPUT: refs/design.md
│   → TOKEN BUDGET: ~8K (80% savings)
│
├─ Contains "architecture", "layers", "cycles", "boundaries", "review design"?
│   → MODE: architecture
│   → OUTPUT: report.md
│   → TOKEN BUDGET: ~5K (83% savings)
│
└─ Ambiguous context?
    → ASK USER: "What would you like me to analyze?"
    → OPTIONS: ["General codebase overview", "Specific feature/component", "System architecture"]
```

**Mode Characteristics**:

| Mode | Purpose | Output | Key Queries | When to Use |
|------|---------|--------|-------------|-------------|
| **overview** | Understand repository | `refs/overview.md` | stats, tree, list, search | New to codebase, need general context |
| **feature** | Deep dive into domain | `refs/design.md` | search, investigate, symbols, dependencies | "How does booking work?", understand specific feature |
| **architecture** | System structure | `report.md` | map-imports, trace, metrics, patterns | Review layers, find cycles, analyze coupling |

**Mode Selection CoD^Σ**:
```
UserMessage("understand this codebase")
  → ContextAnalysis(contains("codebase", "structure"))
  → mode=overview

UserMessage("how does the booking system work?")
  → ContextAnalysis(contains("how does", "booking"))
  → mode=feature, target="booking"

UserMessage("review the architecture for circular dependencies")
  → ContextAnalysis(contains("architecture", "circular"))
  → mode=architecture
```

**Workflow Files**:
- **overview**: `.claude/skills/analyze-code/workflows/overview-workflow.md`
- **feature**: `.claude/skills/analyze-code/workflows/feature-workflow.md`
- **architecture**: `.claude/skills/analyze-code/workflows/architecture-workflow.md`

**Output Templates**:
- **overview**: `.claude/templates/analysis/overview.md` → `refs/overview.md`
- **feature**: `.claude/templates/analysis/design.md` → `refs/design.md`
- **architecture**: `.claude/templates/analysis/architecture.md` → `report.md`

---

## Tree 1: Bug Diagnosis

**Use When**: User reports error/bug or unexpected behavior

**Process**:
```
User reports error/bug
    ↓
1. Search for error message/symptom keywords (project-intel.mjs --search)
    ↓
2. Locate function/component with issue (--symbols)
    ↓
3. Trace dependencies upstream (what does it use?)
    ↓
4. Find discrepancy (missing check, wrong data)
    ↓
5. Verify with MCP if library-related
    ↓
6. Report with root cause at file:line
```

**Key Intelligence Queries**:
- `project-intel.mjs --search "<error-message>" --json`
- `project-intel.mjs --search "<component-name>" --type tsx --json`
- `project-intel.mjs --symbols path/to/suspected-file.tsx --json`
- `project-intel.mjs --dependencies path/to/suspected-file.tsx --direction upstream --json`

**Output Focus**:
- Specific file:line reference for bug location
- Evidence chain from symptom to root cause
- MCP verification if library behavior involved
- Actionable fix recommendation

**Example Objective**:
"Why does LoginForm component re-render infinitely?"

**Example Root Cause**:
```
Root Cause: src/components/LoginForm.tsx:47
Issue: useEffect depends on [user] but mutates user object
Fix: Use functional setState or remove user from dependencies
Evidence: project-intel.mjs symbols query + MCP Ref verification
```

---

## Tree 2: Architecture Analysis

**Use When**: User wants to understand system design, component relationships, or code organization

**Process**:
```
User wants to understand system design
    ↓
1. Get project overview (project-intel.mjs --overview)
    ↓
2. Identify entry points (main.tsx, index.ts, app.tsx)
    ↓
3. Trace dependencies from entry points (--dependencies --downstream)
    ↓
4. Build dependency graph
    ↓
5. Analyze patterns:
   - Circular dependencies?
   - Deep nesting?
   - Tight coupling?
    ↓
6. Report with visualization (mermaid diagram)
```

**Key Intelligence Queries**:
- `project-intel.mjs --overview --json`
- `project-intel.mjs --dependencies path/to/entry-point.tsx --direction downstream --json`
- `project-intel.mjs --trace path/to/component.tsx --json`

**Output Focus**:
- Dependency graph visualization (mermaid)
- Component relationships
- Coupling analysis
- Module boundaries
- Potential architectural issues (circular deps, tight coupling)

**Example Objective**:
"What is the architecture of the authentication module?"

**Example Output**:
```markdown
## Architecture Summary

Entry Point: src/auth/index.ts
Components: 5 files (LoginForm, AuthProvider, useAuth, api, types)

Dependency Graph:
```mermaid
graph TD
  A[LoginForm.tsx] --> B[useAuth.tsx]
  B --> C[AuthProvider.tsx]
  C --> D[api.ts]
  D --> E[types.ts]
```

Analysis:
- Clean layered architecture (UI → hooks → provider → API)
- No circular dependencies
- Proper type separation
```

---

## Tree 3: Performance Analysis

**Use When**: User reports slow operation, high memory usage, or wants optimization

**Process**:
```
User reports slow operation
    ↓
1. Search for suspected slow operations (queries, loops, renders)
    ↓
2. Trace data flow from source to sink
    ↓
3. Identify bottlenecks:
   - N+1 queries?
   - Unnecessary re-renders?
   - Large data processing?
   - Inefficient algorithms?
    ↓
4. Measure impact (how many times called? on what trigger?)
    ↓
5. Verify best practices with MCP (React performance, DB optimization)
    ↓
6. Report with optimization recommendations
```

**Key Intelligence Queries**:
- `project-intel.mjs --search "query|fetch|map|filter" --json`
- `project-intel.mjs --callers suspectedSlowFunction --json`
- `project-intel.mjs --callees suspectedSlowFunction --json`
- `project-intel.mjs --symbols path/to/slow-component.tsx --json`

**Output Focus**:
- Bottleneck identification with file:line
- Call frequency analysis (how often executed)
- Data volume analysis (size of datasets processed)
- Optimization strategy with specific recommendations
- Before/after performance estimates

**Example Objective**:
"Why is the user list page loading slowly?"

**Example Root Cause**:
```
Bottleneck: src/pages/UserList.tsx:67
Issue: Fetching user details individually in loop (N+1 query pattern)
Impact: 100 users = 100 separate API calls (5s total)
Fix: Batch fetch with single API call (0.3s total)
Evidence:
- project-intel.mjs --symbols → fetchUserDetails at line 67
- project-intel.mjs --callers fetchUserDetails → called in map()
- MCP Ref verification: React docs recommend batching data fetches
```

---

## Decision Tree Selection Guide

**Choose Tree 1 (Bug Diagnosis)** when:
- Error message or stack trace present
- User reports "not working" or "broken"
- Unexpected behavior described
- Test failures

**Choose Tree 2 (Architecture Analysis)** when:
- User asks "how does X work?"
- Understanding system structure
- Planning major refactoring
- Evaluating code organization

**Choose Tree 3 (Performance Analysis)** when:
- User reports "slow" or "laggy"
- High resource usage
- Optimization needed
- Scaling concerns

**Can Combine Multiple Trees**:
- Bug diagnosis may reveal architectural issues
- Performance analysis may uncover bugs
- Architecture review may identify performance bottlenecks

---

## Common Patterns Across All Trees

**Always Start With**:
1. Project overview (if first analysis in session)
2. Targeted search for relevant code
3. Symbol analysis before reading files
4. Dependency tracing to understand relationships

**Always End With**:
1. CoD^Σ trace showing reasoning chain
2. Specific file:line references
3. Evidence from intelligence queries
4. MCP verification (if applicable)
5. Actionable recommendations

**Token Budget**:
- Tree 1 (Bug): ~1000-2000 tokens
- Tree 2 (Architecture): ~2000-3000 tokens
- Tree 3 (Performance): ~1500-2500 tokens

Compare to 10,000-20,000 tokens for reading full files.
