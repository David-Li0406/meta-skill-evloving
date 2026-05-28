# React Client Patterns (convex/react)

## Basic Usage

```tsx
import { useQuery, useMutation } from "convex/react";
import { api } from "../convex/_generated/api";

export default function App() {
  const messages = useQuery(api.messages.list) ?? [];

  const sendMessage = useMutation(api.messages.sendMessage);
  const [text, setText] = useState("");

  return (
    <main>
      <ul>
        {messages.map(m => (
          <li key={m._id}>{m.body}</li>
        ))}
      </ul>
      <form
        onSubmit={async e => {
          e.preventDefault();
          if (!text) return;
          await sendMessage({ body: text, author: "User 1234" });
          setText("");
        }}
      >
        <input value={text} onChange={e => setText(e.target.value)} />
        <button disabled={!text}>Send</button>
      </form>
    </main>
  );
}
```

Key points:
- `useQuery()` returns:
  - The query result, or
  - `undefined` while loading / when unsubscribed
- It **live-updates** when data changes

## Never Use Hooks Conditionally

This is a critical pattern.

**Bad:**

```tsx
// ❌ Do not conditionally call useQuery
const avatarUrl = profile?.avatarId
  ? useQuery(api.profiles.getAvatarUrl, { storageId: profile.avatarId })
  : null;
```

**Good:**

```tsx
const avatarUrl = useQuery(
  api.profiles.getAvatarUrl,
  profile?.avatarId ? { storageId: profile.avatarId } : "skip",
);
```

- Use `"skip"` as a special argument to avoid running the query
- This keeps hooks unconditionally called and satisfies React's rules

## Auth-Backed Queries

Given a Convex auth setup like:

```ts
// convex/auth.ts
export const loggedInUser = query({
  args: {},
  handler: async (ctx) => {
    const userId = await getAuthUserId(ctx);
    if (!userId) return null;
    return await ctx.db.get(userId);
  },
});
```

React:

```tsx
const user = useQuery(api.auth.loggedInUser); // user | null | undefined
```
