# Archival Reasons and Guidelines

Detailed guidelines for each archival reason type, including when to use,
requirements, and best practices.

## Overview

Design documents can be archived for four primary reasons:

1. **Superseded** - Replaced by newer documentation
2. **Deprecated** - Feature/system deprecated
3. **Obsolete** - Information no longer accurate
4. **Completed** - Project finished, documented elsewhere

Each reason has specific requirements and implications.

## Reason: Superseded

Document replaced by newer, better documentation covering the same topic.

### Superseded: When to Use

**Appropriate scenarios:**

- New doc covers same topic with more detail or accuracy
- Architecture changed, new doc reflects current state
- Consolidated multiple old docs into one comprehensive doc
- Rewrote doc with better structure or examples
- Split large doc into focused smaller docs

**Not appropriate:**

- Doc just needs minor updates (use /design-update instead)
- Only formatting changes needed
- Content is still accurate but incomplete

### Superseded: Requirements

**Must have:**

- ✅ Replacement document exists and is accessible
- ✅ Replacement covers all important topics from archived doc
- ✅ Replacement has status "current" or "draft"
- ✅ Clear mapping from old to new content

**Should have:**

- Migration notes if significant structural changes
- Explanation of what changed and why
- Cross-reference from replacement back to archived doc

**Frontmatter structure:**

```yaml
---
status: archived
updated: 2026-01-17
archived:
  date: 2026-01-17
  reason: superseded
  replacement: ./new-doc.md
  notes: "Consolidated into new-doc.md with updated architecture"
---
```

### Superseded: Archival Notice Format

```markdown
> **⚠️ ARCHIVED DOCUMENTATION**
>
> This design document was archived on 2026-01-17.
>
> **Reason:** This document has been superseded by newer documentation.
>
> **Replacement:** See [New Document Name](./new-doc.md) for current
> documentation.
>
> **What changed:** Brief summary of major changes in the new doc.
```

### Superseded: Validation Checklist

Before archiving as "superseded":

- [ ] Replacement doc exists at specified path
- [ ] Replacement doc covers all key topics from archived doc
- [ ] Replacement doc has adequate completeness (>70%)
- [ ] All cross-references to old doc updated to point to new doc
- [ ] CLAUDE.md references updated
- [ ] Migration notes added if architecture changed significantly

### Superseded: Best Practices

**Do:**

- Review replacement to ensure comprehensive coverage
- Add "what changed" summary in archival notice
- Update all references atomically (don't leave broken links)
- Keep archived doc accessible for historical reference
- Add bidirectional references (old ↔ new)

**Don't:**

- Archive if replacement doesn't cover critical topics
- Remove archived doc immediately (keep for reference)
- Forget to update CLAUDE.md files
- Archive without user confirmation

### Superseded: Example Scenario

**Old doc:** `cache-v1-design.md` (cache design for v1 system)
**New doc:** `cache-optimization.md` (redesigned cache for v2)
**Reason:** Architecture completely redesigned, v1 doc no longer accurate

**Archival metadata:**

```yaml
archived:
  date: 2026-01-17
  reason: superseded
  replacement: ./cache-optimization.md
  notes: "Cache redesigned for v2 with LRU eviction and TTL support"
```

## Reason: Deprecated

Feature or system documented is deprecated and will be removed.

### Deprecated: When to Use

**Appropriate scenarios:**

- Feature marked for removal in future version
- System being phased out with migration path
- API version deprecated in favor of newer version
- Legacy implementation being replaced

**Not appropriate:**

- Feature just being updated (use /design-update)
- Temporary issues with feature
- Feature paused but may return

### Deprecated: Requirements

**Must have:**

- ✅ Clear deprecation timeline
- ✅ Deprecation date documented
- ✅ Planned removal date (if known)
- ✅ Migration guide or replacement (if available)

**Should have:**

- End of support date
- Reason for deprecation
- Alternative/replacement feature
- Migration instructions

**Frontmatter structure:**

```yaml
---
status: archived
updated: 2026-01-17
archived:
  date: 2026-01-17
  reason: deprecated
  deprecation_timeline:
    deprecated_date: 2026-01-17
    end_of_support: 2026-06-30
    removal_date: 2026-12-31
  replacement: ./v2-feature.md
  notes: "Feature deprecated in favor of v2 implementation"
---
```

### Deprecated: Archival Notice Format

```markdown
> **⚠️ ARCHIVED DOCUMENTATION - DEPRECATED FEATURE**
>
> This design document was archived on 2026-01-17.
>
> **Reason:** This documents a deprecated feature/system.
>
> **Deprecation Timeline:**
>
> - **Deprecated:** 2026-01-17
> - **End of Support:** 2026-06-30
> - **Planned Removal:** 2026-12-31
>
> **Migration:** See [V2 Feature](./v2-feature.md) for the replacement.
```

### Deprecated: Validation Checklist

Before archiving as "deprecated":

- [ ] Feature is officially deprecated (not just planned)
- [ ] Deprecation timeline documented
- [ ] Migration path exists (if applicable)
- [ ] Replacement/alternative documented
- [ ] Users notified of deprecation
- [ ] Keep doc accessible during transition period

### Deprecated: Best Practices

**Do:**

- Keep doc accessible until removal date
- Provide clear migration timeline
- Link to replacement/alternative
- Update user-facing docs with deprecation notice
- Mark clearly as deprecated in all references

**Don't:**

- Move to archive directory during transition
- Remove references while feature still exists
- Archive without clear timeline
- Forget to notify users of deprecation

### Transition Period Handling

During deprecation period (before removal):

- Keep doc in active directory (not _archive)
- Add prominent deprecation notice
- Update status to "archived" but keep accessible
- Monitor usage and support during transition
- Update references to note deprecation

After removal:

- Can move to _archive directory
- Update references to note removal
- Consider keeping for historical reference

### Deprecated: Example Scenario

**Doc:** `legacy-api-v1.md`
**Status:** v1 API deprecated in favor of v2
**Timeline:** 6 months support, then removal

**Archival metadata:**

```yaml
archived:
  date: 2026-01-17
  reason: deprecated
  deprecation_timeline:
    deprecated_date: 2026-01-17
    end_of_support: 2026-07-17
    removal_date: 2027-01-17
  replacement: ./api-v2.md
  notes: "v1 API deprecated. Migrate to v2 before 2027-01-17."
```

## Reason: Obsolete

Information in document is no longer accurate or relevant.

### Obsolete: When to Use

**Appropriate scenarios:**

- Information is outdated and misleading
- System completely rewritten with different approach
- Design decisions no longer apply
- Technology/dependencies changed fundamentally
- Assumptions in doc proven false

**Not appropriate:**

- Doc just needs updates to remain accurate
- Minor details wrong but core content valid
- Temporary state that will return to documented state

### Obsolete: Requirements

**Must have:**

- ✅ Explanation of what changed
- ✅ Date when information became obsolete
- ✅ Link to current docs (if available)

**Should have:**

- Brief summary of what was wrong/outdated
- Context for why approach changed
- Reference to decision to change

**Frontmatter structure:**

```yaml
---
status: archived
updated: 2026-01-17
archived:
  date: 2026-01-17
  reason: obsolete
  became_obsolete: 2025-12-01
  notes: "System rewritten with different architecture. See architecture.md."
  current_docs: ./architecture.md
---
```

### Obsolete: Archival Notice Format

```markdown
> **⚠️ ARCHIVED DOCUMENTATION - OBSOLETE**
>
> This design document was archived on 2026-01-17.
>
> **Reason:** The information in this document is no longer accurate or
> relevant.
>
> **What changed:** System was completely rewritten in December 2025 with a
> different architectural approach.
>
> **Current documentation:** See [Architecture](./architecture.md) for the
> current system design.
```

### Obsolete: Validation Checklist

Before archiving as "obsolete":

- [ ] Information is genuinely obsolete (not just needs update)
- [ ] No reasonable way to update doc to remain accurate
- [ ] Current docs exist covering the topic
- [ ] Clear explanation of what changed
- [ ] References to obsolete doc updated or removed

### Obsolete: Best Practices

**Do:**

- Clearly explain what became obsolete
- Link to current docs if available
- Note when information became obsolete
- Consider if content has historical value
- Update or remove references

**Don't:**

- Archive if doc can be updated to remain accurate
- Remove immediately (may have historical value)
- Forget to update dependent docs
- Leave misleading references in active docs

### Historical Preservation

Even obsolete docs can have value:

- **Preserve if:** Documents important decisions, historical context, or
  lessons learned
- **Remove if:** Misleading with no historical value, contains security
  issues, or takes up significant space

### Obsolete: Example Scenario

**Doc:** `old-caching-strategy.md`
**Status:** Describes caching approach no longer used
**Change:** Complete cache redesign with different technology

**Archival metadata:**

```yaml
archived:
  date: 2026-01-17
  reason: obsolete
  became_obsolete: 2025-11-15
  notes: "Cache completely redesigned using Redis instead of in-memory"
  current_docs: ./cache-optimization.md
```

## Reason: Completed

Project or feature documented is complete and documented elsewhere.

### Completed: When to Use

**Appropriate scenarios:**

- Design doc was for planning, now in user docs
- Proof of concept completed or cancelled
- Temporary implementation removed
- Planning doc no longer needed after completion
- Migration completed

**Not appropriate:**

- Feature complete but design still relevant
- Implementation ongoing
- Doc describes current production system

### Completed: Requirements

**Must have:**

- ✅ Completion date
- ✅ Link to final implementation docs
- ✅ Final status (completed, cancelled, superseded)

**Should have:**

- Summary of outcome
- Link to implementation
- Lessons learned (if valuable)

**Frontmatter structure:**

```yaml
---
status: archived
updated: 2026-01-17
archived:
  date: 2026-01-17
  reason: completed
  completion_date: 2026-01-10
  outcome: "successfully_implemented"
  final_docs: ../../docs/en/features/feature-name.md
  notes: "Feature completed and documented in user docs"
---
```

### Completed: Archival Notice Format

```markdown
> **⚠️ ARCHIVED DOCUMENTATION - COMPLETED**
>
> This design document was archived on 2026-01-17.
>
> **Reason:** The project documented here is complete.
>
> **Completion:** Feature successfully implemented on 2026-01-10.
>
> **Final documentation:** See [Feature Documentation](../../docs/en/features/feature-name.md)
> for user-facing docs.
```

### Completed: Validation Checklist

Before archiving as "completed":

- [ ] Project/feature is genuinely complete
- [ ] Final docs exist (user docs, API docs, etc.)
- [ ] No ongoing work related to this design
- [ ] Implementation matches design (or differences documented)
- [ ] Lessons learned captured if valuable

### Completed: Best Practices

**Do:**

- Link to final implementation docs
- Note completion date
- Capture lessons learned if valuable
- Update status to reflect outcome
- Keep for historical reference

**Don't:**

- Archive active design docs
- Remove immediately (historical value)
- Forget to link to final docs
- Archive without confirming completion

### Outcome Types

**Successfully Implemented:**

- Feature completed as designed
- Link to implementation and user docs
- Note any deviations from design

**Cancelled:**

- Project cancelled before completion
- Note reason for cancellation
- Preserve for historical context

**Superseded During Implementation:**

- Design changed during implementation
- Link to revised design doc
- Note why original approach changed

### Completed: Example Scenario

**Doc:** `new-plugin-architecture-proposal.md`
**Status:** Proposal implemented, now documented in user docs
**Outcome:** Successfully implemented with minor changes

**Archival metadata:**

```yaml
archived:
  date: 2026-01-17
  reason: completed
  completion_date: 2026-01-10
  outcome: "successfully_implemented"
  final_docs: ../../docs/en/packages/plugin-api.md
  notes: "Architecture implemented with minor changes. See final docs."
```

## Choosing the Right Reason

Decision tree for selecting archival reason:

```text
Is there a replacement doc?
├─ Yes → Is old doc wrong/outdated?
│         ├─ Yes → SUPERSEDED
│         └─ No → Is feature deprecated?
│                 ├─ Yes → DEPRECATED
│                 └─ No → COMPLETED
└─ No → Is feature deprecated?
        ├─ Yes → DEPRECATED
        └─ No → Is info wrong/outdated?
                ├─ Yes → OBSOLETE
                └─ No → COMPLETED (or don't archive)
```

**Summary:**

- **SUPERSEDED**: New doc replaces old doc
- **DEPRECATED**: Feature being removed
- **OBSOLETE**: Information wrong/outdated, no direct replacement
- **COMPLETED**: Project done, documented elsewhere

## Archival Metadata Reference

Complete frontmatter structure for each reason:

### Superseded

```yaml
archived:
  date: YYYY-MM-DD
  reason: superseded
  replacement: ./path/to/replacement.md
  notes: "Brief explanation of what changed"
```

### Deprecated

```yaml
archived:
  date: YYYY-MM-DD
  reason: deprecated
  deprecation_timeline:
    deprecated_date: YYYY-MM-DD
    end_of_support: YYYY-MM-DD
    removal_date: YYYY-MM-DD
  replacement: ./path/to/replacement.md  # optional
  notes: "Brief explanation of deprecation"
```

### Obsolete

```yaml
archived:
  date: YYYY-MM-DD
  reason: obsolete
  became_obsolete: YYYY-MM-DD
  notes: "Brief explanation of what became obsolete"
  current_docs: ./path/to/current.md  # optional
```

### Completed

```yaml
archived:
  date: YYYY-MM-DD
  reason: completed
  completion_date: YYYY-MM-DD
  outcome: "successfully_implemented|cancelled|superseded"
  final_docs: ./path/to/final-docs.md
  notes: "Brief summary of completion"
```
