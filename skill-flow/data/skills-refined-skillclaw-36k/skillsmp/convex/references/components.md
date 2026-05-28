# Convex Components Cheat Sheet

Components are NPM packages that bundle tables + functions in a sandbox. You:

1. Install via `npm install @convex-dev/<component>`
2. Add to `convex/convex.config.ts` with `app.use(...)`
3. Expose API through your own `convex/*.ts` file
4. Use the generated functions via `components.<name>...` references from `./_generated/api`

## CRITICAL: Querying Component Tables

**Component tables are NOT in your main database namespace.** You cannot use `ctx.db.query('componentTable')`.

**WRONG:**
```ts
// This will fail with "Index not found" error!
const user = await (ctx.db as any)
  .query('user')
  .withIndex('email', (q) => q.eq('email', email))
  .first();
```

**CORRECT:**
```ts
import { components } from './_generated/api';

// Inside a mutation or action (which have ctx.runQuery):
const user = await ctx.runQuery(
  components.betterAuth.adapter.findOne,
  {
    model: 'user',
    where: [{ field: 'email', operator: 'eq', value: email }],
  }
);

// For getting by ID:
const org = await ctx.runQuery(
  components.betterAuth.adapter.findOne,
  {
    model: 'organization',
    where: [{ field: '_id', operator: 'eq', value: orgId }],
  }
);

// For membership queries (Better Auth specific):
const memberships = await ctx.runQuery(
  components.betterAuth.membership.listByUserId,
  { userId: userId }
);
```

**Key points:**
- `ctx.runQuery` is only available in mutations and actions, NOT in queries
- For code that needs to run in both contexts, create an internalMutation wrapper
- Component adapter functions vary by component - check the component's API

---

## Presence Component (`@convex-dev/presence`)

Use-case: live, real-time list of users in a room.

**convex/convex.config.ts**

```ts
import { defineApp } from "convex/server";
import presence from "@convex-dev/presence/convex.config";

const app = defineApp();
app.use(presence);
export default app;
```

**convex/presence.ts**

```ts
import { mutation, query } from "./_generated/server";
import { components } from "./_generated/api";
import { v } from "convex/values";
import { Presence } from "@convex-dev/presence";
import { getAuthUserId } from "@convex-dev/auth/server";
import type { Id } from "./_generated/dataModel";

export const presence = new Presence(components.presence);

export const getUserId = query({
  args: {},
  handler: async (ctx) => {
    return await getAuthUserId(ctx);
  },
});

export const heartbeat = mutation({
  args: { roomId: v.string(), userId: v.string(), sessionId: v.string(), interval: v.number() },
  handler: async (ctx, { roomId, userId, sessionId, interval }) => {
    const authUserId = await getAuthUserId(ctx);
    if (!authUserId) throw new Error("Not authenticated");
    return await presence.heartbeat(ctx, roomId, authUserId, sessionId, interval);
  },
});

export const list = query({
  args: { roomToken: v.string() },
  handler: async (ctx, { roomToken }) => {
    const presenceList = await presence.list(ctx, roomToken);
    const listWithUserInfo = await Promise.all(
      presenceList.map(async (entry) => {
        const user = await ctx.db.get(entry.userId as Id<"users">);
        if (!user) return entry;
        return { ...entry, name: user.name, image: user.image };
      }),
    );
    return listWithUserInfo;
  },
});

export const disconnect = mutation({
  args: { sessionToken: v.string() },
  handler: async (ctx, { sessionToken }) => {
    return await presence.disconnect(ctx, sessionToken);
  },
});
```

**React:**

```tsx
import { api } from "../convex/_generated/api";
import usePresence from "@convex-dev/presence/react";
import FacePile from "@convex-dev/presence/facepile";

function PresenceIndicator({ userId }: { userId: string }) {
  const presenceState = usePresence(api.presence, "my-chat-room", userId);
  return <FacePile presenceState={presenceState ?? []} />;
}
```

- Prefer the built-in **`FacePile`** component unless user explicitly requests custom UI
- `usePresence` signature:

```ts
usePresence(
  presenceApiRef, // e.g. api.presence
  roomId: string,
  userId: string,
  interval?: number,
  convexUrl?: string,
): PresenceState[] | undefined;
```

---

## ProseMirror / BlockNote Component (`@convex-dev/prosemirror-sync`)

Use-case: collaborative rich text editing with Tiptap / BlockNote / BlockNote + Convex.

**Install + config:**

```bash
npm install @convex-dev/prosemirror-sync
```

```ts
// convex/convex.config.ts
import { defineApp } from "convex/server";
import prosemirrorSync from "@convex-dev/prosemirror-sync/convex.config";

const app = defineApp();
app.use(prosemirrorSync);
export default app;
```

**Expose sync API:**

```ts
// convex/prosemirror.ts
import { components } from "./_generated/api";
import { ProsemirrorSync } from "@convex-dev/prosemirror-sync";

const prosemirrorSync = new ProsemirrorSync(components.prosemirrorSync);
export const {
  getSnapshot,
  submitSnapshot,
  latestVersion,
  getSteps,
  submitSteps,
} = prosemirrorSync.syncApi({
  // optional permission callbacks here
});
```

**React BlockNote usage:**

```tsx
import { useBlockNoteSync } from "@convex-dev/prosemirror-sync/blocknote";
import { BlockNoteView } from "@blocknote/mantine";
import { BlockNoteEditor } from "@blocknote/core";
import { api } from "../convex/_generated/api";

function MyComponent({ id }: { id: string }) {
  const sync = useBlockNoteSync<BlockNoteEditor>(api.prosemirror, id);
  return sync.isLoading ? (
    <p>Loading...</p>
  ) : sync.editor ? (
    <BlockNoteView editor={sync.editor} />
  ) : (
    <button onClick={() => sync.create({ type: "doc", content: [] })}>
      Create document
    </button>
  );
}

export function MyComponentWrapper({ id }: { id: string }) {
  return <MyComponent key={id} id={id} />;
}
```

Important:
- `sync.create` expects a **`JSONContent` object**, **not a string**
- `JSONContent` type must match Tiptap/ProseMirror schema
- `MyComponentWrapper` with `key={id}` is a workaround to ensure re-init when doc ID changes

---

## Resend Component (`@convex-dev/resend`)

Use-case: robust email sending with queueing, batching, retries, status tracking.

**Install + config:**

```bash
npm install @convex-dev/resend
```

```ts
// convex/convex.config.ts
import { defineApp } from "convex/server";
import resend from "@convex-dev/resend/convex.config";

const app = defineApp();
app.use(resend);
export default app;
```

**Env vars:**
- `RESEND_API_KEY`
- `RESEND_DOMAIN`
- (optional) `RESEND_WEBHOOK_SECRET`

**Basic usage:**

```ts
// convex/sendEmails.ts
import { components } from "./_generated/api";
import { Resend } from "@convex-dev/resend";
import { internalMutation } from "./_generated/server";

export const resend = new Resend(components.resend, {});

export const sendTestEmail = internalMutation({
  args: {},
  handler: async (ctx) => {
    await resend.sendEmail(
      ctx,
      `Me <test@${process.env.RESEND_DOMAIN}>`,
      "Resend <delivered@resend.dev>",
      "Hi there",
      "This is a test email",
    );
  },
});
```

**Webhook handling (`convex/http.ts`):**

```ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";
import { resend } from "./sendEmails";

const http = httpRouter();

http.route({
  path: "/resend-webhook",
  method: "POST",
  handler: httpAction(async (ctx, req) => {
    return await resend.handleResendEventWebhook(ctx, req);
  }),
});

export default http;
```

You must instruct the user to:
- Configure a webhook in the Resend dashboard pointing at `<deployment>.convex.site/resend-webhook`
- Enable `email.*` events
- Set `RESEND_WEBHOOK_SECRET`

**Event handling:**

```ts
import { internalMutation } from "./_generated/server";
import { vEmailId, vEmailEvent, Resend } from "@convex-dev/resend";
import { components, internal } from "./_generated/api";

export const resend = new Resend(components.resend, {
  onEmailEvent: internal.sendEmails.handleEmailEvent,
});

export const handleEmailEvent = internalMutation({
  args: { id: vEmailId, event: vEmailEvent },
  handler: async (ctx, args) => {
    console.log("Email event", args.id, args.event);
    // Update status in your own tables if needed
  },
});
```

`ResendOptions` (constructor) includes:
- `apiKey`, `webhookSecret`
- `testMode` (defaults to **true**; must be set to `false` for real emails)
- `onEmailEvent`
