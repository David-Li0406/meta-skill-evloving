---
name: sveltekit-remote-functions
description: SvelteKit remote functions guidance. Use for command(), query(), form() patterns in .remote.ts files.
---

# SvelteKit Remote Functions

## Quick Start

**File naming:** `*.remote.ts` for remote function files.

**Which function?** Use `command()` for one-time actions, `query()` for repeated reads, and `form()` for forms.

## Example

```typescript
// actions.remote.ts
import { command } from '$app/server';
import * as v from 'valibot';

export const delete_user = command(
	v.object({ id: v.string() }),
	async ({ id }) => {
		await db.users.delete(id);
		return { success: true };
	},
);

// Call from client: await delete_user({ id: '123' });
```

## Reference Files

- [references/remote-functions.md](references/remote-functions.md) - Complete guide with all patterns.

## Notes

- Remote functions execute on the server when called from the browser.
- Arguments and returns must be JSON-serializable.
- Schema validation is done via StandardSchemaV1 (Valibot/Zod).
- Use `getRequestEvent()` for accessing cookies and headers.
- **Queries are cached**; use `.refresh()` to get fresh data.
- **No .remote files in `src/lib/server/`**; they won't work there.
- **Last verified:** 2025-12-19

<!--
PROGRESSIVE DISCLOSURE GUIDELINES:
- Keep this file ~50 lines total (max ~150 lines)
- Use 1-2 code blocks only (recommend 1)
- Keep description <200 chars for Level 1 efficiency
- Move detailed docs to references/ for Level 3 loading
- This is Level 2 - quick reference ONLY, not a manual

LLM WORKFLOW (when editing this file):
1. Write/edit SKILL.md
2. Format (if formatter available)
3. Run: claude-skills-cli validate <path>
4. If multi-line description warning: run claude-skills-cli doctor <path>
5. Validate again to confirm
-->