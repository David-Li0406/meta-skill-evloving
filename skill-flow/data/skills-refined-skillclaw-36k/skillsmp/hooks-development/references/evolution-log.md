# Evolution Log

Changelog for hooks-development skill discoveries and updates.

## v1.0.0 (2025-12-17)

**Initial Release**

- Created hooks-development skill documenting PostToolUse visibility patterns
- Documented `decision: block` requirement for Claude visibility
- Added exit code behavior table
- Included working templates from chezmoi-sync-reminder.sh
- Created debugging guide for invisible hook output

**Discovery Source**: Debugging session with chezmoi-sync-reminder hook where stdout was not visible to Claude despite hook executing successfully.

**Key Insight**: PostToolUse hook stdout requires JSON with `"decision": "block"` field for Claude to receive the message. This is counterintuitive since the operation is not actually blocked.

**References**:

- [GitHub Issue #3983](https://github.com/anthropics/claude-code/issues/3983)
- [ADR: PostToolUse Hook Visibility](../../../../../docs/adr/2025-12-17-posttooluse-hook-visibility.md)

---

## Template for Future Entries

```markdown
## vX.Y.Z (YYYY-MM-DD)

**Change Type**: [Discovery | Enhancement | Fix | Deprecation]

**Summary**: Brief description of what changed

**Discovery Source**: How this was learned (debugging session, user report, documentation review)

**Key Insight**: The important takeaway for future reference

**Files Modified**:

- `SKILL.md`: What changed
- `references/X.md`: What changed

**References**:

- Links to related issues, ADRs, or documentation
```
