---
name: fix-zod-import-issues
description: Use this skill when encountering "incompatible schema" errors or type mismatches in Output SDK workflows due to incorrect Zod schema imports.
---

# Fix Zod Import Source Issues

## Overview

This skill helps diagnose and fix issues where Zod schemas are imported from the wrong source during migration to the Output SDK. The Output SDK requires schemas to be imported from `@output.ai/core`, not directly from `zod`.

## When to Use This Skill

Use this skill when you see:
- "incompatible schema" errors
- Type errors at step boundaries
- Schema validation failures when passing data between steps
- Errors mentioning Zod types not matching
- "Expected ZodObject but received..." errors

## Root Cause

The issue arises when you import `z` from `zod` instead of `@output.ai/core`. Although both provide Zod schemas, they create different schema instances that are incompatible within the Output SDK context. This can lead to runtime validation failures and TypeScript errors.

## Error Messages

You may encounter the following error messages:
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

Check your imports to ensure you are not using `zod` elsewhere:

```bash
grep -r "import.*zod" src/
```

All matches should show `@output.ai/core`, not `zod`.

## Example

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
    // ...
  }
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
    // ...
  }
});
```