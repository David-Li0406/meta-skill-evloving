# Usage Examples

Complete examples of design-init skill usage in different scenarios.

## Example 1: Architecture Doc with Explicit Category

**User request:**

> Create an architecture design doc for rspress-plugin-api-extractor called
> component-lifecycle

**Execution:**

1. Module: `rspress-plugin-api-extractor`
2. Topic: `component-lifecycle`
3. Category: `architecture` (inferred from "architecture" in request)
4. Template: `.claude/skills/design-init/templates/architecture.template.md`
5. Output: `.claude/design/rspress-plugin-api-extractor/component-lifecycle.md`

**Frontmatter generated:**

```yaml
---
status: stub
module: rspress-plugin-api-extractor
category: architecture
created: 2026-01-17
updated: 2026-01-17
last-synced: never
completeness: 0
related: []
dependencies: []
---
```

**File created:** `.claude/design/rspress-plugin-api-extractor/component-lifecycle.md`

**Next steps provided:**

- Fill in placeholders
- Add Overview, Current State, Rationale sections
- Update completeness
- Run `/design-validate` when ready

## Example 2: Performance Doc with Category Inference

**User request:**

> Initialize a design doc for effect-type-registry about caching-optimization

**Execution:**

1. Module: `effect-type-registry`
2. Topic: `caching-optimization`
3. Category: `performance` (inferred from "optimization")
4. Template: `.claude/skills/design-init/templates/performance.template.md`
5. Output: `.claude/design/effect-type-registry/caching-optimization.md`

**Inference logic:**

- Topic contains "optimization" keyword
- Maps to `performance` category
- No user confirmation needed (confident inference)

## Example 3: Default Template (Ambiguous Category)

**User request:**

> Create design doc for website module called deployment-process

**Execution:**

1. Module: `website`
2. Topic: `deployment-process`
3. Category: Ambiguous - ask user
4. User presented with options:
   - architecture
   - performance
   - observability
   - testing
   - integration
   - other
5. User selects: `other`
6. Template: `.claude/skills/design-init/templates/design-doc.template.md`
7. Output: `.claude/design/website/deployment-process.md`

**Why ambiguous:**

- "deployment" could be architecture or integration
- No clear keyword match
- Better to ask user than guess wrong

## Example 4: New Module Without Design Docs Path

**User request:**

> Create a design doc for new-package about api-design

**Execution:**

1. Module: `new-package` (exists in config)
2. Check `designDocsPath`: Not configured
3. Suggest: `.claude/design/new-package`
4. Ask user: "Module doesn't have designDocsPath. Create at suggested location?"
5. User confirms
6. Create directory
7. Continue with file creation

**Config before:**

```json
{
  "modules": {
    "new-package": {
      "path": "packages/new-package"
    }
  }
}
```

**Suggested update:**

```json
{
  "modules": {
    "new-package": {
      "path": "packages/new-package",
      "designDocsPath": ".claude/design/new-package"
    }
  }
}
```

## Example 5: Topic with Special Characters

**User request:**

> Create design doc for effect-type-registry called "Type Loading & Caching"

**Execution:**

1. Module: `effect-type-registry`
2. Topic (raw): `Type Loading & Caching`
3. Convert to kebab-case: `type-loading-caching`
4. Notify user: "Converting to: type-loading-caching"
5. Ask confirmation
6. User confirms
7. Category: Infer from converted topic
8. Output: `.claude/design/effect-type-registry/type-loading-caching.md`

**Conversion rules applied:**

- Spaces → hyphens
- Uppercase → lowercase
- Special chars (`&`) → removed

## Example 6: Very Long Topic Name

**User request:**

> Create a design doc for rspress-plugin-api-extractor about
> advanced-performance-optimization-strategies-for-large-type-definitions

**Execution:**

1. Module: `rspress-plugin-api-extractor`
2. Topic: `advanced-performance-optimization-strategies-for-large-type-definitions`
   (72 chars)
3. Warn: Topic too long
4. Suggest: `performance-large-types`
5. Present options:
   - Use suggested short name
   - Keep original name
   - Enter custom name
6. User selects suggested
7. Continue with `performance-large-types`

**Abbreviation logic:**

- Remove: "advanced", "strategies", "for", "definitions"
- Keep: "performance", "large", "types"
- Result: 3-word concise name

## Example 7: File Already Exists

**User request:**

> Create design doc for effect-type-registry about observability

**Execution:**

1. Module: `effect-type-registry`
2. Topic: `observability`
3. Check path: `.claude/design/effect-type-registry/observability.md`
4. File exists!
5. Ask user: "File already exists. Overwrite?"
6. Options:
   - Yes - Replace existing file
   - No - Abort operation
   - Rename - Suggest `observability-v2.md`
7. User selects: No
8. Operation aborted, existing file preserved

## Example 8: Multiple Categories for Same Module

**User request:**

> Create observability design doc for rspress-plugin-api-extractor about
> error-tracking

**Execution:**

1. Module: `rspress-plugin-api-extractor`
2. Topic: `error-tracking`
3. Category from request: `observability`
4. Validate against module's allowed categories:
   - architecture ✅
   - performance ✅
   - observability ✅
   - cross-linking ✅
   - import-generation ✅
   - source-mapping ✅
5. Category valid
6. Template: `.claude/skills/design-init/templates/observability.template.md`
7. Output: `.claude/design/rspress-plugin-api-extractor/error-tracking.md`

## Example 9: Success Report

After successful creation, provide this report:

```markdown
# Design Document Created

**File:** `.claude/design/effect-type-registry/cache-optimization.md`
**Module:** effect-type-registry
**Category:** performance
**Template:** performance.template.md
**Status:** stub

## Next Steps

1. Fill in the placeholders marked with `{...}`
2. Add overview and rationale sections
3. Document current state
4. Update completeness score (0-100)
5. Change status from `stub` to `draft` when partially complete
6. Run `/design-validate effect-type-registry` to check for issues

## Related Documentation

To reference this in CLAUDE.md:

\`\`\`markdown
**For cache optimization details:**
→ `@./.claude/design/effect-type-registry/cache-optimization.md`

Load when working on caching or performance optimization.
\`\`\`
```
