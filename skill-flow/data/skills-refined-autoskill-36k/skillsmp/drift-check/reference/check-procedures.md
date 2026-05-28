# Drift Check Procedures

Detailed procedures for each check category.

## Check 1: Server Actions vs Docs

```bash
# Find all server actions
grep -r "use server" app/actions/ --include="*.ts" -l

# For each action file, verify documented in feature docs
# Cross-reference with Server Actions tables
```

**Drift indicators:**
- Action exists in code but not in any feature doc
- Action documented but doesn't exist
- Action signature/behavior changed but doc not updated

## Check 2: Routes vs User Surfaces

```bash
# Find all routes (Next.js App Router)
find app -name "page.tsx" -o -name "route.ts"

# Cross-reference with User Surfaces tables in feature docs
```

**Drift indicators:**
- Route exists but not in User Surfaces
- Route documented but file doesn't exist
- Route moved but doc shows old path

## Check 3: Schema vs Data Model

```bash
# Get current schema
supabase db dump --schema-only

# Or check migration files
ls supabase/migrations/

# Cross-reference with Data Model sections
```

**Drift indicators:**
- Table/column exists but not documented
- Documented table/column doesn't exist
- Column type or constraints changed

## Check 4: RLS vs Permissions Docs

```bash
# Check RLS policies
supabase db dump --schema-only | grep -A 10 "CREATE POLICY"

# Cross-reference with Permissions & Security sections
```

**Drift indicators:**
- Policy exists but not documented
- Documented policy doesn't exist
- Policy behavior changed

## Check 5: Invariants vs Reality

For each documented invariant:
- Can you find code that enforces it?
- Are there code paths that violate it?
- Has the business rule changed?

## Check 6: Workflow Steps vs UI

For each workflow doc:
- Do the documented steps still work?
- Are there new steps not documented?
- Have buttons/links/navigation changed?

## Deep Check Process

### Action Audit
```
For each file in app/actions/:
  - Extract exported functions
  - Find which feature doc should own it
  - Verify it's in the Server Actions table
  - Verify signature matches
```

### Route Audit
```
For each page.tsx in app/:
  - Extract the route path
  - Find which feature doc should own it
  - Verify it's in User Surfaces
  - Verify description is accurate
```

### Schema Audit
```
For each table in database:
  - Find which feature doc(s) reference it
  - Verify columns match Data Model
  - Verify RLS policies documented
```

### Invariant Audit
```
For each documented invariant:
  - Search code for enforcement
  - Search for violations
  - Flag if can't find enforcement
```
