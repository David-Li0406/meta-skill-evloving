---
name: update-doc
description: Transform documentation into AI-optimized format for Claude Code. Use when user says "update doc", "optimize doc", "rewrite for claude", or "AI optimize". Shows recently modified .md files for selection, verifies accuracy against codebase, generates optimized version, compares for completeness, then replaces with approval.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, TodoWrite, Task
version: 1.3.0
---

# Update Doc

Transform any markdown document into an AI-optimized version using research-backed best practices.

<when_to_use>

## When to Use

Invoke when user says:

- "update doc"
- "optimize doc"
- "rewrite for claude"
- "AI optimize"
- "make this doc AI-friendly"

</when_to_use>

<workflow>

## Workflow

| Phase | Action                                        | Gate          |
| ----- | --------------------------------------------- | ------------- |
| 0     | Find recent .md files, prompt user to select  | User select   |
| 1     | Read original, detect document type           | -             |
| 1.5   | Verify accuracy against codebase              | User choice   |
| 2     | Generate optimized version to `.optimized.md` | -             |
| 3     | Compare original vs optimized for gaps        | -             |
| 4     | Second pass: fill any gaps found              | -             |
| 5     | Present summary with key changes              | User approval |
| 6     | Replace original (with backup) or discard     | -             |

</workflow>

<phase_details>

## Phase Details

### Phase 0: File Selection

1. Use Glob to find `.md` files modified in last 30 days
2. Exclude: `node_modules/`, `.git/`, `*.optimized.md`, `*.backup.md`
3. Use AskUserQuestion to present top 10 most recently modified files
4. Store selected file path for subsequent phases

### Phase 1: Analysis

1. Read the selected document completely
2. Detect document type (see [references/document-types.md](references/document-types.md)):
   - CLAUDE.md → Apply progressive disclosure rules
   - Skill file → Ensure frontmatter and XML tags
   - Pattern file → Add [OK]/[FAIL] examples
   - General markdown → Apply standard optimization
3. Count lines, headings, code blocks, links

### Phase 1.5: Accuracy Verification (Pattern Files)

**For pattern files only** (`claude-patterns/` path), verify content against codebase:

1. Use AskUserQuestion: "This is a pattern file. Verify accuracy against codebase first?"
   - **Yes (Recommended)**: Proceed to verification
   - **Skip**: Jump to Phase 2

2. If verifying, spawn Explore agent with Task tool:
   - Extract key claims from pattern (function names, file paths, type names, workflows)
   - Search codebase for actual implementations
   - Compare pattern claims vs actual code

3. Report findings:

   ```markdown
   ## Accuracy Check

   | Claim                 | Status      | Finding                         |
   | --------------------- | ----------- | ------------------------------- |
   | Uses `functionName()` | ✅ Verified | Found at `src/path/file.ts:123` |
   | Type `TypeName`       | ❌ Outdated | Type renamed to `NewTypeName`   |
   ```

4. If inaccuracies found:
   - Fix the original file first (correct function names, type names, file paths)
   - Then proceed to Phase 2 with accurate content

**Why this matters**: Optimizing inaccurate documentation propagates errors. The email-patterns.md bug showed pattern files can drift from code over time.

### Phase 2: Transformation

Apply rules from [references/transformation-rules.md](references/transformation-rules.md):

1. **Structure**: Fix heading hierarchy, convert prose to tables/bullets
2. **Content**: Consistent terminology, explicit references, imperative form
3. **Format**: XML tags, fenced code blocks, target length

Write output to `[original-name].optimized.md` in same directory.

### Phase 3: Comparison

Follow [references/comparison-checklist.md](references/comparison-checklist.md):

1. Extract all elements from original (headings, code, commands, links, facts)
2. Verify each element present in optimized (may be reformatted)
3. Create gap list of missing items

### Phase 4: Second Pass

For each gap identified:

1. Determine if omission was intentional (redundant, outdated)
2. If needed, add missing content to optimized document
3. Apply formatting rules to added content

### Phase 5: Summary

Present to user:

```markdown
## Optimization Summary

**Original**: [filename] ([X] lines)
**Optimized**: [filename].optimized.md ([Y] lines)
**Reduction**: [Z]%

### Key Changes

1. [Change 1]
2. [Change 2]
3. [Change 3]

### Content Verified

- Headings: [count] preserved
- Code examples: [count] intact
- Commands: [count] included
- Links: [count] working
```

### Phase 6: Finalization

Based on user choice:

- **Replace**: Rename original to `.backup.md`, rename optimized to original name, then **delete the backup**
- **Keep both**: Leave both files in place
- **Discard**: Delete `.optimized.md`, keep original unchanged

**Important**: After successful replacement, delete the `.backup.md` file. The backup is only needed temporarily during the rename operation. Keeping backups clutters the repository.

</phase_details>

<approval_gates>

## Approval Gates

| Gate      | Phase | Question                                            |
| --------- | ----- | --------------------------------------------------- |
| Selection | 0     | "Which file do you want to optimize?"               |
| Accuracy  | 1.5   | "Verify accuracy against codebase first?"           |
| Replace   | 5     | "Replace original? / Keep both? / Discard changes?" |

</approval_gates>

<document_types>

## Document Types

| Type         | Detection               | Key Transformations                  |
| ------------ | ----------------------- | ------------------------------------ |
| CLAUDE.md    | Filename                | < 300 lines, progressive disclosure  |
| Skill file   | `.claude/skills/` path  | Frontmatter, XML tags, references/   |
| Pattern file | `claude-patterns/` path | [OK]/[FAIL] examples, numbered rules |
| General      | `.md` extension         | Standard optimization                |

For full details: [references/document-types.md](references/document-types.md)

</document_types>

<quick_reference>

## Quick Reference

### Transformation Rules Summary

**Structure**:

- Strict heading hierarchy (H1 → H2 → H3, avoid H4+)
- Blockquote summary after H1 title
- Tables over prose
- Bullets over paragraphs
- Single topic per section
- End-load actionable instructions (checklists, summaries at END)

**Content**:

- Consistent terminology (no synonyms)
- Eliminate vague pronouns (it, this, that, they → specific nouns)
- Imperative form ("Run X" not "You should run X")
- Positive framing ("Use X" not "Don't use Y")

**Format**:

- XML tags for semantic sections
- Fenced code blocks with language
- Target length by type

For full rules: [references/transformation-rules.md](references/transformation-rules.md)

</quick_reference>

<references>

## References

- [references/transformation-rules.md](references/transformation-rules.md) - Complete transformation rules
- [references/document-types.md](references/document-types.md) - Type detection and handling
- [references/comparison-checklist.md](references/comparison-checklist.md) - Gap detection and validation

</references>

<version_history>

## Version History

- **v1.3.0** (2026-01-18): Add accuracy verification phase
  - New Phase 1.5: Verify pattern file accuracy against codebase before optimizing
  - Spawn Explore agent to check function names, types, file paths
  - Fix inaccuracies before optimization (prevents propagating errors)
  - Added Task tool to allowed-tools for agent spawning

- **v1.2.0** (2025-01-18): Research-backed transformation updates
  - Add blockquote summary rule after H1 (llms.txt standard)
  - Add end-loading rule for actionable instructions (U-shaped attention)
  - Enhance pronoun elimination guidance
  - Update heading hierarchy to avoid H4+

- **v1.1.0** (2025-01-09): Delete backup after replacement
  - Backup files are now deleted after successful replacement
  - Prevents repository clutter from accumulating .backup.md files

- **v1.0.0** (2025-01-09): Initial release
  - 6-phase workflow with file selection
  - Support for CLAUDE.md, skill, pattern, and general markdown
  - Comparison-based gap detection
  - Backup on replace

</version_history>
