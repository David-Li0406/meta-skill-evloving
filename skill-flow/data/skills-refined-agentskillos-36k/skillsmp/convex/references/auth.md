# Auth Patterns (Convex Auth)

## Common Server Pattern

```ts
import { getAuthUserId } from "@convex-dev/auth/server";

export const currentLoggedInUser = query({
  args: {},
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) return null;

    const user = await ctx.db.get(userId);
    if (!user) return null;

    return user;
  },
});
```

## Important Notes

- You can only call `getAuthUserId` inside `convex/` functions (query/mutation/internal*)
- Scheduled jobs do **not** carry auth context – `getAuthUserId` returns `null` there
