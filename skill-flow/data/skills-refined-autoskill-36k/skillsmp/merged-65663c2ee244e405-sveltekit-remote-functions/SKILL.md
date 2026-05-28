---
name: sveltekit-remote-functions
description: SvelteKit remote functions guidance. Use for command(), query(), form() patterns in .remote.ts files.
---

# SvelteKit Remote Functions

## Quick Start

**File naming:** `*.remote.ts` for remote function files.

**Which function?** One-time action → `command()` | Repeated reads → `query()` | Forms → `form()`.

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

- Remote functions execute on server when called from browser.
- Args/returns must be JSON-serializable.
- Schema validation via StandardSchemaV1 (Valibot/Zod).
- `getRequestEvent()` available for cookies/headers access.
- **Queries are cached** - use `.refresh()` to get fresh data.
- **No .remote files in `src/lib/server/`** - they won't work there.
- **Last verified:** 2025-12-19.