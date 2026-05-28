# Spec Archive Best Practices

## Archive Organization

1. **One archive per completed spec** - Don't combine multiple specs
2. **Preserve directory structure** - Keep all three files together
3. **Update immediately when done** - Don't let completed specs linger in active/
4. **Write good summaries** - Future you will thank present you
5. **Document the why** - Especially for abandoned/incomplete specs
6. **Keep git history** - Don't delete branches until merged and verified

## After Archiving

The `./specs/active/` directory should be empty (or contain only active specs).

If starting new work immediately, use `/spec.create` to set up new documents.

## Troubleshooting

**Q: What if the user didn't provide a spec name?**
A: List available specs in `./specs/active/` and ask: "Which spec should I archive? Usage: `/spec.archive <spec-name>`"

**Q: What if no ./specs/active/ directory exists?**
A: Nothing to archive. Inform user: "No active specs found at ./specs/active/"

**Q: What if the spec has no associated branch?**
A: Skip Git Operations step. Document as "Branch: N/A" in archive index.

**Q: What if multiple people worked on this spec?**
A: In Archive Notes, add "### Contributors" section listing who worked on what.

**Q: Should I archive if tests are failing?**
A: Only with explicit user confirmation. Mark status as "Incomplete - Failing Tests".

**Q: How long to keep archives?**
A: Indefinitely. They're documentation. If they become too large, consider moving older ones to a separate archive-old/ directory, but keep README.md entries.

## Example Archive Notes

```markdown
---

## Archive Notes

**Archived**: 2025-11-07
**Final Status**: Complete

### Summary
Successfully implemented temporal join support with time-based relationship decorators. All type safety maintained with Ibis integration.

### Key Outcomes
- `TemporalJoin` type added to DSL with proper validation
- `@relationship(temporal=True)` decorator supports time columns
- Compilation to Ibis temporal joins working with all backends
- Full test coverage including edge cases

### Technical Debt / Future Work
- Consider adding support for time range joins (not just equality)
- Window-based temporal joins could be added later
- Performance optimization for large temporal datasets

### Lessons Learned
- Ibis expression validation at construction time prevented many runtime errors
- Pattern matching with keyword patterns made IR traversal much cleaner
- Early prototyping with real data exposed edge cases that unit tests missed
```
