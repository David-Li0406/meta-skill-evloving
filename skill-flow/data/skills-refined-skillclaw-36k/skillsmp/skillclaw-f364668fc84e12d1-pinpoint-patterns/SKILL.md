---
name: pinpoint-patterns
description: Use this skill when implementing features to follow established project-specific patterns for Server Actions, data fetching, error handling, and file organization.
---

# Skill body

## When to Use This Skill

Use this skill when:
- Implementing new features
- Wondering "how should I structure this?"
- Looking for established patterns to follow
- Contributing new patterns after implementing the same approach 2+ times
- User mentions: "pattern", "convention", "architecture", "how to", "best practice"

## Quick Reference

### Pattern Discovery Process
1. Check `docs/PATTERNS.md` (index of all patterns)
2. Look in `docs/patterns/` for specific pattern files
3. If implementing the same approach 2+ times, add a new pattern
4. Focus on PinPoint-specific patterns (not general Next.js knowledge)

### Core Patterns
- **Server Actions**: File organization, auth, validation, revalidation
- **Data Fetching**: Drizzle queries, caching, error handling
- **Error Handling**: Validation errors, auth errors, DB errors
- **File Organization**: Where to put files, naming conventions

## Detailed Documentation

Read these files for all established patterns:

```bash
# Index of all patterns
cat docs/PATTERNS.md

# Specific pattern files
ls docs/patterns/
cat docs/patterns/*.md

# Example: Data fetching patterns
cat docs/patterns/data-fetching.md
```

## Server Action Patterns

### File Organization

```
src/server/actions/
├── issues.ts       # Issue-related actions
├── machines.ts     # Machine-related actions
├── users.ts        # User-related actions
└── comments.ts     # Comment-related actions
```

### Server Action Template

```typescript
"use server";

import { createClient } from "~/lib/supabase/server";
import { redirect } from "next/navigation";
import { revalidatePath } from "next/cache";
import { z } from "zod";
import { db } from "~/server/db";
import { issues } from "~/server/db/schema";

// 1. Define validation schema
const createIssueSchema = z.object({
  title: z.string().min(1, "Title required"),
  description: z.string().optional(),
  machineId: z.string().uuid(),
  severity: z.enum(["minor", "playable", "unplayable"]),
});

// 2. Define return type
export type CreateIssueResult =
  | { success: true; issueId: string }
  | { success: false; error: string };

// 3. Implement action
export async function createIssue(
  formData: FormData
): Promise<CreateIssueResult> {
  // Implementation goes here
}
```