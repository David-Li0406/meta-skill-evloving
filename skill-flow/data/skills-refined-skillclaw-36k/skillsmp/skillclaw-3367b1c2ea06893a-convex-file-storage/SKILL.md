---
name: convex-file-storage
description: Use this skill when you need to handle file uploads, storage, serving, and management in Convex applications.
---

# Skill body

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: [Convex File Storage Documentation](https://docs.convex.dev/file-storage)
- Upload Files: [Upload Files Documentation](https://docs.convex.dev/file-storage/upload-files)
- Serve Files: [Serve Files Documentation](https://docs.convex.dev/file-storage/serve-files)
- For broader context: [LLMS Documentation](https://docs.convex.dev/llms.txt)

## Instructions

### File Storage Overview

Convex provides built-in file storage with:
- Automatic URL generation for serving files
- Support for any file type (images, PDFs, videos, etc.)
- File metadata via the `_storage` system table
- Integration with mutations and actions

### Generating Upload URLs

```typescript
// convex/files.ts
import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const generateUploadUrl = mutation({
  args: {},
  returns: v.string(),
  handler: async (ctx) => {
    return await ctx.storage.generateUploadUrl();
  },
});
```

### Client-Side Upload

```typescript
// React component
import { useMutation } from "convex/react";
import { api } from "../convex/_generated/api";
import { useState } from "react";

function FileUploader() {
  const generateUploadUrl = useMutation(api.files.generateUploadUrl);
  const saveFile = useMutation(api.files.saveFile);
  const [uploading, setUploading] = useState(false);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    try {
      // Step 1: Get upload URL
      const uploadUrl = await generateUploadUrl();

      // Step 2: Upload file to storage
      const result = await fetch(uploadUrl, {
        method: "POST",
        headers: { "Content-Type": file.type },
        body: file,
      });

      const { storageId } = await result.json();

      // Step 3: Save file reference to database
      await saveFile({
        storageId,
        fileName: file.name,
        fileType: file.type,
        fileSize: file.size,
      });
    } finally {
      setUploading(false);
    }
  };

  return (
    <input type="file" onChange={handleUpload} disabled={uploading} />
  );
}
```