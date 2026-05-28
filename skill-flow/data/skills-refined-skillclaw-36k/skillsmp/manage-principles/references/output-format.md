# Output Format

## Amendment Report Example

```markdown
# Constitution Amendment Report

**Version**: v1.1.0 → v1.2.0
**Date**: 2025-01-20
**Type**: Clarification

---

## Summary

Updated **Principle VII: Type Safety** to clarify RPC type assertion patterns.

---

## Changes

### Before

VII. **Type Safety** (NON-NEGOTIABLE)

- No `any` types in codebase
- Proper TypeScript types for all functions

### After

VII. **Type Safety** (NON-NEGOTIABLE)

- No `any` types in codebase
- Proper TypeScript types for all functions
- **Exception**: RPC calls use `as unknown as Type` for jsonb returns
  - Pattern: `return data as unknown as Post[];`
  - Rationale: Supabase RPC jsonb type mismatch

---

## Impact Analysis

**Breaking Changes**: No
**Affected Files**: 3
- app/posts/_repositories/PostsRepository.ts (already compliant)
- app/dashboard/_repositories/ActivityRepository.ts (already compliant)
- app/profile/_repositories/ProfileRepository.ts (already compliant)

**Template Updates**: 2
- .claude/commands/speckit.specify.md (updated Principle VII ref)
- .claude/commands/help.md (updated Type Safety section)

---

## Validation

✅ Constitution v1.2.0 validated
✅ All templates synchronized
✅ No orphaned references
✅ Principle numbering consistent

---

## Git Commit

git add .specify/memory/constitution.md .claude/commands/
git commit -m "📝 docs(constitution): Update Principle VII - Type Safety exceptions

- Added RPC type assertion exception
- Clarified 'as unknown as Type' pattern for Supabase jsonb
- Synchronized templates with new version

Constitution: v1.1.0 → v1.2.0"

---

## Team Communication

**Announcement**:

> 📢 Constitution updated to v1.2.0
>
> Principle VII (Type Safety) now includes exception for RPC type assertions.
> Pattern: `return data as unknown as Type;` is approved for Supabase jsonb returns.
>
> All existing code already compliant. No action needed.
```

## Usage Examples

```javascript
// Violation detected during implementation
skill: constitution({
  type: "violation",
  principle: "VII",
  context: "RPC type assertions use 'as unknown as Type'",
});

// New pattern needs codification
skill: constitution({
  type: "gap",
  proposal: "Add principle for error boundary usage",
});

// Clarification needed
skill: constitution({
  type: "clarification",
  principle: "II",
  question: "Does SSR-First apply to admin panels?",
});

// Manual update request
skill: constitution({
  type: "update",
  principle: "V",
  reason: "API mode now supports GraphQL",
});
```

## Error Handling

If Constitution update fails:

1. **Validation Error**
   - Report which validation failed
   - Suggest fix
   - Do not apply changes

2. **Template Sync Error**
   - Partial update may occur
   - Report which templates failed
   - Provide manual sync instructions

3. **Version Conflict**
   - Detect concurrent modifications
   - Show diff
   - Request user resolution

## Success Criteria

This skill succeeds when:

- ✅ Constitution change proposed with clear rationale
- ✅ User approved changes
- ✅ Constitution file updated with correct version
- ✅ All dependent templates synchronized
- ✅ Validation passed (no orphaned refs, consistent numbering)
- ✅ Git commit prepared with descriptive message
- ✅ Team communication draft ready

## Related Skills

- `verify` - Uses Constitution for validation
- `implement` - Follows Constitution principles
- `spec` - References Constitution in planning
