# Dangerous Mode: Complete Example Walkthrough

Step-by-step walkthrough of PRP-001 → PRP-003 learning cycle with real learnings, confidence scores, and invariant creation.

---

## PRP-001: Forecast Dashboard (Weeks 1-2)

### Phase 1: Spec & Validation

**Tuesday, 2026-01-20**

```markdown
# Dashboard Spec

Build a forecast dashboard for SA managers to view pipeline opportunities.

## Requirements

1. Display forecast opportunities by account
2. Filter by stage, days until close, revenue
3. Show confidence scores and risk indicators
4. Real-time update capability
5. Export to CSV

## Success Criteria

- Load 100 opportunities in <2s
- Filter responsiveness: <500ms
- Route coverage: 100% (all internal links tested)
- Accessibility: WCAG 2.1 AA
```

**Wednesday, 2026-01-20 - Validation**

```bash
$ /design validate specs/dashboard.md

Checking Universal Invariants (1-11)...
  [1] Ambiguity is Invalid............... PASS
      └─ All metrics defined (e.g., "load < 2s")
  [2] State Must Be Explicit............ PASS
  ...
  [10] Degradation Path Exists.......... PASS
      └─ Fallback to cached data if API down

Learned Invariants (0 - none yet)
  └─ No learned invariants in system yet

RESULT: PASS ✓
Ready for PRP compilation
```

```bash
$ /design prp specs/dashboard.md

# Generated: PRP-2026-01-22-001

prp_id: PRP-2026-01-22-001
name: Forecast Dashboard v1.0
domain: consumer-product
confidence_score: 7.2

validated_against_invariants:
  universal: [1-11] PASS
  domain: PASS
  learned: (none yet)

phases:
  phase_1_design: 4 hours
  phase_2_implementation: 8 hours
  phase_3_testing: 4 hours
  total: 16 hours
```

---

### Phase 2: Execution (Step by Step)

**Thursday, 2026-01-21**

```bash
$ /design run --dangerous PRP-2026-01-22-001.yaml
```

#### Step 1: Design Data Model

```
Executing Step 1 (Design data model)...

Task: prp-001-step-1
Status: IN PROGRESS

Actions:
  ├─ Define Opportunity schema
  ├─ Define Account schema
  ├─ Define User schema
  ├─ Plan database indexes
  └─ Document relationships

Completion: ✓ DONE (1.5 hours)

Learnings captured: None
Status: Ready for Step 2
```

#### Step 2: Implement API Endpoints

```
Executing Step 2 (Implement API endpoints)...

Task: prp-001-step-2
Status: IN PROGRESS

Actions:
  ├─ GET /api/forecast → List opportunities
  ├─ GET /api/forecast/{id} → Single opportunity
  ├─ POST /api/forecast/filter → Filtered list
  ├─ GET /api/forecast/export → CSV export
  └─ Add error handling + logging

Completion: ✓ DONE (3 hours)

Learnings captured: None
Status: Ready for Step 3
```

#### Step 3: Build UI Routes

```
Executing Step 3 (Build UI routes)...

Task: prp-001-step-3
Status: IN PROGRESS

Actions:
  ├─ Create /forecast route → Dashboard page
  ├─ Create /forecast/{id} route → Opportunity detail
  ├─ Create /account/{name} route → Account summary
  ├─ Add breadcrumb links
  ├─ Test route navigation
  └─ Verify 404 handling

Completion: ✓ DONE (2.5 hours)

Task: generate-learning-LEARN-2026-01-23-001
Status: IN PROGRESS

Learning Captured:
┌──────────────────────────────────────────────────────┐
│ LEARNING_ID: LEARN-2026-01-23-001                   │
├──────────────────────────────────────────────────────┤
│ TITLE: Internal Links Must Have Route Handlers      │
│                                                       │
│ OBSERVATION:                                         │
│ When building Dash SPA with dcc.Link components,    │
│ every internal href (e.g., href="/account/...")    │
│ MUST have a matching route callback. If the route   │
│ doesn't exist, users see "Page not found" instead   │
│ of the target page. This causes poor UX.            │
│                                                       │
│ CONTEXT:                                             │
│ - Observed in this implementation                    │
│ - Links: /forecast/{id}, /account/{name}           │
│ - Routes verified with Playwright clicks            │
│ - All routes loaded correctly                        │
│                                                       │
│ CONFIDENCE ANALYSIS:                                 │
│ Confidence Score: 0.95                              │
│                                                       │
│ Reasoning:                                           │
│   - Observed in Dash documentation (SPA pattern)    │
│   - React Router / Next.js have same requirement    │
│   - Tested in this project (validation passed)      │
│   - Pattern is universal for client-side SPAs       │
│                                                       │
│ APPLIES TO:                                          │
│   ├─ Domain: consumer-product                       │
│   ├─ Framework: Dash, React Router, Next.js         │
│   ├─ Phase: implementation, validation              │
│   └─ Excludes: Server-side-rendered apps           │
│                                                       │
│ VALIDATION METHOD:                                   │
│   1. Extract all href= from Link components         │
│   2. List all route handlers in router/callbacks    │
│   3. Verify each href has a handler                 │
│   4. Playwright test: click each link, verify load  │
│                                                       │
└──────────────────────────────────────────────────────┘

Dangerous Mode Decision:
  ├─ Confidence: 0.95
  ├─ Threshold: >= 0.80
  ├─ Decision: ✓ PROMOTE to system invariant
  ├─ Action: Create INV-L001
  └─ Status: Auto-promotion triggered

Task: promote-invariant-INV-L001
Status: IN PROGRESS
├─ Generate invariant ID: INV-L001
├─ Create invariant metadata
├─ Add to learned-invariants.md
├─ Register globally
└─ Mark task completed

Invariant Created:
┌──────────────────────────────────────────────────────┐
│ INV-L001: Route Coverage                             │
│                                                       │
│ ID: INV-L001                                         │
│ Status: ACTIVE                                       │
│ Confidence: 0.95                                     │
│ Source: PRP-2026-01-22-001 / Step 3                │
│ Created: 2026-01-23T14:22:30Z                       │
│                                                       │
│ RULE:                                                │
│ Every internal link (href) in UI components must    │
│ have a corresponding route handler.                 │
│                                                       │
│ VALIDATION:                                          │
│   1. Extract all href from components               │
│   2. Verify route handler exists                    │
│   3. Playwright test: click → verify page loads     │
│                                                       │
│ ENFORCEMENT:                                         │
│ PRPs targeting consumer-product + implementation    │
│ phase MUST include route coverage test in gates.    │
│ Violation: PRP rejected until test added.           │
│                                                       │
│ VERSION HISTORY:                                    │
│   v1.0 (2026-01-23): Initial creation              │
│   confidence: 0.95                                   │
│   status: ACTIVE                                     │
└──────────────────────────────────────────────────────┘

Task: promote-invariant-INV-L001
Status: COMPLETED ✓
└─ Invariant INV-L001 registered globally
└─ Future /design validate commands will check this
```

#### Step 4: Add Filtering

```
Executing Step 4 (Add filtering)...

Task: prp-001-step-4
Status: IN PROGRESS

Actions:
  ├─ Implement stage filter (Validating → Live)
  ├─ Implement days_until_close filter (≤14, ≤30, ≤90)
  ├─ Implement revenue range filter
  ├─ Test filter interactions
  └─ Test edge cases

Completion: ✓ DONE (2.5 hours)

During implementation, edge case discovered:

Filter code v1 (WRONG):
```python
soon_closing = [
    uc for uc in usecases
    if uc.get('days_until_close') <= 14
]
```

Problem: When days_until_close is NEGATIVE (past close date),
         it satisfies <= 14 comparison!
         So completed/closed deals appear in "soon closing" filter

Filter code v2 (CORRECT):
```python
soon_closing = [
    uc for uc in usecases
    if uc.get('stage') in ACTIVE_STAGES      # Exclude closed
    and 0 < uc.get('days_until_close', 999) <= 14  # Positive + bounded
]
```

Task: generate-learning-LEARN-2026-01-23-002
Status: IN PROGRESS

Learning Captured:
┌──────────────────────────────────────────────────────┐
│ LEARNING_ID: LEARN-2026-01-23-002                   │
├──────────────────────────────────────────────────────┤
│ TITLE: Filters Must Handle Negative Values          │
│        and Lifecycle States                          │
│                                                       │
│ OBSERVATION:                                         │
│ Date filters like "days_until_close <= 14" fail    │
│ when days_until_close is negative (past dates).     │
│ Filters must explicitly:                            │
│   1. Exclude negative values (past dates)           │
│   2. Exclude terminal states (closed, live)         │
│                                                       │
│ CONTEXT:                                             │
│ - Found this bug in Step 4 filter implementation    │
│ - Closed opportunities appeared in "soon closing"   │
│ - Fixed by requiring: stage in ACTIVE + positive days
│                                                       │
│ CONFIDENCE ANALYSIS:                                 │
│ Confidence Score: 0.92                              │
│                                                       │
│ Reasoning:                                           │
│   - Clear logic error (negative <= positive always) │
│   - Matches lifecycle state patterns                │
│   - Observed in another Dash project                │
│   - Pattern applies to date/time filters generally  │
│                                                       │
│ APPLIES TO:                                          │
│   ├─ Domain: consumer-product, data-architecture   │
│   ├─ Phase: implementation, validation              │
│   └─ Any filter with: dates, numeric ranges        │
│                                                       │
│ VALIDATION METHOD:                                   │
│   1. For date filters: test with past dates         │
│   2. For state filters: test with terminal states   │
│   3. Verify filter output excludes both             │
│                                                       │
└──────────────────────────────────────────────────────┘

Dangerous Mode Decision:
  ├─ Confidence: 0.92
  ├─ Threshold: >= 0.80
  ├─ Decision: ✓ PROMOTE to system invariant
  ├─ Action: Create INV-L002
  └─ Status: Auto-promotion triggered

Invariant Created:
┌──────────────────────────────────────────────────────┐
│ INV-L002: Filter Logic Must Handle Edge Cases      │
│                                                       │
│ ID: INV-L002                                         │
│ Status: ACTIVE                                       │
│ Confidence: 0.92                                     │
│ Source: PRP-2026-01-22-001 / Step 4                │
│ Created: 2026-01-23T16:45:00Z                       │
│                                                       │
│ RULE:                                                │
│ Date/time filters must explicitly handle negative   │
│ values (past dates) and lifecycle states.           │
│                                                       │
│ EXAMPLE - VIOLATION:                                │
│   soon_closing = [uc for uc in usecases            │
│                   if uc.get('days_until_close') <= 14]
│   └─ Problem: Includes negative days (closed deals) │
│                                                       │
│ EXAMPLE - CORRECT:                                  │
│   soon_closing = [uc for uc in usecases            │
│       if uc.get('stage') in ACTIVE_STAGES          │
│       and 0 < uc.get('days_until_close', 999) <= 14]
│   └─ Excludes: past dates AND terminal states      │
│                                                       │
│ VALIDATION:                                          │
│   1. Test with items: past dates (negative days)   │
│   2. Test with items: terminal states (closed)     │
│   3. Verify filter excludes both                    │
│                                                       │
│ ENFORCEMENT:                                         │
│ PRPs with filters MUST test edge cases:            │
│   - Date filters: negative/past dates              │
│   - State filters: terminal states                  │
│ Violation: PRP rejected until edge case test added.│
│                                                       │
│ VERSION HISTORY:                                    │
│   v1.0 (2026-01-23): Initial creation              │
│   confidence: 0.92                                   │
│   status: ACTIVE                                     │
└──────────────────────────────────────────────────────┘

Task: promote-invariant-INV-L002
Status: COMPLETED ✓
└─ Invariant INV-L002 registered globally
```

#### Step 5: Test & Validate

```
Executing Step 5 (Test and validate)...

Task: prp-001-step-5
Status: IN PROGRESS

Actions:
  ├─ Route coverage test (all hrefs tested) ✓
  │  └─ Respects INV-L001 (routes must have handlers)
  ├─ Filter edge case test (negative dates, terminal states) ✓
  │  └─ Respects INV-L002 (filter edge case handling)
  ├─ Performance test (100 opportunities < 2s) ✓
  ├─ Accessibility test (WCAG 2.1 AA) ✓
  ├─ Error handling test ✓
  └─ Integration test ✓

Completion: ✓ DONE (4 hours)

Status: Ready for retrospective
```

---

### Phase 3: Retrospective

**Friday, 2026-01-23**

```bash
$ /design retrospective PRP-2026-01-22-001

Retrospective: PRP-2026-01-22-001 (Forecast Dashboard)
```

**Section 5: System Improvements**

```markdown
### 5.2 Missing Invariants

The bugs we caught during execution point to missing system invariants.
We successfully created two:

1. **INV-L001: Route Coverage**
   - Why it was missing: Not obvious until multiple projects
   - When we would have caught it: Design-time route validation
   - Impact if we had this earlier: Prevented 404 errors

2. **INV-L002: Filter Logic Edge Cases**
   - Why it was missing: Subtle logic errors (negative values)
   - When we would have caught it: Pre-mortem on filter requirements
   - Impact if we had this earlier: Prevented filter pollution

### 5.3 CONVENTIONS.md Updates

Added to CONVENTIONS.md - SPA Section:

```
## Single-Page Apps (SPA) Pattern

1. **Route Coverage (INV-L001)**
   Every internal href must have a matching route.
   Test with Playwright: click each link, verify page loads.

2. **Filter Edge Cases (INV-L002)**
   Date filters must handle: negative days, past dates.
   State filters must explicitly exclude: closed, live, terminal.
   Test all edge cases before merging.
```

### 5.5 Validation Command Improvements

Added new validation command:

```bash
validate-route-coverage.sh
  ├─ Extract all href from components
  ├─ List all route handlers
  ├─ Verify 1:1 mapping
  └─ Exit code: 0 if coverage 100%, 1 if gaps
```

---

**Final Assessment**

System now has **2 learned invariants** that will guide future PRPs.

Next PRP (search feature) will be faster because:
  - Route coverage test already planned (respects INV-L001)
  - Filter edge cases will be tested upfront (respects INV-L002)
  - Design-time validation will catch these issues before execution
```

---

## PRP-002: Search Features (Week 2-3)

### Phase 1: Spec with Invariant References

**Monday, 2026-01-25**

```markdown
# Search Feature Spec

Add search + filtering to dashboard.

## Requirements

1. Search opportunities by account, owner, stage
2. Real-time search results (<500ms)
3. Filter: stage, days until close, revenue
4. Pagination for large result sets (100K+)
5. Search API with proper error handling

## Success Criteria

- Search latency: <500ms
- **Route coverage: 100% (INV-L001)**
  └─ All search routes (/search, /search/{query}) tested
- **Filter edge cases handled (INV-L002)**
  └─ Negative dates tested, terminal states excluded
- Pagination: 1000+ records supported
- Cache hit rate: >70%
```

**Validation**

```bash
$ /design validate specs/search.md --include-learned

Checking Universal Invariants (1-11)...
  [1-11] ✓ PASS

Checking Learned Invariants...
  [INV-L001] Route Coverage............... PASS
    └─ Spec includes route test plan ✓

  [INV-L002] Filter Logic Edge Cases..... PASS
    └─ Spec tests for negative dates ✓

RESULT: PASS ✓
PRP-2 respects learned constraints from PRP-1
```

---

### Phase 2: Execution (Abridged)

**Tuesday-Wednesday, 2026-01-25-26**

```
/design run --dangerous PRP-2026-01-25-002.yaml

Step 1: Design search schema
  └─ ✓ COMPLETE

Step 2: Implement search API
  Observations:
    - Large result sets (100K) cause slow queries
    - Solution: Pagination + index optimization

  Learning captured:
    LEARN-2026-01-25-003: "Large search results need pagination"
    Confidence: 0.91
    Decision: PROMOTE → INV-L003

Step 3: Build search UI routes
  Validation:
    ✓ INV-L001 respected (routes + test)
    ✓ INV-L002 respected (filters edge-case tested)

Step 4: Add filter/sort controls
  Observations:
    - Search results cached for performance
    - When data changes, cache becomes stale
    - Solution: Invalidate cache on data mutations

  Learning captured:
    LEARN-2026-01-25-004: "Cache invalidation on updates"
    Confidence: 0.87
    Decision: PROMOTE → INV-L004

Step 5: E2E testing
  ✓ All routes working
  ✓ All filters edge-case tested
  ✓ Pagination verified
  ✓ Cache invalidation working

EXECUTION COMPLETE
Learned 2 new invariants: INV-L003, INV-L004
```

---

## PRP-003: Admin Dashboard (Week 3-4)

### Phase 1: Spec with 4 Inherited Constraints

**Monday, 2026-01-26**

```markdown
# Admin Dashboard Spec

Admin tools for account management and oversight.

## Success Criteria

- **Route coverage: 100% (INV-L001)**
- **Filter edge cases (INV-L002)**
- **Pagination for admin tables (INV-L003)**
- **Cache invalidation on admin actions (INV-L004)**
- Admin-only access (RBAC)
- Audit logging for all admin actions
```

**Validation**

```bash
$ /design validate specs/admin.md --include-learned

Checking Core Invariants (1-11)............ PASS
Checking Learned Invariants (INV-L001-L004)
  [INV-L001] Route Coverage ........... PASS
    └─ Admin routes have tests
  [INV-L002] Filter Edge Cases ....... PASS
    └─ Admin filters test edge cases
  [INV-L003] Pagination .............. PASS
    └─ Admin tables paginated
  [INV-L004] Cache Invalidation ...... PASS
    └─ Admin actions invalidate caches

RESULT: PASS ✓
PRP-3 respects all 4 learned constraints
```

---

### Phase 2: Execution (Abridged)

```
/design run --dangerous PRP-2026-01-26-001.yaml

Step 1: Design admin schema
  └─ ✓ COMPLETE

Step 2: Implement admin APIs
  Validation:
    ✓ INV-L001: Routes tested
    ✓ INV-L004: Cache invalidation

Step 3: Build admin UI
  Observations:
    - Admin pages need role-based access control
    - Users without admin role shouldn't see links
    - Different from data-level filtering

  Learning captured:
    LEARN-2026-01-26-005: "RBAC needed for admin UI"
    Confidence: 0.88
    Decision: PROMOTE → INV-L005

Step 4: Add admin filters
  Validation:
    ✓ INV-L002: Filter edge cases
    ✓ INV-L003: Pagination

Step 5: Add audit logging
  Observations:
    - Every admin action must be logged:
      * WHO (user_id)
      * WHAT (action type)
      * WHEN (timestamp)
      * CHANGED (before/after state)
    - Regulatory requirement for HLS apps

  Learning captured:
    LEARN-2026-01-26-006: "Audit log structure"
    Confidence: 0.93
    Decision: PROMOTE → INV-L006

Step 6: Testing
  ✓ All 4 inherited invariants respected
  ✓ RBAC working
  ✓ Audit logs complete

EXECUTION COMPLETE
Learned 2 new invariants: INV-L005, INV-L006
```

---

## System State After 3 PRPs

### Learned Invariants Registry

```
Created: 6 system invariants

INV-L001: Route Coverage
  confidence: 0.95 (from PRP-1)
  validations: 3 (PRP-1, PRP-2, PRP-3)
  violations: 0
  status: ACTIVE

INV-L002: Filter Logic Edge Cases
  confidence: 0.92 (from PRP-1)
  validations: 3 (PRP-1, PRP-2, PRP-3)
  violations: 0
  status: ACTIVE

INV-L003: Large Result Set Pagination
  confidence: 0.91 (from PRP-2)
  validations: 2 (PRP-2, PRP-3)
  violations: 0
  status: ACTIVE

INV-L004: Cache Invalidation on Update
  confidence: 0.87 (from PRP-2)
  validations: 2 (PRP-2, PRP-3)
  violations: 0
  status: ACTIVE

INV-L005: Role-Based Access Control
  confidence: 0.88 (from PRP-3)
  validations: 1 (PRP-3)
  violations: 0
  status: ACTIVE (needs more validation)

INV-L006: Audit Logging Structure
  confidence: 0.93 (from PRP-3)
  validations: 1 (PRP-3)
  violations: 0
  status: ACTIVE (needs more validation)

Total: 6 active invariants
System Learning Velocity: 2 per PRP
Overall Confidence: 0.91 (average)
```

### Future PRP-004 Benefits

When PRP-4 is created, it will:
- Validate against 6 learned constraints (design-time)
- Execute faster (learned patterns already known)
- Avoid known edge cases (learned from PRP-1, 2, 3)
- Catch violations early (stress-test against 6 invariants)

---

## Key Insights from Walkthrough

### 1. **Dangerous Mode Accelerates Learning**
- PRP-1: 0 constraints, learn 2 invariants (baseline)
- PRP-2: 2 constraints, learn 2 more invariants
- PRP-3: 4 constraints, learn 2 more invariants
- Each cycle learns WHILE respecting prior learnings

### 2. **Confidence Compounds**
- INV-L001 starts at 0.95, validated by 3 PRPs
- INV-L002 starts at 0.92, validated by 3 PRPs
- By PRP-3, these are high-confidence patterns

### 3. **Design-Time Validation Prevents Issues**
- PRP-2 validation catches potential route issues before execution
- PRP-3 validation catches filter edge cases before implementation
- Stress-test makes violations explicit

### 4. **Execution is Faster**
- PRP-1: 16 hours (learning from scratch)
- PRP-2: 14 hours (2 hour savings, respects 2 constraints)
- PRP-3: 12 hours (4 hour savings, respects 4 constraints)
- Dangerous mode compounds efficiency gains

### 5. **System Knowledge is Permanent**
- Once INV-L001 created, all future PRPs must respect it
- No need to re-learn the same lesson
- Knowledge builds across projects and teams

---

*Example Walkthrough v1.0*
*Based on realistic SA Intelligence Platform use cases*
