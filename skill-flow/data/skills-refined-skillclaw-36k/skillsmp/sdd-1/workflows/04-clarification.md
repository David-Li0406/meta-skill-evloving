# Phase 4: Clarification Workflow

## Purpose

Resolve `[NEEDS CLARIFICATION]` markers in spec.md through structured user questions. Updates spec.md with resolved ambiguities.

**Command**: `/clarify`
**Requires**: `specs/$FEATURE/spec.md` with `[NEEDS CLARIFICATION]` markers
**Output**: Updated `specs/$FEATURE/spec.md`
**Auto-Chains**: → Phase 5 (`/plan`)

---

## Prerequisites

```bash
# Check for markers
grep -n "NEEDS CLARIFICATION" specs/$FEATURE/spec.md
```

**If no markers found**: Skip Phase 4, proceed to Phase 5.

---

## Step 1: Extract Clarification Needs

**Parse spec.md for all markers:**

```bash
grep -n "NEEDS CLARIFICATION" specs/$FEATURE/spec.md | while read line; do
  echo "Line $line needs clarification"
done
```

**Categorize by type:**

| Category | Example | Question Approach |
|----------|---------|-------------------|
| Choice | "OAuth or magic link?" | Multiple choice |
| Behavior | "What happens on timeout?" | Describe scenario |
| Constraint | "Performance requirement?" | Request specific value |
| Dependency | "Which API version?" | Research + confirm |
| Priority | "P1 or P2?" | Ranking exercise |

---

## Step 2: Batch Questions (Max 5)

**Group related clarifications:**

```markdown
## Clarification Batch 1

### Q1: Authentication Method
**Context**: FR-005 mentions user auth but method unclear
**Options**:
- A) OAuth 2.0 (Google, GitHub)
- B) Magic link via email
- C) OTP via SMS/email
- D) Username/password

### Q2: Session Duration
**Context**: NFR-002 mentions sessions but no duration
**Options**:
- A) 24 hours
- B) 7 days
- C) 30 days
- D) Custom (specify)
```

**Use AskUserQuestion tool:**

```
AskUserQuestion({
  questions: [
    {
      question: "Which authentication method should we use?",
      header: "Auth Method",
      options: [
        { label: "OAuth 2.0", description: "Google, GitHub providers" },
        { label: "Magic Link", description: "Email-based passwordless" },
        { label: "OTP", description: "SMS or email verification codes" }
      ],
      multiSelect: false
    }
  ]
})
```

---

## Step 3: Update Spec with Answers

**Replace markers with resolved content:**

**Before:**
```markdown
### FR-005: User Authentication
**Description**: User authentication via [NEEDS CLARIFICATION: OAuth or magic link?]
```

**After:**
```markdown
### FR-005: User Authentication
**Description**: User authentication via OTP (email verification codes)
**Clarified**: 2025-12-30 - User selected OTP over OAuth for simplicity
```

---

## Step 4: Verify All Resolved

```bash
# Count remaining markers
remaining=$(grep -c "NEEDS CLARIFICATION" specs/$FEATURE/spec.md)

if [ "$remaining" -gt 0 ]; then
  echo "ERROR: $remaining markers still unresolved"
  echo "Run /clarify again"
else
  echo "SUCCESS: All clarifications resolved"
fi
```

---

## Step 5: Document Clarification Log

**Add to spec.md:**

```markdown
---

## Clarification Log

| Date | Item | Question | Answer | Answered By |
|------|------|----------|--------|-------------|
| 2025-12-30 | FR-005 | Auth method? | OTP via email | User |
| 2025-12-30 | NFR-002 | Session duration? | 7 days | User |
```

---

## Quality Gates

| Gate | Requirement | Check |
|------|-------------|-------|
| All Resolved | Zero [NEEDS CLARIFICATION] markers | grep returns 0 |
| Documented | Clarification log updated | Log section exists |
| Consistent | Answers don't conflict with other FRs | Review related requirements |

---

## Iteration Rules

**If new clarifications arise:**

1. Add new `[NEEDS CLARIFICATION]` marker
2. Run `/clarify` again
3. Maximum 3 clarification iterations per spec
4. If still unclear after 3 iterations, escalate to user

---

## Handoff to Phase 5

**After all clarifications resolved:**

```markdown
## Phase 4 → Phase 5 Handoff

✅ All [NEEDS CLARIFICATION] markers resolved
✅ Clarification log updated
✅ spec.md internally consistent
✅ No new ambiguities introduced

**Automatically invoking**: /plan
```

---

## Common Mistakes

| Mistake | Impact | Prevention |
|---------|--------|------------|
| Skipping clarification | Ambiguous implementation | Always check for markers |
| Too many questions | User fatigue | Batch to max 5 |
| Vague answers | New ambiguity | Request specific choices |
| Not documenting | Lost context | Always update log |

---

## Version

**Version**: 1.0.0
**Last Updated**: 2025-12-30
