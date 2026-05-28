---
name: compressing-plans
description: Use when plan/spec files exceed their usefulness, context is rotting from verbose .md files, or archiving completed implementation plans
---

# Compressing Plans

Reduce verbose planning documents to actionable references while preserving what's needed to implement and verify.

## When to Use

- Plans completed and implemented (archive for reference)
- Context rotting from LOC:LOD ratio imbalance
- Design exploration done, need executable checklist
- Old specs consuming context without value

## Compression Rules

### KEEP (essential for implementation)

| Element                        | Why                  |
| ------------------------------ | -------------------- |
| Status tables (exists/missing) | Shows what to build  |
| Final decisions                | What was chosen      |
| File → change mappings         | Where to edit        |
| Phase/step checklists          | Execution order      |
| Edge cases list                | Prevent bugs         |
| Verification commands          | Know when done       |
| One code example per pattern   | Copy-paste reference |

### REMOVE (exploration, not execution)

| Element                                | Why                      |
| -------------------------------------- | ------------------------ |
| "Problem → Recommendation" pairs       | Keep only recommendation |
| Multiple code examples of same concept | One suffices             |
| Rationale/justification                | Decision made, move on   |
| Alternative approaches not chosen      | Noise                    |
| "Why this matters" explanations        | Already validated        |
| Verbose prose between sections         | Tables > prose           |

## Output Format

```markdown
# [Title] (Compressed)

## Status

[Keep exists/missing table exactly - it's already dense]

## Decisions

- [Bullet per decision, no rationale]

## Implementation

### Phase N: [Name]

**Files:** [list]

- [ ] Step as checkbox
- [ ] Include one code snippet if essential

## Edge Cases

- [Bullet per edge case]

## Verify

- [ ] Command or check
```

## Compression Checklist

- [ ] Status/exists tables preserved verbatim
- [ ] Decisions extracted as bullets (no "because")
- [ ] File mappings preserved
- [ ] Steps converted to checkboxes
- [ ] Rationale sections removed
- [ ] "Problem" descriptions removed (keep "Solution" only)
- [ ] Duplicate code examples removed (keep one)
- [ ] Edge cases preserved as bullets
- [ ] Verification steps preserved as checkboxes
- [ ] Added "(Compressed)" to title

## Anti-patterns

**Don't lose:**

- Status tables (they're already compressed)
- Edge cases (prevent implementation bugs)
- Verification commands (know when done)

**Don't keep:**

- "Rationale: ..." inline explanations
- Multiple examples showing same pattern
- Prose that restates what tables show
- redundant information
