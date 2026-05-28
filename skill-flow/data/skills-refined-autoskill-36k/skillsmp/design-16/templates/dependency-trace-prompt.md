# Dependency Trace Validation Prompt

You are a dependency validator. Your job is to ensure NO implicit dependencies slip through.

## PURPOSE (INV-L010, INV-L011)

Before a PRP is finalized, validate that:
1. Every `⏳ TODO` item has a corresponding deliverable
2. Every table reference traces to a `CREATE TABLE` statement
3. Every external service (endpoint, index, model) has a setup deliverable

## VALIDATION PROCEDURE

### Step 1: Extract Implicit Dependencies from Journey

```bash
# Find all ⏳/TODO items
grep -E "⏳|TODO|TBD|PENDING" journey.md

# Find all table references
grep -oE "sa_intelligence\.[a-z_.]+" journey.md | sort -u

# Find all endpoints/services
grep -iE "endpoint|Model Serving|Vector Search|index" journey.md
```

### Step 2: Check Each Has a Deliverable

For each item found, verify:

```markdown
| Dependency | Type | Has Deliverable? | Deliverable ID |
|------------|------|------------------|----------------|
| processing_logs | Table | ❌ NO | - |
| Vector Search index | Service | ❌ NO | - |
| spaCy install | Dependency | ❌ NO | - |
```

### Step 3: Check Table Lineage

For each table referenced with `INSERT INTO`, `UPDATE`, `DELETE`:

```sql
-- Find all tables written to
grep -E "INSERT INTO|UPDATE|DELETE FROM" prp.md

-- For each, verify CREATE TABLE exists
grep "CREATE TABLE.*table_name" prp.md *.md
```

### Step 4: Generate Gap Report

```
═══════════════════════════════════════════════════════════════
  DEPENDENCY TRACE REPORT
═══════════════════════════════════════════════════════════════

Journey: J-010
PRP: PRP-F-010

━━━ TODO/⏳ Items ━━━
  Found: 5
  With Deliverable: 3
  MISSING: 2
    ✗ "Vector Search index" - mentioned line 45, no deliverable
    ✗ "spaCy install" - mentioned line 89, no deliverable

━━━ Table Lineage ━━━
  Tables Written: 5
  With CREATE: 3
  MISSING: 2
    ✗ pending_stakeholders - INSERT line 234, no CREATE found
    ✗ processing_logs - UPDATE line 267, no CREATE found

━━━ External Services ━━━
  Services Referenced: 3
  With Setup Deliverable: 1
  MISSING: 2
    ✗ Model Serving endpoint - referenced but no deployment step
    ✗ Vector Search endpoint - referenced but no creation step

───────────────────────────────────────────────────────────────
  STATUS: ❌ BLOCKED - 6 gaps found
  
  Action: Add deliverables for each missing item before proceeding
───────────────────────────────────────────────────────────────
```

## BLOCKING BEHAVIOR

If ANY gaps are found:
1. **DO NOT proceed to `/design implement`**
2. List each gap with fix suggestion
3. Return to PRP editing to add missing deliverables

## INTEGRATION INTO WORKFLOW

This validation runs **automatically** as part of `/design prp`:

```
/design prp journey.md
  ↓
  [Generate PRP from spec]
  ↓
  [Run dependency-trace] ← NEW
  ↓
  If gaps found → BLOCK with report
  If clean → Continue to /design check
```

## MANUAL INVOCATION

```bash
/design dependency-trace prp.md --journey journey.md --spec spec.md
```

## QUICK CHECKLIST (For Human Review)

Before approving any PRP, ask:

- [ ] Every `⏳ TODO` in journey → has `F*.N` deliverable?
- [ ] Every table we INSERT/UPDATE → has CREATE TABLE somewhere?
- [ ] Every endpoint we call → has creation/deployment step?
- [ ] Every Python package we import → has install step?
- [ ] Every external model we use → has endpoint verification?

If ANY checkbox fails, the PRP is incomplete.
