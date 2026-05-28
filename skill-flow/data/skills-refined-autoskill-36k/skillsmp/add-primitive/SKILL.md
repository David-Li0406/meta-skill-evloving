---
name: add-primitive
description: Add or modify AI primitive definitions in the data layer with correct typing and complete metadata. Use when adding new primitives, updating descriptions, or extending primitive categories.
---

# Add Primitive

Add or modify AI primitive definitions for agentconfig.org.

## Overview

Primitives appear in three places that must stay synchronized:
1. **Primitive Cards** - `site/src/data/primitives.ts`
2. **File Tree** - `site/src/data/fileTree.ts`
3. **Provider Comparison** - `site/src/data/comparison.ts`

## Step-by-Step Process

### 1. Define the Primitive

Edit `site/src/data/primitives.ts`:

```typescript
{
  id: 'your-primitive-id',           // lowercase, hyphens
  name: 'Display Name',
  description: 'One-sentence summary.',
  whatItIs: 'Detailed explanation of the concept.',
  useWhen: [
    'First use case',
    'Second use case',
  ],
  prevents: 'What problem/failure this prevents',
  combineWith: ['Other Primitive', 'Another Primitive'],
  implementations: [
    {
      provider: 'copilot',
      implementation: 'How Copilot implements this',
      location: '.github/path/to/file',
      support: 'full',  // 'full' | 'partial' | 'diy'
    },
    {
      provider: 'claude',
      implementation: 'How Claude implements this',
      location: '.claude/path/to/file',
      support: 'full',
    },
  ],
  category: 'instructions',  // 'instructions' | 'execution' | 'safety'
}
```

### 2. Add to File Tree (if applicable)

If the primitive has associated files, add nodes to both trees in `site/src/data/fileTree.ts`:

**For Copilot** - Add to `copilotTree`:
```typescript
{
  id: 'copilot-your-primitive',
  name: 'your-file.md',
  type: 'file',
  details: {
    label: 'Short Label',
    description: 'What this file does.',
    whatGoesHere: ['Content item 1', 'Content item 2'],
    whenLoaded: 'When this file is loaded.',
    loadOrder: 5,  // 1 = first loaded
    example: `Example content here`,
  },
}
```

**For Claude** - Add to `claudeTree` with equivalent structure.

### 3. Add to Comparison Matrix

Edit `site/src/data/comparison.ts`:

```typescript
{
  primitiveId: 'your-primitive-id',  // Must match primitives.ts
  primitiveName: 'Display Name',
  copilot: {
    level: 'full',  // 'full' | 'partial' | 'none'
    implementation: 'How Copilot does it',
    location: '.github/path',
  },
  claude: {
    level: 'full',
    implementation: 'How Claude does it',
    location: '.claude/path',
  },
}
```

## Data Types Reference

### Primitive Interface
```typescript
interface Primitive {
  id: string
  name: string
  description: string
  whatItIs: string
  useWhen: string[]
  prevents: string
  combineWith: string[]
  implementations: ProviderImplementation[]
  category: 'instructions' | 'execution' | 'safety'
}
```

### Provider Implementation
```typescript
interface ProviderImplementation {
  provider: 'copilot' | 'claude'
  implementation: string
  location: string
  support: 'full' | 'partial' | 'diy'
}
```

### Support Levels
- `full` - Native, well-documented support
- `partial` - Works but with limitations
- `diy` - Achievable with custom configuration

### Categories
- `execution` - Capability primitives (what it can do)
- `instructions` - Customization primitives (how to shape it)
- `safety` - Control primitives (guardrails and verification)

## Checklist

Before considering the primitive complete:

- [ ] Added to `primitives.ts` with all required fields
- [ ] Added to `fileTree.ts` for both Copilot and Claude (if has files)
- [ ] Added to `comparison.ts` with accurate support levels
- [ ] `id` is unique and matches across all three files
- [ ] `combineWith` references valid primitive names
- [ ] Examples in file tree are accurate and helpful
- [ ] Run `bun run typecheck` - No TypeScript errors
- [ ] Visually verify in all three site sections

## Common Mistakes

1. **Mismatched IDs** - The `id` in primitives.ts must match `primitiveId` in comparison.ts
2. **Missing file tree entries** - If the primitive has files, both trees need updates
3. **Stale combineWith** - Referencing primitives that don't exist
4. **Incorrect load order** - File tree `loadOrder` should reflect actual precedence
5. **Missing support level** - Every provider implementation needs a support level
