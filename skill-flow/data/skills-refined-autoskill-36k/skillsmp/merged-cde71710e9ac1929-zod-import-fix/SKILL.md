---
name: zod-import-fix
description: Use this skill to resolve Zod schema import issues in Output SDK workflows, particularly during migration or when encountering "incompatible schema" errors and type mismatches.
---

# Fix Zod Import Source Issues

## Overview

This skill helps diagnose and fix issues where Zod schemas are imported from the wrong source. The Output SDK requires schemas to be imported from `@output.ai/core`, not directly from `zod`.

## When to Use This Skill

Use this skill when you encounter:
- "incompatible schema" errors
- Type errors at step boundaries
- Schema validation failures when passing data between steps
- Errors mentioning Zod types not matching
- "Expected ZodObject but received..." errors

## Root Cause

The issue arises when `z` is imported from `zod` instead of `@output.ai/core`. Although both provide Zod schemas, they create different schema instances that are incompatible within the Output SDK context. This can lead to runtime validation failures and TypeScript errors.

## Error Messages

Common error messages include:
```
Error: Incompatible schema types
Error: Schema validation failed: expected compatible Zod instance
TypeError: Cannot read property 'parse' of undefined
```

## Solution

### Step 1: Find All Zod Imports

Search your codebase for incorrect imports:

```bash
grep -r "from 'zod'" src/
grep -r 'from "zod"' src/
```

### Step 2: Update Imports

Change all imports from:

```typescript
// Wrong
import { z } from 'zod';
```

To:

```typescript
// Correct
import { z } from '@output.ai/core';
```

### Step 3: Verify No Direct Zod Dependencies

Check your imports to ensure they do not accidentally use `zod` elsewhere:

```bash
grep -r "import.*zod" src/
```

All matches should show `@output.ai/core`, not `zod`.

## Complete Migration Example

### Before (Wrong)

```typescript
// src/workflows/my-workflow/steps/process.ts
import { z } from 'zod';  // Wrong!
import { step } from '@output.ai/core';

export const processStep = step({
  name: 'processData',
  inputSchema: z.object({
    id: z.string(),
  }),
  outputSchema: z.object({
    result: z.string(),
  }),
  fn: async (input) => {
    return { result: `Processed ${input.id}` };
  },
});
```

### After (Correct)

```typescript
// src/workflows/my-workflow/steps/process.ts
import { z, step } from '@output.ai/core';  // Correct!

export const processStep = step({
  name: 'processData',
  inputSchema: z.object({
    id: z.string(),
  }),
  outputSchema: z.object({
    result: z.string(),
  }),
  fn: async (input) => {
    return { result: `Processed ${input.id}` };
  },
});
```

## Verification Steps

1. **Check for remaining wrong imports**:
   ```bash
   grep -r "from 'zod'" src/
   grep -r 'from "zod"' src/
   ```

2. **Build the project**:
   ```bash
   npm run output:workflow:build
   ```

3. **Run the workflow**:
   ```bash
   npx output workflow run <workflowName> '<input>'
   ```

## Prevention

### ESLint Rule

Add a rule to prevent direct Zod imports in your ESLint config:

```javascript
// .eslintrc.js
module.exports = {
  rules: {
    'no-restricted-imports': ['error', {
      paths: [{
        name: 'zod',
        message: "Import { z } from '@output.ai/core' instead of 'zod'"
      }]
    }]
  }
};
```

### IDE Settings

Configure your editor to auto-import from `@output.ai/core`. For VS Code, add to `settings.json`:

```json
{
  "typescript.preferences.autoImportFileExcludePatterns": ["zod"]
}
```

## Common Gotchas

- **Mixed Imports in Same File**: Even one wrong import can cause issues.
  
  ```typescript
  import { z } from '@output.ai/core';
  import { z as zod } from 'zod';  // This causes problems!
  ```

- **Indirect Dependencies**: If a utility file uses the wrong import, it affects all files using these schemas.

  ```typescript
  // utils/schemas.ts
  import { z } from 'zod';  // Wrong! This affects all files using these schemas
  export const idSchema = z.string().uuid();
  ```

- **Third-Party Libraries**: If using external Zod schemas, you may need to recreate them with `@output.ai/core`'s `z`.

## Related Skills

- `flow-convert-activities-to-steps` - Full activity to step conversion
- `flow-error-eslint-compliance` - ESLint compliance for migrated code
- `flow-validation-checklist` - Complete migration validation