# Optimization Patterns for AI Artifacts

## Core Principle

Files are AI artifacts - optimized for AI agent consumption, not human reading. Goal: Maximum token efficiency through progressive disclosure.

**Target**: ~800 lines max per file
**Why**: Optimal context window for AI agents, enables progressive loading

---

## Pattern 1: Break by Phase (Most Common)

### When to Use
- Implementation plans with 8+ phases
- Total plan >800 lines
- Phases are logically independent

### Strategy

**Group Related Phases**:
- Backend phases: 1-3 (Database, Repository, Service)
- API phase: 4 (API Layer)
- Frontend phase: 5 (UI Layer)
- Validation phases: 6-8 (Testing, Documentation, Deployment)

### Example

**Before Optimization**: `sidebar-polish-v1.md` (1200 lines)
```
Phase 1: Database (150 lines)
Phase 2: Repository (150 lines)
Phase 3: Service (150 lines)
Phase 4: API (150 lines)
Phase 5: UI (200 lines)
Phase 6: Testing (150 lines)
Phase 7: Documentation (100 lines)
Phase 8: Deployment (150 lines)
```

**After Optimization**:
```
sidebar-polish-v1.md (200 lines - summary + links)
├── phase-1-3-backend.md (450 lines)
│   ├── Phase 1: Database (150 lines)
│   ├── Phase 2: Repository (150 lines)
│   └── Phase 3: Service (150 lines)
├── phase-4-5-frontend.md (350 lines)
│   ├── Phase 4: API (150 lines)
│   └── Phase 5: UI (200 lines)
└── phase-6-8-validation.md (400 lines)
    ├── Phase 6: Testing (150 lines)
    ├── Phase 7: Documentation (100 lines)
    └── Phase 8: Deployment (150 lines)
```

### Token Efficiency
- **Before**: Load 1200 lines for any query
- **After**: Load 200-line summary + specific phase (450 max) = 650 lines (46% reduction)
- **For overview**: Load 200 lines only (83% reduction)

---

## Pattern 2: Break by Domain

### When to Use
- Large feature spanning multiple domains
- Natural separation between backend and frontend
- Complex integration scenarios

### Strategy

**Domain Grouping**:
- Backend domain: Database → Repository → Service → API
- Frontend domain: UI components → State → Integration
- Validation domain: Testing → Documentation → Deployment

### Example

**Before Optimization**: `realtime-collaboration-v1.md` (1400 lines)
```
Phase 1: Database (200 lines)
Phase 2: Repository (200 lines)
Phase 3: Service (250 lines)
Phase 4: WebSocket API (250 lines)
Phase 5: Collaborative Editor (300 lines)
Phase 6: Testing (200 lines)
```

**After Optimization**:
```
realtime-collaboration-v1.md (250 lines - summary)
├── backend-implementation.md (700 lines)
│   ├── Phase 1: Database (200 lines)
│   ├── Phase 2: Repository (200 lines)
│   ├── Phase 3: Service (250 lines)
│   └── Integration notes (50 lines)
├── frontend-implementation.md (550 lines)
│   ├── Phase 4: WebSocket API (250 lines)
│   ├── Phase 5: Collaborative Editor (300 lines)
│   └── Real-time UI patterns
└── validation-deployment.md (200 lines)
    └── Phase 6: Testing + Deployment
```

### Token Efficiency
- **Before**: Load 1400 lines for any query
- **After**: Load 250 + specific domain (700 max) = 950 lines (32% reduction)
- **For targeted work**: Load only relevant domain (50%+ reduction)

---

## Pattern 3: Break by Task Type

### When to Use
- Implementation and testing/docs are distinct efforts
- Can parallelize implementation and validation work
- Clear separation of concerns

### Strategy

**Type Grouping**:
- Implementation tasks: Phases 1-5
- Validation tasks: Phases 6-8

### Example

**Before Optimization**: `advanced-filtering-v1.md` (1100 lines)
```
Phase 1-5: Implementation (800 lines)
Phase 6-8: Validation (300 lines)
```

**After Optimization**:
```
advanced-filtering-v1.md (200 lines - summary)
├── implementation-tasks.md (800 lines)
│   ├── Phase 1: Database
│   ├── Phase 2: Repository
│   ├── Phase 3: Service
│   ├── Phase 4: API
│   └── Phase 5: UI
└── validation-tasks.md (300 lines)
    ├── Phase 6: Testing
    ├── Phase 7: Documentation
    └── Phase 8: Deployment
```

### Token Efficiency
- **Before**: Load 1100 lines for any query
- **After**: Load 200 + specific type (800 max) = 1000 lines (9% reduction)
- **For validation queries**: Load 200 + 300 = 500 lines (55% reduction)

---

## Pattern 4: Keep Together (Important)

### Always in Parent Plan

**Executive Content** (keep in main plan):
- Executive Summary (50-100 lines)
- Implementation Strategy (50-100 lines)
- Phase Overview Table (20-50 lines)
- Risk Mitigation Summary (50-100 lines)
- Success Metrics Overview (50 lines)
- Resource Requirements (50 lines)

**Total Parent Size**: 200-300 lines

### Always in Phase Files

**Detailed Content** (move to phase files):
- Complete task breakdown tables
- Detailed acceptance criteria
- Technical implementation notes
- Specific integration points
- Per-task subagent assignments
- Quality gates per phase
- Key files with line ranges

---

## Pattern 5: Single Phase Breakout

### When to Use
- One phase is exceptionally large (>400 lines)
- Rest of plan is reasonable size
- Phase has complex sub-tasks

### Strategy

Break only the large phase into its own file, keep rest in parent.

### Example

**Before**: `authentication-refactor-v1.md` (900 lines)
```
Phase 1: Database (100 lines)
Phase 2: Repository (100 lines)
Phase 3: Auth Service (500 lines) ← Large!
Phase 4: API (100 lines)
Phase 5: UI (100 lines)
```

**After**:
```
authentication-refactor-v1.md (400 lines - includes all but Phase 3)
└── phase-3-auth-service.md (500 lines - detailed auth implementation)
```

### Token Efficiency
- **Before**: Load 900 lines for any query
- **After - Phase 3 query**: Load 400 + 500 = 900 lines (no change for this phase)
- **After - Other phases**: Load 400 lines only (56% reduction)

---

## Progressive Disclosure Strategy

### 3-Level Loading

**Level 1: Overview** (200-300 lines)
- Load: Parent plan only
- Contains: Executive summary, phase table, high-level strategy
- **Use Case**: "What is this feature? What phases are there?"

**Level 2: Phase Summary** (400-500 lines)
- Load: Parent + specific phase file
- Contains: Detailed tasks, acceptance criteria, subagent assignments
- **Use Case**: "Implement Phase 3 tasks"

**Level 3: Full Context** (600-800 lines)
- Load: Parent + phase file + related context
- Contains: All details + integration notes + gotchas
- **Use Case**: "Complex implementation with cross-phase dependencies"

### Example Loading

**Query**: "Show me the UI implementation tasks"

**Level 1 Response** (200 lines):
```
Load: Parent plan
See: Phase 5 overview in phase table
Indicate: Details in phase-4-5-frontend.md
```

**Level 2 Response** (200 + 400 = 600 lines):
```
Load: Parent plan + phase-4-5-frontend.md
Show: Complete Phase 5 task breakdown
Ready: For implementation
```

**Level 3 Response** (200 + 400 + 200 = 800 lines):
```
Load: Parent + phase file + context
Show: Tasks + integration points + gotchas
Ready: For complex implementation
```

---

## Token Efficiency Formulas

### Traditional Approach

```
Token Usage = Full File Lines × Token Multiplier
Example: 1200 lines × 2.5 tokens/line = 3000 tokens
```

### Optimized Approach

```
Overview Query:
  Token Usage = Parent Lines × Token Multiplier
  Example: 200 lines × 2.5 = 500 tokens
  Savings: 83%

Targeted Query:
  Token Usage = (Parent + Phase) × Token Multiplier
  Example: (200 + 400) × 2.5 = 1500 tokens
  Savings: 50%

Deep Dive:
  Token Usage = (Parent + Phase + Context) × Token Multiplier
  Example: (200 + 400 + 200) × 2.5 = 2000 tokens
  Savings: 33%
```

### Average Savings

Across typical queries with phase breakout:
- **50-70% token reduction** for most queries
- **Enables working with larger features** without context overflow
- **Faster AI response times** due to smaller context

---

## Implementation Checklist

### When Optimizing a Plan

- [ ] **Analyze Size**: Count total lines
- [ ] **Identify Breakpoints**: Find natural boundaries (phases, domains, types)
- [ ] **Choose Pattern**: Select appropriate pattern (phase, domain, type)
- [ ] **Create Structure**: Set up directories and files
- [ ] **Split Content**: Move content to phase files
- [ ] **Update Parent**: Add summary and links
- [ ] **Cross-Link**: Link phase files back to parent
- [ ] **Validate**: Ensure all content preserved
- [ ] **Test Loading**: Verify token efficiency with test queries

### Quality Gates for Optimization

- [ ] Each file <800 lines
- [ ] Parent plan 200-300 lines (summary + links)
- [ ] All phase files linked from parent
- [ ] All content preserved (nothing lost)
- [ ] Logical grouping maintained
- [ ] Cross-links work correctly
- [ ] Token efficiency >50% for targeted queries
- [ ] Progressive disclosure achievable

---

## Anti-Patterns to Avoid

### ❌ Over-Optimization

**Problem**: Breaking files too small (<200 lines per file)
**Result**: Too many files, overhead of loading multiple files
**Fix**: Group related content, aim for 300-500 lines per phase file

### ❌ Arbitrary Splits

**Problem**: Breaking mid-phase or mid-task
**Result**: Loss of cohesion, harder to understand
**Fix**: Split only on logical boundaries (phase, domain, task type)

### ❌ No Summary in Parent

**Problem**: Parent plan just has links, no overview
**Result**: Must load phase files to understand feature
**Fix**: Keep executive summary, phase table, strategy in parent

### ❌ Duplicate Content

**Problem**: Repeating content in parent and phase files
**Result**: Inconsistency, wasted tokens
**Fix**: Summary in parent, details in phase files only

### ❌ Missing Cross-Links

**Problem**: Phase files don't link back to parent
**Result**: Lost context, hard to navigate
**Fix**: Always link phase files back to parent plan

### ❌ Inconsistent Structure

**Problem**: Each phase file has different format
**Result**: Harder for AI to parse and understand
**Fix**: Use templates for all phase files

---

## Real-World Examples

### Example 1: Data Layer Fixes (No Breakout Needed)

**File**: `data-layer-fixes-filtering-v1.md` (650 lines)

**Analysis**:
- 5 phases, ~130 lines each
- Total 650 lines (under 800 threshold)
- **Decision**: No breakout needed

**Optimization**: None required, file is already optimal size

---

### Example 2: Prompt Modal Improvements (Breakout Required)

**File**: `prompt-modal-improvements-v1.md` (1200 lines)

**Analysis**:
- 8 phases, ~150 lines each
- Total 1200 lines (exceeds 800 threshold)
- Natural grouping: Backend (1-3), Frontend (4-5), Validation (6-8)

**Optimization Pattern**: Break by Phase (Pattern 1)

**Result**:
```
prompt-modal-improvements-v1.md (200 lines)
├── phase-1-3-backend.md (450 lines)
├── phase-4-5-frontend.md (400 lines)
└── phase-6-8-validation.md (350 lines)
```

**Token Savings**: 50-70% for targeted queries

---

### Example 3: Realtime Collaboration (Domain Breakout)

**File**: `realtime-collaboration-v1.md` (1500 lines)

**Analysis**:
- Complex feature spanning backend and frontend
- Natural domain separation
- Different teams working on different domains

**Optimization Pattern**: Break by Domain (Pattern 2)

**Result**:
```
realtime-collaboration-v1.md (250 lines)
├── backend-implementation.md (700 lines)
├── frontend-implementation.md (550 lines)
```

**Token Savings**: 60%+ for domain-specific queries

---

## Automation Opportunities

### Script Support

Create `optimize-plan.sh` script to:
1. Count lines in plan
2. Identify phases
3. Suggest breakout strategy
4. Create phase files
5. Update parent with links
6. Validate optimization

### AI Agent Support

AI agents can:
- Analyze plan size automatically
- Suggest optimal breakout pattern
- Generate phase files with correct structure
- Update parent plan with links
- Validate token efficiency

---

## Measuring Success

### Metrics

**Before Optimization**:
- Average query context: 1200 lines
- Token usage: ~3000 tokens
- AI response time: Slower due to large context

**After Optimization**:
- Average query context: 600 lines (50% reduction)
- Token usage: ~1500 tokens (50% reduction)
- AI response time: Faster due to smaller context

### Validation

Query the optimized plan with typical questions:
- "What tasks are in Phase 3?"
  - Should load: Parent (200) + Phase file (400) = 600 lines ✓
- "Give me an overview of this feature"
  - Should load: Parent only (200 lines) ✓
- "Show me backend implementation details"
  - Should load: Parent (200) + Backend phases (450) = 650 lines ✓

If queries consistently load <800 lines, optimization successful ✓

---

**Key Takeaway**: Optimize for progressive disclosure. AI agents load only what they need, when they need it. This enables working with larger features while maintaining token efficiency.
