# File Storage

## Core Ideas

- Store **file IDs** (`Id<"_storage">`) in your tables, not URLs
- Use `_storage` system table + `ctx.storage` methods

## Typical Pattern (Chat App Example)

**Backend:**

```ts
export const list = query({
  args: {},
  handler: async (ctx) => {
    const messages = await ctx.db.query("messages").collect();
    return Promise.all(
      messages.map(async (message) => ({
        ...message,
        ...(message.format === "image"
          ? { url: await ctx.storage.getUrl(message.body) }
          : {}),
      })),
    );
  },
});

export const generateUploadUrl = mutation({
  args: {},
  handler: async (ctx) => {
    return await ctx.storage.generateUploadUrl();
  },
});

export const sendImage = mutation({
  args: { storageId: v.id("_storage"), author: v.string() },
  handler: async (ctx, args) => {
    await ctx.db.insert("messages", {
      body: args.storageId,
      author: args.author,
      format: "image",
    });
  },
});
```

**Client:**

1. Call `generateUploadUrl` to get a signed upload URL
2. `fetch(POST)` the file to that URL
3. Extract `{ storageId }` from JSON
4. Call `sendImage` with `storageId`

## File Metadata

```ts
import { Id } from "./_generated/dataModel";

type FileMetadata = {
  _id: Id<"_storage">;
  _creationTime: number;
  contentType?: string;
  sha256: string;
  size: number;
};

export const exampleQuery = query({
  args: { fileId: v.id("_storage") },
  handler: async (ctx, args) => {
    const metadata: FileMetadata | null = await ctx.db.system.get(args.fileId);
    console.log(metadata);
    return null;
  },
});
```
