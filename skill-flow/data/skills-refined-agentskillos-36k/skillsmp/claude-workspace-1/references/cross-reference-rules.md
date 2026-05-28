# Cross-Reference Rules

Every workspace file MUST include cross-references to maintain connections between documentation and code.

## Required Sections

Every file MUST have a `## Related` section near the end with these subsections:

```markdown
## Related

### Codebase
- [filename.rb](../../path/to/filename.rb) - Description of relationship

### Related Documentation
- [Document Title](../category/filename.md) - Description of relationship
```

---

## Codebase Links (Required)

### Rule: At Least One Codebase Link

Every workspace file MUST link to at least one codebase file. This ensures no orphan documentation exists.

**Valid link formats:**
```markdown
- [user.rb](../../app/models/user.rb) - Primary model affected
- [auth_controller.rb](../../app/controllers/auth_controller.rb) - Implementation target
- [schema.rb](../../db/schema.rb) - Database changes documented here
```

**Path resolution:**
- From `.claude/plans/my-plan.md` to `app/models/user.rb`
- Path: `../../app/models/user.rb` (up two levels from .claude/plans/)

### What Counts as a Codebase Link

Valid targets:
- Source files (`.rb`, `.py`, `.ts`, `.js`, etc.)
- Configuration files (`.yml`, `.json`, `.toml`)
- Schema files (`schema.rb`, `schema.prisma`)
- Test files (`*_spec.rb`, `*.test.ts`)
- Gemfile, package.json, requirements.txt

Invalid targets:
- Other `.claude/` files (use Related Documentation)
- External URLs (use Sources in frontmatter)
- Generated files

---

## Related Documentation (When Applicable)

### Rule: Link Related .claude/ Files

When a workspace file relates to other `.claude/` documents, include links.

**When to link:**
- A plan implements an architecture decision
- An analysis informs a plan
- Research supports an architecture decision
- Examples demonstrate an architecture pattern
- Multiple plans relate to the same feature

**Format:**
```markdown
### Related Documentation
- [Event Sourcing ADR](../architecture/2025-01-07-event-sourcing.md) - This plan implements this decision
- [Auth Library Research](../research/2025-01-07-auth-research.md) - Informed library choice
- [Performance Analysis](../analysis/2025-01-07-perf-audit.md) - Identified issues this plan addresses
```

---

## Bidirectional Links

### Recommendation: Add Backlinks

When adding a reference from file A to file B, consider adding a backlink from B to A.

**Example:**
1. `plans/auth-migration.md` links to `architecture/auth-design.md`
2. Update `architecture/auth-design.md` to link back:
   ```markdown
   ### Related Documentation
   - [Auth Migration Plan](../plans/2025-01-07-auth-migration.md) - Implementation plan for this decision
   ```

---

## Supersession Links

### Rule: Track Document Evolution

When a document supersedes another:

1. **Add to new document frontmatter:**
   ```yaml
   supersedes:
     - ../plans/2024-06-01-old-auth-plan.md
   ```

2. **Update old document frontmatter:**
   ```yaml
   status: superseded
   superseded_by:
     - ../plans/2025-01-07-new-auth-plan.md
   ```

3. **Add cross-reference in Related section:**
   ```markdown
   ### Related Documentation
   - [Old Auth Plan](../plans/2024-06-01-old-auth-plan.md) - Superseded by this document
   ```

---

## Link Validation

Before creating a file, verify:

1. **Target exists** - Codebase file must exist
2. **Path is correct** - Use relative paths from file location
3. **Description is meaningful** - Explain the relationship

**Example validation:**
```
Checking: ../../app/models/user.rb
From: .claude/plans/2025-01-07-auth-migration.md
Resolved: app/models/user.rb
Status: EXISTS
```

---

## Examples

### Plan with Full Cross-References

```markdown
## Related

### Codebase
- [user.rb](../../app/models/user.rb) - Model requiring authentication changes
- [sessions_controller.rb](../../app/controllers/sessions_controller.rb) - Login flow implementation
- [routes.rb](../../config/routes.rb) - Auth route definitions

### Related Documentation
- [Auth Architecture ADR](../architecture/2025-01-07-auth-design.md) - Design decision this implements
- [Auth Library Research](../research/2025-01-07-auth-comparison.md) - Research informing library choice
```

### Architecture Decision with Cross-References

```markdown
## Related

### Codebase
- [application_controller.rb](../../app/controllers/application_controller.rb) - Base controller for auth middleware
- [user.rb](../../app/models/user.rb) - User model for authentication

### Related Documentation
- [Auth Migration Plan](../plans/2025-01-07-auth-migration.md) - Implementation plan for this decision
- [Session Management Example](../examples/2025-01-07-session-handling.md) - Reference implementation
```

---

## Common Mistakes

**Missing codebase links:**
```markdown
## Related

### Related Documentation
- [Some other doc](../plans/doc.md)
```
INVALID - Must include `### Codebase` with at least one link

**Bare backticks instead of links:**
```markdown
### Codebase
- `app/models/user.rb` - The user model
```
INVALID - Must use markdown link format `[name](path)`

**External URLs in codebase section:**
```markdown
### Codebase
- [Rails Guide](https://guides.rubyonrails.org) - Reference
```
INVALID - External URLs go in frontmatter `sources` field, not codebase links
