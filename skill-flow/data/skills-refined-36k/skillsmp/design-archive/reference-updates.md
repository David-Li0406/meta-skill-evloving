# Cross-Reference Updates

Guidelines for updating cross-references when archiving design documentation.

## Overview

When archiving a design document, all references to it must be updated to:

1. Prevent broken links
2. Point users to current documentation
3. Maintain documentation integrity
4. Preserve historical context when appropriate

## Finding References

### Step 1: Search Design Docs

Use grep to find all references in design documentation:

```bash
# Search for references to the archived doc
grep -r "archived-doc.md" .claude/design/
```

**Search patterns:**

- Exact filename: `grep -r "archived-doc.md"`
- With path: `grep -r "module/archived-doc.md"`
- Without extension: `grep -r "archived-doc"` (catches various references)

### Step 2: Search CLAUDE.md Files

Check all CLAUDE.md files for references:

```bash
# Root CLAUDE.md
grep "archived-doc.md" CLAUDE.md

# Module CLAUDE.md
grep "archived-doc.md" pkgs/*/CLAUDE.md

# All CLAUDE.md files
find . -name "CLAUDE.md" -exec grep -l "archived-doc.md" {} \;
```

### Step 3: Check for Indirect References

Look for references by topic, not just filename:

```bash
# Search for topic mentions
grep -ri "cache optimization" .claude/design/
grep -ri "caching strategy" .claude/design/
```

## Reference Types

### Type 1: Frontmatter References

References in `related` or `dependencies` arrays:

#### Type 1 Example

```yaml
---
related:
  - ./archived-doc.md
  - ./other-doc.md
dependencies:
  - ./archived-doc.md
---
```

### Type 2: Markdown Links

Direct links in document content:

#### Type 2 Example

```markdown
See [Cache Design](./archived-doc.md) for details.

For caching strategy, refer to the [optimization guide](./archived-doc.md).
```

### Type 3: CLAUDE.md Pointers

References in CLAUDE.md files:

#### Type 3 Example

```markdown
**For cache optimization:**
→ `@./.claude/design/module/archived-doc.md`

Load when working on caching.
```

## Update Strategies

### Strategy 1: Replace with Replacement Doc

When archival reason is "superseded", replace with new doc:

#### Strategy 1 Before

```yaml
related:
  - ./old-cache-design.md
```

#### Strategy 1: After

```yaml
related:
  - ./cache-optimization.md
```

**Apply to:**

- All frontmatter references
- Most markdown links
- CLAUDE.md pointers

### Strategy 2: Add Archive Note

Keep reference but note it's archived:

#### Strategy 2 Before

```yaml
related:
  - ./legacy-api.md
```

#### Strategy 1 After

```yaml
related:
  - ./legacy-api.md  # archived, see api-v2.md for current
```

**Apply to:**

- Historical references
- Context-preserving situations
- When both old and new are relevant

### Strategy 3: Remove Reference

Remove if no longer relevant:

#### Strategy 3 Before

```yaml
related:
  - ./obsolete-patterns.md
  - ./current-patterns.md
```

#### Strategy 2 After

```yaml
related:
  - ./current-patterns.md
```

**Apply to:**

- Truly obsolete information
- No replacement exists
- Reference adds no value

### Strategy 4: Update Path (If Moved)

If doc moved to _archive directory:

#### Strategy 4 Before

```yaml
related:
  - ./archived-doc.md
```

#### Strategy 3 After

```yaml
related:
  - ./_archive/archived-doc.md  # archived
```

**Apply to:**

- When keeping historical references
- Archive directory used
- Maintaining documentation trail

## Update Workflow

### For Each Referencing Document

1. **Read the document**

   ```bash
   # Use Read tool
   Read: .claude/design/module/referencing-doc.md
   ```

2. **Identify reference type**

   - Frontmatter: `related` or `dependencies`
   - Content: Markdown link
   - Both

3. **Determine update strategy**

   - Superseded → Replace with new doc
   - Deprecated → Add note, keep accessible
   - Obsolete → Remove or add note
   - Completed → Replace with final docs

4. **Apply update**

   ```bash
   # Use Edit tool
   Edit: .claude/design/module/referencing-doc.md
   old_string: "  - ./archived-doc.md"
   new_string: "  - ./replacement-doc.md"
   ```

5. **Validate**

   - Reference points to valid doc
   - Path is correct
   - Context still makes sense

## Frontmatter Updates

### Update Related Array

#### Example: Superseded

```yaml
# Before
related:
  - ./old-architecture.md
  - ./performance.md

# After
related:
  - ./architecture.md  # replaces old-architecture.md
  - ./performance.md
```

#### Example: Deprecated with Note

```yaml
# Before
related:
  - ./legacy-api.md

# After
related:
  - ./legacy-api.md  # deprecated, migrating to api-v2.md
  - ./api-v2.md
```

### Update Dependencies Array

#### Example: Replace

```yaml
# Before
dependencies:
  - ./old-cache-design.md

# After
dependencies:
  - ./cache-optimization.md
```

#### Example: Remove

```yaml
# Before
dependencies:
  - ./obsolete-implementation.md
  - ./current-implementation.md

# After
dependencies:
  - ./current-implementation.md
```

## Content Link Updates

### Replace Link

#### Replace Link: Before

```markdown
For caching details, see [Cache Design](./old-cache-design.md).
```

#### Strategy 4 After

```markdown
For caching details, see [Cache Optimization](./cache-optimization.md).
```

### Add Archive Note to Link

#### Add Archive Note: Before

```markdown
The [original design](./legacy-design.md) describes the v1 approach.
```

#### Add Archive Note: After

```markdown
The [original design](./legacy-design.md) (archived) describes the v1
approach. See [current design](./design-v2.md) for v2.
```

### Remove Link

#### Remove Link: Before

```markdown
This builds on patterns from [obsolete patterns](./obsolete-patterns.md)
and [current patterns](./current-patterns.md).
```

#### Remove Link: After

```markdown
This builds on patterns from [current patterns](./current-patterns.md).
```

## CLAUDE.md Updates

### Replace Pointer

#### Replace Pointer: Before

```markdown
**For cache optimization:**
→ `@./.claude/design/module/old-cache-design.md`

Load when working on caching.
```

#### Replace Pointer: After

```markdown
**For cache optimization:**
→ `@./.claude/design/module/cache-optimization.md`

Load when working on caching.
```

### Remove Pointer

#### Remove Pointer: Before

```markdown
**For cache optimization:**
→ `@./.claude/design/module/old-cache-design.md`

**For performance:**
→ `@./.claude/design/module/performance.md`
```

#### Remove Pointer: After

```markdown
**For performance:**
→ `@./.claude/design/module/performance.md`
```

### Add Archive Note

#### CLAUDE.md Add Archive Note: Before

```markdown
**For legacy API:**
→ `@./.claude/design/module/legacy-api.md`
```

#### CLAUDE.md Add Archive Note: After

```markdown
**For legacy API (archived):**
→ `@./.claude/design/module/legacy-api.md` (deprecated, see api-v2.md)

**For current API:**
→ `@./.claude/design/module/api-v2.md`
```

## Special Cases

### Bidirectional References

When archived doc is referenced by another doc, and vice versa:

#### Doc A (being archived)

```yaml
related:
  - ./doc-b.md
```

#### Doc B (active)

```yaml
related:
  - ./doc-a.md  # being archived
```

#### Action

1. Update Doc B to point to replacement
2. Keep Doc A's reference to Doc B (still valid)
3. Add archive notice to Doc A

#### Result

#### Doc A (archived)

```yaml
status: archived
related:
  - ./doc-b.md
```

#### Doc B (updated)

```yaml
related:
  - ./doc-a-replacement.md  # replaces doc-a.md
```

### Chain of References

When multiple docs reference each other in a chain:

#### Chain References Example

- Doc A references Doc B (being archived)
- Doc B references Doc C
- Doc C references Doc A

#### Chain References Action

1. Update Doc A: B → B replacement
2. Archive Doc B with notice
3. Update Doc C: B → B replacement (if referenced)

### Circular References

Archived doc and active doc both reference each other:

#### Circular References: Before

- archived-doc.md → active-doc.md
- active-doc.md → archived-doc.md

#### Circular References: After

- archived-doc.md → active-doc.md (keep)
- active-doc.md → replacement-doc.md (update)

## Batch Updates

When archiving affects many docs, use systematic approach:

### Step 1: List All References

```bash
grep -r "archived-doc.md" .claude/design/ > references.txt
```

### Step 2: Categorize by Update Type

- **Replace:** References that should point to replacement
- **Note:** References that should note archival
- **Remove:** References that should be deleted

### Step 3: Update in Order

1. Update frontmatter references first
2. Then content links
3. Finally CLAUDE.md files

### Step 4: Validate All Updates

```bash
# Check no broken links remain
grep -r "archived-doc.md" .claude/design/

# Validate replacement doc exists
ls .claude/design/module/replacement-doc.md
```

## Validation

### After Updates, Verify

#### Check 1: No broken links

```bash
# Should return only the archived doc itself
grep -r "archived-doc.md" .claude/design/
```

#### Check 2: Replacement exists

```bash
# If superseded, verify replacement
ls .claude/design/module/replacement-doc.md
```

#### Check 3: References make sense

- Read updated docs
- Ensure context still valid
- Check links work
- Verify frontmatter arrays correct

#### Check 4: CLAUDE.md updated

```bash
# Should not reference archived doc (unless noted as archived)
grep "archived-doc.md" CLAUDE.md
grep "archived-doc.md" pkgs/*/CLAUDE.md
```

## Error Prevention

### Common Mistakes

#### Mistake 1: Forgetting path updates

```yaml
# Wrong - path unchanged after moving to archive
related:
  - ./archived-doc.md

# Correct - path updated
related:
  - ./_archive/archived-doc.md  # archived
```

#### Mistake 2: Breaking context

```markdown
<!-- Wrong - removing reference breaks understanding -->
This builds on the cache design.

<!-- Correct - keeping context with note -->
This builds on the [cache design](./cache-optimization.md) (previously
old-cache-design.md, now archived).
```

#### Mistake 3: Incomplete updates

- Updated frontmatter but not content links
- Updated design docs but not CLAUDE.md
- Updated some references but not all

#### Prevention

- Use systematic search and update process
- Track all references before starting updates
- Validate all updates after completion

## Summary Report

After completing reference updates, report:

```markdown
## Cross-Reference Updates

**Documents Updated:** 5

### Frontmatter Updates

- module/doc-a.md: replaced reference
- module/doc-b.md: added archive note
- module/doc-c.md: removed reference

### Content Link Updates

- module/doc-d.md: updated 2 links
- module/doc-e.md: removed 1 link

### CLAUDE.md Updates

- CLAUDE.md: removed pointer
- pkgs/module/CLAUDE.md: replaced pointer

**Validation:**

- ✅ No broken links remaining
- ✅ All replacements exist
- ✅ Context preserved where needed
```
