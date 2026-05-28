---
name: sveltekit-remote-functions
description: Use this skill for guidance on implementing remote functions in SvelteKit using command(), query(), and form() patterns in .remote.ts files.
---

# SvelteKit Remote Functions

## Quick Start

**File naming:** `*.remote.ts` for remote function files.

**Which function?** 
- One-time action → `command()`
- Repeated reads → `query()`
- Forms → `form()`

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

## Notes

- Remote functions execute on the server when called from the browser.
- Arguments and returns must be JSON-serializable.
- Schema validation is done via StandardSchemaV1 (Valibot/Zod).
- `getRequestEvent()` is available for accessing cookies and headers.
- **Queries are cached** - use `.refresh()` to get fresh data.
- **No .remote files in `src/lib/server/`** - they won't work there.
- **Last verified:** 2025-12-19