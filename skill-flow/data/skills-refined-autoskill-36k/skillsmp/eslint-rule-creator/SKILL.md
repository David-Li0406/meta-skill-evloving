---
name: eslint-rule-creator
description: Use when creating a new ESLint rule for eslint-cease-nonsense-rules, adding a lint rule, or when user provides incorrect/correct code examples for a new rule
---

# Creating ESLint Rules for eslint-cease-nonsense-rules

## Overview

Creates complete ESLint rules with all required files: rule implementation, tests, documentation, and registry updates.

## When to Use

- User asks to "create a new ESLint rule"
- User asks to "add a lint rule"
- User provides examples of "bad code" and "good code" for linting
- User describes behavior they want to lint against

## Required Files Checklist

**ALWAYS create/update ALL of these:**

1. `src/rules/{rule-name}.ts` - Rule implementation
2. `tests/rules/{rule-name}.test.ts` - Test file (100% coverage required)
3. `docs/rules/{rule-name}.md` - Documentation
4. `README.md` - Add rule to appropriate category
5. `src/index.ts` - Register rule and export types

**CONDITIONALLY update:**

1. `src/utilities/configure-utilities.ts` - Only if rule has configurable options

## Gathering Requirements

Before writing code, ask the user for:

1. **Rule name** (kebab-case, e.g., `no-foo-bar` or `prefer-xyz`)
2. **What it detects** (the bad pattern)
3. **What it suggests** (the good pattern)
4. **Examples of incorrect code**
5. **Examples of correct code**
6. **Should it have options?** If yes, what options?
7. **Should it auto-fix?** If yes, what's the fix?
8. **What category?** (Type Safety, React, Logging, Resource Management, Code Quality, Performance, Module Boundaries, TypeScript)

## Implementation Patterns

### Rule File Structure

See `templates/rule-simple.ts.template` for rules without options.
See `templates/rule-with-options.ts.template` for rules with options.

Key points:

- Use `createRule` from `../utilities/create-rule`
- Use AST selectors when possible (cleaner than visitor functions)
- Define `type MessageIds` for type-safe message IDs
- Export options interface if rule has options

### Test File Structure

See `templates/test.ts.template` for the pattern.

Key points:

- Import `describe` from `bun:test`
- Import `RuleTester` from `eslint`
- Cover all branches for 100% coverage
- Test both valid and invalid cases
- Test options if applicable

### Documentation Structure

See `templates/docs.md.template` for the pattern.

Key points:

- Start with `# rule-name` and description
- Include `## Rule Details` explanation
- Include `## Options` section if applicable
- Include `## Examples` with `### Incorrect` and `### Correct`
- End with `## When Not To Use It` and `## Related Rules`

### README.md Update

Add to appropriate category section following existing format:

```markdown
#### `rule-name`

Short description of what the rule does.

**Configuration** (if options exist)

\`\`\`typescript
{
  "cease-nonsense/rule-name": ["error", { option: value }]
}
\`\`\`

**Incorrect**

\`\`\`typescript
// bad code example
\`\`\`

**Correct**

\`\`\`typescript
// good code example
\`\`\`
```

### src/index.ts Updates

1. Add import: `import ruleName from "./rules/rule-name";`
2. Export type (if options): `export type { RuleNameOptions } from "./rules/rule-name";`
3. Add to `rules` object: `"rule-name": ruleName,`
4. Add to `recommended` config if it should be on by default

### configure-utilities.ts Updates (if options)

Add a factory function:

```typescript
export function createRuleNameOptions(options: Partial<RuleNameOptions> = {}): RuleNameOptions {
    return { defaultValue: "default", ...options };
}
```

## Verification Checklist

Before declaring done:

- [ ] `bun run type-check` passes
- [ ] `bun run lint` passes
- [ ] `bun test` passes with 100% coverage for new rule
- [ ] `bun run build` succeeds
- [ ] All 5+ files created/updated
- [ ] Rule appears in README under correct category
- [ ] Examples in docs match the actual rule behavior
