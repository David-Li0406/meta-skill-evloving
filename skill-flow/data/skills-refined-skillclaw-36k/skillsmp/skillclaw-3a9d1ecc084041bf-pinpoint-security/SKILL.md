---
name: pinpoint-security
description: Use this skill when implementing authentication, handling user input, or setting up security features to ensure robust security practices.
---

# PinPoint Security Guide

## When to Use This Skill

Use this skill when:
- Implementing authentication or authorization
- Creating forms or handling user input
- Setting up security headers (CSP, CORS, etc.)
- Working with Supabase SSR authentication
- User mentions: "security", "auth", "validation", "XSS", "CSRF", "input", "forms"

## Quick Reference

### Critical Security Rules
1. **CSP with nonces**: Dynamic nonces via middleware, static headers via `next.config.ts`.
2. **Validate ALL inputs**: Use Zod for all form data and user inputs.
3. **Supabase SSR contract**: Use `~/lib/supabase/server`, call `auth.getUser()` immediately.
4. **Host consistency**: Use `localhost` for all auth callbacks, dev server, Playwright, Supabase `site_url`.
5. **No logic between** `createClient()` and `getUser()`.

### Common Patterns

**Server Action with Auth**:
```typescript
"use server";
import { createClient } from "~/lib/supabase/server";
import { redirect } from "next/navigation";

export async function protectedAction(formData: FormData) {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser(); // Call immediately!
  if (!user) redirect("/login");

  // Validate inputs
  const schema = z.object({
    title: z.string().min(1),
    description: z.string().optional(),
  });
  const validated = schema.parse({
    title: formData.get("title"),
    description: formData.get("description"),
  });

  // Proceed with validated data
}
```

**Form Validation**:
```typescript
import { z } from "zod";

const createIssueSchema = z.object({
  title: z.string().min(1, "Title required"),
  description: z.string().optional(),
  machineId: z.string().uuid("Invalid machine ID"),
  severity: z.enum(["minor", "playable", "unplayable"]),
});

export async function createIssue(formData: FormData) {
  const rawData = {
    title: formData.get("title"),
    description: formData.get("description"),
    machineId: formData.get("machineId"),
    severity: formData.get("severity"),
  };

  const validData = createIssueSchema.parse(rawData);
  // Use validData safely
}
```

## Detailed Documentation

For comprehensive security guidance, refer to the relevant documentation files.