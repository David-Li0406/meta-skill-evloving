# Phase 1: Load Input Spec

**Purpose**: Extract requirements and constraints from feature specifications or bug reports.

---

## Step 1.1: Determine Input Type

**Input Options**:

1. **feature-spec.md** - For new features
   - Location: `specs/<feature-id>/spec.md`
   - Format: User stories, functional requirements, success criteria
   - Article IV: Specification-First - spec.md MUST exist before planning

2. **bug-report.md** - For bug fixes
   - Location: `docs/bugs/YYYYMMDD-HHMM-bug-<id>.md`
   - Format: Symptom, root cause, fix strategy (from debug-issues skill)
   - Error evidence with file:line references

3. **Natural language** - If neither exists
   - User provides rough requirements
   - Create spec.md first using specify-feature skill
   - Then re-run planning after spec.md exists

**Priority**: Always prefer existing spec.md or bug-report.md over natural language. If neither exists, create spec first (Article IV enforcement).

---

## Step 1.2: Extract Requirements

**From feature-spec.md**:
```markdown
Requirements:
- REQ-001: Users can log in with Google OAuth
- REQ-002: Sessions persist for 7 days
- REQ-003: Users can log out

Constraints:
- Must use existing auth infrastructure
- No breaking changes to current login flow
- Timeline: 2 weeks

Success Criteria:
- OAuth integration complete
- Session management working
- Logout clears all tokens
```

**From bug-report.md**:
```markdown
Root Cause:
- File: src/pricing/calculator.ts:62
- Function: calculateTotal()
- Issue: Division by zero when discount is 100%

Fix Strategy:
- Add validation before division
- Return 0 for 100% discount
- Add unit tests for edge cases
```

---

## Step 1.3: Validate Input Quality

**Checklist**:
- [ ] Requirements are clear and testable
- [ ] Constraints documented (timeline, scope, technical)
- [ ] Success criteria measurable
- [ ] No [NEEDS CLARIFICATION] markers (or max 3)

**If quality insufficient**:
1. For feature specs: Run clarify-specification skill
2. For bug reports: Re-run debug-issues skill with more detail
3. For natural language: Create proper spec.md first

**Article IV Enforcement**: Specification (WHAT/WHY) MUST exist before planning (HOW).

---

## Step 1.4: Load Context

**Intelligence Queries** (Article I: Intelligence-First):

```bash
# Find existing patterns
project-intel.mjs --search "auth|oauth|login" --type ts --json > /tmp/plan_existing_patterns.json

# Understand project structure
project-intel.mjs --overview --json > /tmp/plan_overview.json

# Check for similar implementations
project-intel.mjs --search "<feature-keyword>" --json > /tmp/plan_similar.json
```

**Evidence Required**:
- Save query outputs to /tmp/*.json
- Reference findings in plan (file:line format)
- CoD^Σ trace: `⇄ IntelQuery("auth") → found src/auth/session.ts:23`

---

## Step 1.5: Identify Constraints

**Technical Constraints**:
- Existing code patterns to follow
- Libraries/frameworks in use
- Database schema limitations
- API compatibility requirements

**Timeline Constraints**:
- Sprint duration
- Release deadlines
- Dependency on other teams

**Scope Constraints**:
- MVP vs full feature
- Must-have vs nice-to-have
- Resource limitations

**Document Explicitly**: All constraints affect task breakdown and estimates in Phase 2.

---

## Output of Phase 1

**Data Structure**:
```
Requirements: [REQ-001, REQ-002, REQ-003]
Constraints: [Technical, Timeline, Scope]
Success Criteria: [Measurable outcomes]
Intelligence Context: [Existing patterns from queries]
```

**Proceed to Phase 2**: Task Breakdown with AC requirements
