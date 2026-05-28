---
name: pinpoint-ui
description: Use this skill when building or modifying UI components, creating forms, or working with shadcn/ui components and Tailwind CSS v4.
---

# PinPoint UI Guide

## When to Use This Skill

Use this skill when:
- Building or modifying UI components
- Creating forms
- Working with shadcn/ui components
- Styling with Tailwind CSS v4
- Implementing progressive enhancement
- Deciding between Server and Client Components
- User mentions: "UI", "component", "form", "styling", "Tailwind", "shadcn", "button", "input"

## Quick Reference

### Critical UI Rules
1. **Server Components first**: Default to Server Components, use "use client" only for interactivity.
2. **Progressive enhancement**: Forms must work without JavaScript.
3. **shadcn/ui only**: No MUI components.
4. **Direct Server Action references**: No inline wrappers in forms.
5. **Dropdown Server Actions**: Use `onSelect`, not forms.
6. **Tailwind CSS v4**: Use CSS variables, no hardcoded hex colors.

### Adding Components
```bash
pnpm exec shadcn@latest add [component]
```

## Detailed Documentation

Read these files for comprehensive UI guidance:

```bash
# Primary UI guide - the "Goto" manual for all UI work
cat docs/UI_GUIDE.md

# Specific UI implementation patterns
ls docs/ui-patterns/
cat docs/ui-patterns/*.md
```

## Core UI Patterns

### Server vs Client Components

```typescript
// ✅ Good: Server Component (default)
export default async function MachinesPage() {
  const machines = await getMachines();

  return (
    <div>
      {machines.map((machine) => (
        <MachineCard key={machine.id} machine={machine} />
      ))}
    </div>
  );
}

// ✅ Good: Client Component (only when needed)
"use client";
import { useState } from "react";

export function IssueFilter() {
  const [filter, setFilter] = useState("all");

  return (
    <select value={filter} onChange={(e) => setFilter(e.target.value)}>
      <option value="all">All Issues</option>
      <option value="open">Open</option>
      <option value="resolved">Resolved</option>
    </select>
  );
}
```

### Forms with Progressive Enhancement

```typescript
// ✅ Good: Direct Server Action reference
import { createIssue } from "~/server/actions/issues";

export function CreateIssueForm() {
  return (
    <form action={createIssue}>
      <input name="title" required />
      <textarea name="description" />
      <button type="submit">Create Issue</button>
    </form>
  );
}
```